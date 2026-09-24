---
id: HATHOR-RP-012
title: 'HATHOR-RP-012 — Knowledge Plane: Storage & Retrieval Mechanics'
summary: RFC 2119 keywords apply. Requirements use prefix `AEG-KST-###`.
doc_type: RP
diataxis: explanation
audience: [architect, agent]
tags: []
version: 1.0.0
status: accepted
created: '2026-09-13'
updated: '2026-09-15'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: 180d, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# HATHOR-RP-012 — Knowledge Plane: Storage & Retrieval Mechanics

- **Document ID:** HATHOR-RP-012
- **Status:** ACCEPTED (design) — operator sign-off 2026-09-13 (PENDING-EDITS D5); open questions tracked in §7
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Completes:** the Knowledge Plane pair — RP-004 specified *promotion*; this paper specifies *storage and retrieval* (record schema, tier backing stores, scoring, MCP contracts) behind `AEG-REQ-KNO-001..006`
- **Related:** RP-004 (lifecycle/status), CORE §8, BOT-KNO-001..006, ADR-004 (state residency), RP-013 (redaction strength)
- **Scope rule:** research and interface design only. No implementation authorized.

RFC 2119 keywords apply. Requirements use prefix `AEG-KST-###`.

---

## 1. Problem statement

KNO requirements mandate tiered search, microburst writes, mandatory metadata, and retrieval honesty — but no document defines the record shape, where each tier physically lives, how hybrid retrieval scores, or what "no confident match" means mechanically. Without those, `NO_CONFIDENT_MATCH` (KNO-005) is a slogan, not a threshold.

## 2. Knowledge record v1

Files are the truth; indexes are derived (the registry doctrine of RP-002 applied to knowledge).

```yaml
# .hath0r/knowledgebase/<topic_key>/<record_id>.md — YAML frontmatter + markdown body
record_id: kno-01a0f3…            # uuidv7
topic_key: deploy/dvo-ticket      # at most one verified record per (scope, topic_key) — AEG-KPW-005
tier: project                     # project|machine|organization  (public is reference-only, status=external)
status: draft                     # RP-004 lifecycle: draft|verified|stale|disputed|archived|external
title: "DVO deploy ticket checklist expectations"
breadcrumb: "delivery > deploy > dvo-ticket"
provenance: { author: "…", session: "…", source_run: "…", created_at: "…" }
review: { reviewer: null, verified_at: null }     # human identity when promoted (AEG-KPW-003)
ttl: P90D
hierarchy_link: "runbook:dvo-deploy-ticket"
supersedes: null
tags: [dvo, deploy]
```

