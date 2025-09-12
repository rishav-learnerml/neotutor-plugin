from src.llm.llm import LLM
from langchain.prompts import PromptTemplate
from src.schema.enhance_query_schema import EnhanceQuerySchema
from langchain_core.output_parsers import PydanticOutputParser

def enhance_query(query):
    model = LLM().model
    parser=PydanticOutputParser(pydantic_object=EnhanceQuerySchema)

    prompt = PromptTemplate(
        template="""
            You are a query re-writing expert who understands the user query and generates four
            different queries based on the semantic meaning of the original user query. You have to give back 4 different queries in the specified format by clearly expressing
            them in meaningful questions.\n
            Query: {query}\n\n
            {format_instructions}
        """,
        input_variables=['query'],
        partial_variables={'format_instructions':parser.get_format_instructions()}
        )

    chain = prompt | model | parser

    enhanced_queries = chain.invoke({'query':query})

    return enhanced_queries

    