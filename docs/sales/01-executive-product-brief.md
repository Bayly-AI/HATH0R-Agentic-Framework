---
id: HATHOR-GUIDE-015
title: HATHOR Executive Product Brief
summary: AI agents can increase the speed and volume of engineering work. They can also distribute intent, authority, credentials, evidence, and status across chats, repositories, trackers, CI systems, and provider consoles. W...
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
# HATHOR Executive Product Brief

- **Audience:** Executive sponsors, CIO, CTO, CISO, engineering and platform leaders
- **Disclosure:** Buyer-facing draft; review before external distribution
- **Maturity:** Target product and operating model; implementation and outcomes are not established by the current corpus

## Executive proposition

AI agents can increase the speed and volume of engineering work. They can also distribute intent, authority, credentials, evidence, and status across chats, repositories, trackers, CI systems, and provider consoles. When those fragments are reconciled manually, higher automation volume can reduce an organization’s ability to prove who authorized work, what controls ran, whether required steps completed, and which human retained final authority.

HATHOR is designed as a governance and control layer for that problem.

HATHOR defines the durable framework for agent navigation, project structure, knowledge, governance, credentials, and attributable work. HATHOR proposes to realize that framework through a single operational command surface, explicit sources of authority, small governed automation units, conducted runs, continuous validation, secure integration brokering, and centralized trust and audit services.

HATHOR is not intended to replace foundation models, agent harnesses, source control, CI/CD, enterprise work trackers, or human judgment. It is intended to make those components operate under a consistent, inspectable contract.

## The executive question

> As human and machine work scales, can the organization reconstruct what happened, why it happened, which authority permitted it, what evidence supported it, and which human approved the highest-risk decision?

HATHOR treats this as an operating-model and control problem rather than a prompt-engineering problem.

## The proposed response

### One governed operational front door

The accepted direction establishes the `hath0r` CLI as the public operational ingress for supported human, agent, and bot actions. The intent is to apply identity, policy, routing, refusal, and evidence behavior consistently without requiring every tool to reinvent governance.

One front door does not mean one database. Authority remains deliberately separated:

- **Registry Plane:** which automation definitions may run;
- **Knowledge Plane:** which information is trusted, current, and reviewed;
- **Ticketing Plane:** which work exists and authorizes action;
- **Process run ledger:** how a conducted run advances and completes; and
- **human authority:** which reserved decisions a person may approve.

### Accountability for people and agents

The target model applies the same durable work, identity, evidence, and audit requirements to human and machine actors. Agents may orient, research, build, test, validate, and request progression. They do not create their own authority.

The intended chain is:

`strategic intent → authorized work → actor and capability → conducted run → evidence → outcome → human promotion where required`

### Evidence-backed completion

HATHOR is designed to replace narrative declarations of “done” with a system-evaluated transition. A conductor owns run state; agents and bots submit requests; validation, assumptions, claims, required work, and evidence are reconciled before finalization.

This is a target design. Claims that HATHOR currently prevents skipped work or false completion require implementation and negative-test evidence.

### Governed, replaceable automation

The accepted architecture enumerates 26 single-purpose microbots across orchestration, information hierarchy, validation, and observation. Each target unit has a bounded responsibility, a versioned capability contract, explicit governance, an externalized state model, and a controlled create-to-retire lifecycle.

The business intent is to reduce hidden coupling and blast radius: capabilities can be changed, quarantined, replaced, or retired without making private component state the organization’s memory.

### Brokered external access

The accepted brokering model keeps long-lived provider credentials away from worker bots. External calls are proxied by default through Operator; narrow, short-lived, run-bound token handoff is an explicit exception where proxying is impractical.

The objective is lower credential distribution and better attribution of third-party effects. Production-grade claims require fault-injection, idempotency, persistence, and recovery evidence.

## Intended outcomes

| Outcome theme | Intended business effect | Target mechanism |
|---|---|---|
| Accountability | Trace substantive activity to purpose, authorization, actor, evidence, and outcome | Work, hierarchy, run, and audit linkage |
| Assurance | Reduce unsupported completion and evidence reconstruction | Conducted runs, validation, claims, assumptions, reconciliation |
| Human control | Preserve people’s decision rights at high-risk boundaries | Human-bound waiver, knowledge promotion, and deployment authority |
| Portability | Keep governance stable across tools and agent harnesses | Provider-neutral contracts and capability routing |
| Credential control | Reduce secret distribution across worker automation | Brokered provider access and scoped exceptions |
| Trusted knowledge | Turn project and organizational knowledge into a governed asset | Provenance, status, freshness, tiered retrieval, human promotion |
| Continuity | Continue bounded work through outages without silently inventing authority | Cached trust, backup work capture, visible degradation, reconciliation |
| Economic visibility | Make cost, retries, latency, and quality observable per run | Passive observation and bounded ledgers |

