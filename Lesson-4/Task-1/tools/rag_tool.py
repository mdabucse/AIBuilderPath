"""RAG tool — vector search over Presidio HR policy documents."""

from __future__ import annotations

from pathlib import Path

from langchain_classic.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import Settings

INDEX_NAME = "hr_policies"


def _embeddings(settings: Settings) -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.ollama_embed_model,
        base_url=settings.ollama_base_url,
    )


def load_hr_documents(data_dir: Path) -> list[Document]:
    """Load markdown/text HR policy files from disk."""
    docs: list[Document] = []
    for path in sorted(data_dir.glob("**/*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        docs.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source": path.name},
            )
        )
    return docs


def build_hr_index(settings: Settings | None = None) -> FAISS:
    """Chunk HR policies, embed with Ollama, and persist a FAISS index."""
    settings = settings or Settings.from_env()
    raw_docs = load_hr_documents(settings.hr_data_dir)
    if not raw_docs:
        raise FileNotFoundError(f"No HR documents found in {settings.hr_data_dir}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(raw_docs)

    store = FAISS.from_documents(chunks, _embeddings(settings))
    settings.index_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(settings.index_dir), index_name=INDEX_NAME)
    return store


def load_hr_index(settings: Settings | None = None) -> FAISS:
    """Load a saved FAISS index, building it first when missing."""
    settings = settings or Settings.from_env()
    index_file = settings.index_dir / f"{INDEX_NAME}.faiss"
    if not index_file.exists():
        return build_hr_index(settings)

    return FAISS.load_local(
        str(settings.index_dir),
        _embeddings(settings),
        index_name=INDEX_NAME,
        allow_dangerous_deserialization=True,
    )


def create_hr_policy_tool(settings: Settings | None = None):
    """LangChain tool the agent uses to search HR/compliance policies."""
    settings = settings or Settings.from_env()
    store = load_hr_index(settings)
    retriever = store.as_retriever(search_kwargs={"k": settings.top_k})

    return create_retriever_tool(
        retriever,
        name="search_hr_policies",
        description=(
            "Search Presidio HR and compliance policy documents. "
            "Use for questions about remote work, code of conduct, hiring trends, "
            "AI data handling, confidentiality, and internal compliance rules."
        ),
    )
