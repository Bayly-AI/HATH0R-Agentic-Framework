---
id: HATHOR-GUIDE-027
title: Claims, Evidence, and Source Coverage
summary: 'This document prevents architecture detail from being mistaken for product availability or business proof. It defines:'
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
# Claims, Evidence, and Source Coverage

- **Audience:** Internal sales, solutions, product marketing, product, security, legal, and documentation owners
- **Disclosure:** Internal only
- **Maturity:** Source-governance record through 2026-09-15; the derived business set remains based on the 2026-09-14 architecture index

## Purpose

This document prevents architecture detail from being mistaken for product availability or business proof. It defines:

- source authority;
- claim classes;
- approved and prohibited formulations;
- evidence required to unlock stronger claims;
- disclosure guidance;
- known source conflicts;
- missing commercial proof; and
- coverage of every original documentation artifact reviewed for this sales library.

## Authority order

When sources disagree:

1. [`HATHOR-CANON-010`](../architect/aegis-canon-001-registries-20260913.md) owns enumerated registries and identifiers.
2. Accepted architecture decisions and accepted research/interface decisions own ratified choices.
3. Draft or proposed requirements, research, architectures, and technical specifications remain review material.
4. Approved plans own sequence, not implementation approval or availability.
5. The [business set](../business/INDEX.md) is a derived interpretation.
6. Developer guides and visual boards explain intended roles but do not override architecture status.
7. This sales set translates sources and creates no product doctrine.

The live change-control authority is [`PENDING-EDITS.md`](../architect/PENDING-EDITS.md).

## Product maturity statement

The repository supports:

- a framework identity and Apache-2.0 license;
- detailed business and architecture intent;
- accepted architecture decisions;
- canonical control and bot registries;
- draft requirements and implementation specifications;
- approved sequencing plans;
- developer-role target guidance;
- a legacy/current `infraos-os` baseline used for research; and
- value, control, and pilot hypotheses.

It does not establish:

- greenfield AEGIS implementation;
- a production release;
- a running Control Tower;
- verified provider adapters;
- passed acceptance or recovery tests;
- customer deployment or adoption;
- certification;
- commercial packaging;
- support or SLA;
- measured benefit; or
- ROI.

## Claim classes

| Claim class | Evidence represented | Permitted language |
|---|---|---|
| Framework identity | README and license | “HATHOR is documented as…” |
| Accepted design | Accepted ADR, CANON, or RP decision | “The accepted AEGIS design specifies…” |
| Draft target | Draft requirement, research, architecture, or specification | “The target design proposes…” |
| Approved sequence | Approved plan | “The approved roadmap sequences…” |
| Proposed item | Awaiting sign-off | “A proposal under review would…” |
| Legacy/current baseline | Fact-checked InfraOS research | “The baseline system currently provided…” |
| Implemented AEGIS | Authorized code and configuration | Use only with repository/version evidence |
| Verified AEGIS | Positive, negative, recovery, and boundary tests | Use only with test scope and result |
| Piloted | Real users and workloads in bounded scope | Use only with pilot design and data |
| Operational | Ownership, support, SLOs, retention, access, and incidents active | Use only with operating evidence |
| Scaled | Multiple teams/providers retain outcomes | Use only with longitudinal evidence |
| Business outcome | Credible baseline and comparison | “The measured pilot observed…” with limits |

## Approved baseline formulations

