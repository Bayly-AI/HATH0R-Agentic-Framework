---
id: HATHOR-CANON-011
title: HATHOR-CANON-011 — HATHOR Platform Principles
summary: RFC 2119 keywords appear only inside quoted source requirements.
doc_type: CANON
diataxis: reference
audience: [architect, agent]
tags: []
version: 0.1.0
status: proposed
created: '2026-09-14'
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
# HATHOR-CANON-011 — HATHOR Platform Principles
## The Platform-Altitude Principle Set (`hathor-principles@1`) and Its Relationship to the Bot-Carried Set (`aegis-principles@1`)

- **Document ID:** HATHOR-CANON-011
- **Status:** PROPOSED — awaiting operator ratification (PENDING-EDITS §6, D10)
- **Date:** 2026-09-14
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Derived from:** HATHOR-ARCH-002 §1 (executive summary); HATHOR-REQ-CORE-001 §0.3 (canonical rules); HATHOR-RP-014 §3.5.1 (`aegis-principles@1`, P01–P12); HATHOR-REQ-BOT-001; HATHOR-RP-007/009/011/013; HATHOR-ADR-002/003
- **Companion to:** HATHOR-CANON-010 (registries); HATHOR-ARCH-002 (bot unit compendium)
- **Maintenance rule:** if ratified, this document becomes the single enumeration of platform-altitude principles. A principle is added, reworded, or retired only by operator sign-off recorded in `PENDING-EDITS.md`, and every accepted change bumps the set version (`hathor-principles@<n>`).
- **Scope rule:** proposed doctrine restatement only. The principles below are intended to restate accepted decisions and cite them, but the set itself is not canon until D10 is signed off. No implementation is authorized by this document.

RFC 2119 keywords appear only inside quoted source requirements.

---

## 0. Purpose

### 0.1 Why a second principle set exists
RP-014 §3.5.1 ratified twelve principles (`aegis-principles@1`, P01–P12) that **every bot carries** in its signed bundle and cites in `report.decisions[]`. That set is deliberately compressed to what a bot needs at invocation time. Stakeholders, architects, and reviewers need the same canon at **platform altitude** — covering decisions a bot never makes (roster governance, adoption of prior art, human authority, attribution) and phrased for design and business review rather than for a bot's decision loop.

This document supplies that set. It does not replace, subset, or re-rank `aegis-principles@1`.

### 0.2 Relationship to `aegis-principles@1`
- `aegis-principles@1` (P01–P12) remains the **manifest-referenced, bot-carried** set. Bots continue to cite P-ids; nothing in a bundle references an HP-id.
- `hathor-principles@1` (HP-01–HP-16) is the **platform-altitude** set used in ADRs, plans, PR review, and stakeholder communication. Every HP either restates one or more P-ids at higher altitude or restates a canonical rule that has no bot-level analogue (HP-03, HP-04, HP-12, HP-15, HP-16).
- **Conflict rule (inherited from RP-014 §3.5.1):** platform principles are not ranked against each other. A genuine conflict between two principles is a specification defect; the correct response is HP-05 (refuse with a remediation naming both principles) and a finding, never local arbitration.
- §2 carries the full mapping so the two sets cannot drift silently.

### 0.3 One-line definition

> The proposed HATHOR platform principles compress accepted AEGIS decisions into sixteen review criteria — each answered by "what does this mean in practice" and "where was this decided."

---

## 1. Proposed principles (`hathor-principles@1`)

### HP-01 — One public ingress, explicit domain authorities
Every human or agent action enters through the `aegis` CLI; the Registry, Knowledge, and Ticketing planes remain authoritative for their own domains, and the Control Tower is the authenticated asynchronous authority for registry, distribution, audit, and rollup functions rather than the terminus of every request.
- **In practice:** no bot or agent exposes a second public doorway, listener, or side channel; the CLI mediates routing, the Operator brokers third-party systems, and machines reconcile with the non-bot Tower asynchronously rather than depending on it in the request path.
- **Traces to:** `AEG-BOT-TAX-006`, `AEG-REQ-BOT-006`, `AEG-REQ-PLAT-001/003`, RP-003 (no bus), RP-010 §2, ADR-002; bot-level P03.

