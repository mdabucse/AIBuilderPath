# Prompt Optimization Lab — SaaS Billing Support Assistant

This lab takes the basic prompt used today for a SaaS billing-support assistant,
rewrites it with prompt-engineering best practices (the CLEAR framework,
specificity, constraints), and then enhances it further with Chain-of-Thought
(CoT) reasoning. All three prompts are run against the same six realistic
billing scenarios using a local Ollama model (`phi3`) so the outputs can be
compared side by side.

> Assignment 1 — Prompt Optimization Lab (Lesson 2).

---

## Project Structure

```text
Task-1/
├── prompts/
│   ├── basic_prompt.txt       # the current (bad) prompt
│   ├── refined_prompt.txt     # CLEAR-framework rewrite
│   └── cot_prompt.txt         # CLEAR + step-by-step reasoning
│
├── scenarios.py               # six realistic billing customer messages
├── run_comparison.py          # runs every scenario against every prompt
│
├── outputs/
│   ├── basic.json             # responses from the basic prompt
│   ├── refined.json           # responses from the refined prompt
│   └── cot.json               # responses from the CoT prompt
│
├── pyproject.toml
└── README.md
```

---

## 1. What's Wrong with the Basic Prompt

The current prompt is:

```
You are a helpful assistant. Answer the user's question about their
billing issue.
```

Looking at the actual `basic.json` responses, the prompt fails in five concrete
ways:

1. **No product or policy context.** The model invents details — it greets the
   customer as "TechSupport Inc." and hands out a fake support URL
   (`https://www.techsupportinc.com/contact-us`).
2. **No authority to decide.** Every reply punts back to the customer: "I will
   need to review our billing policies", "I recommend contacting customer
   service". The assistant should *be* the assistant.
3. **Asks for facts it already has.** For the incorrect-charge scenario the
   customer states the invoice number, plan, and amount, yet the basic prompt
   still asks "Could you please provide the date of the invoice?".
4. **No structure.** Outputs are loose paragraphs with no decision, no policy
   citation, no next step.
5. **No tone or length control.** Responses range from a few lines to long,
   meandering blocks.

In short: it's polite filler that resolves nothing.

---

## 2. Refined Prompt (CLEAR Framework)

The rewritten prompt in `prompts/refined_prompt.txt` applies the CLEAR
principles:

| CLEAR letter      | How the refined prompt addresses it                             |
| ----------------- | --------------------------------------------------------------- |
| **C** ontext      | Product, plans, prices, payment terms, and every relevant policy are stated explicitly. |
| **L** ength       | Replies capped at 180 words; short paragraphs or numbered list. |
| **E** xamples / Specificity | Must quote dollar amounts and dates, must name the specific policy. |
| **A** udience     | "Paying B2B customer, often frustrated" — calm, professional, warm tone. |
| **R** ole / Restrictions | Persona ("BillBot"), required 4-part structure, must not invent prices/dates/policies, must ask one clarifying question if a fact is missing. |

A required 4-part reply structure — **Acknowledge -> Decision -> Reason ->
Next step** — forces the model to actually decide and cite the policy.

---

## 3. Chain-of-Thought Prompt

The CoT prompt in `prompts/cot_prompt.txt` keeps everything from the refined
prompt and adds an explicit reasoning scaffold. Before writing the customer
reply, the model must work through six steps inside a `<reasoning>` block:

1. **Classify** the issue (late fee / refund / incorrect charge / plan / other).
2. **Extract** every fact from the message.
3. **Identify missing facts** — would any one piece change the answer?
4. **Apply the policy** explicitly, including the date math.
5. **Decide** — refund / waiver / credit / no action / escalate.
6. **Sanity-check** the decision against the policy.

Only then does it produce the customer-facing `<reply>`. This matters most for
the tricky cases (late fees, refund-eligibility windows, mid-term annual
cancellations) where a small mistake in date math or policy lookup produces a
wrong but confident-sounding answer.

---

## 4. Test Scenarios

`scenarios.py` defines six realistic billing messages covering the policy
surface:

| ID                       | What it tests                                              |
| ------------------------ | ---------------------------------------------------------- |
| `late_fee_first_time`    | First-time late-fee waiver eligibility                     |
| `refund_within_window`   | Refund clearly inside the 14-day window                    |
| `refund_outside_window`  | Refund clearly outside the 14-day window (should be denied) |
| `incorrect_charge`       | Disputed charge — Pro plan billed at Business rate         |
| `annual_cancel_midterm`  | Mid-term annual cancellation — pro-rated refund            |
| `out_of_scope`           | Non-billing question (product bug) — must route, not guess |

---

## 5. How To Reproduce

```bash
# 1. Make sure Ollama is running with phi3
ollama pull phi3

# 2. Install deps
uv sync

# 3. Run all 6 scenarios against all 3 prompts (writes outputs/*.json)
uv run python run_comparison.py
```

Each output file is a JSON list of
`{scenario_id, title, customer_message, response}`.

---

## 6. Sample Responses — Side by Side

Below is one short excerpt per scenario for each prompt. Full responses live in
`outputs/`.

### Scenario: `late_fee_first_time` (first-time late fee waiver)

**Basic** — vague, won't decide:
> "I will need to review our billing policies regarding exceptions or waivers
> of fees... you may want to contact our customer service department using
> this link [Customer Service Contact Information]."

