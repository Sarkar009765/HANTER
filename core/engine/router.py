from __future__ import annotations

from typing import Optional, Dict
from models import Task, TaskType, AgentStatus, SessionContext
from agents.registry import AgentRegistry
from agents.base import BaseAgent


class AgentRouter:
    def __init__(self):
        self._routes: Dict[TaskType, str] = {
            TaskType.CODE: "dev_agent",
            TaskType.SOCIAL: "social_agent",
            TaskType.WEB: "web_agent",
            TaskType.FILE: "file_agent",
            TaskType.SYSTEM: "sys_agent",
        }

    async def select_agent(
        self,
        task_def: dict,
        registry: AgentRegistry,
        context: SessionContext
    ) -> Optional[str]:
        explicit_agent = task_def.get("agent")
        if explicit_agent:
            return explicit_agent

        task_type_str = task_def.get("type", "general")
        try:
            task_type = TaskType(task_type_str)
            return self._routes.get(task_type)
        except ValueError:
            return "dev_agent"

    async def find_best_agent(
        self, task: Task, available_agents: Dict[str, BaseAgent]
    ) -> Optional[tuple[str, BaseAgent]]:
        scores = []
        for name, agent in available_agents.items():
            capability = await agent.can_handle(task)
            status = await agent.get_status()
            availability = 1.0 if status == AgentStatus.IDLE else 0.5 if status == AgentStatus.STANDBY else 0.0
            score = (capability * 0.5) + (availability * 0.3) + (0.2)
            scores.append((name, agent, score))

        if not scores:
            return None
        best = max(scores, key=lambda x: x[2])
        return (best[0], best[1])