These are value hypotheses until measured in a pilot.

## Who benefits

### Executive and portfolio leaders

- clearer lineage from strategic initiative to delivered outcome;
- measurable control and value hypotheses instead of generic productivity claims;
- explicit decisions about risk appetite, human authority, and expansion; and
- a governed path for scaling delegated work.

### Engineering and platform leaders

- a common contract across repositories, languages, providers, and agent harnesses;
- standardized project orientation and structured remediation;
- provider-neutral work and knowledge interfaces; and
- independently replaceable automation capabilities.

### Security, risk, compliance, and audit

- explicit trust and authority boundaries;
- centralized capability provenance, revocation, identity, and brokered effects;
- separation of duties for promotion and exception; and
- a reconstructable evidence model with stated residual risk.

### Developers, operators, and knowledge owners

- predictable orientation and command behavior;
- actionable refusals rather than silent failure;
- bounded outage behavior;
- human review of durable knowledge; and
- retained human authority for higher environments.

## Target v1 scope

The current sources describe a target that includes:

- a bounded `hath0r` CLI and common output/error contract;
- a universal project layout;
- signed definitions, registration, revocation, and offline-verifiable trust material;
- a canonical 26-bot roster and shared bot lifecycle;
- central, event-triggered conducted runs;
- sequence, evidence, claims, assumptions, and completion controls;
- Jira, Azure DevOps, GitHub, and minimal backup ticketing adapters;
- tiered knowledge storage, retrieval, and human promotion;
- brokered third-party integrations;
- spool-and-drain observation and Tower rollups;
- container classes and build/deployment governance; and
- macOS and Linux clients, with an EKS deployment direction for higher environments.

The detailed implementation of many of these capabilities remains draft.

## Out of scope or not established

The sources do not establish:

- a production-ready release;
- a browser-based Control Tower UI in v1;
- multi-tenant SaaS operation;
- Windows client support;
- autonomous waivers, knowledge verification, or production promotion;
- replacement of enterprise trackers or agent harnesses;
- prevention against a fully adversarial local process;
- compliance certification;
- customer deployments, references, or case studies;
- commercial packaging, pricing, support terms, or SLAs; or
- realized business benefit or ROI.

## Material risks and open decisions

Before strong assurance or operational claims, the program must resolve and verify:

- binding executable or image bytes to the signed capability definition;
- the detailed human identity-token claims, audience, action, run binding, expiry, and replay rules;
- authenticated event-emitter policy;
- complex process-graph loop and attempt semantics;
- authoritative run-ledger durability versus telemetry export;
- reconciliation of out-of-process effects;
- Operator persistence, high availability, and crash recovery;
- evidence, telemetry, and knowledge retention and access;
- knowledge confidence calibration;
- four-eyes approval scope; and
- accountable product, service, control, risk, and support ownership.

## Recommended evaluation

Start with one team, one or two repositories, one primary tracker, repeatable development workflows, and no critical production dependency. Establish a baseline, introduce report-only controls, validate negative and recovery paths, then selectively enforce only the controls that produce actionable outcomes within agreed friction.

Expansion should require:

`accepted design + authorized implementation + passing tests + ready owners + prepared users + accepted risk + measured value`

## Source foundation

Primary sources:

- [Business Executive Overview](../business/01-executive-overview.md)
- [Business Requirements](../business/02-business-requirements.md)
- [Architecture Corpus Index](../architect/INDEX.md)
- [Central Orchestration Decision](../architect/hathor-adr-002-orchestration-coordination-model-20260913.md)
- [Greenfield Command Surface Decision](../architect/hathor-adr-003-greenfield-command-surface-20260913.md)
- [Threat Model](../architect/hathor-rp-013-threat-model-20260913.md)
- [Bot Unit Model](../architect/hathor-rp-014-bot-unit-creation-operation-20260913.md)
- [Platform Roadmap](../architect/hathor-plan-001-platform-roadmap-20260913.md)
