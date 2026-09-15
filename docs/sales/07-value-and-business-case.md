---
id: AEGIS-GUIDE-021
title: Value and Business Case
summary: 'AEGIS should be evaluated as both:'
doc_type: GUIDE
diataxis: explanation
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
# Value and Business Case

- **Audience:** Executive sponsor, finance, product, platform, engineering, security, and operations
- **Disclosure:** Buyer-facing value framework; contains no validated ROI claim
- **Maturity:** Value hypotheses and measurement design

## Value position

AEGIS should be evaluated as both:

1. a governance and assurance capability that must prove its controls work; and
2. a business investment that must prove the value of improved control exceeds implementation, operating, and user cost.

Documents, features, commands, tickets, and telemetry volume are not value by themselves.

## Value hypotheses

| Hypothesis | Expected effect | Evidence required |
|---|---|---|
| One governed interface improves accountability | More work has complete authorization, actor, evidence, and outcome linkage | Pre/post coverage and reconstruction |
| System-evaluated completion improves assurance | Fewer unsupported claims and skipped mandatory steps | Negative tests, completeness gaps, escaped defects |
| Brokered integration reduces credential exposure | Fewer worker-held credentials and untracked effects | Runtime inspection and effect receipts |
| Human-only promotion improves release control | Fewer unauthorized reserved actions | Identity coverage and adversarial negative tests |
| Provider-neutral work lowers governance coupling | Policy remains consistent across selected providers | Cross-provider conformance and migration effort |
| Bounded outage handling improves continuity | Less untracked work and fewer lost or duplicate effects | Outage, conflict, replay, and expiry exercises |
| Governed knowledge reduces rediscovery | Faster orientation and greater verified reuse | Search, reuse, staleness, and review measures |
| Proportionate validation catches issues earlier | Earlier findings without excessive delay | Finding timing, rework, false refusal, and latency |
| Modular capabilities reduce blast radius | Components can be changed or retired independently | Isolation and replacement tests |
| Per-run observation improves cost control | Token, retry, latency, and failure anomalies become actionable | Cost records and completed optimization actions |

Each remains a hypothesis until a credible comparison is completed.

## Baseline principles

1. Select representative repositories and workflows.
2. Compare equivalent task and risk classes.
3. Segment human, agent, and mixed execution.
4. Separate active work, waiting, review, and remediation time.
5. Use authoritative work, run, identity, and provider records for business facts.
6. Use telemetry for correlation, not as the only authority.
7. Measure false refusal and user effort alongside control coverage.
8. Report confounders such as model, staffing, process, and workload changes.
9. Do not infer fleet behavior from the existing one-machine sample.
10. Do not infer CLI superiority from the existing non-equivalent payload baseline.

## Control value measures

### Authorization and accountability

- work authorization coverage;
- strategic epic linkage;
- branch and pull-request binding;
- end-to-end traceability;
- audit reconstruction success; and
- analyst time to reconstruct.

### Completion and validation

- evidence-backed completion;
- false-completion prevention;
- completeness gaps;
- claim-to-validation compliance;
- broken-assumption exposure;
- validation false-refusal rate; and
- remediation without bypass.

### Human authority

- reserved actions with valid human proof;
- unauthorized reserved-action success;
- waiver rate and expiry;
- self-approval where four-eyes applies; and
- approval effort and delay.

### Capability trust

- verified dispatch coverage;
- revoked dispatch attempts;
- signature and rollback negative tests;
- executable-binding coverage; and
- isolation during quarantine.

### Credential and external effects

- provider credential exposure to workers;
- persisted long-lived secrets;
- complete effect receipts;
- duplicate effects during retry or resume;
- scoped token-exception use; and
- retry and circuit-policy violations.

### Knowledge

- verified records with reviewer identity;
- machine self-verification attempts;
- metadata completeness;
- sensitive-content failures;
- status-honest retrieval; and
- stale or disputed content presented as current.

### Continuity

- work loss during provider outage;
- buffered work beyond TTL;
- reconciliation conflict age;
- silent overwrite;
- resume duplication;
- observation loss within tested capacity;
- rollup double counting; and
- action success after trust expiry.

## Business outcome measures

The source does not provide validated baselines or targets. The buyer should set them after baseline.

| Outcome | Business question |
|---|---|
| Time to orient | Does a standard layout and bounded context reduce rediscovery? |
| Change lead time | Does governance remove or add net delay? |
| Rework | Are issues found earlier? |
| Escaped defects or failed changes | Does evidence-backed execution improve quality? |
| Manual evidence effort | Is review or audit reconstruction faster? |
| Unauthorized change | Are prohibited actions reduced? |
| Credential incidents | Does brokering reduce exposure? |
| Knowledge success and reuse | Do users find and trust relevant material faster? |
| Knowledge review load | Is curation sustainable? |
| Outage productivity and recovery | Does bounded buffering improve continuity? |
| User effort and satisfaction | Are refusals understandable and workflows usable? |
| Adoption | Do governed paths become normal behavior? |
| Component replacement time | Does modularity reduce change effort? |
| Incident investigation time | Does joined evidence improve response? |

