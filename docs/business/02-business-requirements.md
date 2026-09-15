---
id: AEGIS-GUIDE-004
title: AEGIS Business Requirements
summary: OBJ-*` and `BIZ-*` labels are local traceability aids for this derived document. They do not add canonical AEGIS requirements or amend `AEGIS-CANON-001`.
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
# AEGIS Business Requirements

- **Business document:** 02 of 08
- **Status:** Derived draft for business review
- **Source baseline:** Architecture corpus as of 2026-09-14
- **Purpose:** Translate the architecture corpus into business outcomes, scope, requirements, dependencies, and acceptance conditions

`OBJ-*` and `BIZ-*` labels are local traceability aids for this derived document. They do not add canonical AEGIS requirements or amend `AEGIS-CANON-001`.

## 1. Business problem

The organization needs to scale human and AI-assisted delivery while preserving a durable chain of authorization, strategic alignment, evidence, security, and human decision rights.

Existing delivery tools each hold part of the truth. Work may be authorized in one tracker, implemented in a repository, discussed in chat, validated in CI, deployed through another system, and explained after the fact by the actor that performed it. Increasing agent autonomy multiplies the number and speed of these actions and makes manual reconciliation an unreliable control.

The required business change is to establish a common operating contract in which:

- work is authorized before substantive action;
- automation capabilities are known and governed before use;
- trusted knowledge has provenance and review state;
- evidence, not narrative, determines completion;
- third-party effects use controlled credentials and are attributable;
- human authority remains mandatory for high-risk promotion;
- outages create bounded, visible degradation rather than invisible bypass; and
- every material action can be reconstructed from authoritative records.

## 2. Business objectives

| ID | Objective | Intended outcome |
|---|---|---|
| OBJ-01 | Establish one governance path for human and machine work | Consistent policy, identity, refusal, and evidence behavior |
| OBJ-02 | Make every substantive action accountable | Traceability from strategic mandate to outcome |
| OBJ-03 | Replace self-attested completion with system-evaluated completion | Higher confidence that mandatory work and validation occurred |
| OBJ-04 | Preserve human authority for promotion and exception | Clear separation of duties at the highest-risk decisions |
| OBJ-05 | Reduce tool and provider lock-in | Stable governance above Jira, Azure DevOps, GitHub, languages, and agent harnesses |
| OBJ-06 | Reduce credential and integration risk | Provider access mediated through a controlled broker |
| OBJ-07 | Turn operational knowledge into a governed organizational asset | Reusable information with provenance, freshness, quality, and human review |
| OBJ-08 | Maintain controlled continuity through dependency outages | Work capture and local activity continue only inside declared trust bounds |
| OBJ-09 | Make the economics and quality of automation measurable | Per-run evidence for cost, retry, quality, latency, and control outcomes |
| OBJ-10 | Preserve honest security claims | Controls and product messaging remain inside the accepted trust boundary |

## 3. Stakeholders and needs

| Stakeholder | Need |
|---|---|
| Executive sponsor | Evidence that investment improves throughput and control without creating unmanaged risk |
| Product or platform owner | A prioritized capability model, stable scope, roadmap, and measurable acceptance criteria |
| Engineering leadership | A common operating contract that works across teams, repositories, languages, and tools |
| Developers and AI-agent users | Fast orientation, predictable commands, clear refusals, and minimal manual policy interpretation |
| Delivery operations | Human authority over deployment, reliable evidence, and recoverable workflows |
| Security and risk | Least-privilege external access, provenance, revocation, trust boundaries, and explicit residual risk |
| Compliance and audit | Reconstructable intent, authorization, evidence, decisions, and external effects |
| Knowledge owner or curator | Review authority, provenance, conflict handling, and lifecycle controls for shared knowledge |
| Work-system owner | Provider-neutral integration without surrendering authority of the enterprise tracker |
| Automation component owner | An independent create, test, register, evolve, and retire lifecycle |

Roles not explicitly assigned in the architecture—such as executive sponsor, product owner, risk owner, and service owner—must be assigned by the adopting organization before operational use.

## 4. Scope

### 4.1 Business scope for v1

- governed access to agentic capabilities through one public command surface;
- common accountability rules for people, agents, and automation units;
- three distinct authorities for capability, knowledge, and work;
- conducted work with hierarchy, evidence, sequence, and completion controls;
- work authorization across Jira, Azure DevOps, GitHub, and a backup ticket service;
- governed knowledge retrieval, authoring, review, promotion, dispute, and aging;
- controlled third-party access and secret containment;
- capability provenance, registration, revocation, and bounded offline use;
- passive observation, cost, quality, retry, and audit rollups;
- portable project structure and agent orientation;
- governed container build and human-authorized promotion; and
- per-organization, self-hostable operation on macOS and Linux clients.

### 4.2 Business exclusions for v1

- replacing foundation models or agent harnesses;
- replacing enterprise work trackers;
- a browser-based Control Tower user interface;
- multi-tenant SaaS operation;
- automatic deployment or automatic knowledge promotion;
- autonomous waiver of policy or mandatory work;
- support for a fully adversarial local process as a prevention guarantee;
- Windows client support;
- provider adapters beyond the three named work systems; and
- proof of regulatory compliance without organization-specific control implementation and audit.

## 5. Business requirements

### BIZ-GOV-001 — Single governed operational ingress

All supported human, agent, and automation actions must use one public operational contract so identity, policy, routing, refusal, and evidence are applied consistently.

**Business acceptance:** No supported capability requires a user or agent to bypass the governed interface. Any exception is documented, risk-accepted, time-bounded, and approved through change control.

**Source basis:** Draft `AEG-REQ-PLAT-001`; accepted ADR-003; accepted RP-010 boundary decision.

### BIZ-GOV-002 — Explicit authority boundaries

The organization must maintain distinct sources of truth for runnable automation, trusted knowledge, and authorized work. A platform service may coordinate these authorities but must not silently replace their decision rights.

**Business acceptance:** Every material decision can be attributed to the Registry, Knowledge, Ticketing, human, or run authority that owns it.

**Source basis:** Draft `AEG-REQ-PLAT-003`; accepted RP-010, RP-012, and ADR-002.

### BIZ-ACC-001 — Equal accountability for human and machine actors

Human users, AI agents, and bots must operate under the same requirements for identity, work authorization, evidence, and audit.

**Business acceptance:** The audit model can identify actor type and identity without weakening authorization or evidence requirements for machine actors.

**Source basis:** Draft CORE actor and audit requirements; accepted threat model and bot-unit model.

### BIZ-WRK-001 — Authorized work before substantive action

Implementation, refactoring, configuration or rule changes, commits, branches, pull requests, and other substantive mutations must be linked to an authorizing work item. Read-only orientation, research, and question answering may remain exempt.

**Business acceptance:** Enforced-scope substantive actions without a resolvable ticket are refused with a clear remediation.

**Source basis:** Draft `AEG-REQ-TKT-004`; accepted canonical Gate G04; ticketing architecture remains draft.

### BIZ-WRK-002 — Strategic lineage and change binding

Authorized work must link to a strategic epic, and code changes must bind to the authorizing ticket.

**Business acceptance:** The organization can traverse from initiative to ticket to branch or change to conducted run and outcome.

**Source basis:** Draft `AEG-REQ-TKT-005/006`; accepted canonical ticket-related gates.

### BIZ-WRK-003 — Provider-neutral work contract

People, agents, and policy must interact with work through one provider-neutral contract while the selected Jira, Azure DevOps, GitHub, or backup provider remains authoritative.

**Business acceptance:** The same business operation has consistent fields and control outcomes regardless of the underlying supported tracker.

**Source basis:** Draft RP-006 and CORE ticketing requirements; accepted ADR-005 for the backup approach.

### BIZ-WRK-004 — Controlled continuity and reconciliation

Provider outages must not force work outside the accountability ledger. Eligible work may be captured in a visibly degraded buffer within a declared trust period and reconciled without silent overwrite when authority returns.

**Business acceptance:** Buffered, authoritative, conflicting, and reconciled states are distinguishable; deployment authority cannot originate from unreconciled backup-only state.

**Source basis:** Draft `AEG-REQ-TKT-009/010`; accepted ADR-005 and RP-011 brokering behavior.

### BIZ-RUN-001 — Conducted work with explicit lineage

Every governed run must connect the business procedure and selected strategy to playbook, runbook, workflow, checklist, authorizing ticket, and outcome as required for that work.

**Business acceptance:** A run cannot silently begin mid-process or lose its required hierarchy chain.

**Source basis:** Draft RP-005; accepted ADR-002 central orchestration and canonical hierarchy roster.

### BIZ-RUN-002 — System-evaluated sequence and completion

Actors may request progress, completion, claims, and waivers, but the platform must evaluate sequence, evidence, and required work before changing authoritative run state.

**Business acceptance:** Out-of-order work, unsupported claims, missing required nodes, and false completion are refused or surfaced as explicit gaps.

**Source basis:** Accepted ADR-002; draft RP-009 and TS-002; canonical Sequence/Barrier Gate G03.

### BIZ-AST-001 — Continuous, proportionate assurance

Validation must operate throughout the change lifecycle and scale its cost to the scope and risk of the change.

**Business acceptance:** Changed work receives the required validation tier and evidence; small changes do not routinely incur whole-repository validation cost.

**Source basis:** Draft RP-007 and TS-001; approved PLAN-002/003 sequencing; canonical validation gates and linters.

### BIZ-HUM-001 — Human authority for promotion and exception

Agents may prepare, build, and validate. Authorized humans promote knowledge at every promotable tier; Tower-issued human identity is required for organization-tier promotion, control waiver, and deployment authority.

**Business acceptance:** Machine identity, TTY presence, or chat approval cannot substitute for the required human authorization record.

**Source basis:** Draft CORE deployment and knowledge requirements; accepted RP-010 identity surface, RP-013 threat control, and RP-014 human-only behavior.

### BIZ-KNO-001 — Governed knowledge lifecycle

Shared knowledge must have provenance, ownership, status, freshness, hierarchy linkage, quality information, conflict handling, and a human review path.

**Business acceptance:** New content enters as draft; only an authorized human can verify it; stale, disputed, archived, and external content are not silently presented as current verified truth.

**Source basis:** Draft RP-004; accepted RP-012 storage and retrieval design.

### BIZ-KNO-002 — Honest, tiered retrieval

The platform must prefer project-specific verified knowledge over machine, organization, and public sources and must return no confident match rather than an unqualified low-quality answer.

**Business acceptance:** Retrieval exposes source tier, confidence, status, and freshness, and records when broader or draft content was requested.

**Source basis:** Accepted RP-012; draft CORE knowledge requirements.

### BIZ-SEC-001 — Brokered external access

Worker automation must not own long-lived provider credentials. External calls must use a controlled broker that proxies by default and grants only declared, scoped, short-lived, memory-only tokens when proxying is impractical.

**Business acceptance:** External effects are attributable to actor, intent, run, ticket, provider connection, and idempotency key; no Class-1 worker process receives credential material.

**Source basis:** Accepted RP-011; accepted bot-unit constraints; draft CORE security requirements.

### BIZ-SEC-002 — Verified capability before use

Automation units and organization-distributed execution inputs must be identified, validated, signed, registered, and revocable before enforced use.

**Business acceptance:** Unverified, expired, revoked, or structurally invalid capability definitions are quarantined and cannot receive new work.

**Source basis:** Accepted RP-013 signing choices and RP-014 lifecycle; draft RP-001/002; accepted canonical Provenance Gate.

### BIZ-SEC-003 — Honest trust boundaries

Security and product claims must distinguish protection against cooperative-but-fallible actors from detection and future hardening against malicious local processes.

**Business acceptance:** No-skip, human-only, and tamper-resistance claims state their threat scope and identify residual controls.

**Source basis:** Accepted RP-013.

### BIZ-AUD-001 — Reconstructable intent and outcome

Every material mutation and external effect must be reconstructable from authoritative run and audit records, including identity, declared intent, authorization, hierarchy, evidence, decisions, provider receipts, and result.

**Business acceptance:** An auditor can reconstruct a sampled action without relying on actor memory or telemetry as the sole source of truth.

**Source basis:** Draft `AEG-REQ-PLAT-010`, `AEG-REQ-TEL-007`, and `AEG-REQ-SEC-006`; accepted RP-010/011 query and receipt design.

### BIZ-OPS-001 — Bounded, visible degradation

Loss of a supporting authority may permit only explicitly defined actions inside a time-bounded trust window. The platform must visibly distinguish degraded status and refuse authority-originating actions after expiry.

**Business acceptance:** No dependency outage creates silent success, hidden fallback, or indefinite local authority.

**Source basis:** Draft `AEG-REQ-PLAT-007`; accepted RP-010/011; draft RP-002/003/006.

### BIZ-OPS-002 — Structured refusal with a path forward

Structural, contract, policy, authority, provenance, sequence, and dependency failures must return a consistent refusal that explains the problem and the next required action.

**Business acceptance:** Users and agents can remediate a refusal without guessing or bypassing the control.

**Source basis:** Accepted ADR-003 exit boundaries and canonical refusal registry; draft CORE error contract.

### BIZ-PLT-001 — Portable project and capability model

The governance contract must remain independent of implementation language, code framework, and agent harness and must define a recognizable project structure.

**Business acceptance:** A conforming repository and capability can be used from supported environments without depending on an undocumented tool-specific layout.

**Source basis:** Draft CORE platform and Universal Project Layout requirements; accepted ADR-004 state-residency decisions.

### BIZ-PLT-002 — Independently replaceable automation

Each automation unit must have one primary responsibility and an independent lifecycle so it can be tested, evolved, quarantined, replaced, or retired without hidden shared state.

**Business acceptance:** Failure or retirement is isolated, callers are directed to a successor where available, and durable organizational records survive component retirement.

**Source basis:** Accepted RP-014; accepted canonical 26-bot roster; draft bot taxonomy.

### BIZ-MEA-001 — Observable quality, risk, and cost

The organization must be able to measure authorization coverage, validation outcomes, completion gaps, retries, latency, degraded operation, knowledge quality, external effects, and per-run token usage.

**Business acceptance:** Metrics are derived from governed records and can be segmented by project, capability, environment, and actor type without treating telemetry as the sole business authority.

**Source basis:** Draft telemetry and validation papers; accepted RP-010 Tower query surface; canonical observation roster.

## 6. Non-functional business expectations

| Expectation | Source target | Business significance |
|---|---|---|
| Fast liveness checks | Under 250 ms | Governance should not create visible friction for basic health and orientation |
| Bounded agent orientation | At most 2,500 output tokens | Agents should learn the control surface without excessive context cost |
| Bounded schema pages | At most 8 KB by default | Discovery remains usable and economical |
| Bounded hierarchy resolution | At most three command round-trip waves | Traceability should not create serial orchestration delay |
| Proportionate validation | 50 ms to 10 min tiers, asynchronous above | Assurance cost matches change scope and lifecycle stage |
| Bounded retry | At most five transient retries with backoff | Provider failures do not create retry storms or hidden cost |
| Supported client platforms | macOS and Linux, arm64 and amd64 | Defines the v1 adoption boundary |

These remain target requirements, not observed service levels.

## 7. Assumptions and dependencies

- Adopting projects use Git.
- Enterprise trackers remain authoritative for their mapped work records.
- The organization operates or designates one Control Tower authority.
- Human identity is available through an organization identity provider.
- Control owners define trust TTL, environment, retention, and access policies.
- Provider adapters, identity tokens, signed artifacts, run ledgers, and reconciliation behavior are implemented and tested before strict enforcement.
- Teams accept that direct supported provider access by worker bots is outside the governed model.
- Knowledge curators and work-system owners are assigned.
- Telemetry can fail open only where the authoritative local run and audit record remains safely committed.
- The organization distinguishes design acceptance, implementation authorization, deployment approval, and business benefit realization.

## 8. Business acceptance conditions for v1

The business target should not be accepted until:

1. every in-scope substantive mutation is attributable to authorized, strategically linked work;
2. sampled runs can be reconstructed from intent through outcome without actor testimony;
3. the platform refuses false completion and missing mandatory evidence;
4. deployments, waivers, and authoritative knowledge promotions require verifiable human identity;
5. unverified or revoked capabilities receive no new work;
6. supported tracker operations behave consistently and outages do not lose or silently overwrite work;
7. provider credentials remain behind the broker except for audited, declared, short-lived exceptions;
8. degraded operations are visible and stop at their authority boundary or TTL;
9. knowledge retrieval and promotion preserve status, provenance, and reviewer authority;
10. value, friction, false-refusal, cost, and control metrics are available for pilot comparison;
11. the executable-artifact binding gap is closed before strong supply-chain claims are made; and
12. control testing validates both positive and negative paths inside the accepted threat model.

## 9. Open business decisions

| Decision | Why it matters |
|---|---|
| Product, service, risk, and control ownership | The architecture defines technical actors but not organizational accountability |
| Pilot team, repositories, provider, and enforcement profile | Scope determines baseline quality and blast radius |
| Four-eyes approval policy | Deploy-path waivers and organization knowledge may require stronger separation of duties |
| Human identity-token contract | Enforced high-risk actions depend on action, audience, run, expiry, and replay semantics |
| Executable/image attestation | The current manifest design does not bind runtime bytes |
| Evidence and knowledge retention | Audit, privacy, storage, and legal requirements must be reconciled |
| Trust TTL by authority and environment | Continuity and risk appetite differ between development and production |
| Hosting target | The corpus carries an EKS direction while asking whether ECS/Fargate is permitted |
| Multi-organization tenancy | Tower v1 is described as per organization; future service boundaries remain open |
| Success thresholds and stop conditions | Pilot expansion should depend on agreed business and risk evidence |

## 10. Traceability

Detailed source-to-business traceability and status guidance are maintained in [08 — Glossary and Source Register](./08-glossary-and-source-register.md). If a requirement here appears stronger than its cited source, the source status and wording prevail.

