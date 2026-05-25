from __future__ import annotations

import httpx
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30, follow_redirects=True)

    async def get(self, url: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        response = await self._client.get(url, headers=headers)
        return {
            "status_code": response.status_code,
            "content": response.text,
            "json": self._safe_json(response),
        }

    async def post(self, url: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        response = await self._client.post(url, json=data, headers=headers)
        return {
            "status_code": response.status_code,
            "content": response.text,
            "json": self._safe_json(response),
        }

    def _safe_json(self, response: httpx.Response) -> Optional[Dict]:
        try:
            return response.json()
        except Exception:
            return None

    async def close(self):
        await self._client.aclose()
