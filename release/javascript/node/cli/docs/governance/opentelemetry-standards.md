# OpenTelemetry standards (framework pointer)

> Issue: #45 · Canonical: [HATH0R-CLI opentelemetry-standards.md](https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/opentelemetry-standards.md)

## Local cfg

- `cfg/observability/otel.json`
  - `resource.service_name`: `hath0r-framework`
  - `resource.service_namespace`: `hath0r-opensource`
  - OTLP endpoint via `OTEL_EXPORTER_OTLP_ENDPOINT` (default `http://localhost:4318`)

## Adherence

1. Resource attributes identify this product (`hath0r-framework`), not the CLI.
2. Headers/secrets only via env (`OTEL_EXPORTER_OTLP_HEADERS`); credentials root `/Users/raybayly/Development/.credentials`.
3. Tower setup/ops:
   - https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/playbooks/opentelemetry-setup-playbook.md
   - https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/runbooks/opentelemetry-ops-runbook.md

See also `docs/governance/SUITE_STANDARDS.md`.
