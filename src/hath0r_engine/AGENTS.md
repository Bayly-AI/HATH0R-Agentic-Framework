---
id: engine-core-subsystem
type: subsystem
title: Hath0r Cognitive Engine Core Subsystem
depends_on: [contracts-subsystem, lib-subsystem]
governed_by: [CR-CLI-ENTRY-001, CR-RAG-RETRIEVAL-001, CR-SUBSTRATE-001, CR-PLAYWRIGHT-UI-001, cr-branch-gov-001]
---
# Engine Core Subsystem — AGENTS Context

> **Subsystem Role:** Canonical cognitive substrate providing Tri-Graph memory, deterministic pre-execution guardrails, dynamic tool routing, AI gateway tiered routing, durable event replay, declarative DSPy pipelines, generative UI handshakes, Playwright UI testing, zero-trust sandboxes, and OpenTelemetry instrumentation.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`src/hath0r_engine/memory/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/memory/): `MemoryGraph`, `MemoryNode`, `MemoryEdge` (with temporal `valid_from`/`valid_to`), `MemoryPagingManager`, `ReflectionEngine`.
- [`src/hath0r_engine/guardrails/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/guardrails/): `GuardrailsManager`, `SyntaxGuardrail` (AST/SQL validator), `SchemaRepairEngine`, `HumanEscalationAuditHook`.
- [`src/hath0r_engine/mcp/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/mcp/): `DynamicToolRouter` (BM25 + vector ranking), `SchemaPruner`, `CallerIdentity`, `MCPRoutingTelemetry`.
- [`src/hath0r_engine/gateway/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/gateway/): `AIGatewayClient`, `TieredRouter` (`LIGHT`/`STANDARD`/`REASONING`), `SemanticCache`, `TokenizerTaxAuditor`, `TaxAuditReport`.
- [`src/hath0r_engine/orchestration/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/orchestration/): `DurableWorkflowEngine`, `EventJournal`, `HumanHibernationGate`, `@durable_task`.
- [`src/hath0r_engine/pipeline/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/pipeline/): `Signature`, `InputField`, `OutputField`, `ChainOfThought`, `Assert`, `BootstrapFewShotCompiler`.
- [`src/hath0r_engine/ui/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/ui/): `HandshakeSession`, `UIComponentBuilder`, `BiDirectionalStateSync`, `generate_cryptographic_signature`.
- [`src/hath0r_engine/testing/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/testing/): `PlaywrightMasterCatalogManager`, `PlaywrightTestRunner`, `PlaywrightTestCase`, `PlaywrightTestSuite`.
- [`src/hath0r_engine/optimization/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/optimization/): `TaguchiEngine`, `OrthogonalArray`, `Factor`, `ExperimentMatrix`, `calculate_snr`, `TaguchiLossFunction` (OATS & Robust Parameter Design).
- [`src/hath0r_engine/sandbox/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/sandbox/): `SandboxManager`, `E2BSandboxProvider`, `DaytonaSandboxProvider`, `LocalSandboxProvider`.
- [`src/hath0r_engine/telemetry/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/src/hath0r_engine/telemetry/): `OTELTracerBot`, `TelemetrySpan`.

## 2. Operating Constraints & Invariants
- All agent operations MUST perform pre-execution security checks via `GuardrailsManager`.
- Graph entities and relationships MUST support temporal queries with `is_valid_at(as_of)`.
- Model routing MUST use `TieredRouter` to optimize FinOps costs and leverage `SemanticCache`.
- Complex multi-step reasoning MUST be expressed declaratively via `Signature` and validated with `Assert`.
- Human release gates MUST produce cryptographic HMAC SHA-256 signatures via `generate_cryptographic_signature`.
- All UI components and visual changes MUST be covered by Playwright test cases registered in `tests/e2e/master-playwright-tests.json` and validated during clean repo.
