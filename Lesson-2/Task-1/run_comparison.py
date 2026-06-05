"""Run every scenario against every prompt and save the responses.

Uses the local Ollama server (phi3 by default) so the lab is reproducible and
free. The same code would work against any chat API by swapping the request.

Output: outputs/<prompt>.json — a list of {scenario_id, title, message, response}.
"""

from __future__ import annotations

import json
from pathlib import Path

import requests

from scenarios import SCENARIOS

ROOT = Path(__file__).resolve().parent
PROMPTS_DIR = ROOT / "prompts"
OUTPUTS_DIR = ROOT / "outputs"

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3"

PROMPTS = {
    "basic": PROMPTS_DIR / "basic_prompt.txt",
    "refined": PROMPTS_DIR / "refined_prompt.txt",
    "cot": PROMPTS_DIR / "cot_prompt.txt",
}


def ask(system_prompt: str, user_message: str) -> str:
    """Send one chat turn to Ollama and return the model's reply."""
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "stream": False,
            "options": {"temperature": 0.2},
        },
        timeout=600,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def run_prompt(name: str, prompt_path: Path) -> list[dict]:
    """Run all scenarios against a single prompt file."""
    system_prompt = prompt_path.read_text(encoding="utf-8")
    results: list[dict] = []
    for scenario in SCENARIOS:
        print(f"  - {scenario['id']}")
        reply = ask(system_prompt, scenario["message"])
        results.append(
            {
                "scenario_id": scenario["id"],
                "title": scenario["title"],
                "customer_message": scenario["message"],
                "response": reply,
            }
        )
    return results


def main() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Model: {MODEL}")
    for name, path in PROMPTS.items():
        print(f"\n[{name}] running {len(SCENARIOS)} scenarios...")
        results = run_prompt(name, path)
        out_path = OUTPUTS_DIR / f"{name}.json"
        out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"[{name}] saved -> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
