# Runbook — Docker framework stack

> Issue #41

## Healthy

- Redis PING ok · NGINX `/healthz` · ATC/MCP `/health` when profile apps up.

## Failures

| Symptom | Action |
|---------|--------|
| validate abort | Fix JSON/compose path; ensure tower checkout |
| redis unhealthy | Check volume/network `hath0r-net` |
| nginx port bind | Adjust `HATH0R_NGINX_HOST_PORT` |
| missing images | Build/pull ATC/MCP local tags |

Secrets never in logs. Credentials: `/Users/raybayly/Development/.credentials/hath0r/.env`.
