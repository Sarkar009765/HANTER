from pydantic import BaseModel
from typing import Optional, Any, Dict


class MemoryModel(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = {}
    score: Optional[float] = None
