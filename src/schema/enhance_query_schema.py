from pydantic import BaseModel,Field

class EnhanceQuerySchema(BaseModel):
    question1:str = Field('First enhanced query')
    question2:str = Field('Second enhanced query')
    question3:str = Field('Third enhanced query')
    question4:str = Field('Fourth enhanced query')