| Topic | Approved formulation |
|---|---|
| Category | “AEGIS is a proposed agentic governance and assurance platform.” |
| Framework relationship | “HATHOR is the broader agentic application framework; AEGIS is its proposed governance/control-plane realization.” |
| Value proposition | “AEGIS is designed to make human-and-agent delivery bounded, evidence-backed, and human-governed.” |
| CLI | “The accepted design uses one public `aegis` operational ingress.” |
| Authority | “The target architecture separates capability, knowledge, work, run-state, and human decision authority.” |
| Completion | “The target design makes completion a system-evaluated transition based on required work and evidence.” |
| Bots | “The accepted canonical design enumerates 26 single-purpose bot roles; implementation is not established.” |
| Integrations | “Jira, Azure DevOps, GitHub, and a minimal backup service are documented target work adapters.” |
| Credentials | “The accepted design keeps long-lived provider credentials out of worker bots by default through proxy-based brokering.” |
| Human control | “The target reserves waiver, authoritative knowledge promotion, and higher-environment promotion for verified humans.” |
| Knowledge | “The accepted knowledge design exposes source tier, status, freshness, provenance, and confidence.” |
| Continuity | “The target uses time-bounded cached trust, explicit degradation, and reconciliation.” |
| Threat model | “v1 prevention is scoped to cooperative-but-fallible actors using platform interfaces.” |
| Compliance | “The design may support organization-specific controls; it is not a certification.” |
| Value | “The documentation defines value hypotheses and a measurement plan; realized ROI is not established.” |
| License | “The repository is distributed under Apache License 2.0, subject to its terms.” |
| Existing baseline | “Operational InfraOS research informed the AEGIS design; it is not AEGIS implementation proof.” |

## Claims requiring implementation and tests

Do not say these until scoped evidence exists:

- AEGIS blocks unauthorized work.
- Runs cannot skip required work.
- False completion is prevented.
- Revoked capabilities receive no work.
- Signed definitions cannot be paired with substituted runtime code.
- Workers never see provider credentials.
- Provider effects are idempotent under retry and resume.
- Work continues without loss through outages.
- Knowledge is free of secrets or sensitive information.
- Human-only actions cannot be spoofed or replayed.
- The platform meets its latency or recovery targets.
- All named provider adapters work consistently.

## Claims requiring operating and business evidence

Do not say these based on design or tests alone:

- AEGIS reduces incidents.
- AEGIS improves cycle time.
- AEGIS lowers cost.
- AEGIS accelerates onboarding.
- AEGIS provides governance without drag.
- AEGIS works across the enterprise.
- Customers are using AEGIS.
- AEGIS meets an SLA.
- AEGIS has proven ROI.

## Prohibited or tightly scoped language

Avoid:

- tamper-proof;
- impossible to bypass;
- fully autonomous and safe;
- zero secrets;
- guaranteed exactly once;
- always available;
- never loses work;
- always returns correct knowledge;
- supports every provider;
- compliance-certified;
- production-ready; and
- proven ROI.

## Evidence unlock matrix

| Stronger claim | Minimum evidence |
|---|---|
| “Implemented” | Authorized code, configuration, release/version, and owner |
| “Enforces” | Passing positive and negative tests for named control and scope |
| “Human-only” | Issuer, subject, audience, action, run, nonce, expiry, revocation, and replay tests |
| “Artifact integrity” | Executable/image/attestation binding plus substitution and rollback tests |
| “Idempotent effect” | Provider-specific retry, interruption, ambiguity, and reconciliation tests |
| “Resilient” | Capacity-bounded outage, expiry, replay, conflict, and recovery evidence |
| “Secure credential handling” | Worker inspection, secret scans, exception records, logs, and egress tests |
| “Trusted knowledge” | Retrieval evaluation, metadata, review, freshness, dispute, and sensitive-content tests |
| “Operational” | SLO, support, incident, backup, retention, access, capacity, and ownership records |
| “Faster” or “lower cost” | Representative baseline, equivalent tasks, full costs, confounders, and repeated comparison |
| “Enterprise scale” | Multiple teams/providers, longitudinal results, and no control erosion |
| “Compliant” | Named control mapping, operating evidence, assessment, and approved legal/compliance statement |

## Disclosure levels

### Buyer-safe after review

- product category and relationship;
- problem hypotheses;
- intended outcomes;
- high-level authority model;
- human control;
- brokered-access concept;
- knowledge governance concept;
- measured-pilot recommendation;
- explicit maturity statement; and
- Apache-2.0 license fact.

### Controlled technical diligence

- logical architecture;
- target interfaces and provider scope;
- canonical control themes;
- trust-model boundary;
- identity and artifact prerequisites;
- state and evidence authorities;
- degraded-operation design;
- deployment direction;
- non-functional targets as targets; and
- residual-risk categories.

