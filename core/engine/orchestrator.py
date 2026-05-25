from __future__ import annotations

import asyncio
import time
from uuid import uuid4
from typing import Dict, Optional, List
from datetime import datetime

from models import (
    IntentClassification, IntentType, ExecutionResult,
    Task, TaskTree, TaskStatus, TaskType, SessionContext
)
from engine.planner import TaskPlanner
from engine.router import AgentRouter
from engine.context_manager import ContextManager
from agents.registry import AgentRegistry
from skills.registry import SkillRegistry
from memory.manager import MemoryManager
from llm.client import LLMClient
from utils.logger import logger
from utils.validators import validate_command


class Orchestrator:
    def __init__(self):
        self.planner = TaskPlanner()
        self.agent_router = AgentRouter()
        self.context_manager = ContextManager()
        self.agent_registry = AgentRegistry()
        self.skill_registry = SkillRegistry()
        self.memory_manager = MemoryManager()
        self.llm_client = LLMClient()
        self._active_tasks: Dict[str, asyncio.Task] = {}
        self._task_results: Dict[str, Dict] = {}

    async def process(self, user_input: str, session_id: str) -> ExecutionResult:
        start_time = time.time()
        logger.info("orchestrator.process", session_id=session_id, input=user_input[:100])

        context = await self.context_manager.get_context(session_id)
        intent = await self.classify_intent(user_input)

        if intent.intent == IntentType.CLARIFICATION_NEEDED and intent.clarifying_question:
            return ExecutionResult(
                response=intent.clarifying_question,
                total_time_ms=round((time.time() - start_time) * 1000)
            )

        task_tree = await self.planner.decompose(
            user_input, intent, context
        )

        assigned_tasks = []
        for task_def in task_tree.tasks:
            agent_name = await self.agent_router.select_agent(
                task_def, self.agent_registry, context
            )
            task = Task(
                id=task_def.get("id", str(uuid4())),
                type=TaskType(task_def.get("type", "general")),
                description=task_def.get("description", ""),
                agent=agent_name,
                dependencies=task_def.get("dependencies", []),
                priority=task_def.get("priority", 5),
                timeout_seconds=task_def.get("estimated_time_seconds", 300),
            )
            assigned_tasks.append(task)

        response_parts = []
        completed = 0
        failed = 0

        for task in assigned_tasks:
            if task.dependencies:
                await self._wait_for_dependencies(task, assigned_tasks)

            result = await self._execute_task(task, session_id, context)
            if result.success:
                completed += 1
                if result.output:
                    response_parts.append(str(result.output.get("message", "")))
            else:
                failed += 1
                response_parts.append(f"Failed: {result.error}")

        response = " ".join(response_parts) if response_parts else task_tree.explanation

        await self.memory_manager.store_conversation(
            session_id, user_input, response
        )

        total_time = round((time.time() - start_time) * 1000)
        return ExecutionResult(
            response=response,
            tasks_completed=completed,
            tasks_failed=failed,
            total_time_ms=total_time,
            plan=TaskTree(
                tasks=assigned_tasks,
                explanation=task_tree.explanation
            )
        )

    async def classify_intent(self, text: str) -> IntentClassification:
        return await self.llm_client.classify_intent(text)

    async def cancel_task(self, task_id: str):
        if task_id in self._active_tasks:
            self._active_tasks[task_id].cancel()
            del self._active_tasks[task_id]
            logger.info("task_cancelled", task_id=task_id)

    async def _execute_task(
        self, task: Task, session_id: str, context: SessionContext
    ) -> dict:
        agent = self.agent_registry.get_agent(task.agent)
        if not agent:
            return {"success": False, "error": f"Agent '{task.agent}' not found"}

        loop = asyncio.get_event_loop()
        exec_task = loop.create_task(
            agent.execute(task, context)
        )
        self._active_tasks[task.id] = exec_task

        try:
            result = await asyncio.wait_for(
                exec_task, timeout=task.timeout_seconds
            )
            return result

        except asyncio.TimeoutError:
            exec_task.cancel()
            logger.warning("task_timeout", task_id=task.id, agent=task.agent)
            return {"success": False, "error": "Task timed out"}
        except Exception as e:
            logger.error("task_error", task_id=task.id, error=str(e))
            return {"success": False, "error": str(e)}
        finally:
            if task.id in self._active_tasks:
                del self._active_tasks[task.id]

    async def _wait_for_dependencies(
        self, task: Task, all_tasks: List[Task]
    ):
        for dep_id in task.dependencies:
            dep_task = next((t for t in all_tasks if t.id == dep_id), None)
            if dep_task and dep_task.status != TaskStatus.COMPLETED:
                await asyncio.sleep(0.5)
