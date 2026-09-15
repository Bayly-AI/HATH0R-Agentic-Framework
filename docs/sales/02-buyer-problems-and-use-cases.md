---
id: HATHOR-GUIDE-016
title: Buyer Problems and Use Cases
summary: Organizations adopting AI-assisted engineering may increase activity faster than their existing governance practices can reconcile it. The relevant risk is not simply that an agent can make a mistake. It is that inten...
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
# Buyer Problems and Use Cases

- **Audience:** Business sponsors, technology leaders, security, platform teams, sales, and solutions
- **Disclosure:** Buyer-facing draft; use discovery to validate each problem
- **Maturity:** Problem and outcome hypotheses derived from target design

## Core problem hypothesis

Organizations adopting AI-assisted engineering may increase activity faster than their existing governance practices can reconcile it. The relevant risk is not simply that an agent can make a mistake. It is that intent, authorization, identity, evidence, external effects, and completion may live in different systems and be interpreted differently by humans, agents, and tools.

AEGIS is relevant when a buyer needs to answer several of these questions consistently:

- What work authorized this action?
- Which business initiative did the work support?
- Who or what acted?
- Which approved capability and version ran?
- Which policies and validation controls applied?
- What evidence supports completion?
- Which external services changed, using which governed connection?
- Which human approved a waiver, knowledge promotion, or environment promotion?
- Can the sequence be reconstructed after an incident?
- What happened during a tracker, Tower, or telemetry outage?

Discovery must test whether this is a material problem for the buyer. It must not assume that every organization has the same gap or that AEGIS already solves it operationally.

## Problem-to-capability map

| Buyer problem | Operational symptom | AEGIS target response | Evidence needed in an evaluation |
|---|---|---|---|
| Work begins without durable authorization | Changes originate in chat or agent sessions with incomplete ticket linkage | No-ticket, epic-linkage, and change-binding controls | Pre/post linkage coverage and refused negative cases |
| “Done” is self-declared | Reviewers reconstruct tests and required work after the fact | Conducted run, required-set reconciliation, claims and evidence | False-completion tests and sampled run reconstruction |
| Governance differs by tool or agent | Each harness or repository implements policy differently | One public contract above tools and providers | Equivalent policy behavior across selected workflows |
| Provider credentials spread across workers | Bots use direct SDK credentials or copied secrets | Operator proxy by default and scoped token exceptions | Runtime inspection and complete effect receipts |
| Knowledge is stale or unattributed | Agents repeatedly rediscover context or trust copied content | Tiered retrieval, provenance, status, TTL, human promotion | Search evaluation, staleness handling, and reviewer records |
| Outages drive shadow work | Tracker failure causes untracked notes or later manual recreation | Minimal backup capture, bounded trust, reconciliation | Outage, replay, conflict, and expiry exercises |
| Audit evidence is expensive to reconstruct | Intent, approval, tests, and effects live in separate systems | Joined work, run, evidence, identity, and provider records | Time-boxed reconstruction sample |
| Automation components become opaque dependencies | A component owns private state, credentials, or caller-specific logic | Single-purpose capabilities with external state and lifecycle | Quarantine, replacement, and successor-routing test |
| Agent cost and retry behavior are unclear | Token, validation, and provider calls cannot be attributed to outcomes | Passive per-run observation | Equivalent-task cost and retry baseline |

## Priority use cases

### 1. Governed AI-assisted code change

**Buyer need:** Allow an agent to implement a change without losing work authorization, strategic lineage, validation evidence, or human release authority.

**Target flow:**

1. Resolve an active work item and strategic epic.
2. Bind the actor, capability, branch or change, and run.
3. Admit work only after provenance, contract, sequence, and applicable domain checks.
4. Execute a bounded capability.
5. Record validation findings, claims, assumptions, and evidence.
6. Reconcile mandatory work before completion.
7. Require a verified human for higher-environment promotion.

**Value hypothesis:** Increased delegated throughput with a more complete accountability chain.

**Pilot proof:** Complete traceability for an agreed sample; false completion and unauthorized promotion tests fail safely.

### 2. Evidence-backed completion and audit reconstruction

**Buyer need:** Reduce reliance on actor testimony or manual evidence archaeology.

**Target flow:** Process folds an append-only run record; validators evaluate evidence and required work; provider receipts record external effects; Tower supports bounded query and rollup.

**Value hypothesis:** Faster review, incident investigation, and audit preparation.

**Pilot proof:** An independent reviewer reconstructs selected mutations from authoritative records within a measured time budget.

### 3. Human-controlled environment promotion

**Buyer need:** Let agents build and verify while preventing them from granting their own production authority.

**Target flow:** Agents prepare a request; environment and deployment gates evaluate work; a reconciled deployment ticket and action-bound human identity authorize promotion.

**Value hypothesis:** More automation without removing separation of duties.

**Pilot proof:** Expired, replayed, wrong-action, wrong-audience, and machine-identity attempts do not authorize a reserved action.

**Important boundary:** The detailed token profile remains an open pre-enforcement decision.

### 4. Brokered third-party effects

**Buyer need:** Integrate work systems and external services without distributing long-lived credentials to every worker.

