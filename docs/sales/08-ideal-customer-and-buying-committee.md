---
id: AEGIS-GUIDE-022
title: Ideal Customer and Buying Committee
summary: The strongest prospective fit is an organization that is increasing AI-assisted software delivery and already feels a material gap between automation speed and its ability to preserve authorization, evidence, credenti...
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
# Ideal Customer and Buying Committee

- **Audience:** Internal sales, solutions, product marketing, partnerships, and leadership
- **Disclosure:** Internal only
- **Maturity:** Hypothesis derived from documented buyer problems and operating requirements

## Ideal-customer hypothesis

The strongest prospective fit is an organization that is increasing AI-assisted software delivery and already feels a material gap between automation speed and its ability to preserve authorization, evidence, credential control, human approvals, or audit reconstruction.

The corpus does not establish an industry, company-size, revenue, geography, or regulatory ICP. Do not invent firmographic thresholds. Qualify on operating conditions, risk, urgency, ownership, and willingness to run a measured pilot.

## Primary fit characteristics

### Agentic delivery is becoming operational

- Multiple teams or tools use AI agents for more than question answering.
- Agents create code, configuration, tickets, pull requests, knowledge, or provider effects.
- Leadership expects usage or autonomy to grow.
- Existing controls were designed around human-paced activity.

### Accountability is fragmented

- Work authorization, implementation, tests, approval, and deployment evidence live in different systems.
- Teams depend on chat or actor memory to explain what happened.
- Ticket, epic, branch, pull-request, and deployment linkage is incomplete.
- Audit or incident reconstruction requires manual evidence collection.

### High-risk actions must remain human

- The organization requires separation of duties.
- Production promotion, waiver, or knowledge approval cannot be delegated to an agent.
- Identity and approval context must be demonstrable.
- A risk or control owner is willing to define those boundaries.

### Provider access creates security pressure

- Agent workers use direct provider tokens or SDK credentials.
- Credentials are copied across environments or bot configurations.
- External effects are not consistently bound to intent and work.
- Retries, outages, and ambiguous results create reconciliation risk.

### Tool diversity makes governance inconsistent

- The buyer uses multiple agent harnesses, languages, repositories, or trackers.
- Governance is embedded in tool-specific wrappers or conventions.
- The buyer wants a stable operating contract without immediately replacing Jira, Azure DevOps, GitHub, source control, or CI/CD.

### Knowledge quality matters

- Agents repeatedly rediscover local context.
- Knowledge is stale, duplicated, unattributed, or difficult to distinguish from public material.
- The organization can assign human reviewers or curators.

### The buyer accepts evidence-led adoption

- Leadership will start in development.
- The team accepts baseline measurement and report-only learning.
- Security will participate in negative and recovery testing.
- Expansion depends on agreed thresholds rather than a predetermined rollout.

## Priority customer scenarios

| Scenario | Why AEGIS may fit | Entry motion |
|---|---|---|
| Regulated or high-assurance engineering | Authorization, evidence, separation of duties, reconstruction | Control-gap workshop and development-only pilot |
| Enterprise platform standardization | Many agent tools need a common contract | Architecture and operating-model assessment |
| Credential-risk reduction | Workers have direct access to external systems | Provider-effect and credential-path assessment |
| Audit-intensive delivery | Evidence assembly is slow or incomplete | Reconstruction baseline and evidence POV |
| Multi-tracker governance | Common policy must span Jira, ADO, or GitHub | Canonical work-contract fit assessment |
| Knowledge-intensive engineering | Agent orientation and trust are poor | Representative-query and curation pilot |
| Intermittent connectivity or dependency outages | Work leaves the ledger during failures | Bounded-continuity tabletop and recovery test |
| Modular agent platform | Buyer wants replaceable capabilities, not monolithic agents | Capability lifecycle and registry workshop |

## Anti-ICP and disqualification

The opportunity is not ready when:

- the buyer requires a production-proven product, certification, customer references, or contracted SLA now;
- the buyer wants unsupervised production action with no human promotion boundary;
- there is no durable work-authorization practice and no willingness to introduce one;
- the desired product is a foundation model, agent harness, issue tracker, or CI/CD replacement;
- the organization will not assign product, service, control, identity, work-system, and knowledge owners;
- there is no representative baseline or willingness to measure;
- routine bypass is considered acceptable operating practice;
- prevention against a malicious local process with arbitrary workspace access is a hard v1 requirement;
- the only buying criterion is near-term, guaranteed ROI;
- the buyer cannot support retention, privacy, and access decisions; or
- the pilot would create a critical production dependency.

## Buying committee

### Executive sponsor

**Mandate:** Fund the operating-model change, define business outcomes and risk appetite, and decide expansion.

**Cares about:**

- safe scale of AI-assisted work;
- accountability from strategy to outcome;
- measurable value;
- avoidance of uncontrolled autonomy; and
- ownership and organizational readiness.

**Likely objection:** “Why do we need a new layer?”

**Evidence needed:** Current-state fragmentation, control cost, pilot scope, stop conditions, and a value measurement plan.

### CIO or CTO

**Mandate:** Align AEGIS with enterprise architecture and engineering strategy.

**Cares about:**

