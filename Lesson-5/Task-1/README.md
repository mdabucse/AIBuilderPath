# Multi-Agent Support System (LangGraph)

This project implements a multi-agent support system that routes user queries to specialized agents (IT and Finance) using LangGraph and LangChain. It uses a local Ollama model (`llama3.2:3b`) for privacy and cost-efficiency.

## Architecture

- **Supervisor Agent**: Classifies incoming queries as either 'IT' or 'Finance' and routes them accordingly.
- **IT Agent**: Handles IT-related queries using internal documentation and can perform web searches using Wikipedia.
- **Finance Agent**: Handles Finance-related queries using internal documentation and can perform web searches using Wikipedia.

## Setup Instructions

This project uses `uv` for fast dependency management.

1. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Make sure you have [Ollama](https://ollama.com) installed and the `llama3.2:3b` model downloaded:
   ```bash
   ollama pull llama3.2:3b
   ```
3. Run the interactive chat interface:
   ```bash
   uv run main.py
   ```

## Example Queries

- **IT**: "How do I set up my VPN?" or "What software is approved?"
- **Finance**: "When is payroll processed?" or "How do I file a reimbursement?"
- **General/Web**: "Who is the CEO of Microsoft?"
