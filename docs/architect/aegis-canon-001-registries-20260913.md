---
id: AEGIS-CANON-001
title: AEGIS-CANON-001 — Canonical Registries
summary: Per-paper lists drifted (CORE said ten gates; RP-007 added four; RP-009 added "the 11th"; RP-003's event list lagged CORE's). This document replaces scattered enumerations with one registry per concept. Where a source...
doc_type: CANON
diataxis: reference
audience: [architect, agent]
tags: []
version: 1.0.0
status: accepted
created: '2026-09-13'
updated: '2026-09-15'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: 365d, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# AEGIS-CANON-001 — Canonical Registries
## Gates · Telemetry Events · Refusal Codes · Micro-Linters · Bot Roster · Naming Conventions

- **Document ID:** AEGIS-CANON-001
- **Status:** ACCEPTED — operator sign-off 2026-09-13 (PENDING-EDITS D4); amended 2026-09-15 by D12. This document is the **single source of enumeration** for everything it lists
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Consolidates:** CORE-001 §14 (gates) + §10.1 (events); RP-001 §3.6, RP-003 §3.3, RP-006 §6, TS-001 §3.2/§10.4, TS-002 §3.1 (refusal codes); RP-007 §4.1 + RP-009 §6.4 + CANON-003 §10 (linters); RP-008 §4 + RP-009 §7.4 (roster); RP-012 §4 (`knowledge.retrieval`); CANON-003 §4/§5/§13 (document types, IDs, documentation requirements)
- **Maintenance rule:** any paper that adds a gate, event, refusal code, linter, bot, document type, or requirement prefix MUST amend this document in the same change. Definitions/semantics live in the source papers; **membership and identity live here**. Drift between a paper and this registry is a defect in the paper.
- **Scope rule:** registry document. No implementation authorized.

---

## 1. Purpose & precedence

Per-paper lists drifted (CORE said ten gates; RP-007 added four; RP-009 added "the 11th"; RP-003's event list lagged CORE's). This document replaces scattered enumerations with one registry per concept. Where a source paper's list disagrees with this registry, **this registry wins** and the paper owes an amendment (tracked in `PENDING-EDITS.md`).

---

## 2. Gate Registry (15 mechanical gates)

Exit codes are CLI-boundary codes per CORE §4.5 as amended by ADR-003 §2.3.

| # | Gate | Trigger point | Refuses when | Owner | Exit | Source |
|---|---|---|---|---|---|---|
| G01 | **Provenance Gate** | every dispatch | bot unregistered / signature invalid / quarantined | Proctor | 4 | CORE §14, RP-001/002 |
| G02 | **Contract Gate** | every dispatch | args/output fail JSON Schema; contract mismatch | Proctor | 2 | CORE §14, RP-001 |
| G03 | **Sequence/Barrier Gate** | every dispatch + state transition | predecessors incomplete; phase barrier open; work unbound to an admissible node | Proctor | 2 | RP-009 §4.2, TS-002 §7 |
| G04 | **No-Ticket Gate** | substantive mutation | no resolvable authorizing ticket | Proctor | 7 → 2 after prompt | CORE §14, RP-006 §7.1 |
| G05 | **Epic-Linkage Gate** | ticket advancement past `ready` | ticket has no epic | Proctor | 2 *(was 5; corrected by ADR-003 §2.3)* | CORE §14, RP-006 §7.2 |
| G06 | **PR-Ticket Bind Gate** | branch/PR operations | branch/PR does not reference its ticket | Proctor | 2 | CORE §14, RP-006 §7.3 |
| G07 | **Estimation Gate** | ticket → `in_progress` | missing `base_hours`/`reduced_hours`; reduced > 40h unsplit | Proctor | 2 | CORE §14, RP-006 §7.4 |
| G08 | **Development-Only Gate** | mutating command | target env is not `development` without human grant | Proctor | 4 | CORE §14, SEC-004 |
| G09 | **Deploy-Ticket Gate** | promotion | no human-executed, reconciled DVO deploy ticket | Proctor | 4 | CORE §14, RP-006 §7.5 |
| G10 | **Change-Validation Gate** | change validation (stage/commit/façade) | blocking findings on scoped diff | Proctor (validation) | 2 | RP-007 §5.2, TS-001 §11.1 |
| G11 | **Assumption Gate** | action depending on an assumption | assumption `open/broken/expired` | Proctor (validation) | 2 | RP-007 §5.2, TS-001 §11.1 |
| G12 | **Claim-Evidence Gate** | claim assertion | claim lacks required suite tier or evidence digests | Proctor (validation) | 2 | RP-007 §5.2, TS-001 §11.1 |
| G13 | **Undeclared-Assumption Gate** *(strict profile)* | failure classification | failure matches a known class never declared | Proctor (validation) | 2 | RP-007 §5.2, TS-001 §11.3 |
| G14 | **Micro-Linter Gate** | image build | any blocking linter violation | Build | 2 | CORE §14, CNT-006 |
| G15 | **Knowledge Promotion Gate** | knowledge promote | draft fails mechanical checks (secrets, TTL, breadcrumb) | Knowledge | 2 | CORE §14, RP-004 §2.4 |