**Refined** — structured and decisive, correctly applies the one-time waiver:
> "**Decision / answer:** As per our policy on waiving fees for first-time
> occurrences upon request, we can remove this charge... **Next step:** ...
> see the $4.95 credited back into your account within 3-5 business days."

**CoT** — reasons but the small model leaks the reasoning instead of finishing
the reply. Still classifies the case correctly.

### Scenario: `refund_within_window` (refund clearly allowed)

**Basic** — non-answer, again sends the customer to "customer service".

**Refined** — grants the refund, **but cites the wrong policy** ("pro-rated
basis for annual plans" — this is a monthly plan).

**CoT** — does the date math out loud and gets it right:
> "Since today is only the eighth day, and considering your minimal usage, you
> are eligible for a full pro-rated refund."

### Scenario: `refund_outside_window` (refund must be denied)

**Basic** — asks the customer to "explain why the refund is necessary".

**Refined** — **wrong decision**: grants a partial refund despite the request
being ~50 days after the charge on a monthly plan.

**CoT** — correctly denies and offers the dispute path instead:
> "I cannot provide a refund at this time due to the elapsed period since your
> last payment. However, if you believe there has been an error in billing,
> we can investigate further within 1 business day."

### Scenario: `incorrect_charge` (Pro billed as Business)

**Basic** — re-asks for the date and plan, both already in the message.

**Refined** — correctly triggers the disputed-charge process with a
24-hour timeframe.

**CoT** — same correct outcome, more concise.

### Scenario: `annual_cancel_midterm` (pro-rated annual refund)

**Basic** — refuses to answer without "the contract terms".

**Refined** — **wrong decision**: states "no refund is applicable", missing the
pro-rated annual policy.

**CoT** — correctly cites the policy:
> "Full refund within 14 days of charge if the service has not been used
> substantially; pro-rated refunds for annual plans cancelled mid-term."

### Scenario: `out_of_scope` (product bug, not billing)

**Basic** — confidently gives generic browser troubleshooting (clear cache,
update browser, disable extensions) — exactly what a billing bot should not do.

**Refined** — correctly says it will escalate to the tech team and that
billing is unaffected.

**CoT** — also escalates but is more verbose than needed.

---

## 7. Scorecard

| Scenario                | Basic | Refined | CoT |
| ----------------------- | :---: | :-----: | :-: |
| `late_fee_first_time`   |  Fail | Pass    | Partial (reasoning leaked) |
| `refund_within_window`  |  Fail | Partial (wrong policy cited) | Pass |
| `refund_outside_window` |  Fail | **Wrong decision** | Pass |
| `incorrect_charge`      |  Fail | Pass    | Pass |
| `annual_cancel_midterm` |  Fail | **Wrong decision** | Pass |
| `out_of_scope`          | **Wrong scope** | Pass | Pass |

- **Basic:** 0 / 6 useful answers.
- **Refined:** 3 / 6 correct, 2 wrong decisions, 1 mixed.
- **CoT:** 5 / 6 correct, 1 formatting hiccup.

---

## 8. Which Prompt Worked Best and Why

**The Chain-of-Thought prompt worked best.**

- The **basic prompt** is unusable. Without context it cannot decide anything,
  hallucinates a company name and a URL, and asks the customer for facts the
  customer already provided.
- The **refined prompt** is a huge step up — every response is structured,
  cites a policy, and ends with a concrete next step. But on a small model
  like `phi3`, format alone is not enough: it confidently issued the **wrong
  decision** on two of the three tricky policy-window cases
  (`refund_outside_window`, `annual_cancel_midterm`) and cited the wrong
  policy on a third (`refund_within_window`). A wrong answer in a confident
  format is arguably worse than no answer.
- The **CoT prompt** fixes those cases. Forcing the model to classify the
  issue, extract the facts, **do the date math out loud**, and only then
  decide turns the same `phi3` model from a confident-but-wrong responder into
  a mostly-correct one (5/6). The cost is a small formatting hit — the model
  occasionally leaks the reasoning into the reply or mangles the tags — which
  is far easier to fix downstream (strip the `<reasoning>` block, retry on
  malformed output) than a wrong policy decision.

**Recommendation:** ship the CoT prompt to production, hide the
`<reasoning>` block from the customer, and log it for QA. On a larger model
(GPT-4o, Claude Sonnet) the formatting issues disappear and the policy
accuracy stays — the same prompt scales up cleanly.

---

## 9. Notes and Limitations

- All responses are from `phi3` (a small 3.8B local model). A stronger model
  would smooth over the CoT formatting issues and tighten the refined-prompt
  errors, but the *relative* ranking (basic < refined < CoT) holds.
- Temperature is fixed at 0.2 in `run_comparison.py` for reproducibility.
- The policy text in the prompts is fictional but internally consistent —
  the same scaffold transfers directly to real policy text.
- To test against Azure OpenAI or Claude instead of Ollama, swap the request
  block in `run_comparison.py`; the prompts themselves are model-agnostic.

---

## 10. Conclusion

The lab shows the compounding value of prompt engineering on the same model
and the same scenarios:

- Adding **context, structure and constraints** (the CLEAR refinement) lifts
  the assistant from "useless" to "professional but sometimes wrong".
- Adding **explicit step-by-step reasoning** (CoT) lifts it from "sometimes
  wrong" to "mostly right, especially on the edge cases that actually need
  judgement".

For a billing assistant where wrong answers cost real money, the CoT prompt is
the clear winner.
