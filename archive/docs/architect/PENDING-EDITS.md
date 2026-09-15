# AEGIS Corpus — Pending-Edits & Change-Control Register

Purpose: the single place where cross-document amendments are tracked, per the corpus refactor plan (2026-09-13). A paper that changes another paper's decision MUST add a row here in the same change. Rows are removed only when the target document is amended **and** the amendment is operator-reviewed.

Status legend: **applied** = edit made, pending operator review with its owning decision · **awaiting sign-off** = edit blocked on a PROPOSED decision · **external** = action outside this repo/agent.

## 1. Decisions — APPROVED by operator

D1–D8 received operator sign-off on 2026-09-13; their document statuses were flipped accordingly and the §3 blocked edits applied. D12 and D13 received operator approval on 2026-09-15; CANON-003 and PLAN-004 are accepted/approved, and Phase 0.5 is the next PLAN-004 gate.

| Item | Document | What sign-off ratified |
|---|---|---|
| D1 | AEGIS-ADR-003 | Greenfield `aegis`; nine-domain surface (`validate` top-level, `bots`→`tower`); PLAT-008 ≤ 9; exit-code boundaries + `outcomes[]`; Epic gate exit 5→2; `aegis validate record` rename |
| D2 | AEGIS-ADR-004 | `cfg/port-registry.yaml`; project-tier spool + machine index; `.ai/aegis` cleanup; v1 OS scope (macOS+Linux) |
| D3 | AEGIS-ADR-005 | Greenfield `aegis-backup-ts` (vs Gitea/Redmine) |
| D4 | AEGIS-CANON-001 | Registry precedence rule; 15-gate registry + canonical order; event/refusal/linter/roster registries; naming & ID conventions |
| D5 | AEGIS-RP-010..013 | Tower surface; brokering model (proxy-default); knowledge store mechanics; threat model + trust statement + TUF/DSSE/JCS adoption |
| D6 | AEGIS-PLAN-001/003 | Platform roadmap; gateway/validator/skill-pack scheduling |
| D7 | AEGIS-ADR-002 | Coordination model (event-triggered central orchestration) — covered by the same corpus sign-off; status flipped 2026-09-13 |
| D8 | AEGIS-RP-014 | Bot-unit governance (directive/rules/principles), memory model, lifecycle; §13 Q1–Q6 operator resolutions; manifest 1.1.0 + `BOT_RULE_REFUSED` + `AEG-BOT-GOV/MEM/LIF` + TS3; TS-003 drafted |
| D12 | AEGIS-CANON-003 | HATHOR Documentation Framework `hathor-doc@1` v0.2.1: canonical YAML front-matter; document-type/status/trust registries; SemVer; review marks; staleness; generated `index.json`/`llms.txt`; `docs/sales/**` coverage; `AGENTS.md` instruction-file exception; `GUIDE`/`REPORT`/`SESSION`, `AEG-DOC-###`, and six `ml-doc-*` checks registered in CANON-001. v0.2.1 is the Phase 0.5 erratum adding `SESSION` to the ID type set already implied by the ratified type registry |
| D13 | AEGIS-PLAN-004 | Documentation-refactor execution plan approved 2026-09-15: migrate authored corpus docs in place to `hathor-doc@1`; create seven role guides; generate docs-as-code indexes and validation; share draft project-tier records to `.aegis/knowledge/`; preserve verbatim originals under `archive/`. D12 was ratified separately; Phase 0.5 review remains before migration fan-out |

## 2. Edits applied 2026-09-13 (approved with D1–D6)

