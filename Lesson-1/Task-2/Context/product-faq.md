# Product FAQs

## What does the product do?
- The product is a web-based order management system.
- It tracks customers, orders, and sales performance.
- It includes an API backend, a frontend user interface, and deployment automation.

## Who are the users?
- App developers building new features.
- Data analysts creating reports and dashboards.
- DevOps engineers deploying and monitoring infrastructure.

## Common feature questions
- Q: What is the default order status?
  - A: New orders start with status `pending` and move to `completed` only after payment is confirmed.
- Q: How are sales totals calculated?
  - A: Sales totals come from the `amount` field on the `sales` table and should always be numeric and non-negative.
- Q: What happens if a customer email is duplicated?
  - A: Duplicate emails are not allowed; such requests should be rejected as invalid.

## Support expectations
- Always provide a clear validation error for bad input.
- Use standard HTTP codes: `201` for creation, `400` for bad requests, `422` for validation failures, and `500` for internal errors.
- Keep infrastructure manifests secure and avoid leaking secrets in YAML.
