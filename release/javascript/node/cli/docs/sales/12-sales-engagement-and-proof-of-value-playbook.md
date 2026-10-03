---
id: HATHOR-GUIDE-026
title: Sales Engagement and Proof-of-Value Playbook
summary: Sell the right to evaluate a governance problem, not an unsupported production outcome.
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
# Sales Engagement and Proof-of-Value Playbook

- **Audience:** Internal sales, solutions, product, delivery, security, and executive sponsors
- **Disclosure:** Internal only
- **Maturity:** Engagement model for a design-stage platform

## Engagement principle

Sell the right to evaluate a governance problem, not an unsupported production outcome.

The engagement should progress from validated problem to architecture fit, evidence plan, bounded proof of value, and explicit expansion decision.

## Stage 1 — Qualify

### Objective

Confirm material problem, architecture relevance, maturity fit, ownership, and a plausible development-only evaluation.

### Activities

- conduct initial discovery;
- classify agent actions and environments;
- identify sources of authority;
- validate human decision boundaries;
- map work, credential, evidence, and knowledge pain;
- identify hard v1 conflicts;
- state maturity clearly; and
- identify the buying committee.

### Deliverable

One-page opportunity brief:

- buyer problem;
- affected workflows;
- current cost or exposure;
- target outcome;
- fit and anti-fit;
- stakeholders;
- maturity expectation;
- open decisions; and
- next step.

### Exit

Proceed only if the problem is material and the buyer accepts architecture/pilot discovery rather than a production promise.

## Stage 2 — Architecture and control workshop

### Objective

Map the buyer’s environment to HATHOR authority and control boundaries.

### Participants

- executive or product sponsor;
- platform architecture;
- engineering;
- security or risk;
- identity;
- work-system owner;
- DevOps or release;
- knowledge owner if in scope; and
- solutions/product team.

### Agenda

1. Current agent workflows and future intent.
2. Systems of authority.
3. Work authorization and strategic linkage.
4. Completion and evidence.
5. Human-reserved actions.
6. Credential and provider effects.
7. Knowledge lifecycle.
8. Outage and recovery.
9. Threat and assurance requirements.
10. Operating ownership.
11. Pilot candidate and exclusions.

### Deliverables

- current-state architecture;
- target logical architecture;
- authority matrix;
- control objectives;
- integration inventory;
- open decision log;
- data and retention questions;
- proof criteria; and
- no-go conditions.

## Stage 3 — Baseline definition

### Objective

Create a credible comparison before product effects are introduced.

### Select

- one or two repositories;
- one repeatable workflow;
- one work provider;
- defined human, agent, or mixed execution modes;
- representative risk classes;
- a baseline window;
- accepted exclusions; and
- data-quality checks.

### Measure

- time to orient and first valid action;
- lead time and waiting;
- work and strategic linkage;
- evidence completeness;
- audit reconstruction time;
- validation time and rework;
- credential access paths;
- provider-effect records;
- knowledge search and review;
- outage behavior;
- tokens, retries, and external calls; and
- user and operator effort.

### Exit

Buyer and seller approve the baseline, limitations, and target ranges. No target should be reverse-engineered from an arbitrary marketing promise.

## Stage 4 — Solution and POV design

### Objective

Define the smallest implementation or simulation that can test the value and control hypotheses.

### Scope boundaries

- development only;
- no critical production dependency;
- no automatic promotion;
- no unsupported provider called “integrated”;
- no human-only action before identity is valid;
- no strong supply-chain claim before artifact binding;
- no complex graph before semantics are frozen; and
- no security promise beyond the agreed threat model.

### POV workstreams

1. **Foundation:** operational ingress, bounded context, schemas, records.
2. **Authorization:** work and strategic linkage.
3. **Validation:** selected low-ambiguity checks.
4. **Conducted run:** simple sequence and completion.
5. **Provider effect:** brokered test integration.
6. **Human boundary:** dry-run or implemented identity test.
7. **Knowledge:** representative query and draft/review flow.
8. **Recovery:** selected outage, expiry, and resume cases.
9. **Measurement:** scorecard and user feedback.

### POV design record

For each capability state:

- source status;
- implemented scope;
- authoritative records;
- positive tests;
- negative tests;
- recovery tests;
- residual risk;
- owner;
- evidence location; and
- sales claim unlocked by successful proof.

## Stage 5 — Execute proof of value

### Operating cadence

#### Kickoff

- confirm scope and exclusions;
- restate design-stage maturity;
- verify owners and access;
- freeze scorecard;
- review incident and rollback path; and
- confirm stop authority.

#### Weekly

