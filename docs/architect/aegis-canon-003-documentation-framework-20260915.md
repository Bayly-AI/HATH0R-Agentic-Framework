---
id: AEGIS-CANON-003
title: "HATHOR Documentation Framework"
summary: "Metadata schema, IDs, versioning, review, staleness, indexing, and enforcement for HATHOR docs."
doc_type: CANON
diataxis: reference
audience: [architect, agent]
tags: [documentation, metadata, governance]
version: 0.2.1
status: accepted
created: 2026-09-15
updated: 2026-09-15
owner: "Raymond Bayly (BaylyAI)"
review:
  reviewed_by: "Raymond Bayly (BaylyAI)"
  reviewed_at: 2026-09-15
  trust: human-reviewed
  interval: 365d
  next_review: 2027-09-15
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: [AEGIS-CANON-001, AEGIS-CANON-002, AEGIS-RP-004, AEGIS-RP-012]
---
# AEGIS-CANON-003 — HATHOR Documentation Framework
## Metadata Schema · Document Types · IDs · Versioning · Review & Sign-off · Staleness · Indexing · Enforcement

> This document carries a machine-readable `hathor-doc@1` front-matter block (above) as the canonical header and the human-readable bulleted header (below) as the rendered view — the dual form defined in §3.1. It is the first conformant example of the standard it specifies.

- **Document ID:** AEGIS-CANON-003
- **Status:** ACCEPTED — operator ratification 2026-09-15 (PENDING-EDITS D12)
- **Version:** 0.2.1
- **Date:** 2026-09-15
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Derived from / Consolidates:** README knowledge properties (discoverability, digital provenance, TTL/staleness, draft/verified status, machine-readable manifest); AEGIS-CANON-001 §7 (naming & ID conventions) and §8 (requirement-prefix index); INDEX.md (corpus index + reading order); PENDING-EDITS.md (change-control register); AEGIS-RP-004 (knowledge promotion: draft→verified, TTL) and AEGIS-RP-012 (knowledge storage/retrieval, record v1); AEGIS-CANON-002 HP-11 (provenance over recency) and HP-12 (attributable & reconstructable)
- **Companion to:** AEGIS-CANON-001 (registries — this document is the registry authority for documentation types, statuses, and metadata), AEGIS-CANON-002 (platform principles)
- **External standards adopted:** Diátaxis (content architecture), llms.txt v2 (agent-facing index), docs-as-code (CI-validated docs in VCS), Dublin Core / DCMI + PAV (metadata vocabulary), Semantic Versioning 2.0.0 (document versioning), Keep a Changelog (change history), RFC 2119 (normative keywords), Michael Nygard ADRs (decision records). Adoption rationale and rejected alternatives are logged in §14.
- **Maintenance rule:** any paper that adds a document type, status value, review tier, or metadata field MUST amend this document in the same change. Semantics may live in a source paper; **membership and the canonical metadata schema live here**. Drift between a paper and this registry is a defect in the paper (mirrors CANON-001).
- **Scope rule:** standard/interface definition only. No implementation is authorized by this document; tooling (linters, indexer, CI) is scheduled through the owning plan and an authorizing ticket.

RFC 2119 keywords apply: **MUST / SHOULD / MAY**. Requirements in this paper use the prefix `AEG-DOC-###` (registered in CANON-001 §8; see §13 and PENDING-EDITS D12). Acceptance criteria are inline.

---

## 0. Purpose

### 0.1 Why this document
The AEGIS/HATHOR corpus already practices strong conventions — stable Document IDs, a status front-matter block, an INDEX with a Doc-ID column, and a `PENDING-EDITS` change-control register (CANON-001 §7.5; INDEX.md). What it does **not** yet have is a single, machine-checkable contract that:

1. is **parseable by agents** and **readable by humans** from the *same* artifact;
2. gives every document a **version**, a stable **ID**, an **index** entry, and an explicit **review / reviewed** mark; and
3. carries a **staleness flag** so a document that has drifted past its review window is treated with intention rather than trusted blindly.

