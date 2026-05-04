# Model Context Test

## Instructions
1. Load all context files from `Context/*.md` into the model.
2. Ask each question below in the same session.
3. Confirm whether the answer references the provided context and follows the rules.
4. Record the result using the self-assessment rubric.

## Test question 1 — Coding standards
**Prompt:**
> Based on the coding standards file, rewrite the following function signature and explain why the change is needed:
> 
> ```python
> def ValidateUserData(USERDATA):
>     pass
> ```

**Expected answer:**
- Use `snake_case` for function names and parameters.
- Use `validate_user_data(user_data)`.
- Explain that `PascalCase` is reserved for classes and `snake_case` improves readability in Python.

## Test question 2 — Schema rules
**Prompt:**
> Using the schema rules document, write a PostgreSQL query to get the top 5 customers by total completed orders in the last 6 months. Include proper aliases and grouping.

**Expected answer:**
- A query that joins `customers` and `orders`.
- Filters `status = 'completed'` and `order_date >= CURRENT_DATE - INTERVAL '6 months'`.
- Uses `GROUP BY c.id, c.name, c.email`.
- Aliases totals clearly like `total_spent` and `number_of_orders`.

## Test question 3 — Infra troubleshooting
**Prompt:**
> The Kubernetes deployment is stuck in `CrashLoopBackOff` because the container cannot access files. What steps from the troubleshooting guide should you follow?

**Expected answer:**
- Check pod logs with `kubectl logs`.
- Confirm the container user has permission to read files.
- Verify the pod spec and security context.
- Mention the guide principle: reproduce locally and inspect logs first.

## Test question 4 — Product FAQ
**Prompt:**
> A user reports that a new order remains in `pending` after payment confirmation. Based on the FAQ, how should the API respond and which status codes are appropriate?

**Expected answer:**
- Explain that `pending` is the default status and should change to `completed` only after confirmation.
- If the API request is invalid, respond with `400` or `422` depending on the failure.
- Use `201` for successful creation and `500` only for server errors.

## Self-assessment rubric
- **Pass:** Model correctly references context and gives precise, context-aligned answers.
- **Partial:** Model answer is mostly correct but misses a context-specific detail.
- **Fail:** Model ignores the context or gives incorrect advice.

## Sample evaluation table
| Question | Result | Notes |
| --- | --- | --- |
| Coding standards | Pass | Used correct naming convention and rationale. |
| Schema rules | Pass | Reference to `CURRENT_DATE - INTERVAL '6 months'` and proper GROUP BY. |
| Infra troubleshooting | Partial | Mentioned logs but not permission checks. |
| Product FAQ | Pass | Correct status code guidance and behavior. |
