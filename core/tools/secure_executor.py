from __future__ import annotations

import asyncio
import subprocess
from typing import Optional, Dict, Any
from pathlib import Path
import json
import os

from tools.shell import SecureShell
from utils.logger import logger


class SecureCodeExecutor:
    def __init__(self):
        self.allowed_commands = [
            "git", "npm", "yarn", "pnpm", "python", "pip",
            "npx", "vercel", "netlify", "docker"
        ]
        self.blocked_patterns = [
            "rm -rf /", "sudo", "chmod 777", "> /etc",
            "curl | sh", "wget | bash", "mkfs", "dd if"
        ]
        self.shell = SecureShell()

    async def execute(self, command: str, cwd: str = ".") -> Dict[str, Any]:
        for pattern in self.blocked_patterns:
            if pattern in command:
                return {"success": False, "error": f"Blocked dangerous command pattern: {pattern}", "blocked": True}

        cmd_parts = command.split()
        if cmd_parts[0] not in self.allowed_commands:
            return {"success": False, "error": f"Command '{cmd_parts[0]}' not allowed", "blocked": True}

        return await self.shell.execute(command, cwd)


class SecureFileSystem:
    def __init__(self):
        self.allowed_roots = [
            str(Path("~/hanterProjects").expanduser().resolve()),
            str(Path("~/Downloads").expanduser().resolve()),
            str(Path("~/Documents").expanduser().resolve()),
        ]
        self.blocked_paths = [
            "/etc", "/usr", "/bin", "/sbin", "/sys", "/proc",
            "C:\\Windows", "C:\\Program Files"
        ]

    def validate_path(self, path: str) -> bool:
        resolved = str(Path(path).resolve())
        for blocked in self.blocked_paths:
            if resolved.startswith(blocked):
                return False
        for allowed in self.allowed_roots:
            if resolved.startswith(allowed):
                return True
        return False


class SecureKeyManager:
    def __init__(self):
        self.key_file = str(Path("~/.HANTER/keys.enc").expanduser())
        self._keys: Dict[str, str] = {}

    def load_keys(self, master_password: Optional[str] = None):
        key_path = Path(self.key_file)
        if key_path.exists():
            try:
                data = key_path.read_text()
                self._keys = json.loads(data)
            except Exception:
                self._keys = {}

    def get_key(self, service: str) -> Optional[str]:
        return self._keys.get(service)

    def set_key(self, service: str, key: str):
        self._keys[service] = key
        self._save_keys()

    def _save_keys(self):
        key_path = Path(self.key_file)
        key_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.write_text(json.dumps(self._keys, indent=2))
        os.chmod(key_path, 0o600)
