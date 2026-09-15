---
id: AEGIS-GUIDE-032
title: "Release Manager Guide"
summary: "How Release Managers run ticket-authorized, gate-enforced promotion along the AEGIS environment path without skipping stages."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [release, promotion, dvo, gates]
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
sources: [AEGIS-CANON-001, AEGIS-CANON-002, AEGIS-RP-007, AEGIS-TS-001, AEGIS-GUIDE-013, AEGIS-ADR-003]
---
# Release Manager Guide

As a Release Manager, you choreograph *authorized* movement of change across environments. AEGIS treats promotion as a governed operation: ticket first, validate at every altitude, never skip CR-BAI-001 stages.

## 1. Canonical Promotion Path

Required order (never skip):

```text
local → development → testing → staging → master (Production)
```

* PRs into `testing` only from `development`.
* PRs into `staging` only from `testing`.
* PRs into `master` only from `staging`.
* Each stage needs **deploy + URL validation** before the next promote.

CI enforcement lives in `.github/workflows/enforce-promotion-path.yml`. Treat failures as hard stops, not warnings.

## 2. Ticketing and DVO Authority

* **Human-executed promotion:** Higher environments require a DVO/deploy ticket you (or the designated operator) authorize; the system executes (AEGIS-GUIDE-013).
* **Agents do not promote:** Agents build and verify locally/development. They must not deploy testing→prod.
* **No-Ticket Gate:** Release trains without an authorized ticket are refused at dispatch (AEGIS-CANON-001 gates).
* Keep ticket fields current: target stage, build/image digests, validation run IDs, rollback pointer.

## 3. Validation Gates Before You Cut a Release

Align the release checklist to continuous validation (AEGIS-RP-007, AEGIS-TS-001):

1. **Build-Time:** Micro-linters clean; nothing un-linted is containerized.
2. **Change-Time:** `val-*` bots and PR checks green; known refused claims documented.
3. **Dispatch-Time:** Proctor/Sequence/Barrier gates allow the release workflow only under lawful plan data.
4. **Runtime:** Observation spool draining; no silent telemetry loss at quota hard-stop without a decision.

Use `aegis process ... --dry-run` for the release playbook, then `--yes` only with ticket + plan match (AEGIS-ADR-003).

## 4. Artifacts and Provenance

* Prefer signed manifests and digests verifiable offline via Control Tower artifacts.
* Record image tags, chart versions, and config hashes on the ticket and in Knowledge as **draft** until human verification promotes them (AEGIS-RP-004).
* On Control Tower disconnect, respect trust TTL (`verified-local` → `PROVENANCE_UNVERIFIED`). Do not mint production authority from stale local cache.

## 5. Coordination with Roles

| Role | You need from them |
| --- | --- |
| Platform Engineer | Gate and CLI contracts stable for the train |
| DevOps/DVO | EKS topology, IRSA/secrets, spool capacity |
| QA | Stage URL/health evidence and altitude coverage |
| Security | Exception register empty or time-boxed |
| Engineering Manager | Scope freeze and rollback owner |

## 6. Definition of Done (Release)

1. Ticket authorized for the exact stage transition.
2. Prior stage deploy + URL validation attached.
3. Promotion PR source branch matches CR-BAI-001.
4. Rollback path tested or explicitly waived on the ticket with expiry.
5. Post-release observation check: spool drain healthy; no unresolved gate refusals left “for later.”
