# Changelog

All notable changes to the **HATH0R Agentic Framework** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2026-10-02

### Taguchi Robust Optimization, FinOps Tokenizer Tax Auditor & Pixel-Native Vision

This major update introduces the Taguchi Robust Parameter Optimization Engine, FinOps Tokenizer Tax Auditor, Pixel-Native 2D Document Parsing, and DOM-Independent Playwright Visual Grounding.

### Added & Enhanced

- **Taguchi Robust Parameter Optimization Engine (`hath0r_engine.optimization.taguchi`) (#153, #154)**:
  - Ratified [ADR-007](docs/architect/hathor-adr-007-taguchi-techniques-robust-design-20261002.md) for Robust Parameter Design in Agentic Systems.
  - Implemented Orthogonal Array Testing Strategy (OATS) generators for $L_4, L_8, L_9, L_{12}, L_{18}$ matrices.
  - Signal-to-Noise Ratio (SNR) calculations across Nominal-is-Best, Smaller-is-Better, and Larger-is-Better criteria.
  - Taguchi Quadratic Quality Loss Function ($L(y) = k(y-m)^2$) for variance cost quantification.
- **FinOps Tokenizer Tax Auditor (`hath0r_engine.gateway.tokenizer_tax`) (#157, #158)**:
  - Ratified [ADR-008](docs/architect/hathor-adr-008-pixel-native-vision-tokenizer-tax-20261002.md) for Pixel-Native Vision Ingestion and Tokenizer Tax Auditing.
  - Pure-Python Unicode script classifier spanning Latin, Arabic, Devanagari, CJK, Cyrillic, Hebrew, and others.
  - Token inflation ratio ($\tau_{lang}$) and vocabulary parameter/VRAM overhead calculator ($P_{vocab} = 2 \cdot V \cdot d_{model}$).
  - Continuous visual patch budget equivalent calculator.
- **Pixel-Native 2D Document Parsing & Playwright Grounding (`hath0r_engine.vision`) (#159)**:
  - `DocumentLayoutParser.parse_pixel_native` preserving 2D table cell matrices and diagram topologies without OCR licenses.
  - `VisualGroundingEngine.ground_to_playwright_step` translating natural language element directives directly into Playwright-compliant coordinate action steps.
  - Added `coordinates` and `bounding_box` fields to `PlaywrightStep` in `src/hath0r_engine/testing/models.py` and `contracts/hath0r-playwright-test-spec-v1.schema.json`.
- **Comprehensive Verification**:
  - Full test suite expanded to 178 unit and integration tests passing across all cognitive modules.

---

## [1.0.1] - 2026-09-30

### Advanced Cognitive Engine, Temporal RAG & Tri-Graph Substrates

This release introduces the complete next-generation cognitive architecture for Hath0r, adding temporal graph memory, dynamic tool routing, multi-provider AI gateway tiering, pre-execution guardrails, DSPy declarative pipelines, durable replayable workflows, generative UI evidence handshakes, zero-trust compute sandboxes, and unified agent governance.

### Added & Enhanced

- **Temporal Knowledge Graphs & Letta Memory Substrate (#126)**:
  - Temporal graph edges with `valid_from`, `valid_to`, `is_current`, and point-in-time validity filtering `is_valid_at(as_of)`.
  - Letta-compatible `MemoryPagingManager` and `ReflectionEngine.consolidate_sleep_cycle`.
- **Dynamic Semantic Tool Router & Context Schema Pruning (#127)**:
  - Hybrid BM25 + dense vector tool ranking (`DynamicToolRouter`) for massive MCP server swarms.
  - Aggressive context compression via `SchemaPruner` (`AGGRESSIVE`, `STANDARD`, `MINIMAL`, `NONE`).
  - Caller identity tracking and OpenTelemetry metrics (`MCPRoutingTelemetry`).
- **Zero-Trust Isolated Compute Sandboxes (#128)**:
  - Pluggable provider hierarchy (`E2BSandboxProvider`, `DaytonaSandboxProvider`, `LocalSandboxProvider`) with zero-trust network egress controls managed via `SandboxManager`.
- **Durable Orchestration & Event-Sourced Replay Engine (#129)**:
  - SQLite-backed append-only `EventJournal` with deterministic step memoization and crash recovery in `DurableWorkflowEngine`.
  - Zero-compute human suspension with `HumanHibernationGate` and `@durable_task` decorator.
- **Multi-Provider AI Gateway & Tiered Routing (#130)**:
  - Universal gateway adapter `AIGatewayClient` with dynamic tiered model routing (`LIGHT`, `STANDARD`, `REASONING`).
  - Cosine-similarity `SemanticCache` with FinOps token and cost savings tracking.
- **Declarative Agent Pipelines with DSPy Module Compilation (#131)**:
  - Typed declarative `Signature` with `InputField` and `OutputField`.
  - Programmatic invariant validation and auto-correction (`Assert`, `Suggest`, `validate_json_contract`).
  - Step-by-step reasoning modules (`ChainOfThought`, `Predictor`) and teleprompter compilation (`BootstrapFewShotCompiler`).
- **Deterministic Pre-Execution Tool Guardrails (#132)**:
  - Static Python AST analyzer (`SyntaxGuardrail`) preventing unauthorized execution, destructive shell scripts, and SQL drops.
  - Automated in-flight parameter coercion (`SchemaRepairEngine`) and `HumanEscalationAuditHook`.
- **Generative UI & Evidence Handshake Protocol (#133)**:
  - Structured dashboard streaming cards (`DiffViewer`, `TestBadge`, `ParameterSlider`, `CryptoSignoffCard`).
  - Bi-directional state synchronization (`BiDirectionalStateSync`) and cryptographic HMAC SHA-256 sign-offs (`generate_cryptographic_signature`).
- **Agent Governance & CLI-First RAG Doctrine (#142)**:
  - Formally codified `CR-RAG-RETRIEVAL-001` and `CR-SUBSTRATE-001` across `AGENTS.md` and all subsystem contexts.
  - Added `docs/governance/strategies/` and `docs/governance/playbooks/` specifications.

---

## [1.0.0] - 2026-09-29

### Official 1.0.0 Release — Enterprise Agentic Framework & Standalone CLI Operator

This is the first major official production release of the **HATH0R Agentic Framework**, providing an enterprise multi-agent orchestration architecture, canonical Tri-Graph intelligence substrate, and zero-dependency standalone CLI binaries across all major platforms.

### Key Highlights & Features

- **Cross-Platform Standalone CLI Binaries (`release/`)**:
  - macOS Apple Silicon (`hath0r-darwin-arm64`)
  - macOS Intel (`hath0r-darwin-x86_64`)
  - Linux ARM64 (`hath0r-linux-arm64`)
  - Linux x86_64 (`hath0r-linux-x86_64`)
  - Windows x64 (`hath0r-windows-x64.cmd`)
  - Verified SHA-256 integrity checksums in [`release/CHECKSUMS.sha256`](release/CHECKSUMS.sha256).

- **Tri-Graph Agentic Substrate**:
  - **KnowledgeGraph (KG)**: Structured semantic nodes, taxonomy hierarchies, and relationships indexing enterprise corpus knowledge.
  - **ContextGraph (CG)**: Real-time context framing, dynamic scoping, and prompt boundary governance.
  - **MemoryGraph (MG)**: Persistent long-term agent memory storage with SQLite backing, embedding indexing, and 143 governance documents ingested.

- **Unified Architectural Subsystems**:
  - `contracts/`: JSON schemas, exit codes, and interface definitions for all bot and agent interactions.
  - `lib/`: Portable runtime libraries including JEV tool-guard system, MemoryGraph persistence, and graph indexing.
  - `docs/`: Canonical 143-document governance, architecture, developer, and sales documentation corpus.
  - `cfg/`: Multi-agent configuration, observability presets, and feature flags.
  - `tests/`: 100% passing test suite across all architectural subsystems.

- **Operator Governance & Promotion**:
  - Fully automated `local → development → testing → staging → master` promotion path with strict CI enforcement.
  - Release tagging, branch governance, and automated validation.
