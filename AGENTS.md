# AGENTS.md — HATH0R Agentic Framework

> Role: **OpenSource HATHOR framework + docs corpus** · member of **OpenSource Project** (`hath0r-opensource`)  
> Updated: 2026-10-29

## Group membership (CRITICAL)

| Field | Value |
|-------|-------|
| Group | `hath0r-opensource` |
| Project | **OpenSource Project** |
| Group root | `/Users/raybayly/Development/OpenSource` |
| **Control tower** | `/Users/raybayly/Development/OpenSource/hathor-cli` (`Bayly-AI/HATH0R-CLI`) |
| This product | `HATH0R-Agentic-Framework` |
| GitHub | `Bayly-AI/HATH0R-Agentic-Framework` |
| Local path | `/Users/raybayly/Development/OpenSource/hath0r-framework` |
| Canonical KB | `/Users/raybayly/Development/OpenSource/.hath0r/knowledgebase` |
| Operator CLI | `hath0r` |
| Docs | `docs/` (canonical OpenSource documentation corpus) |

### Canonical siblings (all under OpenSource are project members)

- **Control tower / CLI**: `/Users/raybayly/Development/OpenSource/hathor-cli` → `Bayly-AI/HATH0R-CLI`
- **Infra Control Tower / ATC**: `/Users/raybayly/Development/OpenSource/hath0r-atc` → `Bayly-AI/HATH0R-ATC`
- **Framework**: `/Users/raybayly/Development/OpenSource/hath0r-framework` → `Bayly-AI/HATH0R-Agentic-Framework`
- **MCP**: `/Users/raybayly/Development/OpenSource/hath0r-mcp` → `Bayly-AI/HATH0R-MCP`
- **POC**: `/Users/raybayly/Development/OpenSource/hath0r-poc` → `Bayly-AI/HATH0R-Agentic-POC`

Group rules: `/Users/raybayly/Development/OpenSource/AGENTS.md`  
Group policy: `/Users/raybayly/Development/OpenSource/WARP.md`

## CR-CLI-ENTRY-001: Start with the CLI & Missing Capability Offer (CRITICAL — org-wide)

1. **Start with the CLI (CRITICAL ENTRY GATE)**: When receiving ANY request or starting any task, agents **MUST ALWAYS START WITH THE OPERATOR CLI (`hath0r`)** rather than inventing ad-hoc scripts or direct unverified actions.
2. **Missing Capability Offer**: If the required connection, MCP, workflow, bot, or factory does not exist in `hath0r`, do **not** silently improvise. Offer to create/register the missing capability and use the original request as the immediate acceptance test.
3. **Docs before code**: Require procedure/strategy/playbook/runbook (see `docs/governance/workflow-documentation-standard.md`) before scaffolding implementation.
4. **CR-CLI-FEATURE-STANDARD-001 (Shared Code in CLI & Artifact Hexad — CRITICAL · CANONICAL)**:
   - Anything usable across multiple repos MUST live in `HATH0R-CLI`.
   - Feature packages must include CLI commands, managing bots, workflows, and the documentation hexad (Strategy, Procedure, Playbook, Runbook, Workflow, Bot Spec).
   - This repo contains declarative configuration files (`cfg/`, `otel.json`, factory YAMLs) that bind to CLI tools.
5. **Detail**: `docs/governance/rules/cr-cli-entry-001.md` · `docs/governance/cli-first-rules.md` · tower canonical: https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/cli-first-rules.md

## CR-CLAUDE-SYNC-001: Mandatory `CLAUDE.md` ↔ `AGENTS.md` 1:1 Synchronization (CRITICAL — org-wide)

1. **Exact 1:1 Mirror**: `CLAUDE.md` at the repository root MUST remain an exact byte-for-byte mirror of `AGENTS.md` so all agentic runtimes enforce identical non-conflicting rules.
2. **Automated Sync & Verification**: Run `hath0r agentgraph sync` and `hath0r memory hash --sync` whenever `AGENTS.md` is updated, and verify with `hath0r agentgraph validate` and `hath0r skills audit`.

