---
id: AEGIS-GUIDE-010
title: AEGIS Business Glossary and Source Register
summary: 1. [`AEGIS-CANON-001`](../architect/aegis-canon-001-registries-20260913.md) is the authority for enumerated gates, events, refusal codes, linters, bot roster, and identifiers.
doc_type: GUIDE
diataxis: reference
audience: [business, agent]
tags: []
version: 0.1.0
status: draft
created: '2026-09-14'
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
# AEGIS Business Glossary and Source Register

- **Business document:** 08 of 08
- **Status:** Derived draft for business review
- **Source baseline:** Architecture corpus as of 2026-09-14
- **Purpose:** Preserve terminology, source authority, status, and claim traceability for the business documentation set

## 1. Authority rules

1. [`AEGIS-CANON-001`](../architect/aegis-canon-001-registries-20260913.md) is the authority for enumerated gates, events, refusal codes, linters, bot roster, and identifiers.
2. Accepted ADRs and accepted research/interface decisions own ratified choices.
3. Draft or proposed requirements, research papers, architectures, and technical specifications remain review material except where later accepted decisions explicitly amend them.
4. Approved plans schedule work but do not ratify a draft design, authorize code, prove delivery, or realize benefits.
5. Synthesis documents do not promote the status of their sources.
6. This business set introduces business organization and recommended adoption practices; it does not create architecture doctrine.
7. On conflict, the source architecture wins and this set must be amended.

These files intentionally use descriptive business-series numbers rather than minting `AEGIS-BUS-*` identifiers. `AEGIS-CANON-001` reserves canonical AEGIS document IDs for the architecture document types it enumerates.

## 2. Business glossary

