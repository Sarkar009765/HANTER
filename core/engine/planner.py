from __future__ import annotations

from typing import Dict, Any, List
from models import IntentClassification, IntentType, SessionContext


class TaskPlanner:
    def __init__(self):
        self._decomposition_templates: Dict[IntentType, List[Dict]] = {
            IntentType.CODE_GENERATION: [
                {"id": "task_scaffold", "description": "Set up project structure", "agent": "dev_agent", "dependencies": [], "estimated_time_seconds": 30},
                {"id": "task_generate", "description": "Generate source code", "agent": "dev_agent", "dependencies": ["task_scaffold"], "estimated_time_seconds": 60},
                {"id": "task_install", "description": "Install dependencies", "agent": "dev_agent", "dependencies": ["task_generate"], "estimated_time_seconds": 120},
            ],
            IntentType.PROJECT_SCAFFOLD: [
                {"id": "task_scaffold", "description": "Scaffold project with template", "agent": "dev_agent", "dependencies": [], "estimated_time_seconds": 30},
                {"id": "task_init_git", "description": "Initialize git repository", "agent": "dev_agent", "dependencies": ["task_scaffold"], "estimated_time_seconds": 10},
            ],
            IntentType.DEPLOYMENT: [
                {"id": "task_build", "description": "Build project for production", "agent": "dev_agent", "dependencies": [], "estimated_time_seconds": 60},
                {"id": "task_deploy", "description": "Deploy to hosting platform", "agent": "dev_agent", "dependencies": ["task_build"], "estimated_time_seconds": 120},
            ],
            IntentType.SOCIAL_MEDIA: [
                {"id": "task_content", "description": "Generate social media content", "agent": "social_agent", "dependencies": [], "estimated_time_seconds": 30},
                {"id": "task_schedule", "description": "Schedule or publish post", "agent": "social_agent", "dependencies": ["task_content"], "estimated_time_seconds": 30},
            ],
            IntentType.WEB_RESEARCH: [
                {"id": "task_search", "description": "Search for information", "agent": "web_agent", "dependencies": [], "estimated_time_seconds": 30},
                {"id": "task_summarize", "description": "Summarize findings", "agent": "web_agent", "dependencies": ["task_search"], "estimated_time_seconds": 30},
            ],
            IntentType.FILE_ORGANIZATION: [
                {"id": "task_scan", "description": "Scan directory", "agent": "file_agent", "dependencies": [], "estimated_time_seconds": 15},
                {"id": "task_organize", "description": "Organize files", "agent": "file_agent", "dependencies": ["task_scan"], "estimated_time_seconds": 30},
            ],
            IntentType.SYSTEM_AUTOMATION: [
                {"id": "task_analyze", "description": "Analyze system state", "agent": "sys_agent", "dependencies": [], "estimated_time_seconds": 15},
                {"id": "task_execute", "description": "Execute automation", "agent": "sys_agent", "dependencies": ["task_analyze"], "estimated_time_seconds": 60},
            ],
            IntentType.GENERAL_CHAT: [
                {"id": "task_respond", "description": "Generate response to user", "agent": None, "dependencies": [], "estimated_time_seconds": 10},
            ],
        }

    async def decompose(
        self, user_input: str, intent: IntentClassification, context: SessionContext
    ) -> Dict[str, Any]:
        template = self._decomposition_templates.get(intent.intent, self._decomposition_templates[IntentType.GENERAL_CHAT])

        tasks = []
        for tpl in template:
            task = {
                "id": tpl["id"],
                "description": tpl["description"],
                "type": intent.intent.value.lower(),
                "agent": tpl.get("agent"),
                "dependencies": tpl.get("dependencies", []),
                "priority": 5,
                "estimated_time_seconds": tpl.get("estimated_time_seconds", 30),
            }
            tasks.append(task)

        explanations = {
            IntentType.CODE_GENERATION: "I'll help you build that project. Let me set up the structure first.",
            IntentType.PROJECT_SCAFFOLD: "Let me scaffold a new project for you.",
            IntentType.DEPLOYMENT: "I'll build and deploy your project.",
            IntentType.SOCIAL_MEDIA: "Let me create and schedule that content.",
            IntentType.WEB_RESEARCH: "Let me search and gather that information.",
            IntentType.FILE_ORGANIZATION: "I'll organize those files for you.",
            IntentType.SYSTEM_AUTOMATION: "Let me handle that system task.",
            IntentType.GENERAL_CHAT: "",
        }

        return {
            "tasks": tasks,
            "explanation": explanations.get(intent.intent, "Let me help you with that.")
        }
