from __future__ import annotations

from typing import Optional


class Browser:
    def __init__(self):
        self.headless = True

    async def scrape(self, url: str) -> dict:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                response = await client.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                })
                return {
                    "success": response.status_code == 200,
                    "content": response.text,
                    "status_code": response.status_code,
                    "url": str(response.url)
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
