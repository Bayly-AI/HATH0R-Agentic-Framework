# HATHOR Framework — Technical Architecture & Engine Reference

> Language-agnostic agentic application framework and cognitive substrate for the Enterprise Agentic Platform.  
> Release Version: **v1.2.0**

---

## 🛠️ Developers Working on HATH0R-CLI & Core Framework

This document contains deep technical specifications, Tri-Graph substrate data structures, repository layouts, binary build pipelines, and cognitive engine modules for developers building or extending `hath0r`, `hath0r-framework`, and `hath0r-engine`.

> **Looking to install and use Hath0r in your own projects?**  
> You only need the **HATH0R CLI** (`hath0r`). Download pre-compiled standalone binaries in [`release/python/cli/`](release/python/cli/) or see the [CLI Quick Start](#-quick-start-operators--users) below.

---

## 🚀 Quick Start: Operators & Users

The Hath0r CLI is distributed as a zero-dependency standalone binary for macOS, Linux, and Windows:

```sh
# Option 1: Direct Standalone Binary (Zero Setup Required)
chmod +x release/python/cli/hath0r-darwin-arm64
./release/python/cli/hath0r-darwin-arm64 doctor
./release/python/cli/hath0r-darwin-arm64 init

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
│ TaguchiEngine      │ TokenizerTaxAudit │ VisionEngine  │
│ PlaywrightRunner   │ MasterCatalogSync │ SchemaPruner  │
└────────────────────┴───────────────────┴───────────────┘
```

---

## 🧠 Cognitive Engine Modules (`src/hath0r_engine/`)

The cognitive engine is packaged under `src/hath0r_engine/` and installable as `hath0r-engine`:

### 1. Taguchi Robust Parameter Optimization Engine (`hath0r_engine.optimization.taguchi`)

Applies Genichi Taguchi's Design of Experiments (DoE) and Orthogonal Array Testing Strategies (OATS) to eliminate combinatorial brute-force tuning in prompt engineering, model temperature, and agent routing.

* **Standard Orthogonal Arrays:** Built-in generators for $L_4(2^3)$, $L_8(2^7)$, $L_9(3^4)$, $L_{12}(2^{11})$, and $L_{18}(2^1 \times 3^7)$.
* **Signal-to-Noise Ratio (SNR):**
  * *Nominal-is-Best:* $\text{SNR} = 10 \log_{10} \left( \frac{\bar{y}^2}{s^2} \right)$
  * *Smaller-is-Better (Latency / Cost):* $\text{SNR} = -10 \log_{10} \left( \frac{1}{n} \sum y_i^2 \right)$
  * *Larger-is-Better (Accuracy / Precision):* $\text{SNR} = -10 \log_{10} \left( \frac{1}{n} \sum \frac{1}{y_i^2} \right)$
* **Taguchi Quality Loss Function:** $L(y) = k(y - m)^2$ quantifying financial loss per unit variance.

```python
from hath0r_engine import TaguchiEngine, TaguchiLossFunction, calculate_snr

engine = TaguchiEngine()
# Generate 9-trial orthogonal design for 4 three-level parameters (vs. 81 full-factorial runs)
matrix = engine.generate_matrix(
    array_type="L9",
    factors=["temperature", "top_p", "retrieval_k", "chunk_size"],
    levels={
        "temperature": [0.0, 0.5, 1.0],
        "top_p": [0.7, 0.85, 1.0],
        "retrieval_k": [3, 5, 10],
        "chunk_size": [256, 512, 1024],
    },
)

# Compute Signal-to-Noise Ratio for response latencies (Smaller-is-Better)
snr = calculate_snr([120.0, 115.0, 130.0], criterion="smaller_is_better")
```

---

### 2. FinOps Tokenizer Tax Auditor (`hath0r_engine.gateway.tokenizer_tax`)

Quantifies the hidden infrastructure and financial penalties imposed by subword tokenizers (BPE/WordPiece) on enterprise multi-tenant deployments.

* **Unicode Script Classifier:** Analyzes character distributions across Latin, Cyrillic, Greek, Arabic, Hebrew, Devanagari, Bengali, Tamil, CJK, Hiragana, Katakana, and Hangul.
* **Token Inflation Ratio ($\tau_{lang}$):** Measures token expansion relative to an equivalent Latin baseline.
* **Vocabulary VRAM Footprint:** Computes parameter count ($P_{vocab} = 2 \cdot V \cdot d_{model}$) and memory footprint in FP16 / FP32.
* **Continuous Visual Patch Budget:** Calculates equivalent patch count ($N_{patch} = \lceil H/P \rceil \times \lceil W/P \rceil$) for pixel-native vision ingestion.

```python
from hath0r_engine import TokenizerTaxAuditor

auditor = TokenizerTaxAuditor()
report = auditor.audit(
    text="شركة هتحور للذكاء الاصطناعي تقدم نماذج معالجة متقدمة",  # Arabic enterprise document
    vocab_size=256_000,
    hidden_dim=4096,
    precision_bytes=2,  # FP16
)

print(f"Token Inflation: {report.inflation_ratio:.2f}x")
print(f"Vocab VRAM Overhead: {report.vram_footprint.vram_gb:.2f} GB")
print(f"Equivalent Patch Budget (16x16): {report.patch_budget.total_patches} patches")
```

---

### 3. Pixel-Native 2D Document Parsing (`hath0r_engine.vision.document_parser`)

Parses visual documents, technical diagrams, invoices, and balance sheets as continuous 2D visual patches rather than flattening them into 1D text token streams.

* **Zero OCR Dependency:** Ingests rendered pages directly, bypassing costly OCR licensing.
* **2D Relational Matrix Preservation:** Retains spatial cell coordinates, table dimensions (rows, columns), and topological flow hierarchies.

```python
from hath0r_engine.vision import DocumentLayoutParser

parser = DocumentLayoutParser()
result = parser.parse_pixel_native(image_path="docs/invoices/balance_sheet_q3.png", patch_size=16)

assert result.success is True
assert result.document_structure.doc_type == "2d_tabular_document"
assert len(result.document_structure.tables) > 0
# Cell spatial bounding box coordinates [ymin, xmin, ymax, xmax] preserved
first_cell = result.document_structure.tables[0]["cells"][0]
print(f"Cell ({first_cell['row']}, {first_cell['col']}) Bounding Box: {first_cell['bbox']}")
```

---

### 4. DOM-Independent Playwright Grounding (`hath0r_engine.vision.grounding`)

Resolves natural language UI directives directly into pixel coordinates and generates Playwright-compliant automation steps without relying on CSS selectors, XPath, or DOM tree parsing.

* **Layout Resilient:** Operating enterprise web applications (SAP, Salesforce, Workday) remains reliable across CSS rewrites and framework upgrades.
* **Playwright Schema Integration:** Emits `PlaywrightStep` structures with `coordinates: {"x": float, "y": float}` conforming to `contracts/hath0r-playwright-test-spec-v1.schema.json`.

```python
from hath0r_engine.vision import VisualGroundingEngine
from hath0r_engine.testing.models import PlaywrightStep

grounding = VisualGroundingEngine()
step_dict = grounding.ground_to_playwright_step(
    image_path="screenshots/sap_checkout_screen.png",
    target="Submit Order & Sign Off Button",
    action="click",
    step_number=1,
)

step = PlaywrightStep.from_dict(step_dict)
assert step.selector is None  # DOM-independent!
assert step.coordinates["x"] > 0
assert step.coordinates["y"] > 0
```

---

### 5. Playwright UI Test Runner & Master Catalog Manager (`hath0r_engine.testing`)

Provides automated Playwright-compliant end-to-end UI testing and test case catalog lifecycle management.

* **Master Specification:** Single source of truth maintained at `tests/e2e/master-playwright-tests.json`.
* **Clean Repo Synchronization:** `PlaywrightMasterCatalogManager.audit_and_sync_test_cases()` automatically synchronizes UI test cases with actual component implementations during Step 7 of the Clean Repo lifecycle.

---

### 6. Pre-Execution Guardrails & Schema Repair (`hath0r_engine.guardrails`)

```python
from hath0r_engine import GuardrailsManager, SyntaxGuardrail, SchemaRepairEngine

manager = GuardrailsManager(guardrails=[SyntaxGuardrail()])
manager.register_schema("execute_sql", {"type": "object", "properties": {"query": {"type": "string"}}})

evaluation = manager.evaluate_and_repair("execute_sql", {"query": "SELECT * FROM users;"})
assert evaluation.is_allowed is True
```

---

### 7. Multi-Provider AI Gateway & Tiered Routing (`hath0r_engine.gateway`)

```python
from hath0r_engine import AIGatewayClient, ModelTier, TieredRouter, SemanticCache

client = AIGatewayClient(api_base="https://ai-gateway.local", default_tier=ModelTier.STANDARD)
cache = SemanticCache(similarity_threshold=0.92)

# Cosine-similarity memoized routing
cached_resp = cache.get("Summarize PR 142")
```

---

### 8. Declarative DSPy Pipelines with Assertions (`hath0r_engine.pipeline`)

```python
from hath0r_engine import Signature, InputField, OutputField, Assert, ChainOfThought

class CodeRefactor(Signature):
    """Refactor code while preserving interface invariants."""
    source_code: str = InputField(desc="Legacy code block")
    target_code: str = OutputField(desc="Modernized code")

module = ChainOfThought(CodeRefactor)
```

---

### 9. Durable Execution & Replayable Workflows (`hath0r_engine.orchestration`)

```python
from hath0r_engine import DurableWorkflowEngine, EventJournal, HumanHibernationGate, durable_task

journal = EventJournal(db_path=":memory:")
engine = DurableWorkflowEngine(journal=journal)

@durable_task(name="build_binaries")
def build_step(ctx):
    return {"status": "ok"}
```

---

### 10. Generative UI & Cryptographic Evidence Handshake (`hath0r_engine.ui`)

```python
from hath0r_engine import HandshakeSession, UIComponentBuilder, BiDirectionalStateSync

session = HandshakeSession(task_name="release_v1_2_0")
diff_card = UIComponentBuilder.build_diff_viewer("VERSION", "1.1.0", "1.2.0")
session.add_component(diff_card)

# Cryptographic immutable sign-off
sign_off = session.sign_off(reviewer="somesayray", role="architect", decision=True)
assert len(sign_off.signature) == 64  # SHA-256 HMAC
```

---

### 11. Dynamic MCP Tool Router & Schema Pruning (`hath0r_engine.mcp`)

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
| **`src/hath0r_engine/`** | Cognitive substrate, optimization, vision, guardrails, gateway | `src/hath0r_engine/AGENTS.md` |
| **`cfg/`** | Configuration files, factory workflows, docker setups | `cfg/AGENTS.md` |
| **`bin/`** | Executables, hooks, and member bootstrap scripts | `bin/hath0r-bootstrap.sh` |
| **`lib/`** | Graph engines, cognitive substrate, shared libraries | `lib/AGENTS.md` |
| **`contracts/`** | Formal JSON schemas and protocol specifications | `contracts/AGENTS.md` |
| **`release/python/cli/`** | Standalone pre-compiled CLI executables and checksums | `release/python/cli/README.md` |
| **`tests/`** | Unit, integration, and contract verification test harnesses | `tests/AGENTS.md` |
| **`docs/`** | Canonical OpenSource documentation corpus | `docs/AGENTS.md` |
| **`.hath0r/`** | Hidden agent state, caches, working memory, and lineage | Local `.hath0r/` |

---

## 🧪 Testing & Verification

Run the comprehensive test suite across all cognitive subsystems:

```bash
pytest -v
```

**178 passed unit & integration tests** validate:
- Taguchi Robust Parameter Design, Orthogonal Arrays ($L_4 - L_{18}$), and Quality Loss Functions
- FinOps Tokenizer Tax Auditor, script detection, and VRAM overhead calculation
- Pixel-native 2D document parsing and spatial cell preservation
- DOM-independent Playwright grounding and coordinate step execution
- Playwright UI Test Runner, Master Catalog synchronization, and JSON schema validation
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