| Target | Edit | Owner |
|---|---|---|
| ADR-001 header, repo §, alternatives | superseded-in-part banner; `.ai/aegis` annotation; greenfield row struck | ADR-003/004 |
| CORE-001 (§0.4, §4.1, §4.5, PLAT-008, §7.1, §9, §10.1, §12, §13, §14, §15, §16, §17) | nine-domain tree; boundary mapping + clispec envelope map; gate banner + Epic exit; vocab pointer; Adopt(design); CNT-003/004; NFR-007; Q2/Q3/Q6/Q7 updates; TKT-007 decision note | ADR-003/004, CANON, RP-010/013 |
| ARCH-001 (header, §1, §6, §15, §16, new §19/§20) | wave-model fan-out fix; fifteen-gate banner + order note; env naming; validation-fabric + AOG diagrams | ADR-002/003/004, RP-007/009 |
| RP-002/RP-003/RP-006/RP-007/RP-008 headers | Amended-by lines; RP-007 §6.1 supersession banner; RP-007 §4.1 +2 linters; RP-003 §3.1 spool wording; RP-006 contract fixes (assignee null, provider.kind, legacy paths, AMD/DVO note) | ADR-002/003/004, RP-009 |
| TS-001 §8.2/§10.1/§17.2; TS-002 (via TS-001 ref); PLAN-002 P2-E1 | PIPE_BUF rationale corrected; `aegis validate record` rename | ADR-003, E11 |
| BOT-001 §10 | `papers/` → same-folder links | E15 |
| UUIDv7 examples (CORE, RP-003, RP-007, RP-009) | `0192…` → `01a0…` (2026-plausible timestamps) | E17 |
| Containerization article + presentation; whitepaper; CLI research report | port-registry path notes; target-design tense + ADR-005 ref; historical-baseline banner | ADR-004/005, R8 |
| RP-001 §2/§2.9/§2.10/AEG-MAN-007; BOT-001 CMD-011/013/018; CANON-001 §4/§8; ADR-003 §2.2; RP-007 §4.1; TS-001 §2.3/§13 | manifest 1.1.0 `governance` triad + runtime fields; `status` governance group; `manifest --with-governance`; `report.decisions[]`; `BOT_RULE_REFUSED`; `AEG-BOT-GOV/MEM/LIF` + TS3 prefixes; `tower bots init`; `ml-manifest-schema` 1.1.0 scope; per-bot config path | RP-014 (D8) |

## 3. Formerly blocked edits — resolution after the 2026-09-13 sign-off

| Target | Edit | Resolution |
|---|---|---|
| RP-001 §2 | canonicalization → RFC 8785 (JCS); signature → DSSE envelope | **Applied 2026-09-13** |
| RP-001 Q1, RP-002 Q3/§3.4 | key rotation/bootstrap → TUF role layout (Tower serves TUF repo) | **Applied 2026-09-13** |
| TS-001 §8.6 (+ TS-002 Q6) | waiver identity: TTY heuristic → Tower-issued human token (dev-profile exception per PLAN-003 §5) | **Applied 2026-09-13** |
| RP-005 §4 / Process-Bot contract | formalize the batch-dispatch primitive assumed by the ≤3-wave model (ARCH §6) | **Applied 2026-09-13** — RP-005 §4 + `AEG-HIE-007` define `hierarchy.resolve.chain@1`; WS1 implements |
| RP-009 §12 item 4 ("the 11th gate") | reword to reference CANON-001 G03 / 15-gate registry | **Applied 2026-09-13** |
| CORE §14 / RP-009 §7 / TS-002 §9 | embed RP-013 §2 trust-model statement where no-skip/human-only guarantees are claimed (AEG-THR-001) | **Applied 2026-09-13** |
| Older docs, bot-name casing sweep | normalize to CANON-001 §7.3 | **Closed without sweep** — §7.3 makes the manifest-lowercase form authoritative and explicitly permits capitalized prose; no text changes required |

## 4. External actions

| Item | Action | Owner |
|---|---|---|
| `AEGIS.pdf` re-export | The current export is a single-page raster: panel text is illegible at any zoom and the bottom row (Bot-Orchestration / Bot-Anatomy / Bot-Principles) is **clipped by the export itself** — unrecoverable from this file. Re-export from the source board as **per-panel PNGs ≥ 2000 px wide** into `images/` (pattern of `images/00–03`), or as a vector-text PDF, including the full bottom row. Then update the INDEX row. | Board owner (Raymond) |
| Fleet-wide invocation evidence | Report 01 is one developer machine; fleet validation remains open (CLI report §8) | Operator |
| Benchmark v2 | KnowMCP healthy + multi-run CLI/MCP comparison (report 05 §8) | Operator/eng |

