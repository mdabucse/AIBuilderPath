#!/usr/bin/env python3
"""CLI runner for the Presidio Research Agent."""

from __future__ import annotations

import argparse
import sys
import time

from agent.research_agent import get_research_agent
from config import Settings


def run_query(agent, query: str) -> None:
    """Invoke the agent with a single query and log runtime details."""
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    start_time = time.time()
    try:
        # We invoke the agent executor
        response = agent.invoke({"input": query})
        output = response.get("output", "No response content.")
        duration = time.time() - start_time

        print("\n" + "-" * 40 + " AGENT ANSWER " + "-" * 40)
        print(output)
        print("-" * 94)
        print(f"Time Taken: {duration:.2f} seconds\n")
    except Exception as exc:
        print(f"\nAgent execution failed: {exc}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Presidio Internal Research Agent CLI runner."
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="A custom search or research query to run with the agent.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the three predefined benchmark test queries.",
    )
    args = parser.parse_args()

    settings = Settings.from_env()
    print("Initializing agent...")
    agent = get_research_agent(settings)
    print("Agent ready.")

    if args.test:
        test_queries = [
            "Summarize all customer feedback related to our Q1 marketing campaigns.",
            "Compare our current hiring trend with industry benchmarks.",
            "Find relevant compliance policies related to AI data handling.",
        ]
        print(f"Running {len(test_queries)} benchmark queries...\n")
        for q in test_queries:
            run_query(agent, q)
    elif args.query:
        run_query(agent, args.query)
    else:
        # Prompt user if no arguments provided
        try:
            while True:
                query = input("\nEnter query (or 'exit' to quit): ").strip()
                if not query:
                    continue
                if query.lower() in {"exit", "quit"}:
                    break
                run_query(agent, query)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")


if __name__ == "__main__":
    main()
