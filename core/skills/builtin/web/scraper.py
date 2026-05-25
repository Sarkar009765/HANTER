from __future__ import annotations

from skills.base import Skill
from models import Task, AgentResult, SessionContext


class WebScraperSkill(Skill):
    name = "web"
    description = "Web automation: scraping, monitoring, research"
    version = "1.0.0"
    category = "web"
    ram_usage_mb = 60
    cpu_intensity = "medium"
    network_required = True
    supported_tasks = [
        "scrape_page", "monitor_url", "search_web",
        "summarize_article", "download_file", "check_broken_links"
    ]
    required_tools = ["browser", "api_client"]

    def can_handle(self, task: Task) -> float:
        if any(t in task.description.lower() for t in self.supported_tasks):
            return 0.85
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        self.use_count += 1
        return AgentResult(
            success=True,
            output={"message": f"Executed web skill: {task.description}"}
        )

    def _on_load(self):
        pass

    def _on_unload(self):
        pass
