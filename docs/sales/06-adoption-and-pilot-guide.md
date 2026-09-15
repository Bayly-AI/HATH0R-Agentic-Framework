---
id: HATHOR-GUIDE-020
title: Adoption and Pilot Guide
summary: 'AEGIS should move from design to governed use incrementally:'
doc_type: GUIDE
diataxis: how-to
audience: [sales, agent]
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
# Adoption and Pilot Guide

- **Audience:** Executive sponsors, product owners, platform leaders, security, operations, and evaluation teams
- **Disclosure:** Buyer-facing evaluation guide
- **Maturity:** Recommended adoption overlay on approved and draft delivery plans

## Adoption principle

AEGIS should move from design to governed use incrementally:

> Establish ownership and baseline evidence, introduce visible low-risk controls, prove negative and recovery paths, then expand enforcement only when control effectiveness and measured value pass together.

Feature completion alone is not an expansion criterion.

## Recommended pilot profile

A suitable initial pilot has:

- one engaged team;
- one or two representative repositories;
- one primary work tracker;
- development-only mutation;
- a small set of repeatable workflows;
- enough agent activity to measure;
- a known current process;
- named product, platform, control, identity, work-system, and knowledge owners;
- users willing to record friction; and
- no critical production dependency on immature controls.

## Phase 0 — Authorize

### Objective

Make the evaluation governable before implementation or enforcement expands.

### Decisions

- Name executive sponsor, product owner, service owner, control owners, risk owner, and pilot owner.
- Select repositories, actors, workflows, provider, and development boundary.
- Define value hypotheses and stop conditions.
- Confirm source authority and maturity language.
- Create authorizing epics and tickets.
- Decide the human identity-token profile.
- Decide executable or image binding.
- Assign retention, privacy, access, backup, and cleanup ownership.
- Set four-eyes policy.
- Define initial trust TTL and degraded operations.

### Exit evidence

- approved charter and scope;
- assigned responsibilities;
- risk register;
- measurement plan;
- interface decision log; and
- funded, authorized backlog.

## Phase 1 — Baseline

### Objective

Measure the current state before introducing blocking controls.

### Baseline measures

- repository orientation time and token use;
- ticket, epic, branch, PR, run, and deployment linkage;
- audit reconstruction effort;
- direct provider and credential paths;
- validation time, reruns, rework, and escaped defects;
- outage work capture and reconciliation;
- knowledge search success, staleness, duplication, and review effort;
- user interventions and waiting time; and
- equivalent-task CLI, MCP, and hybrid behavior where relevant.

### Exit evidence

- representative sample definition;
- reproducible data;
- known limitations and confounders;
- approved target ranges; and
- no unsupported enterprise or ROI claim.

## Phase 2 — Foundation and report-only controls

### Objective

Introduce the common contract and observe behavior before broad refusal.

### Candidate scope

- CLI and project orientation;
- common response and refusal envelopes;
- bounded schemas;
- initial diff and contract checks;
- local findings and evidence records;
- definition and governance validation;
- warnings or report-only findings;
- no production writes; and
- passive task, latency, retry, and token measurement.

### Change activities

- train users on authority boundaries and remediation;
- record bypass pressure as product evidence;
- review false positives weekly;
- compare pilot behavior with baseline;
- freeze interfaces before dependent work fans out; and
- retain the existing enterprise tracker.

### Exit evidence

- stable contracts;
- bounded orientation and validation cost;
- acceptable finding accuracy;
- recoverable authoritative local records;
- no unassigned critical findings; and
- explicit approval for selective enforcement.

## Phase 3 — Controlled development enforcement

### Objective

Enforce low-ambiguity controls in a safe boundary.

### Recommended order

1. Contract and structural validation.
2. Capability provenance and registration.
3. Change, assumption, claim, and evidence checks.
4. Simple linear sequence and barrier behavior.
5. Revocation and trust expiry.
6. Human-only actions only after the identity contract is implemented.

### Required tests

- invalid schema and contract;
- invalid, unknown, stale, and revoked definition;
- false completion and missing evidence;
- out-of-order action;
- process interruption and resume;
- trust-TTL expiry;
- actionable refusal and resubmission; and
- waiver refusal until valid human identity exists.

### Exit evidence

- control outcomes and false-refusal trend;
- artifact binding implemented to the stated level;
- trust-model language in user material;
- development exceptions visibly degraded;
- active incident and support route; and
- approval for work and knowledge integration.

## Phase 4 — Conducted delivery

### Objective

Prove the end-to-end accountability chain for a bounded development workflow.

