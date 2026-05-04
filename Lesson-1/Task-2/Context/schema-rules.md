# Schema Rule Docs

## Customer and Order Schema
- `customers` table
  - `id` (UUID, PK)
  - `name` (text, required)
  - `email` (text, required, unique)
  - `created_at` (timestamp, default current timestamp)

- `orders` table
  - `id` (UUID, PK)
  - `customer_id` (UUID, FK -> customers.id)
  - `total_amount` (numeric, required, >= 0)
  - `status` (text, values: `pending`, `completed`, `cancelled`)
  - `order_date` (timestamp, required)

## Sales Schema
- `sales` table
  - `sale_id` (UUID, PK)
  - `sale_date` (timestamp, required)
  - `region` (text, required)
  - `amount` (numeric, required, >= 0)

## Naming rules
- Table and column names use `snake_case`.
- Foreign keys end with `_id`.
- Timestamps use `_at` or `_date` suffix.
- Aggregated values should be aliased clearly in queries.

## Validation rules
- Do not aggregate data before filtering invalid rows.
- Use `NULLIF(..., 0)` to prevent division-by-zero in computed ratios.
- For time windows, prefer `CURRENT_DATE - INTERVAL` in PostgreSQL.
- Group-by clauses must include all non-aggregated output columns.
