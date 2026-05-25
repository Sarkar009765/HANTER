from __future__ import annotations

from typing import Dict, Optional
from models import SessionContext
from datetime import datetime
import json


class ContextManager:
    def __init__(self):
        self._sessions: Dict[str, SessionContext] = {}

    async def get_context(self, session_id: str) -> SessionContext:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionContext(
                session_id=session_id,
                conversation_buffer=[]
            )
        return self._sessions[session_id]

    async def update_context(
        self, session_id: str, updates: dict
    ):
        context = await self.get_context(session_id)
        for key, value in updates.items():
            if hasattr(context, key):
                setattr(context, key, value)

    async def add_to_buffer(
        self, session_id: str, role: str, content: str
    ):
        context = await self.get_context(session_id)
        context.conversation_buffer.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(context.conversation_buffer) > 10:
            context.conversation_buffer = context.conversation_buffer[-10:]

    async def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]

    async def get_session_count(self) -> int:
        return len(self._sessions)