### Candidate scope

- one primary work provider;
- minimal backup capture and reconciliation;
- live ticket, epic, and change-binding checks;
- brokered provider access;
- complete work, hierarchy, run, evidence, and outcome linkage;
- knowledge draft and human review;
- sequence and completeness reconciliation;
- action-bound human identity;
- deployment dry-run and refusal; and
- Tower ingest and query.

### Recovery exercises

- work-provider outage and conflict;
- Operator interruption and replay;
- Tower outage and trust expiry;
- telemetry outage with authoritative ledger intact;
- torn or concurrent run record;
- missing mandatory node;
- stale or disputed knowledge;
- key and component revocation; and
- expired, replayed, wrong-action, wrong-audience, and spoofed human authority.

### Exit evidence

- independent end-to-end reconstruction;
- no silent loss, overwrite, or duplicate effect in tested cases;
- complete human authorization for in-scope reserved actions;
- reconciliation within approved bounds;
- acceptable user and operator effort; and
- sponsor decision to continue, redesign, or stop.

## Phase 5 — Expand

Potential expansion:

- additional work-provider adapters;
- organization knowledge and curation;
- broader hierarchy;
- complete passive observation;
- complex graphs after semantics are frozen;
- container and build governance;
- additional repositories; and
- a second team.

Repeat baseline, threat, recovery, friction, and value review for each new scope. Do not assume evidence transfers automatically across providers or environments.

## Phase 6 — Operate and optimize

Operational readiness requires:

- SLOs and capacity;
- support and incident management;
- access and key review;
- backup and recovery;
- evidence and data retention;
- policy and schema drift controls;
- cost and benefit reporting;
- waiver and degraded-operation governance;
- knowledge quality calibration;
- release and deprecation management; and
- periodic risk and value re-approval.

## Proof-of-value scorecard

Agree measures before the pilot:

| Dimension | Example measure | Acceptance direction |
|---|---|---|
| Authorization | In-scope mutations with valid work | Complete for enforced scope |
| Traceability | Outcomes traversable from epic to evidence | Complete for acceptance sample |
| Completion | False-completion cases refused | All defined negative tests |
| Human authority | Reserved actions with valid human proof | Complete |
| Credentials | Class-1 worker credential exposure | None |
| External effects | Provider mutations with complete receipt | Complete for governed scope |
| Recovery | Silent loss, overwrite, or duplicate effect | None in tested scenarios |
| Knowledge | Correct status, provenance, freshness display | Complete in evaluation sample |
| Friction | False refusal and remediation effort | Within agreed threshold |
| Performance | Orientation and validation latency | Within agreed target |
| Value | Time, quality, risk, or effort change | Baseline-relative, buyer-approved |
| Adoption | Eligible work using governed path | Increasing without shadow-path shift |

## Stop or redesign conditions

Stop expansion when:

- users require routine bypass;
- identity or artifact trust fails negative tests;
- legitimate work is frequently blocked without useful remediation;
- authoritative records are lost or diverge;
- retry or recovery creates duplicate or silent effects;
- operating effort exceeds agreed bounds without offsetting value;
- outcomes do not improve;
- privacy or retention cannot be met; or
- the implementation requires claims stronger than its trust model.

## Roadmap context

The approved platform plan sequences eight workstreams and six milestones. Its estimate of 2,370–3,080 base engineering hours and approximately 20–26 weeks for two engineers or 12–16 weeks for four engineers is:

- post-foundation interface freeze;
- planning grade;
- pre-implementation;
- exclusive of important product, control, adoption, support, and audit work;
- not a fixed delivery date; and
- not a commercial price.

Re-baseline after foundations.

## Mutual responsibilities

### AEGIS product or implementation team

- maintain source and claim status;
- define interfaces and acceptance tests;
- provide implementation and test evidence;
- document known gaps;
- train pilot users;
- support recovery exercises; and
- report friction and outcomes honestly.

### Adopting organization

- provide owners and approvers;
- define policies and risk appetite;
- select representative workflows;
- provide identity, work, source, and deployment integration;
- approve retention and access;
- participate in baseline and evaluation;
- review waivers and incidents; and
- decide expansion from evidence.

## Sources

- [Adoption Roadmap](../business/06-adoption-roadmap.md)
- [Value and Success Measures](../business/07-value-and-success-measures.md)
- [Platform Roadmap](../architect/aegis-plan-001-platform-roadmap-20260913.md)
- [Gateway and Validator Roadmap](../architect/aegis-plan-003-gateway-validators-roadmap-20260913.md)