### Internal only unless specifically approved

- exploit-enabling implementation gaps;
- exact local paths, ports, quotas, TTLs, and credential locations;
- employee or personal filesystem paths;
- internal ticket, branch, channel, commit, or provider details;
- unresolved module ownership;
- raw project estimates and staffing assumptions;
- weak benchmark results without full limitations;
- internal role acronyms not defined for the buyer;
- detailed bot/gate identifiers where unnecessary;
- defective source boards; and
- admin, CI, or process weaknesses.

## Material source conflicts

### README versus architecture canon

The README includes legacy hidden-folder and credential-resolution behavior, including project and sibling environment-file fallback. Later architecture sources center `.aegis/` and accepted Operator brokering. Use architecture sources for target behavior.

### Present tense versus early formation

Some README, developer, and visual language uses “is,” “must,” or “will” as if behavior exists. The README status and architecture index make clear that implementation is not established. Treat normative developer text as target contract.

### Tower on every request

Visual material suggests actions terminate at Control Tower. Accepted architecture says Tower is asynchronous and not every request’s terminus.

### Gate, bot, and validation counts

Legacy visuals and guides contain differing counts. Use `HATHOR-CANON-010` for the accepted 15-gate and 26-bot enumerations. A count still does not prove implementation.

### Telemetry topology and authority

Container material emphasizes OTel, while the telemetry research favors a file spool for machine-tier transport. A further conflict exists between fail-open telemetry and completion evidence. Do not publish one definitive deployed topology.

### Hosting

EKS appears as an internal/reference direction, but hosting and alternate container targets are not fully frozen. Do not state a universal EKS-only commitment.

### Knowledge verification

“Agents build and verify” refers to technical work. Agents must not verify their own knowledge as authoritative.

### DVO

DVO is used as a human deployment role or workflow but lacks a complete organizational definition. Prefer “authorized human deployment operator.”

### Session records versus live register

A session summary said decisions were closed, but the later pending-edits register records D9–D11 and R1–R10. Use the later register.

## Commercial and content gaps

No source defines:

- product SKU or edition;
- hosted versus self-managed commercial offering;
- price or consumption unit;
- support package;
- SLA or service credit;
- warranty or indemnity;
- data-processing terms;
- privacy and security addendum;
- trademark usage rights;
- implementation service;
- channel or partner model;
- customer reference;
- case study;
- competitive analysis;
- analyst validation;
- production benchmark;
- accessibility statement; or
- general-availability date.

These must be created and approved outside architecture documentation before use.

## Source coverage method

The inventory included all Markdown, text/license, PDF, and documentation-image artifacts in the repository tree, excluding the newly generated `docs/sales` folder. Architecture source status is taken from the architecture index and pending-edits register. PDFs and images are treated as visual concept sources, not authority.

## Top-level source coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`README.md`](../../README.md) | Early framework identity with known drift | HATHOR proposition, design principles, early-formation disclosure, Apache license pointer |
| [`LICENSE`](../../LICENSE) | Apache License 2.0 | Open-source rights and legal limitations; no trademark, warranty, support, or indemnity inference |
| [`AGENTS.md`](../../AGENTS.md) | Internal operating rule | Required environment-promotion path; internal-only policy detail |

## Business source coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`docs/business/INDEX.md`](../business/INDEX.md) | Derived draft index | Product relationship, source authority, maturity, claim classes |
| [`01-executive-overview.md`](../business/01-executive-overview.md) | Derived draft | Executive proposition, stakeholder value, v1 scope, risks, roadmap |
| [`02-business-requirements.md`](../business/02-business-requirements.md) | Derived draft | Buyer objectives, stakeholders, scope, requirements, acceptance, open decisions |
| [`03-business-capability-model.md`](../business/03-business-capability-model.md) | Derived draft | Capability model, differentiators, dependencies, maturity |
| [`04-operating-model.md`](../business/04-operating-model.md) | Derived draft | Authorities, roles, decision rights, workflows, records, policies |
| [`05-governance-risk-and-controls.md`](../business/05-governance-risk-and-controls.md) | Derived draft | Control layers, gates, threat boundary, risks, claim guidance |
| [`06-adoption-roadmap.md`](../business/06-adoption-roadmap.md) | Derived draft | Pilot phases, entry/exit evidence, checkpoints, stop conditions |
| [`07-value-and-success-measures.md`](../business/07-value-and-success-measures.md) | Derived draft | Control, outcome, economic, and decision measures |
| [`08-glossary-and-source-register.md`](../business/08-glossary-and-source-register.md) | Derived draft source register | Terminology, source status, traceability, inconsistencies |

