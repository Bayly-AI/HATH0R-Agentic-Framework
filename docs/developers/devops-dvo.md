---
id: HATHOR-GUIDE-013
title: DevOps & DVO Guide
summary: As a DevOps Engineer or Deployment & Validation Operator (DVO), your responsibility is to manage the environments, container deployments, telemetry ingestion, and authorized promotions for the AEGIS platform.
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
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
# DevOps & DVO Guide

As a DevOps Engineer or Deployment & Validation Operator (DVO), your responsibility is to manage the environments, container deployments, telemetry ingestion, and authorized promotions for the AEGIS platform.

## 1. Container Taxonomy and Build Pipeline

AEGIS relies on a strict container taxonomy:
* **Class A (Control Plane):** CLI, Orchestration bots, MCP servers. Only these terminate agent traffic.
* **Class B (Knowledge):** Stateful stores (VectorDB, Embeddings API). Governed by backup policies.
* **Class C (Worker / Bot-Host):** Stateless micro-bots. Zero secrets.
* **Class D (Observation):** OTel Collector and consumers. Holds telemetry-backend credentials.

**Pipeline Rule:** *Nothing un-linted gets containerized.* 
Your CI/CD pipelines must enforce the Micro-Linter Gate. Any linting violation must halt the container image build. Ensure `/version` and `/health` endpoints are available on all images.

## 2. Deployment Topology (EKS)

Testing, staging, and production environments target Amazon EKS.
* **Agent Role Boundary:** Agents build and verify locally or in development. They DO NOT deploy to higher environments.
* **Environment Promotion Path (CR-BAI-001):** You must strictly enforce the following promotion path: `local → development → testing → staging → master (Production)`.
  * PRs into `testing` must come from `development`.
  * PRs into `staging` must come from `testing`.
  * PRs into `master` must come from `staging`.
  * Each stage requires deploy + URL validation before the next promote.
* **DVO Promotion:** Promotion to higher environments requires a human-executed DVO deploy ticket. You authorize the ticket; the system executes the deployment.
* **Secrets:** Use IAM Roles for Service Accounts (IRSA) / EKS Pod Identity and secret mounts. Enforce the Zero Baked Credentials invariant in ECR images.

## 3. Telemetry: Spool-and-Drain

AEGIS uses a decoupled telemetry model to ensure observability never blocks business logic.
* **Spool:** Bots append JSONL events to `.aegis/state/spool/` locally.
* **Drain:** `Observation-Bot` (or Class D OTel Collectors in EKS) tails the spool and forwards batched rollups to the Control Tower or your observability backend (e.g., OpenObserve).
* **Quotas:** The local spool obeys a strict quota (80% warn, 90% shed debug, 100% hard stop) to protect node disk space. EKS volumes should be provisioned with this in mind.

## 4. Control Tower and Degraded Operations

You operate the Control Tower. Ensure its uptime, but understand AEGIS's offline capabilities.
* **Bounded Offline Trust:** If the Tower goes down, local environments operate in `verified-local` mode until their trust TTL expires.
* **Registry (TBR):** The Tower is the authority for the registry, keys, and revocations. Local machines cache this in their Machine-Local Index (MBI).
* **Reconciliation:** Upon reconnection, the platform automatically reconciles buffered tickets, telemetry rollups, and registry CRLs. Ensure your ingests can handle UUIDv7 deduplication to achieve at-least-once delivery guarantees without duplicating data.
