from __future__ import annotations

import aiofiles
import os
from pathlib import Path
from typing import Optional, List

from utils.validators import validate_path
from utils.logger import logger


class SecureFileSystem:
    def __init__(self):
        self.allowed_roots = [
            str(Path("~/BroAIProjects").expanduser().resolve()),
            str(Path("~/Downloads").expanduser().resolve()),
            str(Path("~/Documents").expanduser().resolve()),
        ]

    def validate_path(self, path: str) -> bool:
        resolved = str(Path(path).resolve())
        for root in self.allowed_roots:
            if resolved.startswith(root):
                return True
        return False

    async def read_file(self, path: str) -> Optional[str]:
        if not self.validate_path(path):
            raise PermissionError(f"Access denied: {path}")
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return await f.read()

    async def write_file(self, path: str, content: str) -> bool:
        if not self.validate_path(path):
            raise PermissionError(f"Access denied: {path}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(content)
        return True

    async def list_directory(self, path: str) -> List[str]:
        if not self.validate_path(path):
            raise PermissionError(f"Access denied: {path}")
        return os.listdir(path)

    async def delete_file(self, path: str) -> bool:
        if not self.validate_path(path):
            raise PermissionError(f"Access denied: {path}")
        os.remove(path)
        return True
