# OpenFeature standards (framework pointer)

> Issue: #44 · Canonical: [HATH0R-CLI openfeature-standards.md](https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/openfeature-standards.md)

## Local cfg

- `cfg/feature-flags/openfeature.json` — default in-memory provider
- `cfg/feature-flags/catalog.example.json` — example flags only (no secrets)

## Adherence

1. Evaluate flags through OpenFeature-shaped config; fail-safe defaults on.
2. Provider options via `OPENFEATURE_PROVIDER_OPTIONS` env — never commit provider secrets.
3. Tower setup/ops:
   - https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/playbooks/openfeature-setup-playbook.md
   - https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/runbooks/openfeature-ops-runbook.md

See also `docs/governance/SUITE_STANDARDS.md`.
