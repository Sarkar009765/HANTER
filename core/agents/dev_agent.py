from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path
from agents.base import BaseAgent
from models import Task, SessionContext, AgentResult, TaskType
from utils.logger import logger
from utils.validators import validate_command


class DevAgent(BaseAgent):
    name = "dev_agent"
    description = "Full-stack development agent - code generation, debugging, deployment"
    version = "1.0.0"
    required_skills = ["dev"]
    ram_budget_mb = 100

    async def can_handle(self, task: Task) -> float:
        code_keywords = ["code", "build", "deploy", "react", "python", "app", "website", "git", "npm"]
        if any(kw in task.description.lower() for kw in code_keywords):
            return 0.9
        return 0.2

    async def execute(self, task: Task, context: SessionContext) -> AgentResult:
        await self.pre_execute()
        try:
            logger.info("dev_agent.execute", task_id=task.id, description=task.description)

            if "deploy" in task.description.lower():
                return await self._handle_deploy(task)
            elif "scaffold" in task.description.lower() or "create" in task.description.lower():
                return await self._handle_scaffold(task)
            elif "git" in task.description.lower():
                return await self._handle_git(task)
            else:
                return AgentResult(
                    success=True,
                    output={
                        "message": f"Executed development task: {task.description}",
                        "task_type": task.type.value
                    }
                )
        except Exception as e:
            logger.error("dev_agent.error", error=str(e))
            return AgentResult(success=False, error=str(e))
        finally:
            await self.post_execute()

    async def _handle_deploy(self, task: Task) -> AgentResult:
        project_path = task.input_data.get("project_path", ".")
        platform = task.input_data.get("platform", "vercel")
        command = f"npx {platform} --prod" if platform == "vercel" else f"npx netlify deploy --prod"
        valid, msg = validate_command(command)
        if not valid:
            return AgentResult(success=False, error=msg)
        proc = await asyncio.create_subprocess_shell(
            command, cwd=project_path,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            return AgentResult(success=True, output={"message": f"Deployed to {platform}", "stdout": stdout.decode()})
        return AgentResult(success=False, error=stderr.decode())

    async def _handle_scaffold(self, task: Task) -> AgentResult:
        return AgentResult(success=True, output={"message": f"Scaffolding: {task.description}"})

    async def _handle_git(self, task: Task) -> AgentResult:
        return AgentResult(success=True, output={"message": f"Git operation: {task.description}"})
