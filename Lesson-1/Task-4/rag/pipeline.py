"""The RAG pipeline glued together: ingest -> retrieve -> generate.

Two public pieces:

* ``build_index`` / ``load_or_build_index`` — turn the ``data/`` folder into a
  searchable :class:`VectorStore` (and cache it to disk).
* ``RAGChatbot`` — a small, conversational wrapper that retrieves context for
  the latest question, injects it into a prompt alongside the running chat
  history, and streams the model's answer back.
"""

from __future__ import annotations

from typing import Iterator

from .chunker import chunk_documents
from .config import Settings
from .embeddings import embed_texts
from .llm import stream_chat
from .loaders import load_documents
from .retriever import format_context, retrieve
from .vector_store import VectorStore

SYSTEM_PROMPT = (
    "You are a helpful, friendly assistant that answers questions strictly from "
    "the provided context. Follow these rules:\n"
    "1. Use ONLY the information in the context to answer.\n"
    "2. If the answer is not in the context, say you don't have that information "
    "in the knowledge base — do not invent facts.\n"
    "3. Be concise and clear. When useful, mention the source filename you used.\n"
    "4. You may use the earlier conversation to understand follow-up questions."
)


def build_index(settings: Settings) -> VectorStore:
    """Read documents, chunk them, embed them, and persist the index."""
    documents = load_documents(settings.data_path)
    if not documents:
        raise RuntimeError(
            f"No documents found in '{settings.data_path}'. "
            "Add .txt/.md/.pdf files first."
        )

    chunks = chunk_documents(
        documents, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap
    )
    embeddings = embed_texts([c["text"] for c in chunks], settings)

    store = VectorStore()
    store.add(embeddings, chunks)
    store.save(settings.index_path)
    return store


def load_or_build_index(settings: Settings, rebuild: bool = False) -> VectorStore:
    """Load the cached index if present (and ``rebuild`` is False), else build it."""
    if not rebuild and VectorStore.exists(settings.index_path):
        return VectorStore.load(settings.index_path)
    return build_index(settings)


class RAGChatbot:
    """Conversational RAG: keeps history, retrieves per turn, streams answers."""

    def __init__(self, store: VectorStore, settings: Settings) -> None:
        self.store = store
        self.settings = settings

    def _build_messages(self, query: str, history: list[dict], context: str) -> list[dict]:
        """system + prior turns + (context-augmented) current question."""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Prior turns are stored "clean" (no context), keeping history readable.
        messages.extend(history)
        if context:
            user_content = (
                f"Use the following context to answer the question.\n\n"
                f"--- CONTEXT ---\n{context}\n--- END CONTEXT ---\n\n"
                f"Question: {query}"
            )
        else:
            user_content = query
        messages.append({"role": "user", "content": user_content})
        return messages

    def answer(self, query: str, history: list[dict] | None = None) -> tuple[Iterator[str], list[dict]]:
        """Retrieve context for ``query`` and stream the answer.

        Returns ``(token_iterator, sources)`` where ``sources`` are the chunks
        used, so the UI can show provenance.
        """
        history = history or []
        sources = retrieve(query, self.store, self.settings)
        context = format_context(sources)
        messages = self._build_messages(query, history, context)
        return stream_chat(messages, self.settings), sources
