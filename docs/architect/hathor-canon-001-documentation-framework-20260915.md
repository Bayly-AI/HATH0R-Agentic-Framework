---
id: HATHOR-CANON-001
title: "HATHOR Documentation Framework"
summary: "Metadata schema, IDs, versioning, review, staleness, indexing, and enforcement for OpenSource HATHOR docs (hathor-doc@1)."
doc_type: CANON
diataxis: reference
audience: [architect, developer, agent]
tags: [documentation, metadata, governance, opensource]
version: 0.1.1
status: proposed
created: 2026-09-15
updated: 2026-09-15
owner: "Raymond Bayly (BaylyAI)"
review:
  reviewed_by: null
  reviewed_at: null
  trust: unverified
  interval: 365d
  next_review: null
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# HATHOR-CANON-001 — HATHOR Documentation Framework
## Metadata Schema · Document Types · IDs · Versioning · Review & Sign-off · Staleness · Indexing · Enforcement

> Machine-readable `hathor-doc@1` front-matter (above) is the canonical header; the bulleted header (below) is the human-rendered view (§3.1). This is the first conformant example of the standard it proposes.

- **Document ID:** HATHOR-CANON-001
- **Status:** PROPOSED — awaiting operator sign-off (issue #5)
- **Version:** 0.1.1
- **Date:** 2026-09-15
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Group:** `hath0r-opensource` · Control tower: `HATH0R-CLI` · Corpus root: `docs/` in this repo
- **External standards adopted:** Diátaxis, llms.txt v2, docs-as-code, Dublin Core/PAV (mapping), SemVer 2.0.0, Keep a Changelog, RFC 2119, Nygard ADRs
- **Maintenance rule:** any paper that adds a document type, status value, review tier, or metadata field MUST amend this document in the same change
- **Scope rule:** standard/interface definition only; tooling is scheduled through an authorizing ticket

RFC 2119 keywords apply: **MUST / SHOULD / MAY**. Framework requirements use prefix `HT-DOC-###` (§13).

---

## 0. Purpose

### 0.1 Why this document
OpenSource HATHOR needs one machine-checkable contract that:

1. is **parseable by agents** and **readable by humans** from the same artifact;
2. gives every document a **version**, stable **ID**, **index** entry, and explicit **review / reviewed** mark; and
3. carries a **stale** flag so drift past a review window is intentional, not silent.

### 0.2 One-line definition
> A HATHOR document is a **UTF-8 Markdown file with a machine-readable metadata header** that carries a stable **id**, semantic **version**, **status**, explicit **review** record, and computable **staleness** — authored once for humans and agents, discoverable through a generated **index**, and governed as docs-as-code.

### 0.3 Relationship to the Knowledge Plane and instruction files
- This framework governs **authored corpus documents** under `docs/**` in `HATH0R-Agentic-Framework` and, by extension, member-repo authored docs that opt in (e.g. product READMEs when migrated).
- Runtime knowledge records under `.hath0r/knowledgebase/` (group hub) remain distinct: files-as-truth, draft→verified promotion by human review.
- **`AGENTS.md` / `WARP.md` instruction and policy files are excluded** from `hathor-doc@1`. Inventories MUST list them by exception without adding documentation front-matter.

### 0.4 Design goals (dual audience)
- **Agent-efficient:** small entry points; token-bounded index; stable IDs; YAML header parseable without a bespoke parser.
- **Human-friendly:** Diátaxis-clear modes; glanceable rendered header; predictable paths.
- **Trustworthy:** provenance, explicit review, honest staleness.
- **Cheap to keep current:** docs in VCS, PR-reviewed, CI-validated.

---

## 1. Dual-consumption model — one artifact, two readers

| Reader | Needs | How this framework serves it |
|---|---|---|
| **Human** | Orientation, rationale, right content type | Rendered header; Diátaxis mode; INDEX tables; reading order |
| **Agent** | Token-cheap discovery, precise IDs, freshness/trust | YAML front-matter; generated `index.json` + `llms.txt`; cite-by-ID; `stale` / `review.trust` |

**Principle (HT-DOC-001).** A single Markdown file MUST satisfy both readers. We do not maintain a separate human copy and agent copy; the agent view is *generated* from the same source (§9).

---

## 2. Scope of documents covered

Applies to authored documentation in the OpenSource group:

- **Canonical corpus** — `docs/**` in `Bayly-AI/HATH0R-Agentic-Framework` (this repo).
- **Opt-in member docs** — other `hath0r-opensource` products MAY adopt the same header for product guides and READMEs.
- **Repo-root authored docs** in this repo — `README.md` when migrated.

Does **not** govern: `AGENTS.md`, `WARP.md`, runtime KB records, telemetry, or source comments. Non-Markdown assets (PDF/PNG) are inventoried only.

**Private internal product trees are not OpenSource canonical sources** (group AGENTS.md cr-kb-tower-001).

---

## 3. Metadata schema (the canonical header)

### 3.1 Form: YAML front-matter is canonical; the rendered header is a view
New documents MUST start with a YAML front-matter block delimited by `---`. A human-readable bulleted header MAY follow as a rendered view and MAY be generated from front-matter.

### 3.2 Canonical front-matter (schema `hathor-doc@1`)

```yaml
---
# ---- Identity (required) ----
id: HATHOR-CANON-001
title: "HATHOR Documentation Framework"
summary: "One-sentence purpose for INDEX + llms.txt."

# ---- Classification (required) ----
doc_type: CANON          # §4.1
diataxis: reference      # §4.2
audience: [architect, agent]
tags: [documentation]

# ---- Versioning & status (required) ----
version: 0.1.0           # SemVer §6
status: proposed         # §7.1
created: 2026-09-15
updated: 2026-09-15

# ---- Ownership & review (required) ----
owner: "Raymond Bayly (BaylyAI)"
review:
  reviewed_by: null
  reviewed_at: null
  trust: unverified      # §7.3
  interval: 365d         # §8.3
  next_review: null

# ---- Freshness (managed; may be CI-set) ----
stale: false             # §8

# ---- Relationships (optional) ----
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
```

### 3.3 Field requirements
- **Required:** `id`, `title`, `summary`, `doc_type`, `diataxis`, `audience`, `version`, `status`, `created`, `updated`, `owner`, `review` (with `trust` and `interval` at minimum). **HT-DOC-002**.
- **Conditionally required:** `superseded_by` when `status: superseded`; `supersedes` on the replacing doc.
- **Optional:** `tags`, `amended_by`, `parent`, `sources`, plus producer-defined keys (consumers MUST preserve unknowns).

### 3.4 Dublin Core / PAV mapping (non-binding)
`id→dc:identifier`, `title→dc:title`, `summary→dc:description`, `doc_type→dc:type`, `created→dc:created`, `updated→pav:lastUpdateOn`, `owner→dc:creator`, `reviewed_by→pav:curatedBy`, `superseded_by→dc:isReplacedBy`, `supersedes→dc:replaces`, `sources→dc:source`, `version→pav:version`.

---

## 4. Document types and content architecture

### 4.1 Corpus document-type registry (`doc_type`)

| `doc_type` | Meaning | Immutable once accepted? |
|---|---|---|
| `ADR` | Architecture Decision Record — ratified choice + rejected alternatives | Yes — superseded, never edited in place |
| `RP` | Research / interface design | No |
| `TS` | Technical specification (implementation-grade) | No |
| `PLAN` | Roadmap / delivery plan | No |
| `REQ` | Requirements document | No |
| `ARCH` | Architecture / diagrams / synthesis | No |
| `CANON` | Canonical registry (owns enumerations) | No; membership changes bump set version |
| `GUIDE` | How-to, tutorial, or authored product/role prose; `diataxis` disambiguates mode | No |
| `REPORT` | Point-in-time analysis / audit output | Yes — dated snapshot |
| `SESSION` | Archived session record | Yes — historical record |

### 4.2 Content mode (`diataxis`)

| `diataxis` | Purpose | Typical `doc_type` |
|---|---|---|
| `tutorial` | Learning-oriented | GUIDE |
| `how-to` | Task-oriented | GUIDE, TS |
| `reference` | Facts, schemas, registries | CANON, REQ, TS |
| `explanation` | Why / trade-offs | ARCH, RP |
| `decision` | Ratified decision + alternatives | ADR |
| `mixed` | Explicit hybrid; MUST justify in first section | ARCH, REPORT |

**HT-DOC-003:** prefer one dominant mode; `mixed` requires one-line justification.

### 4.3 Audience tiers (`audience`)
`architect` · `developer` · `operator` · `business` · `sales` · `agent` · `all`.

Path defaults (this repo): `docs/architect/**→architect`, `docs/developers/**→developer`, `docs/operators/**→operator`, `README.md→all`. Overrides allowed when the true reader differs.

---

## 5. Identifiers and file naming

### 5.1 Document IDs
- **New documents:** `HATHOR-<TYPE>-<NNN>` where `TYPE ∈ {ADR, RP, TS, PLAN, REQ, ARCH, CANON, GUIDE, REPORT, SESSION}` and `NNN` is zero-padded and monotonic per type.
- **Requirement IDs** (inside docs): `HT-<AREA>-###` (e.g. `HT-DOC-001`). A document `id` MUST NOT collide with a requirement-style prefix.
- `id` is **immutable**. Replacement is by supersession (§7.2), never rename-in-place.

### 5.2 File naming
`hathor-<type>-<nnn>-<slug>-<yyyymmdd>.md`, lowercase, hyphenated. The date is **creation** date; later edits update `updated`/`version` only. Existing files keep names; lookup is by `id` and INDEX.

### 5.3 Section & anchor stability
Headings MUST stay stable citation targets. Renaming a cited section is a change event and SHOULD leave a redirect note. **HT-DOC-004**.

---

## 6. Versioning and change history

### 6.1 Semantic Versioning for documents (`version`)
- **MAJOR** — alters a decision, requirement meaning, or enumerated membership (breaking for consumers). For immutable types (`ADR`, `REPORT`, `SESSION`), MAJOR means a **new superseding document**, not an in-place rewrite.
- **MINOR** — additive clarification, new section, non-breaking row/field.
- **PATCH** — editorial only (typo, formatting, link) with no meaning change.

**HT-DOC-005:** any content change MUST bump `version` and `updated` consistently.

### 6.2 Change history
Living documents SHOULD keep a `## Changelog` (most recent first). Cross-document amendments MUST also appear in `docs/architect/PENDING-EDITS.md`.

### 6.3 Set-versioned registries
`CANON` docs that publish a named set (e.g. `hathor-doc@1`) bump the **set version** on meaning change, independently of document `version`.

---

## 7. Status, supersession, and review marks

### 7.1 Status lifecycle (`status`)

```text
draft ──▶ proposed ──▶ accepted ──▶ superseded
                          │
                          └────────▶ retired
```

| `status` | Meaning | Gate to enter |
|---|---|---|
| `draft` | Under construction | author creates |
| `proposed` | Complete; awaiting operator sign-off | author marks ready; PENDING-EDITS row |
| `accepted` | Ratified | operator sign-off in PENDING-EDITS |
| `superseded` | Replaced | replacement accepted; `superseded_by` set |
| `retired` | Withdrawn without replacement | operator decision |

Status is **ratification**. It is orthogonal to `review.trust` (§7.3) and `stale` (§8).

### 7.2 Supersession
Never silently overwrite a decision. New doc lists old in `supersedes`; old becomes `status: superseded` with `superseded_by`. Section-level supersession uses an inline banner.

### 7.3 Review / reviewed mark (`review.trust`)

| `trust` | Meaning | Who sets it |
|---|---|---|
| `unverified` | Not checked end-to-end | default |
| `machine-checked` | Automated gates passed; no human end-to-end review | CI |
| `human-reviewed` | Named human verified end-to-end on `reviewed_at` | reviewer |

`reviewed_by` + `reviewed_at` are the **verification** timestamp — not the edit timestamp. A typo fix does not reset them; a re-verification does.

**HT-DOC-006:** `trust: human-reviewed` requires non-null `reviewed_by` and `reviewed_at`.

---

## 8. Staleness (the stale flag)

### 8.1 Definition
A document is **stale** when it has drifted past its review window or its cited sources changed since last verification. Stale means *treat with intention* — not automatically wrong.

### 8.2 Computation
`stale` is computed on docs changes and on a schedule when **any** of:

1. **Interval lapse:** `today > reviewed_at + review.interval` (or if `reviewed_at` is null: `today > created + interval`).
2. **Source drift:** any path/glob in `sources` has a commit newer than `reviewed_at`.
3. **Broken reference:** cited `id` missing/`retired`, or dead internal link/anchor.

```text
stale(doc) = interval_lapsed(doc) OR source_drift(doc) OR broken_reference(doc)
```

Immutable types (`ADR`, `REPORT`, `SESSION`) are **interval-exempt**; they still fail on broken references and are replaced by supersession.

### 8.3 Default review intervals

| `doc_type` | Default `interval` |
|---|---|
| `TS`, `PLAN` | `90d` |
| `REQ`, `ARCH`, `GUIDE`, `RP` | `180d` |
| `CANON` | `365d` |
| `ADR`, `REPORT`, `SESSION` | n/a (interval-exempt) |

### 8.4 Behavior on stale
- Interval lapse / source drift: CI **warns** (does not hard-fail solely for freshness).
- Broken reference / missing required fields: CI **hard-fails**.
- Agents consuming `stale: true` MUST surface staleness and prefer fresher, higher-trust sources when available.

**HT-DOC-007:** staleness MUST be visible per-document and in aggregate indexes/reports.

---

## 9. Indexing and discovery

### 9.1 Human index (`INDEX.md`)
Each documentation tree keeps an `INDEX.md`: table by Doc ID with date, status, purpose, and reading order. Every document in the tree MUST appear. **HT-DOC-008**.

### 9.2 Machine index (generated)
- `docs/index.json` — generated array of front-matter records (id, title, summary, doc_type, diataxis, audience, status, version, updated, review, stale, relationships). Never hand-maintained as source of truth.

### 9.3 Agent index (`llms.txt`)
Each tree publishes `llms.txt` (llms.txt v2): H1 title, one-line blockquote, H2 link lists with one-line summaries from each doc's `summary`. Target ≤ ~10k tokens. Optional `llms-full.txt` MAY concatenate high-value docs.

### 9.4 Generation, not duplication
**HT-DOC-009:** `index.json` and `llms.txt` MUST be regenerated from front-matter; hand-edited machine indexes are defects.

---

## 10. Enforcement (docs-as-code)

| Linter | Severity | Fails when |
|---|---|---|
| `ml-doc-frontmatter` | blocking | required field missing/invalid vs `hathor-doc@1` |
| `ml-doc-id-unique` | blocking | duplicate `id` or requirement-prefix collision |
| `ml-doc-links` | blocking | dead internal link/anchor or cited id missing/retired |
| `ml-doc-index` | blocking | document absent from tree INDEX / index.json |
| `ml-doc-staleness` | warn | interval lapse or source drift |
| `ml-doc-diataxis` | warn | `mixed` without justification or obvious mode blur |

**HT-DOC-010:** blocking checks MUST pass before merge; status transitions remain recorded in `PENDING-EDITS.md`.

---

## 11. Adoption & migration

1. **New documents** adopt `hathor-doc@1` immediately (this file is the first example).
2. **Existing documents** are grandfathered until migrated: add front-matter only if missing; preserve body, ids, and ratification status.
3. **Order:** CANON + INDEX first, then accepted ADR/RP, then the rest.
4. **No status inflation:** migration sets `trust: unverified` and conservative intervals; it never promotes to `human-reviewed` or `accepted`.

---

## 12. Worked example — this document
This file carries `hathor-doc@1` with `id: HATHOR-CANON-001`, `doc_type: CANON`, `diataxis: reference`, `version: 0.1.0`, `status: proposed`, `review.trust: unverified`, and `review.interval: 365d`.

---

## 13. Requirements (`HT-DOC-###`)

- **HT-DOC-001 — Dual consumption.** One Markdown file serves human and agent; agent view is generated.
- **HT-DOC-002 — Required front-matter.** New docs carry all §3.3 required fields.
- **HT-DOC-003 — One content mode.** Single `diataxis` mode; `mixed` requires justification.
- **HT-DOC-004 — Stable IDs & anchors.** `id` immutable; cited sections keep stable anchors.
- **HT-DOC-005 — SemVer + change class.** Changes bump `version`/`updated` per §6.1.
- **HT-DOC-006 — Review record.** `human-reviewed` requires `reviewed_by` + `reviewed_at`.
- **HT-DOC-007 — Staleness visibility.** Per-document and aggregate.
- **HT-DOC-008 — Human index completeness.** Every doc in tree `INDEX.md`.
- **HT-DOC-009 — Generated machine index.** `index.json` / `llms.txt` from front-matter.
- **HT-DOC-010 — Docs-as-code gate.** Blocking linters pass before merge; sign-off in PENDING-EDITS.

---

## 14. Adoption decision log

| Standard | Decision | Rationale |
|---|---|---|
| **Diátaxis** | Adopted | Lightweight content modes for humans |
| **llms.txt v2** | Adopted | Token-bounded agent map |
| **Docs-as-code + CI** | Adopted | Keeps docs honest in PR flow |
| **YAML front-matter** | Adopted | Deterministic parse; still readable |
| **Dublin Core / PAV** | Mapping only | Interop without RDF runtime |
| **SemVer + Keep a Changelog** | Adopted | Clear change classes |
| **Trust tiers (unverified / machine-checked / human-reviewed)** | Adopted | Separates ratification from accuracy review |
| **DITA / DocBook** | Rejected | Too heavy for Markdown-first corpus |
| **Hand-maintained machine index** | Rejected | Guaranteed drift |

---

## 15. Open questions (for operator sign-off)

1. Confirm `HATHOR-<TYPE>-<NNN>` as the public ID namespace (vs reusing private `HATHOR-` IDs).
2. Confirm requirement prefix `HT-DOC-###` / `HT-<AREA>-###`.
3. Confirm initial trees: `docs/architect`, `docs/developers`, `docs/operators` (create on demand).
4. Confirm tooling home: Framework `bin/docs/` vs Control Tower (`HATH0R-CLI`) commands.
5. Ratify `hathor-doc@1` as the set version for this schema.

---

## 16. Changelog

- **0.1.1 — 2026-09-15:** live corpus ID namespace normalized to `HATHOR-*` (issue #12); archive retains `AEGIS-*` provenance.
- **0.1.0 — 2026-09-15:** initial proposed OpenSource documentation framework (issue #5).

---

*Proposed standard v0.1.0 — not yet accepted. Definitions of the documentation contract live here; cross-document amendments are tracked in `PENDING-EDITS.md`.*