- review findings and false refusals;
- review remediation effort;
- inspect shadow-path pressure;
- review failed and degraded states;
- track open security decisions;
- check data quality; and
- update risk and decision logs.

#### Control tests

- invalid work and missing linkage;
- invalid or revoked capability;
- missing evidence and false completion;
- out-of-order action;
- expired or wrong human authority;
- provider retry and ambiguous response;
- outage, trust expiry, and reconciliation;
- interrupted run and resume; and
- stale or disputed knowledge.

#### User research

- time to orient;
- clarity of refusal;
- usefulness of remediation;
- interruption to normal work;
- trust in knowledge and evidence;
- willingness to use governed path; and
- reasons for bypass.

## Stage 6 — Evaluate

### Control decision

Did every critical negative test refuse as expected? Were authoritative records durable? Did recovery avoid silent loss, overwrite, and duplicate effects in the tested scope?

### Usability decision

Were false refusal, latency, remediation, review load, and operator effort within agreed limits?

### Value decision

Did the selected measures improve relative to baseline after including full operating cost?

### Risk decision

Are identity, artifact, retention, provider, and threat-model residual risks accepted for the next scope?

### Outcome

- continue unchanged;
- continue with remediation;
- remain report-only;
- narrow scope;
- redesign;
- pause; or
- stop.

## Stage 7 — Expansion proposal

Expansion is a new decision, not automatic conversion.

For each new team, provider, environment, or capability:

- repeat fit assessment;
- update threat model;
- confirm authority and ownership;
- test provider semantics;
- establish baseline;
- validate recovery;
- review retention and privacy;
- set performance and friction thresholds; and
- require sponsor and risk approval.

Higher-environment promotion must follow:

`local → development → testing → staging → master (Production)`

PR source branches, deployment, and URL validation must comply with the organization’s promotion policy. Do not use this policy as a universal customer requirement.

## Mutual action plan template

| Milestone | Buyer owner | HATHOR owner | Evidence | Exit decision |
|---|---|---|---|---|
| Problem validated | Sponsor | Account lead | Opportunity brief | Workshop |
| Architecture mapped | Platform/security | Solutions | Authority and integration map | Baseline |
| Baseline approved | Product/value | Solutions | Reproducible baseline | POV design |
| Decisions frozen | Identity/security/platform | Product/engineering | Decision log | Build or simulate |
| POV ready | Pilot owner | Delivery | Test and rollback plan | Execute |
| Control tests complete | Control owner | Engineering | Test reports | Evaluate |
| Value review complete | Sponsor/finance | Account lead | Scorecard and cost | Continue/stop |
| Expansion approved | Sponsor/risk | Product/service owner | Readiness record | Next scope |

## POV scorecard

### Must-pass controls

- valid work authorization for all enforced mutations;
- complete acceptance-sample traceability;
- no successful reserved action without valid human proof;
- no successful revoked or invalid capability dispatch;
- no provider credential exposure to default worker path;
- no silent loss, overwrite, or duplicate effect in tested recovery;
- no false completion in defined negative cases; and
- correct knowledge status and provenance in sampled results.

### Buyer-set thresholds

- false-refusal rate;
- remediation time;
- orientation time;
- validation latency;
- lead time;
- review and curation effort;
- operator intervention;
- reconciliation age;
- adoption; and
- net value.

## Commercial handoff rules

The repository does not define price, license package, hosting service, support, SLA, warranty, or indemnity.

Before proposal:

- identify what is product, implementation, or advisory service;
- confirm license obligations;
- define accepted deliverables;
- separate roadmap from committed scope;
- state buyer dependencies;
- state exclusions and threat boundary;
- define support and acceptance;
- avoid fixed outcomes not under seller control; and
- route legal, security, and commercial language for approval.

## Required artifacts

Maintain:

- opportunity brief;
- discovery record;
- architecture and authority map;
- integration inventory;
- risk and decision register;
- baseline specification;
- POV plan;
- scorecard;
- test evidence;
- user feedback;
- weekly status;
- final evaluation; and
- approved claim updates.

## Deal review questions

1. Is the buyer problem validated or assumed?
2. Are we selling design, implementation, or an operating service?
3. Which claims have evidence?
4. Which requirements are outside v1?
5. Are human authority and artifact binding addressed?
6. Who owns service and controls?
7. Is the provider authoritative model accepted?
8. Is the pilot development-only?
9. Are baseline, thresholds, and stop conditions agreed?
10. Are commercial terms defined outside the repository?

## Sources

- [Discovery and Qualification](./09-discovery-and-qualification.md)
- [Adoption and Pilot Guide](./06-adoption-and-pilot-guide.md)
- [Value and Business Case](./07-value-and-business-case.md)
