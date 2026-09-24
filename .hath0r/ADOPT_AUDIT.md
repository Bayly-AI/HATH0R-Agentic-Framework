# Hathor adopt audit — HATH0R-Agentic-Framework

> Updated: 2026-09-24 · Fan-out issues #41, #43–#48 · Control tower PR Bayly-AI/HATH0R-CLI#111

| Check | Status | Evidence |
|-------|--------|----------|
| Hidden root `.hath0r/` only | OK | `.hath0r/` present; no `.ai/` / `.aegis/` / `.infraOS/` |
| Knowledgebase stub | OK | `.hath0r/knowledgebase/README.md` → group hub |
| `VERSION` SemVer | OK | root `VERSION` = `0.2.0` · `docs/governance/semantic-versioning.md` |
| Product runbook | OK | `docs/runbook.md` |
| Init playbook | OK | `docs/developers/hathor-playbook-001-repo-init-setup-20260919.md` |
| Suite / product cfg | OK | `cfg/suite.yaml`, `cfg/product.yaml`, `cfg/knowledge-tower.yaml` |
| MCP project-first | OK | `cfg/mcp.servers.json` — `hath0r-mcp` priority `1` |
| OTel stub | OK | `cfg/observability/otel.json` (`service_name`: `hath0r-framework`) |
| OpenObservation stub | OK | `cfg/observability/openobservation.json` |
| OpenFeature stub | OK | `cfg/feature-flags/openfeature.json` |
| Suite standards index | OK | `docs/governance/SUITE_STANDARDS.md` |
| Docker group pointer | OK | `cfg/docker/groups/hath0r/README.md` → tower compose |
| Docker workflow JSON | OK | `cfg/docker/workflows/hath0r-framework-stack.json` |
| CLI-first agent rule | OK | `AGENTS.md` cr-cli-first-001 + `docs/governance/cli-first-rules.md` |
| Contracts pin | NOTE | Prefer pin via control-tower contracts inventory when refreshing UPL; no large binaries in-repo |
| Control tower cfg pointers | OK | `docs/governance/SUITE_STANDARDS.md` GitHub `development` URLs |

## Gaps / follow-ups

- Full compose/nginx assets remain on **HATH0R-CLI** (intentional; avoid fork drift).
- Runtime OTel/OpenFeature SDK wiring is out of scope for this docs+cfg fan-out.
- Refresh contracts pin note when UPL/contracts issue opens on this product.
