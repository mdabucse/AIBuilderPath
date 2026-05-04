# Infrastructure Troubleshooting Guide

## Docker / Container issues
- `docker build` fails with missing dependency:
  - Confirm `requirements.txt` is copied before dependency installation.
  - Use `pip install --no-cache-dir -r requirements.txt`.
- Container exits immediately:
  - Check the final `CMD` or entrypoint.
  - Confirm the app listens on the exposed port.
- Health check fails:
  - Ensure `/health` returns a 200 response.
  - Check `HEALTHCHECK` command syntax and container network.

## Kubernetes issues
- Pod stuck in `CrashLoopBackOff`:
  - Inspect pod logs with `kubectl logs`.
  - Confirm the container user has permission to read needed files.
- Deployment not rolling out:
  - Check `kubectl rollout status deployment/<name>`.
  - Verify `maxUnavailable` and `maxSurge` values.
- Service not reachable:
  - Confirm service selectors match pod labels.
  - Confirm port names and target ports are correct.

## CI/CD pipeline issues
- Workflow fails on dependency install:
  - Use cached pip packages and pin versions.
  - Ensure the correct Python version is selected.
- Build step passes but deploy step does not:
  - Confirm secrets are configured in the repository.
  - Confirm the `if: github.ref == 'refs/heads/main'` condition matches the branch.

## Troubleshooting principles
- Reproduce the issue locally first.
- Check logs before changing configuration.
- Use smallest possible change to isolate the failure.
- Prefer explicit error messages and documented behavior.