## CR-AGENTIC-SEC-001: Agentic Security, Supply-Chain & Governance Controls (CRITICAL — org-wide)

1. **BITE Supply-Chain & Skill Integrity (`hath0r skills audit` / `hath0r mcp audit`)**: Audit all `.agents/skills/**/SKILL.md`, `CLAUDE.md`, `AGENTS.md`, `WARP.md`, and MCP tool schemas for prompt injection, hidden Unicode tag characters, reverse shells, and credential exfiltration, and pin SHA-256 digests in `.hath0r/security/mcp-schema-pins.json`.
2. **L2 Output Sanitizer & Canary Honeytokens (`src/hath0r_engine/security/l2_output_sanitizer.py`)**: Enforce output-side taint and canary honeytoken verification (`L2OutputSanitizer`) on RAG/MCP tool results before LLM context injection.
3. **Cryptographic Hash-Chained Token & Tool Ledger (`hath0r finops tokens verify-ledger`)**: Every tool/completion event is recorded in `.hath0r/state/finops/token_ledger.jsonl` with a tamper-evident SHA-256 hash chain (`prev_hash` → `entry_hash`).
4. **Dynamic Purpose-Based Access Control (PBAC) & Confused-Deputy Prevention (`src/hath0r_engine/security/pbac_engine.py`)**: Enforce clearance, sensitivity classification, and stated mission purpose (`PBACPolicyEngine`) across knowledge retrieval and MCP tools.
5. **Two-Stage AST + Adversarial Reachability (`hath0r security openant`) & Red-Team Probing (`hath0r kb redteam`)**: Verify exploitability of findings via `OpenAntReachabilityVerifier` (`src/hath0r_engine/security/openant_verifier.py`) and run automated multi-persona RBAC boundary probing.
6. **Fail-Closed `THREATMODEL.md` Gate (`hath0r threatmodel validate`) & Slopsquatting Guard**: Maintain a valid `THREATMODEL.md` in every repository and verify dependency/rule drift (`DependencyGuardBot`) during preflight.

## CR-AGENTGRAPH-001 / CR-RAG-RETRIEVAL-001: Mandatory AgentGraph Querying & Zero-Prompt-Tax Doctrine (CRITICAL — org-wide)

1. **No Context Stuffing & No Unbounded File Reading (CRITICAL)**: Agents, subagents, and workflows must **NEVER** load whole unbounded file trees, full `AGENTS.md` files, or complete rulebooks into prompt context. Use targeted line slices or pre-compiled graph nodes.
2. **Mandatory AgentGraph Retrieval**: Always query the **AgentGraph** substrate via CLI (`hath0r agentgraph query "<topic>"`, `hath0r agentgraph route --role <role>`, or `hath0r kb search -q "<topic>"`) to retrieve strictly contextual, scoped, and relevant data, rules, policies, and tool permissions.
3. **Unified Quad-Graph Retrieval**:
   - **KnowledgeGraph (`lib.graph` / `contracts/` / `docs/`)**: Static architecture, contracts, schemas, and specifications.
   - **ContextGraph (`lib.context` / `hath0r context`)**: Dynamic session state, active subagent executions, and span lineages.
   - **MemoryGraph (`hath0r_engine.memory` / `hath0r memory`)**: Long-term temporal entity nodes, Letta-compatible memory paging (`MemoryPagingManager`), and consolidation reflections (`ReflectionEngine`).
   - **RulesGraph (`hath0r_engine.graph` / `hath0r agentgraph`)**: Deterministic rule inheritance DAG ($\text{Org Invariant} \succ \text{Repo Standard} \succ \text{Subsystem} \succ \text{Role}$), tool RBAC, and action permissions.
