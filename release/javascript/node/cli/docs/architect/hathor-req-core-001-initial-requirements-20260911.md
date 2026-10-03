---
id: HATHOR-REQ-CORE-001
title: HATHOR — Initial Platform Requirements (Core)
summary: 'RFC 2119 keywords apply: **MUST / SHOULD / MAY**. Every requirement in this document is prefixed `AEG-REQ-<AREA>-###`. Acceptance criteria are listed inline. Traceability tags to the source research paper appear in sq...'
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
# HATHOR — Initial Platform Requirements (Core)
## Consolidated Requirements for the HATHOR Agentic Governance Platform

- **Document ID:** HATHOR-REQ-CORE-001
- **Status:** DRAFT v0 — greenfield platform requirements, pending operator review
- **Date:** 2026-09-11
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Supersedes:** N/A (new-project bootstrap)
- **Consolidates:**
  - HATHOR-REQ-BOT-001 (bot taxonomy, anatomy, default command contract)
  - HATHOR-RP-001..006 (manifest, registry, telemetry, knowledge promotion, hierarchy topology, ticketing plane)
  - HATHOR-ADR-001 (target command tree — `hath0r-adr-001-target-command-tree-20260911.md`)
  - HATHOR Containerization article (bot ↔ container isomorphism)
  - HATHOR CLI Research Report (industry baseline)
  - InfraOS carry-overs (see §12 — decision log)
- **Companion docs:** `hathor-arch-001-architecture-mermaid-20260911.md` (diagrams), plan `HATHOR-PLAN-001` (platform roadmap — `hath0r-plan-001-platform-roadmap-20260913.md`)
- **Amended by (2026-09-13):** HATHOR-ADR-002/RP-009 (Orchestration Gateway; gate registry grows to 15); HATHOR-ADR-003 (nine-domain surface; exit-code boundaries); HATHOR-ADR-004 (layout/state residency; OS scope); HATHOR-CANON-010 (canonical registries). Amended in place below; residual edits tracked in `PENDING-EDITS.md`.

RFC 2119 keywords apply: **MUST / SHOULD / MAY**. Every requirement in this document is prefixed `AEG-REQ-<AREA>-###`. Acceptance criteria are listed inline. Traceability tags to the source research paper appear in square brackets, e.g. `[RP-001 §2.4]`.

---

## 0. Framing

### 0.1 What HATHOR is
HATHOR is an **agentic governance platform** — a code-agnostic, agent-agnostic control plane that turns humans + AI agents into first-class, accountable actors against any codebase or operational surface. It is the concrete realization of the HATHOR Agentic Application Framework's control-plane pillar.

### 0.2 What HATHOR is not
- Not an AI model or foundation-model wrapper.
- Not a workflow-automation SaaS.
- Not a replacement for Jira/ADO/GitHub — it *unifies* work tracking above them via the Ticketing Plane.
- Not a rewrite of `infraos-os`. HATHOR is a **greenfield core platform**; specific InfraOS assets are carried forward per §12.

### 0.3 Canonical rules (project-level)
1. **CLI is the sole control plane.** Every agent, human, and bot reaches every capability through one CLI contract. No secondary control surface may be added without ADR.
2. **Refuse-never-guess.** Any structural, contract, provenance, or authority failure MUST produce a structured refusal with a remediation hint. Silent fallback is a defect.
3. **Provenance over recency.** Verified provenance and quality outrank freshness in retrieval, routing, and promotion decisions.
4. **Infra reuse only when better.** An InfraOS component is adopted only when it *demonstrably exceeds* a from-scratch HATHOR design. Every adoption is logged (§12).
5. **Builder + verifier, never operator.** Agents build and validate; humans authorize promotion. Deploy authority originates only from a ticket.
6. **Graceful degradation with bounded offline trust.** Every plane MUST tolerate loss of its authority for a bounded TTL, must report the condition honestly, and MUST refuse authority-originating actions past TTL.

### 0.4 Success shape (v1 platform)
- One CLI binary (`hath0r`) with ≤ 9 top-level domains + always-on meta commands (ADR-003 §2.2).
- Three brokerable planes of authority (Registry, Knowledge, Ticketing) — one CLI to reach them all.
- Micro-bot runtime with signed manifests, capability-based routing, and a spool-and-drain telemetry substrate.
- Universal Project Layout (`.hath0r/`) recognizable in any repository — code-agnostic.
- Every runtime action traceable end-to-end: **intent → ticket → hierarchy chain → bot(s) → telemetry → outcome → knowledge microburst**.

---

## 1. Scope

### 1.1 In scope for v1
- Core CLI (`hath0r`) — command tree, global contract, exit-code contract, schema introspection.
- Bot chassis (shared implementation for all bot roles) + reference implementations of each canonical bot.
- Manifest v1 + registry (MBI + TBR).
- Telemetry v1 (spool-and-drain, event envelope, Observation-Bot drain).
- Knowledge Plane v1 (tiered search, microburst writes, promotion queue-as-view).
- Ticketing Plane v1 (canonical contract; Jira + ADO + GitHub adapters + Backup TS).
- Universal Project Layout tooling (`hath0r repo init|validate`).
- Container taxonomy + build/lint pipeline (Class A/B/C/D).
- Micro-linter set (build-time immune system).
- DVO deploy-ticket workflow (governance gate).

### 1.2 Out of scope for v1
- Cloud-hosted Control Tower UI (Tower APIs are in scope; the browser UI is a v2 concern).
- Non-hierarchy execution engines beyond `Workflow-Bot`'s existing capability set.
- Provider adapters beyond Jira / Azure DevOps / GitHub.
- Auto-promotion of knowledge or work (both remain human-gated).
- Multi-tenant SaaS operation. HATHOR v1 is per-org, self-hostable.

---

## 2. Actors & Personas

| Actor | Role | Primary surface |
|---|---|---|
| **Human operator** (dev/DVO/curator) | Authors tickets, promotes drafts, executes deploys | CLI (TTY) + web (Tower v2) |
| **AI agent** (any harness) | Builds, verifies, files/reads work, drives runbooks | CLI (non-interactive JSON) |
| **Bot** | Single-role capability provider | CLI-mediated bot-to-bot |
| **Control Tower authority** | Registry / policy / audit / rollup | Tower service (registry API) |
| **External provider** (Jira/ADO/GitHub/Teams/Slack/…) | System of record for work or notification | Operator-Bot connection pool only |

