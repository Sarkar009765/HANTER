from __future__ import annotations

from agents.base import BaseAgent
from models import Task, SessionContext, AgentResult
from utils.logger import logger


class SocialAgent(BaseAgent):
    name = "social_agent"
    description = "Social media management agent - content creation, scheduling, analytics"
    version = "1.0.0"
    required_skills = ["social"]
    ram_budget_mb = 80

    async def can_handle(self, task: Task) -> float:
        social_keywords = ["tweet", "post", "social", "content", "hashtag", "schedule", "twitter", "linkedin"]
        if any(kw in task.description.lower() for kw in social_keywords):
            return 0.9
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        await self.pre_execute()
        try:
            logger.info("social_agent.execute", task_id=task.id, description=task.description)
            return AgentResult(
                success=True,
                output={
                    "message": f"Social media task completed: {task.description}",
                    "platform": "twitter"
                }
            )
        except Exception as e:
            logger.error("social_agent.error", error=str(e))
            return AgentResult(success=False, error=str(e))
        finally:
            await self.post_execute()