4. **Deterministic Tool & Role RBAC**: Use `hath0r agentgraph route --role <role> [--tool <tool>]` to deterministically prune unauthorized tools before execution rather than relying on LLM self-governance.
5. **Temporal Validity Filtering**: Edges and nodes must be evaluated using `is_valid_at(as_of)` to respect entity state mutations over time.
6. **Detail**: `docs/governance/rules/cr-agentgraph-001.md`.

## CR-MEMORY-COMPOUND-001: Mandatory `.hath0r/memory` Repository Presence, Micro Memory Sessions & Pre-Announcement MemoryGraph Compounding (CRITICAL — org-wide)

1. **Universal `.hath0r/memory`, `.hath0r/memory/sessions`, `.hath0r/memory/hashes.json` & Un-Ignored Graph Folders**: Every project repository in `/Users/raybayly/Development` MUST maintain an initialized `.hath0r/memory/` directory containing `.hath0r/memory/graph.json`, `.hath0r/memory/sessions/current.json`, `.hath0r/memory/sessions/latest.json`, `.hath0r/memory/hashes.json`, `core_rules.md`, and `architecture.md` (`hath0r memory init` / `hath0r memory ensure-all`), and MUST ensure all graph folders (`.hath0r/memory/`, `.hath0r/agentgraph/`, `.hath0r/graphs/`, `.hath0r/state/cache/`, `.hath0r/state/context/`, `lib/graph/`, `lib/context/`, `lib/memory/`) are explicitly un-ignored in `.gitignore` (`graphs_not_ignored: True`).
2. **True Micro Memory Session Read & Write on Every Session**: Every session MUST read and write a compact (<2KB) micro memory session (`hath0r memory session start|read` at session/task start, `hath0r memory session write` during execution, and `hath0r memory session end` at completion), linking sessions via `PRECEDES` edges in `.hath0r/memory/graph.json`.
3. **Cryptographic SHA-256 File Hashing & CAS Conflict Prevention (`hath0r memory hash`)**: Every file in `.hath0r/memory/` and every repository `source_files` path referenced on a `MemoryNode` MUST be tracked with canonical `SHA-256` digests and monotonic `revision` counters in `.hath0r/memory/hashes.json`. Concurrent writes use optimistic Compare-And-Swap (`expected_hash` / `base_hash`) with deterministic set-union auto-merging for non-conflicting additions and atomic file replacement (`os.replace`), rejecting true same-ID/explicit hash conflicts (`HASH_CONFLICT`).
4. **Mandatory Pre-Announcement Compounding**: Every task, bugfix, feature, refactor, or clean-repo cycle MUST compound structured knowledge (`episode`, `decision`, `fact`, `insight`, `concept`, or `rule`) and relational edges (`DERIVES_FROM`, `RESOLVES`, `RELATES_TO`, `SUPERSEDES`, `ENFORCES`, `PRECEDES`) into `.hath0r/memory/graph.json` **prior to announcing task completion** (`hath0r memory compound` + `hath0r memory verify`).
5. **Hard Gate & Immediate AgentGraph Sync**: `TaskAnnouncerBot.announce_complete`, `EndOfTaskBot`, and `CleanReposWorkflowBot` enforce `MemoryManagerBot.verify_compounded()` (requiring `read_count >= 1`, `write_count >= 1`, `compounded_nodes_count >= 1`, `hashes_verified: True`, and `graphs_not_ignored: True`) before announcing complete, and automatically sync `.hath0r/agentgraph/snapshot.json` and `CLAUDE.md` on every memory mutation.
6. **Detail**: `docs/governance/rules/cr-memory-compound-001.md` · `docs/governance/strategies/memorygraph-compounding-strategy.md`.

## CR-CICCCDCT-001 / CR-CICCCD-001: Continuous Integration, Calibration, Deployment & Continuous Training (CIC³DCT / CIC{qubed}DCT) Methodology (CRITICAL — org-wide)

