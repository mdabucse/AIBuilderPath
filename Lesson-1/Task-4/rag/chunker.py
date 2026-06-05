from __future__ import annotations

import re

# Split on blank lines (paragraphs) OR after sentence-ending punctuation.
_UNIT_SPLIT = re.compile(r"\n{2,}|(?<=[.!?])\s+")


def _to_units(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)          # collapse runs of spaces/tabs
    text = re.sub(r"\n{3,}", "\n\n", text)        # collapse big gaps
    units = _UNIT_SPLIT.split(text.strip())
    return [u.strip() for u in units if u and u.strip()]


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    """Split ``text`` into overlapping chunks of roughly ``chunk_size`` chars."""
    if not text or not text.strip():
        return []

    units = _to_units(text)
    chunks: list[str] = []
    current = ""

    for unit in units:
        # A single unit longer than a whole chunk: hard-split it.
        while len(unit) > chunk_size:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(unit[:chunk_size])
            unit = unit[chunk_size - overlap:] if overlap else unit[chunk_size:]

        candidate = f"{current} {unit}".strip() if current else unit
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            # Flush the current chunk and start a new one with an overlap tail.
            if current:
                chunks.append(current)
            tail = current[-overlap:] if overlap and current else ""
            current = f"{tail} {unit}".strip() if tail else unit

    if current.strip():
        chunks.append(current.strip())

    return chunks


def chunk_documents(
    documents: list[dict], chunk_size: int = 800, overlap: int = 120
) -> list[dict]:
    records: list[dict] = []
    for doc in documents:
        pieces = chunk_text(doc["text"], chunk_size=chunk_size, overlap=overlap)
        for i, piece in enumerate(pieces):
            records.append(
                {"text": piece, "source": doc["source"], "chunk_index": i}
            )
    return records
