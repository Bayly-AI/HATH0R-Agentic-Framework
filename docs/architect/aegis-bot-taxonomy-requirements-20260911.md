---
id: AEGIS-REQ-BOT-001
title: AEGIS — Bot Taxonomy, Anatomy & Default Command Contract
summary: 1. **Infra reuse only when better** — AEGIS may adopt Infra processes/architecture only where they demonstrably exceed a from-scratch AEGIS design. Every adoption is logged in §9.
doc_type: REQ
diataxis: reference
audience: [architect, agent]
tags: []
version: 0.1.0
status: draft
created: '2026-09-11'
updated: '2026-09-15'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: 180d, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# AEGIS — Bot Taxonomy, Anatomy & Default Command Contract
## Formal Requirements Document

- **Document ID:** AEGIS-REQ-BOT-001
- **Status:** DRAFT (research output — pending operator review)
- **Date:** 2026-09-11
- **Author:** Oz (Agent), commissioned by Raymond Bayly
- **Amended by:** AEGIS-RP-014 (2026-09-13, operator-approved): `status` gains a `governance` group; `manifest --with-governance`; `report.payload.decisions[]` (details in RP-014 §3/§11)
- **Sources:** AEGIS "CLI" board, AEGIS/HATHOR "Overview" board (Agentic Application Framework)

---

## 0. Canonical Rules Governing This Document

1. **Infra reuse only when better** — AEGIS may adopt Infra processes/architecture only where they demonstrably exceed a from-scratch AEGIS design. Every adoption is logged in §9.
2. **Research only** — AEGIS work is limited to reports and requirements. No implementation is authorized by this document.

---

## 1. Purpose & Scope

Define the canonical taxonomy (bot families and roles), anatomy (mandatory structural blocks), runtime behavior, knowledge/storage model, and the default command contract that **every** AEGIS bot MUST implement.

Out of scope: implementation language choices, deployment topology, Control Tower internal design, MCP server schemas.

Requirement keywords follow RFC 2119 (MUST / SHOULD / MAY).

---

## 2. Taxonomy Requirements (AEG-BOT-TAX)

### AEG-BOT-TAX-001 — Microbot architecture
Every AEGIS capability MUST be delivered as a small, single-role bot ("microbot"). One bot, one responsibility.
**Acceptance criteria:**
- A bot's manifest declares exactly one primary role.
- Composition of roles occurs only at orchestration level (Proctor/Process), never inside a bot.

### AEG-BOT-TAX-002 — Three canonical families
Every bot MUST belong to exactly one family: **Orchestration**, **Information Hierarchy**, or **Observation**.
**Acceptance criteria:**
- Manifest carries a `family` field with one of the three enumerated values.
- No bot appears in more than one family in the Tower registry.

### AEG-BOT-TAX-003 — Orchestration family roster
The Orchestration family consists of: **Proctor-Bot** (contract validation + routing), **Process-Bot** (hierarchy resolution and conducted-run state), **Operator-Bot** (exclusive external-connection broker). The **Control Tower** is an authenticated asynchronous platform authority and is NOT a bot.
**Acceptance criteria:**
- Every bot dispatch enters through `CLI → Proctor`. Process is required only for conducted runs; Operator is required only for third-party effects; Tower authority calls/reconciliation use a separate authenticated CLI path and are not a universal terminal hop. *(Aligned with CORE `AEG-REQ-BOT-003`, ARCH-001 §5, and RP-010 §2.)*
- Only Operator-Bot holds connection-pool access rights.

### AEG-BOT-TAX-004 — Information Hierarchy family roster
The Information Hierarchy family consists of six tier bots, each chaining to the next: **Procedure-Bot → Strategy-Bot → Playbook-Bot → Runbook-Bot → Workflow-Bot → Checklist-Bot**.
**Acceptance criteria:**
- Each tier bot resolves only its own tier and delegates downward.
- Every unit of work executed under AEGIS can be traced to a complete chain (Procedure through Checklist).
- A Procedure MAY have multiple Strategies; all other links are one-to-many downward.

