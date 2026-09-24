# Docker group standard (framework pointer)

> Issue: #48 · Canonical: [HATH0R-CLI docker-group-standard.md](https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/docker-group-standard.md)

## Topology (OpenSource / 1-Nation pattern)

| Role | Component | Notes |
|------|-----------|-------|
| Shared state | Redis | `HATH0R-Redis` |
| Shared edge | NGINX | `HATH0R-NGINX` |
| Config manager | ATC | profile `apps` |
| Tools | MCP | profile `apps` |
| Experience | UXP | profile `apps` when present |

## Canonical compose (control tower)

Do **not** fork large compose trees here. Canonical group template:

- https://github.com/Bayly-AI/HATH0R-CLI/blob/development/cfg/docker/groups/hath0r/docker-compose.yml
- Local pointer: `cfg/docker/groups/hath0r/README.md`

## Operator

```bash
# From HATH0R-CLI checkout (control tower)
docker compose -f cfg/docker/groups/hath0r/docker-compose.yml up -d redis nginx
docker compose -f cfg/docker/groups/hath0r/docker-compose.yml --profile apps up -d

# Validate workflow JSON (member or tower)
hath0r docker workflow validate cfg/docker/workflows/hath0r-framework-stack.json
```

Secrets: `Development/.credentials/hath0r/.env` only — never commit.
