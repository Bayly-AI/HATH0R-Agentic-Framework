# AEGIS Developer Documentation

Welcome to the AEGIS Developer Documentation. This section provides technical guidance for building, integrating, and operating the AEGIS agentic governance platform and the HATHOR framework. 

To ensure you find the most relevant technical details for your tasks, this documentation is organized by **Developer Role**.

## Role-Based Guides

* **[Bot Developer](bot-developer.md)**
  For developers building and maintaining AEGIS micro-bots. Covers Bot Anatomy, Manifest v1, standard CLI contracts, stateless execution, and Class C containerization.
  
* **[Agent Integrator](agent-integrator.md)**
  For developers and AI agents interacting with the AEGIS platform. Covers navigating the Universal Project Layout (`.aegis/`), interacting with the Ticketing and Knowledge planes, and executing runs via the `aegis` CLI.

* **[Platform Engineer](platform-engineer.md)**
  For core engineers developing the `aegis` CLI, the Go bot chassis, Orchestration bots (Proctor, Process, Operator), Governance Gates, and Control Tower APIs.

* **[DevOps & DVO (Deployment & Validation Operator)](devops-dvo.md)**
  For operators managing the deployment topology. Covers the Class A-D container taxonomy, EKS deployments, spool-and-drain telemetry, and ticket-authorized promotion paths.

## Core Architectural Concepts (TL;DR)

AEGIS is built on strict boundaries and mechanical enforcement:
* **Single CLI Control Plane:** Every action flows through the `aegis` CLI.
* **Three Planes of Authority:** Registry (what can run), Knowledge (what we know), Ticketing (what work exists).
* **Zero Baked Secrets:** Operator-Bot brokers external connections; OTel Collector brokers telemetry. Worker bots (Class C) have zero secrets.
* **No Auto-Promotion:** Knowledge and deployment promotions always require human-executed authorization.
* **Bounded Offline Trust:** Systems degrade gracefully with a trust TTL when the Control Tower is unreachable.