### AEG-BOT-TAX-005 — Observation family roster
The Observation family consists of **Observation-Bot** (parent) and children: **task-Bot**, **benchmark-Bot**, **success-rate-Bot**, **retry-Bot**, **token-Bot**.
**Acceptance criteria:**
- Observation bots are strictly passive: read/record only, never mutate work products, knowledge tiers, or connections.
- All telemetry rolls up to the Control Tower.

### AEG-BOT-TAX-006 — CLI as sole control plane
Bots MUST be reachable only through the AEGIS CLI. Agents, users, and bots MUST NOT invoke bots directly.
**Acceptance criteria:**
- No bot exposes a public listener outside CLI mediation.
- Bot-to-bot calls traverse the CLI routing layer (Proctor).

---

## 3. Anatomy Requirements (AEG-BOT-ANA)

Every bot MUST be composed of the following seven blocks.

### AEG-BOT-ANA-001 — Identity block
UUID, canonical name (`<role>-Bot`), family, tier (where applicable), semver version, owner, and digital provenance (builder, source, build time).
**Acceptance criteria:**
- `version` command returns all identity fields.
- Provenance is verifiable against the Tower registry entry.

### AEG-BOT-ANA-002 — Machine-readable manifest
A JSON manifest declaring: commands + argument schemas, exit codes, capabilities, knowledge scopes read/written, and required connections (by name, never credentials).
**Acceptance criteria:**
- `manifest` command emits the manifest; it validates against AEGIS manifest schema 1.1.0 (AEGIS-RP-001, as amended by RP-014).
- Any command not declared in the manifest is a contract violation and MUST be refused by the CLI.

### AEG-BOT-ANA-003 — Versioned communication contract
Bots and agents MUST exchange JSON by default with standardized success/error codes. Contracts are semver-versioned.
**Acceptance criteria:**
- Contract-version mismatch produces a structured refusal (never a best-effort guess).
- `contract validate <payload>` pre-flights any request without side effects.

### AEG-BOT-ANA-004 — Code-agnostic executor
The role logic MAY be implemented in any language provided the manifest and contract are honored.
**Acceptance criteria:**
- Conformance is asserted by the standard `selftest` command, not by implementation inspection.

### AEG-BOT-ANA-005 — Knowledge interface
Reads follow the tiered search order (§5); writes are knowledge microbursts only, always mediated by the CLI.
**Acceptance criteria:**
- No bot holds direct store credentials (vector DB, MCP) — access is CLI-brokered.
- Every write carries the mandatory metadata set (AEG-BOT-KNO-004).

### AEG-BOT-ANA-006 — Indirect connection interface
Worker bots request external sessions from Operator-Bot. Class-1 flows are proxied so workers never receive provider credentials; a declared Class-2 flow may provide only a scoped, short-lived, run-bound token held in memory (RP-011).
**Acceptance criteria:**
- Secrets never appear in a worker bot's config, logs, knowledge writes, or memory dumps; Class-2 tokens are never persisted.
- Operator-Bot validates/reuses pool connections before creating new ones.

### AEG-BOT-ANA-007 — Telemetry surface
Bots emit standardized events (task start/stop, tokens, retries, outcome) consumable by the Observation family.
**Acceptance criteria:**
- Event schema is uniform across all bots.
- A run with telemetry disabled is flagged `degraded` (exit 2) by `status`.

---

## 4. Runtime Behavior Requirements (AEG-BOT-RUN)

