# AGENTS.md — HATH0R Agentic Framework

> Role: **OpenSource HATHOR framework + docs corpus** · member of **OpenSource Project** (`hath0r-opensource`)  
> Updated: 2026-09-30

## Group membership (CRITICAL)

| Field | Value |
|-------|-------|
| Group | `hath0r-opensource` |
| Project | **OpenSource Project** |
| Group root | `/Users/raybayly/Development/OpenSource` |
| **Control tower** | `/Users/raybayly/Development/OpenSource/HATH0R-CLI` (`Bayly-AI/HATH0R-CLI`) |
| This product | `HATH0R-Agentic-Framework` |
| GitHub | `Bayly-AI/HATH0R-Agentic-Framework` |
| Local path | `/Users/raybayly/Development/OpenSource/hath0r` |
| Canonical KB | `/Users/raybayly/Development/OpenSource/.hath0r/knowledgebase` |
| Operator CLI | `hath0r` |
| Docs | `docs/` (canonical OpenSource documentation corpus) |

### Canonical siblings (all under OpenSource are project members)

- **Control tower / CLI**: `/Users/raybayly/Development/OpenSource/HATH0R-CLI` → `Bayly-AI/HATH0R-CLI`
- Framework: `/Users/raybayly/Development/OpenSource/hath0r` → `Bayly-AI/HATH0R-Agentic-Framework`
- POC: `/Users/raybayly/Development/OpenSource/hath0r-poc` → `Bayly-AI/HATH0R-Agentic-POC`

Group rules: `/Users/raybayly/Development/OpenSource/AGENTS.md`  
Group policy: `/Users/raybayly/Development/OpenSource/WARP.md`

## CR-CLI-ENTRY-001: Start with the CLI & Missing Capability Offer (CRITICAL — org-wide)

1. **Start with the CLI (CRITICAL ENTRY GATE)**: When receiving ANY request or starting any task, agents **MUST ALWAYS START WITH THE OPERATOR CLI (`hath0r`)** rather than inventing ad-hoc scripts or direct unverified actions.
2. **Missing Capability Offer**: If the required connection, MCP, workflow, bot, or factory does not exist in `hath0r`, do **not** silently improvise. Offer to create/register the missing capability and use the original request as the immediate acceptance test.
3. **Docs before code**: Require procedure/strategy/playbook/runbook (see `docs/governance/workflow-documentation-standard.md`) before scaffolding implementation.
4. **Detail**: `docs/governance/rules/cr-cli-entry-001.md` · `docs/governance/cli-first-rules.md` · tower canonical: https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/cli-first-rules.md

## CR-RAG-RETRIEVAL-001: Hybrid Tri-Graph RAG & Memory Doctrine (CRITICAL — org-wide)

1. **No Context Stuffing**: Agents must never load whole unbounded file trees into prompt context.
2. **Tri-Graph Hybrid Retrieval**:
   - **KnowledgeGraph (`lib.graph` / `contracts/` / `docs/`)**: Static architecture, contracts, schemas, and rule invariants.
   - **ContextGraph (`lib.context` / `hath0r context`)**: Dynamic session state, active subagent executions, and span lineages.
   - **MemoryGraph (`hath0r_engine.memory` / `hath0r memory`)**: Long-term temporal entity nodes, Letta-compatible memory paging (`MemoryPagingManager`), and consolidation reflections (`ReflectionEngine`).
3. **Temporal Validity Filtering**: Edges and nodes must be evaluated using `is_valid_at(as_of)` to respect entity state mutations over time.
4. **Tool Dynamic Routing & Pruning**: Use `DynamicToolRouter` with BM25 + dense vector ranking and `SchemaPruner` to compress tool descriptions.

## CR-SUBSTRATE-001: Mandatory Cognitive Substrate Technology Utilization (CRITICAL — org-wide)

