from __future__ import annotations

from typing import List, Dict, Optional, Any
from uuid import uuid4
import os
from pathlib import Path


class LongTermMemory:
    def __init__(self, persist_path: Optional[str] = None):
        if persist_path is None:
            persist_path = str(Path("data/chromadb").resolve())
        self._persist_path = persist_path
        self._collection = None
        self._client = None

    async def initialize(self):
        try:
            import chromadb
            os.makedirs(self._persist_path, exist_ok=True)
            self._client = chromadb.PersistentClient(path=self._persist_path)
            self._collection = self._client.get_or_create_collection(
                name="long_term_memory",
                metadata={"hnsw:space": "cosine"}
            )
        except ImportError:
            pass

    async def store(
        self, text: str, metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None
    ):
        if not self._collection:
            return
        doc_id = str(uuid4())
        if metadata is None:
            metadata = {}
        if embedding:
            self._collection.add(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata],
                embeddings=[embedding]
            )
        else:
            self._collection.add(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata]
            )

    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        if not self._collection:
            return []
        results = self._collection.query(
            query_texts=[query],
            n_results=limit
        )
        output = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                output.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": results["distances"][0][i] if results["distances"] else 0.0
                })
        return output

    async def delete(self, doc_id: str):
        if self._collection:
            self._collection.delete(ids=[doc_id])

    async def close(self):
        if self._client:
            self._client = None
