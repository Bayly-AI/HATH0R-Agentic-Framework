# HATHOR Framework — Technical Architecture & Engine Reference

> Language-agnostic agentic application framework and cognitive substrate for the Enterprise Agentic Platform.

---

## 🛠️ Developers Working on HATH0R-CLI & Core Framework

This document contains deep technical specifications, Tri-Graph substrate data structures, repository layouts, binary build pipelines, and cognitive engine modules for developers building or extending `hath0r`, `hath0r-framework`, and `hath0r-engine`.

> **Looking to install and use Hath0r in your own projects?**  
> You only need the **HATH0R CLI** (`hath0r`). Download pre-compiled standalone binaries in [`release/`](release/) or see the [CLI Quick Start](#-quick-start-operators--users) below.

---

## 🚀 Quick Start: Operators & Users

The Hath0r CLI is distributed as a zero-dependency standalone binary for macOS, Linux, and Windows:

```sh
# Option 1: Direct Standalone Binary (Zero Setup Required)
chmod +x release/hath0r-darwin-arm64
./release/hath0r-darwin-arm64 doctor
./release/hath0r-darwin-arm64 init

# Option 2: Python / pipx package
pipx install hath0r-cli
hath0r doctor
hath0r init
```

---

## 🏗️ Architecture at a Glance

```text
Operator / Human Developer / Autonomous Agent
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│                   HATH0R Operator CLI                  │
├────────────────────────────────────────────────────────┤
│ • Execution Engine (`step_runner`, `factories`)        │
│ • Elevation of Authority (`guest` → `sovereign`)       │
│ • Credential Mediation (`AWS Secrets` → `~/.env`)      │
│ • Voice Streaming Interface (Ambient Daemon)           │
│ • Preflight & Quality Hard Gates (`preflight`, `qual`) │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│              Tri-Graph Cognitive Substrate             │
├────────────────────┬───────────────────┬───────────────┤
│   KnowledgeGraph   │   ContextGraph    │  MemoryGraph  │
│   (Static Truth)   │ (Dynamic Runtime) │(Working State)│
└────────────────────┴───────────────────┴───────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│            Hath0r Cognitive Engine Subsystems          │
├────────────────────┬───────────────────┬───────────────┤
│ GuardrailsManager  │ DynamicToolRouter │ AIGateway     │
│ DurableWorkflow    │ DSPy Declarative  │ Generative UI │
│ SandboxManager     │ OTELTracerBot     │ VoiceEngine   │
└────────────────────┴───────────────────┴───────────────┘
```

---

## 🧠 Cognitive Engine Modules (`hath0r_engine`)

The cognitive engine is packaged under `src/hath0r_engine/` and installable as `hath0r-engine`:

### 1. Pre-Execution Guardrails & Schema Repair
```python
from hath0r_engine import GuardrailsManager, SyntaxGuardrail, SchemaRepairEngine

manager = GuardrailsManager(guardrails=[SyntaxGuardrail()])
manager.register_schema("execute_sql", {"type": "object", "properties": {"query": {"type": "string"}}})

evaluation = manager.evaluate_and_repair("execute_sql", {"query": "SELECT * FROM users;"})
assert evaluation.is_allowed is True
```

### 2. Multi-Provider AI Gateway & Tiered Routing
```python
from hath0r_engine import AIGatewayClient, ModelTier, TieredRouter, SemanticCache

client = AIGatewayClient(api_base="https://ai-gateway.local", default_tier=ModelTier.STANDARD)
cache = SemanticCache(similarity_threshold=0.92)

# Cosine-similarity memoized routing
cached_resp = cache.get("Summarize PR 142")
```

### 3. Declarative DSPy Pipelines with Assertions
```python
from hath0r_engine import Signature, InputField, OutputField, Assert, ChainOfThought

class CodeRefactor(Signature):
    """Refactor code while preserving interface invariants."""
    source_code: str = InputField(desc="Legacy code block")
    target_code: str = OutputField(desc="Modernized code")

module = ChainOfThought(CodeRefactor)
Assert(len(result.target_code) > 0, "Target code must not be empty")
```

### 4. Durable Execution & Replayable Workflows
```python
from hath0r_engine import DurableWorkflowEngine, EventJournal, HumanHibernationGate, durable_task

journal = EventJournal(db_path=":memory:")
engine = DurableWorkflowEngine(journal=journal)

@durable_task(name="build_binaries")
def build_step(ctx):
    return {"status": "ok"}
```

### 5. Generative UI & Cryptographic Evidence Handshake
```python
from hath0r_engine import HandshakeSession, UIComponentBuilder, BiDirectionalStateSync

session = HandshakeSession(task_name="release_v1_0_1")
diff_card = UIComponentBuilder.build_diff_viewer("VERSION", "1.0.0", "1.0.1")
session.add_component(diff_card)

# Cryptographic immutable sign-off
sign_off = session.sign_off(reviewer="somesayray", role="architect", decision=True)
assert len(sign_off.signature) == 64  # SHA-256 HMAC
```

### 6. Dynamic MCP Tool Router & Schema Pruning
```python
from hath0r_engine import DynamicToolRouter, SchemaPruner, PruningLevel

router = DynamicToolRouter(similarity_threshold=0.6)
pruner = SchemaPruner(level=PruningLevel.AGGRESSIVE)
```

---

## 📂 Universal Project Layout & Subsystem Governance

The HATHOR layout is strictly language-agnostic and organized for autonomous agent navigation:

| Directory | Subsystem Role | Governance Pointer |
| :--- | :--- | :--- |
| **`src/hath0r_engine/`** | Cognitive substrate, guardrails, gateway, durable orchestration | `src/hath0r_engine/AGENTS.md` |
| **`cfg/`** | Configuration files, factory workflows, docker setups | `cfg/AGENTS.md` |
| **`bin/`** | Executables, hooks, and member bootstrap scripts | `bin/hath0r-bootstrap.sh` |
| **`lib/`** | Graph engines, cognitive substrate, shared libraries | `lib/AGENTS.md` |
| **`contracts/`** | Formal JSON schemas and protocol specifications | `contracts/AGENTS.md` |
| **`release/`** | Standalone pre-compiled CLI executables and checksums | `release/README.md` |
| **`tests/`** | Unit, integration, and contract verification test harnesses | `tests/AGENTS.md` |
| **`docs/`** | Canonical OpenSource documentation corpus | `docs/AGENTS.md` |
| **`.hath0r/`** | Hidden agent state, caches, working memory, and lineage | Local `.hath0r/` |

---

## 🧪 Testing & Verification

Run the comprehensive test suite across all cognitive subsystems:

```bash
pytest -v
```

**97 passed unit tests** validate:
- Temporal Knowledge Graphs & SQLite graph persistence
- Dynamic MCP Tool Router ranking & Schema Pruning
- AI Gateway Tiered Routing & Semantic Cache
- Durable Workflow Engine & Event Journal replay
- Declarative DSPy signatures & Assert invariants
- Deterministic Tool Guardrails & AST security
- Generative UI evidence handshakes & Cryptographic sign-offs
- Zero-Trust Sandboxes & OpenTelemetry tracing

---

## ⚖️ License

Licensed under the [Apache License, Version 2.0](LICENSE).