All actors reach bots exclusively through the CLI. No bot exposes a public listener outside CLI mediation. `[BOT-TAX-006]`

---

## 3. Platform Requirements (AEG-REQ-PLAT)

### AEG-REQ-PLAT-001 — Single CLI control plane
The platform MUST expose exactly one operational entrypoint (`hath0r`). Every agent, human, or bot capability is reached through it.
**AC:** No auxiliary control plane is documented for public use; static analysis fails any bot that opens a non-CLI listener.

### AEG-REQ-PLAT-002 — Code-agnostic, agent-agnostic
The CLI contract MUST NOT assume a specific implementation language, agent runtime, or repo shape beyond the Universal Project Layout (§7).
**AC:** Reference bots ship in at least two languages by v1.0 (Python + Go); an external agent harness completes the same task using only public CLI contracts.

### AEG-REQ-PLAT-003 — Three planes of authority, one control plane
The platform MUST maintain exactly three source-of-truth planes — **Registry Plane** (which bots may run), **Knowledge Plane** (what we know), **Ticketing Plane** (what work exists) — all reached through the single CLI. `[RP-006 §2.2]`
**AC:** `hath0r planes list` enumerates the three; each plane has a designated authority and a bounded-degradation policy.

### AEG-REQ-PLAT-004 — Communication contract by default
Inter-actor communication MUST default to versioned JSON with a standardized error envelope `{code, message, remediation, provenance, ttl}`. `[BOT-ANA-003, CMD-003, RP-001 §2.3]`
**AC:** Every bot's manifest declares a contract version; contract-mismatch produces a structured refusal, never a best-effort guess.

### AEG-REQ-PLAT-005 — Exit-code contract (public API)
Exit codes MUST follow the canonical table (§4.5); no command may reuse a code for a different meaning. `[ADR-001, BOT-CMD-002]`
**AC:** `hath0r doctor exit-codes` prints the table; conformance test verifies every command in the manifest.

### AEG-REQ-PLAT-006 — Universal Project Layout
Every HATHOR project MUST carry a canonical layout (§7). Bots and CLI logic MUST treat every project identically once the layout is validated.
**AC:** `hath0r repo validate` returns exit 0 for a compliant project; scoped `AGENTS.md` chain resolves cleanly from root down.

### AEG-REQ-PLAT-007 — Graceful degradation with bounded offline trust
Every plane MUST tolerate authority loss up to a trust TTL (default 72h), report the condition, and refuse authority-originating actions past TTL. `[RP-002 §3.4, RP-006 §5.4]`
**AC:** With Tower unreachable, `verified-tower` bots continue; `verified-local` bots continue within TTL; expired trust is refused with `PROVENANCE_UNVERIFIED`.

### AEG-REQ-PLAT-008 — Progressive disclosure of the command tree
The root help MUST expose ≤ 9 top-level domains + always-on meta commands (revised from ≤ 8 by ADR-003 §2.2; a tenth domain requires an ADR). Deprecated/legacy paths are hidden by default. `[CLI-Research §5-D, ADR-001, ADR-003]`
**AC:** `hath0r --help` renders one screen; `hath0r --help --include-legacy` shows aliases.

### AEG-REQ-PLAT-009 — Machine-readable schema introspection
The CLI MUST expose a bounded schema surface (`hath0r schema` with `--domain` and pagination). Full unfiltered dump is opt-in only. `[Spike 04, ADR-001]`
**AC:** Default filtered response ≤ 8 KB per page; every command has `effects`, `output_kind`, `cardinality` declared.

### AEG-REQ-PLAT-010 — Complete audit trail
Every mutating command invocation MUST produce a durable audit record consumable by the Tower: caller identity, intent, ticket ref, hierarchy chain, arguments (redacted), exit code, envelope, telemetry `run_id`. `[CLI-Research §3.4]`
**AC:** Any mutation is reconstructable from its authoritative audit/run ledger and, for third-party effects, provider receipt/idempotency record; telemetry correlates and exports that evidence without becoming the sole source of truth. No mutation is audit-less.

---

## 4. CLI Contract Requirements (AEG-REQ-CLI)

### 4.1 Command tree (canonical top-level)

```
hath0r
├── help | version | schema | doctor | planes         # always-on meta
├── process …                                          # Process-Bot — hierarchy execution + orchestration runs
├── proctor …                                          # Proctor-Bot — gates, policy, gateway admission
├── operator …                                         # Operator-Bot — external systems (brokered)
├── tower …                                            # Control Tower authority surface (incl. `tower bots …`)
├── knowledge …                                        # Knowledge Plane
├── work …                                             # Ticketing Plane
├── repo …                                             # Universal Project Layout + repo ops
├── delivery …                                         # PR / quality / release façade
└── validate …                                         # Continuous Validation System (RP-007/TS-001)
```

Nine domains per ADR-003 §2.2: `validate` is promoted (highest agent-traffic surface); registry introspection folds under `tower bots …` with `hath0r bots …` retained as a hidden alias. Compatibility aliases from InfraOS are hidden behind `--include-legacy` (see §12).

### AEG-REQ-CLI-001 — Global contract flags
```
--output, -o json|text|auto  # default: TTY→text, pipe→json
--profile <name>              # config profile
--quiet                       # suppress non-error telemetry stream
--include-legacy              # opt-in for hidden aliases
```
**AC:** Every command inherits these; `-o json` output validates against the command's declared `output_schema`.

### AEG-REQ-CLI-002 — Mutation flags where meaningful
`--dry-run` MUST be present on every non-idempotent command that can produce a meaningful plan; `--yes` gates non-interactive live mutations. `[ADR-001]`
**AC:** In a non-TTY context, live mutation without `--yes` returns exit 7 `confirmation_required`.

### AEG-REQ-CLI-003 — Bounded collections
Any command producing a collection MUST support `--fields`, `--limit`, and `--cursor` (cursor pagination). Default `--limit` 25.
**AC:** No collection endpoint returns >8KB by default without an explicit `--limit` override.

