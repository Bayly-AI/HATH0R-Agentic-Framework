# Suite standards (member pointer)

> Product: **HATH0R-Agentic-Framework** · Group: `hath0r-opensource`  
> Control tower: [`Bayly-AI/HATH0R-CLI`](https://github.com/Bayly-AI/HATH0R-CLI) · branch `development`  
> Fan-out issues: #43–#48, #41 · Tower epic: HATH0R-CLI #58–#63 / PR #111

This repository **adopts** suite governance from the control tower. Canonical prose lives on the tower `development` branch; this product keeps **local stubs** (`cfg/`), **agent rules** (`AGENTS.md`), and short pointers so agents resolve the right source of truth.

## Canonical tower URLs (`development`)

| Standard | Control-tower document |
|----------|------------------------|
| OpenObservation | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/openobservation-standards.md |
| OpenFeature | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/openfeature-standards.md |
| OpenTelemetry | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/opentelemetry-standards.md |
| CLI-first | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/cli-first-rules.md |
| Workflow documentation | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/workflow-documentation-standard.md |
| Docker group | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/docker-group-standard.md |
| Semantic versioning | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/semantic-versioning.md |
| MCP configuration | https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/mcp-configuration.md |
| Agent RAG & CLI-First Doctrine | `docs/governance/strategies/agent-rules-rag-cli-first-strategy.md` |
| Generative UI Evidence Handshake | `docs/governance/strategies/generative-ui-evidence-handshake-strategy.md` |
| Deterministic Tool Guardrails | `docs/governance/strategies/deterministic-tool-guardrails-strategy.md` |
| Declarative DSPy Agent Pipelines | `docs/governance/strategies/declarative-dspy-pipeline-strategy.md` |
| AI Gateway Tiered Routing | `docs/governance/strategies/ai-gateway-tiered-routing-strategy.md` |
| Durable Workflow Replay Engine | `docs/governance/strategies/durable-execution-checkpointing-strategy.md` |
| Zero-Trust Sandbox Isolation | `docs/governance/strategies/isolated-compute-sandbox-strategy.md` |
| Dynamic MCP Tool Router & Pruning | `docs/governance/strategies/dynamic-mcp-tool-router-strategy.md` |
| Temporal Knowledge Graphs | `docs/governance/strategies/temporal-knowledge-graph-strategy.md` |

## Local product stubs

| Concern | Local path | Notes |
|---------|------------|-------|
| OTel | `cfg/observability/otel.json` | `service_name`: `hath0r-framework` |
| OpenObservation | `cfg/observability/openobservation.json` | Framework SLIs; spool under `.hath0r/spool` |
| OpenFeature | `cfg/feature-flags/openfeature.json` | In-memory default provider |
| Feature catalog example | `cfg/feature-flags/catalog.example.json` | Non-secret examples only |
| Docker group pointer | `cfg/docker/groups/hath0r/README.md` | Compose lives on tower |
| Docker workflows | `cfg/docker/workflows/*.json` | Hathor validate → factory execute |
| MCP servers | `cfg/mcp.servers.json` | Project MCP priority `1` |
| Suite / product | `cfg/suite.yaml`, `cfg/product.yaml` | Orientation stubs |
| Adopt audit | `.hath0r/ADOPT_AUDIT.md` | Hathor adopt checklist evidence |

## Operator entry

Use **`hath0r`** (control-tower CLI) for doctor, MCP check, docker workflow validate, factory validate, and suite orientation. Do not invent ad-hoc scripts when a CLI path exists (see `cli-first-rules.md` pointer and `AGENTS.md` cr-cli-first-001).

## Secrets

Never commit secrets. Credentials only under `/Users/raybayly/Development/.credentials/<service>/.env`.