This paper specifies that contract. It is the documentation-layer analogue of what RP-014 did for the bot unit: it names the artifact, fixes its metadata, and walks its lifecycle from **draft → reviewed → accepted → superseded/retired**.

### 0.2 One-line definition
> A HATHOR document is a **UTF-8 Markdown file with a machine-readable metadata header** that carries a stable **id**, a semantic **version**, a **status**, an explicit **review record**, and a computable **staleness** signal — authored once to serve both a **human reader** and an **agent**, discoverable through a generated **index**, and governed by the same docs-as-code discipline as source code.

### 0.3 Relationship to the runtime Knowledge Plane (important)
This framework governs **authored corpus documents** under `docs/**` and the repo-root `README.md`. Agent-instruction files named `AGENTS.md` are governed by their own directory-scoped precedence chain and are explicitly excluded from `hathor-doc@1`; migration inventories MUST list them by exception without adding documentation front-matter. The framework is deliberately **consistent with**, but distinct from, the runtime **Knowledge Plane** (RP-004 promotion; RP-012 record v1):

- Both use a **draft → verified** trust model and a **TTL/staleness** signal; this document reuses that vocabulary so a corpus document can be **promoted into** the Knowledge Plane without a metadata rewrite.
- The Knowledge Plane owns *runtime retrieval* of knowledge records; this framework owns *authored documentation at rest*. Where the two disagree on a field name or trust tier, that is a defect to reconcile in `PENDING-EDITS`, not a silent fork.

### 0.4 Design goals (dual audience)
- **Agent-efficient:** small, curated entry points; token-bounded index; one concept per file; stable anchors; cite-by-ID; machine-readable header parseable with regex/YAML — no bespoke parser (llms.txt v2; OKF).
- **Human-friendly:** Diátaxis-clear content types; a rendered header a person can read at a glance; predictable file names and locations.
- **Trustworthy:** provenance, explicit review, and honest staleness over recency (CANON-002 HP-11).
- **Cheap to keep current:** docs live beside the corpus in VCS, reviewed in PRs, validated in CI (docs-as-code).

---

## 1. Dual-consumption model — one artifact, two readers

Every document is authored once and consumed two ways:

| Reader | Needs | How this framework serves it |
|---|---|---|
| **Human** | Orientation, rationale, the right content type for the moment | Rendered header; Diátaxis content mode (§4); INDEX tables; reading order (INDEX.md) |
| **Agent** | Token-cheap discovery, precise IDs, freshness/trust signals | YAML front-matter (§3); generated machine index + `llms.txt` (§9); cite-by-ID; staleness/trust fields |

**Principle (AEG-DOC-001).** A single Markdown file, with a machine-readable header and a disciplined body, MUST satisfy both readers. We do not maintain a separate human copy and agent copy of the same document; the agent view is *generated* from the same source (§9), never hand-forked.

---

## 2. Scope of documents covered

This framework applies to all authored documentation in the repository:

- **Architecture corpus** — `docs/architect/**` (ADR, RP, TS, PLAN, REQ, ARCH, CANON, reports, sessions).
- **Business docs** — `docs/business/**`.
- **Developer docs** — `docs/developers/**`.
- **Sales docs** — `docs/sales/**`.
- **Repo-root authored docs** — `README.md`.

It does **not** govern: `AGENTS.md` instruction files, runtime Knowledge-Plane records (RP-012), telemetry, or source-code comments. Generated API reference (if any) is in scope only for its front-matter and index entry, not its body (which is generated).

---

## 3. Metadata schema (the canonical header)

### 3.1 Form: YAML front-matter is canonical; the rendered header is a view
New documents MUST carry a **YAML front-matter block** delimited by `---` as the first bytes of the file (Jekyll/GitHub-docs convention; parseable by standard tools). The existing human-readable **bulleted header** (as used throughout the corpus today) is retained as a *rendered view* and MAY be generated from the front-matter. Existing documents are **grandfathered** (§11): they keep their bulleted header until migrated, and the indexer tolerates both forms during migration.