### AEG-BOT-RUN-001 — Request lifecycle
Every bot request MUST enter through CLI intake and Proctor contract/provenance validation plus routing. Conducted-run requests additionally attach Process-owned run state and any required hierarchy; third-party effects branch through Operator; telemetry/reporting is appended locally and reaches Tower asynchronously. Direct bot capabilities and authenticated Tower authority commands omit branches that do not apply.
**Acceptance criteria:**
- Every dispatch has an admission record and attributable result; every completed conducted run additionally has an authoritative run-ledger record, its required hierarchy/ticket references, and correlated telemetry. Tower unavailability does not invalidate a locally committed run within the applicable trust TTL.

### AEG-BOT-RUN-002 — Statelessness
Bots MUST be stateless between invocations; durable state lives in sanctioned plane stores and authoritative run/audit ledgers. Telemetry is a correlated observation/export view, not the sole state authority.
**Acceptance criteria:**
- Killing and reinvoking a bot mid-idle loses no durable data.
- Conducted-run state is reconstructed from the Process-owned run event log; bot working memory is disposable.

### AEG-BOT-RUN-003 — Graceful degradation
On third-party dependency unavailability, a bot MUST consult Operator-Bot's declared connection fallback; other dependencies use their owning plane/capability policy. If no permitted fallback exists, the CLI returns a structured error—never a crash, hang, or guessed result.
**Acceptance criteria:**
- Error envelope contains `code`, `message`, `remediation`, `provenance`, `ttl`.
- Degraded operation is reported as `{degraded:true}` at the CLI boundary; bot-boundary `status` may return 2, which the chassis translates per ADR-003 §2.3.

### AEG-BOT-RUN-004 — Retry semantics
Transient failures MUST be retried up to 5 times with backoff; retries are recorded by retry-Bot; exhaustion produces a failure report with full context.
**Acceptance criteria:**
- Retry counts and outcomes are queryable per run.
- No silent retry beyond the cap. *(Adopted from Infra cr-007 — see §9.)*

---

## 5. Knowledge & Storage Requirements (AEG-BOT-KNO)

### AEG-BOT-KNO-001 — Tiered search order
Reads MUST follow: **Project → Machine → Organization → Public**, all through the CLI.
**Acceptance criteria:**
- Retrieval logs show tier traversal order.
- Project-level hits short-circuit lower-priority tiers unless breadth is explicitly requested.

### AEG-BOT-KNO-002 — Tier backing stores
Project = repo-local knowledge + project MCP (under the hidden `.aegis/` folder of the Universal Project Layout). Machine = CLI knowledge + local vector server (hybrid keyword + vector). Organization = org MCP. Public = last resort.
**Acceptance criteria:**
- Each tier is independently reachable and independently health-checked via `status --group knowledge`.

### AEG-BOT-KNO-003 — Microburst writes only
Knowledge writes MUST be small, session-scoped, incremental microbursts. Bulk/full syncs are prohibited unless explicitly operator-requested.
**Acceptance criteria:**
- Each microburst is attributable to a single run/session.
- No scheduled bulk sync exists in any bot.

### AEG-BOT-KNO-004 — Mandatory record metadata
Every knowledge record MUST carry: provenance, TTL/staleness stamp, draft/verified status, hierarchy-tier link, and retrieval-quality fields (title + breadcrumb prepended to each chunk).
**Acceptance criteria:**
- Records missing any field are rejected at write time.
- New writes default to `draft`; only human review promotes to `verified`.

### AEG-BOT-KNO-005 — Retrieval honesty
Retrieval MUST return "no compliant match" rather than low-quality batches; expired-TTL knowledge is flagged, never silently served.
**Acceptance criteria:**
- A quality threshold gate exists on all retrieval paths.
- Responses containing expired records carry an explicit staleness flag per record.

### AEG-BOT-KNO-006 — No secrets in knowledge
Secrets MUST never be stored in bots or any knowledge tier.
**Acceptance criteria:**
- Automated redaction/PII-secret scan runs on every microburst before commit.

---

## 6. Default Command Contract (AEG-BOT-CMD)

### Global conventions

