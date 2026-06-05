
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load the .env that sits next to this project (works regardless of cwd).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _env(key: str, default: str = "") -> str:
    """Read an env var, treating empty strings as 'unset'."""
    value = os.getenv(key)
    return value if value not in (None, "") else default


@dataclass
class Settings:
    """All knobs for the chatbot in one place."""

    # --- which backends to use -------------------------------------------
    llm_backend: str = "ollama"      # ollama | azure | claude
    embed_backend: str = "ollama"    # ollama | azure

    # --- Ollama (local) ---------------------------------------------------
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "phi3"
    ollama_embed_model: str = "nomic-embed-text"

    # --- Azure OpenAI -----------------------------------------------------
    azure_endpoint: str = ""
    azure_api_key: str = ""
    azure_api_version: str = "2024-02-15-preview"
    azure_chat_deployment: str = "gpt-4o"
    azure_embed_deployment: str = "text-embedding-3-small"

    # --- Anthropic / Claude ----------------------------------------------
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-5"

    # --- RAG parameters ---------------------------------------------------
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 4

    # --- paths ------------------------------------------------------------
    data_dir: str = "data"
    index_dir: str = "index"

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from environment variables, falling back to defaults."""
        return cls(
            llm_backend=_env("LLM_BACKEND", "ollama").lower(),
            embed_backend=_env("EMBED_BACKEND", "ollama").lower(),
            ollama_base_url=_env("OLLAMA_BASE_URL", "http://localhost:11434"),
            ollama_chat_model=_env("OLLAMA_CHAT_MODEL", "phi3"),
            ollama_embed_model=_env("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
            azure_endpoint=_env("AZURE_OPENAI_ENDPOINT"),
            azure_api_key=_env("AZURE_OPENAI_API_KEY"),
            azure_api_version=_env("AZURE_OPENAI_VERSION", "2024-02-15-preview"),
            azure_chat_deployment=_env("AZURE_DEPLOYMENT_NAME", "gpt-4o"),
            azure_embed_deployment=_env("AZURE_EMBED_DEPLOYMENT_NAME", "text-embedding-3-small"),
            anthropic_api_key=_env("ANTHROPIC_API_KEY"),
            anthropic_model=_env("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
            chunk_size=int(_env("CHUNK_SIZE", "800")),
            chunk_overlap=int(_env("CHUNK_OVERLAP", "120")),
            top_k=int(_env("TOP_K", "4")),
            data_dir=_env("DATA_DIR", "data"),
            index_dir=_env("INDEX_DIR", "index"),
        )

    # Convenience absolute paths -------------------------------------------
    @property
    def data_path(self) -> Path:
        p = Path(self.data_dir)
        return p if p.is_absolute() else PROJECT_ROOT / p

    @property
    def index_path(self) -> Path:
        p = Path(self.index_dir)
        return p if p.is_absolute() else PROJECT_ROOT / p