Rationale: a bulleted Markdown header is human-readable but not reliably machine-parseable; CI staleness, indexing, and `llms.txt` generation need a deterministic block. YAML front-matter is that block and is still perfectly readable by a human.

### 3.2 Canonical front-matter (schema `hathor-doc@1`)

```yaml
---
# ---- Identity (required) ----
id: AEGIS-CANON-003                 # stable Document ID (§5); immutable for the life of the doc
title: "HATHOR Documentation Framework"
summary: "Metadata schema, IDs, versioning, review, staleness, indexing, and enforcement for HATHOR docs."
                                     # one sentence; feeds INDEX + llms.txt + blockquote

# ---- Classification (required) ----
doc_type: CANON                     # corpus type registry (§4.1): ADR|RP|TS|PLAN|REQ|ARCH|CANON|GUIDE|REPORT|SESSION
diataxis: reference                 # content mode (§4.2): tutorial|how-to|reference|explanation|decision|mixed
audience: [architect, agent]        # §4.3: architect|developer|business|sales|operator|agent|all
tags: [documentation, metadata, governance]

# ---- Versioning & status (required) ----
version: 0.2.1                      # SemVer for document content (§6)
status: accepted                    # lifecycle (§7.1): draft|proposed|accepted|superseded|retired
created: 2026-09-15
updated: 2026-09-15                 # last edit of any kind (content date; may be Git-derived)

# ---- Ownership & review (required) ----
owner: "Raymond Bayly (BaylyAI)"   # single responsibility path (person or role)
review:
  reviewed_by: "Raymond Bayly (BaylyAI)" # actor who last verified end-to-end
  reviewed_at: 2026-09-15           # date of last end-to-end verification (NOT the edit date)
  trust: human-reviewed             # trust tier (§7.3): unverified|machine-checked|human-reviewed
  interval: 365d                    # review TTL; drives staleness (§8). Supports 30d|12w|6m|1y. 365d is the CANON default (§8.3)
  next_review: 2027-09-15           # computed: reviewed_at + interval

# ---- Freshness (managed; may be CI-set) ----
stale: false                        # computed by CI (§8); MAY be set true manually to force review

# ---- Relationships (optional) ----
supersedes: []                      # list of doc IDs this replaces
superseded_by: null                 # doc ID that replaces this, once superseded
amended_by: []                      # doc IDs that amend sections here (mirror in PENDING-EDITS)
parent: null                        # parent doc ID (e.g., RP-014 parent = REQ-BOT-001)
sources: [AEGIS-CANON-001, AEGIS-CANON-002, AEGIS-RP-004, AEGIS-RP-012]  # source doc IDs, requirement IDs, or code globs (§8.3)
---
```

### 3.3 Field requirements
- **Required on every document:** `id`, `title`, `summary`, `doc_type`, `diataxis`, `audience`, `version`, `status`, `created`, `updated`, `owner`, `review` (with `trust` and `interval` at minimum). `AEG-DOC-002`.
- **Conditionally required:** `superseded_by` MUST be set when `status: superseded`; `supersedes` MUST list the superseded ID(s) on the replacing doc.
- **Optional:** `tags`, `amended_by`, `parent`, `sources`, plus any producer-defined keys. Consumers MUST tolerate and preserve unknown keys (OKF rule; forward-compatible).

**AC (AEG-DOC-002):** a document missing any required field fails `ml-doc-frontmatter` (§10) and is rejected at PR time.

### 3.4 Dublin Core / PAV mapping (interoperability, non-binding)
For external interoperability, the header maps cleanly onto Dublin Core / PAV so records can be exported without loss: `id→dc:identifier`, `title→dc:title`, `summary→dc:description`, `doc_type→dc:type`, `created→dc:created`, `updated→pav:lastUpdateOn`, `owner→dc:creator`, `reviewed_by→pav:curatedBy`, `superseded_by→dc:isReplacedBy`, `supersedes→dc:replaces`, `sources→dc:source`, `version→pav:version`. Implementations MAY emit a DCMI record from front-matter; the mapping is documentation, not a runtime dependency.

---

## 4. Document types and content architecture

