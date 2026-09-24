# AEGIS Business Documentation

- **Status:** Derived draft for business review
- **Source baseline:** `docs/architect` as indexed on 2026-09-14
- **Audience:** Executive sponsors, product and platform leaders, engineering management, security and compliance, delivery operations, knowledge owners, and auditors
- **Authority:** This folder interprets the architecture corpus for business use; it does not replace or ratify any source design

## Purpose

This documentation explains the business problem AEGIS is intended to solve, the value it is expected to create, the capabilities and operating model required to create that value, the controls that bound its use, and the roadmap and measures needed to assess adoption.

The central proposition is:

> HATHOR defines a durable operating framework for people and agents; AEGIS realizes its governance and control plane so automation can scale without losing authorization, evidence, human accountability, or operational control.

The documents describe a **target operating model and target product design**. They must not be read as evidence that the platform is implemented, deployed, or producing realized benefits.

## Document map

| Document | Primary question | Recommended readers |
|---|---|---|
| [01 — Executive Overview](./01-executive-overview.md) | What is AEGIS, why does it matter, and what decisions does it support? | Executives, sponsors, product and technology leaders |
| [02 — Business Requirements](./02-business-requirements.md) | What business outcomes and conditions must the platform satisfy? | Product, architecture, governance, program leadership |
| [03 — Business Capability Model](./03-business-capability-model.md) | Which business capabilities are required and how do they depend on one another? | Product, platform, enterprise architecture |
| [04 — Operating Model](./04-operating-model.md) | Who decides, who acts, what records are authoritative, and how does work flow? | Engineering, delivery operations, knowledge owners, auditors |
| [05 — Governance, Risk, and Controls](./05-governance-risk-and-controls.md) | How is risk controlled, what can be claimed, and what gaps remain? | Security, risk, compliance, architecture, audit |
| [06 — Adoption Roadmap](./06-adoption-roadmap.md) | How should the design move from foundations to governed use? | Sponsors, program leadership, platform teams |
| [07 — Value and Success Measures](./07-value-and-success-measures.md) | How will the organization know whether AEGIS creates value safely? | Sponsors, finance, product, operations, governance |
| [08 — Glossary and Source Register](./08-glossary-and-source-register.md) | What do the terms mean and which architecture sources support each business claim? | All readers |

## Business context in one page

### The problem

AI-assisted engineering may increase the volume and speed of work beyond what manual reconciliation can reliably govern. Common operating practices can leave intent in chat, approvals in memory, status in a tracker, evidence in CI, credentials in local environments, and completion in an actor's own narrative. This is a business problem hypothesis to test during baseline and pilot work, not a measured fleet-wide conclusion. If the hypothesis holds, the organization can lose the ability to answer:

- What work was authorized?
- Which strategic outcome did it support?
- Who or what acted, using which approved capability?
- What evidence proves that mandatory steps completed?
- Which human authorized promotion or deployment?
- What external systems were changed and with which credentials?
- What knowledge was created, reviewed, and trusted?
- Can the full sequence be reconstructed after an incident or audit?

### The proposed response

AEGIS adds a single governed command surface over three distinct sources of truth:

1. **Registry Plane:** which automation units may run.
2. **Knowledge Plane:** what information is trusted and how it was verified.
3. **Ticketing Plane:** what work exists and what authorizes action.

Conducted runs connect these authorities to an evidence-backed hierarchy from business procedure through executable checklist. Small, single-purpose automation units are admitted by policy, external connections are brokered, run progress is event-sourced, and the system—not the actor performing the work—determines completion.

### The intended business result

AEGIS is intended to create **bounded, evidence-backed automation**, not autonomy without constraint. Its business value depends on five outcomes:

- **Accountability:** every substantive change traces to authorized work, strategic lineage, actors, evidence, and outcome.
- **Assurance:** completion and claims are evaluated against recorded evidence rather than accepted from narrative.
- **Human authority:** people retain decision rights for deployment, knowledge promotion, waiver, and other high-risk actions.
- **Portability:** the governance model operates above Jira, Azure DevOps, GitHub, languages, and agent harnesses.
- **Resilience:** local work can continue through bounded outages without concealing degraded trust or bypassing authority.

## Source authority and status rules

Business readers should apply the following precedence:

1. [`AEGIS-CANON-001`](../architect/aegis-canon-001-registries-20260913.md) owns enumerated registries and identifiers.
2. Accepted architecture decisions and accepted research/interface decisions define ratified choices.
3. Draft and proposed requirements, research papers, architecture syntheses, and technical specifications remain review material unless an amendment is explicitly ratified.
4. Approved plans sequence work; they do not approve a draft design or authorize implementation.
5. This business set is a derived interpretation. If it conflicts with a source, the source wins and this set must be corrected.

### Claim classes used in this folder

| Label | Meaning |
|---|---|
| **Accepted direction** | Supported by an accepted ADR, canonical registry, or accepted research/interface decision |
| **Draft requirement** | Present in a draft requirement or specification and not independently ratified |
| **Approved sequence** | Scheduled in an approved roadmap, but not evidence of implementation |
| **Recommended practice** | Business recommendation introduced here for adoption, measurement, or governance |
| **Open decision** | Material issue requiring an operator, product, security, or governance decision |

## Current maturity

As of the source baseline:

- The greenfield `aegis` command surface, central orchestration model, state-residency model, backup ticketing approach, canonical registries, Control Tower surface, Operator brokering, Knowledge storage/retrieval, threat model, and bot-unit model have accepted design decisions.
- The platform roadmap and gateway/validator roadmap are approved as planning artifacts.
- Core platform requirements, several foundational research papers, and implementation specifications remain draft.
- The bot-unit stakeholder compendium and HATHOR platform-principle synthesis await operator sign-off.
- The repository describes HATHOR as being in early formation; this corpus does not establish production readiness or realized customer outcomes.
- The architecture records unresolved human-token contract and identity-provider details, event integrity, executable-artifact binding, effect reconciliation, approval, hosting, and operating-policy decisions.

## Intended use

This set is suitable for:

- business and product review of the target operating model;
- funding, sequencing, and pilot-scope decisions;
- control and risk workshops;
- stakeholder onboarding;
- preparation of epics, acceptance criteria, and value hypotheses; and
- evaluation of whether implementation evidence supports moving from report-only to enforced use.

It is not, by itself:

- an implementation authorization;
- a production-readiness assessment;
- a security certification or compliance attestation;
- a validated ROI case;
- a commitment to roadmap dates or estimates; or
- permission for agents to deploy, waive controls, or promote knowledge.

## Maintenance

Update this folder when a source decision changes a business outcome, capability boundary, decision right, risk statement, roadmap dependency, or metric definition. Keep each change traceable through [08 — Glossary and Source Register](./08-glossary-and-source-register.md).

