---
id: HATHOR-CANON-005
title: "HATHOR Corpus — Pending-Edits & Change-Control Register"
summary: "Cross-document amendments and decision sign-offs for the OpenSource documentation corpus."
doc_type: CANON
diataxis: reference
audience: [architect, agent]
tags: [governance, change-control]
version: 0.2.0
status: draft
created: 2026-09-15
updated: 2026-09-15
owner: "Raymond Bayly (BaylyAI)"
review:
  trust: unverified
  reviewed_by: null
  reviewed_at: null
  interval: 365d
  next_review: null
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: [HATHOR-CANON-001]
---
# HATHOR Corpus — Pending-Edits & Change-Control Register

Purpose: track cross-document amendments and decision sign-offs for the OpenSource documentation corpus.

Status legend: **proposed** · **applied** · **accepted** · **external**

## 1. Decisions

| Item | Document | What sign-off would ratify | Status |
|---|---|---|---|
| D1 | HATHOR-CANON-001 | `hathor-doc@1` metadata schema; ID/version/review/stale/index model; `HT-DOC-###` requirements; docs-as-code linters | proposed (issue #5; corpus landed via PR #8) |
| D2 | ID namespace | Live corpus document IDs are `HATHOR-*`; archive retains `AEGIS-*` provenance | **applied 2026-09-15 (issue #12)** |
| N1 | Adoption notice | Team notified via issue #18 + HATHOR-REPORT-001 adoption summary | **applied 2026-09-15 (issue #18)** |

## 2. Applied amendments

| Target | Edit | Owner | Status |
|---|---|---|---|
| Live `docs/**` | Remap document IDs `AEGIS-<TYPE>-…` → `HATHOR-<TYPE>-…`; special CANON map 001/002/003 → 010/011/012 to protect `HATHOR-CANON-001` | issue #12 | **applied** |
| Tree INDEX.md | Full document tables for architect/business/developers/sales | issue #12 | **applied** |
| `docs/index.json` + `llms.txt` | Regenerated from front-matter | issue #12 | **applied** |
| `archive/**` | Provenance policy: frozen AEGIS-era snapshot; not re-ID'd | issue #12 | **applied** |
| `id-namespace-map-20260915.json` | Machine-readable AEGIS→HATHOR map | issue #12 | **applied** |

## 3. Open follow-ups

| Item | Action | Owner |
|---|---|---|
| D1 sign-off | Operator ratify HATHOR-CANON-001 | operator |
| Tooling | `ml-doc-*` linters + gen-index automation | operator |
| Filename hygiene | Optional later rename `aegis-*.md` filenames (IDs already HATHOR; filenames may stay for link stability) | authors |

---

*Last updated: 2026-09-15 — adoption summary HATHOR-REPORT-001 + team notice #18. Prior:  2026-09-15 — D2 ID/index/archive normalization applied (issue #12).*
