---
id: HATHOR-GUIDE-031
title: "Product Manager Guide"
summary: "How Product Managers shape AEGIS work through tickets, planes of authority, and evidence-backed outcomes without bypassing gates."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [product, ticketing, roadmap, governance]
version: 0.1.0
status: draft
created: 2026-09-15
updated: 2026-09-15
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
sources: [HATHOR-CANON-010, HATHOR-CANON-011, HATHOR-ADR-003, HATHOR-RP-004, HATHOR-RP-012, HATHOR-GUIDE-011]
---
# Product Manager Guide

As a Product Manager for AEGIS/HATHOR, you steer *what* gets built by authorizing work on the Ticketing Plane and by insisting that claims, knowledge, and releases carry provenance. You do not ask engineers or agents to skip Governance Gates for speed.

## 1. Three Planes of Authority

Orient every epic to the planes (HATHOR-CANON-010 registries; HATHOR-GUIDE-011):

| Plane | Question you own | Product implication |
| --- | --- | --- |
| **Registry** | What is allowed to run? | Capabilities, manifests, and CLI surface changes are product decisions with mechanical enforcement. |
| **Knowledge** | What do we know, and at what trust? | Draft vs verified is a product trust signal, not a docs nicety (HATHOR-RP-004, HATHOR-RP-012). |
| **Ticketing** | What work exists and is authorized? | No ticket, no substantive mutation. Epics gate features; estimates live on the ticket. |

If a request cannot name its plane impact, it is not ready for an agent or engineer to execute.

## 2. Ticketing as the Product Backlog Contract

* **Authorize before build:** Every feature, spike that mutates the tree, and customer-visible claim needs an Epic-linked ticket.
* **Estimation policy:** Store base and reduced hours under a named policy on the ticket — agents and humans estimate against the same fields.
* **PR binding:** Branches/PRs follow `feature/<KEY>-<initials>-<slug>` so Control Tower and adapters can reconcile work.
* **Promotion is a product event:** CR-BAI-001 path `local → development → testing → staging → master` is non-negotiable. “Ship straight to prod” is out of contract.
* **Degraded truth:** When adapters report `degraded: true`, treat upstream systems as authoritative once reconciled — do not invent local status for stakeholders.

## 3. Knowledge and Claims

* Product copy, runbooks, and “how we work” notes enter Knowledge as **draft** microbursts; promotion to **verified** is human-gated — no auto-promotion.
* Sales or customer claims must map to evidence IDs (docs, run IDs, tickets). Prefer cite-by-ID over narrative memory (HATHOR-CANON-011).
* Stale knowledge (TTL/interval exceeded) is a product risk: schedule review rather than quietly relying on it.

## 4. CLI and Agent Operating Model

* The `aegis` CLI is the single control plane (HATHOR-ADR-003). Ask agents to plan with `--dry-run` and to surface JSON refusals, not to “just apply the change.”
* Governance Gate refusals (missing ticket, contract mismatch, failed micro-linter) are **correct behavior**. Your remediation is to fix scope, ticket, or acceptance criteria — not to request a bypass.
* Exit codes and error envelopes are part of the user-visible product for agent operators; treat breaking envelope changes as breaking API changes.

## 5. Roadmap Shaping for Platform Work

Prioritize in this order unless a ratified ADR says otherwise:

1. Integrity of gates, tickets, and secrets mediation (Class A/C boundaries).
2. Knowledge trust (draft→verified, provenance, offline TTL).
3. Operator and agent ergonomics on the CLI.
4. New capability bots only after Manifest v1, contracts, and validation hooks exist.

## 6. Definition of Done (PM)

1. Epic + tickets state outcome, non-goals, and plane impacts.
2. Acceptance criteria reference gates, environments, or knowledge trust tiers explicitly.
3. Launch notes cite document IDs and ticket keys; no unverifiable claims.
4. Promotion stage and DVO/Release owners named before “done” is declared.
