---
id: HATHOR-GUIDE-017
title: Platform Capabilities
summary: 'AEGIS is designed around one top-level business capability: **governed agentic delivery**.'
doc_type: GUIDE
diataxis: reference
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
# Platform Capabilities

- **Audience:** Technology, engineering, platform, security, and operations buyers
- **Disclosure:** Buyer-facing draft; preserve target-state language
- **Maturity:** Defined capabilities with mixed accepted, draft, and proposed design status

## Capability model

AEGIS is designed around one top-level business capability: **governed agentic delivery**.

This means delegating work to humans and AI agents while preserving authorization, strategic lineage, trusted knowledge, evidence-based completion, controlled external access, human decision rights, and reconstructable outcomes.

The platform capability areas are:

1. governance and trust;
2. work and conducted delivery;
3. knowledge and integration;
4. operations and assurance; and
5. platform enablement.

## 1. Governance and trust

### Governed interaction

**Purpose:** Apply a common operational contract to supported human, agent, and automation actions.

**Target behavior:**

- one public `aegis` command surface;
- structured text or JSON outputs;
- bounded schema discovery;
- stable exit and refusal behavior;
- capability-based routing rather than caller knowledge of component names; and
- policy application independent of language or agent harness.

**Buyer value hypothesis:** Lower process variation and less governance logic embedded in individual tools.

**Status:** Greenfield CLI direction and nine-domain surface are accepted; detailed core implementation remains draft.

### Identity and human authority

**Purpose:** Distinguish people, agents, machines, and bots and reserve named decisions for verified humans.

**Target reserved actions include:**

- control waiver;
- deployment or environment promotion;
- authoritative knowledge promotion;
- capability revocation; and
- selected governance changes.

**Buyer value hypothesis:** Automation can prepare and request without approving its own highest-risk action.

**Status:** Tower identity surface and human-only direction are accepted design; the full token and replay profile remains open.

### Capability provenance and lifecycle

**Purpose:** Know which capability definition may run and manage it from creation to retirement.

**Target lifecycle:**

`authorize → create → self-test → sign → register → operate → evolve → revoke or retire`

**Target controls:**

- versioned manifest and contract;
- governance artifacts;
- signature and registration;
- local and Tower registry state;
- revocation and quarantine;
- side-by-side contract versions; and
- successor routing.

**Status:** Bot lifecycle and governance model are accepted design; registry mechanics are partly draft. The manifest does not yet bind executable or image bytes.

### Policy and control management

**Purpose:** Make constraints inspectable and consistent.

The bot governance model separates:

- **directive:** what the capability is for;
- **rules:** what it must not do;
- **principles:** how discretionary choices are explained; and
- **configuration:** bounded tuning that cannot grant permission.

The accepted gate registry defines 15 mechanical control points. A proposed project-rules and policy-floor design remains under review.

## 2. Work and conducted delivery

### Work authorization and strategic linkage

**Purpose:** Bind substantive work to durable authorization and business context.

**Target linkage:**

`strategic epic → authorized ticket → branch/change → conducted run → evidence → outcome`

**Target work providers:** Jira, Azure DevOps, GitHub, and a minimal backup ticket service.

**Status:** Canonical work-related gates and backup approach are accepted directions; the Ticketing Plane and adapters remain draft.

### Conducted runs and hierarchy

**Purpose:** Make plans, required work, sequence, and state explicit.

The information hierarchy is:

1. Procedure — business problem and required outcome;
2. Strategy — selected direction;
3. Playbook — governing guidance;
4. Runbook — concrete task set;
5. Workflow — scripts and tools; and
6. Checklist — step-level completion ledger.

Events may trigger evaluation. Process decides run transitions. Proctor admits or refuses dispatch.

**Status:** Central event-triggered orchestration is accepted. Detailed graph, loop, attempt, and gateway behavior remains draft.

### Evidence-based completion

**Purpose:** Make completion a controlled state transition rather than an actor assertion.

**Target inputs:**

- required and executed work sets;
- validation findings;
- evidence records;
- claims and mapped validation tiers;
- assumptions and expiry;
- lawful skips; and
- provider receipts.

**Status:** Validation and gateway designs are draft, with accepted orchestration and canonical gate boundaries.

### Human-authorized promotion

**Purpose:** Keep higher-risk promotion under verified human authority.

Agents may author, build, test, and prepare. The target model requires human-executed authorization for deployment and human review for promotable knowledge.

The organization must define roles, four-eyes policy, emergency handling, and environment scope.

## 3. Knowledge and integration

### Governed knowledge

**Purpose:** Treat knowledge as a lifecycle-managed asset rather than unqualified chat history.

**Target search order:**

`Project → Machine → Organization → Public`

**Target record properties:**

- provenance and ownership;
- status and reviewer identity;
- freshness and TTL;
- hierarchy linkage;
- confidence and quality;
- conflict, dispute, supersession, and archive state; and
- secret and sensitive-data checks.

New material enters as draft. Promotion is a human act.

**Status:** Storage and retrieval mechanics are accepted design; promotion workflow details remain draft.