**Canonical evaluation order (dispatch path):** G01 → G02 → G03 → applicable domain gates (G04–G09). Validation gates (G10–G13) fire at their validation triggers (RP-007 §3.1); G14 at build; G15 at promotion. This order is normative and supersedes the illustrative sequence in ARCH-001 §15 (No-Ticket-first) — *is the caller legitimate → is the action lawful now → is the domain precondition met*.

---

## 3. Telemetry Event Registry

Envelope: CORE §10.1 (event envelope v1). `event_id` = UUIDv7; delivery at-least-once; consumers dedupe (`AEG-TEL-003`).

### 3.1 Core vocabulary (CORE §10.1)
`task.start` · `task.end` · `retry` · `tokens` · `benchmark` · `contract.refused` · `registry.state_change` · `knowledge.microburst` · `knowledge.status_change` · `work.ticket.status_change` · `work.ticket.reconcile` · `degraded`

### 3.2 Validation vocabulary (RP-007 §8)
`validation.finding` · `validation.suite.start` · `validation.suite.end` · `validation.assumption.status_change` · `validation.claim.asserted` · `validation.waive`

### 3.3 Knowledge vocabulary (RP-012 §4)
`knowledge.retrieval`

### 3.4 Orchestration vocabulary (TS-002 §11)
`orchestration.run.opened` · `orchestration.node.status_change` · `orchestration.gateway.branch` · `orchestration.barrier.refused` · `orchestration.reconcile` · `orchestration.waiver`
### 3.5 Run-log event types (TS-002 §5.1 — run ledger, not spool)
`run.opened` · `node.entered` · `node.suite.started` · `node.suite.ended` · `node.evidence.recorded` · `node.completed` · `node.blocked` · `node.skipped` · `gateway.branch.selected` · `gateway.event.received` · `run.reconcile.started` · `run.reconcile.passed` · `run.reconcile.failed` · `run.finalized` · `waiver.recorded`

Run-log events live in `.aegis/state/runs/<run_id>/events.jsonl` and are *mirrored* to the spool as `orchestration.*` events; they are two views of one fact, deduped on `event_id`.

---

## 4. Refusal-Code Registry

All refusals use the standard envelope `{code, message, remediation, provenance, ttl}` (CORE `AEG-REQ-PLAT-004`).

