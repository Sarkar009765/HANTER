from __future__ import annotations

import re
from pathlib import Path


BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"sudo",
    r"chmod\s+777",
    r"mkfs",
    r"dd\s+if",
    r">\s+/dev/",
    r"curl\s+\|.*sh",
    r"wget\s+\|.*bash",
    r":\(\)\s*\{",
    r"eval\s+\$",
]


def validate_command(command: str) -> tuple[bool, str]:
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"Command blocked by security policy: matches pattern '{pattern}'"
    return True, ""


def validate_path(path: str, allowed_roots: list[str] | None = None) -> bool:
    if allowed_roots is None:
        allowed_roots = ["~/HANTERProjects", "~/Downloads", "~/Documents"]
    resolved = str(Path(path).resolve())
    for root in allowed_roots:
        root_resolved = str(Path(root).expanduser().resolve())
        if resolved.startswith(root_resolved):
            return True
    return False


def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name)
