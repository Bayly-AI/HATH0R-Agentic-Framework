---
id: HATHOR-GUIDE-028
title: Sales Glossary
summary: Sales Glossary
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
# Sales Glossary

- **Audience:** Sales, solutions, product marketing, executives, technical buyers, and documentation owners
- **Disclosure:** Internal reference; definitions may support approved collateral
- **Maturity:** Terminology aligned to the documentation baseline

## Product and category

| Term | Sales definition | Usage guidance |
|---|---|---|
| AEGIS | Proposed agentic governance and assurance platform that realizes HATHOR’s control-plane concerns | Do not call it implemented or production-ready without evidence |
| HATHOR | Broader agentic application framework for portable project structure, knowledge, governance, secure capability access, and attributable work | Do not use as a synonym for the full AEGIS platform |
| Governed agentic delivery | Delegating work to humans and AI agents while retaining authorization, evidence, strategic lineage, secure access, human decisions, and reconstructability | Preferred category outcome |
| Agentic governance | Policies, authority, evidence, identity, and controls applied to agent-assisted work | Avoid reducing it to prompt rules |
| Control plane | Coordination and governance layer that applies contracts and routes to authorities | Does not mean one centralized source of truth |
| Greenfield | New AEGIS implementation direction rather than a rename of InfraOS | Implies design/build work remains |
| InfraOS | Existing baseline system studied to inform AEGIS design and migration | Never present InfraOS runtime proof as AEGIS proof |

## Actors and platform components

| Term | Sales definition | Usage guidance |
|---|---|---|
| Actor | Human, AI agent, service, machine, or bot identity requesting or performing action | Identity type does not remove accountability |
| Agent | Model-backed or other AI worker using platform interfaces | Requests action; does not own platform authority |
| Bot or microbot | Single-purpose governed capability unit with a contract and lifecycle | Canonical design has 26 roles; not 26 proven implementations |
| Capability | Versioned intent used for routing independently of implementation name | Supports replaceability |
| `aegis` CLI | Accepted public operational ingress for supported humans and agents | It is a control surface, not every domain’s authority |
| Control Tower | Asynchronous authority for registration, trust/policy distribution, identity, revocation, ingest, and query | Not a bot, general workflow engine, or every request’s terminus |
| Proctor | Admission and routing authority that evaluates provenance, contract, sequence, and applicable gates | Proctor enforces but does not own run state |
| Process | Conductor and sole target writer of authoritative run transitions | Agents request; Process decides |
| Operator | Broker for supported third-party connections, credentials, sessions, and effects | Not a human operator in this specific component usage |
| Validator | Active checker that produces findings or refusal verdicts | Does not write authoritative plane state |
| Observation bot | Passive recorder or aggregator | Must not mutate or refuse work |
| Adapter | Non-autonomous provider translation module | Do not call every adapter a bot |
| DVO | Internal source term for a human deployment role or workflow | Prefer “authorized human deployment operator” externally |

## Authority

| Term | Sales definition | Usage guidance |
|---|---|---|
| Authority | Source permitted to decide a specific class of truth or transition | One ingress does not mean one authority |
| Registry Plane | Authority for which capability definitions may run | Does not authorize work |
| Knowledge Plane | Authority for knowledge record status, provenance, freshness, and verification | Does not authorize deployment |
| Ticketing Plane | Authority for which work exists and its provider-backed state | Does not authorize capabilities |
| Run ledger | Authoritative record of conducted-run events and reconstructed state | Distinct from telemetry |
| Human authority | Verified decision right reserved for a person | Applies to specified waiver, promotion, curation, or revocation |
| Provider authority | The selected enterprise system remains authoritative for its mapped records | Backup or cache does not become equal truth |
| System of record | Authoritative source for a defined domain | Avoid using loosely for every database |

## Work and orchestration

| Term | Sales definition | Usage guidance |
|---|---|---|
| Authorized work | Durable work item that permits an in-scope substantive action | Read-only orientation may be exempt by policy |
| Strategic linkage | Relationship from work item to business initiative or epic | Supports portfolio-to-outcome traceability |
| Ticket Contract | Provider-neutral target representation of work | Draft contract; not verified cross-provider conformance |
| Conducted run | Governed execution whose state and sequence are controlled by Process and admitted by Proctor | Preferred over “autonomous workflow” |
| Orchestration Gateway | Draft design for event-triggered evaluation, central state decision, and gateway enforcement | Not pure choreography |
| Information hierarchy | Procedure → Strategy → Playbook → Runbook → Workflow → Checklist | Provides lineage and required-work structure |
| Procedure | Business problem and required outcome | Root of hierarchy |
| Strategy | Selected direction under a procedure | One procedure may have alternatives |
| Playbook | Guidelines implementing a strategy | Governing guidance |
| Runbook | Concrete task set and execution entry point | Binds work to execution |
| Workflow | Scripts and tools that progress the runbook | Execution mechanism |
| Checklist | Step-level completion ledger | Evidence-bearing, not a cosmetic list |
| Process graph | Machine-readable required work, sequence, branches, and completion | Complex loop semantics remain open |
| Required set | Mandatory reachable work derived from the graph | Compared to execution at finalization |
| Executed set | Work and evidence recorded as completed | Actor claims alone are insufficient |
| Lawful skip | Explicit optional or non-selected branch recorded as skipped | Not omission of mandatory work |
| Fold | Deterministic reconstruction of run state from events | Supports resume and audit |
| Finalization | Controlled decision that required work and evidence are complete | Target behavior, not current proof |