## 5. AEGIS-RP-014 — ratified & applied (D8, 2026-09-13)

RP-014 is **ACCEPTED**. Its §11 deltas are applied in the target documents and recorded in §2 above; this section is retained as the trace of the original proposal. The §13 Q1–Q6 operator resolutions: predicate language = JSON Schema default + `cel` opt-in; post-rule compensation = detect-and-flag, **human-executed only** (never auto-compensate); directive budget = **1000 tokens**; principle audit = continuous + threshold-triggered (governance-class stricter); transition profile = **instant** (no free-governance grace); agent-backed executor = **allowed by exception** (`runtime.executor_kind`). All eight deltas below are `applied (D8)`.

## 6. Decisions — PROPOSED 2026-09-14, awaiting operator sign-off

D9 and D10 are **synthesis / restatement only**; their sign-off confirms fidelity to source papers rather than a design change. D11 is a normative proposal whose sign-off requires the prerequisites and cross-document changes listed below. D12 moved to §1 after ratification on 2026-09-15.

| Item | Document | What sign-off would ratify | Status |
|---|---|---|---|
| D9 | AEGIS-ARCH-002 | Bot unit compendium as the stakeholder-facing summary of record: executive summary; 26-bot roster with definitions (per CANON-001 §6); family profiles; anatomy diagrams + technical/business explanation (per BOT-001 §3, RP-014 §2–§6); memory/performance/state-management comparison tables (per RP-014 §7, RP-008 §4) | awaiting sign-off |
| D10 | AEGIS-CANON-002 | `hathor-principles@1` (HP-01..HP-16) as the platform-altitude principle set; §0.2 relationship rule (bot bundles keep citing `aegis-principles@1` P-ids only); §2 P↔HP mapping; §3 usage; §4 change control | awaiting sign-off |
| D11 | AEGIS-TS-004 | DMZ implementation spec. Requires, before acceptance: (a) the DMZ Integration Boundary report (2026-09-14 session output) filed and accepted as design basis (proposed AEGIS-RP-015); (b) operator decisions on the project-rules layer (`.aegis/rules/rules.yaml`, RP-014 §3.4 amendment) and policy floors (TS-001 §6.1 amendment); (c) CANON-001 amendments in §6.1 below; (d) a nested-`.aegis/`-roots ADR before TS-004 P4 | awaiting sign-off |

### 6.1 Cross-document edits proposed by D9/D10/D11 and applied by D12

