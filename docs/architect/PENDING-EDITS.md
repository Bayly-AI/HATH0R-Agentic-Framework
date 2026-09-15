# HATHOR Corpus — Pending-Edits & Change-Control Register

Purpose: track cross-document amendments and decision sign-offs for the OpenSource documentation corpus.

Status legend: **proposed** · **applied** · **accepted** · **external**

## 1. Decisions

| Item | Document | What sign-off would ratify | Status |
|---|---|---|---|
| D1 | HATHOR-CANON-001 | `hathor-doc@1` metadata schema; ID/version/review/stale/index model; `HT-DOC-###` requirements; docs-as-code linters | proposed (issue #5) |

## 2. Open follow-ups after D1

| Item | Action | Owner |
|---|---|---|
| Tooling | `ml-doc-*` linters + `gen-index` under Framework or Control Tower | operator |
| Trees | Create `docs/developers`, `docs/operators` as needed | authors |
| Migration | Front-matter migrate existing Markdown when present | authors |

---

*Last updated: 2026-09-15 — HATHOR-CANON-001 drafted as proposed.*
