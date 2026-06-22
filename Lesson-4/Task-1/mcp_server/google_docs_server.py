"""MCP server — Presidio insurance Google Docs (local mirror + optional Google API)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("presidio-google-docs")

SCOPES = (
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
)


@dataclass
class InsuranceDocument:
    doc_id: str
    title: str
    content: str
    source: str  # "local" | "google"


def _insurance_dir() -> Path:
    return Path(os.getenv("INSURANCE_DATA_DIR", "data/insurance"))


def _load_local_documents() -> list[InsuranceDocument]:
    docs: list[InsuranceDocument] = []
    data_dir = _insurance_dir()
    if not data_dir.exists():
        return docs

    for path in sorted(data_dir.glob("**/*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        title = path.stem.replace("_", " ").title()
        docs.append(
            InsuranceDocument(
                doc_id=path.stem,
                title=title,
                content=path.read_text(encoding="utf-8"),
                source="local",
            )
        )
    return docs


def _extract_google_doc_text(document: dict) -> str:
    chunks: list[str] = []

    def walk(elements: list[dict]) -> None:
        for element in elements:
            if "paragraph" in element:
                for part in element["paragraph"].get("elements", []):
                    text = part.get("textRun", {}).get("content", "")
                    if text:
                        chunks.append(text)
            elif "table" in element:
                for row in element["table"].get("tableRows", []):
                    for cell in row.get("tableCells", []):
                        walk(cell.get("content", []))

    walk(document.get("body", {}).get("content", []))
    return "".join(chunks)


def _load_google_documents() -> list[InsuranceDocument]:
    service_account = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()
    if not service_account or not Path(service_account).exists():
        return []

    try:
        from google.oauth2 import service_account as google_sa
        from googleapiclient.discovery import build
    except ImportError:
        return []

    credentials = google_sa.Credentials.from_service_account_file(
        service_account,
        scopes=list(SCOPES),
    )
    docs_service = build("docs", "v1", credentials=credentials, cache_discovery=False)
    drive_service = build("drive", "v3", credentials=credentials, cache_discovery=False)

    doc_ids: list[tuple[str, str]] = []
    configured_ids = [
        doc_id.strip()
        for doc_id in os.getenv("GOOGLE_DOC_IDS", "").split(",")
        if doc_id.strip()
    ]
    for doc_id in configured_ids:
        doc_ids.append((doc_id, doc_id))

    folder_id = os.getenv("GOOGLE_DOCS_FOLDER_ID", "").strip()
    if folder_id:
        response = (
            drive_service.files()
            .list(
                q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.document' and trashed=false",
                fields="files(id, name)",
                pageSize=20,
            )
            .execute()
        )
        for item in response.get("files", []):
            doc_ids.append((item["id"], item["name"]))

    loaded: list[InsuranceDocument] = []
    seen: set[str] = set()
    for doc_id, title in doc_ids:
        if doc_id in seen:
            continue
        seen.add(doc_id)
        try:
            document = docs_service.documents().get(documentId=doc_id).execute()
            loaded.append(
                InsuranceDocument(
                    doc_id=doc_id,
                    title=document.get("title", title),
                    content=_extract_google_doc_text(document),
                    source="google",
                )
            )
        except Exception:
            continue
    return loaded


def _all_documents() -> list[InsuranceDocument]:
    docs = _load_google_documents()
    if docs:
        return docs
    return _load_local_documents()


def _score_text(text: str, query: str) -> int:
    text_lower = text.lower()
    terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
    if not terms:
        return 0
    return sum(text_lower.count(term) for term in terms)


def _format_doc(doc: InsuranceDocument) -> str:
    return f"Title: {doc.title}\nSource: {doc.source}\nDoc ID: {doc.doc_id}\n\n{doc.content}"


@mcp.tool()
def list_insurance_google_docs() -> str:
    """List Presidio insurance Google Docs (customer feedback, product info, campaigns)."""
    docs = _all_documents()
    if not docs:
        return "No insurance documents found. Configure Google Docs credentials or add files to data/insurance/."

    lines = [
        f"- {doc.title} (id={doc.doc_id}, source={doc.source})"
        for doc in docs
    ]
    backend = "Google Docs API" if docs[0].source == "google" else "local mirror of Google Docs"
    return f"Backend: {backend}\n\n" + "\n".join(lines)


@mcp.tool()
def search_insurance_google_docs(query: str) -> str:
    """Search Presidio insurance Google Docs for customer feedback, marketing campaigns, and product details."""
    docs = _all_documents()
    if not docs:
        return "No insurance documents available to search."

    ranked = sorted(
        ((doc, _score_text(doc.content, query)) for doc in docs),
        key=lambda item: item[1],
        reverse=True,
    )
    top = [(doc, score) for doc, score in ranked if score > 0][:3]
    if not top:
        top = ranked[:2]

    sections = []
    for doc, score in top:
        header = f"## {doc.title} (relevance={score}, source={doc.source})"
        sections.append(f"{header}\n\n{doc.content}")

    return "\n\n---\n\n".join(sections)


@mcp.tool()
def read_insurance_google_doc(doc_id: str) -> str:
    """Read the full text of one Presidio insurance Google Doc by its id or filename stem."""
    docs = _all_documents()
    match = next((doc for doc in docs if doc.doc_id == doc_id), None)
    if match is None:
        doc_id_lower = doc_id.lower()
        match = next(
            (doc for doc in docs if doc.title.lower() == doc_id_lower or doc.doc_id.lower() == doc_id_lower),
            None,
        )
    if match is None:
        available = ", ".join(doc.doc_id for doc in docs)
        return f"Document '{doc_id}' not found. Available ids: {available}"
    return _format_doc(match)


if __name__ == "__main__":
    mcp.run(transport="stdio")
