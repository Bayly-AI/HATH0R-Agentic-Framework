---
id: HATHOR-RP-004
title: AEGIS Research Paper 004 — Draft→Verified Knowledge Promotion Workflow
summary: 'Every knowledge write lands as `draft`; only human review promotes to `verified` (KNO-004). Undefined: **who reviews**, **where the queue lives**, and the full status lifecycle including demotion and expiry. The board...'
doc_type: RP
diataxis: explanation
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
# AEGIS Research Paper 004 — Draft→Verified Knowledge Promotion Workflow

- **Document ID:** HATHOR-RP-004
- **Status:** DRAFT (research output — pending operator review)
- **Date:** 2026-09-11
- **Parent:** HATHOR-REQ-BOT-001 (§10 Q4)
- **Related:** HATHOR-RP-003 (promotion/demotion telemetry events)
- **Author:** Oz (Agent), commissioned by Raymond Bayly

---

## 1. Problem Statement

Every knowledge write lands as `draft`; only human review promotes to `verified` (KNO-004). Undefined: **who reviews**, **where the queue lives**, and the full status lifecycle including demotion and expiry. The boards establish: human review happens "from part of the CLI" against articles behind a lightweight editor; knowledge priority ordering favors provenance and correctness over recency; retrieval must be honest about status.

## 2. Design Positions

### 2.1 The queue is a view, not a store

Rejected: a separate queue database that duplicates knowledge records (drift risk, second source of truth). **Recommended:** status lives **on the record** (KNO-004 metadata); the "review queue" is a query over records where `status=draft`, scoped by tier and project. The Tower indexes drafts org-wide; the CLI surfaces the queue locally:

- `aegis knowledge review` — interactive queue for the operator (lightweight editor per the boards).
- `aegis knowledge review --list --json` — machine-readable queue for reporting.

One store, one status field, many views. No queue/record reconciliation problem can exist.

### 2.2 Reviewer roles by tier

Review authority follows the knowledge tier (KNO-001/002), narrowest competent audience first:

- **Project tier** → the project owner (or a project-designated curator). They have the context; drafts here never wait on org-level staff.
- **Machine tier** → the machine's operator. Machine-tier knowledge (tool paths, local capabilities) is personal-scope; the operator self-reviews, but promotion still requires the explicit act — no auto-verify.
- **Organization tier** → a named **domain curator** per knowledge domain (registry of curators held by the Tower). Org-tier promotion is the strictest gate because blast radius is org-wide.
- **Public tier** → not promotable by AEGIS; external material is ingested as reference with `status=external`, never `verified`.

Escalation: a project curator MAY nominate a project-tier `verified` record for org-tier promotion; that nomination re-enters the org queue as `draft` at org scope (promotion never leaks across tiers implicitly).

### 2.3 Status lifecycle

```
            ┌────────── nominate up-tier ──────────┐
            ▼                                      │
draft ──review──▶ verified ──dispute──▶ disputed ──┤
  │                  │                     │       │
  │ expire/reject    │ TTL lapse           │ re-review
  ▼                  ▼                     ▼
archived         stale (flagged)    verified | draft | archived
```

- **draft** — retrievable only when the caller explicitly opts in (`--include-drafts`); never served by default retrieval (KNO-005 honesty).
- **verified** — default-retrievable within TTL.
- **stale** — verified past TTL; served only with an explicit per-record staleness flag; appears automatically in the review queue for re-verification.
- **disputed** — any operator or bot (via evidence, e.g. a failed run traced to the record) can dispute; record drops out of default retrieval until re-reviewed. Dispute requires a reason and links the evidence (telemetry `run_id` where applicable).
- **archived** — terminal; retained for provenance, excluded from retrieval.

### 2.4 Promotion criteria (the reviewer's gate checklist)

A reviewer MUST be shown, and the CLI MUST verify mechanically where possible:
1. Provenance complete (author bot/agent, session, source run).
2. Secrets/PII scan passed (KNO-006 — mechanical, blocking).
3. TTL set and appropriate to content class.
4. Hierarchy-tier link present and plausible.
5. Retrieval-quality fields present (title, breadcrumb) — mechanical.
6. No conflict with an existing `verified` record — if conflict, reviewer chooses **supersede** (old record → archived, linked as superseded-by) or **reject**. Two contradictory verified records may never coexist in one scope.
7. Optional supporting signal: usage evidence (retrieval hit count while draft, successful runs referencing it) surfaced from Observation data.