### AEG-REQ-CLI-004 — Stream discipline
Data on stdout; telemetry / progress / warnings on stderr; interactive prompts only when a TTY is detected; never both. `[CLI-Research §3.1, CLI Spec P3+P4]`
**AC:** Piped stdout parses cleanly; `--quiet` suppresses stderr to error-only.

### AEG-REQ-CLI-005 — Discoverability integrity
`hath0r help`, `hath0r <cmd> --help`, and `hath0r <cmd> help` MUST all work. `[CLI-Research §2.3.2]`
**AC:** No help path returns exit 2 "invalid choice".

### 4.5 Canonical exit codes
| Code | Meaning |
|---|---|
| 0 | Success (including dry-run and idempotent no-op) |
| 1 | Runtime / internal failure |
| 2 | Usage / validation error |
| 3 | Not found |
| 4 | Auth / permission |
| 5 | Conflict / already exists |
| 6 | Dependency unhealthy (connections/mcp/plane) |
| 7 | Confirmation required in non-interactive context |

Named non-error data states (e.g. `degraded`, `changes_pending`) MUST be represented as fields in the response envelope, not by reusing an error code. `[ADR-001]`

**Exit-code boundaries (ADR-003 §2.3).** The table above governs the `hath0r` CLI boundary only. The CR-017 bot boundary (`0|1|2`, where 2 = degraded) applies to bot executables and is translated by the chassis: a bot-boundary `2` surfaces as `{degraded: true}` in the response envelope, never as CLI exit 2. Where a distinct process exit is operationally required for a data state, it MUST be declared as a CLI Spec v0.3 `outcomes[]` entry with a code overlapping no error code. Legacy corpus phrasing "degraded (exit 2)" reads accordingly.

**CLI Spec envelope mapping.** The HATHOR error envelope `{code, message, remediation, provenance, ttl}` maps onto the CLI Spec error envelope as `code → error.kind`, `message → error.message`, `remediation → error.hint`, `{provenance, ttl} → error.details`; `hath0r schema` declares the full `errors[]` (and `outcomes[]`) tables so both contracts hold simultaneously.

---

## 5. Bot Taxonomy Requirements (AEG-REQ-BOT)

Full taxonomy is defined in HATHOR-REQ-BOT-001. This section restates the load-bearing rules and adds the platform-level integration.

### AEG-REQ-BOT-001 — Microbot architecture
Every capability MUST be delivered by a single-role bot. Composition happens only at Proctor/Process, never inside a bot. `[BOT-TAX-001]`
**AC:** Manifest declares exactly one `family` and (for hierarchy) `tier`.

### AEG-REQ-BOT-002 — Three canonical families
Every bot MUST belong to exactly one of: **Orchestration**, **Hierarchy**, **Observation**. `[BOT-TAX-002]`

### AEG-REQ-BOT-003 — Orchestration roster
The Orchestration family consists of **Proctor-Bot**, **Process-Bot**, **Operator-Bot**. All bot dispatch enters through `CLI → Proctor`; Process participates only in conducted runs, Operator only for third-party effects, and authenticated Tower authority calls/reconciliation are separate request classes rather than a universal terminal hop. `[BOT-TAX-003, RP-010 §2]`
**AC:** Only Operator-Bot holds connection-pool access; static + runtime checks confirm no worker bot links a provider SDK.

### AEG-REQ-BOT-004 — Hierarchy roster (six identities, one chassis)
The Hierarchy family consists of six tier bots: **Procedure-Bot → Strategy-Bot → Playbook-Bot → Runbook-Bot → Workflow-Bot → Checklist-Bot**. They MAY share an implementation chassis. `[BOT-TAX-004, HIE-001..006]`
**AC:** Registry (MBI/TBR) shows six entries; chassis version is provenance-visible; per-tier telemetry aggregates without payload disambiguation.

### AEG-REQ-BOT-005 — Observation roster
The Observation family consists of **Observation-Bot** (parent) and children **task-Bot**, **benchmark-Bot**, **success-rate-Bot**, **retry-Bot**, **token-Bot**. Observation bots are strictly passive. `[BOT-TAX-005]`

### AEG-REQ-BOT-006 — Control Tower is not a bot
The Control Tower is an authenticated platform authority for registry, policy distribution, identity, revocation, ingest, and audit query. It is not a bot, is never routed to as a bot capability provider, and is not the terminus of every request. `[BOT-TAX-003, RP-010 §2]`

### AEG-REQ-BOT-007 — Seven-block anatomy
Every bot MUST carry: **Identity**, **Manifest**, **Contract**, **Executor**, **Knowledge interface**, **Connection interface**, **Telemetry surface**. `[BOT-ANA-001..007]`

### AEG-REQ-BOT-008 — Default command contract
Every bot MUST implement the default command set: `health`, `status`, `version`, `manifest`, `contract`, `config`, `selftest`, `knowledge`, `report`. Resident bots additionally implement `drain|stop`. `[BOT-CMD-010..019]`
**AC:** `selftest` exercises every declared command's help/dry-run path; missing commands fail registration.

### AEG-REQ-BOT-009 — Statelessness (v1)
All bots MUST be stateless between invocations; durable state lives in sanctioned plane stores and authoritative run/audit ledgers, with telemetry as a correlated observation/export view. `[BOT-RUN-002, AEG-GW-004, AEG-REQ-TEL-007]`
**AC:** Killing and reinvoking mid-idle loses no durable data.

### AEG-REQ-BOT-010 — Bounded retry
Transient failures MUST retry ≤ 5 times with backoff; retries are recorded by retry-Bot; exhaustion produces a failure report with full context. `[BOT-RUN-004]`

---

## 6. Manifest & Registry Requirements (AEG-REQ-MAN, AEG-REQ-REG)

Detailed spec: RP-001 (manifest) and RP-002 (registry).

### AEG-REQ-MAN-001 — Canonical manifest v1
Every bot ships one JSON manifest conforming to schema v1; the canonicalized SHA-256 digest is its registration fingerprint. `[RP-001 §2, AEG-MAN-001]`

### AEG-REQ-MAN-002 — Embedded schemas
Every declared command MUST embed `args_schema` and `output_schema` (JSON Schema 2020-12); the CLI validates both directions. `[AEG-MAN-002]`

### AEG-REQ-MAN-003 — Capability-based routing
Callers address **capabilities** (`<domain>.<noun>.<verb>@<major>`), never bot names. Proctor resolves. `[AEG-MAN-003]`