1. **Continuous Integration (CI)**: All PRs must pass schema contract validation (`hath0r contracts validate`), AgentGraph policy checks (`hath0r agentgraph validate`), AST syntax guardrails, and automated unit tests.
2. **Continuous Calibration (CC)**: Calibration state freshness limit is $\le 24.0\text{ hours}$. AgentGraph runtime substrate uses `CICCCDCTTelemetryHook` (`src/hath0r_engine/telemetry/cicccd_telemetry.py`) to record span metrics and track parameter drift. Trigger on-demand calibration via `hath0r cicccdct calibrate` or `hath0r cccd calibrate`.
3. **Continuous Deployment (CD)**: Maintain automated promotion validation through canonical environments (`development` -> `testing` -> `staging` -> `master`), complete Artifact Hexad documentation, and background auto-tune monitoring via `hath0r cicccdct auto-tune`.
4. **Continuous Training (CT — SFT / LoRA / PEFT)**: Model training freshness SLA is $\le 168.0\text{ hours}$ (7 days). Retraining is automatically triggered when accuracy drift $\Delta_{\text{acc}} > 0.05$ or token tax drift $\Delta_{\text{tok}} > 0.15$. Candidate models must beat production baseline on the golden benchmark suite ($R_{\text{candidate}} \ge R_{\text{production}} + 0.02$) and be registered in MLflow Model Registry before promotion to production. Trigger on-demand SFT/LoRA/PEFT training via `hath0r cccd train` (`SFTLoRATrainer`).
5. **Detail**: Mathematical $CIC^3DCT$ ($CIC^{\text{qubed}}DCT$) doctrine: `docs/governance/strategies/cicccdct-strategy.md` · `hath0r cicccdct validate` / `hath0r cic3dct validate`.

## CR-SUBSTRATE-001: Mandatory Cognitive Substrate Technology Utilization (CRITICAL — org-wide)

All agents executing tasks within Hath0r must utilize our unified cognitive modules (`src/hath0r_engine/`):
- **Pre-Execution & Output Safety**: Apply `GuardrailsManager`, `SyntaxGuardrail` (AST/SQL validation), `L2OutputSanitizer`, `PBACPolicyEngine`, and `OpenAntReachabilityVerifier` with in-flight `SchemaRepairEngine` parameter coercion.
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

## CR-IAC-001: Mandatory Infrastructure as Code, Container Salting & EKS Fargate Standards (CRITICAL — org-wide)

1. **Mandatory Infrastructure as Code (IaC)**: All services, backends, frontends, bots, and MCP nodes in `~/Development` MUST declare production-ready IaC adhering to `contracts/hath0r-iac-spec-v1.schema.json`. Ad-hoc, imperative host deployments are strictly forbidden.
2. **Container Hardening Standards**: Every containerized repository MUST provide a multi-stage Dockerfile:
   - Build stage: Installs dependencies and compiles assets.
   - Runtime stage: Uses minimal slim/distroless/alpine base images without dev compilers.
   - User security: Must execute as non-root user (`UID 10001:GID 10001` or equivalent).
   - Container health: Must define an explicit `HEALTHCHECK` directive.
   - Filesystem: Runtime root filesystem must be mounted read-only (`readOnlyRootFilesystem: true`) where supported.
3. **Container Salting & Cryptographic Attestation**:
   - Container images MUST NOT be deployed using mutable tags (e.g. `:latest`). Deployments must pin immutable cryptographic SHA-256 digests (`image@sha256:...`).
   - Images must have cryptographic signatures and SLSA provenance attestations verified via Cosign / Sigstore.
   - Secrets must never be baked into container layers or Git repos. Secret salting and runtime injection must leverage AWS Secrets Manager, Parameter Store, or External Secrets Operator.