## Validation and evidence

| Term | Sales definition | Usage guidance |
|---|---|---|
| Continuous Validation System | Draft target fabric for linters, validators, findings, assumptions, claims, evidence, and gates | Do not call it deployed |
| Validation fabric | Collective assurance components across build, change, dispatch, and runtime observation | Enforcement layer, not a fourth authority plane |
| Micro-linter | Pure, bounded structural check | Normally build/change time |
| Finding | Normalized validation result with severity, scope, evidence, and remediation | Supports actionable refusal |
| Claim | Actor assertion requiring mapped validation and evidence | Not accepted merely because an agent states it |
| Evidence | Recorded proof such as commands, exits, reports, digests, and receipts | Quality and freshness matter |
| Evidence ledger | Run-scoped record of validation proof | Authority depends on finalized contract |
| Assumption | Declared condition on which work depends | Can be open, broken, expired, or satisfied |
| Assumption ledger | Run-scoped assumption status and recheck record | Prevents hidden dependencies |
| Gate | Mechanical control that admits or refuses at a defined trigger | Canonical design has 15 gates |
| Refusal | Structured denial with code, explanation, remediation, provenance, and relevant timing | Preferred to opaque failure |
| Remediation | Next action required to resolve a refusal | Essential to usability |
| Evidence-backed completion | Completion evaluated from required work and current evidence | A value proposition and target control |

## Knowledge

| Term | Sales definition | Usage guidance |
|---|---|---|
| Knowledge tier | Project, machine, organization, or public source level | Search prefers nearer, verified context |
| Provenance | Origin, ownership, identity, and trace of a record | More than a URL |
| Draft knowledge | Authored content not yet human-verified | Must not be presented as authoritative |
| Verified knowledge | Content promoted by an authorized human with identity and time | Verification is scoped, not eternal truth |
| Microburst | One bounded knowledge record or patch | Technical/internal term; define before external use |
| TTL | Time after which trust or freshness must be reconsidered | Does not automatically delete data |
| Stale | Content older than its approved freshness window | Must not be silently presented as current |
| Disputed | Record challenged with evidence | Requires visible status and review |
| Superseded | Record replaced by a linked successor | Preserve lineage |
| Confidence threshold | Minimum retrieval score for a qualified result | Must be calibrated |
| No confident match | Honest outcome when retrieval quality is below threshold | Preferred over unqualified low-quality answer |
| Provenance over recency | Verified source and quality may outrank newer unverified content | Context-dependent retrieval principle |

## Security and integration

| Term | Sales definition | Usage guidance |
|---|---|---|
| Brokered external access | Provider interaction mediated by Operator | Preferred external description |
| Class 1 connection | Default proxied call; worker receives no provider credential | Strong credential-minimization path |
| Class 2 connection | Declared exception using a scoped, short-lived, run-bound, memory-only token | Reason not to say “zero secrets” |
| Idempotency key | Stable request identity used to limit duplicate effects | Does not guarantee universal exactly-once behavior |
| Provider receipt | Record of an external effect and its context/result | Needed for reconstruction |
| Capability provenance | Evidence of a capability definition’s identity, version, governance, and eligibility | Distinct from work authorization |
| Governance triad | Directive, rules, and principles bound to a bot definition | Accepted bot model |
| Directive | Bounded charter describing what a bot is for | Target budget is an internal detail |
| Rule | Constraint describing what a bot must not do | Narrowing-only; cannot grant permission |
| Principle | Decision heuristic used when rules are silent | Decisions should be observable |
| Configuration | Validated tuning outside signed governance | Must not relax policy |
| Revocation | Withdrawal of capability or trust eligibility | Requires distribution and quarantine behavior |
| Quarantine | State preventing a suspect definition from receiving new work | Preserve evidence and reason |
| Trust TTL | Period cached authority may support declared degraded operation | Expiry must not silently extend authority |
| Cooperative-but-fallible | v1 actor may drift, forget, reorder, hallucinate, or overclaim but not deliberately subvert platform files | Required security qualifier |
| Adversarial local process | Process with arbitrary workspace access | Outside v1 prevention guarantees |
| Artifact binding | Cryptographic linkage between definition and executable/image/attestation | Open prerequisite for strong supply-chain claims |
| Human token | Short-lived identity proof for a reserved action | Detailed contract remains open |

