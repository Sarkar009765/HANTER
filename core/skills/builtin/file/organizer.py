from __future__ import annotations

from skills.base import Skill
from models import Task, AgentResult, SessionContext


class FileOrganizerSkill(Skill):
    name = "file"
    description = "File operations: organize, search, convert, sync"
    version = "1.0.0"
    category = "file"
    ram_usage_mb = 40
    cpu_intensity = "low"
    network_required = False
    supported_tasks = [
        "organize_folder", "search_files", "convert_format",
        "compress_files", "sync_folder", "clean_duplicates"
    ]
    required_tools = ["file_system"]

    def can_handle(self, task: Task) -> float:
        if any(t in task.description.lower() for t in self.supported_tasks):
            return 0.85
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        self.use_count += 1
        return AgentResult(
            success=True,
            output={"message": f"Executed file skill: {task.description}"}
        )

    def _on_load(self):
        pass

    def _on_unload(self):
        pass