| Target | Edit | Owner | Status |
|---|---|---|---|
| CANON-001 §8 | add row `HP-##` → HATHOR platform principles (review criteria, non-enforcing) → AEGIS-CANON-002 | CANON-002 §5 | awaiting sign-off |
| INDEX.md | rows for ARCH-002 and CANON-002 | — | **applied 2026-09-14** (listing only; statuses show awaiting sign-off) |
| CANON-001 §4 | refusal codes `POLICY_CONFLICT` (exit 2; `details.sides[]`) and `PROJECT_RULE_REFUSED` (exit 2; `rule_id`, `rule_scope`) | TS-004 §19 | awaiting sign-off (D11) |
| CANON-001 §5 · RP-007 §4.1 | linter `ml-agents-directive-conflict` (class `upl.agents_directive_conflict`); catalog 20 → 21 | TS-004 §7, §19 | awaiting sign-off (D11) |
| CANON-001 §8 | row `TS4-D/C/I-###` → AEGIS-TS-004 | TS-004 §19 | awaiting sign-off (D11) |
| RP-007 §2.2 · TS-001 §4 | finding class `governance.conflict` | TS-004 §8.2 | awaiting sign-off (D11) |
| TS-001 §6.1, §13 · TS-002 §4.3, §12 · TS-003 §5.3 | suite override above floor; `profile.active` (`report-only\|dev\|enforced`); graph node-kind floor; rule context gains `capability`/`project` | TS-004 §19 | awaiting sign-off (D11) |
| RP-010 §3.2 | policy pack gains `min_profile` and `floors` | TS-004 §13.2 | awaiting sign-off (D11) |
| RP-014 §3.4 item 2 · CORE §7.1 | name `.aegis/rules/rules.yaml` as the project-rules artifact; show in UPL tree | TS-004 §5 | awaiting sign-off (D11; amends D8) |
| INDEX.md | row for TS-004 | — | **applied 2026-09-14** (listing only; status shows awaiting sign-off) |
| CANON-001 §7.1 | extend document-type set with `GUIDE` and `REPORT` (new-doc `AEGIS-<TYPE>-<NNN>` naming) | CANON-003 §4.1, §5.1 | **applied 2026-09-15 (D12)** |
| CANON-001 §8 | add row `AEG-DOC-###` → HATHOR documentation framework → AEGIS-CANON-003 | CANON-003 §13 | **applied 2026-09-15 (D12)** |
| CANON-001 §5 | register `ml-doc-frontmatter`, `ml-doc-id-unique`, `ml-doc-links`, `ml-doc-index`, `ml-doc-staleness`, `ml-doc-diataxis` (doc-as-code checks; §10) | CANON-003 §10 | **applied 2026-09-15 (D12)** |
| INDEX.md | row for CANON-003 | — | **applied 2026-09-15; accepted by D12** |
| CANON-003 §§0.3, 2, 4.1, 4.3, 12, 15–16 | version 0.2.0: include `docs/sales/**` and `sales` audience; define `GUIDE` as the non-corpus prose catch-all; exclude `AGENTS.md` instruction files from `hathor-doc@1` while inventorying them by exception | PLAN-004 Phase 0 | **applied and operator-reviewed 2026-09-15 (D12)** |
| CANON-001 §7.1 · CANON-003 §5.1/§16 | v0.2.1 erratum: add the already-registered `SESSION` type to the `AEGIS-<TYPE>-<NNN>` ID set so session migration can mint valid IDs | PLAN-004 Phase 0.5 | **applied 2026-09-15 as corrective D12 alignment; included in Phase 0.5 review** |
| INDEX.md | row for PLAN-004 | — | **applied 2026-09-15 (D13); Phase 0.5 next** |

No gate, event, refusal code, linter, bot, family, requirement, or CLI verb is introduced by D9/D10. **D11 proposes two refusal codes, one linter, one finding class, and additive `aegis repo policy …` verbs under the existing `repo` domain (no new domain, gate, event, bot, or family).** **D12 accepted the documentation standard and registered the `AEG-DOC-###` requirement prefix, six additive `ml-doc-*` documentation linters, and two new document types (`GUIDE`/`REPORT`) — no new gate, event, refusal code, bot, family, or CLI domain; existing documents remain grandfathered.**

## 7. Documentation audit amendments — applied, pending operator review

The 2026-09-14 corpus audit corrected drift against decisions already recorded in D1–D8. These edits do **not** ratify D9/D10, any Draft/Proposed source paper, or any new implementation.

