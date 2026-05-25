from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from models import Task, SessionContext, AgentResult, AgentStatus


class BaseAgent(ABC):
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    required_skills: List[str] = []
    ram_budget_mb: int = 50
    _status: AgentStatus = AgentStatus.IDLE

    @abstractmethod
    async def can_handle(self, task: Task) -> float:
        pass

    @abstractmethod
    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        pass

    async def get_status(self) -> AgentStatus:
        return self._status

    async def pre_execute(self):
        self._status = AgentStatus.BUSY

    async def post_execute(self):
        self._status = AgentStatus.IDLE