## Architecture control, requirements, and synthesis coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`docs/architect/INDEX.md`](../architect/INDEX.md) | Canonical corpus index | Product boundary, reading order, source status, implementation-authority rule |
| [`PENDING-EDITS.md`](../architect/PENDING-EDITS.md) | Live change-control register | Accepted amendments, pending sign-offs, open design and assurance gaps |
| [`HATHOR-REQ-CORE-001`](../architect/HATHOR-REQ-CORE-001-initial-requirements-20260911.md) | Draft, amended | Platform scope, actors, requirements, non-functional targets, exclusions |
| [`aegis-bot-taxonomy-requirements`](../architect/aegis-bot-taxonomy-requirements-20260911.md) | Draft | Bot families, anatomy, runtime and command contracts |
| [`HATHOR-ARCH-001`](../architect/HATHOR-ARCH-001-architecture-mermaid-20260911.md) | Draft visual companion | Logical architecture and lifecycle diagrams |
| [`HATHOR-ARCH-002`](../architect/aegis-arch-002-bot-unit-compendium-20260914.md) | Draft synthesis awaiting sign-off | Stakeholder bot model; not independent authority |
| [`HATHOR-CANON-010`](../architect/aegis-canon-001-registries-20260913.md) | Accepted canonical authority | Fifteen gates, refusal/event/linter registries, 26-bot roster, identifiers |
| [`HATHOR-CANON-011`](../architect/aegis-canon-002-platform-principles-20260914.md) | Proposed, awaiting sign-off | Platform-principle synthesis; not accepted doctrine |
| [`HATHOR-CANON-012`](../architect/aegis-canon-003-documentation-framework-20260915.md) | Proposed, awaiting sign-off | Documentation metadata, types, review, staleness, indexing, and docs-as-code model; not yet binding on this sales set |

## Architecture decision coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`HATHOR-ADR-001`](../architect/aegis-adr-001-target-command-tree-20260911.md) | Proposed, partly superseded | Historical taxonomy and InfraOS migration context |
| [`HATHOR-ADR-002`](../architect/aegis-adr-002-orchestration-coordination-model-20260913.md) | Accepted | Event-triggered central orchestration; Process decides, Proctor enforces |
| [`HATHOR-ADR-003`](../architect/aegis-adr-003-greenfield-command-surface-20260913.md) | Accepted | Greenfield `aegis`, nine domains, CLI/bot exit boundary, no-code maturity evidence |
| [`HATHOR-ADR-004`](../architect/aegis-adr-004-layout-state-residency-20260913.md) | Accepted | `.aegis` residency, project spool, macOS/Linux v1 |
| [`HATHOR-ADR-005`](../architect/aegis-adr-005-backup-ticketing-system-20260913.md) | Accepted | Minimal first-party backup work service direction |

