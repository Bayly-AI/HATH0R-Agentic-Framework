---
id: HATHOR-GUIDE-033
title: "Security & Compliance Officer Guide"
summary: "How Security and Compliance Officers use HATHOR gates, zero-secret invariants, and knowledge trust tiers as mechanical controls."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [security, compliance, secrets, provenance]
version: 0.1.1
status: draft
created: 2026-09-15
P26-09-19
owner: "Raymond Bayly (BaylyAI)"
review:
  trust: unverified
  reviewed_by: null
  reviewed_at: null
  interval: 180d
  next_review: null
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: [HATHOR-CANON-010, HATHOR-CANON-011, HATHOR-RP-004, HATHOR-RP-012, HATHOR-RP-007, HATHOR-GUIDE-013, HATHOR-ADR-003]
---
# Security & Compliance Officer Guide

As a Security or Compliance Officer, you treat HATHOR Governance Gates, credential mediation, and knowledge promotion as **controls**, not documentation theater. Your how-to is: verify the control still fires, evidence it on the ticket, and refuse silent exceptions.

## 1. Non-Negotiable Invariants

* **Zero baked secrets:** Class C worker bots and ECR images carry no long-lived credentials. Operator-Bot brokers external effects; Class D OTel holds telemetry-backend credentials only (HATHOR-GUIDE-013).
* **CLI mediation:** Credential lookup order is policy-owned (Secrets Manager → user credentials → project `.env` → allowed siblings). Agents request capability through the CLI; they do not scrape keys (repo-root HATHOR README / HATHOR-ADR-003).
* **No auto-promotion:** Knowledge draft→verified and environment promotion always require human authorization (HATHOR-RP-004; CR-BAI-001).
* **Provenance over recency:** Prefer attributable, reconstructable evidence (HATHOR-CANON-011 HP-11/HP-12).

## 2. Gates as Controls (Map Them)

Use the 15 Governance Gates (HATHOR-CANON-010 §2) and validation altitudes (HATHOR-RP-007) as your control catalog:

| Control intent | Mechanical surface |
| --- | --- |
| Change authorization | No-Ticket Gate; Epic linkage |
| Supply chain / build integrity | Build-time micro-linters; “nothing un-linted gets containerized” |
| Unlawful dispatch | Proctor G01–G09; Sequence/Barrier gates |
| Claim hygiene | Change-time `val-*` bots; secrets/PII scanners on knowledge promotion |
| Runtime honesty | Observation records only; spool quotas prevent disk wipeout |

Compliance evidence = run IDs + ticket keys + signed manifests — not screenshots of chat.

## 3. Knowledge Plane Compliance

* New knowledge is **draft**, session-scoped microbursts only; bulk sync is forbidden (HATHOR-RP-012).
* Promotion to **verified** requires human review **and** mechanical gates (secrets/PII). Fail closed.
* Retrieval trust tiers: Project → Machine → Organization → Public. Lower tiers must not silently override higher trust without citation.
* Stale/TTL flags force intentional use; do not allow “still online” to mean “still approved.”

## 4. Ticketing, Audit, and Exceptions

* Every exception is a ticket with owner, expiry, compensating control, and stage scope. Open-ended waivers are defects.
* Upstream ticketing systems win on authority reconciliation; local buffer may show `degraded: true` — document that in audits.
* Control Tower is authoritative for registry, policy, identity, revocation, ingest, and audit query. It is **not** a bot and not the terminus of every request — design reviews accordingly.
* Offline mode: trust TTL expiry must surface `PROVENANCE_UNVERIFIED`. Continuity plans cannot assume infinite local authority.

## 5. Container and Runtime Reviews

* Class A terminates agent traffic; Class B stateful knowledge stores need backup/policy review; Class C zero-secrets; Class D telemetry credentials isolated.
* Require `/health` and `/version` on deployable images.
* IRSA / EKS Pod Identity and secret mounts over embedded env in images.

## 6. Definition of Done (Security)

1. Controls mapped to gates/linters with ticket-traceable test or audit samples.
2. No new secret material in `SRC`, agent transcripts, or Class C images.
3. Knowledge and env promotions human-authorized with scanner evidence.
4. Exceptions time-boxed; Control Tower revocation/CRL path understood for the change.