### HP-02 — Small units, whole responsibilities
Capability is delivered as single-role microbots; composition happens only in orchestration, never inside a unit.
- **In practice:** one bot, one manifest, one primary role; three fixed families plus one sanctioned Proctor-owned extension; roster changes require an ADR; adapters are pool entries, not bots.
- **Traces to:** `AEG-BOT-TAX-001..005`, `AEG-MBL-002/003`, RP-007 §1.3; bot-level P02.

### HP-03 — Trust is cryptographic, not assumed
Nothing routes until its provenance is verified; the signed manifest binds declared interface and governance behaviour.
- **In practice:** an external DSSE envelope signs the JCS-canonical manifest, whose fields carry the directive, rules, and principles digests; a change to any of those artifacts re-signs, re-registers, and invalidates bindings (`MANIFEST_DIGEST_STALE`), while unverified units are quarantined (`PROVENANCE_UNVERIFIED`, Gate G01). Manifest 1.1.0 does not yet bind executor bytes, so R10 must be resolved before this principle can imply executable substitution resistance.
- **Traces to:** `AEG-BOT-SEC-003`, `AEG-BOT-GOV-001`, `AEG-BOT-LIF-002`, `AEG-MAN-005`, RP-013 §6.

### HP-04 — Policy is data, and it only narrows
Governance is expressed as declarative, platform-evaluated predicates that can restrict but never grant.
- **In practice:** precedence is platform → project → bot → directive; bot rules have only `refuse` and `degrade` effects; rules are pure and evaluated by the dispatch seam, not by the executor; configuration tunes but cannot relax a rule.
- **Traces to:** `AEG-BOT-GOV-003/004/005/008`, RP-014 §3.4, §3.6.

### HP-05 — Refuse, never guess — and always steer
A structural, contract, provenance, or authority failure yields a structured refusal with a remediation; silent fallback is a defect.
- **In practice:** one error envelope `{code, message, remediation, provenance, ttl}` everywhere; every refusal names what must happen next (`next_required`, `aegis proctor gateway explain`); contract mismatch is `CONTRACT_NO_OVERLAP`, never a best-effort guess.
- **Traces to:** CORE §0.3 r2, `AEG-REQ-PLAT-004`, `AEG-BOT-CMD-003`, `AEG-GW-014`; bot-level P01, P09.

### HP-06 — The system decides completion; agents only request it
Progress, "done," and readiness are verdicts derived from recorded evidence, not claims made by the actor doing the work.
- **In practice:** only the conductor (Process-Bot) advances run state; `claim.step.done` and `node complete` are requests; claims map to required validation tiers (`CLAIM_TIER_INSUFFICIENT`); `val-evidence-Bot` attests commands ran; `val-completeness-Bot` proves at finalize that no mandatory node was skipped (`COMPLETENESS_GAP`).
- **Traces to:** `AEG-GW-001/007`, `AEG-VAL-006/008`, `AEG-BOT-MEM-004`, ADR-002; bot-level P06.

### HP-07 — Memory is externalised and shared, never private
No unit owns a durable store or learns privately; everything durable lives in a sanctioned, provenance-stamped tier reachable through the CLI.
- **In practice:** working memory dies with the invocation; run ledgers are append-only and event-sourced; caches are digest-keyed and disposable; knowledge enters as draft microbursts and is promoted only by humans; resident state is bounded and rebuildable.
- **Traces to:** `AEG-REQ-BOT-009`, `AEG-BOT-RUN-002`, `AEG-BOT-MEM-001..005`, `AEG-BOT-KNO-003/004`; bot-level P08.

