from __future__ import annotations

from typing import Optional
import os


class LocalLLM:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = os.getenv("OLLAMA_MODEL", "tinyllama")
        self.available = False

    async def check_available(self) -> bool:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                self.available = response.status_code == 200
                return self.available
        except Exception:
            self.available = False
            return False

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.available:
            return "Local LLM not available"

        try:
            import httpx
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("message", {}).get("content", "")
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Local LLM error: {str(e)}"
