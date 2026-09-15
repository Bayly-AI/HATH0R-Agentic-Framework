---
id: AEGIS-GUIDE-030
title: "QA/Test Engineer Guide"
summary: "How QA and Test Engineers exercise AEGIS validation altitudes, refuse bad claims, and keep promotion evidence honest."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [qa, testing, validation, gates]
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
sources: [AEGIS-CANON-001, AEGIS-CANON-002, AEGIS-RP-007, AEGIS-TS-001, AEGIS-ADR-003, AEGIS-GUIDE-013]
---
# QA/Test Engineer Guide

As a QA or Test Engineer on AEGIS, you do not “hope the build is green.” You exercise the four-altitude validation fabric, treat refusals as success when they protect integrity, and attach evidence to tickets before any environment promote.

## 1. Your Place in the Validation Fabric

AEGIS continuous validation is specified across altitudes (AEGIS-RP-007, AEGIS-TS-001):

1. **Build-Time (1):** Micro-linters are pure and exit `0|2`. Un-linted images must fail the build.
2. **Change-Time (2):** Micro-linters plus validator bots (`val-*`) refuse bad changes, assumptions, or claims.
3. **Dispatch-Time (3):** Proctor gates (G01–G09 and the broader 15 Governance Gates in AEGIS-CANON-001 §2) refuse unlawful dispatch.
4. **Runtime (4):** Observation family records only — never refuses.

Your job is to design suites that *prove* each altitude still holds, not to bypass them with privileged scripts.

## 2. Ticketing Plane: Evidence, Not Vibes

* **No-Ticket Gate:** Substantive test automation changes, fixture data that affects shared environments, and promotion sign-offs require an authorized ticket linked to an Epic.
* **Commands:** Prefer `aegis work ...` and `aegis process ...` over ad-hoc shell when mutating project state.
* **Evidence on the record:** Attach run IDs, validator outputs, and URL checks to the ticket. Observation rollups live on the record; chat paste is not provenance (AEGIS-CANON-002 HP-11/HP-12).
* **Promotion path (CR-BAI-001):** `local → development → testing → staging → master (Production)`. You own the *testing* gate quality bar: deploy + URL validation must pass before Release/DVO promote further (see AEGIS-GUIDE-013).

## 3. CLI Contracts and Exit Codes

Drive verification through the `aegis` CLI (AEGIS-ADR-003 command surface):

* Use `--output=json` (or pipe auto-detection) and assert on structured envelopes `{code, message, remediation, provenance, ttl}`.
* Treat CLI exit codes as the public contract: `0` success, `1` runtime, `2` usage/validation, `3` not found, `4` auth, `5` conflict, `6` dependency unhealthy, `7` confirmation required.
* Bot under test must honor bot exit boundaries `0|1|2` (degraded). Map and assert the CLI envelope, not free-form stderr.

Always start non-idempotent verification with `--dry-run`, then `--yes` only when the plan matches the ticket.

## 4. What to Test by Plane

* **Registry / Control Tower:** Offline verification of signed manifests and keys; TTL expiry degrades to `PROVENANCE_UNVERIFIED` without inventing authority.
* **Knowledge Plane (AEGIS-RP-004 / AEGIS-RP-012):** Drafts are invisible without `--include-drafts`; no auto-promotion to `verified`; secrets/PII scanners must block promotion.
* **Ticketing adapters:** Authority reconciliation (upstream wins), buffered/`degraded: true` states, and UUIDv7 dedupe on reconnect.
* **Telemetry spool:** JSONL Event Envelope v1; spool quotas (warn/shed/hard-stop) must not block primary execution under load tests.

## 5. Working with Agents and Bots

* Agents and bots are subjects under test, not privileged oracles. Refuse “the model said it passed.”
* Class C worker bots: zero baked secrets, `/health` + `/version`, stateless between invocations.
* When Proctor or a validator refuses, read `remediation`, fix the cause, re-run — do not open a backdoor path around the gate.

## 6. Definition of Done (QA)

1. Ticket authorized; branch naming `feature/<KEY>-<initials>-<slug>` when code changes ship.
2. Build-time micro-linters clean; change-time validators green or intentionally refused with ticket notes.
3. Dispatch-time dry-run plan reviewed; live run IDs cited.
4. Environment URL/health checks recorded for the stage under test.
5. Knowledge or claims introduced by the change are draft-or-verified explicitly — never silently trusted.
