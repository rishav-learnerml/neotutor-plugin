from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.llm.llm import LLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import os

class RAG():
    def __init__(self,transcript:str="",vector_store=None)->None:
        self.transcript=transcript
        self.splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        self.vector_store=vector_store

    def _format_docs(self,retrieved_docs)->str:
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
            return context_text


    def index_documents(self) -> None:
        if(self.transcript is None):
             print("No tarnscript available - unable to create index")
             return None
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
            print("Vector Store is empty - Unable to process query!")
            return None
        
        try:
            parser = StrOutputParser()
            
            retriever = self.vector_store.as_retriever(search_type='similarity',search_kwargs={'k':4})

            # define llm model and prompt template
            llm = LLM()
            model = llm.model

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
            parallel_chain = RunnableParallel({
                 'context':retriever | RunnableLambda(self._format_docs),
                 'query':RunnablePassthrough()
            })

            ## Generate

            main_chain = parallel_chain | prompt | model | parser

            answer = main_chain.invoke(query)

            return answer
        
        except Exception as e:
            print("Unable to resolve query",e)












    