**Target flow:** A worker submits a canonical request; Operator resolves the governed connection, applies rate, retry, circuit, and idempotency policy, and returns a receipt. A narrow token handoff is declared only when proxying is impractical.

**Value hypothesis:** Lower credential exposure and better attribution.

**Pilot proof:** Class-1 workers receive no provider credentials; retries and resumes do not create duplicate effects in tested scenarios.

### 5. Provider-neutral work governance

**Buyer need:** Apply consistent authorization and policy while retaining Jira, Azure DevOps, or GitHub as the authoritative tracker.

**Target flow:** A canonical Ticket Contract maps common operations to provider adapters. The selected provider remains authoritative.

**Value hypothesis:** Lower governance coupling to a specific work provider.

**Pilot proof:** Selected operations and refusal behavior remain consistent across the buyer’s initial provider and a controlled adapter test.

### 6. Governed organizational knowledge

**Buyer need:** Help agents find local context without treating every retrieved fragment as current truth.

**Target flow:** Search prioritizes project, machine, organization, then public sources. Results expose provenance, status, freshness, and confidence. New knowledge enters as draft and requires human promotion.

**Value hypothesis:** Less rediscovery and safer reuse.

**Pilot proof:** Representative queries improve successful orientation while stale, disputed, external, and draft material remain correctly labeled.

### 7. Bounded continuity during provider outages

**Buyer need:** Avoid losing work or silently bypassing authority when a dependency is unavailable.

**Target flow:** Signed cached trust and local records allow only declared activity inside a trust TTL. Eligible work capture may buffer in a minimal backup service. The authoritative provider wins during reconciliation; conflicts remain explicit.

**Value hypothesis:** More resilient work capture without creating a second source of truth.

**Pilot proof:** No silent loss, overwrite, deployment authority, or duplicate effect during tested outage and recovery paths.

### 8. Governed automation-component lifecycle

**Buyer need:** Know which automation can run and retire or replace it without hidden organizational state.

**Target flow:** Authorize, scaffold, self-test, sign, register, operate, evolve, revoke, and retire a versioned capability.

**Value hypothesis:** Lower blast radius and faster replacement.

**Pilot proof:** Revoked components receive no new work after reconciliation, and unrelated capabilities remain available during quarantine.

### 9. Proportionate continuous validation

**Buyer need:** Add assurance early without applying whole-repository cost to every small change.

**Target flow:** Pure micro-linters and plane-aware validators run at defined lifecycle triggers and tiers, from fast static checks to asynchronous analysis.

**Value hypothesis:** Earlier defects and evidence with acceptable latency.

**Pilot proof:** Finding quality, remediation, false-refusal rate, suite duration, rework, and lead-time trends.

### 10. Portfolio-to-outcome traceability

**Buyer need:** Understand how delegated execution supports strategic work.

**Target flow:** Strategic epic, ticket, hierarchy chain, actor, capability, run, evidence, and outcome are linked.

**Value hypothesis:** Better investment and accountability visibility.

**Pilot proof:** Complete traversal for the acceptance sample and no orphaned in-scope changes.

## Buyer personas and outcome language

| Persona | Lead with | Avoid leading with |
|---|---|---|
| Executive sponsor | Safe scale, accountability, measured value, decision rights | Bot names, manifest schemas, token benchmarks |
| CTO or platform leader | Common operating contract, portability, modularity, adoption path | “Replace your stack” |
| CISO or risk leader | Explicit threat model, credentials, identity, provenance, evidence | Unqualified “secure” or “tamper-proof” |
| Engineering leader | Faster orientation, consistent remediation, evidence-backed workflow | Governance as surveillance |
| Audit or compliance | Reconstruction, separation of duties, retained authority | Certification claims |
| DevOps or release leader | Human promotion, environment controls, recoverability, telemetry | Autonomous deployment |
| Knowledge owner | Provenance, lifecycle, human curation, stale-content handling | Automatic truth generation |
| Developer or agent integrator | Predictable commands, bounded context, structured refusal | Central control with no remediation |

## Strong qualification signals

- The buyer already uses multiple agent tools or expects significant growth.
- Work authorization and evidence are materially fragmented.
- Regulated, high-assurance, or high-cost change requires reconstruction.
- Agent access to credentials or external providers is a concern.
- Teams want common governance without replacing current trackers or harnesses.
- Knowledge provenance and staleness are active problems.
- Provider outages create untracked work or manual reconciliation.
- Leadership will fund a baseline and accept a bounded development pilot.
- Named owners can participate across product, engineering, security, identity, work systems, and knowledge.

## Weak fit or anti-fit

- The buyer wants immediate production autonomy with no human promotion boundary.
- The buyer requires a production-proven product, certification, or customer references today.
- The organization will not establish durable work authorization or evidence.
- The buyer expects AEGIS to replace its model, harness, tracker, or CI/CD platform.
- No team can own controls, service operations, identity, retention, or curation.
- The buyer will not tolerate report-only learning before enforcement.
- The primary requirement is prevention against a malicious process with arbitrary local workspace access.

## Sources

- [Business Requirements](../business/02-business-requirements.md)
- [Business Capability Model](../business/03-business-capability-model.md)
- [Target Operating Model](../business/04-operating-model.md)
- [Value and Success Measures](../business/07-value-and-success-measures.md)
