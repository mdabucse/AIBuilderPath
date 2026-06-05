"""Retrieval: embed the user's question and pull the closest chunks."""

from __future__ import annotations

from .config import Settings
from .embeddings import embed_query
from .vector_store import VectorStore


def retrieve(query: str, store: VectorStore, settings: Settings) -> list[dict]:
    """Return the top-k chunks most relevant to ``query``."""
    if store.size == 0:
        return []
    query_vector = embed_query(query, settings)
    return store.search(query_vector, top_k=settings.top_k)


def format_context(results: list[dict]) -> str:
    """Render retrieved chunks into a numbered context block for the prompt."""
    blocks = []
    for i, r in enumerate(results, start=1):
        source = r.get("source", "unknown")
        blocks.append(f"[{i}] (source: {source})\n{r['text']}")
    return "\n\n".join(blocks)