### Secure external integration

**Purpose:** Centralize provider connection handling without turning worker bots into credential holders.

**Class 1:** Operator proxies the call; the worker receives no provider credential.

**Class 2:** A declared exception uses a narrow, short-lived, run-bound, memory-only token when proxying is impractical.

Operator is intended to manage credential resolution, sessions, rate limiting, circuit breaking, idempotency, degradation, and effect receipts.

**Status:** Brokering direction is accepted design; production persistence, HA, and fault behavior need implementation evidence.

### Tracker portability and reconciliation

**Purpose:** Apply a common work contract while retaining the selected enterprise tracker as authority.

During outages, eligible work may be buffered and marked degraded. Reconciliation must distinguish authoritative, buffered, conflicting, and resolved state. Backup-only work cannot create deployment authority.

## 4. Operations and assurance

### Continuous validation

**Purpose:** Apply assurance throughout the change lifecycle at a cost proportionate to risk.

**Target layers:**

- build-time structural micro-linters;
- change-time linters and validator bots;
- dispatch-time provenance, contract, sequence, and domain gates; and
- runtime passive observation.

**Target validation tiers range from:** fast static checks through asynchronous analysis.

**Status:** Continuous-validation research and implementation specifications remain draft; roadmap sequencing exists.

### Audit and reconstruction

**Purpose:** Reconstruct intent, authorization, run state, evidence, decisions, and effects.

Authoritative records include work items, registry entries, run events, findings, assumptions, claims, evidence, human decisions, and provider receipts. Telemetry provides correlated analysis but is not intended to become the source of business truth.

### Observation and economics

**Purpose:** Measure task outcomes, latency, retries, degradation, validation, and token use without allowing monitoring to mutate work.

Observation components are passive by design. Export can degrade without blocking business logic only if the authoritative local run and audit record remains safely committed.

### Bounded continuity and recovery

**Purpose:** Continue eligible activity through dependency outages without silently granting authority.

**Target mechanisms:**

- signed cached trust and local verified state;
- explicit trust TTL;
- append-only local ledgers;
- spool-and-drain delivery;
- minimal backup work capture;
- idempotency and deduplication;
- run fold and resume; and
- explicit conflict reconciliation.

## 5. Platform enablement

### Portable project orientation

**Purpose:** Give humans and agents a predictable way to understand a repository.

The target Universal Project Layout defines known locations for configuration, scripts, libraries/assets, source, build output, tests, documentation, agent instructions, manifests, rules, state, and knowledge.

**Important:** The root README and visual source contain legacy layout and credential descriptions that differ from later architecture decisions. The architecture index and accepted residency/brokering decisions take precedence.

### Component modularity

**Purpose:** Keep each capability single-purpose, independently testable, late-bound, and replaceable.

The canonical design enumerates 26 bots. The number is an architecture roster, not proof that 26 implementations exist.

### Container and delivery governance

**Purpose:** Apply identity, health, version, secret, lint, and promotion rules to deployment units.

The draft taxonomy includes:

- Class A — control-plane interfaces;
- Class B — stateful knowledge services;
- Class C — stateless worker or bot hosts; and
- Class D — observation and telemetry services.

The deployment direction names EKS for higher environments, while final hosting boundaries remain an open business decision.

## Differentiation themes

These are design distinctions, not competitively validated superiority claims.

### Governance above the model and harness

AEGIS is intended to remain stable when models, agent harnesses, repositories, and work providers change.

### Separate authorities, one operating contract

The design avoids making one orchestration service the source of truth for capability, knowledge, work, and run state.

### Completion evaluated from evidence

The target separates actor requests from authoritative progression.

### Human authority by design

Agents can increase execution capacity without becoming approvers.

### Credential mediation instead of credential distribution

The brokered model reduces the number of components expected to handle provider secrets.

### Honest degraded operation

Outage behavior is intended to expose reduced trust and expire local authority rather than report silent success.

### Replaceable micro-capabilities

Single-purpose components, capability routing, and external state are intended to reduce coupling.

### Knowledge with status and provenance

Retrieval quality includes source tier, freshness, verification state, and confidence—not similarity alone.

## Capability maturity rule

| Level | Required evidence |
|---|---|
| Defined | Outcome, authority, interface, and control intent are documented |
| Implemented | Authorized code and configuration exist |
| Verified | Positive, negative, recovery, replay, and threat-boundary tests pass |
| Piloted | Real users and agent workloads produce measured evidence in bounded scope |
| Operational | Ownership, SLOs, support, retention, access, and incident processes are active |
| Scaled | Multiple teams and providers retain value without control erosion |

The documentation establishes substantial **Defined** maturity. Later levels require separate evidence.

## Sources

- [Business Capability Model](../business/03-business-capability-model.md)
- [Canonical Registries](../architect/aegis-canon-001-registries-20260913.md)
- [Bot Unit Model](../architect/aegis-rp-014-bot-unit-creation-operation-20260913.md)
- [Architecture Corpus Index](../architect/INDEX.md)
