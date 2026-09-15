---
id: AEGIS-GUIDE-023
title: Discovery and Qualification
summary: Determine whether the buyer has a material governed-agentic-delivery problem, whether AEGIS fits the intended architecture, whether the organization can support a measured pilot, and what evidence would justify the ne...
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
# Discovery and Qualification

- **Audience:** Internal sales, solutions, product, and technical evaluators
- **Disclosure:** Internal only
- **Maturity:** Qualification framework derived from target use cases and adoption prerequisites

## Discovery objective

Determine whether the buyer has a material governed-agentic-delivery problem, whether AEGIS fits the intended architecture, whether the organization can support a measured pilot, and what evidence would justify the next step.

Discovery is not a product demonstration. Do not lead the buyer toward claims the repository cannot prove.

## Opening questions

1. What work do AI agents perform today?
2. Which actions can change code, configuration, work records, knowledge, or external systems?
3. How do you know that work was authorized?
4. What evidence is required before work is considered complete?
5. Which actions must remain human-approved?
6. Where do agent credentials come from?
7. How do you reconstruct an agent-assisted change after an incident?
8. Which trackers, repositories, pipelines, and agent harnesses are in scope?
9. What happens when a tracker or governance dependency is unavailable?
10. What would a successful, low-risk evaluation prove?

## Problem discovery

### Agent adoption and scope

- How many teams use agents, and for which task classes?
- Are agents advisory, code-writing, tool-using, or externally acting?
- Which models and harnesses are used?
- Which agent actions are allowed without human review?
- What growth or autonomy is planned?
- Which environments are reachable?
- Are human and agent actions governed differently?

**Listen for:** Multiple tools, rapid growth, unclear action inventory, and inconsistent control.

### Work authorization

- What authorizes a substantive change?
- Must work link to a portfolio initiative or epic?
- How are tickets linked to branches, pull requests, runs, and deployments?
- Can agents create or modify work records?
- How are oversized or unestimated changes handled?
- What percentage of changes have complete linkage?
- What exceptions are tolerated?

**Listen for:** Chat-based authorization, missing linkage, manual reconciliation, and after-the-fact tickets.

### Completion and evidence

- Who or what declares work complete?
- Where are required steps represented?
- How are tests and validation mapped to claims?
- How are assumptions recorded and rechecked?
- Can an agent skip a step without an explicit record?
- How long does audit evidence assembly take?
- What does a failed completion attempt look like?

**Listen for:** Actor narrative as authority, checklist drift, evidence gathering after the fact, and no negative tests.

### Human authority

- Which actions require a person?
- How is human identity proven at action time?
- Is chat approval sufficient?
- Are approvals bound to action, work, environment, and expiry?
- Which actions require two people?
- Can an agent request or use a waiver?
- How are emergency actions handled?

**Listen for:** TTY or chat as proof, reusable approvals, unclear roles, and self-approval.

### Credentials and external providers

- Which worker processes can read provider credentials?
- Do agents call provider SDKs directly?
- How are tokens scoped, issued, rotated, and revoked?
- Are external effects bound to work and run context?
- How are retries and ambiguous provider responses handled?
- Are duplicate effects a known problem?
- Which providers cannot be proxied?

**Listen for:** Long-lived tokens in environment files, direct worker access, missing idempotency, and weak receipts.

### Knowledge

- Where do agents search first?
- How do users distinguish project, organization, and public information?
- Who owns knowledge quality?
- How are provenance, freshness, status, and confidence represented?
- Can an agent promote its own answer to trusted knowledge?
- How are stale, disputed, and superseded records handled?
- What is the current search success and review workload?

**Listen for:** Unqualified vector results, no human review, repeated research, and no staleness model.

### Outage, recovery, and trust

- What happens when the tracker, identity service, governance service, or telemetry backend is down?
- Can work continue, and under what authority?
- Is there a trust expiry?
- How is buffered work reconciled?
- Which system wins conflicts?
- How are interrupted runs resumed?
- How are duplicate external effects detected?

**Listen for:** Silent fallback, indefinite cached authority, shadow notes, lost work, and manual replay.

### Architecture and ecosystem

- Which operating systems and architectures are required?
- Is Git universal for the target scope?
- Which trackers and CI/CD platforms are authoritative?
- What network and egress restrictions apply?
- Is self-hosting required?
- What are data residency and tenancy requirements?
- What is the preferred container platform?
- What must remain available offline?

**Listen for:** Windows-only scope, required SaaS tenancy, unsupported provider needs, or architecture assumptions that conflict with v1.

### Operations and ownership

- Who would own the product, service, controls, identity, work adapters, knowledge, and support?
- What SLOs and incident practices are required?
- Who manages signing and revocation?
- Who owns retention and deletion?
- What on-call and escalation model is expected?
- What level of implementation capacity exists?

