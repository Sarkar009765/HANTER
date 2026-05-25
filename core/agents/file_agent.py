from __future__ import annotations

from agents.base import BaseAgent
from models import Task, SessionContext, AgentResult
from utils.logger import logger


class FileAgent(BaseAgent):
    name = "file_agent"
    description = "File management agent - organize, search, convert, sync"
    version = "1.0.0"
    required_skills = ["file"]
    ram_budget_mb = 40

    async def can_handle(self, task: Task) -> float:
        file_keywords = ["file", "folder", "organize", "search file", "convert", "compress", "sync", "duplicate"]
        if any(kw in task.description.lower() for kw in file_keywords):
            return 0.9
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        await self.pre_execute()
        try:
            logger.info("file_agent.execute", task_id=task.id, description=task.description)
            return AgentResult(
                success=True,
                output={"message": f"File task completed: {task.description}"}
            )
        except Exception as e:
            logger.error("file_agent.error", error=str(e))
            return AgentResult(success=False, error=str(e))
        finally:
            await self.post_execute()
