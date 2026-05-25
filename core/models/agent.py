from pydantic import BaseModel
from typing import Optional


class AgentModel(BaseModel):
    name: str
    description: str
    version: str
    status: str = "idle"
    ram_budget_mb: int
    current_task: Optional[str] = None
    skills_loaded: list[str] = []
