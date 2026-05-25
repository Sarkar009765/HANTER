from __future__ import annotations

from agents.base import BaseAgent
from models import Task, SessionContext, AgentResult
from utils.logger import logger


class SysAgent(BaseAgent):
    name = "sys_agent"
    description = "System automation agent - maintenance, monitoring, optimization"
    version = "1.0.0"
    required_skills = ["system"]
    ram_budget_mb = 50

    async def can_handle(self, task: Task) -> float:
        sys_keywords = ["system", "cpu", "ram", "monitor", "process", "clean", "optimize", "automation"]
        if any(kw in task.description.lower() for kw in sys_keywords):
            return 0.9
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        await self.pre_execute()
        try:
            logger.info("sys_agent.execute", task_id=task.id, description=task.description)
            return AgentResult(
                success=True,
                output={"message": f"System task completed: {task.description}"}
            )
        except Exception as e:
            logger.error("sys_agent.error", error=str(e))
            return AgentResult(success=False, error=str(e))
        finally:
            await self.post_execute()
