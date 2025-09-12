from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

class LLM():
    def __init__(self)->None:
        self.model = ChatGroq(api_key=SecretStr(os.getenv('GROQ_API_KEY','')),model='llama-3.3-70b-versatile')