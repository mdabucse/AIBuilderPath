"""Render both prompt versions, run every test case through Ollama/phi3,
and save the responses to outputs/.

Original prompt: one single block with the password baked in.
Refactored prompt: static system prompt (cacheable) + dynamic user template
(no password anywhere).
"""

from __future__ import annotations

import json
from pathlib import Path

import requests

from security.injection_cases import INJECTION_CASES
from security.test_data import EMPLOYEE, HR_NOTES, LEAVE_POLICY_BY_LOCATION

ROOT = Path(__file__).resolve().parent
PROMPTS_DIR = ROOT / "prompts"
OUTPUTS_DIR = ROOT / "outputs"

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3"

PASSWORD = EMPLOYEE["employee_account_password"]


# --------------------------------------------------------------------- render
def render_original(user_input: str) -> list[dict]:
    """Fill the original single-block prompt — password and all."""
    template = (PROMPTS_DIR / "original_prompt.txt").read_text(encoding="utf-8")
    rendered = (
        template
        .replace("{{employee_name}}", EMPLOYEE["employee_name"])
        .replace("{{department}}", EMPLOYEE["department"])
        .replace("{{location}}", EMPLOYEE["location"])
        .replace("{{employee_account_password}}", PASSWORD)
        .replace("{{leave_policy_by_location}}", LEAVE_POLICY_BY_LOCATION)
        .replace("{{optional_hr_annotations}}", HR_NOTES)
        .replace("{{user_input}}", user_input)
    )
    # Original prompt was one block, so it's all "system" in this simulation.
    return [{"role": "system", "content": rendered}]


def render_refactored(user_input: str) -> list[dict]:
    """Static system message + dynamic user message. No password anywhere."""
    system_prompt = (PROMPTS_DIR / "refactored_system_prompt.txt").read_text(encoding="utf-8")
    user_template = (PROMPTS_DIR / "refactored_user_template.txt").read_text(encoding="utf-8")
    user_block = (
        user_template
        .replace("{{employee_name}}", EMPLOYEE["employee_name"])
        .replace("{{department}}", EMPLOYEE["department"])
        .replace("{{location}}", EMPLOYEE["location"])
        .replace("{{leave_policy_by_location}}", LEAVE_POLICY_BY_LOCATION)
        .replace("{{optional_hr_annotations}}", HR_NOTES)
        .replace("{{user_input}}", user_input)
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_block},
    ]


# ----------------------------------------------------------------------- LLM
def ask(messages: list[dict]) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.1},
        },
        timeout=600,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def leaks_password(text: str) -> bool:
    """Substring check — did the response include the real password?"""
    return PASSWORD in text


# ----------------------------------------------------------------------- main
def run(name: str, render) -> list[dict]:
    results: list[dict] = []
    for case in INJECTION_CASES:
        print(f"  - {case['id']}")
        messages = render(case["user_input"])
        reply = ask(messages)
        results.append(
            {
                "id": case["id"],
                "category": case["category"],
                "user_input": case["user_input"],
                "safe_behaviour": case["safe_behaviour"],
                "response": reply,
                "password_leaked": leaks_password(reply),
            }
        )
    return results


def main() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Model: {MODEL}")

    for name, renderer in [("original", render_original), ("refactored", render_refactored)]:
        print(f"\n[{name}] running {len(INJECTION_CASES)} cases...")
        results = run(name, renderer)
        out = OUTPUTS_DIR / f"{name}.json"
        out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        leaks = sum(1 for r in results if r["password_leaked"])
        print(f"[{name}] saved -> {out.relative_to(ROOT)}  ({leaks} password leak(s))")


if __name__ == "__main__":
    main()
