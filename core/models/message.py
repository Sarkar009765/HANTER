from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    agent_name: Optional[str] = None
    skill_used: Optional[str] = None
    tokens_used: Optional[int] = None
    latency_ms: Optional[int] = None
