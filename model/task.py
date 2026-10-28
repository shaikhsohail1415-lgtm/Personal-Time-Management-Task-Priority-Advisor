from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class Task(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    deadline: Optional[date] = None
    estimated_hours: float = Field(gt=0, le=100)
    importance: float = Field(ge=0, le=100)
    difficulty: float = Field(ge=0, le=100)
    category: str = "Other"
    dependencies: List[str] = Field(default_factory=list)

class TaskAnalysis(BaseModel):
    task: Task
    urgency: float
    time_pressure: float
    priority_score: float
    priority_level: str
    membership_values: Dict[str, Dict[str, float]]
    activated_rules: List[Dict[str, Any]]
    aggregated_output: Dict[str, List[float]]