4. **AWS EKS / Fargate Serverless Deployment**:
   - Deployments must target AWS EKS Fargate using declarative manifests under `k8s/` or `iac/`.
   - All Fargate pods must adhere to serverless constraints: no `privileged: true`, no `hostPath`, no `hostNetwork`.
   - Pod resources (`requests` and `limits`) must align strictly with AWS Fargate vCPU and memory allocation brackets (e.g., 0.25 vCPU / 512Mi–2Gi, 0.5 vCPU / 1Gi–4Gi, 1 vCPU / 2Gi–8Gi).
   - Ingress controllers must declare AWS Application Load Balancer (ALB) with IP target routing (`alb.ingress.kubernetes.io/target-type: ip`).
   - IAM access must use IAM Roles for Service Accounts (IRSA) with fine-grained least-privilege policies.
5. **Operator CLI Entry Gate**: All audits, scaffolding, validation, and manifest generation must be executed through `hath0r iac` (`hath0r iac audit`, `hath0r iac init`, `hath0r iac validate`, `hath0r iac salt`, `hath0r iac render`).
6. **Detail**: `docs/governance/strategies/iac-eks-fargate-strategy.md` · `docs/governance/rules/cr-iac-001.md`.

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

Use the verified multi-repo search (all OpenSource products):

```text
is:issue state:open repo:Bayly-AI/HATH0R-Agentic-Framework repo:Bayly-AI/HATH0R-Agentic-POC repo:Bayly-AI/HATH0R-CLI repo:Bayly-AI/HATH0R-MCP repo:Bayly-AI/HATH0R-ATC
```

Canonical definition: group `AGENTS.md` (*Open issues tracking*). Also listed in `docs/README.md`.

## Branch & PR targets (CRITICAL — cr-branch-gov-001)

1. **Issue first**: create a GitHub issue before any work branch (`hath0r branch start <type> <issue> <slug>`). No issue → no branch.
2. Branch from `development` only, using:
   `feature|bugfix|enhancement|research|fix|chore/<issue-number>-short-slug`
   Example: `chore/4-control-tower-cli`
3. Validate branch: `hath0r branch validate <branch-name>`.
4. Open the PR with **base = `development`** (`hath0r pr create --semver <patch|minor|major>` — feature work never targets testing/staging/master).
5. Work PRs → `development` (agent/bot review + CODEOWNERS; owner `@somesayray` has admin merge authority).
6. Merge into **`development` only** for feature work (`hath0r pr merge <n>`).
7. Promote via `development → testing → staging → master` (`hath0r promote to <stage> --gate`) — do not skip stages; **human gate** required before `staging` and `master`.
8. **PR CI failures notify `@somesayray`** via `.github/workflows/notify-pr-failure.yml`.

### Canonical branches (locked)

`development` (default), `testing`, `staging`, `master`

- Must not be deleted
- Must not be used as feature/work branches
- Must not be merged into each other except along the promotion path above
- Branch protection: PR required, CODEOWNERS & `validate-promotion-path` required, no force-push, no deletions (owner `@somesayray` admin bypass enabled; human gate enforced on `staging`/`master`)

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
   - `/Users/raybayly/Development/OpenSource/hath0r-framework/docs/developers/hathor-playbook-001-repo-init-setup-20260919.md`
   - If the playbook is missing or incomplete, **create or update it first**, then proceed.
2. **Same-technology runbook** — Locate a runbook for an **individual repo with the same technology stack** (e.g. React+Vite UXP, Python CLI):
   - Prefer a sibling/product `docs/runbook.md` (or `docs/*runbook*`) in that tech family.
   - If none exists, **create a tech-appropriate runbook in the target repo** before finishing init.
3. Only after (1) and (2) are satisfied: apply fileset/layout, `.hath0r/`, `cfg/`, contracts pin, `AGENTS.md` identity, and `./bin/hath0r-bootstrap.sh`.

Do not skip the playbook/runbook gate. Layout scaffolding without a documented ops path is incomplete initialization.

