from __future__ import annotations

from typing import Dict, Type, Optional
from agents.base import BaseAgent
from agents.dev_agent import DevAgent
from agents.social_agent import SocialAgent
from agents.web_agent import WebAgent
from agents.file_agent import FileAgent
from agents.sys_agent import SysAgent
from utils.logger import logger


class AgentRegistry:
    _instance: Optional["AgentRegistry"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._agents: Dict[str, Type[BaseAgent]] = {}
            cls._instance._loaded: Dict[str, BaseAgent] = {}
            cls._instance._register_defaults()
        return cls._instance

    @classmethod
    def _register_defaults(cls):
        default_agents = [
            DevAgent,
            SocialAgent,
            WebAgent,
            FileAgent,
            SysAgent,
        ]
        for agent_cls in default_agents:
            cls._instance.register(agent_cls)
            logger.info("agent_registered", name=agent_cls.name)

    def register(self, agent_class: Type[BaseAgent]):
        self._agents[agent_class.name.lower()] = agent_class

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        key = name.lower()
        if key not in self._loaded:
            agent_cls = self._agents.get(key)
            if not agent_cls:
                logger.warning("agent_not_found", name=name)
                return None
            self._loaded[key] = agent_cls()
        return self._loaded.get(key)

    def list_agents(self) -> Dict[str, dict]:
        return {
            name: {
                "description": cls.description,
                "version": cls.version,
                "ram_budget_mb": cls.ram_budget_mb,
                "skills": cls.required_skills,
            }
            for name, cls in self._agents.items()
        }
