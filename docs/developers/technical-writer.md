---
id: AEGIS-GUIDE-034
title: "Technical Writer Guide"
summary: "How Technical Writers author hathor-doc@1 corpus docs, keep IDs stable, and align docs with Knowledge Plane trust."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [documentation, hathor-doc, diataxis, knowledge]
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
sources: [AEGIS-CANON-003, AEGIS-CANON-001, AEGIS-RP-004, AEGIS-RP-012, AEGIS-GUIDE-029]
---
# Technical Writer Guide

As a Technical Writer on AEGIS/HATHOR, you author **one artifact for two readers**: humans and agents. The contract is `hathor-doc@1` (AEGIS-CANON-003). You do not maintain a separate “agent copy” of the same page.

## 1. Corpus Rules You Enforce

* **In scope:** `docs/architect/**`, `docs/business/**`, `docs/developers/**`, `docs/sales/**`, repo-root `README.md`.
* **Out of scope for front-matter:** `AGENTS.md` (nearest-first instruction files), runtime Knowledge records, generated API bodies beyond their header/index entry.
* **Stable IDs:** `AEGIS-(ADR|RP|TS|PLAN|REQ|ARCH|CANON|GUIDE|REPORT|SESSION)-NNN`. Never reuse requirement-style prefixes (`AEG-…`) as document IDs (AEGIS-CANON-001 §8).
* **Diátaxis:** Prefer a single mode (`tutorial|how-to|reference|explanation|decision`). `mixed` needs a one-line justification in the first body section.

## 2. Front-Matter Checklist (every new doc)

Required: `id`, `title`, `summary`, `doc_type`, `diataxis`, `audience`, `version`, `status`, `created`, `updated`, `owner`, `review.trust`, `review.interval`.

Typical writer defaults for role/how-to guides:

* `doc_type: GUIDE`, `diataxis: how-to`
* `audience: [developer, agent]` (adjust by tree)
* `status: draft`, `version: 0.1.0` until reviewed
* `review.trust: unverified` until a human end-to-end review
* `sources: [...]` cite canon/RP/TS IDs you relied on

Run from repo root:

```bash
python3 bin/docs/ml-doc-frontmatter docs/developers/your-doc.md
python3 bin/docs/ml-doc-links docs/developers/your-doc.md
```

## 3. Body Craft for Agents and Humans

* Lead with a one-sentence purpose that can feed `summary` and INDEX/llms.txt.
* Prefer **cite-by-ID** (`AEGIS-RP-012`) over brittle path-only references when the concept is canonical.
* Keep local markdown links resolvable; CI `ml-doc-links` fails dead paths.
* Do not put secrets, tokens, or live credentials in docs. Describe mediation order instead (AEGIS-GUIDE-029).
* Dual header: YAML is canonical; a human bulleted header MAY mirror it for long canon papers — do not fork meaning between them.

## 4. Knowledge Plane Alignment

Authored docs and runtime knowledge share vocabulary (AEGIS-RP-004 / AEGIS-RP-012):

* Docs lifecycle: draft → proposed → accepted (and superseded/retired).
* Knowledge trust: draft → verified with **no auto-promotion**.
* Staleness/TTL: set honest `review.interval`; let CI mark `stale` rather than pretending freshness.
* When promoting doc insight into `.aegis/knowledge/`, keep `status: draft` until human review; `source:` must point at the docs path.

## 5. Change Control and Indexes

* Structural type/status/field changes amend AEGIS-CANON-003 in the same change.
* Human `INDEX.md` files keep curated prose; optional `<!-- BEGIN:hathor-doc-list -->` regions may be machine-maintained.
* `docs/index.json` / tree `llms.txt` are generated (`bin/docs/gen-index`) — do not hand-edit as source of truth.
* Ticket your doc changes like code: no-ticket gate still applies to substantive corpus mutations executed by agents.

## 6. Definition of Done (Writer)

1. `hathor-doc@1` valid; ID unique; links resolve.
2. Diátaxis mode matches the reader’s job-to-be-done.
3. Sources and relationships filled for non-trivial papers.
4. INDEX entry (or marked list region) updated for new files.
5. Trust tier honest (`unverified` until reviewed).