### HP-08 — Hold nothing worth stealing
Long-lived provider secrets remain behind Operator's connection broker; worker bots normally receive opaque Class-1 proxy sessions and may receive only an explicitly declared Class-2, scoped, short-lived, memory-only token when proxying is impractical.
- **In practice:** Operator resolves provider credentials secrets-manager-first and never persists them in bot state; Class-2 token mint and expiry are audited. Tower-issued human identity tokens and machine/signing keys are separate platform identity material governed by their own trust surfaces, not provider credentials hidden behind Operator. Build-time linters (`ml-no-listener`, `ml-broker-symmetry`, `ml-secrets-layer`, `ml-secrets-diff`) refuse persistence or leakage; no secret enters a knowledge tier.
- **Traces to:** `AEG-BOT-ANA-006`, `AEG-BOT-SEC-001/002`, `AEG-BOT-KNO-006`, `AEG-OPB-001/002`, RP-010 §5, RP-011 §2, RP-013 §6; bot-level P04.

### HP-09 — Enforcement fails closed; observation fails open
Unreadable state blocks mandatory action; telemetry trouble never blocks business work.
- **In practice:** the admission path refuses on doubt with the applicable structured CLI error rather than collapsing validation, authority, and dependency failures into one code; the telemetry spool degrades bot `status` but keeps the business path moving; Observation bots may record but never mutate or refuse; validators refuse but never write authoritative state.
- **Traces to:** `AEG-GW-013`, `AEG-REQ-TEL-002`, `AEG-BOT-TAX-005`, `AEG-VAL-011`; bot-level P12.

### HP-10 — Degrade honestly, within bounded trust
When an authority is unreachable, continue only inside a declared trust window, report `degraded`, and refuse authority-originating actions past its TTL.
- **In practice:** at the bot contract boundary, exit 2 is a degraded/warning result carrying its cause; at the CLI boundary, degradation is an envelope/status state and command-specific exit policy applies. `verified-local` bots route within trust TTL (default 72 h) with runs flagged degraded; expired knowledge is flagged, never silently served. An unresolved optional dependency may degrade status, but attempting to dispatch an unknown capability refuses with `CAPABILITY_UNKNOWN` and CLI exit 3.
- **Traces to:** `AEG-BOT-RUN-003`, `AEG-REQ-PLAT-007`, `AEG-BOT-KNO-005`, RP-002 §3.4; bot-level P07.

### HP-11 — Provenance over recency
Verified origin and quality outrank freshness in every retrieval, routing, and promotion decision.
- **In practice:** tiered search Project → Machine → Org → Public with a quality gate; "no compliant match" beats a low-quality batch; new knowledge defaults to `draft` and only human review promotes to `verified`; a bot never mints its own `verified` record.
- **Traces to:** CORE §0.3 r3, `AEG-BOT-KNO-001/004/005`, `AEG-KST-008`, RP-004; bot-level P05.

### HP-12 — Every action is attributable and reconstructable
Each message carries its run, ticket, binding, and hierarchy chain so a run can be audited from authoritative ledgers and independently attributable receipts.
- **In practice:** no substantive mutation without an authorizing ticket (Gate G04); every conducted unit of work carries its required Procedure-through-Checklist chain. The append-only run ledger is the source for run-state reconstruction, provider receipts establish external effects, and telemetry/Tower rollups are replayable audit and operational views rather than the sole source of truth.
- **Traces to:** `AEG-REQ-TEL-007`, `AEG-REQ-SEC-006`, `AEG-BOT-TAX-004`, `AEG-BOT-OBS-001/002`, RP-006 §7.1, RP-009 §5, RP-011 §4/§6.

### HP-13 — Small, attributable increments
Work, writes, and validation are diff-scoped and session-scoped; bulk operations are the exception and require explicit human request.
- **In practice:** microburst-only knowledge writes, each attributable to one run; validation cost ladder scoped to the change set (L0 ≤ 50 ms → L3 ≤ 10 min); retries bounded at five with backoff; one run per attribution.
- **Traces to:** `AEG-BOT-KNO-003`, `AEG-BOT-RUN-004`, `AEG-VAL-007`, RP-007 §3.2; bot-level P10.

### HP-14 — Build and verify; never operate
The platform prepares and proves; humans authorize promotion and deployment, and deploy authority originates only from a ticket.
- **In practice:** agents cannot waive gates or mandatory nodes (`WAIVER_FORBIDDEN`, exit 4); knowledge promotion and deploy tickets are human-executed; post-rule compensation hints are surfaced, never auto-run; mutating commands outside `development` require a human grant (Gate G08).
- **Traces to:** CORE §0.3 r5, `AEG-REQ-TKT-011`, `AEG-VAL-005`, `AEG-GW-012`, RP-014 §3.4.2; bot-level P11.

