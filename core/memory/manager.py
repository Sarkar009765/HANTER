from __future__ import annotations

import sqlite3
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import uuid4

from utils.logger import logger


class MemoryManager:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.getenv("hanter_DB_PATH", str(Path("data/hanter.db").resolve()))
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    async def initialize(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        await self._create_tables()
        logger.info("memory_initialized", db_path=self.db_path)

    async def _create_tables(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title TEXT,
                context_summary TEXT
            );

            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES sessions(id),
                role TEXT CHECK(role IN ('user','assistant','system','agent')),
                content TEXT NOT NULL,
                agent_name TEXT,
                skill_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tokens_used INTEGER,
                latency_ms INTEGER
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES sessions(id),
                agent_name TEXT,
                description TEXT,
                status TEXT CHECK(status IN ('pending','running','completed','failed','cancelled')),
                input_data TEXT,
                output_data TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT,
                retry_count INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                category TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS agent_stats (
                agent_name TEXT PRIMARY KEY,
                total_tasks INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                avg_latency_ms INTEGER,
                last_used TIMESTAMP,
                total_ram_used_mb INTEGER
            );

            CREATE TABLE IF NOT EXISTS skills (
                name TEXT PRIMARY KEY,
                description TEXT,
                category TEXT,
                ram_usage_mb INTEGER,
                is_loaded BOOLEAN DEFAULT FALSE,
                load_count INTEGER DEFAULT 0,
                last_loaded TIMESTAMP
            );
        """)
        self._conn.commit()

    async def store_conversation(self, session_id: str, user_input: str, response: str):
        cursor = self._conn.cursor()
        now = datetime.now().isoformat()

        self._conn.execute(
            "INSERT OR IGNORE INTO sessions (id, created_at, last_active) VALUES (?, ?, ?)",
            (session_id, now, now)
        )
        self._conn.execute(
            "UPDATE sessions SET last_active = ? WHERE id = ?",
            (now, session_id)
        )

        msg_id = str(uuid4())
        self._conn.execute(
            "INSERT INTO messages (id, session_id, role, content) VALUES (?, ?, ?, ?)",
            (msg_id, session_id, "user", user_input)
        )
        msg_id2 = str(uuid4())
        self._conn.execute(
            "INSERT INTO messages (id, session_id, role, content) VALUES (?, ?, ?, ?)",
            (msg_id2, session_id, "assistant", response)
        )
        self._conn.commit()

    async def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict]:
        cursor = self._conn.cursor()
        rows = cursor.execute(
            "SELECT * FROM messages WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
            (session_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]

    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        cursor = self._conn.cursor()
        rows = cursor.execute(
            "SELECT content, role, created_at FROM messages WHERE content LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{query}%", limit)
        ).fetchall()
        return [{"text": r["content"], "role": r["role"], "created_at": r["created_at"]} for r in rows]

    async def store_preference(self, key: str, value: str, category: str = "general"):
        self._conn.execute(
            "INSERT OR REPLACE INTO preferences (key, value, category, updated_at) VALUES (?, ?, ?, ?)",
            (key, value, category, datetime.now().isoformat())
        )
        self._conn.commit()

    async def get_preference(self, key: str) -> Optional[str]:
        cursor = self._conn.cursor()
        row = cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    async def close(self):
        if self._conn:
            self._conn.close()
            logger.info("memory_closed")