| Code | Meaning | CLI exit | Source |
|---|---|---|---|
| `CONTRACT_NO_OVERLAP` | no common contract version; envelope carries both ranges | 2 | RP-001 §3.6 |
| `CONTRACT_MAJOR_MISMATCH` | contract major versions differ | 2 | RP-001 §3.6 |
| `CONTRACT_OUTPUT_INVALID` | bot output fails declared schema | 1 | RP-001 §2.4 |
| `MANIFEST_DIGEST_STALE` | binding refers to superseded manifest; re-HELLO | 2 | RP-001 §3.6 |
| `PROVENANCE_UNVERIFIED` | signature/registry check failed; reported to Tower | 4 | RP-001 §3.6, RP-002 |
| `CAPABILITY_UNKNOWN` | no registered bot offers the requested intent; unresolved optional dependencies may make `status` degraded, but attempted dispatch still refuses | 3 | RP-001 §3.6, RP-014 §3.2 |
| `TICKET_RECONCILE_CONFLICT` | buffered delta cannot replay cleanly; operator decision required | 2 | RP-006 §6 |
| `TELEMETRY_SPOOL_FULL` | spool quota hard stop (degraded status, never fatal to business path) | — (status) | RP-003 §3.3 |
| `CLAIM_TIER_INSUFFICIENT` | claim asserted below required suite tier | 2 | RP-007 §3.2, TS-001 §10.4 |
| `SEQUENCE_VIOLATION` | action not lawful in current run state | 2 | TS-002 §3.1 |
| `BARRIER_NOT_MET` | predecessors/phase barrier incomplete; lists `next_required` | 2 | TS-002 §3.1 |
| `CHANGE_VALIDATION` | blocking findings on scoped diff at admission | 2 | TS-002 §3.1 |
| `EVIDENCE_MISSING` | required evidence class absent/stale | 2 | TS-002 §3.1 |
| `ASSUMPTION_BROKEN` | bound assumption broken/expired | 2 | TS-002 §3.1 |
| `COMPLETENESS_GAP` | finalize reconciler found missing mandatory units | 2 | TS-002 §3.1 |
| `GRAPH_INVALID` | process graph fails `ml-graph-integrity` or provenance | 2 (3 if unknown ref) | TS-002 §3.1 |
| `WAIVER_FORBIDDEN` | agent attempted human-only waiver | 4 | TS-002 §3.1 |
| `BOT_RULE_REFUSED` | bot-local pre-rule refused the action (envelope carries `rule_id`) | 2 | RP-014 §3.4 |

New codes require a row here plus a definition in their owning paper. Post-rule violations reuse `CONTRACT_OUTPUT_INVALID` (exit 1) with `rule_id` in `error.details` (RP-014 §3.4).

---

## 5. Micro-Linter Catalog (v1 — 26 native linters)

Semantics: RP-007 §4 (anatomy, purity, exit `0|2`) and CANON-003 §10 (documentation checks; staleness/Diátaxis warn-only). Always-on structural set:

`ml-upl-layout` · `ml-agents-chain` · `ml-manifest-schema` · `ml-manifest-digest` · `ml-exit-codes` · `ml-no-listener` · `ml-secrets-diff` · `ml-secrets-layer` · `ml-port-registry` · `ml-cvs-labels` · `ml-otel-contract` · `ml-line-endings` · `ml-path-case` · `ml-ticket-bind` · `ml-hierarchy-link` · `ml-knowledge-meta` · `ml-microburst-size` · `ml-broker-symmetry` · `ml-langpack-present` · `ml-graph-integrity` *(RP-009 §6.4)* · `ml-doc-frontmatter` · `ml-doc-id-unique` · `ml-doc-links` · `ml-doc-index` · `ml-doc-staleness` *(warn-only)* · `ml-doc-diataxis` *(warn-only)* *(CANON-003 §10)*

Language/product linters are project-registered packs (`.aegis/rules/linters.yaml`, RP-007 §4.2) and are not enumerated here; org-distributed packs MUST be signed (RP-013).

---

## 6. Canonical Bot Roster (26)

| Roster group | Members | Count |
|---|---|---|
| Orchestration (fixed, `AEG-REQ-BOT-003`) | `proctor-Bot`, `process-Bot`, `operator-Bot` | 3 |
| Orchestration / Validation role (Proctor-owned, `role=validator`, RP-007 §5 + RP-009 §7.4) | `val-diff-Bot`, `val-contract-Bot`, `val-assumption-Bot`, `val-registry-Bot`, `val-ticket-Bot`, `val-hierarchy-Bot`, `val-knowledge-Bot`, `val-claim-Bot`, `val-drift-Bot`, `val-evidence-Bot`, `val-completeness-Bot` | 11 |
| Information Hierarchy (fixed, `AEG-BOT-TAX-004`) | `procedure-Bot`, `strategy-Bot`, `playbook-Bot`, `runbook-Bot`, `workflow-Bot`, `checklist-Bot` | 6 |
| Observation (fixed, `AEG-BOT-TAX-005`) | `observation-Bot`, `task-Bot`, `benchmark-Bot`, `success-rate-Bot`, `retry-Bot`, `token-Bot` | 6 |

The Control Tower is **not a bot** (`AEG-REQ-BOT-006`). Operator connection adapters (Atlassian/GitHub/AWS/Azure/Firebase, RP-008 §5) are pool entries, **never** roster members (`AEG-MBL-003`). Roster expansion requires an ADR (`AEG-MBL-002`); the open Cleaner/maintenance candidate (RP-008 §7 Q1) remains undecided.