### AEG-REQ-MAN-004 — Contract negotiation (HELLO/OFFER/BIND/VERIFY)
Contract negotiation MUST follow the four-phase handshake with a fast-path digest comparison for cached bindings. `[RP-001 §3, AEG-MAN-004]`

### AEG-REQ-MAN-005 — Signed provenance
Manifests MUST carry a detached signature verifiable offline against Tower-distributed public keys within their key TTL. `[AEG-MAN-006]`

### AEG-REQ-MAN-006 — Registration-time enforcement
The CLI MUST refuse manifests violating structural rules (resident without drain/stop, non-`0|1|2` exit codes at bot boundary, `microburst_only=false`, embedded credentials). `[AEG-MAN-007]`

### AEG-REQ-REG-001 — Hybrid registry (MBI + TBR)
Runtime resolution uses the machine-local index (**MBI**); the Tower registry (**TBR**) is the authority for registration, keys, and revocation. `[RP-002 §3, AEG-REG-001]`
**AC:** No Tower round-trip appears in any request-path trace; revocations propagate on next reconciliation.

### AEG-REQ-REG-002 — Install-time indexing
The MBI MUST be updated at install/update, never by request-time filesystem scanning. `[AEG-REG-002]`

### AEG-REQ-REG-003 — Verification states
Every MBI entry MUST be exactly one of `verified-tower | verified-local | quarantined`. Only the first two are routable; `verified-local` only within trust TTL. `[AEG-REG-003..004]`

### AEG-REQ-REG-004 — Immediate revocation on reconcile
CRL updates MUST quarantine matching MBI digests before the next dispatch. `[AEG-REG-005]`

### AEG-REQ-REG-005 — Registry introspection
`hath0r bots list [--json]` MUST expose the MBI (identity, capabilities, state, digests) sufficient to diagnose any routing refusal without Tower access. `[AEG-REG-006]`

---

## 7. Universal Project Layout (AEG-REQ-UPL)

### 7.1 Canonical layout
```text
<project>/
  .hath0r/           # hidden HATHOR metadata (manifests, rules, run state, checklists)
    manifests/
    rules/
    state/
      runs/
      checklists/
      spool/                # telemetry spool (per-machine variant may relocate)
    knowledge/              # project-tier knowledge tier
  cfg/              # configuration not required at repo root (canonical port registry: cfg/port-registry.yaml — ADR-004 §2.1)
  src/              # source
  lib/              # assets and non-narrative supporting material
  bin/              # project-specific executables / wrapper scripts
  dist/             # build / distribution output
  test/             # tests and test automation
  docs/             # narrative documentation
  .docker/          # container + deployment files
  AGENTS.md         # root scope; children may override per folder
  Makefile          # OPTIONAL thin façade over stable hath0r CLI contracts
```

### AEG-REQ-UPL-001 — Layout as contract
`hath0r repo validate` MUST succeed only for a project matching the canonical layout (case-sensitive paths). Missing `.hath0r/` fails validation. `[CLI-Research §1.7]`

### AEG-REQ-UPL-002 — Scoped AGENTS.md chain
Each significant folder MAY carry an `AGENTS.md`; the CLI MUST resolve nearest-first when loading agent context. `[CLI-Research §1.7]`
**AC:** `hath0r repo agents list` prints the resolved chain for any path.

### AEG-REQ-UPL-003 — Makefile as thin façade
Any Makefile in a HATHOR project SHOULD invoke only stable `hath0r` CLI contracts. `bin/` MUST NOT contain a parallel control plane. `[CLI-Research §2.2, §5-E]`
**AC:** `hath0r repo validate --deep` warns when `bin/` contains executables not registered as CLI aliases.

### AEG-REQ-UPL-004 — Git-first
Every HATHOR project MUST be a Git repository. Non-git projects are outside v1 scope.

### AEG-REQ-UPL-005 — Migration from `.infraOS`
`hath0r repo init --from-infraos` MUST convert a legacy `.infraOS/` tree into `.hath0r/`, preserving runbooks, checklists, workflows, and rules; original tree retained until operator confirms.
**AC:** Post-migration `hath0r repo validate` passes; a diff report is produced for operator review.

---

## 8. Knowledge Plane Requirements (AEG-REQ-KNO)

Detailed spec: RP-004 (promotion) and BOT-KNO-001..006.

### AEG-REQ-KNO-001 — Tiered search order
Retrieval MUST traverse **Project → Machine → Organization → Public**; a project-tier hit short-circuits lower priorities unless breadth is explicitly requested. `[BOT-KNO-001]`

### AEG-REQ-KNO-002 — Tier backing stores
- **Project** = repo-local `.hath0r/knowledgebase/` + project MCP
- **Machine** = CLI knowledge + local vector server
- **Organization** = org MCP
- **Public** = last-resort external reference (`status=external`, never `verified`) `[BOT-KNO-002]`

### AEG-REQ-KNO-003 — Microburst writes only
Writes MUST be small, session-scoped, incremental microbursts. Bulk sync requires explicit operator authorization. `[BOT-KNO-003]`

### AEG-REQ-KNO-004 — Mandatory record metadata
Every record MUST carry: provenance, TTL/staleness, draft/verified status, hierarchy-tier link, retrieval-quality fields (title + breadcrumb prepended to each chunk). `[BOT-KNO-004]`

### AEG-REQ-KNO-005 — Retrieval honesty
Retrieval MUST return "no confident match" rather than a low-quality batch; expired TTL is flagged, never silently served. `[BOT-KNO-005]`

### AEG-REQ-KNO-006 — Secrets never in knowledge
Automated redaction / PII-secret scan MUST run on every microburst before commit. `[BOT-KNO-006, KPW-004]`

### AEG-REQ-KNO-007 — Status-on-record, queue-as-view
Review status lives solely on the record; queues are queries. No separate queue store may exist. `[AEG-KPW-001]`

### AEG-REQ-KNO-008 — Tiered reviewer authority
Project → project owner; Machine → machine operator; Organization → domain curator; Public → not promotable. `[AEG-KPW-002]`

### AEG-REQ-KNO-009 — Explicit human promotion
No auto-promotion, ever. Every `verified` record carries reviewer identity + timestamp; zero records verified by a bot identity. `[AEG-KPW-003]`

