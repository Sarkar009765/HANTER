from __future__ import annotations

import asyncio
import shlex
from typing import Optional
from pathlib import Path

from utils.logger import logger
from utils.validators import validate_command


class SecureShell:
    def __init__(self):
        self.allowed_commands = [
            "git", "npm", "yarn", "pnpm", "python", "pip",
            "npx", "vercel", "netlify", "docker"
        ]
        self.timeout = 300
        self.output_limit = 1048576

    async def execute(self, command: str, cwd: Optional[str] = None) -> dict:
        valid, error = validate_command(command)
        if not valid:
            return {"success": False, "error": error, "blocked": True}

        parts = shlex.split(command)
        if parts[0] not in self.allowed_commands:
            return {"success": False, "error": f"Command '{parts[0]}' not allowed", "blocked": True}

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                cwd=cwd or str(Path.home()),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                limit=self.output_limit,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=self.timeout
                )
                return {
                    "success": proc.returncode == 0,
                    "stdout": stdout.decode(errors="replace"),
                    "stderr": stderr.decode(errors="replace"),
                    "returncode": proc.returncode,
                }
            except asyncio.TimeoutError:
                proc.kill()
                return {"success": False, "error": f"Command timed out after {self.timeout}s"}
        except Exception as e:
            logger.error("shell_execution_error", error=str(e))
            return {"success": False, "error": str(e)}