All agents executing tasks within Hath0r must utilize our unified cognitive modules (`src/hath0r_engine/`):
- **Pre-Execution Safety**: Apply `GuardrailsManager` and `SyntaxGuardrail` (AST/SQL validation) with in-flight `SchemaRepairEngine` parameter coercion.
- **AI Gateway & FinOps**: Route completion requests through `AIGatewayClient` and `TieredRouter` (`LIGHT`, `STANDARD`, `REASONING`) with `SemanticCache` memoization.
- **Durable Orchestration**: Execute multi-step flows via `DurableWorkflowEngine` and `EventJournal` to support replayability and `HumanHibernationGate` suspension.
- **Declarative DSPy Pipelines**: Build structured reasoning with `Signature`, `ChainOfThought`, programmatic `Assert`, and `BootstrapFewShotCompiler`.
- **Generative UI & Evidence Handshake**: Emit interactive diffs, sliders, and HMAC SHA-256 signatures via `HandshakeSession` and `UIComponentBuilder`.
- **Playwright UI Testing & Test Catalog**: Execute UI verification with `PlaywrightTestRunner` and maintain Playwright-compliant master test specifications via `PlaywrightMasterCatalogManager`.
- **Zero-Trust Sandboxing**: Run untrusted user commands inside isolated providers (`E2BSandboxProvider`, `DaytonaSandboxProvider`, `LocalSandboxProvider`).
- **Robust Design & Optimization**: Apply Taguchi Methods (`TaguchiEngine`, `calculate_snr`, `TaguchiLossFunction`) for Orthogonal Array Testing Strategy (OATS) matrix reduction and hyperparameter tuning.

## CR-PLAYWRIGHT-UI-001: Mandatory Playwright UI Testing & Master Test Catalog (CRITICAL — org-wide)

1. **Mandatory Playwright UI Validation**: All UI components, Generative UI widgets, dashboard panels, and web views MUST have automated test coverage executed via Playwright (`PlaywrightTestRunner` / `pytest tests/test_playwright_testing.py`).
2. **Master Test Case Specification**: Maintain the single source of truth at `tests/e2e/master-playwright-tests.json` conforming to `contracts/hath0r-playwright-test-spec-v1.schema.json`.
3. **Clean Repo Synchronization**: During Step 7 of the Clean Repo lifecycle (`.agents/skills/clean-repos/`), agents and bots MUST execute test catalog synchronization (`PlaywrightMasterCatalogManager.audit_and_sync_test_cases()`), ensuring all new or modified UI components are cataloged before committing and opening PRs.
4. **Visual Regression Baselines**: Maintain verified snapshot baselines for visual regression testing (`expectVisualMatch`).

## Suite standards (member pointers)

Index: `docs/governance/SUITE_STANDARDS.md`  
Local cfg: `cfg/observability/`, `cfg/feature-flags/`, `cfg/docker/`  
Adopt audit: `.hath0r/ADOPT_AUDIT.md`  
Control tower epic: HATH0R-CLI #58–#63 / PR #111

## Framework hidden root (CRITICAL — cr-hath0r-root-001)

Use **only** `.hath0r/` for framework-created / modified / saved project metadata.

Do **not** use `.ai/`, `.customerSystem/`, or `.infraOS/`.

## Knowledgebase (CRITICAL — cr-kb-tower-001)

1. Point local knowledgebase operations at the OpenSource group hub (`hath0r kb path`).
2. Keep member `.hath0r/knowledgebase` as stub/pointer only.
3. Resolve control-tower / suite orientation to **HATH0R-CLI**.
4. Framework `docs/` is the **canonical OpenSource documentation** corpus.
5. Do **not** treat private internal product trees as OpenSource canonical sources.

## Open issues tracking (group-wide)

Use the verified multi-repo search (all three OpenSource products):

```text
is:issue state:open repo:Bayly-AI/HATH0R-Agentic-Framework repo:Bayly-AI/HATH0R-Agentic-POC repo:Bayly-AI/HATH0R-CLI
```

Canonical definition: group `AGENTS.md` (*Open issues tracking*). Also listed in `docs/README.md`.

## Branch & PR targets (CRITICAL — cr-branch-gov-001)

1. **Issue first**: create a GitHub issue before any work branch. No issue → no branch.
2. Branch from `development` only, using:
   `feature|bugfix|enhancement|research|fix|chore/<issue-number>-short-slug`
   Example: `chore/4-control-tower-cli`
3. Validate branch: `hath0r branch validate <branch-name>`.
4. Open the PR with **base = `development`** (feature work never targets testing/staging/master).
5. **Owner (`@somesayray`) may merge any PR at any time** (admin bypass enabled; approvals not required).
6. Merge into **`development` only** for feature work.
7. Promote via `development → testing → staging → master` — do not skip stages.
8. **PR CI failures notify `@somesayray`** via `.github/workflows/notify-pr-failure.yml`.