## Architecture research and interface coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`HATHOR-RP-001`](../architect/aegis-rp-001-manifest-schema-v1-20260911.md) | Draft, amended | Definition schema, contracts, handshake, signing boundary |
| [`HATHOR-RP-002`](../architect/aegis-rp-002-registry-discovery-20260911.md) | Draft, amended | Local/Tower registry, verification state, trust TTL |
| [`HATHOR-RP-003`](../architect/aegis-rp-003-telemetry-transport-20260911.md) | Draft, amended | Spool-and-drain, at-least-once delivery, quotas, deduplication |
| [`HATHOR-RP-004`](../architect/aegis-rp-004-knowledge-promotion-20260911.md) | Draft | Draft-to-verified lifecycle, human review, dispute, aging |
| [`HATHOR-RP-005`](../architect/aegis-rp-005-hierarchy-consolidation-20260911.md) | Draft, amended | Six-level hierarchy and bounded resolution |
| [`HATHOR-RP-006`](../architect/aegis-rp-006-ticketing-plane-20260911.md) | Draft, amended | Canonical Ticket Contract, providers, backup, reconciliation |
| [`HATHOR-RP-007`](../architect/aegis-rp-007-continuous-validation-20260911.md) | Draft, partly superseded | Validation fabric, findings, assumptions, claims, evidence, latency |
| [`HATHOR-RP-008`](../architect/aegis-rp-008-microbot-launch-roster-20260912.md) | Draft, amended | Launch sequencing and canonical roster reconciliation |
| [`HATHOR-RP-009`](../architect/aegis-rp-009-orchestration-gateway-20260912.md) | Draft | Conducted run, sequence, graph, completion, resume |
| [`HATHOR-RP-010`](../architect/aegis-rp-010-tower-surface-20260913.md) | Accepted design | Tower registry, distribution, curators, identity, ingest, query |
| [`HATHOR-RP-011`](../architect/aegis-rp-011-operator-brokering-20260913.md) | Accepted design | Proxy default, scoped token exception, provider sessions and receipts |
| [`HATHOR-RP-012`](../architect/aegis-rp-012-knowledge-storage-retrieval-20260913.md) | Accepted design | Files as truth, FTS5/optional vectors, thresholds, status-honest retrieval |
| [`HATHOR-RP-013`](../architect/aegis-rp-013-threat-model-20260913.md) | Accepted design | Trust scope, signing standards, identity, integrity, hardening |
| [`HATHOR-RP-014`](../architect/aegis-rp-014-bot-unit-creation-operation-20260913.md) | Accepted design | Governance triad, state/memory, channels, lifecycle |

## Technical specification coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`HATHOR-TS-001`](../architect/aegis-ts-001-continuous-validation-implementation-20260911.md) | Draft | Go chassis, validation implementation, tests, performance targets |
| [`HATHOR-TS-002`](../architect/aegis-ts-002-orchestration-gateway-implementation-20260913.md) | Draft | Run ledger, conductor, admission, resume, reconciliation |
| [`HATHOR-TS-003`](../architect/aegis-ts-003-bot-unit-implementation-20260913.md) | Draft | Bundle, governance engine, effects, scaffold, memory enforcement |
| [`HATHOR-TS-004`](../architect/aegis-ts-004-dmz-integration-boundary-20260914.md) | Draft, blocked, awaiting decisions | Proposed policy DMZ, project rules, floors, profiles, conflict envelope; internal future concept only |

## Roadmap coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`HATHOR-PLAN-001`](../architect/aegis-plan-001-platform-roadmap-20260913.md) | Approved planning artifact | Eight workstreams, six milestones, dependencies, planning estimate |
| [`HATHOR-PLAN-002`](../architect/aegis-plan-002-cvs-p0-p2-roadmap-20260911.md) | Draft, amended | Detailed validation build sequence and exclusions |
| [`HATHOR-PLAN-003`](../architect/aegis-plan-003-gateway-validators-roadmap-20260913.md) | Approved planning artifact | Gateway, validators, and bounded skill-pack sequence |

