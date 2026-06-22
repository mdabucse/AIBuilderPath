"""Web search tool — Tavily (preferred) or DuckDuckGo fallback."""

from __future__ import annotations

import os

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import BaseTool

from config import Settings


def create_web_search_tool(settings: Settings | None = None) -> BaseTool:
    """Return a LangChain tool for industry benchmarks and regulatory updates."""
    settings = settings or Settings.from_env()

    if settings.tavily_api_key:
        os.environ.setdefault("TAVILY_API_KEY", settings.tavily_api_key)
        return TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            name="web_search",
            description=(
                "Search the public web for insurance industry benchmarks, hiring trends, "
                "regulatory updates, and market news. Use when comparing Presidio metrics "
                "to external data or finding current compliance/regulatory information."
            ),
        )

    return DuckDuckGoSearchRun(
        name="web_search",
        description=(
            "Search the public web for insurance industry benchmarks, hiring trends, "
            "regulatory updates, and market news. Use when comparing Presidio metrics "
            "to external data or finding current compliance/regulatory information."
        ),
    )