### AEG-REQ-KNO-010 — Supersede-or-reject on conflict
Promotion conflicting with an existing verified record requires an explicit supersede-or-reject decision; superseded records are archived with linkage. `[AEG-KPW-005]`

### AEG-REQ-KNO-011 — Dispute path
Any operator or a bot (with linked run evidence) MAY move a `verified` record to `disputed`; dispute requires reason + evidence link. `[AEG-KPW-006]`

### AEG-REQ-KNO-012 — Draft SLA + auto-archive
Draft age beyond SLA (14d project/machine, 30d org) degrades `status`; 2× SLA drafts auto-archive recoverably. `[AEG-KPW-007]`

---

## 9. Ticketing Plane Requirements (AEG-REQ-TKT)

Detailed spec: RP-006.

### AEG-REQ-TKT-001 — Source of truth for work
Work existence, state, linkage, estimation, and authorization MUST come from the Ticketing Plane. Chat and agent memory are inputs, not authority. `[AEG-TKT-001]`

### AEG-REQ-TKT-002 — Canonical Ticket Contract v1
All bots and agents interact with work through a provider-agnostic Ticket Contract; provider-native fields are confined to adapters. `[AEG-TKT-002]`

### AEG-REQ-TKT-003 — Brokered provider access only
Jira, Azure DevOps, GitHub, and the Backup TS are reached exclusively via Operator-Bot; no worker bot links a provider SDK or resolves/persists long-lived provider credentials. A declared RP-011 Class-2 flow may expose only a scoped, short-lived, memory-only token. `[AEG-TKT-003, SEC-002, AEG-OPB-002]`

### AEG-REQ-TKT-004 — No-Ticket Gate
Substantive work (implementation, refactor, config/rule change, commit, branch, PR) MUST be blocked until an authorizing ticket exists. Read-only Q&A, orientation, research are exempt. `[AEG-TKT-004]`

### AEG-REQ-TKT-005 — Epic-Linkage Gate
Every ticket MUST link to an epic; epic-less tickets cannot advance past `ready`. `[AEG-TKT-005]`

### AEG-REQ-TKT-006 — PR/branch binding
Every PR and branch MUST reference its ticket using canonical naming (`feature/<KEY>-<initials>-<slug>`). `[AEG-TKT-006]`

### AEG-REQ-TKT-007 — Estimation discipline
Tickets MUST store base and governance-reduced hours under a named policy (`jira-standards@50pct`); reduced > 40h triggers a split prompt. `[AEG-TKT-007]`
*(Decision 2026-09-13, resolves RP-006 Q4: the plane **records** both values and mechanically enforces presence + the >40h split; the reduction arithmetic itself is governance policy applied at authoring time — the plane never recomputes it.)*

### AEG-REQ-TKT-008 — Backup Ticketing System
The Backup TS MUST implement the same Ticket Contract v1 as any provider adapter. `[AEG-TKT-008]`

### AEG-REQ-TKT-009 — Degraded write with bounded reconciliation
Provider outage MUST NEVER block ticket capture; buffered work is `state=buffered`, run flagged `degraded: true` in the response envelope (bot-boundary exit 2 only — ADR-003 §2.3), bounded by trust TTL. `[AEG-TKT-009]`

### AEG-REQ-TKT-010 — Authority reconciliation
On reconnect, buffered work MUST reconcile to the authoritative provider. Provider wins as authority; conflicting delta replays as an update or surfaces `TICKET_RECONCILE_CONFLICT`. Never silently drop or overwrite. `[AEG-TKT-010]`

### AEG-REQ-TKT-011 — Deploy authority via ticket only
Promotion authority originates solely from a human-executed DVO deploy ticket. Agents author; humans execute. `[AEG-TKT-011, cr-deploy-gov-001]`

### AEG-REQ-TKT-012 — Ticket ↔ hierarchy/telemetry linkage
Every run MUST report its `ticket_ref` alongside its hierarchy chain and telemetry. `[AEG-TKT-012]`

### AEG-REQ-TKT-013 — Honest work-state reporting
`hath0r work status` MUST report authoritative vs buffered counts, epic-compliance, and reconcile health. `[AEG-TKT-013]`

---

## 10. Telemetry & Observability Requirements (AEG-REQ-TEL, AEG-REQ-OBS)

Detailed spec: RP-003 (transport) and BOT-OBS-001..002.

### AEG-REQ-TEL-001 — Spool-and-drain transport
Machine-tier telemetry MUST use CLI-mediated append to a local append-only spool, drained asynchronously by Observation-Bot. No broker daemon at machine tier in v1. `[AEG-TEL-001]`
**AC:** Emitting bot's critical path contains no network I/O and no Observation-Bot dependency.

### AEG-REQ-TEL-002 — Never fatal
Telemetry failure MUST NEVER fail or block business work; it degrades `status` instead. `[AEG-TEL-002]`

### AEG-REQ-TEL-003 — At-least-once with idempotent consumers
Delivery MUST be at-least-once; every consumer dedupes on `event_id` (UUIDv7). `[AEG-TEL-003]`

### AEG-REQ-TEL-004 — Envelope conformance (v1)
All events MUST conform to envelope v1 (§10.1). Undeclared events are quarantined to a dead-letter segment. `[AEG-TEL-004]`

### AEG-REQ-TEL-005 — Offline durability
Events MUST survive Observation-Bot / Tower outages within retention. Default retention 7 days or drained+age>24h. `[AEG-TEL-005]`

### AEG-REQ-TEL-006 — Bounded disk usage
Spool obeys quota with the warn (80%) / shed debug (90%) / hard stop (100%) ladder; business-outcome events shed last. `[AEG-TEL-006]`

### AEG-REQ-TEL-007 — Hierarchy traceability
Every event MUST carry the hierarchy chain reference so spool/Tower views correlate with the authoritative run ledger, evidence records, and provider receipts. Telemetry MUST support audit replay but is not the sole run-state source. `[AEG-TEL-007, AEG-GW-004, AEG-OPB-005/007]`

### AEG-REQ-OBS-001 — Uniform event schema
All bots emit the same telemetry event shapes; Observation children consume any bot's events with zero bot-specific adapters. `[BOT-OBS-001]`

