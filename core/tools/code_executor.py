from __future__ import annotations

import ast
import sys
from typing import Optional, Dict, Any
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr


class CodeExecutor:
    BLOCKED_MODULES = ["os", "subprocess", "shutil", "socket", "ctypes", "multiprocessing"]

    async def execute(self, code: str, language: str = "python") -> Dict[str, Any]:
        if language == "python":
            return await self._execute_python(code)
        return {"success": False, "error": f"Unsupported language: {language}"}

    async def _execute_python(self, code: str) -> Dict[str, Any]:
        for module in self.BLOCKED_MODULES:
            if f"import {module}" in code or f"from {module}" in code:
                return {"success": False, "error": f"Module '{module}' is blocked for security"}

        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            tree = ast.parse(code)
            if any(
                isinstance(node, (ast.Call, ast.Exec))
                for node in ast.walk(tree)
            ):
                pass

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                compiled = compile(tree, "<sandbox>", "exec")
                exec(compiled, {"__builtins__": __builtins__})

            return {
                "success": True,
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
            }