## Resilience and operations

| Term | Sales definition | Usage guidance |
|---|---|---|
| Degraded | Explicit reduced-assurance state with policy-bounded behavior | Not success and not always failure |
| Bounded offline trust | Cached signed authority usable only for permitted actions and time | Avoid “works offline indefinitely” |
| Buffered work | Work captured during provider outage and awaiting reconciliation | Not authoritative provider state |
| Reconciliation | Controlled comparison and replay to authority with explicit conflict handling | Authority wins; no silent overwrite |
| Spool-and-drain | Local append followed by asynchronous event delivery | Draft telemetry design |
| At-least-once delivery | Event may be retried and requires deduplication | Not exactly once |
| Recovery | Restoration and reconciliation after interruption | Must be tested by scenario |
| SLO | Measured service-level objective with ownership | Design latency target is not an SLO |
| Observability | Passive operational insight into health, latency, retry, cost, and failure | Must not become business-state authority |

## Project and deployment

| Term | Sales definition | Usage guidance |
|---|---|---|
| Universal Project Layout | Target predictable repository structure for humans and agents | Canonical details need README alignment |
| `.aegis/` | Target hidden metadata location for manifests, rules, state, and knowledge | Preferred over legacy folder references |
| Class A container | Target control-plane interface class | Technical diligence term |
| Class B container | Target stateful knowledge-service class | Technical diligence term |
| Class C container | Target stateless worker/bot-host class | Technical diligence term |
| Class D container | Target observation/telemetry class | Technical diligence term |
| Promotion | Controlled movement to a higher trust or environment state | Human authority applies to named promotions |
| Environment path | Local → development → testing → staging → master/Production | Organization-specific policy |

## Maturity and evidence

| Term | Sales definition | Usage guidance |
|---|---|---|
| Accepted design | Ratified architecture choice | Not implementation proof |
| Draft target | Requirement, research, architecture, or specification under review | Not commitment |
| Approved sequence | Planned order accepted for scheduling | Not code authorization |
| Proposed | Awaiting sign-off | Do not present as accepted |
| Defined | Outcome, authority, interface, and control intent documented | Strongest broadly evidenced AEGIS maturity |
| Implemented | Authorized code and configuration exist | Require version and scope |
| Verified | Positive, negative, recovery, and boundary tests pass | Require test evidence |
| Piloted | Real users and workloads operate in a bounded evaluation | Require baseline and pilot record |
| Operational | Ownership, SLOs, support, access, retention, and incidents are active | Require operating evidence |
| Scaled | Outcomes persist across multiple teams or providers | Require longitudinal evidence |
| Value hypothesis | Expected business effect requiring measurement | Do not present as benefit |
| Proof of value | Bounded evaluation of control, usability, risk, and value hypotheses | Not production rollout |
| Production-ready | Suitable for operational production use with evidence and ownership | Not supported by current corpus |

## Commercial and legal

| Term | Sales definition | Usage guidance |
|---|---|---|
| Apache License 2.0 | Repository license granting broad rights subject to conditions | Does not create support, warranty, trademark, or commercial terms |
| Open source | Source available under an open-source license | Confirm scope and notices with legal |
| Trademark | Product-name and brand right | Apache license does not grant it |
| Warranty | Contractual assurance about the product | Repository license is “AS IS” |
| Indemnity | Contractual allocation of third-party risk | Not provided by the repository |
| SLA | Contracted service level and remedy | Not defined |
| Pricing | Commercial charge and metric | Not defined |

## Preferred external vocabulary

Use:

- governed agentic delivery;
- bounded, evidence-backed automation;
- proposed governance and assurance platform;
- one operating contract with separate authorities;
- human-authorized promotion;
- brokered external access;
- status-honest knowledge;
- explicit degraded operation;
- target architecture;
- accepted design; and
- measured development pilot.

Avoid unexplained:

- MBI;
- TBR;
- AOG;
- CVS;
- DVO;
- Backup TS;
- microburst;
- fold;
- sovereign;
- Tower of Power;
- gate IDs;
- bot roster names; and
- internal milestone or decision IDs.

## Sources

- [Business Glossary and Source Register](../business/08-glossary-and-source-register.md)
- [Canonical Registries](../architect/aegis-canon-001-registries-20260913.md)
- [Claims and Evidence](./13-claims-evidence-and-source-coverage.md)
