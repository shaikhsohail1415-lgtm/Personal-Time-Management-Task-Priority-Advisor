from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .prompts import TASK_EXTRACTION_SYSTEM, EXPLANATION_SYSTEM

def build_extraction_chain():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", TASK_EXTRACTION_SYSTEM),
        ("human", "{text}")
    ])
    return prompt | llm

def build_explanation_chain():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXPLANATION_SYSTEM),
        ("human", "{results}")
    ])
    return prompt | llm
