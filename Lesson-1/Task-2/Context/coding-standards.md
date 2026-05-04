# Coding Standards

## Python
- Use `snake_case` for variables and functions.
- Use `PascalCase` for classes.
- Keep line length under 88 characters.
- Prefer type hints for public functions and data structures.
- Use `pathlib.Path` for file paths.
- Use `try/except` blocks only for expected errors.
- Validate user input early and return clear error messages.
- Use `logging` instead of `print` for server-side applications.

## JavaScript / TypeScript
- Use `camelCase` for variables and functions.
- Use `PascalCase` for React components.
- Prefer `const` for values that do not change and `let` only when reassignment is needed.
- Use functional React components and hooks (`useState`, `useEffect`).
- Keep state minimal and derive it when possible.
- Add explicit return types for exported functions in TypeScript.
- Avoid inline styles when the component behavior is more important than exact visuals.

## Infrastructure as Code
- Use descriptive resource names.
- Keep secrets and credentials out of repository YAML files.
- Use health checks for all production workloads.
- Define resource requests and limits for containers.
- Use rolling updates for deployments.
- Prefer `readOnlyRootFilesystem: true` and drop unnecessary capabilities.
- Use non-root service accounts or users when possible.

## Documentation Style
- Write short, precise sentences.
- Use bullet lists for requirements and constraints.
- Add examples only when they clarify behavior.
- Clearly label inputs, outputs, and expected responses.
