"""Test scenarios for the prompt optimization lab.

Each scenario is a realistic billing message a customer might send. The three
prompts (basic / refined / CoT) are run against the same scenarios so the
outputs are directly comparable.
"""

SCENARIOS: list[dict] = [
    {
        "id": "late_fee_first_time",
        "title": "Late fee — first-time offender asking for a waiver",
        "message": (
            "Hi, I just noticed a $4.95 late fee on my invoice INV-10234 dated "
            "May 1. I paid on May 22 — yes, I missed the due date, but this is "
            "the first time it has ever happened in two years on the Pro plan. "
            "Can you remove the late fee?"
        ),
    },
    {
        "id": "refund_within_window",
        "title": "Refund request — inside the 14-day window",
        "message": (
            "I signed up for the Starter monthly plan on June 1 and was charged "
            "$29. I've barely logged in. Today is June 9 and I'd like to cancel "
            "and get a refund please."
        ),
    },
    {
        "id": "refund_outside_window",
        "title": "Refund request — outside the 14-day window",
        "message": (
            "I want a refund for my last month's $99 Pro charge. I was charged "
            "on April 1 and I'm only emailing now (May 20) because I forgot. I "
            "didn't use the product much last month."
        ),
    },
    {
        "id": "incorrect_charge",
        "title": "Incorrect / disputed charge",
        "message": (
            "My company is on the Pro plan ($99/mo) but my latest invoice "
            "INV-10987 charged me $299. I did not upgrade. Please fix this."
        ),
    },
    {
        "id": "annual_cancel_midterm",
        "title": "Annual plan cancellation mid-term — pro-rated refund",
        "message": (
            "We signed up for the Business annual plan in January and paid "
            "$2,990 up front. We need to cancel now (it's August). What "
            "refund are we entitled to?"
        ),
    },
    {
        "id": "out_of_scope",
        "title": "Out-of-scope question (product bug, not billing)",
        "message": (
            "My dashboard keeps crashing whenever I open the Reports tab. "
            "Can you fix it? Also, am I still being billed correctly while "
            "this is broken?"
        ),
    },
]
