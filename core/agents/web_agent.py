from __future__ import annotations

from agents.base import BaseAgent
from models import Task, SessionContext, AgentResult
from utils.logger import logger


class WebAgent(BaseAgent):
    name = "web_agent"
    description = "Web automation agent - scraping, monitoring, research"
    version = "1.0.0"
    required_skills = ["web"]
    ram_budget_mb = 60

    async def can_handle(self, task: Task) -> float:
        web_keywords = ["scrape", "web", "search", "url", "monitor", "research", "crawl", "download"]
        if any(kw in task.description.lower() for kw in web_keywords):
            return 0.9
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        await self.pre_execute()
        try:
            logger.info("web_agent.execute", task_id=task.id, description=task.description)
            return AgentResult(
                success=True,
                output={
                    "message": f"Web task completed: {task.description}",
                    "source": "web"
                }
            )
        except Exception as e:
            logger.error("web_agent.error", error=str(e))
            return AgentResult(success=False, error=str(e))
        finally:
            await self.post_execute()
