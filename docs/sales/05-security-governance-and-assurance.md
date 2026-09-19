---
id: HATHOR-GUIDE-019
title: Security, Governance, and Assurance
summary: HATHOR is designed to add layered governance to human and AI-assisted work. It does not claim that a CLI, signature, ticket, gate, or telemetry stream is sufficient on its own.
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
# Security, Governance, and Assurance

- **Audience:** CISO, security architecture, risk, compliance, audit, platform, and legal
- **Disclosure:** Buyer-facing security brief; detailed threat material should be shared under the organization’s disclosure process
- **Maturity:** Accepted threat and control design with material implementation and operating gaps

## Security position

HATHOR is designed to add layered governance to human and AI-assisted work. It does not claim that a CLI, signature, ticket, gate, or telemetry stream is sufficient on its own.

The control objective is to scale delegated work without weakening:

- authorization;
- separation of duties;
- traceability;
- evidence quality;
- credential control;
- capability provenance;
- knowledge integrity;
- change governance;
- resilience; or
- honesty about residual risk.

## Trust model

The accepted v1 prevention scope is a **cooperative-but-fallible** actor using platform interfaces. Such an actor may drift, forget, reorder, hallucinate, or overclaim, but does not deliberately subvert platform files.

A malicious local process with arbitrary workspace access is:

- outside v1 prevention guarantees;
- inside detection goals; and
- a subject of later integrity hardening.

Every statement about no-skip, human-only behavior, state ownership, tamper resistance, or control enforcement must retain this boundary.

## Layered control model

| Layer | Objective | Target evidence |
|---|---|---|
| Identity and authority | Identify actor type and reserve named decisions for humans | Machine signature, human token reference, actor record |
| Capability trust | Admit only known, eligible, non-revoked automation | Definition signature, governance digests, registry state |
| Contract and policy | Constrain inputs, outputs, side effects, and tuning | Schemas, rules, policy, structured refusal |
| Work governance | Bind substantive work to authorization and strategy | Ticket, epic, branch, PR, and run links |
| Conducted execution | Control sequence and authoritative transitions | Process graph and run event ledger |
| Continuous assurance | Evaluate change, assumptions, claims, evidence, and completion | Findings and run-scoped ledgers |
| External-effect control | Contain credentials and make effects attributable | Broker session, idempotency record, provider receipt |
| Human decision | Preserve approval for waiver, deployment, and promotion | Action-bound human identity, reason, expiry, approval |
| Observation and review | Detect drift, failure, cost, retry, and degraded operation | Passive telemetry, query, and control review |

## Canonical control gates

The accepted registry contains 15 gates:

| ID | Gate | Control objective |
|---|---|---|
| G01 | Provenance | Refuse unknown, invalidly signed, revoked, or quarantined capabilities |
| G02 | Contract | Refuse incompatible or structurally invalid requests and responses |
| G03 | Sequence/Barrier | Refuse out-of-order, predecessor-incomplete, or unbound execution |
| G04 | No-Ticket | Refuse in-scope substantive work without durable authorization |
| G05 | Epic Linkage | Require strategic lineage |
| G06 | PR-Ticket Bind | Preserve change-to-work linkage |
| G07 | Estimation | Require planning data and expose oversized work |
| G08 | Development Only | Prevent higher-environment mutation without human grant |
| G09 | Deploy Ticket | Require reconciled, human-executed deployment authority |
| G10 | Change Validation | Prevent progression with blocking findings |
| G11 | Assumption | Prevent action on open, broken, or expired assumptions |
| G12 | Claim Evidence | Require mapped validation and evidence |
| G13 | Undeclared Assumption | Surface known but undeclared failure classes in strict profiles |
| G14 | Micro-Linter | Prevent structurally noncompliant artifacts from containerization |
| G15 | Knowledge Promotion | Prevent unfit drafts from entering trusted knowledge |

The registry is accepted. Implemented enforcement must be demonstrated separately.

## Preventive controls

Target preventive measures include:

- signed capability definitions and governance;
- registration, verification state, revocation, and quarantine;
- schema validation and contract negotiation;
- sequence and barrier checks;
- work, linkage, environment, and deployment gates;
- narrowing-only rules;
- Operator-mediated provider access;
- human identity for reserved actions;
- signed organization-distributed trust and policy material;
- build-time structural linting;
- secret and sensitive-data checks;
- explicit trust TTL; and
- no public listeners for worker bots.

## Detective controls

Target detective measures include:

- append-only run, evidence, finding, and assumption records;
- completion reconciliation;
- provider receipts and idempotency records;
- Tower registration, revocation, ingest, and query;
- drift and validation findings;
- knowledge staleness and dispute;
- retry, success, latency, token, and degradation observation;
- rule and principle reporting; and
- planned hash-chain and independent cross-check hardening.

## Corrective controls

Target corrective measures include:

- structured refusals with remediation;
- fix and resubmit;
- quarantine and revocation;
- scoped, recorded, expiring human waiver;
- provider conflict escalation;
- run reconstruction and resume;
- knowledge rejection, supersession, dispute, review, or archive;
- replay and deduplication; and
- controlled design and policy amendment.

Automatic compensation after a violating external effect is excluded from the accepted bot model. Detection and human-led correction are the intended response.

## Identity and separation of duties

The target distinguishes human, agent, machine, bot, service, and provider identities.

Reserved human actions require more than an interactive terminal or chat statement. The intended proof is a short-lived Tower-issued identity token bound to the action and context.

