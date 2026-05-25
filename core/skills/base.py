from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import gc
from models import Task, AgentResult, SessionContext


class Skill(ABC):
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    category: str = ""
    author: str = "HANTER Team"
    ram_usage_mb: int = 50
    cpu_intensity: str = "low"
    network_required: bool = False
    supported_tasks: List[str] = []
    required_tools: List[str] = []
    is_loaded: bool = False
    load_time: Optional[datetime] = None
    last_used: Optional[datetime] = None
    use_count: int = 0

    def load(self):
        if not self.is_loaded:
            self._on_load()
            self.is_loaded = True
            self.load_time = datetime.now()

    def unload(self):
        if self.is_loaded:
            self._on_unload()
            self.is_loaded = False
            gc.collect()

    @abstractmethod
    def can_handle(self, task: Task) -> float:
        pass

    @abstractmethod
    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        pass

    def _on_load(self):
        pass

    def _on_unload(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "ram_usage_mb": self.ram_usage_mb,
            "cpu_intensity": self.cpu_intensity,
            "network_required": self.network_required,
            "supported_tasks": self.supported_tasks,
            "is_loaded": self.is_loaded,
            "use_count": self.use_count,
        }