### 4.1 Corpus document-type registry (`doc_type`)
These are the AEGIS corpus types; membership lives here (extends CANON-001 §7.1). A new type requires an amendment to this section.

| `doc_type` | Meaning | Immutable once accepted? |
|---|---|---|
| `ADR` | Architecture Decision Record (Nygard) — a ratified choice + rejected alternatives | Yes — superseded, never edited in place |
| `RP` | Research paper / interface design | No (living until superseded) |
| `TS` | Technical specification (implementation-grade) | No |
| `PLAN` | Roadmap / delivery plan | No |
| `REQ` | Requirements document | No |
| `ARCH` | Architecture / diagrams / synthesis | No |
| `CANON` | Canonical registry (owns enumerations) | No, but changes bump set version |
| `GUIDE` | Human/agent how-to, tutorial, or authored non-corpus prose (business, sales, developer, and role docs); `diataxis` disambiguates its content mode | No |
| `REPORT` | Point-in-time analysis / audit output | Yes — a dated snapshot |
| `SESSION` | Archived session record | Yes — a historical record |

### 4.2 Content mode (`diataxis`) — Diátaxis, with two corpus additions
Every document declares its primary content mode. Mixing modes in one file is the most common documentation defect (Diátaxis); a document SHOULD be predominantly one mode.

| `diataxis` | Purpose | Typical `doc_type` |
|---|---|---|
| `tutorial` | Learning-oriented (teach a first success) | GUIDE |
| `how-to` | Task-oriented (achieve a goal) | GUIDE, TS |
| `reference` | Information-oriented (facts, schemas, registries) | CANON, REQ, TS |
| `explanation` | Understanding-oriented (why, trade-offs) | ARCH, RP |
| `decision` | *(corpus addition)* a ratified decision + alternatives | ADR |
| `mixed` | Explicitly hybrid (e.g., a synthesis); MUST justify | ARCH, REPORT |

**AC (AEG-DOC-003):** `diataxis: mixed` requires a one-line justification in the body's first section; every other value expects a single dominant mode.

### 4.3 Audience tiers (`audience`)
Mirrors the existing `docs/` subtrees and the reader roles in the corpus. A document MAY serve several.

`architect` · `developer` · `business` · `sales` · `operator` · `agent` · `all`. Path defaults: `docs/architect/**→architect`, `docs/business/**→business`, `docs/developers/**→developer`, `docs/sales/**→sales`, repo-root `README.md→all`. Overrides allowed when the path does not match the true reader. `AGENTS.md` files are instruction artifacts outside this enumeration and schema (§0.3).

---

## 5. Identifiers and file naming

### 5.1 Document IDs (extends CANON-001 §7.1)
- **New documents** use `AEGIS-<TYPE>-<NNN>`, `TYPE ∈ {ADR, RP, TS, PLAN, REQ, ARCH, CANON, GUIDE, REPORT, SESSION}` (adds `GUIDE`, `REPORT`, and the registered `SESSION` type to the CANON-001 set), `NNN` zero-padded and monotonic per type.
- The near-collision rule stands: a new document MUST NOT mint an ID whose body matches an existing **requirement** prefix (`AEG-…`). Requirements in a document use `AEG-<AREA>-###`; documentation-framework requirements use `AEG-DOC-###` (§13).
- `id` is **immutable**. A document is never renamed to a new ID; it is **superseded** (§7.2).

### 5.2 File naming (extends CANON-001 §7.2)
`aegis-<type>-<nnn>-<slug>-<yyyymmdd>.md`, lowercase, hyphenated. The `<yyyymmdd>` records the file's creation/authored date and does **not** change on later edits (edits are tracked by `updated`/`version`, not the filename). Existing files keep their names; the INDEX and front-matter `id` are the lookup keys.

### 5.3 Section & anchor stability (agent addressability)
Headings MUST use stable, human-meaningful text so that `path/file:§N` and Markdown anchors remain valid citation targets (agents cite `AEG-…` IDs and section anchors). Renaming a section that is cited elsewhere is a change event (§6) and SHOULD leave a redirect note. `AEG-DOC-004`.