## Research baseline and narrative coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`AEGIS CLI Research Report`](../architect/AEGIS-CLI-Research-Report-2026-09-11.md) | Historical/current baseline, annotated | Verified InfraOS 9.3.0 capabilities, gaps, target rationale |
| [`Invocation Inventory`](../architect/01-Invocation-Inventory-Top30-2026-09-11.md) | One-machine baseline | 378 history matches and top-30 use discovery; not fleet evidence |
| [`CLI Spec Scoring`](../architect/02-CLI-Spec-Scoring-2026-09-11.md) | Baseline | Provisional 5.7/16 interface score and improvement need |
| [`Schema/Runbook Spike`](../architect/04-Spike-Schema-Runbook-Checklist-2026-09-11.md) | Spike design | Bounded discovery and runbook/checklist learning |
| [`Token Benchmark`](../architect/05-Token-Benchmark-CLI-vs-MCP-2026-09-11.md) | Limited baseline | Bounded-context evidence with n=1 and non-equivalent-path limits |
| [`Ticketing Economy Whitepaper`](../architect/aegis-ticketing-economy-whitepaper-20260911.md) | Draft, annotated | Ticket-as-authorization narrative and pilot hypothesis |
| [`Containerization Article`](../architect/aegis-containerization-article-20260911.md) | Draft, annotated | Container classes, build gates, human promotion, reference deployment |
| [`Containerization Presentation`](../architect/aegis-containerization-presentation-script-20260911.md) | Draft, annotated | Presentation narrative; not independent authority |

## Session-record coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`Corpus Refactor Session Log`](../architect/sessions/2026-09-13-corpus-refactor-session-log.md) | Historical session record | Documentation process and decision timeline; not product evidence |
| [`Corpus Refactor Summary`](../architect/sessions/2026-09-13-corpus-refactor-summary-report.md) | Historical summary | Corpus consolidation and sign-off process; later register supersedes closure claim |

## Developer-guide coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`docs/developers/INDEX.md`](../developers/INDEX.md) | Role-oriented target guide | Audiences and concise architecture principles |
| [`bot-developer.md`](../developers/bot-developer.md) | Normative target guide | Seven-block bot anatomy, statelessness, brokered effects, Class C target |
| [`agent-integrator.md`](../developers/agent-integrator.md) | Normative target guide | CLI, project layout, work, knowledge, dry-run, refusal, promotion policy |
| [`platform-engineer.md`](../developers/platform-engineer.md) | Normative target guide | Greenfield implementation, Go, orchestration, four validation layers, Tower |
| [`devops-dvo.md`](../developers/devops-dvo.md) | Normative target guide | Containers, EKS direction, staged promotion, spool-and-drain, offline trust |

## Visual and PDF coverage

| Source | Status/use | Sales contribution |
|---|---|---|
| [`docs/architect/AEGIS.pdf`](../architect/AEGIS.pdf) | Known-defective image-only board export | Legacy concept coverage; clipped and unsuitable as authority or external collateral |
| [`lib/AEGIS Overview.pdf`](../../lib/AEGIS%20Overview.pdf) | Untracked image-only overview at review time | More complete internal poster; target concepts only |
| [`lib/assets/AEGIS Overview.pdf`](../../lib/assets/AEGIS%20Overview.pdf) | Tracked image-only overview asset | Internal overview poster; target concepts only |
| [`00-outline-agent-anatomy-taxonomy.png`](../architect/images/00-outline-agent-anatomy-taxonomy.png) | Legacy visual | CLI, hierarchy, connection broker, observation concept |
| [`01-outline-universal-project-layout.png`](../architect/images/01-outline-universal-project-layout.png) | Legacy visual | Framework, project layout, knowledge, security concept |
| [`02-outline-universal-project-layout-detailed.png`](../architect/images/02-outline-universal-project-layout-detailed.png) | Legacy visual | Detailed version of the same concept; not canonical text |
| [`03-outline-micro-bot-architecture.png`](../architect/images/03-outline-micro-bot-architecture.png) | Legacy visual | Microbot anatomy, hierarchy, connections, storage concept |

## Maintenance

When a source changes:

1. verify status and authority;
2. inspect the pending-edits register;
3. update affected sales statements;
4. preserve target versus implementation distinction;
5. add implementation or test evidence only with exact scope;
6. update content gaps and disclosure;
7. run link and source-coverage validation; and
8. obtain product, security, legal, and commercial approval as applicable.

## Final interpretation rule

If a sales statement does not reveal whether it is design, plan, implementation, test result, operating fact, or measured outcome, it is incomplete and must not be used.
