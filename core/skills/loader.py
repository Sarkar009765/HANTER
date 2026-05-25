from __future__ import annotations

import asyncio
import gc
from typing import Dict, Type, Optional, List
from datetime import datetime

from skills.base import Skill
from skills.builtin.dev.code_generator import CodeGeneratorSkill
from skills.builtin.social.content_creator import ContentCreatorSkill
from skills.builtin.web.scraper import WebScraperSkill
from skills.builtin.file.organizer import FileOrganizerSkill
from skills.builtin.system.monitor import SystemMonitorSkill
from utils.logger import logger


class SkillLoader:
    def __init__(self):
        self._registry: Dict[str, Type[Skill]] = {}
        self._loaded: Dict[str, Skill] = {}
        self._ram_usage: int = 0
        self._max_ram_mb: int = 400
        self._idle_timeout_seconds: int = 300
        self._lock = asyncio.Lock()
        self._register_defaults()

    def _register_defaults(self):
        builtins = [
            CodeGeneratorSkill,
            ContentCreatorSkill,
            WebScraperSkill,
            FileOrganizerSkill,
            SystemMonitorSkill,
        ]
        for skill_cls in builtins:
            self.register(skill_cls)

    def register(self, skill_class: Type[Skill]):
        self._registry[skill_class.name] = skill_class
        logger.info("skill_registered", name=skill_class.name)

    async def get_skill(self, name: str) -> Optional[Skill]:
        async with self._lock:
            if name in self._loaded:
                self._loaded[name].last_used = datetime.now()
                return self._loaded[name]

            skill_class = self._registry.get(name)
            if not skill_class:
                logger.warning("skill_not_found", name=name)
                return None

            if self._ram_usage + skill_class.ram_usage_mb > self._max_ram_mb:
                await self._unload_oldest()

            skill = skill_class()
            skill.load()
            self._loaded[name] = skill
            self._ram_usage += skill.ram_usage_mb
            logger.info("skill_loaded", name=name, ram=skill.ram_usage_mb, total_ram=self._ram_usage)
            return skill

    async def _unload_oldest(self):
        if not self._loaded:
            return
        oldest = min(
            self._loaded.values(),
            key=lambda s: (s.last_used or datetime.min, s.use_count)
        )
        self.unload_skill(oldest.name)

    def unload_skill(self, name: str):
        skill = self._loaded.get(name)
        if skill:
            skill.unload()
            self._ram_usage -= skill.ram_usage_mb
            del self._loaded[name]
            logger.info("skill_unloaded", name=name, freed_mb=skill.ram_usage_mb)

    def list_skills(self) -> List[dict]:
        result = []
        for name, cls in self._registry.items():
            info = {
                "name": name,
                "description": cls.description,
                "version": cls.version,
                "category": cls.category,
                "ram_usage_mb": cls.ram_usage_mb,
                "is_loaded": name in self._loaded,
            }
            if name in self._loaded:
                info["use_count"] = self._loaded[name].use_count
            result.append(info)
        return result

    async def cleanup_idle(self):
        now = datetime.now()
        to_unload = []
        for name, skill in self._loaded.items():
            if skill.last_used and (now - skill.last_used).seconds > self._idle_timeout_seconds:
                to_unload.append(name)
        for name in to_unload:
            self.unload_skill(name)

    def unload_all_non_essential(self):
        for name in list(self._loaded.keys()):
            self.unload_skill(name)

    @property
    def ram_usage_mb(self) -> int:
        return self._ram_usage
