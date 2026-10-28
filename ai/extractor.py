from datetime import date, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .prompts import TASK_EXTRACTION_SYSTEM
from models.task import Task

class ExtractedTask(BaseModel):
    name: str
    description: str = ""
    deadline: Optional[date] = None
    estimated_hours: float = Field(default=1.0, gt=0, le=100)
    importance: float = Field(default=50, ge=0, le=100)
    difficulty: float = Field(default=50, ge=0, le=100)
    category: str = "Other"
    dependencies: List[str] = []

class ExtractedTasks(BaseModel):
    tasks: List[ExtractedTask]

def extract_tasks(text: str) -> List[Task]:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(ExtractedTasks)
    prompt = ChatPromptTemplate.from_messages([
        ("system", TASK_EXTRACTION_SYSTEM),
        ("human", "{text}")
    ])
    chain = prompt | structured_llm
    result = chain.invoke({"text": text})
    if not result.tasks:
        raise ValueError("No tasks were extracted.")
    return [Task(**t.model_dump()) for t in result.tasks]