## Cost model

Include all relevant costs:

- engineering implementation;
- product and program management;
- architecture, security, and control design;
- identity and provider integration;
- infrastructure and storage;
- model and token use;
- validation compute;
- knowledge curation;
- support and incident response;
- training and change management;
- audit and control testing;
- user waiting and remediation;
- migration and deprecation; and
- ongoing evidence, access, and retention operations.

The roadmap’s engineering hours do not cover every category.

## Benefit model

Measure only evidenced benefit:

- avoided manual evidence collection;
- reduced rework;
- reduced failed-change cost;
- reduced credential incident response;
- reduced untracked-work recovery;
- reduced provider migration effort;
- reduced orientation and onboarding effort;
- avoided duplicate external effects;
- continuity value during outages; and
- increased safe throughput at equal or lower risk.

Do not count gross agent output, generated tokens, ticket volume, or prevented test cases as realized business benefit.

## Value equation

Use the buyer’s approved financial method:

`net value = evidenced avoided cost + evidenced capacity value + risk-adjusted loss reduction - implementation and operating cost`

For risk-adjusted benefit, require an approved probability and impact model. Do not monetize hypothetical control failures informally.

## Existing research evidence

The source corpus includes narrow baseline observations:

- 378 local invocation-history matches from one repository and one developer machine;
- concentration in Operator- and Process-style activity;
- limited hierarchy use in that sample;
- one readiness pack around 1,525 output tokens and 2.7 seconds;
- one full inventory around 41,000 tokens, approximately 27 times heavier in that run;
- a provisional top-30 CLI Spec average of 5.7/16; and
- a single-run CLI/MCP payload study with rough token estimation, non-equivalent paths, and an unhealthy knowledge path.

This evidence supports further investigation into bounded context and interface design. It does not prove:

- enterprise demand;
- fleet usage patterns;
- general CLI-versus-MCP superiority;
- production reliability;
- cost savings;
- customer willingness to adopt; or
- ROI.

## Business-case template

### 1. Current-state cost and exposure

- number and class of agent-assisted workflows;
- manual linkage and evidence effort;
- rework and failed-change cost;
- credential paths and incidents;
- audit and incident reconstruction time;
- provider outage impact;
- knowledge rediscovery and curation effort; and
- existing platform and control cost.

### 2. Target scope

- teams and repositories;
- task and risk classes;
- work provider;
- identity and deployment boundary;
- knowledge tiers;
- enabled control profile;
- required integrations; and
- excluded environments.

### 3. Investment

- foundation and integration;
- pilot and change management;
- security and control validation;
- service operation;
- curation and support; and
- risk contingency.

### 4. Benefit assumptions

For every benefit, state:

- baseline;
- proposed mechanism;
- target range;
- data source;
- owner;
- confidence;
- confounders; and
- validation date.

### 5. Decision thresholds

At minimum:

- no successful critical negative test;
- complete human authorization for reserved actions;
- complete traceability for the acceptance sample;
- no silent loss, overwrite, or duplicate effect in tested recovery;
- acceptable false refusal and latency;
- ready owners and incident paths;
- approved retention and privacy;
- no shift to shadow workflows; and
- credible value after full operating cost.

## Reporting views

### Executive

- safe throughput;
- traceability and human-authority coverage;
- quality and incident trend;
- audit effort;
- total cost and evidenced benefit;
- adoption and bypass; and
- top residual risks.

### Product and platform

- orientation and task success;
- lead time;
- false refusal and remediation;
- capability availability and replacement;
- schema and documentation drift;
- provider and knowledge usage; and
- roadmap acceptance.

### Risk and control

- gate outcomes;
- waiver and identity failures;
- provenance and revocation;
- credential findings;
- completion gaps;
- duplicate external effects;
- degradation and expiry;
- reconciliation conflict; and
- control-test status.

### Operations

- health and latency;
- retries and circuit behavior;
- spool and ingest lag;
- run resume;
- storage and retention;
- token and validation cost; and
- incidents and SLOs.

## Decision rule

AEGIS creates value only if:

- accountability and assurance improve;
- human authority remains verifiable;
- credential and provider effects are more controlled;
- continuity improves without hidden authority;
- friction stays inside agreed limits;
- quality or risk-adjusted throughput improves;
- full operating cost is included; and
- every claim remains inside the available evidence.

## Sources

- [Value and Success Measures](../business/07-value-and-success-measures.md)
- [Executive Overview](../business/01-executive-overview.md)
- [Token Benchmark](../architect/05-Token-Benchmark-CLI-vs-MCP-2026-09-11.md)
- [Invocation Inventory](../architect/01-Invocation-Inventory-Top30-2026-09-11.md)