---

## 6. Versioning and change history

### 6.1 Semantic Versioning for documents (`version`)
Document content is versioned with SemVer 2.0.0:

- **MAJOR** — a change that alters a decision, requirement meaning, or enumerated membership (i.e., could break a consumer relying on the prior text). For `ADR`/`REPORT`/`SESSION` (immutable), a MAJOR change is not an edit — it is a **new document that supersedes** (§7.2).
- **MINOR** — additive clarification, new section, new non-breaking field/row.
- **PATCH** — editorial fix (typo, formatting, link) with no change in meaning.

`AEG-DOC-005`: any change to a document MUST bump `version` and `updated` consistently with the classes above.

### 6.2 Change history (Keep a Changelog)
Living documents (`RP`, `TS`, `PLAN`, `REQ`, `ARCH`, `CANON`, `GUIDE`) SHOULD carry a `## Changelog` section (or a footer note, as the corpus does today) recording notable changes per version, most-recent first. Cross-document amendments MUST **also** be recorded in `PENDING-EDITS.md` (the corpus's existing register) — the changelog is local narrative; `PENDING-EDITS` is the cross-document source of truth.

### 6.3 Set-versioned registries
`CANON` documents that publish a versioned set (e.g., `hathor-principles@1`) bump the **set version** on any meaning change, independently of the document `version`, exactly as CANON-002 §4 already prescribes.

---

## 7. Status, supersession, and review marks

### 7.1 Status lifecycle (`status`)
The corpus already uses these values; this fixes them as an enumeration.

```
draft ──▶ proposed ──▶ accepted ──▶ superseded
                          │
                          └────────▶ retired
```

| `status` | Meaning | Gate to enter |
|---|---|---|
| `draft` | Under construction; not review material | author creates |
| `proposed` | Complete; awaiting operator sign-off | author marks ready; row added to PENDING-EDITS |
| `accepted` | Ratified by operator sign-off | operator sign-off recorded in PENDING-EDITS |
| `superseded` | Replaced by another document | `superseded_by` set; replacement accepted |
| `retired` | Withdrawn without replacement | operator decision; kept for history, flagged non-authoritative |

Status is about **ratification**. It is **orthogonal** to the review/trust mark (§7.3) and to staleness (§8): an `accepted` document can still go `stale`, and a `draft` can be `human-reviewed` for accuracy.

### 7.2 Supersession (never rename, never silently overwrite)
Replacing a document's decision means authoring a new document that **supersedes** it: the new doc lists the old in `supersedes`; the old doc is set `status: superseded` with `superseded_by` pointing forward. Superseded *sections* carry an inline banner at the section head (CANON-001 §7.5). This preserves the audit trail (HP-12) and keeps every citation resolvable.

### 7.3 Review / reviewed mark and trust tiers (`review.trust`)
Distinct from ratification, every document carries an accuracy-review mark modeled on the corpus draft/verified model (RP-004) and OKF trust tiers:

| `trust` | Meaning | Who sets it |
|---|---|---|
| `unverified` | Not yet checked end-to-end | default on creation |
| `machine-checked` | Passed automated checks (front-matter, links, examples, drift) but no human end-to-end review | CI |
| `human-reviewed` | A named human read it end-to-end and confirmed it matches reality on `reviewed_at` | reviewer |

`reviewed_by` + `reviewed_at` record the last **end-to-end human verification** — explicitly *not* the edit date (a typo fix does not reset it; a re-verification does). This is the two-timestamp pattern (edit vs verify) that prevents silent drift.

**AC (AEG-DOC-006):** promotion to `trust: human-reviewed` requires non-null `reviewed_by` and `reviewed_at`; CI sets `machine-checked` only after all automated gates pass.

---

## 8. Staleness (the stale flag)

### 8.1 Definition
A document is **stale** when it has drifted past its declared review window or its cited sources have changed since it was last verified. Stale means *treat with intention* — not automatically wrong, but no longer trusted as current (this is exactly the README "TTL/staleness" intent, made mechanical).

### 8.2 Computation (CI-managed `stale`)
`stale` is computed on every docs change and on a schedule. A document is flagged stale when **any** of:

1. **Interval lapse:** `today > reviewed_at + review.interval` (or `reviewed_at` is null and `today > created + interval`).
2. **Source drift:** any glob in `sources` (§8.3) has a commit newer than `reviewed_at` (Git-derived; `git log --follow`).
3. **Broken reference:** a cited doc `id` is missing or `retired`, or an internal link/anchor is dead.

```
stale(doc) = interval_lapsed(doc) OR source_drift(doc) OR broken_reference(doc)
```

Immutable types (`ADR`, `REPORT`, `SESSION`) are **exempt from interval lapse** (a decision does not rot with time); they can still be flagged by broken reference and are handled by supersession, not staleness.

### 8.3 Default review intervals by type
Defaults; a document MAY set a shorter `review.interval`. Fast-moving documents get shorter windows (industry defaults cluster at ~90–180 days).

| `doc_type` | Default `interval` | Note |
|---|---|---|
| `TS`, `PLAN` | `90d` | Tracks implementation; drifts fastest |
| `REQ`, `ARCH`, `GUIDE` | `180d` | Living, moderate churn |
| `CANON` | `365d` | Stable registries; membership changes are event-driven, not time-driven |
| `RP` | `180d` | Living until superseded |
| `ADR`, `REPORT`, `SESSION` | n/a | Interval-exempt (immutable snapshots) |

### 8.4 Behavior on stale
- CI **warns** on stale and opens/updates a tracked review item; it does **not** hard-fail the build for interval lapse alone (staleness is a signal, not a blocker) — mirroring "enforcement fails closed; observation fails open" (HP-09) applied to docs.
- Broken-reference and missing-required-field failures **do** hard-fail (they are correctness defects, not freshness).
- An agent consuming a `stale: true` document MUST surface the staleness in its reasoning and prefer a fresher, higher-trust source when one exists (HP-11).

`AEG-DOC-007`: the corpus MUST expose staleness both per-document (`stale`) and in aggregate (index + `aegis`-style report), so drift is visible rather than silent.

---

## 9. Indexing and discovery

### 9.1 Human index (INDEX.md) — retained
Each documentation tree keeps its human `INDEX.md` (as `docs/architect/INDEX.md` already does): a table keyed by Doc ID with date, status, and purpose, plus reading order. `INDEX.md` remains the human entry point and MUST list every document in its tree (`AEG-DOC-008`).

### 9.2 Machine index (generated)
A machine-readable index MUST be **generated** from front-matter (never hand-maintained as the source of truth), so humans and agents never diverge:

- `docs/index.json` — array of every document's front-matter (id, title, summary, doc_type, diataxis, audience, status, version, updated, review, stale, relationships). This is the agent's O(1) map of the corpus.

### 9.3 Agent index (llms.txt)
Each tree MUST publish an `llms.txt` (llms.txt v2) — a curated, token-bounded Markdown map: an H1 title, a one-line blockquote summary, and H2 link-lists to the highest-value documents with one-line descriptions drawn from each doc's `summary`. Keep it small (target ≤ ~10k tokens); it is a *map*, not a dump. An optional `llms-full.txt` MAY concatenate high-value documents for large-context ingestion.

Example (`docs/architect/llms.txt`):

```
# AEGIS / HATHOR Architecture Corpus

> Governance and control-plane design for the HATHOR agentic application framework. Start with the canon, then accepted ADRs and RPs.

## Canon
- [AEGIS-CANON-001 Registries](./aegis-canon-001-registries-20260913.md): gates, events, refusal codes, linters, bot roster, IDs.
- [AEGIS-CANON-003 Documentation Framework](./aegis-canon-003-documentation-framework-20260915.md): how every doc is structured, versioned, reviewed, and indexed.

## Decisions
- [AEGIS-ADR-003 Greenfield command surface](./aegis-adr-003-greenfield-command-surface-20260913.md): nine-domain CLI.
```

### 9.4 Generation, not duplication
`index.json` and `llms.txt` are build artifacts regenerated from source front-matter. `AEG-DOC-009`: the machine index and `llms.txt` MUST be generated; a hand-edited machine index is a defect.

---

## 10. Enforcement (docs-as-code)

Documentation is validated like source code — in the same repo, in PR review, in CI. The following checks are registered in the CANON-001 §5 linter catalog by D12:

| Linter | Class | Fails the build when |
|---|---|---|
| `ml-doc-frontmatter` | `doc.frontmatter_schema` | required front-matter field missing/invalid against `hathor-doc@1` |
| `ml-doc-id-unique` | `doc.id_collision` | duplicate `id`, or `id` collides with a requirement prefix (§5.1) |
| `ml-doc-links` | `doc.broken_reference` | dead internal link/anchor, or cited `id` missing/`retired` |
| `ml-doc-index` | `doc.index_drift` | a document is absent from its tree's `INDEX.md`/`index.json` |
| `ml-doc-staleness` | `doc.staleness` | *(warn-only)* interval lapse or source drift (§8) |
| `ml-doc-diataxis` | `doc.mode_mixed` | *(warn-only)* `mixed` without justification, or obvious mode-blur |

Enforcement policy follows §8.4: correctness defects (schema, id, links, index) **block merge**; freshness/mode signals **warn**. Prose style MAY be linted (e.g., Vale) as a non-blocking check.

`AEG-DOC-010`: a documentation change MUST pass the blocking checks above before merge; the review/sign-off record for `status` transitions continues to live in `PENDING-EDITS.md`.

---

## 11. Adoption & migration

1. **New documents** adopt `hathor-doc@1` front-matter immediately (this document is the first example).
2. **Existing documents** are grandfathered: the indexer reads their current bulleted header; a migration pass (idempotent, path-defaulted, Git-derived dates) adds the YAML front-matter **only if missing**, preserving existing values — no body edits. Migration does not change any `id`, filename, or status.
3. **Order:** CANON and INDEX first (highest reference value), then accepted ADRs/RPs, then the rest — one document at a time (Diátaxis "work one step at a time"; no big-bang rewrite).
4. **No status inflation:** migration sets `trust: unverified` and a conservative `interval`; it never promotes a document to `human-reviewed` or `accepted`. Those transitions remain operator/reviewer actions.

---

## 12. Worked example — this document's own header
This file demonstrates conformance: the `hathor-doc@1` front-matter block at the top carries `id`, `title`, `summary`, `version: 0.2.1`, `status: accepted`, `created`/`updated`, `owner`, a `review` block (`trust: human-reviewed`, `reviewed_at: 2026-09-15`, `interval: 365d`), `doc_type: CANON`, `diataxis: reference`, and `audience: [architect, agent]`, with the bulleted header as its rendered view (§3.1).

---

## 13. Requirements (AEG-DOC-###)

- **AEG-DOC-001 — Dual consumption.** One Markdown file MUST serve human and agent readers; the agent view is generated, not hand-forked. **AC:** no document has a separate agent-only twin.
- **AEG-DOC-002 — Required front-matter.** Every new document MUST carry `hathor-doc@1` required fields (§3.3). **AC:** `ml-doc-frontmatter` passes.
- **AEG-DOC-003 — One content mode.** Each document declares a single `diataxis` mode; `mixed` requires justification. **AC:** §4.2 satisfied.
- **AEG-DOC-004 — Stable IDs & anchors.** `id` is immutable; cited sections keep stable anchors. **AC:** no ID reuse; renamed cited sections leave a redirect note.
- **AEG-DOC-005 — SemVer + change class.** Every change bumps `version`/`updated` per §6.1. **AC:** CI diff shows a version bump on any content change.
- **AEG-DOC-006 — Review record.** `trust: human-reviewed` requires `reviewed_by`+`reviewed_at`. **AC:** §7.3 enforced.
- **AEG-DOC-007 — Staleness visibility.** Staleness MUST be computable per-document and in aggregate. **AC:** `stale` present; index reports it.
- **AEG-DOC-008 — Human index completeness.** Every document appears in its tree's `INDEX.md`. **AC:** `ml-doc-index` passes.
- **AEG-DOC-009 — Generated machine index.** `index.json` and `llms.txt` are generated from front-matter. **AC:** regeneration is byte-reproducible from sources.
- **AEG-DOC-010 — Docs-as-code gate.** Blocking checks pass before merge; sign-off recorded in `PENDING-EDITS`. **AC:** §10 policy enforced in CI.

Registered CANON-001 §8 row (D12): `AEG-DOC-###` → *HATHOR documentation framework* → **AEGIS-CANON-003**.

---

## 14. Adoption decision log (per HP-16)

| Standard | Decision | Rationale |
|---|---|---|
| **Diátaxis** | **Adopted** for `diataxis` content modes | Proven, lightweight, tool-agnostic; separates human content needs cleanly |
| **llms.txt v2** | **Adopted** for the agent index | De-facto standard for agent-facing doc maps; token-bounded; Markdown (human+machine) |
| **Docs-as-code + CI** | **Adopted** for enforcement | Only pattern shown to keep docs fresh; matches corpus PR/CI practice |
| **YAML front-matter** | **Adopted** as canonical header | Deterministic parse for staleness/index/llms.txt; still human-readable |
| **Dublin Core / PAV** | **Adopted as a mapping** (non-binding) | Interoperable export vocabulary without imposing RDF at runtime |
| **SemVer 2.0.0 + Keep a Changelog** | **Adopted** for `version` + changelog | Familiar, unambiguous change semantics |
| **OKF trust tiers** | **Adopted** for `review.trust` | Aligns with corpus draft/verified (RP-004) and agent-maintained-corpus needs |
| **DITA / DocBook** | **Rejected** | Heavyweight XML authoring; contradicts Markdown-first, low-friction corpus |
| **`.well-known/` URIs for the agent index** | **Rejected** in favor of per-tree `llms.txt` | Per-path scope matches `docs/**` subtrees; no origin-root control needed |
| **Hand-maintained machine index** | **Rejected** | Guaranteed to drift from source; must be generated (§9.4) |

---

## 15. Ratification record (D12)

Operator sign-off on 2026-09-15 made this document `accepted` after confirming:

1. The `hathor-doc@1` metadata schema (§3) is accepted as the canonical header for new documents, with existing docs grandfathered (§11).
2. The document-type (§4.1), content-mode (§4.2), status (§7.1), and trust-tier (§7.3) enumerations are accepted, and the CANON-001 §7.1 type set is extended with `GUIDE`/`REPORT`.
3. The staleness model (§8) — interval + source-drift + broken-reference, with immutable types interval-exempt — is accepted.
4. The indexing model (§9): retain `INDEX.md`, generate `index.json` and `llms.txt`.
5. The `AEG-DOC-###` prefix (§13) and the `ml-doc-*` linters (§10) are registered in CANON-001 §§8 and 5 (tracked in PENDING-EDITS §6.1).
6. `INDEX.md` lists this document.
7. `docs/sales/**` uses the `sales` audience, `GUIDE` is the catch-all for authored business/sales/developer prose, and `AGENTS.md` instruction files remain outside `hathor-doc@1`.

---

## 16. Changelog

- **0.2.1 — 2026-09-15:** corrected the new-document ID type set to include the already-registered `SESSION` document type.
- **0.2.0 — 2026-09-15:** ratified as D12; added `docs/sales/**` and the `sales` audience; clarified `GUIDE` as the authored non-corpus prose type; excluded directory-scoped `AGENTS.md` instruction files from `hathor-doc@1`.
- **0.1.0 — 2026-09-15:** initial proposed documentation framework.

---

*Accepted standard v0.2.1 — ratified 2026-09-15 under D12 and corrected by the Phase 0.5 `SESSION` ID-set erratum. Consistent with CANON-001 (IDs/registries), CANON-002 (HP-11/HP-12), and the runtime Knowledge Plane's draft/verified + TTL model (RP-004/RP-012). Definitions of the documentation contract live here; cross-document amendments are tracked in `PENDING-EDITS.md`.*