| Term | Business meaning |
|---|---|
| AEGIS | The proposed governance and control-plane realization of the HATHOR framework |
| HATHOR | The broader agentic application framework for portable project structure, discoverable knowledge, governance, secure capability access, and attributable work |
| `aegis` CLI | The sole public operational ingress for supported human, agent, and bot actions; not itself a source-of-truth plane |
| Actor | A human, AI agent, system, or bot identity that requests or performs an action |
| Agent | A model-backed or other AI worker that uses platform interfaces; it supplies work content but does not own platform authority |
| Microbot or bot | A single-purpose capability unit with an independent definition, contract, governance, runtime behavior, and lifecycle |
| Bot Definition Bundle | The manifest, contract, governance artifacts, executor, interfaces, telemetry definition, fixtures, and external signature envelope that define a bot |
| Capability | Versioned intent used for routing, shaped as `<domain>.<noun>.<verb>@<major>`; callers address capability, not bot name |
| Registry Plane | Authority for which bot definitions may run |
| MBI | Machine Bot Index used for local routing and verification state |
| TBR | Tower Bot Registry used for organization registration, acknowledgement, and revocation authority |
| Knowledge Plane | Authority for what the organization knows, including record provenance, status, review, freshness, and retrieval |
| Ticketing Plane | Authority for what work exists and how it is authorized, linked, estimated, and reconciled |
| Control Tower | Non-bot platform authority for registration, trust distribution, identity, curator registry, rollup ingest, and bounded query |
| Proctor-Bot | Admission and routing authority that verifies provenance and contract and applies gates |
| Process-Bot | Conductor of governed runs and sole writer of authoritative run-transition events |
| Operator-Bot | Exclusive broker for supported third-party connections and long-lived provider credentials |
| Validator bot | Proctor-owned, single-purpose checker that may produce a refusing verdict but cannot write authoritative plane state |
| Observation bot | Passive recorder or aggregator that never mutates or refuses business work |
| Information hierarchy | Procedure → Strategy → Playbook → Runbook → Workflow → Checklist |
| Procedure | The business problem and required outcome that root a unit of work |
| Strategy | A chosen direction under a procedure |
| Playbook | Guidelines that implement a strategy |
| Runbook | Concrete task set and execution entry point |
| Workflow | Scripts or tools that progress a runbook |
| Checklist | Step-level completion ledger |
| Conducted run | A governed execution whose sequence and state are controlled by Process and admitted by Proctor |
| Orchestration Gateway | Draft execution and enforcement design in which events trigger, Process decides, and Proctor enforces |
| Process graph | Machine-readable required work, sequence, branching, and completion structure for a conducted run |
| Required set | Mandatory reachable nodes derived from the process graph |
| Executed set | Nodes and evidence recorded as completed in authoritative ledgers |
| Lawful skip | An explicit optional node or non-selected exclusive branch recorded as skipped; not an omitted mandatory step |
| Fold | Deterministic reconstruction of current run state from append-only events |
| Finding | Normalized validation result with severity, scope, evidence, and remediation |
| Assumption ledger | Run-scoped record of assumptions, status, expiry, and recheck evidence |
| Claim | Actor assertion that requires a mapped validation tier and evidence before acceptance |
| Evidence ledger | Record of commands, exits, report digests, and related proof used for validation and completion |
| Continuous Validation System | Change-time assurance model combining linters, validators, suites, assumptions, claims, evidence, and gates |
| Micro-linter | Pure, bounded structural check, normally using `ml-*` naming |
| Gate | Mechanical control that admits or refuses an action at a defined trigger |
| Refusal | Structured denial with code, message, remediation, provenance, and relevant TTL |
| Degraded | Explicitly reduced assurance or dependency state in which only policy-approved action may continue; not silent success |
| Trust TTL | Maximum period cached authority may support declared degraded operation before authority-originating action refuses |
| Human authority | Verified decision right reserved for a human, including specified waiver, deployment, and knowledge-promotion actions |
| DVO | Source term for the human deployment role or workflow; the corpus does not expand it, so each organization must define it |
| Ticketing Economy | Business concept in which ticket is the unit of authorized work, epic is the mandate, and the Ticketing Plane is the ledger |
| Canonical Ticket Contract | Provider-neutral representation of work translated by Jira, Azure DevOps, GitHub, or backup adapters |
| Buffered work | Work recorded during provider outage and pending reconciliation; not equal to authoritative provider state |
| Reconciliation | Controlled comparison and replay from local or backup state to its authority, with explicit conflict handling |
| Microburst | One bounded knowledge record or patch that enters as draft with provenance and required metadata |
| Draft knowledge | Authored content that has not received the required human verification |
| Verified knowledge | Content explicitly promoted by an authorized human reviewer with identity and time |
| Provenance over recency | Verified source and quality outrank mere freshness in routing and retrieval |
| Class 1 connection | Default Operator-proxied external call; worker receives no provider credential |
| Class 2 connection | Declared exception using a scoped, short-lived, run-bound, memory-only token |
| Idempotency key | Stable request identity used to prevent duplicate external effects during retry or resume |
| Spool-and-drain | Local append of passive events followed by asynchronous Observation delivery and Tower rollup |
| Governance triad | Directive, rules, and principles digest-referenced by the bot manifest |
| Directive | Bounded charter describing what the bot is for |
| Rules | Platform-evaluated constraints describing what the bot must never do; they may narrow but not grant |
| Principles | Decision heuristics used where rules are silent and made observable through reported decisions |
| Configuration | Schema-validated tuning outside the signed governance bundle; cannot relax policy |
| `aegis-principles@1` | Accepted bot-carried principle set from RP-014 |
| `hathor-principles@1` | Proposed platform-altitude principle synthesis in CANON-002; not accepted until D10 sign-off |
| Cooperative-but-fallible | Accepted v1 threat focus: an actor may drift, forget, reorder, hallucinate, or overclaim but does not deliberately subvert platform files |
| Adversarial local process | Process with arbitrary workspace access; outside v1 prevention guarantees and inside detection/hardening scope |
| Universal Project Layout | Draft canonical repository structure intended to make projects predictable to people and agents |
| InfraOS | Baseline system and migration/façade source studied by the corpus; not the AEGIS target platform |

## 3. Source-status register

### 3.1 Corpus control

