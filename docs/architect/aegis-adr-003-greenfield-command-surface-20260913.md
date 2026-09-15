---
id: AEGIS-ADR-003
title: AEGIS-ADR-003 — Greenfield Binary, Canonical Command Surface & Exit-Code Boundaries
summary: RFC 2119 keywords apply.
doc_type: ADR
diataxis: decision
audience: [architect, agent]
tags: []
version: 1.0.0
status: accepted
created: '2026-09-13'
updated: '2026-09-15'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: null, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# AEGIS-ADR-003 — Greenfield Binary, Canonical Command Surface & Exit-Code Boundaries

- **Document ID:** AEGIS-ADR-003
- **Status:** ACCEPTED — operator sign-off 2026-09-13 (PENDING-EDITS D1)
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Supersedes:** AEGIS-ADR-001 *in part* — specifically its "Greenfield AEGIS binary — rejected" alternative and its `infraos-os`-rooted target surface. ADR-001 remains authoritative for the domain taxonomy, lifecycle rule, and the InfraOS migration/alias path.
- **Amends:** AEGIS-REQ-CORE-001 §4.1, §4.5, §14, `AEG-REQ-PLAT-008`, §16.1; AEGIS-ARCH-001 §15; AEGIS-TS-001 §10.1
- **Resolves findings:** E1 (unrecorded greenfield reversal), E2 (domain-count arithmetic), E3 (exit code 2 dual meaning), E5 (Epic gate exit code)
- **Scope rule:** decision record only. No implementation authorized by this document.

RFC 2119 keywords apply.

---

## 1. Context

Three contradictions accumulated between ADR-001 (2026-09-11) and the later corpus:

1. **Binary strategy.** ADR-001 rejected a "Greenfield AEGIS binary" ("splits control plane; violates AD-001 spirit") and rooted the target tree at `infraos-os`. AEGIS-REQ-CORE-001 §0.2 subsequently declared AEGIS "a greenfield core platform," and AEGIS-TS-001 `TS-D-005` selected a greenfield `aegis` CLI as the first build and dogfood target. The reversal was real and deliberate but never recorded as a decision.
2. **Domain count.** `AEG-REQ-PLAT-008` mandates ≤ 8 top-level domains. CORE §4.1's own tree lists nine (`process, proctor, operator, tower, knowledge, work, repo, delivery, bots`). RP-007 §14 recommends a top-level `validate` (ten) and leaves the cap unresolved. TS-001 §10.1 introduces a top-level `aegis run --record` (eleven) that appears in no tree. RP-009 `AEG-GW-015` asserts ≤ 8 still holds.
3. **Exit code 2.** The CLI table (ADR-001 / CORE §4.5) defines `2 = usage/validation error` and forbids reusing an error code for named non-error states. Yet "run flagged degraded (exit 2)" appears normatively in RP-002 §3.3, RP-006 §5.3, and CORE `AEG-REQ-TKT-009`/`AEG-REQ-SEC-001` — the Infra CR-017 *bot-boundary* scheme (0/1/2, where 2 = degraded) leaking into *CLI-boundary* text.

## 2. Decisions

### 2.1 D1 — Greenfield `aegis` binary (supersedes ADR-001 alternative log)

AEGIS ships as a **greenfield `aegis` binary** (TS-001 TS-D-001/005). TS-001 examples use the working module path `github.com/baylyai/aegis`, but repository/module ownership is an M0 interface freeze rather than a decision ratified by this ADR. ADR-001's façade-over-`infraos-os` approach is re-scoped as the **InfraOS migration path**: legacy products may run the façade + compatibility aliases during transition, but the platform of record is `aegis`.

- ADR-001's taxonomy (domain trees, lifecycle rule `process runbook run`, global flags, migration phases) **stands** and is inherited by `aegis`.
- ADR-001's "Alternatives considered → Greenfield AEGIS binary → rejected" row is **superseded by this ADR**.
- The AD-001 "single entrypoint" spirit is preserved *within each fleet*: an InfraOS product keeps one entrypoint (`infraos-os`, façaded) until migrated; a migrated/greenfield project has exactly one entrypoint (`aegis`).

### 2.2 D2 — Canonical top-level domain list (nine domains)

The canonical root surface is:

```text
aegis
├── help | version | schema | doctor | planes        # always-on meta
├── process …        # Process-Bot — hierarchy execution + orchestration runs
├── proctor …        # Proctor-Bot — gates, policy, gateway admission
├── operator …       # Operator-Bot — external systems (brokered)
├── tower …          # Control Tower authority surface (+ `tower bots …`)
├── knowledge …      # Knowledge Plane
├── work …           # Ticketing Plane
├── repo …           # Universal Project Layout + repo ops
├── delivery …       # PR / quality / release façade
└── validate …       # Continuous Validation System (RP-007/TS-001)
```

Normative changes:

