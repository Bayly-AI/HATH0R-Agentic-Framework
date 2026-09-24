# Summary Report — AEGIS Framework Documentation Refactor

- **Record type:** summary report (session record; no `AEGIS-` Doc ID per CANON-001 §7.1)
- **Date:** 2026-09-13
- **Prepared by:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Status:** COMPLETE — all plan waves executed; D1–D7 operator-approved; promoted to `staging` via PR #2 (merge `6ecc88d`)
- **Companions:** `2026-09-13-corpus-refactor-session-log.md` (timeline), `../PENDING-EDITS.md` (register), `../INDEX.md` (corpus catalog)

---

## 1. Executive summary

The AEGIS research corpus was reviewed end-to-end, found to be strong in discipline but carrying **coherence debt** (later decisions contradicting earlier canonical documents), and refactored in one approved, seven-wave pass. The refactor recorded three previously implicit decisions as ADRs, consolidated all drifting enumerations into a single registry authority, closed the four largest specification gaps with new research packs, installed change control, and finished with operator sign-off on all seven decisions (D1–D7) and promotion to `staging`. The corpus grew from 26 to 37 documents; every v1 acceptance criterion in CORE-001 §16 now has a defining specification and an owning workstream.

## 2. Problem found (review phase)

40 findings across three classes:
- **E1–E18 — errors/contradictions.** Headliners: ADR-001 rejected the greenfield binary while CORE/TS-001 built one (unrecorded reversal); the ≤ 8 domain cap was violated by CORE's own 9-domain tree, RP-007's `validate` proposal, and TS-001's `aegis run` (arithmetic reached 11); exit code 2 meant both "usage error" (CLI) and "degraded" (bot boundary) in the same documents; gate counts drifted 10 → 14 → "the 11th" (really 15); a POSIX atomicity misconception (PIPE_BUF) in the ledger spec; three conflicting port-registry paths; ambiguous spool residency; a defective 29 MB board export.
- **G1–G14 — gaps.** No Tower surface, no brokering mechanism behind "brokered sessions," no knowledge storage/retrieval mechanics, no threat model (TTY-spoofable "human-only" waivers; agent-writable run logs undermining the no-skip guarantee against adversaries), bespoke signing infrastructure, unscheduled highest-ROI skill pack, no platform-wide roadmap.
- **R1–R8 — structural refactors.** No change control or supersession tracking; per-paper enumerations; document/requirement ID collision (`AEGIS-REQ-BOT-001` vs `AEG-REQ-BOT-001`).

## 3. Delivered

### 3.1 Decisions recorded and accepted (D1–D7)
- **ADR-003** — greenfield `aegis` binary (supersedes ADR-001 in part); canonical nine-domain surface (`validate` top-level, `bots` → `tower`, PLAT-008 ≤ 9); two-boundary exit-code model with clispec `outcomes[]`; Epic gate exit 5 → 2.
- **ADR-004** — `cfg/port-registry.yaml`; project-tier spool with machine indexing; `.ai/aegis` retired; v1 OS scope macOS + Linux.
- **ADR-005** — Backup TS: build minimal contract-native `aegis-backup-ts` over adopting Gitea/Redmine.
- **ADR-002** — coordination model (event-triggered central orchestration) accepted under the same sign-off (D7).

### 3.2 Canonical registries (CANON-001 — now the enumeration authority)
15-gate registry with canonical evaluation order (Provenance → Contract → Sequence/Barrier → domain gates); telemetry event registry (core + `validation.*` + `orchestration.*` + run-log types); 17-code refusal registry; 20-linter catalog; 26-bot roster; naming/ID conventions (`AEGIS-` = document, `AEG-` = requirement).

### 3.3 Gap-closing research packs (accepted as design)
- **RP-010 Tower Surface v1** — five REST facets (TBR, signed distribution, curators, ingest, query) + machine/human identity model. `AEG-TWR-001..008`.
- **RP-011 Operator brokering** — proxy-by-default with a declared, scoped, short-lived token escape hatch; pool schema; idempotency-key store; rate/circuit policy. `AEG-OPB-001..008`.
- **RP-012 Knowledge storage & retrieval** — files-as-truth record v1, FTS5-first hybrid retrieval, explicit `NO_CONFIDENT_MATCH` threshold, MCP contracts. `AEG-KST-001..008`.
- **RP-013 Threat model** — normative trust statement (guarantees hold vs *cooperative-but-fallible* agents), Tower-issued human identity tokens replacing TTY inference, hash-chained run-log hardening path, signed execution inputs, and adopt-don't-invent signing: **RFC 8785 JCS + DSSE/Ed25519 + TUF + SLSA/in-toto** (applied into RP-001/RP-002). `AEG-THR-001..008`.

### 3.4 Planning
- **PLAN-001** — platform roadmap: 8 workstreams (WS1–WS8), milestones M-A..M-F, ~2,370–3,080 base hours; every CORE §16 criterion mapped to an owner.
- **PLAN-003** — gateway epics (AOG-P0..P5), the four unscheduled validators placed, and the ~800-token agent skill pack scheduled with a CI drift check.

### 3.5 Canon alignment & governance
CORE-001 and ARCH-001 amended in place (nine-domain tree, exit-boundary section + clispec envelope mapping, fifteen-gate banner, corrected ≤ 3-wave fan-out model with the new `AEG-HIE-007` batch-dispatch primitive, new ARCH §19/§20 diagrams, NFR-007); supersession banners and `Amended by` headers across the corpus; `PENDING-EDITS.md` change-control register; `INDEX.md` rebuilt with Doc-ID/Status columns; repo hygiene (`.gitignore`, six `.DS_Store` files untracked, duplicate board export removed).

## 4. Metrics

| Metric | Before | After |
|---|---|---|
| Corpus documents (`docs/architect/*.md`) | 26 | 37 (+2 session records) |
| Recorded decisions (ADRs accepted) | 0 accepted (2 proposed) | 5 accepted (ADR-001 superseded in part) |
| Requirement IDs | ~150 (`AEG-*`) | +33 new (`TWR/OPB/KST/THR` ×8, `HIE-007`) |
| Gate enumeration | 3 conflicting counts (10/14/15) | 1 registry (G01–G15, ordered) |
| Open internal register items | — | 0 (1 external: board re-export) |
| Session commits | — | `fc5aa25` (+1,802/−98) · `700f2d7` · `ab3d01c` · merge `6ecc88d` |

## 5. Verification
- Cross-reference audit: all ADR/CANON citations resolve; residual "≤ 8" strings confirmed as budgets or historical quotes.
- External-claims check: CLI Spec versions/dates verified against clispec.dev; benchmark caveats confirmed already sound; two genuine technical corrections applied (PIPE_BUF; ad-hoc canonicalization → JCS).
- PR #2 merged at `CLEAN`/`MERGEABLE`, head `ab3d01c`, zero CI checks configured (admin merge, branch retained).

## 6. Outstanding items
1. **`AEGIS.pdf` per-panel re-export** — external, board owner (PENDING-EDITS §4): current export is raster-illegible with a clipped bottom row.
2. **Fleet-wide invocation evidence** and **benchmark v2** — pre-existing research follow-ups (reports 01/05).
3. **Next execution step (PLAN-001 §6):** cut WS1/WS2 epics in the Ticketing Plane; ratify nothing further — all corpus decisions are closed.

---

*Session record. Normative content lives in the corpus documents referenced above.*
