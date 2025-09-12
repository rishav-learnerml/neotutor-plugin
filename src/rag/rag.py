from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from src.llm.llm import LLM
from langchain.prompts import PromptTemplate
import os

class RAG():
    def __init__(self,transcript:str)->None:
        self.transcript=transcript
        self.splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        self.vector_store=None

    def index_documents(self) -> None:
        ## Chunk / split the txt file
        chunks=self.splitter.create_documents([self.transcript])

        ## Create embeddings

        embedding_model = HuggingFaceEmbeddings(model_name=os.getenv('HUGGINGFACE_EMBEDDING_MODEL','sentence-transformers/all-MiniLM-L6-v2'))

        ## Store in a vector store
        vector_store=FAISS.from_documents(chunks,embedding_model)

        self.vector_store = vector_store
    
    def generate_answer(self,query)->str | None:
        ## define a retriever
        if(self.vector_store is None):
            return None
        
        try:
            
            retriever = self.vector_store.as_retriever(search_type='similarity',search_kwargs={'k':4})

            ## get top-k chunks --> retrieve
            docs = retriever.invoke(query) #list of docs

            # define llm model and prompt template
            llm = LLM()

            prompt = PromptTemplate(
                template="""
                    You are a helpful assistant.
                    Answer ONLY from the provided transcript context,
                    If the context is insufficient, just say you don't know.
                    Do not make assumtions and strictly answer following the centext.

                    {context}\n
                    Question: {query}
                """,
                input_variables=['context','query']
            )

            # augment
            context_text = "\n\n".join(doc.page_content for doc in docs)
            final_prompt = prompt.invoke({
                'context':context_text,
                'query':query
            })

            ## Generate

            response = llm.model.invoke(final_prompt)

            return str(response.content)
        
        except Exception as e:
            print("Unable to resolve query",e)












    








