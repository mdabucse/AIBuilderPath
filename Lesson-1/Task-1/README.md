# AI Model Comparison — Assignment 1

## Models compared
- **GPT-4o** — OpenAI (`openai.json`)
- **Claude Sonnet** — Anthropic (`claude.json`)
- **Gemini Flash** — Google (`gemini.json`)
- **Local model** — local baseline output (`phi3.json`) representing a smaller model quality reference

## Use cases
- **AppDev**: Code Generation
- **Data**: Data Analysis & SQL Generation
- **DevOps**: Infrastructure Automation

## Comparison table
| Criteria | GPT-4o | Claude Sonnet | Gemini Flash | Local model (`phi3` / deepseek-r1:7b baseline) |
| --- | --- | --- | --- | --- |
| Code Quality | Excellent | Good | Good | Basic |
| SQL Generation | Excellent | Good | Good | Basic |
| Infra Automation | Excellent | Good | Good | Basic |
| Ease of Use | Excellent | Good | Good | Basic |
| Speed / Latency | Good (cloud) | Good (cloud) | Good (cloud) | Good (local) |
| Comments | Strong, production-ready code across FastAPI, React, auth, SQL, Docker/K8s. Best overall polish and discipline. | Solid responses, good structure, but some endpoints use 200 instead of 201 and less advanced validation detail. | Reliable standard output; good templates but fewer advanced refinements and notes than GPT-4o. | Functional baseline with working code, but simpler output and fewer production-quality safeguards. |

## Highlights by use case

### AppDev — Code Generation
- **GPT-4o**: Best overall. FastAPI endpoint uses proper `201` response, extensive validation, and clean error handling. React and auth examples are robust and production-ready.
- **Claude Sonnet**: Good quality and well-structured. The FastAPI example is correct, but it returns `200` instead of `201` for creation and lacks some higher-quality validation detail.
- **Gemini Flash**: Good standard implementation. Solid React component and auth function, but slightly less polished than GPT-4o.
- **Local model (`phi3`)**: Basic but usable. The FastAPI endpoint is simpler, React output is less feature-rich, and auth handling is more minimal.

### Data — Data Analysis & SQL Generation
- **GPT-4o**: Excellent SQL with aggregation, DISTINCT counting, rounding, and clear reasoning. The data cleaning pipeline is comprehensive and robust.
- **Claude Sonnet**: Good SQL output with correct joins and filtering; it is competent but not as extensive in notes or edge-case handling.
- **Gemini Flash**: Good SQL and data cleaning. It produces workable queries and pipeline code, though the output is more straightforward than GPT-4o.
- **Local model (`phi3`)**: Basic SQL and pandas cleaning. Functional, but not as strong in optimization and advanced query detail.

### DevOps — Infrastructure Automation
- **GPT-4o**: Excellent Docker/Kubernetes examples with strong security, multi-stage build, non-root user, healthchecks, and capacity planning. Best automation readiness.
- **Claude Sonnet**: Good deployment automation examples. Solid Dockerfile and Kubernetes manifest, but less layered optimization than GPT-4o.
- **Gemini Flash**: Good, stable infrastructure templates. The Docker and GitHub Actions examples are sensible, though not as advanced in security hardening.
- **Local model (`phi3`)**: Basic automation. The Dockerfile works but is simpler and uses fewer production-grade best practices.

## Notes
- The local model reference here is based on the available `phi3.json` output and serves as the lower-cost/local baseline for comparison.
- For a public GitHub submission, attach this file to your repository and share the repo URL.

## Recommendation
- Use **GPT-4o** for highest-quality code generation and infrastructure automation.
- Use **Claude Sonnet** or **Gemini Flash** when you need reliable cloud-powered assistance with good structure.
- Use the **local model** only for quick local experimentation or when cloud access is restricted; it is helpful, but not as polished.
