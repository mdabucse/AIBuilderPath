"""Load raw documents from the knowledge-base folder.

Supports plain text (`.txt`), Markdown (`.md`) and PDF (`.pdf`, via PyMuPDF).
No framework involved — just file reading and text extraction.
"""

from __future__ import annotations

from pathlib import Path

SUPPORTED_SUFFIXES = {".txt", ".md", ".markdown", ".pdf"}


def _read_pdf(path: Path) -> str:
    """Extract text from a PDF, page by page, using PyMuPDF."""
    import pymupdf  # imported lazily so non-PDF setups don't need it at import time

    parts: list[str] = []
    with pymupdf.open(path) as doc:
        for page in doc:
            parts.append(page.get_text())
    return "\n".join(parts)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_document(path: str | Path) -> str:
    """Return the text content of a single file."""
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        return _read_pdf(path)
    return _read_text(path)


def load_documents(data_dir: str | Path) -> list[dict]:
    """Load every supported file in `data_dir`.

    Returns a list of ``{"source": <filename>, "text": <content>}`` dicts,
    sorted by filename for deterministic indexing.
    """
    data_dir = Path(data_dir)
    if not data_dir.exists():
        return []

    docs: list[dict] = []
    for path in sorted(data_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            text = load_document(path).strip()
            if text:
                docs.append({"source": path.name, "text": text})
    return docs
