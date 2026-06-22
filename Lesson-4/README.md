# Assignment 1 — Internal Research Agent (Presidio)

Build a **LangChain agent** with three tools for Presidio's internal research use cases.

| Tool | Purpose |
| --- | --- |
| MCP Tool | Connect to Google Docs for insurance-related queries |
| RAG Tool | Search HR policy documents (vectorize before querying) |
| Web Search Tool | Industry benchmarks, trends, and regulatory updates |

## Example queries

- *"Summarize all customer feedback related to our Q1 marketing campaigns."*
- *"Compare our current hiring trend with industry benchmarks."*
- *"Find relevant compliance policies related to AI data handling."*

---

## Build plan (step by step)

| Step | What we build | Status |
| --- | --- | --- |
| **1** | Project scaffold, sample data, config | Done |
| **2** | RAG tool — ingest HR policies into FAISS | Done |
| **3** | Web search tool — DuckDuckGo / Tavily | Done |
| **4** | MCP tool — Google Docs for insurance docs | Done |
| **5** | LangChain ReAct agent wiring all three tools | Next |
| **6** | CLI runner + test the three example queries | Pending |

---

## Project structure

```text
Task-1/
├── agent/              # LangChain agent assembly (Step 5)
├── tools/              # MCP, RAG, and web search tools (Steps 2–4)
├── data/
│   ├── hr_policies/    # RAG knowledge base
│   └── insurance/      # Local fallback for Google Docs content
├── index/              # FAISS vector store (generated)
├── mcp_server/         # Stdio MCP server for insurance Google Docs (Step 4)
├── ingest.py           # Build HR policy index (Step 2)
├── docs_test.py        # Test Google Docs MCP tools (Step 4)
├── main.py             # CLI entry point (Step 6)
├── pyproject.toml
└── .env.example
```

---

## Setup

```bash
cd Lesson-4/Task-1
uv sync
cp .env.example .env
```

Ensure Ollama is running with chat and embedding models:

```bash
ollama pull phi3
ollama pull nomic-embed-text
```

---

## Sample data

- **HR policies** (`data/hr_policies/`) — AI data handling, remote work, code of conduct
- **Insurance docs** (`data/insurance/`) — Q1 marketing feedback, product overview (MCP fallback until Google Docs is wired)

---

## Step 2 — RAG tool (done)

Build the HR policy index:

```bash
cd Lesson-4/Task-1
uv run python ingest.py --rebuild
```

Test retrieval without the full agent:

```bash
uv run python ingest.py --query "What are the rules for AI data handling?"
```

The LangChain tool `search_hr_policies` lives in `tools/rag_tool.py` and will be wired into the agent in Step 5.

## Step 3 — Web search tool (done)

Uses **Tavily** when `TAVILY_API_KEY` is set in `.env`, otherwise falls back to DuckDuckGo.

```bash
cp .env.example .env
# Add your Tavily key to .env (keep secrets out of .env.example)

cd Lesson-4/Task-1
uv run python search_test.py "insurance industry hiring trends 2026"
```

The LangChain tool `web_search` lives in `tools/web_search_tool.py`.

## Step 4 — MCP Google Docs tool (done)

A stdio MCP server (`mcp_server/google_docs_server.py`) exposes three tools:

| MCP tool | Purpose |
| --- | --- |
| `list_insurance_google_docs` | List available insurance documents |
| `search_insurance_google_docs` | Search customer feedback, campaigns, products |
| `read_insurance_google_doc` | Read one document by id |

**Without Google credentials:** reads from `data/insurance/` (local mirror of Google Docs content).

**With Google credentials:** set in `.env`:

```bash
GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
GOOGLE_DOCS_FOLDER_ID=your-drive-folder-id
# or comma-separated doc ids:
GOOGLE_DOC_IDS=doc-id-1,doc-id-2
```

Test the MCP connection:

```bash
cd Lesson-4/Task-1
uv run python docs_test.py "Q1 marketing customer feedback"
```

LangChain loads these tools via `tools/mcp_docs_tool.py` using `langchain-mcp-adapters`.

## Next step

**Step 5:** Wire all three tools into a LangChain ReAct agent.