### AEG-BOT-CMD-001 — JSON-first I/O
Every command defaults to JSON output; `--human` renders text.
**Acceptance criteria:** JSON output of every command validates against its manifest-declared schema.

### AEG-BOT-CMD-002 — Exit codes
`0` = healthy/success, `1` = failure, `2` = degraded/warning. *(Adopted from Infra CR-017 — see §9.)*
**Acceptance criteria:** No command uses any other exit code; `selftest` verifies all three paths.

### AEG-BOT-CMD-003 — Standard error envelope
All failures emit `{code, message, remediation, provenance, ttl}`.
**Acceptance criteria:** Error envelope schema is shared across all bots; free-text-only errors are non-compliant.

### AEG-BOT-CMD-004 — Manifest completeness
Every implemented command MUST appear in the manifest; the CLI refuses undeclared commands.
**Acceptance criteria:** CLI-side enforcement test exists; drift between manifest and binary fails `selftest`.

### Required commands (every bot)

### AEG-BOT-CMD-010 — `health`
Liveness/readiness only. MUST complete in <250 ms with no network calls.
**Acceptance criteria:** Returns exit 0/1/2; safe to poll at high frequency; no side effects.

### AEG-BOT-CMD-011 — `status`
Grouped deep checks: identity, config, contract, knowledge access, connections (via Operator), telemetry, governance. Supports `--full`, `--group <X>`, `--json`.
**Acceptance criteria:**
- Per-bot groups are the slim **seven** above; the added `governance` group reports digests-match, rule-fixture health, and the principle-set version (RP-014). The full platform-wide check set lives at CLI/Tower level, not per bot. *(Pattern adopted, payload rejected, from Infra CR-017 — see §9.)*
- Text and JSON outputs carry identical data.

### AEG-BOT-CMD-012 — `version`
Semver + build hash + contract version + provenance.
**Acceptance criteria:** Output is sufficient to verify the bot against the Tower registry without network access to the build system.

### AEG-BOT-CMD-013 — `manifest`
Emit the machine-readable command/capability manifest; `manifest --with-governance` additionally emits the directive, rules, and principles bodies (RP-014).
**Acceptance criteria:** Output validates against the AEGIS manifest schema; equals what the CLI has registered.

### AEG-BOT-CMD-014 — `contract`
Show contract version; `contract validate <payload>` pre-flights a request.
**Acceptance criteria:** Validation is side-effect free and returns structured pass/fail with per-field errors.

### AEG-BOT-CMD-015 — `config show|validate`
Redacted config display; schema validation.
**Acceptance criteria:** No secret values ever rendered; validation failures name the offending keys only.

### AEG-BOT-CMD-016 — `selftest`
Manifest-driven smoke test of the bot's own commands.
**Acceptance criteria:** Exercises every declared command's help/dry-run path; exit codes per AEG-BOT-CMD-002.

### AEG-BOT-CMD-017 — `knowledge query|push`
Tier-aware read; microburst write (draft), through the CLI.
**Acceptance criteria:** Honors AEG-BOT-KNO-001..006 end to end.

### AEG-BOT-CMD-018 — `report`
Emit standardized run report to Observation/Tower; the payload carries `decisions[]` (≤ 10) citing the governing principle for each discretionary choice (RP-014 §3.5.3).
**Acceptance criteria:** Report schema uniform across bots; includes hierarchy chain reference, telemetry summary, and `decisions[]`.

### AEG-BOT-CMD-019 — `drain|stop` (conditional)
Required only for resident bots (Operator-Bot, Observation-Bot). `drain` completes in-flight work, refuses new; `stop` terminates after drain.
**Acceptance criteria:** No in-flight loss on drain; non-resident bots omit these commands from their manifest.

---

## 7. Security Requirements (AEG-BOT-SEC)