- **Chunking:** heading-based; every chunk is embedded/indexed as `title + " > " + breadcrumb + "\n" + chunk` (KNO-004's retrieval-quality rule made mechanical).
- **Microburst = one record file (or one bounded patch to one record) per write**; `ml-microburst-size` bounds size; `ml-knowledge-meta` refuses missing frontmatter fields at write time.

## 3. Tier backing stores

| Tier | Truth | Derived index | Reached via |
|---|---|---|---|
| **Project** | `.hath0r/knowledgebase/**` (files in git) | `.hath0r/state/cache/knowledge.db` (SQLite: FTS5 + vector table) | CLI direct + project MCP (read surface) |
| **Machine** | `${XDG_DATA_HOME:-~/.local/share}/hath0r/knowledge/**` | machine `knowledge.db` (same schema) | CLI direct |
| **Organization** | org KB behind **org MCP** (KnowMCP-class, Class A) | server-side | CLI → MCP contract (§5) |
| **Public** | external references only | none | last resort; `status=external`, never promotable |

Design rules: the SQLite index is disposable and rebuilt from files (`hath0r knowledge index refresh`); embeddings are optional per machine — **FTS5 keyword search MUST work with zero model dependencies**, vectors improve ranking when a local embedding service is configured (Class B container locally, per the containerization taxonomy).

## 4. Retrieval algorithm (hybrid, honest)

```text
search(q, scope=auto):
  for tier in [project, machine, organization]:          # KNO-001 order
    kw  := bm25(FTS5, q, tier)                           # always available
    vec := cosine(embeddings, q, tier)  if vectors ready # optional
    score := blend(kw, vec)             # reciprocal-rank fusion; kw-only when no vectors
    apply status filter: verified in-TTL by default; stale flagged per record;
      drafts only with --include-drafts; disputed/archived excluded   # AEG-KPW-008
    if top_score ≥ τ_tier: return results (tier short-circuit, unless --broad)
  return NO_CONFIDENT_MATCH { best_below_threshold_refs }  # explicit, never a weak batch
```

- **τ (confidence threshold)** is configuration, not folklore: `.hath0r/rules/knowledge.yaml` `thresholds: {project: τ₁, machine: τ₂, organization: τ₃}` with bundled defaults; calibrated per org from retrieval-feedback telemetry (`knowledge.retrieval` events — registry addition, CANON-001 §3).
- Responses expose per-record `status`, `ttl` state, and the blended score — retrieval honesty is *visible*, not asserted.

## 5. MCP contracts (project + organization)

Minimal tool surface, both MCPs (Class A):
- `kb.search {query, scope, limit, include_drafts} → {results[], no_confident_match, threshold}`
- `kb.get {record_id} → record`
- `kb.push {record} → {record_id, status: draft}` — always lands as draft; promotion only via the CLI review flow (RP-004); org `kb.push` requires authenticated caller identity for provenance.
Records on the wire use the §2 schema verbatim — no MCP-specific shape.

## 6. Requirements (AEG-KST)

### AEG-KST-001 — Files as truth, index as cache
Project/machine tiers store records as files; indexes are derived and rebuildable.
**AC:** Deleting `knowledge.db` loses zero records; `index refresh` restores search.

### AEG-KST-002 — Record schema v1 mandatory
Every record carries the §2 frontmatter; writes missing fields are refused at write time (`ml-knowledge-meta`).
**AC:** Negative-path write test refuses per missing field.

### AEG-KST-003 — Keyword search without models
FTS5 retrieval MUST function with no embedding dependency; vectors only improve ranking.
**AC:** Fresh machine with no model serves correct keyword results.

### AEG-KST-004 — Explicit confidence threshold
`NO_CONFIDENT_MATCH` is returned iff the blended top score < τ_tier; τ is configured, surfaced in responses, and never silently bypassed.
**AC:** Threshold visible in every search response; below-τ queries return the explicit miss with best-below-threshold refs.

### AEG-KST-005 — Status-honest responses
Default retrieval serves only in-TTL `verified`; drafts need opt-in; stale is flagged per record; disputed/archived excluded (`AEG-KPW-008` restated at the store).
**AC:** Response schema carries status verbatim; opt-ins are recorded on the query event.

### AEG-KST-006 — Tier short-circuit with explicit breadth
A confident project-tier hit ends the search unless `--broad`; traversal order is logged.
**AC:** Retrieval logs show tier order and short-circuit point (`BOT-KNO-001` AC made testable).

### AEG-KST-007 — Chunk quality rule
Every indexed chunk is prefixed `title > breadcrumb`; chunking is heading-based.
**AC:** Index inspection shows zero naked chunks.

### AEG-KST-008 — Draft-only ingress everywhere
Every write path (CLI, project MCP, org MCP) lands `status=draft`; no path can mint `verified` (`AEG-KPW-003` restated at the store).
**AC:** Zero verified records without reviewer identity + timestamp.

## 7. Open questions

1. Embedding model/runtime default (local Class B service vs none) and dimension pinning across tiers.
2. τ calibration procedure and the feedback-event schema powering it.
3. Org MCP authn (ties to RP-010 §5 human/machine identity).
4. Cross-tier duplicate handling on `--broad` (same topic_key at two tiers).

---

*ACCEPTED (design) 2026-09-13. No implementation authorized by this document; open interface details remain tracked in §7.*
