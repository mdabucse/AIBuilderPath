# Presidio — AI Data Handling & Compliance Policy

**Effective date:** January 1, 2026  
**Owner:** Chief Compliance Officer  
**Applies to:** All employees, contractors, and approved AI systems

## 1. Purpose

Presidio uses artificial intelligence to improve customer service, underwriting support, and internal research. This policy defines how employee and customer data may be collected, processed, stored, and shared in AI workflows.

## 2. Scope

This policy covers:

- Internal research agents and copilots
- Customer-facing chatbots
- Model training, fine-tuning, and RAG knowledge bases
- Third-party LLM and embedding providers

## 3. Data classification

| Class | Examples | AI usage |
| --- | --- | --- |
| Public | Marketing brochures, published rates | Allowed in any approved tool |
| Internal | HR handbooks, internal benchmarks | Allowed only in approved internal systems |
| Confidential | Claims files, underwriting notes | Masked or excluded from external LLMs |
| Restricted | SSN, payment card data, PHI | **Never** sent to external AI services |

## 4. Approved AI practices

Employees **may**:

- Use approved internal agents to search HR and compliance documents
- Summarize de-identified customer feedback for quarterly reviews
- Compare hiring metrics against public industry benchmarks

Employees **must not**:

- Paste restricted or confidential data into public chatbots
- Train models on customer PII without Legal and Security sign-off
- Bypass data-loss-prevention controls

## 5. Retention and audit

- Prompts and outputs from production agents are retained for **90 days** for audit.
- RAG indexes must be rebuilt when underlying policy documents change.
- All new AI tools require Security review before production use.

## 6. Incident reporting

Suspected data leakage into an unapproved AI system must be reported to **security@presidio.com** within **24 hours**.

## 7. Related policies

- Information Security Policy (ISP-001)
- Acceptable Use Policy (AUP-003)
- Vendor Risk Management (VRM-012)
