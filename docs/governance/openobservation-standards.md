# OpenObservation standards (framework pointer)

> Issue: #43 · Canonical: [HATH0R-CLI openobservation-standards.md](https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/openobservation-standards.md)

## Local cfg

- `cfg/observability/openobservation.json` — golden signals, SLIs, spool `.hath0r/spool`
- Spool policy: never block request path; never write secrets

## Adherence

1. Emit / plan for latency, traffic, errors, saturation on framework surfaces.
2. Prefer control-tower playbooks/runbooks for ops:
   - https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/playbooks/openobservation-setup-playbook.md
   - https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/runbooks/openobservation-ops-runbook.md
3. Alert hooks via env only (`HATH0R_OBSERVATION_WEBHOOK_URL`).

See also `docs/governance/SUITE_STANDARDS.md`.