### HP-15 — Judgement must be observable
Where rules cannot decide, the choice and its governing principle are recorded so drift in judgement is detected as readily as drift in contract.
- **In practice:** `report.decisions[]` (≤ 10) on every run citing the governing principle; principle-usage and rule-violation distributions monitored continuously at the Tower with threshold-triggered review; an undeclared principle id auto-opens a dispute-style review item; governance-class bots carry a stricter tolerance.
- **Traces to:** `AEG-BOT-GOV-007`, `AEG-BOT-CMD-018`, RP-014 §3.5.3, `AEG-KPW-006`.

### HP-16 — Adopt only what is demonstrably better
Prior-art processes and architectures are reused only where they exceed a from-scratch design, and every adoption or rejection is logged.
- **In practice:** each paper carries an adoption decision log (BOT-001 §9, RP-007 §11, RP-008 §3, RP-014 §12); the microbot single-control-plane model superseded the monolithic CLI-service model; the outline's fifteen "services" were reconciled to zero new bots.
- **Traces to:** BOT-001 §0 rule 1 and §9; CORE §0.3 r4 (reuse over invention); RP-008 §3; ADR-002 §2 driver 7.

### 1.1 Trust-model scope
These principles inherit RP-013's v1 trust model: mechanical no-skip, human-only, provenance, and enforcement claims hold against a **cooperative-but-fallible** agent using the platform interfaces. A fully adversarial local process with arbitrary workspace-file access is outside v1 prevention guarantees; v1 aims to detect that class through reconciliation and Tower-side cross-checks, with stronger integrity controls scheduled as hardening. HP-03, HP-06, HP-09, and HP-14 must not be read as expanding that boundary.

---

## 2. Mapping — `hathor-principles@1` ↔ `aegis-principles@1` ↔ canonical sources

| HP | Title | Bot-level P-id(s) | Primary canonical source |
|---|---|---|---|
| HP-01 | One public ingress, explicit domain authorities | P03 | `AEG-BOT-TAX-006`, `AEG-REQ-PLAT-001/003`, RP-010 §2, ADR-002 |
| HP-02 | Small units, whole responsibilities | P02 | `AEG-BOT-TAX-001..005`, `AEG-MBL-002/003` |
| HP-03 | Trust is cryptographic, not assumed | — (platform-only) | `AEG-BOT-SEC-003`, `AEG-BOT-GOV-001`, RP-013 §6 |
| HP-04 | Policy is data, and it only narrows | — (platform-only) | `AEG-BOT-GOV-003/004/005/008` |
| HP-05 | Refuse, never guess — and always steer | P01, P09 | CORE §0.3 r2, `AEG-GW-014` |
| HP-06 | The system decides completion | P06 | `AEG-GW-001/007`, `AEG-VAL-008`, ADR-002 |
| HP-07 | Memory is externalised and shared | P08 | `AEG-REQ-BOT-009`, `AEG-BOT-MEM-001..005` |
| HP-08 | Hold nothing worth stealing | P04 | `AEG-BOT-ANA-006`, `AEG-BOT-SEC-002`, RP-011 |
| HP-09 | Enforcement fails closed; observation fails open | P12 | `AEG-GW-013`, `AEG-REQ-TEL-002` |
| HP-10 | Degrade honestly, within bounded trust | P07 | `AEG-BOT-RUN-003`, `AEG-REQ-PLAT-007` |
| HP-11 | Provenance over recency | P05 | CORE §0.3 r3, `AEG-BOT-KNO-005` |
| HP-12 | Every action is attributable and reconstructable | — (platform-only) | `AEG-REQ-TEL-007`, `AEG-REQ-SEC-006`, Gate G04 |
| HP-13 | Small, attributable increments | P10 | `AEG-BOT-KNO-003`, `AEG-VAL-007` |
| HP-14 | Build and verify; never operate | P11 | CORE §0.3 r5, `AEG-REQ-TKT-011` |
| HP-15 | Judgement must be observable | — (meta; realizes P01–P12 audit) | `AEG-BOT-GOV-007`, RP-014 §3.5.3 |
| HP-16 | Adopt only what is demonstrably better | — (platform-only) | BOT-001 §0 r1, CORE §0.3 r4 |