1. **`validate` is promoted to a top-level domain.** It is the highest-frequency agent surface (RP-007 §14 rationale accepted); folding it under `proctor` would bury the hot path.
2. **`bots` folds under `tower`** as `aegis tower bots list|show|selftest|install|init`. Registry introspection is a Registry-Plane/Tower concern (`AEG-REG-006`); `aegis bots …` remains a hidden compatibility alias behind `--include-legacy`. `init` (bot scaffold) is additive per RP-014 — domain count unchanged.
3. **`AEG-REQ-PLAT-008` is revised from ≤ 8 to ≤ 9** top-level domains + always-on meta. Nine is the ratified count; any tenth domain requires an ADR.
4. **`aegis run --record` (TS-001 §10.1) is renamed `aegis validate record -- <cmd>`.** Evidence capture is a validation-fabric primitive; a bare top-level `run` verb collides with `process run …` vocabulary and would breach the cap.

### 2.3 D3 — Exit-code boundaries (two tables, one mapping)

There are exactly **two exit-code boundaries**, and they never mix:

1. **CLI boundary (`aegis` process exit):** the canonical CORE §4.5 table (0–7) is authoritative. Named non-error data states (`degraded`, `blocking`, `changes_pending`, `buffered`) are **envelope fields**, never reused error codes. Where a distinct process exit is operationally required for a data state, it MUST be declared as a CLI Spec v0.3 `outcomes[]` entry with a code that overlaps no error code — never by reusing `2`.
2. **Bot boundary (bot executable exit, CR-017):** `0 = healthy, 1 = failure, 2 = degraded/warning` remains the per-bot contract (`AEG-BOT-CMD-002`). Bot-boundary codes are consumed by the chassis/CLI and **never surface uncontexted at the `aegis` boundary**: the CLI translates a bot-boundary `2` into `{degraded: true, …}` in the response envelope with CLI exit `0` (or the applicable error code if the command itself failed).

**Reading rule for the existing corpus:** every occurrence of "run flagged degraded (exit 2)" in RP-002 §3.3, RP-006 §5.3/§5.4, CORE `AEG-REQ-TKT-009`, `AEG-REQ-SEC-001`, and `AEG-BOT-ANA-007` is to be read as "run flagged `degraded: true` in the response envelope; per-bot `status`-class commands may exit 2 *at the bot boundary only*." Documents are amended to this phrasing as they are next touched (tracked in `PENDING-EDITS.md`).

**Gate exit correction:** the Epic-Linkage Gate exit changes from `5` (conflict/already exists) to `2` (usage/validation — precondition unmet). An epic-less ticket is a validation failure, not a conflict. CORE §14 and ARCH-001 §15 are amended accordingly; the canonical gate table lives in AEGIS-CANON-001.

## 3. Consequences

### 3.1 Positive
- The greenfield strategy is now a recorded, citable decision instead of an implicit drift.
- Domain arithmetic closes: nine domains, cap ≤ 9, no undeclared top-level commands.
- `degraded` semantics become unambiguous and CLI Spec-conformant (`outcomes[]` is the sanctioned mechanism for non-error exits).

### 3.2 Negative / costs
- ADR-001 readers must consult this ADR for the binary strategy (mitigated by the supersession banner added to ADR-001).
- TS-001 §10.1 command rename is a breaking doc change (no code exists yet; zero runtime cost).
- Documents citing "≤ 8 domains" (`AEG-GW-015`, RP-009 §9, CORE §16.1) require mechanical updates to "≤ 9".

### 3.3 Edits queued by this ADR
CORE-001 §4.1 tree, PLAT-008, §4.5 boundary section, §14 epic exit, §16.1; ARCH-001 §15; RP-009 `AEG-GW-015` wording; TS-001 §10.1 rename; RP-002/RP-006 degraded phrasing. Tracked in `PENDING-EDITS.md`.

## 4. Alternatives considered

| Alternative | Why rejected |
|---|---|
| Keep ≤ 8 by folding `validate` under `proctor` | Buries the highest-traffic agent surface; RP-007 §14 evidence stands |
| Keep ≤ 8 by folding `work` under `operator` | Conflates a source-of-truth plane with its broker; violates the three-planes framing (PLAT-003) |
| Reuse exit 2 for degraded at CLI boundary | Directly contradicts ADR-001/CORE §4.5; breaks agent branching on exit codes |
| Rename bot-boundary codes instead (2 → other) | CR-017 is adopted and proven (CORE §12); translation at the chassis is cheaper than re-litigating the bot contract |

## 5. Compliance

| Ratified decision | This ADR |
|---|---|
| `AEG-REQ-PLAT-001` single control plane | ✓ one binary per fleet; façade is a migration state, not a second plane |
| ADR-001 taxonomy + lifecycle | ✓ inherited unchanged |
| CLI Spec v0.3 outcomes/errors separation | ✓ D3 adopts `outcomes[]` for data-state exits |
| Canonical Rule 4 (reuse when better) | ✓ CR-017 retained at bot boundary; translated, not replaced |

---

*Decision record — ACCEPTED 2026-09-13. No implementation authorized by this document.*
