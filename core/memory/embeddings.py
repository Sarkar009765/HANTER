from __future__ import annotations

from sentence_transformers import SentenceTransformer
from typing import List, Optional


class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self._model_name = model_name
        self._model: Optional[SentenceTransformer] = None

    def load(self):
        if self._model is None:
            self._model = SentenceTransformer(self._model_name)

    def unload(self):
        self._model = None

    def generate(self, text: str) -> List[float]:
        self.load()
        embedding = self._model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        self.load()
        embeddings = self._model.encode(texts, normalize_embeddings=True)
        return [e.tolist() for e in embeddings]