---

## 7. Naming & ID conventions

1. **`AEGIS-` prefix = document; `AEG-` prefix = requirement.** `AEGIS-REQ-BOT-001` is a *document*; `AEG-REQ-BOT-001` is a *requirement in CORE-001*. This near-collision is grandfathered for existing docs; **new documents** use `AEGIS-<TYPE>-<NNN>` with `TYPE ∈ {ADR, RP, TS, PLAN, REQ, ARCH, CANON, GUIDE, REPORT, SESSION}` and MUST NOT mint a document ID whose body matches an existing requirement prefix.
2. **File naming (new docs):** `aegis-<type>-<nnn>-<slug>-<yyyymmdd>.md`, lowercase. Existing files keep their names; INDEX.md carries the Doc-ID column for lookup.
3. **Bot naming:** family bots are `<role>-Bot` with lowercase role in machine contexts (`runbook-Bot`, manifest `name`) — prose may capitalize the role (`Runbook-Bot`); the manifest form is authoritative. Observation children and validators are always lowercase-rooted (`task-Bot`, `val-diff-Bot`). Validators always carry the `val-` prefix where a plane-facing capability shares the root name (`AEG-MBL-006`).
4. **Capabilities:** `<domain>.<noun>.<verb>@<major>` (RP-001 §2.5). **Events:** dot-namespaced lowercase (§3). **Refusal codes:** SCREAMING_SNAKE (§4). **Linters:** `ml-<class-slug>` (§5).
5. **Documentation metadata:** the `hathor-doc@1` YAML block in CANON-003 §3 is canonical for new and migrated authored documents. Existing bulleted `Status` / `Supersedes` / `Superseded by` / `Amended by` headers are grandfathered until migration; superseded *sections* carry an inline banner at the section head.

---

## 8. Requirement-prefix index

| Prefix | Domain | Defining document |
|---|---|---|
| `AEG-REQ-PLAT/CLI/BOT/MAN/REG/UPL/KNO/TKT/TEL/OBS/CNT/SEC/NFR-###` | platform requirements | AEGIS-REQ-CORE-001 |
| `AEG-BOT-TAX/ANA/RUN/KNO/CMD/SEC/OBS-###` | bot taxonomy/anatomy | AEGIS-REQ-BOT-001 |
| `AEG-MAN-###` | manifest + handshake | AEGIS-RP-001 |
| `AEG-REG-###` | registry & discovery | AEGIS-RP-002 |
| `AEG-TEL-###` | telemetry transport | AEGIS-RP-003 |
| `AEG-KPW-###` | knowledge promotion | AEGIS-RP-004 |
| `AEG-HIE-###` | hierarchy topology | AEGIS-RP-005 |
| `AEG-TKT-###` | ticketing plane | AEGIS-RP-006 |
| `AEG-VAL-###` | continuous validation | AEGIS-RP-007 |
| `AEG-MBL-###` | micro-bot launch | AEGIS-RP-008 |
| `AEG-GW-###` | orchestration gateway | AEGIS-RP-009 |
| `AEG-TWR-###` | tower surface | AEGIS-RP-010 |
| `AEG-OPB-###` | operator brokering | AEGIS-RP-011 |
| `AEG-KST-###` | knowledge storage/retrieval | AEGIS-RP-012 |
| `AEG-THR-###` | threat model & trust | AEGIS-RP-013 |
| `AEG-BOT-GOV/MEM/LIF-###` | bot-unit governance / memory / lifecycle | AEGIS-RP-014 |
| `AEG-DOC-###` | HATHOR documentation framework | AEGIS-CANON-003 |
| `TS-D/C/I-###` | CVS implementation ids | AEGIS-TS-001 |
| `TS2-D/C/I-###` | gateway implementation ids | AEGIS-TS-002 |
| `TS3-D/C/I-###` | bot-unit implementation ids | AEGIS-TS-003 |

---

*Registry document — ACCEPTED 2026-09-13 (D4), amended 2026-09-14 for the accepted RP-012 retrieval event and 2026-09-15 by D12 for `GUIDE`/`REPORT`/`SESSION`, `AEG-DOC-###`, and six `ml-doc-*` linters. Definitions live in the source papers; membership lives here. Amend in the same change as any addition.*
