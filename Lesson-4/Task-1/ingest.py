#!/usr/bin/env python3
"""Build or rebuild the HR policy FAISS index, with optional retrieval test."""

from __future__ import annotations

import argparse
import sys

from config import Settings
from tools.rag_tool import build_hr_index, create_hr_policy_tool, load_hr_documents


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest HR policies into FAISS.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild even if an index already exists.",
    )
    parser.add_argument(
        "--query",
        help="Run a test retrieval after indexing (or against the existing index).",
    )
    args = parser.parse_args()

    settings = Settings.from_env()
    docs = load_hr_documents(settings.hr_data_dir)
    if not docs:
        print(f"No documents found in {settings.hr_data_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(docs)} HR policy file(s) in {settings.hr_data_dir}")

    if args.rebuild or not (settings.index_dir / "hr_policies.faiss").exists():
        print("Building FAISS index (this calls Ollama for embeddings)...")
        store = build_hr_index(settings)
        print(f"Saved index to {settings.index_dir} ({len(store.docstore._dict)} chunks)")
    else:
        print(f"Index already exists at {settings.index_dir} (use --rebuild to refresh)")

    if args.query:
        print(f"\nTest query: {args.query}\n")
        tool = create_hr_policy_tool(settings)
        print(tool.invoke(args.query))


if __name__ == "__main__":
    main()
