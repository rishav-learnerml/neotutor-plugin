from src.utils.enhance_query import enhance_query
from src.rag.rag import RAG
from src.schema.enhance_query_schema import EnhanceQuerySchema
from src.llm.llm import LLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_polished_answer(vector_store,query):

    rag=RAG(vector_store=vector_store)

    if(rag.vector_store is None):
        print('Vectore Store is Empty!')
        return None
    
    get_enhanced_questions : EnhanceQuerySchema =enhance_query(query)

    
    answer1 = rag.generate_answer(get_enhanced_questions.question1)
    answer2 = rag.generate_answer(get_enhanced_questions.question2)
    answer3 = rag.generate_answer(get_enhanced_questions.question3)
    answer4 = rag.generate_answer(get_enhanced_questions.question4)

    llm = LLM()
    model=llm.model

    parser = StrOutputParser()

    prompt=PromptTemplate(
        template="""
        You are a helpful AI Assistant and a answer re-writing expert, given the 4 versions of answers, you have to give a helpful final answer which is human like and maintains a professional tone.
        \n
        Answer1: {answer1}\n
        Answer2: {answer2}\n
        Answer3: {answer3}\n
        Answer4: {answer4}\n
        """,
        input_variables=['answer1','answer2','answer3','answer4']
    )

    chain = prompt | model | parser

    context_dict = {'answer1':answer1,'answer2':answer2,'answer3':answer3,'answer4':answer4}

    final_answer = chain.invoke(context_dict)

    return final_answer



    