## CR-SEMVER-BUMP-001 (Semantic Version Bump on Every PR — CANONICAL)
- Every pull request that is created and merged must create or bump this product's Semantic Version (`MAJOR.MINOR.PATCH`, https://semver.org). The root `VERSION` file is the source of truth; keep `VERSION`, `pyproject.toml` and `CHANGELOG.md` in step with it.
- Pick the bump by impact: MAJOR for breaking changes, MINOR for backward-compatible features, PATCH for fixes, docs, chores and everything else. `Version Impact: none` is not allowed.
- New products start at `0.1.0`.
- Declare the bump in the PR body as `Version Impact: patch|minor|major` and add a matching `CHANGELOG.md` entry. Verify with `hath0r release validate` before announcing complete.
- A PR merged without a version bump is not Complete.

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

## Hyper Context Subsystem Pointers
- **Engine Core Subsystem**: `src/hath0r_engine/AGENTS.md`
- **Docs Subsystem**: `docs/AGENTS.md`
- **Contracts Subsystem**: `contracts/AGENTS.md`
- **Testing Subsystem**: `tests/AGENTS.md`
- **Configuration Subsystem**: `cfg/AGENTS.md`
- **Library Subsystem**: `lib/AGENTS.md`
- **Archive Subsystem**: `archive/AGENTS.md`

## AgentGraph Substrate

This repository is governed by the Hath0r AgentGraph substrate. Dynamic rule retrieval, role RBAC, and policy graphs are stored under `.hath0r/agentgraph/`.
- Query status: `hath0r agentgraph status`
- Query rules: `hath0r agentgraph query "<topic>"`
- Route role: `hath0r agentgraph route --role <role>`
- Sync rules & `CLAUDE.md`: `hath0r agentgraph sync`
- Validate rules: `hath0r agentgraph validate`

---

## CR-SONAR-PREANNOUNCE-001 (SonarCloud Thresholds Before Announcing Complete — CANONICAL)
- **Pre-Announcement SonarCloud Gate**: Before announcing any work as Complete, the agent MUST analyze the code and confirm it meets this repository's SonarCloud Quality Gate thresholds (coverage on new code, duplication, reliability, security, maintainability, and security hotspots reviewed).
- **How to Verify**: Use `hath0r quality sonar` (project key from `sonar-project.properties`) together with local test and coverage runs. If the gate cannot be checked, state that plainly instead of announcing Complete.
- **Not Complete Until Green**: A failing or unverified Quality Gate means the work is not Complete.

---

## CR-TASK-EVAL-001 (Automatic Task Evaluation Before Announcing Complete — CRITICAL · CANONICAL)
- **Mandatory Pre-Announcement Task Evaluation Gate**: Every task MUST be evaluated across the 4-tier hybrid evaluation pipeline (Tier 1 Deterministic Rubrics, Tier 2 Trajectory & FinOps Efficiency, Tier 3 Adversarial & Diff Critics, Tier 4 Goal Alignment & Consensus) prior to announcing work as Complete.
- **Composite Reward Threshold**: Task completion requires `passed_gate: true` and composite reward score `R_task >= 0.80` persisted in `.hath0r/evals/latest.json` and compounded as an `eval:<task_id>` node in `.hath0r/memory/graph.json`.
- **How to Verify**: Run `hath0r evals run` and `hath0r evals verify` before announcing Complete (`EndOfTaskBot`, `TaskAnnouncerBot.announce_complete`, and `CleanReposWorkflowBot` enforce this gate automatically).
- **Mandatory Eval Scorecard Summary After Every Task (CRITICAL · CANONICAL)**: Immediately after running task evaluations (`hath0r evals run`), the agent MUST always return a structured summary of the **Eval Scorecard** (`eval_id`, `task_id`, `passed_gate`, composite `R_task`, Tier 1–4 scores, and `.hath0r/evals/latest.json` path) in its completion response to the user.
- **Not Complete Until Evaluated & Scorecard Returned**: A missing, failing, unverified, or unreported task evaluation scorecard means the work is not Complete.
