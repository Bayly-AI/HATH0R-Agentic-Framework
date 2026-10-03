# Workflow documentation standard (framework pointer)

> Issue: #47 · Canonical: [HATH0R-CLI workflow-documentation-standard.md](https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/workflow-documentation-standard.md)

## Requirement

Every durable workflow (factory, Docker workflow, operator procedure) MUST have matching documentation types as defined on the control tower:

- procedure
- strategy
- playbook
- runbook
- checklist
- test-doc (or explicit test plan section)

## Local practice

1. Prefer linking/extending tower docs over duplicating large prose.
2. Framework-specific ops: `docs/runbook.md`, `docs/governance/playbooks/`, `docs/governance/checklists/`.
3. Docker workflow JSON under `cfg/docker/workflows/` must reference or ship the doc set (or pointer) before marking the workflow production-ready.
4. Gap-fill for new workflows: create the six doc types (short stubs OK) before implementation code.

## Tower inventory & templates

See control-tower `docs/governance/{procedures,strategies,playbooks,runbooks,checklists}/` on `development`.
