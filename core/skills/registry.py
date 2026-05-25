from __future__ import annotations

from typing import Dict, Optional
import yaml
from pathlib import Path

from utils.logger import logger


class SkillConfig:
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "skills.yaml"
        self.config_path = Path(config_path)
        self._skills_config: Dict = {}
        self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                self._skills_config = yaml.safe_load(f) or {}
            logger.info("skill_config_loaded", path=str(self.config_path))

    def get_skill_config(self, name: str) -> Optional[Dict]:
        skills = self._skills_config.get("skills", {})
        return skills.get(name)

    def list_skill_configs(self) -> Dict:
        return self._skills_config.get("skills", {})