- portability across models, harnesses, providers, and languages;
- integration with existing tools;
- long-term operating cost;
- modularity and migration; and
- platform ownership.

**Likely objection:** “Is this another orchestration platform?”

**Evidence needed:** Clear authority boundaries, complement-not-replace architecture, integration map, and phased roadmap.

### CISO or security architecture

**Mandate:** Approve trust assumptions, identity, credentials, provenance, and residual risk.

**Cares about:**

- cooperative versus adversarial threat scope;
- executable and image integrity;
- human identity and replay;
- provider credential custody;
- egress and external effects;
- evidence integrity; and
- revocation and incident response.

**Likely objection:** “Can a local agent bypass the controls?”

**Evidence needed:** Honest threat model, negative-test plan, artifact-binding decision, identity profile, and hardening roadmap.

### Risk, compliance, or audit

**Mandate:** Map platform evidence to organization-specific controls and determine assurance requirements.

**Cares about:**

- authorization;
- separation of duties;
- evidence retention;
- reconstructability;
- control ownership;
- exception governance; and
- independent assessment.

**Likely objection:** “Is this compliant?”

**Evidence needed:** Control mapping and operating evidence, not a generic compliance claim.

### VP Engineering or engineering leader

**Mandate:** Ensure the operating model improves delivery without unacceptable friction.

**Cares about:**

- orientation and lead time;
- validation cost;
- false refusals;
- remediation quality;
- developer adoption;
- reliability; and
- shadow workflows.

**Likely objection:** “Will this slow teams down?”

**Evidence needed:** Baseline, latency budgets, report-only findings, user effort, and bypass trend.

### Platform engineering

**Mandate:** Build or operate shared CLI, runtime, registry, validation, Tower, and integrations.

**Cares about:**

- interfaces and schemas;
- capability lifecycle;
- deployment and scaling;
- state ownership;
- provider adapters;
- HA, backup, and SLOs; and
- release and support.

**Likely objection:** “How much must we build and own?”

**Evidence needed:** Defined scope, interface freeze, ownership matrix, operating model, and total-cost estimate.

### DevOps or release management

**Mandate:** Govern environment promotion, deployment evidence, and recoverability.

**Cares about:**

- human authorization;
- CI/CD compatibility;
- container standards;
- secrets;
- environment progression;
- rollback and recovery; and
- telemetry.

**Likely objection:** “Does this replace our pipeline?”

**Evidence needed:** Complementary control points, deployment-ticket handoff, and stage-specific responsibilities.

### Identity and access management

**Mandate:** Define organization identity, token issuance, role claims, expiry, and revocation.

**Cares about:**

- OIDC or equivalent integration;
- action and audience binding;
- replay prevention;
- role and four-eyes policy; and
- audit.

**Likely objection:** “The token contract is not complete.”

**Evidence needed:** Agreement that identity is a pre-enforcement design decision, not a hidden dependency.

### Work-system owner

**Mandate:** Preserve tracker authority and approve adapter and reconciliation behavior.

**Cares about:**

- provider-native semantics;
- rate limits;
- fields and workflows;
- outage behavior;
- conflicts; and
- migration impact.

**Likely objection:** “Will AEGIS become another tracker?”

**Evidence needed:** Authority-wins model, minimal backup scope, and canonical contract mapping.

### Knowledge owner or curator lead

**Mandate:** Define reviewer authority, quality, staleness, conflict, and retention.

**Cares about:**

- provenance;
- review workload;
- confidence and misses;
- secrets and sensitive content;
- dispute; and
- lifecycle.

**Likely objection:** “Will human review become a bottleneck?”

**Evidence needed:** Queue, review effort, SLA, quality, and stop criteria in the pilot.

### Finance or value owner

**Mandate:** Validate total cost and realized benefit.

**Cares about:**

- full implementation and operating cost;
- credible baseline;
- attributable benefit;
- risk valuation;
- ongoing curation and support; and
- decision thresholds.

**Likely objection:** “Where is the ROI?”

**Evidence needed:** Measurement plan; never present roadmap hours or output volume as ROI.

### Developers and agent integrators

**Role:** Daily users and critical adoption stakeholders.

**Cares about:**

- predictable commands;
- bounded context;
- useful errors;
- low latency;
- no duplicate work;
- local operation; and
- clear human handoffs.

**Likely objection:** “This is governance overhead.”

**Evidence needed:** Report-only feedback, remediation success, orientation comparison, and workflow fit.

## Champion profile

The best champion:

- owns or influences developer-platform strategy;
- has a documented governance or evidence problem;
- can convene engineering and security;
- accepts design-stage transparency;
- can secure a development-only pilot;
- is willing to baseline current work;
- values control and usability together; and
- will stop or redesign rather than force rollout.

## Required coalition

Do not advance to an enforced POV with only one enthusiastic technical user. At minimum secure:

- executive or budget sponsorship;
- platform and engineering participation;
- security or risk review;
- work-system ownership;
- identity participation before human-only controls;
- a knowledge reviewer if knowledge is in scope; and
- a pilot team owner.

## Sources

- [Business Stakeholders and Requirements](../business/02-business-requirements.md)
- [Target Operating Model](../business/04-operating-model.md)
- [Buyer Problems and Use Cases](./02-buyer-problems-and-use-cases.md)
