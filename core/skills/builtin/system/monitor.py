from __future__ import annotations

from skills.base import Skill
from models import Task, AgentResult, SessionContext


class SystemMonitorSkill(Skill):
    name = "system"
    description = "System operations: automation, monitoring, optimization"
    version = "1.0.0"
    category = "system"
    ram_usage_mb = 50
    cpu_intensity = "low"
    network_required = False
    supported_tasks = [
        "run_automation", "monitor_system", "clean_temp_files",
        "optimize_performance", "manage_processes"
    ]
    required_tools = ["shell"]

    def can_handle(self, task: Task) -> float:
        if any(t in task.description.lower() for t in self.supported_tasks):
            return 0.85
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        self.use_count += 1
        return AgentResult(
            success=True,
            output={"message": f"Executed system skill: {task.description}"}
        )

    def _on_load(self):
        pass

    def _on_unload(self):
        pass