### AEG-REQ-OBS-002 — Tower rollup
All observation data MUST roll up to the Control Tower for cross-project visibility. `[BOT-OBS-002]`

### 10.1 Event envelope v1 (normative)
```json
{
  "event_id": "01a0b6a4-…-uuidv7",
  "schema_version": "1.0.0",
  "event": "task.end",
  "occurred_at": "2026-09-11T11:58:00.123Z",
  "emitter": {
    "bot_uuid": "…",
    "name": "runbook-Bot",
    "family": "hierarchy",
    "manifest_digest": "sha256:…"
  },
  "run": {
    "run_id": "…",
    "binding_id": "…",
    "hierarchy_chain": "procedure:…/strategy:…/playbook:…/runbook:…/workflow:…/checklist:…",
    "ticket_ref": "AMD-1234",
    "project": "…",
    "machine": "…"
  },
  "severity": "info",
  "payload": { "outcome": "success", "duration_ms": 412, "tokens": { "in": 1200, "out": 300 }, "retries": 0 }
}
```

Core event vocabulary (extensible per manifest `telemetry.events_emitted`):
`task.start`, `task.end`, `retry`, `tokens`, `benchmark`, `contract.refused`, `registry.state_change`, `knowledge.microburst`, `knowledge.status_change`, `work.ticket.status_change`, `work.ticket.reconcile`, `degraded`.

Extended vocabularies: `validation.*` (RP-007 §8), `knowledge.retrieval` (RP-012 §4), and `orchestration.*` (TS-002 §11). The canonical event registry is **HATHOR-CANON-010 §3**.

---

## 11. Container & Deployment Requirements (AEG-REQ-CNT)

Detailed spec: containerization article.

### AEG-REQ-CNT-001 — Container taxonomy
Every container MUST belong to exactly one class:
- **Class A** — Control-Plane containers (CLI + Orchestration bots + MCP servers). Only Class A terminates agent traffic.
- **Class B** — Knowledge containers (VectorDB, embeddings, KB APIs). Stateful, backup-governed.
- **Class C** — Worker / Bot-Host containers. One micro-bot per container preferred; a family may share one image when it shares contract version and failure domain.
- **Class D** — Observation containers (OTel Collector, observation consumers). Sole holder of telemetry-backend credentials.

### AEG-REQ-CNT-002 — Container isomorphism to bot anatomy
Every HATHOR container MUST carry the seven anatomical blocks (Identity, Manifest, Contract, Executor, Knowledge interface, Connection interface, Telemetry surface) at the deployment layer.

### AEG-REQ-CNT-003 — Registry-first identity
Ports, names, groups MUST come from a canonical registry (`cfg/port-registry.yaml` at the project root — ADR-004 §2.1; org-central registries remain an organization-tier source the project file must not contradict) — never invented per repo.

### AEG-REQ-CNT-004 — Zero baked secrets
Containers MUST contain zero baked credentials. Runtime injection only (`hath0r secrets exec` locally; IRSA or EKS Pod Identity + secret mounts on EKS).

### AEG-REQ-CNT-005 — Contract endpoints
Every HTTP-serving container MUST expose `/version` (JSON + branded HTML via content negotiation) and `/health`. Both endpoints follow the canonical exit-code table.

### AEG-REQ-CNT-006 — Micro-linter Q-Gate
Nothing un-linted gets containerized. The build MUST run the canonical micro-linter set (canonical naming, port registry, line-ending, secrets-in-layer, CVS labels, observability contract) and fail the build on any violation.

### AEG-REQ-CNT-007 — Agent role boundary
Agents build and verify container images in local + development only. Promotion beyond development MUST go through the DVO deploy-ticket workflow (§9, AEG-TKT-011).

### AEG-REQ-CNT-008 — Broker symmetry
Worker containers persist zero provider credentials (Operator-Bot brokers; RP-011 Class-2 tokens are scoped, short-lived, and memory-only) AND zero telemetry-backend credentials (Collector brokers). Long-lived secrets stay behind the broker at both altitudes.

---

## 12. Infra Adoption Decision Log (per Canonical Rule 4)

Every InfraOS carry-over decision is logged. Adopt = brought into HATHOR unchanged in spirit; Adopt (shaped) = restated to fit HATHOR taxonomy; Reject = not carried forward.

