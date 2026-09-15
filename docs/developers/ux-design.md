---
id: AEGIS-GUIDE-036
title: "UX/Design Guide"
summary: "How UX and Design shape AEGIS agent/CLI experiences around envelopes, gates, trust tiers, and honest degradation."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [ux, design, cli, agents, trust]
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
sources: [AEGIS-CANON-002, AEGIS-ADR-003, AEGIS-RP-004, AEGIS-RP-012, AEGIS-CANON-001, AEGIS-GUIDE-011]
---
# UX/Design Guide

As a UX Designer on AEGIS/HATHOR, your primary surfaces are often **CLI envelopes, agent workflows, and Control Tower-facing status** — not only graphical UI. Design for refusal, provenance, and degradation as first-class states.

## 1. Design Principles (Productized)

Anchor flows in platform principles (AEGIS-CANON-002) and the agent integrator model (AEGIS-GUIDE-011):

* **CLI as control plane** — one place to elevate trust (`guest → elevated → sovereign`) and mediate credentials (AEGIS-ADR-003).
* **Local context wins** — project truth before generic model memory; show *where* an answer came from.
* **Provenance over vibes** — cite article/doc IDs, run IDs, ticket keys in human-readable summaries.
* **Degrade, don’t die** — missing Tower/MCP/org services remain operable with explicit trust loss.
* **Secure by mediation** — never coach users to paste secrets into prompts or source trees.

## 2. Information Architecture: Planes and Trust

Make the three planes legible in IA and empty states:

| Plane | User question | UX must show |
| --- | --- | --- |
| Registry | Can this run? | Capability, version, signature/verify state |
| Knowledge | Is this true enough? | draft / verified, tier (project→public), stale/TTL |
| Ticketing | Am I allowed to change this? | ticket/Epic binding, degraded adapter state |

Knowledge promotion is human-gated (AEGIS-RP-004 / AEGIS-RP-012). UI copy must never imply auto-verify.

## 3. Designing Gate Refusals

Governance Gates will refuse work (AEGIS-CANON-001). Treat refusal UX as a happy path for integrity:

* Surface the structured envelope fields: `code`, `message`, `remediation`, `provenance`, `ttl`.
* Map CLI exit codes to consistent severity and next actions (`2` validation vs `4` auth vs `7` needs confirmation).
* Prefer actionable remediation (“link ticket KEY”, “re-run linter X”) over generic failure toast.
* Dry-run plans should be visually distinct from live mutations; require explicit confirm (`--yes` equivalent) for non-idempotent acts.

## 4. Agent-Facing Experience

* Universal Project Layout and nearest-first `AGENTS.md` are navigation UX — keep labels stable; do not invent parallel hidden trees (no `.infraOS/`).
* Microburst knowledge writes: design session-scoped capture, not bulk “sync everything” affordances.
* Branch/PR naming `feature/<KEY>-<initials>-<slug>` should be guided in templates, not only documented.
* Promotion path CR-BAI-001 should appear in release/checklists UX as a stepper that cannot skip stages.

## 5. Visual or Console UI (When Present)

* Status chips for trust: `unverified` / `machine-checked` / `human-reviewed` (docs) and knowledge `draft` / `verified`.
* Offline badge when operating inside trust TTL; stronger warning after `PROVENANCE_UNVERIFIED`.
* Class taxonomy (A–D containers) only where operators need it — hide worker-secret absence as a positive guarantee, not a missing feature.
* Accessibility: machine-readable JSON and human text are dual outputs; neither is optional for the primary operator journeys.

## 6. Definition of Done (UX)

1. Every critical flow shows plane + trust + ticket context or why it is N/A.
2. Refusal and degraded states designed, copied, and tested — not only success.
3. No design that requires secret exfiltration or gate bypass.
4. Agent and human paths share vocabulary with role guides and CANON IDs.