| Source | Status at baseline | Business use |
|---|---|---|
| [`INDEX.md`](../architect/INDEX.md) | Canonical corpus index | Framework boundary, reading order, source status, scope rule |
| [`PENDING-EDITS.md`](../architect/PENDING-EDITS.md) | Living change-control register | Ratified amendments, pending sign-offs, external actions, unresolved decisions |
| [`AEGIS-CANON-001`](../architect/aegis-canon-001-registries-20260913.md) | Accepted | Canonical gates, events, refusals, linters, bot roster, naming |
| [`AEGIS-CANON-002`](../architect/aegis-canon-002-platform-principles-20260914.md) | Proposed; awaiting D10 sign-off | Platform-principle synthesis; may not be cited as accepted doctrine |

### 3.2 Requirements and architecture

| Source | Status at baseline | Business use |
|---|---|---|
| [`AEGIS-REQ-CORE-001`](../architect/AEGIS-REQ-CORE-001-initial-requirements-20260911.md) | Draft, amended | Platform framing, actors, scope, core requirements, acceptance targets, open decisions |
| [`AEGIS-REQ-BOT-001`](../architect/aegis-bot-taxonomy-requirements-20260911.md) | Draft | Bot families, anatomy, command and runtime contract |
| [`AEGIS-ARCH-001`](../architect/AEGIS-ARCH-001-architecture-mermaid-20260911.md) | Draft, amended | End-to-end architecture and lifecycle diagrams |
| [`AEGIS-ARCH-002`](../architect/aegis-arch-002-bot-unit-compendium-20260914.md) | Draft synthesis; awaiting D9 sign-off | Stakeholder bot summary; source papers remain authoritative |

### 3.3 Architecture decisions

| Source | Status at baseline | Business use |
|---|---|---|
| [`AEGIS-ADR-001`](../architect/aegis-adr-001-target-command-tree-20260911.md) | Proposed; partly superseded by ADR-003 | Taxonomy and migration history only where retained |
| [`AEGIS-ADR-002`](../architect/aegis-adr-002-orchestration-coordination-model-20260913.md) | Accepted | Central event-triggered orchestration; Process decision and Proctor enforcement |
| [`AEGIS-ADR-003`](../architect/aegis-adr-003-greenfield-command-surface-20260913.md) | Accepted | Greenfield `aegis`, nine domains, exit boundaries, InfraOS façade |
| [`AEGIS-ADR-004`](../architect/aegis-adr-004-layout-state-residency-20260913.md) | Accepted | Canonical paths, spool/state residency, macOS/Linux v1 boundary |
| [`AEGIS-ADR-005`](../architect/aegis-adr-005-backup-ticketing-system-20260913.md) | Accepted | Minimal first-party backup ticket service rather than adopting a full tracker |

### 3.4 Research and interface decisions

| Source | Status at baseline | Business use |
|---|---|---|
| [`AEGIS-RP-001`](../architect/aegis-rp-001-manifest-schema-v1-20260911.md) | Draft, amended | Manifest, contract handshake, registration behavior |
| [`AEGIS-RP-002`](../architect/aegis-rp-002-registry-discovery-20260911.md) | Draft, amended | Local/Tower registry, verification states, trust TTL |
| [`AEGIS-RP-003`](../architect/aegis-rp-003-telemetry-transport-20260911.md) | Draft, amended | Spool-and-drain telemetry, event delivery and quota |
| [`AEGIS-RP-004`](../architect/aegis-rp-004-knowledge-promotion-20260911.md) | Draft | Knowledge promotion, reviewer authority, dispute and aging |
| [`AEGIS-RP-005`](../architect/aegis-rp-005-hierarchy-consolidation-20260911.md) | Draft, amended | Six identities, one chassis, chain resolution and degradation |
| [`AEGIS-RP-006`](../architect/aegis-rp-006-ticketing-plane-20260911.md) | Draft, amended | Ticket Contract, providers, backup, reconciliation, work governance |
| [`AEGIS-RP-007`](../architect/aegis-rp-007-continuous-validation-20260911.md) | Draft, partly superseded | Validation fabric, findings, assumptions, claims, evidence, gates |
| [`AEGIS-RP-008`](../architect/aegis-rp-008-microbot-launch-roster-20260912.md) | Draft, amended | Launch phasing and roster reconciliation |
| [`AEGIS-RP-009`](../architect/aegis-rp-009-orchestration-gateway-20260912.md) | Draft | Conducted run, sequence/barrier, graph, completion, resume |
| [`AEGIS-RP-010`](../architect/aegis-rp-010-tower-surface-20260913.md) | Accepted design | Tower registration, distribution, curators, ingest, query, identity |
| [`AEGIS-RP-011`](../architect/aegis-rp-011-operator-brokering-20260913.md) | Accepted design | Proxy default, scoped-token exception, idempotency and broker audit |
| [`AEGIS-RP-012`](../architect/aegis-rp-012-knowledge-storage-retrieval-20260913.md) | Accepted design | Knowledge record, storage, retrieval, confidence, MCP contracts |
| [`AEGIS-RP-013`](../architect/aegis-rp-013-threat-model-20260913.md) | Accepted design | Threat actors, trust boundary, identity, signing, hardening |
| [`AEGIS-RP-014`](../architect/aegis-rp-014-bot-unit-creation-operation-20260913.md) | Accepted design | Governance triad, state/memory, channels, bot lifecycle |