### Canonical branches (locked)

`development` (default), `testing`, `staging`, `master`

- Must not be deleted
- Must not be used as feature/work branches
- Must not be merged into each other except along the promotion path above
- Branch protection: PR required (0 approvals), no code-owner gate, admin bypass on, no force-push, no deletions, `validate-promotion-path` required (non-strict; admin can bypass)

Forbidden: feature PRs targeting `master`, `testing`, or `staging`; PRs without an issue number in the branch name; merging canonical branches sideways.

## CR-BAI-001: Environment Promotion Path (CRITICAL — org-wide)

Canonical policy: `/Users/raybayly/Development/BAI/WARP.md` (org-wide). Group mirror: `/Users/raybayly/Development/OpenSource/WARP.md`.

Required order (never skip):

```text
local → development → testing → staging → master (Production)
```

CI enforcement: `.github/workflows/enforce-promotion-path.yml`

- PRs into `testing` must come from `development`
- PRs into `staging` must come from `testing`
- PRs into `master` must come from `staging`
- Each stage needs deploy + URL validation before the next promote

## Credentials

`/Users/raybayly/Development/.credentials/<service>/.env` — never hardcode or print secrets.

## CR-HATH0R-INIT-001: Hath0r repo initialization entry gate (CRITICAL — org-wide)

**Main entry statement:** Before initializing (or re-initializing) any repository with Hath0r, agents MUST:

1. **Setup playbook** — Locate and follow the canonical Hath0r setup playbook:
   - `/Users/raybayly/Development/OpenSource/hath0r/docs/developers/hathor-playbook-001-repo-init-setup-20260919.md`
   - If the playbook is missing or incomplete, **create or update it first**, then proceed.
2. **Same-technology runbook** — Locate a runbook for an **individual repo with the same technology stack** (e.g. React+Vite UXP, Python CLI):
   - Prefer a sibling/product `docs/runbook.md` (or `docs/*runbook*`) in that tech family.
   - If none exists, **create a tech-appropriate runbook in the target repo** before finishing init.
3. Only after (1) and (2) are satisfied: apply fileset/layout, `.hath0r/`, `cfg/`, contracts pin, `AGENTS.md` identity, and `./bin/hath0r-bootstrap.sh`.

Do not skip the playbook/runbook gate. Layout scaffolding without a documented ops path is incomplete initialization.

## Branch rules (pointer)

See `docs/governance/branch-rules.md` (cr-branch-gov-001 / CR-BAI-001). Work PRs → `development` only; release trains use `release/x.x.x`.

## PR workflow hardening

See `docs/governance/pr-workflow.md`. Work PRs → `development` (agents + CODEOWNERS). **Human gate** before staging/master.

## SonarCloud Quality Gate (CRITICAL)

- Canonical thresholds: SonarCloud Quality Gate only — do not modify gate thresholds ad hoc.
- PR check **SonarCloud Quality Gate** is a hard stop on failure.
- See `docs/governance/sonarcloud-quality-gates.md`
- Secret required: `SONAR_TOKEN`

## Documentation → MCP

Docs are published to the **proper group MCP** via control-tower:
`hath0r docs share --pr <pr-number>` or `python3 scripts/publish-docs-to-mcp.py` (`cfg/mcp-doc-publish.json`).
See HATH0R-CLI `docs/governance/mcp-doc-publish.md`.

## Semantic Versioning (SemVer)

- Canonical source of truth: `VERSION` in repo root.
- PRs must declare version impact (`major`, `minor`, `patch`, or `none`).
- See `docs/governance/semantic-versioning.md` and `docs/governance/playbooks/release-runbook.md`.

## Hyper Context Subsystem Pointers
- **Engine Core Subsystem**: `src/hath0r_engine/AGENTS.md`
- **Docs Subsystem**: `docs/AGENTS.md`
- **Contracts Subsystem**: `contracts/AGENTS.md`
- **Testing Subsystem**: `tests/AGENTS.md`
- **Configuration Subsystem**: `cfg/AGENTS.md`
- **Library Subsystem**: `lib/AGENTS.md`
- **Archive Subsystem**: `archive/AGENTS.md`