Items 2, 3, 5 are hard mechanical gates (the CLI refuses promotion); 1, 4, 6, 7 are reviewer judgment with mechanical assistance.

### 2.5 Queue hygiene (no rotting drafts)

- Draft age SLA: drafts older than a threshold (proposed 14 days project/machine, 30 days org) are flagged in `status --group knowledge` as degraded — unreviewed knowledge is a system smell, not background noise.
- Auto-archive: drafts untouched past 2× SLA are archived with reason `expired-unreviewed` (recoverable — archive is not deletion).
- Every transition emits a `knowledge.status_change` telemetry event (extends HATHOR-RP-003 vocabulary) so promotion throughput and queue depth are Tower-visible metrics.

## 3. Requirements (AEG-KPW)

### AEG-KPW-001 — Status-on-record; queue-as-view
Review state lives solely in the record's status field; queues are queries, never separate stores.
**AC:** No component persists queue entries apart from the records; deleting the "queue" is impossible as a distinct operation.

### AEG-KPW-002 — Tiered reviewer authority
Promotion rights: project tier → project owner/curator; machine tier → machine operator; org tier → registered domain curator; public tier → never promotable.
**AC:** The CLI refuses promotion attempts by identities outside the tier's authority; curator registry is Tower-held and auditable.

### AEG-KPW-003 — Explicit human act
No auto-promotion under any circumstance, including machine tier and high usage evidence.
**AC:** Every `verified` record carries reviewer identity + timestamp; zero records verified by a bot identity.

### AEG-KPW-004 — Mechanical gates
Secrets/PII scan, TTL presence, and retrieval-quality fields are CLI-enforced blockers on promotion.
**AC:** A record failing any mechanical gate cannot be promoted regardless of reviewer intent.

### AEG-KPW-005 — Conflict resolution by supersession
Promoting a record that conflicts with an existing verified record requires an explicit supersede-or-reject decision; superseded records are archived with linkage.
**AC:** For any scope and topic key, at most one verified record exists; supersession chains are traversable.

### AEG-KPW-006 — Dispute path
Any operator, or a bot with linked run evidence, can move a verified record to `disputed`, removing it from default retrieval pending re-review.
**AC:** Dispute requires reason + evidence link; re-review outcomes are limited to verified/draft/archived.

### AEG-KPW-007 — Draft SLA and auto-archive
Draft age beyond SLA degrades `status`; beyond 2× SLA drafts auto-archive recoverably.
**AC:** Queue depth and age are derived from the authoritative record index; deduplicated telemetry exports transition/latency metrics to Tower without becoming the status authority.

### AEG-KPW-008 — Honest retrieval by status
Default retrieval serves only in-TTL `verified`; drafts require explicit opt-in; stale requires per-record flags; disputed/archived are excluded.
**AC:** Retrieval responses expose record status verbatim; no path serves a draft without the caller's opt-in recorded.

## 4. Infra Adoption Decision Log

- **Infra session-only/incremental knowledge push discipline (cr-009/cr-kb-push-001) — Adopt the principle** (session-scoped microbursts are already canonical via KNO-003); the *destination-environment* rules are Infra-specific and not carried over.
- **Infra "draft/verified" concept from the Overview board — native AEGIS**, not an Infra import; noted for completeness.
- **Jira-style workflow engine for the queue — Reject.** External ticketing for knowledge review adds a second store and breaks queue-as-view; the CLI editor flow the boards describe exceeds it for this purpose.

## 5. Open Questions

1. Curator registry shape: per-domain list vs capability-style grants (`knowledge.promote.org.<domain>@1`) — the latter would reuse the manifest/capability vocabulary (HATHOR-RP-001).
2. Should dispute by bots be rate-limited to prevent evidence-spam from a misbehaving bot? (Interaction with retry-Bot data.)
3. TTL defaults per content class (procedure vs workflow vs checklist knowledge age very differently).
4. Whether org-tier promotion should require two curators (four-eyes) for governance-class records.

---

*Research output only. No implementation authorized.*
