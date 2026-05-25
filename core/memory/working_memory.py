from __future__ import annotations

from typing import Dict, List, Optional
from datetime import datetime


class WorkingMemory:
    def __init__(self):
        self._sessions: Dict[str, Dict] = {}
        self._max_messages = 10

    def get_or_create(self, session_id: str) -> Dict:
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "session_id": session_id,
                "current_intent": None,
                "active_agents": [],
                "loaded_skills": [],
                "conversation_buffer": [],
                "context_variables": {},
                "temp_files": [],
                "ram_usage_mb": 0,
                "last_accessed": datetime.now().isoformat()
            }
        return self._sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        session = self.get_or_create(session_id)
        session["conversation_buffer"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(session["conversation_buffer"]) > self._max_messages:
            session["conversation_buffer"] = session["conversation_buffer"][-self._max_messages:]
        session["last_accessed"] = datetime.now().isoformat()

    def get_context(self, session_id: str) -> Optional[Dict]:
        session = self.get_or_create(session_id)
        return session

    def update_variable(self, session_id: str, key: str, value):
        session = self.get_or_create(session_id)
        session["context_variables"][key] = value

    def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]

    def clear_cache(self):
        self._sessions.clear()
