# Checklist — Docker framework stack

> Issue #41 · Test plan section satisfies workflow test-doc requirement

- [ ] Workflow JSON present under `cfg/docker/workflows/`
- [ ] Docs set linked (procedure/strategy/playbook/runbook/checklist)
- [ ] Compose resolved from control tower
- [ ] `hath0r docker workflow validate` passes
- [ ] No secrets in repo
- [ ] Healthcheck services listed: atc, mcp, redis, nginx
