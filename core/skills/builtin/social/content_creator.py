from __future__ import annotations

from skills.base import Skill
from models import Task, AgentResult, SessionContext


class ContentCreatorSkill(Skill):
    name = "social"
    description = "Social media management: content creation, scheduling, analytics"
    version = "1.0.0"
    category = "social"
    ram_usage_mb = 80
    cpu_intensity = "low"
    network_required = True
    supported_tasks = [
        "create_tweet", "create_post", "schedule_content",
        "analyze_engagement", "reply_mentions", "generate_hashtags"
    ]
    required_tools = ["api_client"]

    def can_handle(self, task: Task) -> float:
        if any(t in task.description.lower() for t in self.supported_tasks):
            return 0.85
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        self.use_count += 1
        return AgentResult(
            success=True,
            output={"message": f"Executed social skill: {task.description}"}
        )

    def _on_load(self):
        pass

    def _on_unload(self):
        pass
