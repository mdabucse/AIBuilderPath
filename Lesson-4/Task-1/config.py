"""Shared configuration for the Presidio research agent."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT / ".env")


@dataclass
class Settings:
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "llama3.2:3b"
    ollama_embed_model: str = "nomic-embed-text"

    hr_data_dir: Path = ROOT / "data" / "hr_policies"
    insurance_data_dir: Path = ROOT / "data" / "insurance"
    index_dir: Path = ROOT / "index"

    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 4

    google_service_account_file: str = ""
    google_docs_folder_id: str = ""
    google_doc_ids: tuple[str, ...] = ()

    tavily_api_key: str = ""

    @classmethod
    def from_env(cls) -> Settings:
        doc_ids = os.getenv("GOOGLE_DOC_IDS", "")
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            ollama_chat_model=os.getenv("OLLAMA_CHAT_MODEL", "llama3.2:3b"),
            ollama_embed_model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
            hr_data_dir=Path(os.getenv("HR_DATA_DIR", ROOT / "data" / "hr_policies")),
            insurance_data_dir=Path(os.getenv("INSURANCE_DATA_DIR", ROOT / "data" / "insurance")),
            index_dir=Path(os.getenv("INDEX_DIR", ROOT / "index")),
            chunk_size=int(os.getenv("CHUNK_SIZE", "800")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "120")),
            top_k=int(os.getenv("TOP_K", "4")),
            google_service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", ""),
            google_docs_folder_id=os.getenv("GOOGLE_DOCS_FOLDER_ID", ""),
            google_doc_ids=tuple(x.strip() for x in doc_ids.split(",") if x.strip()),
            tavily_api_key=os.getenv("TAVILY_API_KEY", ""),
        )
