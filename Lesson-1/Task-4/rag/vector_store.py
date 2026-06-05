"""A tiny vector store backed by NumPy — no FAISS, no external DB.

Embeddings are L2-normalised on the way in, so a cosine-similarity search is
just a single matrix-vector dot product. For the small/medium knowledge bases
this chatbot targets, brute-force search is instant and keeps the code honest
about what "retrieval" actually means.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def _normalise(matrix: np.ndarray) -> np.ndarray:
    """Scale each row to unit length (guarding against divide-by-zero)."""
    matrix = np.asarray(matrix, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


class VectorStore:
    """Holds chunk metadata alongside their (normalised) embedding vectors."""

    def __init__(self) -> None:
        self.embeddings: np.ndarray | None = None   # shape (N, dim)
        self.chunks: list[dict] = []                # parallel metadata

    # ------------------------------------------------------------------ build
    def add(self, embeddings: np.ndarray, chunks: list[dict]) -> None:
        vectors = _normalise(embeddings)
        if self.embeddings is None:
            self.embeddings = vectors
        else:
            self.embeddings = np.vstack([self.embeddings, vectors])
        self.chunks.extend(chunks)

    @property
    def size(self) -> int:
        return len(self.chunks)

    # ------------------------------------------------------------------ search
    def search(self, query_vector: np.ndarray, top_k: int = 4) -> list[dict]:
        """Return the ``top_k`` most similar chunks, each with a ``score``."""
        if self.embeddings is None or self.size == 0:
            return []

        query = _normalise(np.asarray(query_vector, dtype=np.float32).reshape(1, -1))[0]
        scores = self.embeddings @ query              # cosine similarity
        k = min(top_k, self.size)
        # argpartition for the top-k, then sort just those by score (descending).
        top_idx = np.argpartition(-scores, k - 1)[:k]
        top_idx = top_idx[np.argsort(-scores[top_idx])]

        results = []
        for idx in top_idx:
            record = dict(self.chunks[int(idx)])
            record["score"] = float(scores[int(idx)])
            results.append(record)
        return results

    # ------------------------------------------------------------- persistence
    def save(self, index_dir: str | Path) -> None:
        index_dir = Path(index_dir)
        index_dir.mkdir(parents=True, exist_ok=True)
        np.save(index_dir / "embeddings.npy", self.embeddings)
        with open(index_dir / "chunks.json", "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, index_dir: str | Path) -> "VectorStore":
        index_dir = Path(index_dir)
        store = cls()
        store.embeddings = np.load(index_dir / "embeddings.npy")
        with open(index_dir / "chunks.json", "r", encoding="utf-8") as f:
            store.chunks = json.load(f)
        return store

    @staticmethod
    def exists(index_dir: str | Path) -> bool:
        index_dir = Path(index_dir)
        return (index_dir / "embeddings.npy").exists() and (
            index_dir / "chunks.json"
        ).exists()