**Listen for:** No accountable owner, no support capacity, or the assumption that governance is installation-only.

### Value

- What does current evidence gathering cost?
- How often does work lack complete authorization?
- What are current lead time, rework, failed-change, and investigation measures?
- What credential or provider incidents have occurred?
- How much time is spent rediscovering project knowledge?
- What is the cost of tracker outages?
- Which outcome would justify a pilot?
- What friction would make the pilot fail?

**Listen for:** Measurable current-state burden and an owner who accepts full-cost evaluation.

## Qualification rubric

Score each dimension as strong, conditional, or weak.

| Dimension | Strong | Conditional | Weak |
|---|---|---|---|
| Problem | Material authorization, evidence, credential, or reconstruction gap | Concern exists but is not measured | Generic interest only |
| Agent scope | Tool-using agents or planned growth | Limited agent-assisted development | Advisory chat only |
| Risk | Human authority or audit matters | Moderate governance need | No consequence for missing control |
| Ecosystem | Git, macOS/Linux, supported target tracker | Some adapter or hosting work | Hard dependency on out-of-scope v1 |
| Ownership | Named cross-functional owners | Owners can be assigned | No one will own service or controls |
| Pilot | Development-only baseline and POV accepted | Scope needs negotiation | Immediate production deployment required |
| Evidence | Buyer will collect baseline and negative tests | Limited data available | Wants guaranteed outcome without measurement |
| Maturity fit | Accepts early/design-stage engagement | Requires near-term implementation evidence | Requires production references/certification now |
| Human authority | Agrees to explicit reserved actions | Policy not yet decided | Wants agents to self-authorize production |
| Security fit | Accepts stated trust boundary and hardening path | Additional controls may bridge gap | Requires malicious-local-process prevention now |
| Value | Current cost/exposure can be measured | Hypothesis only | ROI expected from roadmap estimates |

## Qualification outcomes

### Qualified for discovery workshop

- material problem exists;
- relevant stakeholders will participate;
- design-stage maturity is accepted; and
- the buyer wants architecture, controls, or baseline definition.

### Qualified for proof of value

- target workflow is bounded;
- development-only scope is approved;
- authoritative systems are identified;
- owners and reviewers are named;
- baseline measures and negative tests are agreed;
- retention and access are addressable; and
- stop conditions are explicit.

### Nurture

- problem is relevant, but ownership, timing, budget, or target scope is not ready;
- required design decisions are still internal to the buyer; or
- implementation evidence must mature first.

### Disqualify

- hard requirements conflict with the stated v1 boundary;
- the buyer requires unsupported proof or commitments;
- no accountable operating model can be established; or
- the desired outcome removes rather than preserves human authority.

## Evidence to request

Request the smallest representative sample:

- workflow diagrams or operating procedures;
- anonymized ticket, branch, PR, validation, and deployment linkage;
- current agent/tool inventory;
- provider and credential flow;
- evidence package from a recent change or incident;
- outage and recovery procedure;
- knowledge sources and representative queries;
- current policies for waiver and promotion;
- operating-system and deployment constraints; and
- baseline metrics or measurement access.

Do not request secrets, raw credentials, unnecessary personal data, or production access during discovery.

## Opportunity record

Capture:

- business problem in buyer language;
- target users and workflows;
- current systems of authority;
- agent actions and environments;
- reserved human decisions;
- security and threat requirements;
- provider and identity dependencies;
- ownership;
- measurable baseline;
- desired outcomes;
- disqualifiers and open decisions;
- maturity expectations;
- proof criteria;
- commercial unknowns; and
- next mutual action.

## Red flags

- “We need a demo next week that proves production enforcement.”
- “Agents should be able to waive anything when they are confident.”
- “We do not use tickets for small changes.”
- “Every bot gets the same admin token.”
- “The tracker is down often, so people work in chat and backfill later.”
- “Security wants a guarantee that local root-level malware cannot bypass it.”
- “We need Windows and multi-tenant SaaS in v1.”
- “We need a fixed price and date from the architecture estimate.”
- “There is no one to curate knowledge or own the service.”
- “We cannot measure baseline because we only want future-state projections.”

## Handoff to solutions or product

Provide:

- validated problem statement;
- source systems and target workflow;
- fit and anti-fit findings;
- required architecture decisions;
- security diligence needs;
- explicit unsupported requirements;
- proposed pilot scope;
- baseline and scorecard;
- buyer stakeholders;
- risks and stop conditions; and
- requested commitments.

## Sources

- [Buyer Problems and Use Cases](./02-buyer-problems-and-use-cases.md)
- [Adoption and Pilot Guide](./06-adoption-and-pilot-guide.md)
- [Target Operating Model](../business/04-operating-model.md)
