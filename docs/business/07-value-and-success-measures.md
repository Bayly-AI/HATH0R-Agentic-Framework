---
id: AEGIS-GUIDE-009
title: AEGIS Value and Success Measures
summary: CTL-*` and `VAL-*` labels are local measurement aids. They do not add canonical AEGIS identifiers or alter source acceptance criteria.
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
# AEGIS Value and Success Measures

- **Business document:** 07 of 08
- **Status:** Derived draft for business review
- **Source baseline:** Architecture corpus as of 2026-09-14
- **Purpose:** Separate control effectiveness, operational performance, adoption, and business value into measurable outcomes

`CTL-*` and `VAL-*` labels are local measurement aids. They do not add canonical AEGIS identifiers or alter source acceptance criteria.

## 1. Measurement objective

AEGIS should be evaluated as both:

1. a **governance and assurance capability**, which must prove that its controls work; and
2. a **business investment**, which must prove that improved control does not cost more than the value it creates.

Feature completion, document approval, command volume, ticket count, and telemetry volume are not measures of value by themselves.

## 2. Measurement principles

1. Establish a representative baseline before enforcement.
2. Compare equivalent tasks and risk classes.
3. Segment human, agent, and mixed execution.
4. Separate target design, test result, pilot result, and operational result.
5. Use authoritative work, run, identity, and provider records for business facts.
6. Use telemetry for correlated operational analysis, not as the sole source of truth.
7. Measure friction and false refusal alongside control coverage.
8. Do not treat the source `50%` ticket-sizing convention as measured productivity savings.
9. Do not infer fleet behavior from the one-machine invocation inventory.
10. Do not infer CLI superiority from the current non-equivalent, single-run payload baseline.
11. Report trust-model and data-quality limitations with every assurance result.
12. Expand adoption only when value and control measures pass together.

## 3. Value hypotheses

| Hypothesis | Expected effect | Evidence needed |
|---|---|---|
| One governed interface improves accountability | More work has complete authorization, actor, evidence, and outcome linkage | Pre/post traceability coverage and reconstruction samples |
| System-evaluated completion improves assurance | Fewer unsupported completion claims and skipped mandatory steps | False-completion tests, completeness gaps, escaped defects |
| Brokered integration reduces credential exposure | Fewer worker-held credentials and untracked provider effects | Process inspection, secret findings, complete effect receipts |
| Human-only promotion improves release control | Fewer unapproved high-risk actions | Human-token coverage and unauthorized-promotion attempts |
| Provider-neutral work reduces process lock-in | Equivalent policy works across supported trackers | Cross-provider conformance and migration effort |
| Bounded outage handling improves continuity | Less untracked work and fewer duplicate or lost effects during provider failure | Outage, buffer, reconciliation, conflict, and replay measures |
| Governed knowledge reduces rediscovery | Faster orientation and more reuse of verified local knowledge | Search success, reuse, staleness, reviewer effort, orientation time |
| Proportional validation reduces late rework without excessive drag | Earlier defects with acceptable latency | Finding timing, rework, lead time, false refusals, suite duration |
| Modular bots reduce change blast radius | Components can evolve or retire independently | Isolation, replacement time, stale-binding, and successor tests |
| Observation improves cost control | Token, retry, latency, and failure anomalies become actionable | Per-run cost data and completed optimization actions |

These remain hypotheses until a pilot establishes causal or credible comparative evidence.

## 4. Control-effectiveness measures

### 4.1 Authorization and accountability

| ID | Measure | Definition | Target for enforced scope | Primary source |
|---|---|---|---|---|
| CTL-A01 | Work authorization coverage | In-scope substantive mutations with a valid authorizing ticket ÷ all in-scope substantive mutations | 100% | Ticketing Plane plus audit ledger |
| CTL-A02 | Strategic-linkage coverage | In-scope tickets with a valid epic ÷ in-scope tickets advanced past readiness | 100% | Ticketing Plane |
| CTL-A03 | Change-binding coverage | In-scope branches and PRs correctly linked to their ticket ÷ all in-scope branches and PRs | 100% | Ticketing provider and repository metadata |
| CTL-A04 | End-to-end traceability | Sampled outcomes that traverse epic → ticket → actor → run → hierarchy → evidence → outcome | 100% of accepted sample | Joined authoritative records |
| CTL-A05 | Audit reconstruction success | Sampled mutations reconstructed without actor testimony ÷ sampled mutations | 100% for acceptance sample | Run/audit ledgers and provider receipts |
| CTL-A06 | Reconstruction time | Elapsed analyst time to produce the approved evidence package | Baseline, then stakeholder target | Audit exercise |

### 4.2 Completion and validation

| ID | Measure | Definition | Target for enforced scope | Primary source |
|---|---|---|---|---|
| CTL-C01 | Evidence-backed completion | Completed required nodes with current required evidence ÷ all completed required nodes | 100% | Run and evidence ledgers |
| CTL-C02 | False-completion prevention | Negative test cases correctly refused ÷ all false-completion cases | 100% in release testing | Control test suite |
| CTL-C03 | Completeness-gap rate | Runs refused at finalize for missing mandatory work ÷ finalized attempts | Observe trend; investigate recurring classes | Findings and run ledger |
| CTL-C04 | Claim-tier compliance | Claims with required suite tier and evidence ÷ all claims | 100% in enforced scope | Claim and evidence ledgers |
| CTL-C05 | Broken-assumption exposure | Actions attempted while a bound assumption is open, broken, or expired | Zero successful prohibited actions | Assumption and refusal records |
| CTL-C06 | Validation false-refusal rate | Legitimate actions incorrectly blocked ÷ all blocked actions reviewed | Baseline then agreed ceiling | Finding review and user appeal |
| CTL-C07 | Remediation success | Refusals resolved without bypass ÷ reviewed legitimate refusals | Baseline then improve | Refusal and resubmission records |

### 4.3 Human authority

| ID | Measure | Definition | Target | Primary source |
|---|---|---|---|---|
| CTL-H01 | Verified human-action coverage | Reserved actions with valid action-bound human identity ÷ all reserved actions | 100% | Tower identity and audit records |
| CTL-H02 | Unauthorized reserved-action success | Agent, expired, replayed, wrong-audience, or wrong-action attempts that succeed | 0 | Negative tests and audit |
| CTL-H03 | Waiver rate | Waived blocking controls ÷ blocking control events | No source target; threshold set by risk owner | Waiver and finding records |
| CTL-H04 | Waiver expiry compliance | Waivers still effective after expiry | 0 | Run and policy evaluation |
| CTL-H05 | Self-approval incidence | High-risk actions approved by the same identity where four-eyes policy applies | 0 once policy is adopted | Identity and approval records |

### 4.4 Capability and supply-chain trust

| ID | Measure | Definition | Target | Primary source |
|---|---|---|---|---|
| CTL-P01 | Verified dispatch coverage | Dispatches resolved to a currently eligible registry entry ÷ all successful dispatches | 100% | Proctor and registry records |
| CTL-P02 | Post-reconcile revoked dispatch | Successful dispatch to a revoked component after reconciliation | 0 | MBI/TBR and run records |
| CTL-P03 | Signature negative-test pass rate | Tampered, stale, unknown-key, or rollback inputs correctly refused | 100% | Registration and distribution tests |
| CTL-P04 | Executable binding coverage | Registered components whose runtime bytes or attestation are bound to the signed definition | Target set after R10 decision; required for strong assurance | Manifest and attestation |
| CTL-P05 | Independent component recovery | Quarantine or failure tests that leave unrelated siblings available | 100% for defined isolation cases | Resilience tests |

### 4.5 Credential and external-effect control

| ID | Measure | Definition | Target | Primary source |
|---|---|---|---|---|
| CTL-E01 | Class-1 worker credential exposure | Class-1 worker processes receiving provider credential material | 0 | Runtime inspection and tests |
| CTL-E02 | Long-lived worker secret persistence | Long-lived provider secrets found in worker config, logs, files, knowledge, or images | 0 | Linters, scans, incident records |
| CTL-E03 | External-effect receipt coverage | Provider mutations with actor, capability, run, ticket, connection, and idempotency receipt ÷ all governed provider mutations | 100% | Operator and provider records |
| CTL-E04 | Replay duplicate effects | Duplicate provider effects created by retry or resume | 0 in acceptance and incident samples | Fault injection and provider data |
| CTL-E05 | Class-2 exception usage | Token-handoff sessions by provider, capability, reason, and TTL | Observe; each use must be declared and audited | Operator sessions |
| CTL-E06 | Circuit and retry containment | Calls exceeding provider rate, breaker, or five-retry policy | 0 successful policy violations | Operator and retry records |

### 4.6 Knowledge control

| ID | Measure | Definition | Target | Primary source |
|---|---|---|---|---|
| CTL-K01 | Human-verified knowledge coverage | Verified records with reviewer identity and time ÷ all verified records | 100% | Knowledge records |
| CTL-K02 | Bot-self-verified records | Verified records created without authorized human promotion | 0 | Knowledge records |
| CTL-K03 | Metadata completeness | New records with required provenance, TTL, title, breadcrumb, hierarchy, and status | 100% | Knowledge write validation |
| CTL-K04 | Secret-bearing promoted records | Records promoted despite secret/PII control failure | 0 | Promotion tests and incidents |
| CTL-K05 | Status-honest retrieval | Results exposing correct status, freshness, tier, and confidence ÷ sampled results | 100% | Retrieval evaluation |
| CTL-K06 | Stale-as-current errors | Stale, disputed, archived, or external content silently represented as current verified truth | 0 | Retrieval evaluation and incidents |

### 4.7 Continuity and evidence durability

| ID | Measure | Definition | Target | Primary source |
|---|---|---|---|---|
| CTL-R01 | Work lost during provider outage | Authorized work items not recoverable after tested outage | 0 in tested capacity and trust bounds | Backup/provider reconciliation |
| CTL-R02 | Buffered work past TTL | Buffered items older than approved trust TTL without refusal or escalation | 0 | Ticket status and reconciliation |
| CTL-R03 | Reconciliation conflict age | Time from conflict detection to authorized resolution | Target set by service owner | Ticket and incident records |
| CTL-R04 | Silent overwrite | Reconciliation conflicts that replace data without an explicit conflict record | 0 | Fault injection and audit |
| CTL-R05 | Run resume duplication | Completed nodes or external effects repeated after resume | 0 in acceptance tests | Run and provider records |
| CTL-R06 | Telemetry loss under reference outage | Events lost during the specified 24-hour Observation outage with sufficient quota | 0 | Spool and replay test |
| CTL-R07 | Rollup double counting | Aggregate changes when the same batch is replayed | 0 | Tower ingest test |
| CTL-R08 | Expired-trust action success | Authority-originating actions that succeed after trust TTL expiry | 0 | Offline/expiry tests |

## 5. Architecture performance targets

These are source acceptance targets, not observed production SLOs.

| Measure | Source target |
|---|---|
| Cheap command or bot health latency | Under 250 ms in steady state |
| Default agent orientation output | At most 2,500 output tokens |
| Agent skill pack | Approximately 800 tokens in the approved plan |
| Default schema page | At most 8 KB |
| Full hierarchy resolution | At most three CLI round-trip waves |
| Transient retry | No more than five attempts with backoff |
| Validation L0 | At most 50 ms |
| Validation L1 | At most 2 seconds |
| Validation L2 | At most 30 seconds |
| Validation L3 | At most 10 minutes |
| Validation L4 | Asynchronous |
| Post-v1 top-30 CLI Spec score | At least 12/16 |

Operational SLOs must be defined separately after measured pilot behavior.

## 6. Business-outcome measures

The architecture does not set baselines or targets for these measures. The pilot must do so.

| ID | Outcome measure | Why it matters | Segmentation |
|---|---|---|---|
| VAL-01 | Time to orient to a repository and first valid action | Tests whether standard structure and bounded guidance reduce rediscovery | New/experienced user; human/agent; repository type |
| VAL-02 | Change lead time | Tests whether governance adds or removes end-to-end delay | Risk class; human/agent/mixed; wait vs active time |
| VAL-03 | Rework rate | Tests whether early validation reduces repeated or discarded work | Finding class; lifecycle stage detected |
| VAL-04 | Escaped-defect or failed-change rate | Tests whether evidence and controls improve delivered quality | Severity; environment; workflow |
| VAL-05 | Manual evidence-gathering effort | Tests whether reconstruction reduces audit and review labor | Review type; project; time period |
| VAL-06 | Unauthorized-change incidence | Tests whether work and human-authority controls reduce exposure | Attempted vs successful; actor; environment |
| VAL-07 | Credential-exposure incidents | Tests whether brokering reduces secret distribution risk | Provider; path; severity |
| VAL-08 | Knowledge search success and reuse | Tests whether governed knowledge reduces repeated research | Tier; topic; confidence; status |
| VAL-09 | Knowledge review effort and queue age | Tests whether governance creates a sustainable curation load | Tier; curator; topic |
| VAL-10 | Provider-outage productivity and recovery | Tests whether buffering improves continuity without weakening authority | Provider; outage duration; conflict count |
| VAL-11 | User effort and satisfaction | Detects policy friction, confusing refusals, and shadow-path pressure | Role; team; control class |
| VAL-12 | Automation adoption | Shows whether governed paths become normal behavior | Eligible users, repos, tasks, and active usage |
| VAL-13 | Time to replace or retire a component | Tests the modularity proposition | Component class; breaking/non-breaking |
| VAL-14 | Incident investigation time | Tests whether evidence reduces time to understand cause and authority | Incident severity and evidence completeness |

## 7. Economic measures

### 7.1 Cost categories

Measure:

- engineering implementation;
- product and program management;
- security, architecture, and control design;
- provider and identity integration;
- infrastructure and storage;
- model and token consumption;
- validation compute;
- knowledge curation;
- operational support and incident response;
- training and change management;
- audit and control testing; and
- user delay caused by controls.

### 7.2 Benefit categories

Measure only where evidence exists:

- avoided manual evidence collection;
- reduced rework;
- reduced escaped-defect or failed-change cost;
- reduced credential-exposure response;
- reduced untracked-work recovery;
- reduced provider-migration or integration effort;
- reduced onboarding and orientation effort;
- avoided duplicate provider effects;
- continuity value during outages; and
- increased safe throughput at unchanged or improved risk.

### 7.3 Value equation

Use an organization-approved model:

`net value = evidenced avoided cost + evidenced capacity value + risk-adjusted loss reduction - implementation and operating cost`

Do not:

- count gross agent output as value;
- count prevented test cases as prevented production incidents;
- treat ticket estimate reduction as realized savings;
- monetize hypothetical risk without an approved probability and impact method; or
- omit human review, curation, support, and control costs.

## 8. Existing baseline evidence and limitations

The corpus contains useful but narrow research:

- one Communications repository and one developer machine produced 378 local invocation-history matches;
- the observed usage is concentrated in Operator and Process-style work;
- the hierarchy was rarely used operationally in that sample;
- one readiness pack was measured at roughly 1,525 output tokens and 2.7 seconds;
- a full inventory added roughly 41,000 tokens and was about 27 times heavier in that run;
- the top-30 command set received a provisional average CLI Spec score of 5.7/16; and
- the current CLI/MCP payload study used rough token estimation, non-equivalent paths, a single run, and an unhealthy KnowMCP path.

These data may justify better bounded orientation and broader measurement. They do not establish:

- fleet-wide demand;
- an enterprise usage distribution;
- a general CLI-versus-MCP performance ratio;
- production reliability;
- business savings;
- customer willingness to adopt; or
- ROI.

## 9. Measurement design

### 9.1 Baseline window

Define:

- repositories and teams;
- task classes and risk levels;
- human, agent, and mixed modes;
- providers and environments;
- sample size and time period;
- current policy and tooling;
- exclusion and failure rules; and
- data-quality checks.

### 9.2 Pilot comparison

Use repeated equivalent tasks where possible. Record:

- task outcome and quality;
- active and waiting time;
- model input/output tokens;
- number of calls and retries;
- validation time;
- user and operator interventions;
- refusal and remediation;
- ticket and evidence completeness;
- external effects;
- degraded intervals; and
- exceptions or bypasses.

### 9.3 Attribution

AEGIS adoption may coincide with model, staffing, process, or workload changes. Where controlled comparison is impractical:

- use matched workflow cohorts;
- report confounders;
- compare trends over multiple periods;
- separate implementation learning from steady operation; and
- avoid causal language stronger than the design supports.

## 10. Dashboard layers

### Executive

- safe throughput;
- traceability and human-authority coverage;
- change quality and incident trend;
- audit and evidence effort;
- net operating cost and evidenced benefit;
- adoption and bypass rate; and
- top residual risks.

### Product and platform

- time to orient;
- task success and lead time;
- false refusal and remediation;
- capability availability and replacement;
- schema/documentation drift;
- provider and knowledge usage; and
- milestone acceptance.

### Risk and control

- gate outcomes;
- waiver and identity failures;
- provenance and revocation;
- secret and credential findings;
- completion gaps;
- external-effect duplicates;
- degraded operation and expiry;
- reconciliation conflict; and
- control-test status.

### Operations

- health and latency;
- retries and circuit breakers;
- spool and ingest lag;
- run resume;
- storage and retention;
- token and validation cost; and
- incidents and SLOs.

## 11. Decision thresholds

Set numerical pilot thresholds after baseline. At minimum, require:

- no successful critical-control negative test;
- complete human authorization for reserved actions;
- complete traceability for the acceptance sample;
- no silent loss, overwrite, or duplicate effect in recovery tests;
- false-refusal and latency within approved bounds;
- all critical operating owners and incident paths active;
- retention and privacy controls approved;
- measured user behavior not shifting to shadow paths; and
- a credible value case after full operating cost.

## 12. Review cadence

| Cadence | Review |
|---|---|
| Per build or release | Architecture acceptance targets and negative paths |
| Weekly during pilot | False refusals, remediation, bypass pressure, data quality, and user feedback |
| Monthly during pilot | Control coverage, value measures, cost, risks, and scope decision |
| Quarterly when operational | Benefit realization, control effectiveness, SLOs, access, exceptions, and risk appetite |
| After incident or major outage | Reconstruction, control failure, recovery, and design assumptions |
| Before scope expansion | New provider, team, environment, data, and threat analysis |

## 13. Success definition

AEGIS is successful only if the organization can demonstrate that:

1. more delegated work is authorized, attributable, and reconstructable;
2. evidence and completion controls behave correctly under positive and negative tests;
3. high-risk decisions remain verifiably human;
4. credential and provider effects are more controlled;
5. continuity improves without silent loss of authority;
6. user and operator friction stays inside agreed limits;
7. quality or risk-adjusted throughput improves;
8. benefits persist after including full operating cost; and
9. claims remain honest about maturity, evidence, and threat scope.

