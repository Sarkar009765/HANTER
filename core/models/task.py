from __future__ import annotations

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    type: str
    description: str
    agent: str | None = None
    dependencies: list[str] = []
    priority: int = 5
    status: str = "pending"
    input_data: dict = {}
    output_data: dict | None = None
    max_retries: int = 3
    timeout_seconds: int = 300
    ram_required_mb: int = 50
    error_message: str | None = None