| Source | Decision | Rationale | Landing requirement |
|---|---|---|---|
| Single-binary CLI entrypoint (AD-001, `infraos-os`) | **Adopt** | Already a HATHOR-class ambition; proven ergonomics. | AEG-REQ-PLAT-001 |
| 79-group flat command surface | **Reject** | Discovery + token cost too high; violates progressive disclosure. | AEG-REQ-PLAT-008 |
| Plugin registry + legacy `commands_*.py` (AD-002) | **Adopt (shaped)** | Registry pattern is sound; hybrid legacy path is not carried over. | Manifest v1 + MBI |
| Workflows executor (AD-003/004) | **Adopt (design)** | Proven execution semantics; re-implemented in the Go chassis per TS-D-001 — design adoption, not code reuse (the Python executor is not linked). | AEG-REQ-BOT-004 |
| Connections vs MCP split (AD-005) | **Adopt** | Matches 2026 hybrid guidance; explicit router story required. | Operator-Bot design |
| Orchestration lifecycle (ReAct, persisted state, AD-007) | **Adopt** | Feeds Process-Bot state machine. | AEG-REQ-BOT-003 |
| Quality/release gates + AGENTS contracts (AD-008) | **Adopt** | Feeds Proctor-Bot gate surface. | `hath0r proctor gate` |
| Product `.infraOS/` per-repo state | **Adopt (shaped) → `.hath0r/`** | Same idea, canonicalized layout + migration tool. | AEG-REQ-UPL-005 |
| Makefile + `bin/*` parallel tooling (Communications pattern) | **Reject** | Diluted "CLI as single contact"; Makefile must become a thin façade. | AEG-REQ-UPL-003 |
| CR-017 exit codes 0/1/2 (bot boundary) | **Adopt** | Proven minimal set for bot self-checks. | AEG-REQ-BOT-008 |
| CR-017 full 11-group `status` payload per bot | **Reject** | Too heavy for microbots; full check set at CLI/Tower level. | Per-bot slim `status` |
| cr-007 retry cap 5 with context | **Adopt** | Bounded, validated. | AEG-REQ-BOT-010 |
| cr-005 secrets-manager-first credential order | **Adopt (Operator-Bot only)** | Exceeds ad hoc env-file handling. | AEG-REQ-CNT-004 |
| cr-jira-ticket-001/002/003 (ticket economy, epic, PR bind) | **Adopt (native)** | Native to HATHOR ticketing plane. | AEG-REQ-TKT-004..006 |
| cr-deploy-gov-001 (dev-only writes, DVO deploy ticket) | **Adopt** | Deploy authority origin. | AEG-REQ-TKT-011 |
| `jira-standards.md` (hours, 50% reduction) | **Adopt** | Stored as `base_hours` + `reduced_hours` under named policy. | AEG-REQ-TKT-007 |
| cr-observability-001 (async export, never fail business) | **Adopt (doctrine)** | Feeds spool-and-drain doctrine. | AEG-REQ-TEL-002 |
| OTel Collector at machine tier | **Reject (v1 machine)** | Broker daemon overhead exceeds need; adopt at Tower ingestion tier. | RP-003 §6 |
| cr-cvs-001 Container Version Standard | **Adopt** | Provenance labels + `/version` contract. | AEG-REQ-CNT-005 |
| cr-docker-ports-001, cr-011 port registry | **Adopt** | Registry-first container identity. | AEG-REQ-CNT-003 |
| cr-aws-gov-001 EKS-only rule | **Adopt** | HATHOR containers deployed on EKS only in AWS environments. | Deployment doctrine |
| cr-kb-push-001 Development MCP push discipline | **Adopt (native)** | Aligns with microburst-only writes. | AEG-REQ-KNO-003 |
| `commands inventory` (~41k tokens, opt-in only) | **Adopt (shaped)** | Full unfiltered dump remains opt-in; default is filtered `schema --domain`. | AEG-REQ-PLAT-009 |
| KnowMCP / InfraMCP separation | **Adopt** | Two Class-A MCP servers as canonical reference. | Container catalog |
| InfraOS `cfg/mcp-servers.json` flat config | **Reject** | No per-command schema, signatures, negotiation. | Manifest v1 |
| Infra monolithic CLI-service model | **Reject** | Microbot + single control plane supersedes. | Chassis + manifest |
| InfraOS single-provider (Jira-only) assumption | **Reject** | Canonical Ticket Contract spans Jira + ADO + GitHub. | AEG-REQ-TKT-002 |

---

## 13. Security Requirements (AEG-REQ-SEC)

### AEG-REQ-SEC-001 — Credential resolution order
Operator-Bot resolves credentials: secrets manager → project env → credentials file. Non-secrets-manager paths are **degraded** (envelope `degraded:true`; bot-boundary exit 2 in `status --group connections` — ADR-003 §2.3). `[BOT-SEC-001]`

### AEG-REQ-SEC-002 — Connection exclusivity
Only Operator-Bot touches the Connection Pool; worker bots receive brokered sessions. `[BOT-SEC-002]`

### AEG-REQ-SEC-003 — Provenance verification before dispatch
Bots MUST be verifiable (identity + provenance) before Proctor routes work. Unregistered or provenance-mismatched bots yield `PROVENANCE_UNVERIFIED`, reported to Tower. `[BOT-SEC-003]`

### AEG-REQ-SEC-004 — Development-only writes by default
Agents have full mutation rights only in `development`. Testing/staging/production writes require explicit human grant via ticket. `[cr-deploy-gov-001]`

### AEG-REQ-SEC-005 — Automated secret/PII redaction
Every knowledge microburst, every ticket update, every telemetry event MUST pass a redaction scan before commit. `[BOT-KNO-006, AEG-KPW-004]`

### AEG-REQ-SEC-006 — Audit of intent, not just command text
Audit records MUST capture the caller's declared intent (capability) and hierarchy chain — not merely the shell string. `[CLI-Research §3.4]`

---

## 14. Governance Gates (mechanical enforcement)

> **Registry note (2026-09-13):** the canonical gate registry is **HATHOR-CANON-010 §2** — fifteen gates (G01–G15), adding the four validation gates (RP-007 §5.2) and the Sequence/Barrier Gate (RP-009 §4.2, per ADR-002) to the ten below. Canonical evaluation order on the dispatch path: Provenance → Contract → Sequence/Barrier → domain gates.
>
> **Trust model (`AEG-THR-001`):** these mechanical guarantees hold against a *cooperative-but-fallible* agent; a fully adversarial local process is out of scope for v1 enforcement and in scope for detection + phased hardening (RP-013 §2/§4).

These are the moments the CLI actively blocks work. All produce structured refusals with remediation.

| Gate | Refuses when | Bot | Exit |
|---|---|---|---|
| **No-Ticket Gate** | Substantive mutation without a resolvable ticket | Proctor | 7 → 2 after prompt |
| **Epic-Linkage Gate** | Ticket has no epic | Proctor | 2 *(was 5; ADR-003 §2.3)* |
| **PR-Ticket Bind Gate** | Branch/PR does not reference ticket | Proctor | 2 |
| **Estimation Gate** | Ticket missing `base_hours` / `reduced_hours` or reduced > 40h | Proctor | 2 |
| **Provenance Gate** | Bot unregistered / signature invalid | Proctor | 4 |
| **Contract Gate** | Args/output fail JSON Schema | Proctor | 2 |
| **Development-Only Gate** | Mutating command targets non-development env | Proctor | 4 |
| **Deploy-Ticket Gate** | Promotion attempted without human-executed DVO ticket | Proctor | 4 |
| **Micro-Linter Gate** | Image build with any linter violation | Build | 2 |
| **Knowledge Promotion Gate** | Draft fails mechanical checks (secrets, TTL, breadcrumb) | Knowledge | 2 |

---

## 15. Non-Functional Requirements (AEG-REQ-NFR)

### AEG-REQ-NFR-001 — Cold command latency
Cheap commands (`hath0r version`, `hath0r health`, per-bot `health`) MUST complete in < 250 ms wall clock in steady state. `[BOT-CMD-010]`

### AEG-REQ-NFR-002 — Agent-orientation token budget
The default orientation pack (`hath0r version`, `hath0r proctor preflight agent`, `hath0r process orient`, `hath0r operator connections list`, `hath0r operator mcp-servers list`, `hath0r process workflow list`) MUST fit in ≤ 2500 output tokens. `[Report 05 §7]`