### AEG-BOT-SEC-001 — Credential resolution order
Operator-Bot resolves credentials in the order: secrets manager (brokered execution) → project env fallback → credentials file fallback, and treats non-secrets-manager paths as degraded mode.
**Acceptance criteria:** Fallback use is logged and surfaced as exit 2 in `status --group connections`. *(Aligned with Infra cr-005 pattern — see §9.)*

### AEG-BOT-SEC-002 — Connection exclusivity
Only Operator-Bot touches the Connection Pool; worker bots receive brokered sessions.
**Acceptance criteria:** Static and runtime checks confirm no worker bot links a connector SDK directly.

### AEG-BOT-SEC-003 — Provenance verification
Bots MUST be verifiable (identity + provenance) before Proctor routes work to them.
**Acceptance criteria:** Unregistered or provenance-mismatched bots are refused with a structured error and reported to the Tower.

---

## 8. Observability Requirements (AEG-BOT-OBS)

### AEG-BOT-OBS-001 — Uniform event schema
All bots emit the same telemetry event shapes (task lifecycle, tokens, retries, outcomes, benchmarks).
**Acceptance criteria:** Observation children (task/benchmark/success-rate/retry/token) can consume any bot's events with zero bot-specific adapters.

### AEG-BOT-OBS-002 — Tower rollup
All observation data rolls up to the Control Tower for cross-project visibility.
**Acceptance criteria:** Per-bot, per-project, and per-machine views are derivable from Tower query records that correlate deduplicated rollups with ingested/linked authoritative run ledgers and provider receipts; telemetry alone is not treated as run authority.

---

## 9. Infra Adoption Decision Log (per canonical rule 1)

| Infra source | Decision | Rationale |
|---|---|---|
| CR-017 exit codes (0/1/2) | **Adopt** | Proven, minimal, exceeds inventing a new scheme. |
| CR-017 grouped `status` pattern | **Adopt pattern only** | Grouping + `--full`/`--group`/`--json` is sound. |
| CR-017 full 11-group payload per bot | **Reject** | Too heavy for microbots; full check set belongs at CLI/Tower level. |
| cr-007 retry cap (5, with context capture) | **Adopt** | Simple, bounded, already validated in Infra operations. |
| cr-005 secrets-manager-first credential order | **Adopt (Operator-Bot only)** | Exceeds ad hoc env-file handling; scoped to the single connection broker. |
| Infra monolithic CLI-service model | **Reject** | AEGIS microbot + single control plane supersedes it. |

---

## 10. Open Questions — RESOLVED (2026-09-11)

All five questions have dedicated research papers in this folder:

1. **Manifest schema v1** → **AEGIS-RP-001** (`./aegis-rp-001-manifest-schema-v1-20260911.md`) — full JSON schema; 4-phase HELLO/OFFER/BIND/VERIFY handshake; capability-based routing; AEG-MAN-001..007.
2. **Registry model** → **AEGIS-RP-002** (`./aegis-rp-002-registry-discovery-20260911.md`) — hybrid: machine-local index (MBI) for all runtime routing, Tower registry (TBR) as authority; bounded offline trust; AEG-REG-001..006.
3. **Telemetry transport** → **AEGIS-RP-003** (`./aegis-rp-003-telemetry-transport-20260911.md`) — spool-and-drain (CLI append to local spool, Observation-Bot drains); event bus rejected at machine tier; AEG-TEL-001..007.
4. **Draft→verified promotion** → **AEGIS-RP-004** (`./aegis-rp-004-knowledge-promotion-20260911.md`) — status-on-record, queue-as-view; tiered reviewer authority; dispute/supersede/expiry lifecycle; AEG-KPW-001..008.
5. **Hierarchy consolidation** → **AEGIS-RP-005** (`./aegis-rp-005-hierarchy-consolidation-20260911.md`) — six identities, one chassis; consolidation rejected; fan-out chain resolution; AEG-HIE-001..006.

Remaining open questions are tracked inside each paper's own Open Questions section.

---

*Research output only. No implementation authorized. Review and amend before promotion to verified status.*
