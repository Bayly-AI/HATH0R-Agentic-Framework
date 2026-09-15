---
id: AEGIS-CANON-007
title: AEGIS Developer Documentation
summary: Welcome to the AEGIS Developer Documentation. This section provides technical guidance for building, integrating, and operating the AEGIS agentic governance platform and the HATHOR framework.
doc_type: CANON
diataxis: reference
audience: [developer, agent]
tags: []
version: 0.1.0
status: draft
created: '2026-09-14'
updated: '2026-09-15'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: 365d, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# AEGIS Developer Documentation

Welcome to the AEGIS Developer Documentation. This section provides technical guidance for building, integrating, and operating the AEGIS agentic governance platform and the HATHOR framework. 

To ensure you find the most relevant technical details for your tasks, this documentation is organized by **Developer Role**.

## Role-Based Guides

* **[Bot Developer](bot-developer.md)** (`AEGIS-GUIDE-012`)
  For developers building and maintaining AEGIS micro-bots. Covers Bot Anatomy, Manifest v1, standard CLI contracts, stateless execution, and Class C containerization.

* **[Agent Integrator](agent-integrator.md)** (`AEGIS-GUIDE-011`)
  For developers and AI agents interacting with the AEGIS platform. Covers navigating the Universal Project Layout (`.aegis/`), interacting with the Ticketing and Knowledge planes, and executing runs via the `aegis` CLI.

* **[Platform Engineer](platform-engineer.md)** (`AEGIS-GUIDE-014`)
  For core engineers developing the `aegis` CLI, the Go bot chassis, Orchestration bots (Proctor, Process, Operator), Governance Gates, and Control Tower APIs.

* **[DevOps & DVO (Deployment & Validation Operator)](devops-dvo.md)** (`AEGIS-GUIDE-013`)
  For operators managing the deployment topology. Covers the Class A-D container taxonomy, EKS deployments, spool-and-drain telemetry, and ticket-authorized promotion paths.

* **[QA / Test Engineer](qa-test-engineer.md)** (`AEGIS-GUIDE-030`)
  For engineers exercising the four-altitude validation fabric, ticket-backed evidence, and promotion URL checks without bypassing gates.

* **[Product Manager](product-manager.md)** (`AEGIS-GUIDE-031`)
  For PMs authorizing work on the Ticketing Plane, shaping roadmap against Registry/Knowledge/Ticketing impacts, and insisting on provenance for claims.

* **[Release Manager](release-manager.md)** (`AEGIS-GUIDE-032`)
  For release owners running CR-BAI-001 stage promotion with DVO tickets, dry-run playbooks, and deploy+URL validation at each hop.

* **[Security & Compliance Officer](security-compliance-officer.md)** (`AEGIS-GUIDE-033`)
  For security/compliance mapping Governance Gates and zero-secret invariants to auditable controls and time-boxed exceptions.

* **[Technical Writer](technical-writer.md)** (`AEGIS-GUIDE-034`)
  For writers authoring `hathor-doc@1` corpus docs, stable IDs, Diátaxis modes, and Knowledge Plane–aligned trust/staleness.

* **[Engineering Manager](engineering-manager.md)** (`AEGIS-GUIDE-035`)
  For EMs staffing delivery around planes, gates, bot unit discipline, and healthy responses to refusals—not bypass culture.

* **[UX / Design](ux-design.md)** (`AEGIS-GUIDE-036`)
  For designers shaping CLI/agent experiences where envelopes, trust tiers, degradation, and gate remediation are first-class states.

## Core Architectural Concepts (TL;DR)

AEGIS is built on strict boundaries and mechanical enforcement:
* **Single CLI Control Plane:** Every action flows through the `aegis` CLI.
* **Three Planes of Authority:** Registry (what can run), Knowledge (what we know), Ticketing (what work exists).
* **Zero Baked Secrets:** Operator-Bot brokers external connections; OTel Collector brokers telemetry. Worker bots (Class C) have zero secrets.
* **No Auto-Promotion:** Knowledge and deployment promotions always require human-executed authorization.
* **Bounded Offline Trust:** Systems degrade gracefully with a trust TTL when the Control Tower is unreachable.
