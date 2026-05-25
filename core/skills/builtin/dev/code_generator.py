from __future__ import annotations

from skills.base import Skill
from models import Task, AgentResult, SessionContext


class CodeGeneratorSkill(Skill):
    name = "dev"
    description = "Full-stack development: code generation, debugging, deployment"
    version = "1.0.0"
    category = "dev"
    ram_usage_mb = 100
    cpu_intensity = "medium"
    network_required = True
    supported_tasks = [
        "generate_code", "debug", "refactor", "scaffold_project",
        "git_commit", "git_push", "deploy_vercel", "deploy_netlify",
        "run_tests", "fix_lint"
    ]
    required_tools = ["shell", "file_system", "api_client"]

    def can_handle(self, task: Task) -> float:
        if any(t in task.description.lower() for t in self.supported_tasks):
            return 0.85
        return 0.1

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        self.use_count += 1
        return AgentResult(
            success=True,
            output={"message": f"Executed dev skill: {task.description}"}
        )

    def _on_load(self):
        pass

    def _on_unload(self):
        pass