| Target | Correction | Existing authority |
|---|---|---|
| INDEX | define the HATHOR → AEGIS relationship, authority boundaries, reading order, and implementation-authority rule | CORE §0.1; ADR-002/003; RP-010/013 |
| CORE/BOT/ARCH-001/ARCH-002/CANON-002 | distinguish the CLI control surface, three domain authorities, Tower internal APIs, and Operator provider brokering | CORE `PLAT-001/003`; RP-010 §2; RP-011 |
| CORE/BOT/ARCH-002/CANON-002 | separate bot exit `2=degraded` from CLI error exit `2`; split optional dependency degradation from `CAPABILITY_UNKNOWN` exit 3 | ADR-003 §2.3; CANON-001 §4 |
| CORE/ADR-002/RP-009/TS-002 | replace stale “11th gate” language with Sequence/Barrier Gate G03 in the 15-gate registry | CANON-001 §2 |
| RP-001/RP-010/RP-014/TS-003/ARCH-002/CANON-002 | make the DSSE envelope external to the canonical manifest payload; distinguish manifest/governance coverage from unresolved executable-artifact binding (R10) | RP-013 §6; manifest 1.1.0 fields |
| RP-008 | reconcile residual 25/10-bot text and validator scheduling to the canonical 26-bot roster | CANON-001 §6; PLAN-003 §2 |
| RP-009/TS-002/ARCH-002/CANON-002 | scope no-skip/tamper claims to the accepted cooperative-but-fallible v1 trust model | RP-013 §2/§4.1 |
| RP-012/CANON-001 | register `knowledge.retrieval` and clarify Public-tier fallback | RP-012 §3/§4; CANON-001 maintenance rule |
| PLAN-001/PLAN-003 | align approved headers, next actions, and footers without implying code authorization | D6 |

## 8. Recommendations requiring an operator decision or interface freeze

| Item | Gap | Recommended next decision |
|---|---|---|
| R1 | HATHOR/AEGIS relationship and canonical UPL differ from the repository README | Align the README to INDEX/CORE/ADR-004 after operator confirms the framework boundary; remove unsupported sibling-repo secret scanning |
| R2 | Signed-pack admission is accepted by `AEG-THR-004`, but TS-001/PLAN-002 originally scheduled repo-controlled subprocess execution first | Keep pack verification in M0/P0: enforced profiles refuse unsigned content before process creation; dev requires explicit, audited `--allow-unsigned` |
| R3 | Human tokens lack a frozen claims/audience/action/run/replay contract | Add a Tower identity-token profile and negative-test matrix before enforced waiver/deploy work |
| R4 | `gateway.event` may select authority-bearing branches without an emitter/evidence policy | Bind each event class to authenticated emitters, evidence, run, nonce/idempotency, and replay refusal |
| R5 | RP-009 calls a looping graph a DAG and leaves attempt/loop semantics incomplete | Decide cyclic state-machine vs DAG expansion; define loop bounds, attempt events, required-set semantics, and crash-resume tests |
| R6 | “Telemetry never blocks” conflicts with finalize depending on telemetry evidence | Make the local run/audit ledger authoritative and fail closed for its commit; keep export/rollup fail open via outbox/replay |
| R7 | RP-014's no-private-store acceptance criterion is stronger than TS-003 self-declared effects | Preserve static/integration checks and define mediated or observed-effect reconciliation for out-of-process executors |
| R8 | RP-004 promotion, Operator crash-window/idempotency, principle-report ingestion, and retrieval calibration remain insufficiently frozen for implementation | Gate the relevant WS5/WS6/TS-003 tickets on explicit interface specs and concurrent/fault-injection acceptance tests |
| R9 | TS-001/002/003 examples use `github.com/baylyai/aegis`, but no accepted decision fixes repository/module ownership | Freeze the public module path at M0 and update all specs/plans atomically before any package API is published |
| R10 | Manifest 1.1.0 signs the canonical manifest and digest-referenced governance files but contains no executor/image/artifact digest, despite the accepted “signed bundle” intent | Before registration implementation, bind executable bytes or an OCI/SLSA attestation to the manifest with a frozen schema and negative substitution tests |

---

*Register maintained by hand until the corpus adopts generated registries (CANON-001 §7 note / plan R7). Last updated: 2026-09-15 — CANON-003 v0.2.1 ratified/aligned as D12 with its CANON-001 registry amendments and `SESSION` ID-set erratum; PLAN-004 approved as D13 and registered. D9 (ARCH-002), D10 (CANON-002), and D11 (TS-004, DMZ) remain proposed and await explicit operator sign-off.*