### 3.5 Technical specifications and plans

| Source | Status at baseline | Business use |
|---|---|---|
| [`AEGIS-TS-001`](../architect/aegis-ts-001-continuous-validation-implementation-20260911.md) | Draft | Implementation-level CVS P0–P2 design and technical tests |
| [`AEGIS-TS-002`](../architect/aegis-ts-002-orchestration-gateway-implementation-20260913.md) | Draft | Run log, conductor, admission, resume, reconciliation implementation design |
| [`AEGIS-TS-003`](../architect/aegis-ts-003-bot-unit-implementation-20260913.md) | Draft | Bundle, governance engine, effects, scaffold, registration, memory implementation |
| [`AEGIS-PLAN-001`](../architect/aegis-plan-001-platform-roadmap-20260913.md) | Approved planning artifact | Eight workstreams, six milestones, estimates, dependencies |
| [`AEGIS-PLAN-002`](../architect/aegis-plan-002-cvs-p0-p2-roadmap-20260911.md) | Draft, amended | Detailed validation roadmap; ticket-sizing convention is not realized savings |
| [`AEGIS-PLAN-003`](../architect/aegis-plan-003-gateway-validators-roadmap-20260913.md) | Approved planning artifact | Gateway epics, remaining validators, bounded agent skill pack |

### 3.6 Research baselines and business narratives

| Source | Status at baseline | Business use and limitation |
|---|---|---|
| [`AEGIS CLI Research Report`](../architect/AEGIS-CLI-Research-Report-2026-09-11.md) | Historical baseline, annotated | Vision and prior-art baseline; later ADRs own target decisions |
| [`Invocation Inventory`](../architect/01-Invocation-Inventory-Top30-2026-09-11.md) | Baseline | One-machine usage evidence; not fleet evidence |
| [`CLI Spec Scoring`](../architect/02-CLI-Spec-Scoring-2026-09-11.md) | Baseline | Provisional scoring; does not prove conformance |
| [`Schema/Runbook Spike`](../architect/04-Spike-Schema-Runbook-Checklist-2026-09-11.md) | Spike design | Non-production learning and decision artifact |
| [`Token Benchmark`](../architect/05-Token-Benchmark-CLI-vs-MCP-2026-09-11.md) | Baseline | Single-run, rough-token, non-equivalent comparison with an unhealthy path |
| [`Ticketing Economy Whitepaper`](../architect/aegis-ticketing-economy-whitepaper-20260911.md) | Draft, annotated | Business value hypotheses and pilot suggestion; not delivered benefit evidence |
| [`Containerization Article`](../architect/aegis-containerization-article-20260911.md) | Draft, annotated | Target container taxonomy and business rationale |
| [`Containerization Presentation`](../architect/aegis-containerization-presentation-script-20260911.md) | Draft, annotated | Presentation companion, not independent authority |
| [`AEGIS.pdf`](../architect/AEGIS.pdf) | Known-defective reference export | Raster text is illegible and the bottom row is clipped; do not use as authoritative evidence |

## 4. Business-document traceability

