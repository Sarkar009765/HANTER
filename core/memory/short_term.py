from __future__ import annotations

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import sqlite3
import json
from uuid import uuid4


class ShortTermMemory:
    def __init__(self, db_conn: sqlite3.Connection):
        self._conn = db_conn
        self._retention_days = 7

    async def store(self, session_id: str, content: str, metadata: Optional[Dict] = None):
        self._conn.execute(
            "INSERT INTO messages (id, session_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
            (str(uuid4()), session_id, "system", content, datetime.now().isoformat())
        )
        self._conn.commit()

    async def get_recent(self, session_id: str, limit: int = 20) -> List[Dict]:
        cursor = self._conn.cursor()
        rows = cursor.execute(
            "SELECT * FROM messages WHERE session_id = ? AND created_at > ? ORDER BY created_at DESC LIMIT ?",
            (session_id, (datetime.now() - timedelta(days=self._retention_days)).isoformat(), limit)
        ).fetchall()
        return [dict(r) for r in rows]

    async def cleanup_old(self):
        cursor = self._conn.cursor()
        cutoff = (datetime.now() - timedelta(days=self._retention_days)).isoformat()
        cursor.execute("DELETE FROM messages WHERE created_at < ? AND role != 'system'", (cutoff,))
        self._conn.commit()
