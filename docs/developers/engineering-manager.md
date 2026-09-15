---
id: HATHOR-GUIDE-035
title: "Engineering Manager Guide"
summary: "How Engineering Managers run AEGIS delivery through tickets, gates, validation altitudes, and honest promotion without heroics."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [engineering-management, delivery, gates, teams]
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
sources: [HATHOR-CANON-010, HATHOR-CANON-011, HATHOR-RP-007, HATHOR-TS-001, HATHOR-RP-014, HATHOR-GUIDE-011, HATHOR-GUIDE-014]
---
# Engineering Manager Guide

As an Engineering Manager in AEGIS, you optimize for **mechanical integrity under delivery pressure**. Throughput that skips tickets, linters, or promotion stages is regression, not velocity.

## 1. Operating Model You Staff For

Staff and review work against the platform shape (HATHOR-GUIDE-014, HATHOR-GUIDE-011):

* **Single CLI control plane** — agents and humans share `aegis` contracts (exit codes, JSON envelopes, dry-run).
* **Orchestration split** — events append; Process-Bot alone advances run state; Proctor enforces gates.
* **Bot unit discipline** — new bots follow seven-block anatomy and Manifest v1 (HATHOR-RP-014).
* **Four validation altitudes** — build, change, dispatch, runtime (HATHOR-RP-007 / HATHOR-TS-001).

Your 1:1s and planning rituals should name which altitude or plane a workstream hardens.

## 2. Tickets, WIP, and Agent Labor

* **No-Ticket Gate is a management control:** if engineers or agents routinely need bypasses, the backlog or estimation policy is wrong — fix the system of work.
* Require Epic linkage, named estimation policy fields, and PR names `feature/<KEY>-<initials>-<slug>`.
* Agents are capacity, not an escape hatch: they still hit Governance Gates and must remediate from JSON `remediation` fields.
* Bound WIP to what QA and Release can evidence on the CR-BAI-001 path.

## 3. Quality Bar Without Hero Culture

| Signal | Healthy | Unhealthy |
| --- | --- | --- |
| Gate refusal | Fixed and re-run | Bypassed or “run locally with force” |
| Knowledge | Draft then verified | Paste into chat as source of truth |
| Secrets | Operator-Bot / IRSA | Keys in repo or agent logs |
| Promote | Stage-by-stage with URL checks | Hotfix to `master` |
| Offline Tower | TTL degradation observed | Fake authority from stale MBI |

Reward the left column in performance conversations.

## 4. Team Topology Hints

* **Platform Engineers** own CLI, chassis, gates, Control Tower API lean surface.
* **Bot Developers** own Class C workers — stateless, zero secrets, contract commands.
* **DevOps/DVO** own topology, spool-and-drain, authorized deploys.
* **QA** owns altitude coverage and promotion evidence quality.
* **Security** owns control mapping and exception expiry.
* Cross-cut: every squad can explain Registry vs Knowledge vs Ticketing impact of their epic.

## 5. Risk and Continuity

* Control Tower downtime is expected in design: plan reviews must include trust TTL and `PROVENANCE_UNVERIFIED` behavior.
* Telemetry must not block primary execution; spool quotas are capacity planning inputs, not “someone else’s pager only.”
* Documentation and ADRs are delivery artifacts: unstable IDs or unreviewed canon are delivery risks (HATHOR-CANON-011).

## 6. Definition of Done (EM)

1. Epic outcomes map to planes/gates; owners named per stage of promotion.
2. Team Definition of Done includes ticket, linters, dry-run, and evidence links.
3. No standing gate bypasses; exceptions ticketed with expiry.
4. Agent/human onboarding points at role guides under `docs/developers/` and nearest `AGENTS.md`.