| Business document | Primary architecture sources |
|---|---|
| [01 — Executive Overview](./01-executive-overview.md) | INDEX, CORE, ADR-002/003, RP-010..014, PLAN-001, ARCH-002 with draft caveat |
| [02 — Business Requirements](./02-business-requirements.md) | CORE, CANON-001, ADR-002..005, RP-001..014 |
| [03 — Business Capability Model](./03-business-capability-model.md) | CORE scope, CANON-001, RP-004/006/007/009..014, PLAN-001 |
| [04 — Operating Model](./04-operating-model.md) | ADR-002, RP-004..014, ARCH-001/002, CANON-001 |
| [05 — Governance, Risk, and Controls](./05-governance-risk-and-controls.md) | CANON-001, RP-013, RP-010/011/014, PENDING-EDITS |
| [06 — Adoption Roadmap](./06-adoption-roadmap.md) | PLAN-001/002/003, RP-008/009, Ticketing Economy pilot, baselines |
| [07 — Value and Success Measures](./07-value-and-success-measures.md) | CORE acceptance, RP-003/004/006/007/009..014, research baselines |
| [08 — Glossary and Source Register](./08-glossary-and-source-register.md) | INDEX, CANON-001, PENDING-EDITS, all listed source groups |

## 5. Status-sensitive statements

| Topic | Permitted statement at baseline |
|---|---|
| HATHOR/AEGIS relationship | Canonical corpus boundary |
| Central orchestration | Accepted decision |
| Nine-domain greenfield CLI | Accepted decision |
| Canonical gates and 26-bot roster | Accepted enumeration; implementation not established |
| Tower, brokering, knowledge mechanics, threat model, bot governance | Accepted design; no implementation authorization |
| Core v1 requirements | Draft target |
| Ticketing, promotion, registry, telemetry, hierarchy, validation, gateway | Draft target except later accepted amendments |
| Platform roadmap | Approved sequence and planning estimate; not implementation proof |
| Bot compendium | Draft synthesis awaiting D9 |
| HATHOR platform principles and HP identifiers | Proposed synthesis awaiting D10 |
| Product benefits | Intended outcomes or hypotheses until measured |
| Security, outage, replay, and completion guarantees | Require implementation tests and stated threat boundary |

## 6. Open decision register for business review

The live authority remains [`PENDING-EDITS.md`](../architect/PENDING-EDITS.md). Business review should track at least:

- framework/README alignment;
- signed-pack admission timing;
- human-token claims, action binding, and replay;
- authenticated gateway event policy;
- cyclic graph, attempt, and required-set semantics;
- authoritative local ledger versus telemetry export;
- out-of-process effect verification;
- Operator crash, concurrency, and idempotency behavior;
- knowledge promotion and retrieval calibration;
- module/repository path;
- executable or image binding;
- four-eyes scope;
- EKS-only versus alternate hosting;
- local registry scope;
- Tower tenancy and identity provider;
- state retention and cleaner ownership; and
- fleet evidence and benchmark v2.

## 7. Known documentation inconsistencies

- The repository `README.md` contains layout and credential-resolution descriptions that differ from the amended corpus. Use the architecture `INDEX`, CORE, ADR-004, and accepted brokering decisions for the target boundary until the README is aligned.
- `AEGIS.pdf` is not legible enough to recover the complete board and has clipped source content.
- Older papers may contain lists superseded by `AEGIS-CANON-001`.
- ADR-001 is partly superseded by ADR-003.
- RP-007 orchestration language is partly superseded by ADR-002 and RP-009.
- D9 and D10 remain pending sign-off.

## 8. Maintenance procedure

When an architecture source changes:

1. verify its source status and owning authority;
2. check `PENDING-EDITS.md` for ratification and cross-document impacts;
3. update the affected business requirement, capability, workflow, risk, roadmap, or metric;
4. preserve the distinction between accepted direction, draft target, approved sequence, recommendation, and delivered evidence;
5. update the traceability table;
6. validate internal links and terms; and
7. record the business reviewer and decision outside this derived set according to organization policy.

## 9. Interpretation rule

If a reader cannot tell whether a statement is a design, plan, implementation fact, operational result, or business outcome, the statement is incomplete and must be qualified before use.