### AEG-REQ-NFR-003 — Schema payload budget
`hath0r schema --domain <x>` default page MUST be ≤ 8 KB. `[Spike 04 §3.4]`

### AEG-REQ-NFR-004 — Chain resolution latency
Full six-tier hierarchy chain resolution MUST complete in ≤ 3 CLI round-trip waves via fan-out. `[AEG-HIE-004]`

### AEG-REQ-NFR-005 — Availability of degraded modes
Telemetry, ticketing, and knowledge planes MUST all continue in degraded mode when their authority is unreachable, up to trust TTL.

### AEG-REQ-NFR-006 — CLI Spec score
Post-v1, the top-30 command set MUST score ≥ 12/16 on the CLI Spec rubric (report 02).

### AEG-REQ-NFR-007 — v1 platform support
HATHOR v1 MUST support macOS and Linux (darwin/linux, arm64+amd64); Windows is out of scope for v1 (ADR-004 §2.4). POSIX facilities (`flock`, TTY semantics, XDG paths) MAY be relied on without shims.

---

## 16. Validation Criteria (v1 acceptance)

An HATHOR v1 release is accepted when *all* of the following pass:

1. **Command tree** — Root help renders one screen with ≤ 9 domains + meta (ADR-003 §2.2).
2. **Contract** — Every top-30 command declares `effects`, `output_kind`, `cardinality`; every declared command has embedded `args_schema` + `output_schema`; every exit code appears in the canonical table.
3. **Bots** — Six hierarchy bots + three orchestration bots + Observation-Bot family are registered, signed, and pass `selftest`.
4. **Handshake** — HELLO/OFFER/BIND/VERIFY works end-to-end; fast-path digest comparison is measurable in traces.
5. **Registry** — MBI/TBR reconciliation works; CRL revokes within one reconciliation cycle; `verified-local` expires at TTL.
6. **Telemetry** — Spool-and-drain survives a 24 h Observation-Bot outage with zero event loss (given quota headroom); replay produces zero double-counting.
7. **Knowledge** — Draft-to-verified queue-as-view works; secrets/PII gate blocks promotion of tainted records; SLA degradation surfaces in `status`.
8. **Ticketing** — Canonical Ticket Contract v1 round-trips through Jira, Azure DevOps, GitHub, and Backup TS adapters; No-Ticket / Epic / PR-Bind gates refuse cleanly; buffered→reconciled works with authority-wins conflict resolution.
9. **DVO deploy** — `hath0r process runbook run dvo-deploy-ticket --dry-run` produces a JSON plan with no side effects; live run refuses without `--yes` and human authority.
10. **Universal layout** — `hath0r repo init --from-infraos` migrates a reference InfraOS product cleanly; `hath0r repo validate` returns 0.
11. **Containers** — Reference Class A/B/C/D containers build, pass micro-linter gate, expose `/version` + `/health`, run with zero baked secrets.
12. **Governance** — Fifteen mechanical gates (HATHOR-CANON-010 §2) all refuse in negative-path tests and pass in positive-path tests.
13. **NFR** — Cold command < 250 ms; orientation pack ≤ 2500 tokens; schema page ≤ 8 KB; CLI Spec score ≥ 12/16.

---

## 17. Platform decisions and open questions

Research-paper questions are tracked in their owning papers. Resolved platform decisions are retained here for traceability; unresolved items remain explicitly open:

1. **CLI binary name — resolved.** `hath0r` is the greenfield binary of record (ADR-003 §2.1).
2. **Language for the chassis.** ~~Rust vs Go vs Python~~ **Resolved by TS-001 TS-D-001 (2026-09-11): Go 1.23+ for chassis/CLI/native linters; Python remains a valid reference-bot language for PLAT-002 two-language conformance.**
3. **Tower service surface v1 — resolved.** One small REST service with five facets plus offline-verifiable signed artifacts; browser UI remains v2 (accepted RP-010).
4. **CLI daemon.** Long-lived local daemon (Unix socket) for MCP fan-out + connection cache — is it v1 (measured need) or v2 (opt-in)?
5. **Cross-project MBI scope.** Machine-level vs project-workspace-level when multiple HATHOR projects coexist on one host. `[RP-002 Q2]`
6. **Backup TS implementation choice — resolved.** Build the minimal greenfield `hath0r-backup-ts` (accepted ADR-005).
7. **Signing stack — resolved at architecture level.** RFC 8785 JCS canonicalization, Ed25519 DSSE envelopes, and TUF distribution/rotation/revocation are accepted (RP-013 §6); concrete operational key cadences remain an implementation policy.
8. **AWS deployment target parity.** EKS-only per InfraOS carry-over — confirm for HATHOR v1 or allow ECS-Fargate as an alternative Class-A hosting model.
9. **Governance four-eyes.** Whether DVO deploy tickets and org-tier knowledge promotions require two human approvers. `[RP-004 Q4, RP-006 Q7]`

---

## 18. Traceability Matrix (research corpus → requirements)

| Source doc | Requirements folded in |
|---|---|
| HATHOR-REQ-BOT-001 (bot taxonomy) | §5, §8, §10, §13 |
| HATHOR-RP-001 (manifest schema + handshake) | §6, §14 (Contract, Provenance gates) |
| HATHOR-RP-002 (registry & discovery) | §6, §13 (SEC-003), §15 (offline trust) |
| HATHOR-RP-003 (telemetry transport) | §10 |
| HATHOR-RP-004 (knowledge promotion) | §8, §14 (Knowledge Promotion Gate) |
| HATHOR-RP-005 (hierarchy topology) | §5 (six identities, chassis) |
| HATHOR-RP-006 (ticketing plane) | §9, §14 (No-Ticket / Epic / PR-Bind / Deploy gates) |
| HATHOR-ADR-001 (target command tree) | §4, §12 (InfraOS aliasing) |
| Containerization article | §11 |
| CLI Research Report + Scoring + Payload baseline | §4, §15 (NFR) |
| InfraOS AGENTS / rules | §12 (adoption log) |

---

*Draft v0 — research-informed platform requirements for the greenfield HATHOR core. No implementation authorized by this document. Review and amend before promotion to `verified`.*
