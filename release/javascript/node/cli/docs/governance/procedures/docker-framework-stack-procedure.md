# Procedure — Docker framework stack

> Workflow: `cfg/docker/workflows/hath0r-framework-stack.json` · Issue #41

1. Confirm control-tower checkout has `cfg/docker/groups/hath0r/docker-compose.yml`.
2. Load env from `Development/.credentials/hath0r/.env` (never commit).
3. Run `hath0r docker workflow validate` on the member workflow JSON.
4. Execute via Docker Factory: validate → up (detach) → healthcheck (atc, mcp, redis, nginx).
5. On failure: abort, capture logs, follow runbook.