Before enforcement, the design must freeze and test:

- issuer and signing authority;
- subject and role;
- audience;
- exact action;
- run and work context;
- nonce or replay protection;
- issuance and expiry;
- revocation;
- four-eyes rules; and
- negative cases for expired, replayed, wrong-action, wrong-audience, and machine identity.

## Credential and integration security

The accepted default is proxy-based brokering:

- workers do not own long-lived provider credentials;
- Operator resolves and uses the governed connection;
- each external effect is intended to carry actor, intent, run, ticket, capability, connection, and idempotency context;
- retries and circuit behavior are bounded; and
- token handoff is an explicit, narrow exception.

Production assurance requires evidence for secret custody, memory handling, logs, crash recovery, concurrency, idempotency, provider semantics, and egress controls.

## Capability and supply-chain trust

The target uses canonicalized definitions, digest-referenced governance artifacts, signatures, registration, trust distribution, and revocation.

**Known gap:** The accepted definition does not yet bind the runtime executable, container image, or an OCI/SLSA-style attestation. A valid definition could therefore be paired with substituted code unless the implementation adds and verifies artifact binding.

Do not claim complete software supply-chain integrity until this is resolved and substitution tests pass.

## Evidence and audit

The target reconstructs a material action from:

- authorizing work and strategic lineage;
- actor identity;
- capability and version;
- policy and admission result;
- run events;
- findings, assumptions, claims, and evidence;
- reserved human decisions;
- external-effect receipts; and
- final outcome.

Telemetry provides correlation and analysis. It must not be the sole authoritative record.

## Resilience and degraded trust

HATHOR aims to make degraded operation explicit:

- cached signed trust may remain usable within policy and TTL;
- expired authority-originating actions refuse;
- provider work may buffer only where allowed;
- buffered state is not authoritative;
- reconciliation exposes conflict;
- idempotency and deduplication limit repeated effects; and
- observation export can replay later if authoritative business records remain durable.

The documentation does not prove lossless recovery or exactly-once effects.

## Knowledge security

The target Knowledge Plane includes:

- provenance and ownership;
- human review;
- record status;
- TTL and staleness;
- secret and PII checks;
- dispute and supersession;
- source-tier and confidence display; and
- explicit inclusion of drafts or external material.

It does not establish that knowledge is currently free of secrets or that retrieval quality is calibrated.

## Compliance-aligned outcomes

The design may support an organization’s controls for:

- change authorization;
- separation of duties;
- least privilege;
- credential management;
- software provenance;
- audit logging;
- evidence retention;
- incident reconstruction;
- continuity;
- data and knowledge quality; and
- third-party integration oversight.

HATHOR does not create certification or compliance by architecture alone. The buyer remains responsible for control mapping, configuration, access review, retention, operating evidence, testing, and independent assessment.

## Material residual risks

| Risk | Current design position | Required treatment before strong claim |
|---|---|---|
| Design mistaken for delivery | Corpus labels source maturity | Link claims to code, tests, and operations |
| Runtime artifact substitution | Definition is signed; executable binding open | Freeze and test artifact or attestation binding |
| Human-token replay or mis-scope | Identity surface accepted; profile open | Define and negatively test complete contract |
| Local evidence tampering | Adversarial process outside v1 prevention | Hash chain, external anchor, independent evidence |
| Spoofed gateway event | Event authority incomplete | Authenticated emitter, nonce, evidence, replay policy |
| Complex graph ambiguity | Loop and attempt semantics incomplete | Freeze state model and crash-resume tests |
| Run record versus telemetry ambiguity | Local authority direction recommended | Make authoritative commit fail closed |
| Self-declared out-of-process effects | Cooperative trust assumption | Mediated or observed effect reconciliation |
| Broker interruption | HA and persistence not frozen | Fault injection and recovery specification |
| Insider approval misuse | Four-eyes scope open | Organizational separation-of-duties policy |
| Retention and privacy | Ownership absent | Approved classification, access, retention, deletion |
| Documentation drift | Generation and CI checks planned | Contract-driven docs and conformance testing |

## Security diligence questions

A buyer should ask:

1. Which controls are implemented, and where is the evidence?
2. Which negative, replay, expiry, and recovery tests pass?
3. What is the exact local threat assumption?
4. How are executables and images bound to registered definitions?
5. How is human authority issued, scoped, and replay-protected?
6. Where do authoritative records live?
7. Which provider credentials can any worker process observe?
8. How are broker crashes and ambiguous provider results reconciled?
9. What happens at trust-TTL expiry?
10. How are evidence, identity, telemetry, and knowledge retained and accessed?
11. Which actions require four-eyes approval?
12. What is the incident and revocation process?

## Enforcement expansion blockers

Do not expand to higher-risk environments if:

- human identity can be spoofed or replayed;
- artifact integrity is below the claimed assurance level;
- normal failures can lose authoritative run records;
- provider recovery can silently overwrite or duplicate effects;
- mandatory work can be skipped inside the accepted threat model;
- users require routine bypass;
- false refusal or latency exceeds agreed limits;
- control and incident owners are unassigned;
- retention or privacy is undefined; or
- measured value does not justify control cost.

## Sources

- [Governance, Risk, and Controls](../business/05-governance-risk-and-controls.md)
- [Threat Model](../architect/hathor-rp-013-threat-model-20260913.md)
- [Canonical Registries](../architect/hathor-canon-001-registries-20260913.md)
- [Pending Decisions and Risks](../architect/PENDING-EDITS.md)
