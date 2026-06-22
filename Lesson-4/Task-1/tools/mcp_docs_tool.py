"""Load Presidio insurance Google Docs tools via MCP."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from config import ROOT, Settings

SERVER_PATH = ROOT / "mcp_server" / "google_docs_server.py"


def _mcp_connection(settings: Settings) -> dict:
    env = {
        "INSURANCE_DATA_DIR": str(settings.insurance_data_dir),
        "GOOGLE_SERVICE_ACCOUNT_FILE": settings.google_service_account_file,
        "GOOGLE_DOCS_FOLDER_ID": settings.google_docs_folder_id,
        "GOOGLE_DOC_IDS": ",".join(settings.google_doc_ids),
    }
    return {
        "google_docs": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(SERVER_PATH)],
            "env": env,
        }
    }


async def create_google_docs_tools(settings: Settings | None = None) -> list[BaseTool]:
    """Connect to the Google Docs MCP server and return LangChain tools."""
    settings = settings or Settings.from_env()
    client = MultiServerMCPClient(_mcp_connection(settings))
    return await client.get_tools()


def create_google_docs_tools_sync(settings: Settings | None = None) -> list[BaseTool]:
    """Synchronous helper for scripts and the CLI agent."""
    return asyncio.run(create_google_docs_tools(settings))