Coverage check: every P01–P12 is restated by at least one HP; the five platform-only HPs (03, 04, 12, 15, 16) cover concerns a bot never decides at invocation time.

---

## 3. How the principles are used
The usages below apply only after D10 is ratified. Until then, reviewers may discuss these proposals but must cite the accepted source requirements for authoritative decisions.

| Context | Use |
|---|---|
| **ADR review** | Each option in an ADR is scored against the HPs it honours or violates (pattern: ADR-002 §6/§8 compliance tables). An option that violates any HP without an explicit, logged exception is rejected. |
| **Plan / roadmap review** | Workstreams cite the HPs they realize; a workstream that introduces a second control surface, a private store, or an unsigned unit is out of scope until an ADR amends the relevant HP. |
| **PR / change review** | Reviewers may cite `HP-nn` in findings. Mechanical enforcement remains with gates, linters, and validators (CANON-001); HPs explain *why* a gate exists, they do not replace it. |
| **Stakeholder communication** | ARCH-002 §1 and §5 are the narrative form of this set; this document is the citable form. |
| **Bot authoring** | Not used directly. Bots reference `aegis-principles@1`; a bot principle traces to a P-id, never to an HP-id (`AEG-BOT-GOV-006`). |

**Conflict handling.** Platform principles are not ranked. A design that cannot satisfy two HPs simultaneously has found a specification defect: record it as a finding naming both principles and escalate to an ADR. No paper, plan, or bot arbitrates canon locally (RP-014 §3.5.1).

---

## 4. Change control

1. **Versioning.** The proposed set identifier is `hathor-principles@1`. After ratification, any addition, removal, or rewording that changes meaning bumps to `@2`; editorial fixes do not.
2. **Authority.** Changes require operator sign-off recorded in `PENDING-EDITS.md`. A change that also alters a bot-level principle must amend RP-014 §3.5.1 in the same change (and therefore bumps `aegis-principles`), because bots' `principles.yaml` files pin the bot-carried `aegis-principles@<n>` set by version.
3. **Drift rule.** If a ratified paper and this document disagree on a principle's meaning, the paper's *requirement* wins on enforcement and this document owes an amendment; if two papers disagree, that is an ADR.
4. **No enforcement by this document.** HPs are review criteria. Anything mechanically enforceable already lives in a gate, linter, validator, or bot rule registered in CANON-001; a proposal to "enforce an HP" is a proposal to add one of those, and follows CANON-001's maintenance rule.

---

## 5. Requirement-prefix note (proposed CANON-001 §8 row)

| Prefix | Domain | Defining document |
|---|---|---|
| `HP-##` | HATHOR platform principles (review criteria, non-enforcing) | HATHOR-CANON-011 |

Recorded in `PENDING-EDITS.md` §6 as awaiting sign-off; CANON-001 is not edited by this paper.

---

## 6. Acceptance criteria for ratification

Operator sign-off makes this document ACCEPTED when:

1. The sixteen principles are accepted as a faithful platform-altitude restatement of ratified doctrine, with no principle lacking a canonical trace.
2. The §2 mapping is accepted as complete (every P01–P12 covered) and the five platform-only HPs are accepted as legitimately outside the bot-level set.
3. The relationship rule in §0.2 is accepted: `aegis-principles@1` remains the bot-carried set; HP-ids are never referenced from a bot bundle.
4. §3 usage and §4 change control are accepted; the proposed CANON-001 §8 row (§5) is applied.
5. `INDEX.md` lists this paper.

---

*Proposed doctrine restatement — awaiting operator ratification under D10. Sixteen principles, each traced; none may be cited as accepted `hathor-principles@1` until sign-off.*
