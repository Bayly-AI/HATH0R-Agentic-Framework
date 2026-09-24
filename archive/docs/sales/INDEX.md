# AEGIS Sales Documentation

- **Status:** Derived sales-enablement draft
- **Source baseline:** Project documentation through 2026-09-15; the derived business set remains based on the 2026-09-14 architecture index
- **Product maturity:** Design stage; the corpus does not establish implementation, production readiness, customer adoption, certification, or realized ROI
- **Authority:** This folder translates source material for sales use; architecture and business sources remain authoritative

## Purpose

This library explains how to position, qualify, discuss, and evaluate AEGIS without overstating what the current project proves.

HATHOR is the broader agentic application framework. AEGIS is its proposed governance and control-plane realization: a common operating layer intended to connect people, AI agents, automation units, project knowledge, work systems, validation, and external services under explicit authority and evidence rules.

The concise proposition is:

> AEGIS is designed to help organizations scale AI-assisted delivery while preserving authorization, evidence, human decision rights, and reconstructable accountability.

That is a target proposition, not a claim that the system is implemented or producing customer outcomes today.

## How to use this library

### Buyer-facing documents

These documents may inform external conversations after product, legal, security, and commercial review. Preserve maturity qualifiers when quoting them.

| Document | Use |
|---|---|
| [01 — Executive Product Brief](./01-executive-product-brief.md) | Executive introduction, strategic problem, proposition, and boundaries |
| [02 — Buyer Problems and Use Cases](./02-buyer-problems-and-use-cases.md) | Buyer pain, use-case framing, outcomes, and qualification signals |
| [03 — Platform Capabilities](./03-platform-capabilities.md) | Capability narrative, differentiators, user value, and target scope |
| [04 — Architecture and Integrations](./04-architecture-and-integrations.md) | Technical buyer overview, ecosystem fit, deployment direction, and integration boundaries |
| [05 — Security, Governance, and Assurance](./05-security-governance-and-assurance.md) | Trust model, control layers, residual risk, and compliance-aligned discussion |
| [06 — Adoption and Pilot Guide](./06-adoption-and-pilot-guide.md) | Low-risk evaluation path, proof criteria, governance checkpoints, and expansion rules |
| [07 — Value and Business Case](./07-value-and-business-case.md) | Value hypotheses, baseline design, measures, costs, and decision framework |

### Internal sales-enablement documents

These documents are internal working material and are not customer collateral without review.

| Document | Use |
|---|---|
| [08 — Ideal Customer and Buying Committee](./08-ideal-customer-and-buying-committee.md) | ICP, fit, anti-fit, stakeholders, and role-specific value |
| [09 — Discovery and Qualification](./09-discovery-and-qualification.md) | Discovery questions, qualification rubric, evidence collection, and handoff |
| [10 — Messaging and Talk Tracks](./10-messaging-and-talk-tracks.md) | Positioning, pitches, persona messages, presentation flow, and language rules |
| [11 — Objection Handling and FAQ](./11-objection-handling-and-faq.md) | Direct, source-grounded responses to common buyer questions |
| [12 — Sales Engagement and Proof-of-Value Playbook](./12-sales-engagement-and-proof-of-value-playbook.md) | Engagement stages, deliverables, mutual action plan, POV, and exit criteria |
| [13 — Claims, Evidence, and Source Coverage](./13-claims-evidence-and-source-coverage.md) | Claim policy, approved formulations, evidence gaps, disclosure rules, and full source accounting |
| [14 — Sales Glossary](./14-sales-glossary.md) | Consistent product, architecture, governance, and maturity terminology |

## Recommended reading paths

### Executive sponsor

1. [Executive Product Brief](./01-executive-product-brief.md)
2. [Buyer Problems and Use Cases](./02-buyer-problems-and-use-cases.md)
3. [Value and Business Case](./07-value-and-business-case.md)
4. [Adoption and Pilot Guide](./06-adoption-and-pilot-guide.md)

### CIO, CTO, platform, or enterprise architecture

1. [Executive Product Brief](./01-executive-product-brief.md)
2. [Platform Capabilities](./03-platform-capabilities.md)
3. [Architecture and Integrations](./04-architecture-and-integrations.md)
4. [Adoption and Pilot Guide](./06-adoption-and-pilot-guide.md)

### CISO, risk, compliance, or audit

1. [Security, Governance, and Assurance](./05-security-governance-and-assurance.md)
2. [Architecture and Integrations](./04-architecture-and-integrations.md)
3. [Claims, Evidence, and Source Coverage](./13-claims-evidence-and-source-coverage.md)
4. [Adoption and Pilot Guide](./06-adoption-and-pilot-guide.md)

### Sales, solutions, or product marketing

1. [Claims, Evidence, and Source Coverage](./13-claims-evidence-and-source-coverage.md)
2. [Ideal Customer and Buying Committee](./08-ideal-customer-and-buying-committee.md)
3. [Discovery and Qualification](./09-discovery-and-qualification.md)
4. [Messaging and Talk Tracks](./10-messaging-and-talk-tracks.md)
5. [Objection Handling and FAQ](./11-objection-handling-and-faq.md)
6. [Sales Engagement and Proof-of-Value Playbook](./12-sales-engagement-and-proof-of-value-playbook.md)

## Claim classes

| Class | Meaning | Safe formulation |
|---|---|---|
| Accepted design | Ratified architecture direction | “The accepted design uses…” |
| Draft target | Requirement, research paper, architecture, or technical specification still under review | “The target design proposes…” |
| Approved sequence | Work is sequenced in an approved plan | “The approved roadmap sequences…” |
| Proposed item | Awaiting explicit sign-off | “A proposed design under review would…” |
| Implemented | Code and configuration exist for an authorized scope | Use only with repository and test evidence |
| Verified | Positive, negative, recovery, and boundary tests pass | Use only with test evidence and stated scope |
| Piloted or operational | Real workloads and operating ownership are evidenced | Use only with pilot or production records |
| Measured outcome | A business benefit has a credible baseline and comparison | Use only with approved measurement evidence |

## Non-negotiable sales rules

1. Do not call AEGIS production-ready.
2. Do not claim customers, deployments, certifications, SLAs, or realized ROI without evidence outside this corpus.
3. Do not describe accepted designs as implemented features.
4. Do not promise “tamper-proof,” “impossible to bypass,” “fully autonomous and safe,” or “guaranteed exactly once.”
5. Scope security statements to the cooperative-but-fallible v1 trust model.
6. State that executable or image-byte binding and the detailed human-token contract remain open before strong assurance claims.
7. Preserve human authority: agents may prepare and request; they do not approve their own waivers, production promotion, or authoritative knowledge.
8. Treat roadmap hours and weeks as planning estimates, not delivery commitments or prices.
9. Do not use the existing one-machine inventory or limited token benchmark as enterprise proof.
10. Use the source register before introducing a new claim.

## Source authority

When sources conflict, use this order:

1. [`AEGIS-CANON-001`](../architect/aegis-canon-001-registries-20260913.md) for canonical registries and identifiers.
2. Accepted architecture decisions and accepted research/interface decisions.
3. Draft requirements, research, architecture, and technical specifications, preserving their status.
4. Approved plans for sequence only.
5. The derived [business documentation](../business/INDEX.md).
6. This sales translation.

See [13 — Claims, Evidence, and Source Coverage](./13-claims-evidence-and-source-coverage.md) for the complete register.
