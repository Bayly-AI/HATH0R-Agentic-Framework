# AEGIS Research Corpus

Canonical folder for AEGIS / CLI / HATHOR research artifacts.

**Change control:** cross-document amendments and sign-off state are tracked in [`PENDING-EDITS.md`](./PENDING-EDITS.md). Document/requirement ID conventions and all canonical registries (gates, events, refusal codes, linters, bot roster): [`AEGIS-CANON-001`](./aegis-canon-001-registries-20260913.md).
## Framework goal and boundaries

**HATHOR is the agentic application framework; AEGIS is its governance and control-plane realization.** HATHOR defines the durable operating model for agents: portable project structure, discoverable knowledge, explicit governance, secure capability access, and attributable work. AEGIS makes that model concrete through the `aegis` CLI, bot runtime, validation and orchestration fabrics, three authority planes, and Control Tower services (CORE-001 §0.1; ADR-002/003; RP-010).

The boundaries are distinct:

| Concept | Responsibility |
|---|---|
| **HATHOR framework** | Cross-project principles and contracts for agent navigation, knowledge, governance, credentials, and accountability |
| **AEGIS CLI** | Sole public entry point for human/agent commands and bot dispatch; not itself a source-of-truth plane |
| **Registry / Knowledge / Ticketing planes** | Separate domain authorities for which bots may run, what knowledge is trusted, and what work exists |
| **Control Tower** | Authenticated, asynchronous platform authority for registry, policy, identity, revocation, ingest, and audit query; not a bot and not the terminus of every request |
| **Proctor / Process / Operator** | Admission and routing / conducted run state / third-party connection brokering |

The intended outcome is not autonomous action without constraint. It is **bounded, evidence-backed automation** in which work is attributable to an authorizing ticket and hierarchy chain, completion is evaluated by the platform, provider credentials are brokered, and offline operation degrades honestly. Per RP-013, v1 prevention guarantees are scoped to cooperative-but-fallible agents; adversarial local processes are detected and require later hardening.

## How to read this corpus

1. **AEGIS-CANON-001** owns enumerated membership and identifiers.
2. **Accepted ADRs and accepted research/interface decisions** define ratified choices.
3. **CORE, BOT, RP, ARCH, and TS documents marked Draft/Proposed** remain review material except for amendments explicitly ratified in `PENDING-EDITS.md`.
4. **Approved plans schedule work; they do not ratify a draft design and do not authorize implementation.** Implementation still requires the owning design decision and an authorizing ticket.
5. **Synthesis documents do not promote their sources.** A proposed summary may restate accepted and draft material, but each source keeps its own status.

## Outline source images & board export
The AEGIS outline (as submitted) lives in [`images/`](./images/):

| File | Outline concept |
|------|-----------------|
| [`images/00-outline-agent-anatomy-taxonomy.png`](./images/00-outline-agent-anatomy-taxonomy.png) | Agent Anatomy/Taxonomy + CLI as control plane |
| [`images/01-outline-universal-project-layout.png`](./images/01-outline-universal-project-layout.png) | Universal Project Layout + Knowledge Infrastructure |
| [`images/02-outline-universal-project-layout-detailed.png`](./images/02-outline-universal-project-layout-detailed.png) | Universal Project Layout (detailed tiers + search order) |
| [`images/03-outline-micro-bot-architecture.png`](./images/03-outline-micro-bot-architecture.png) | Micro-Bot Architecture |
| [`AEGIS.pdf`](./AEGIS.pdf) | Full 12-panel board export. **Known-defective:** single-page raster, panel text illegible, bottom row (Bot-Orchestration/Bot-Anatomy/Bot-Principles) clipped by the export. Re-export pending — see `PENDING-EDITS.md` §4. |

## Documents
| Doc ID | Date | Document | Status | Purpose |
|--------|------|----------|--------|---------|
| — | 2026-09-11 | [AEGIS-CLI-Research-Report-2026-09-11.md](./AEGIS-CLI-Research-Report-2026-09-11.md) | Baseline (annotated 09-13) | AEGIS vision vs `infraos-os` vs industry; historical baseline for ADR-003 |
| — | 2026-09-11 | [01-Invocation-Inventory-Top30-2026-09-11.md](./01-Invocation-Inventory-Top30-2026-09-11.md) | Baseline | Top 30 real invocations; hierarchy + bot-role classification |
| — | 2026-09-11 | [02-CLI-Spec-Scoring-2026-09-11.md](./02-CLI-Spec-Scoring-2026-09-11.md) | Baseline | CLI Spec v0.2/v0.3 scoring of the top 30 |
| — | 2026-09-11 | [04-Spike-Schema-Runbook-Checklist-2026-09-11.md](./04-Spike-Schema-Runbook-Checklist-2026-09-11.md) | Spike design | Bounded schema dump + runbook→checklist lifecycle spike |
| — | 2026-09-11 | [05-Token-Benchmark-CLI-vs-MCP-2026-09-11.md](./05-Token-Benchmark-CLI-vs-MCP-2026-09-11.md) | Baseline | Payload baseline (CLI / HTTP / MCP-catalog proxies); not head-to-head |
| AEGIS-ADR-001 | 2026-09-11 | [aegis-adr-001-target-command-tree-20260911.md](./aegis-adr-001-target-command-tree-20260911.md) | Proposed · superseded in part by ADR-003 | Target command tree; retained as taxonomy source + InfraOS migration path |
| AEGIS-REQ-BOT-001 | 2026-09-11 | [aegis-bot-taxonomy-requirements-20260911.md](./aegis-bot-taxonomy-requirements-20260911.md) | Draft | Bot taxonomy, seven-block anatomy, default command contract |
| AEGIS-RP-001 | 2026-09-11 | [aegis-rp-001-manifest-schema-v1-20260911.md](./aegis-rp-001-manifest-schema-v1-20260911.md) | Draft · amended (JCS/DSSE per RP-013) | Manifest schema v1 + HELLO/OFFER/BIND/VERIFY handshake |
| AEGIS-RP-002 | 2026-09-11 | [aegis-rp-002-registry-discovery-20260911.md](./aegis-rp-002-registry-discovery-20260911.md) | Draft · amended (TUF per RP-013) | Hybrid registry: MBI router + TBR authority |
| AEGIS-RP-003 | 2026-09-11 | [aegis-rp-003-telemetry-transport-20260911.md](./aegis-rp-003-telemetry-transport-20260911.md) | Draft · amended (ADR-004) | Spool-and-drain transport; envelope v1; vocabulary → CANON-001 §3 |
| AEGIS-RP-004 | 2026-09-11 | [aegis-rp-004-knowledge-promotion-20260911.md](./aegis-rp-004-knowledge-promotion-20260911.md) | Draft | Draft→verified promotion; status-on-record; tiered reviewers |
| AEGIS-RP-005 | 2026-09-11 | [aegis-rp-005-hierarchy-consolidation-20260911.md](./aegis-rp-005-hierarchy-consolidation-20260911.md) | Draft · amended (`AEG-HIE-007` batch dispatch) | Six identities, one chassis; fan-out chain resolution |
| AEGIS-RP-006 | 2026-09-11 | [aegis-rp-006-ticketing-plane-20260911.md](./aegis-rp-006-ticketing-plane-20260911.md) | Draft · amended | Ticketing Plane: Ticket Contract v1, adapters, Backup TS doctrine |
| AEGIS-RP-007 | 2026-09-11 | [aegis-rp-007-continuous-validation-20260911.md](./aegis-rp-007-continuous-validation-20260911.md) | Draft · §6.1 superseded (ADR-002/RP-009) | Continuous Validation System: linters, validators, assumptions, claims |
| AEGIS-RP-008 | 2026-09-12 | [aegis-rp-008-microbot-launch-roster-20260912.md](./aegis-rp-008-microbot-launch-roster-20260912.md) | Draft · amended (roster now 26) | Outline reconciliation + phased launch roster |
| AEGIS-RP-009 | 2026-09-12 | [aegis-rp-009-orchestration-gateway-20260912.md](./aegis-rp-009-orchestration-gateway-20260912.md) | Draft | Orchestration Gateway: conductor + Sequence/Barrier Gate + no-skip |
| AEGIS-RP-010 | 2026-09-13 | [aegis-rp-010-tower-surface-20260913.md](./aegis-rp-010-tower-surface-20260913.md) | Accepted (design) 09-13 | Tower v1: TBR API, TUF distribution, curators, ingest, query |
| AEGIS-RP-011 | 2026-09-13 | [aegis-rp-011-operator-brokering-20260913.md](./aegis-rp-011-operator-brokering-20260913.md) | Accepted (design) 09-13 | Brokering model: proxy-by-default, scoped-token escape hatch, pool schema |
| AEGIS-RP-012 | 2026-09-13 | [aegis-rp-012-knowledge-storage-retrieval-20260913.md](./aegis-rp-012-knowledge-storage-retrieval-20260913.md) | Accepted (design) 09-13 | Knowledge store & retrieval: record v1, tier stores, τ threshold, MCP contracts |
| AEGIS-RP-013 | 2026-09-13 | [aegis-rp-013-threat-model-20260913.md](./aegis-rp-013-threat-model-20260913.md) | Accepted (design) 09-13 · security-priority | Threat model, trust statement, run-log integrity, human tokens, TUF/DSSE/JCS |
| AEGIS-RP-014 | 2026-09-13 | [aegis-rp-014-bot-unit-creation-operation-20260913.md](./aegis-rp-014-bot-unit-creation-operation-20260913.md) | Accepted 09-13 (D8) · amendments applied | The bot unit: independence, directive/rules/principles triad, state & memory model, six communication channels, create→retire lifecycle |
| AEGIS-ADR-002 | 2026-09-13 | [aegis-adr-002-orchestration-coordination-model-20260913.md](./aegis-adr-002-orchestration-coordination-model-20260913.md) | Accepted 09-13 | Coordination model: event-triggered central orchestration over choreography |
| AEGIS-ADR-003 | 2026-09-13 | [aegis-adr-003-greenfield-command-surface-20260913.md](./aegis-adr-003-greenfield-command-surface-20260913.md) | Accepted 09-13 | Greenfield `aegis`; nine-domain surface; exit-code boundaries |
| AEGIS-ADR-004 | 2026-09-13 | [aegis-adr-004-layout-state-residency-20260913.md](./aegis-adr-004-layout-state-residency-20260913.md) | Accepted 09-13 | Port-registry path; spool residency; `.ai/aegis` cleanup; OS scope |
| AEGIS-ADR-005 | 2026-09-13 | [aegis-adr-005-backup-ticketing-system-20260913.md](./aegis-adr-005-backup-ticketing-system-20260913.md) | Accepted 09-13 | Backup TS: build minimal `aegis-backup-ts` over adopting a tracker |
| AEGIS-CANON-001 | 2026-09-13 | [aegis-canon-001-registries-20260913.md](./aegis-canon-001-registries-20260913.md) | Accepted 09-13 · registry authority | Canonical registries: 15 gates, events, refusal codes, linters, 26-bot roster, naming/IDs |
| AEGIS-CANON-002 | 2026-09-14 | [aegis-canon-002-platform-principles-20260914.md](./aegis-canon-002-platform-principles-20260914.md) | Proposed (final draft) · awaiting sign-off (D10) | HATHOR platform principles `hathor-principles@1` (HP-01..16), mapped to `aegis-principles@1`; review criteria, non-enforcing |
| AEGIS-CANON-003 | 2026-09-15 | [aegis-canon-003-documentation-framework-20260915.md](./aegis-canon-003-documentation-framework-20260915.md) | Accepted 09-15 (D12) · v0.2.1 erratum | HATHOR Documentation Framework `hathor-doc@1`: doc metadata schema, type/status/trust registries, SemVer + review/reviewed marks, staleness flag, INDEX + machine index/`llms.txt`, docs-as-code enforcement (`AEG-DOC-###`) |
| AEGIS-REQ-CORE-001 | 2026-09-11 | [AEGIS-REQ-CORE-001-initial-requirements-20260911.md](./AEGIS-REQ-CORE-001-initial-requirements-20260911.md) | Draft v0 (amended 09-13) | Consolidated platform requirements (PLAT/CLI/BOT/UPL/KNO/TKT/TEL/CNT/SEC/NFR) |
| AEGIS-ARCH-001 | 2026-09-11 | [AEGIS-ARCH-001-architecture-mermaid-20260911.md](./AEGIS-ARCH-001-architecture-mermaid-20260911.md) | Draft v0 (amended 09-13) | Visual companion to CORE-001 (+§19 validation fabric, +§20 AOG) |
| AEGIS-ARCH-002 | 2026-09-14 | [aegis-arch-002-bot-unit-compendium-20260914.md](./aegis-arch-002-bot-unit-compendium-20260914.md) | Draft v0 · synthesis · awaiting sign-off (D9) | Bot unit compendium: executive summary, 26-bot roster with definitions, family profiles, anatomy diagrams + explanation, memory/performance/state comparison tables |
| AEGIS-TS-001 | 2026-09-11 | [aegis-ts-001-continuous-validation-implementation-20260911.md](./aegis-ts-001-continuous-validation-implementation-20260911.md) | Draft · amended | CVS implementation spec (Go chassis); P0–P2 implementation-grade |
| AEGIS-TS-002 | 2026-09-13 | [aegis-ts-002-orchestration-gateway-implementation-20260913.md](./aegis-ts-002-orchestration-gateway-implementation-20260913.md) | Draft | Gateway implementation spec (run log, conductor, admission, reconciler) |
| AEGIS-TS-003 | 2026-09-13 | [aegis-ts-003-bot-unit-implementation-20260913.md](./aegis-ts-003-bot-unit-implementation-20260913.md) | Draft (implements RP-014) | Bot-unit implementation spec: bundle, governance engine (directive/rules/principles), effects, scaffold + registration, memory enforcement |
| AEGIS-TS-004 | 2026-09-14 | [aegis-ts-004-dmz-integration-boundary-20260914.md](./aegis-ts-004-dmz-integration-boundary-20260914.md) | Draft v0 · awaiting design basis (DMZ report, proposed RP-015) + D11 | DMZ implementation spec: outer/inner walls, project `rules.yaml`, policy floors, `POLICY_CONFLICT` envelope, report-only/dev/enforced profiles, onboarding ramp |
| AEGIS-PLAN-001 | 2026-09-13 | [aegis-plan-001-platform-roadmap-20260913.md](./aegis-plan-001-platform-roadmap-20260913.md) | Approved 09-13 | Platform roadmap: eight workstreams, milestones M-A..M-F |
| AEGIS-PLAN-002 | 2026-09-11 | [aegis-plan-002-cvs-p0-p2-roadmap-20260911.md](./aegis-plan-002-cvs-p0-p2-roadmap-20260911.md) | Draft · amended | CVS P0–P2 delivery roadmap + task breakdown |
| AEGIS-PLAN-003 | 2026-09-13 | [aegis-plan-003-gateway-validators-roadmap-20260913.md](./aegis-plan-003-gateway-validators-roadmap-20260913.md) | Approved 09-13 | Gateway epics; remaining validators; agent skill pack |
| AEGIS-PLAN-004 | 2026-09-15 | [aegis-plan-004-docs-refactor-knowledge-share-20260915.md](../../.ai/plans/aegis-plan-004-docs-refactor-knowledge-share-20260915.md) | Approved 09-15 (D13) · Phase 0.5 next | Corpus migration to `hathor-doc@1`; seven role guides; local Knowledge Plane share; verbatim archive; docs-as-code validation |
| — | 2026-09-11 | [aegis-containerization-article-20260911.md](./aegis-containerization-article-20260911.md) | Draft · annotated | Containerization: Class A–D taxonomy, anatomy isomorphism, micro-linters |
| — | 2026-09-11 | [aegis-containerization-presentation-script-20260911.md](./aegis-containerization-presentation-script-20260911.md) | Draft · annotated | Presentation companion to the containerization article |
| — | 2026-09-11 | [aegis-ticketing-economy-whitepaper-20260911.md](./aegis-ticketing-economy-whitepaper-20260911.md) | Draft · annotated | Business whitepaper companion to RP-006 |
| — | 2026-09-13 | [PENDING-EDITS.md](./PENDING-EDITS.md) | Register (living) | Cross-document amendment + sign-off tracking |
| — | 2026-09-13 | [sessions/2026-09-13-corpus-refactor-session-log.md](./sessions/2026-09-13-corpus-refactor-session-log.md) | Session record | Archived timeline of the corpus-refactor session (analysis → waves → sign-off → merge) |
| — | 2026-09-13 | [sessions/2026-09-13-corpus-refactor-summary-report.md](./sessions/2026-09-13-corpus-refactor-summary-report.md) | Session record | Summary report of the completed documentation refactor (findings, deliverables, metrics, outstanding) |

**Scope rule:** the corpus contains research, decisions, requirements, architecture, technical specifications, and plans. None authorizes implementation without the owning design approval and a Ticketing Plane ticket.

**System of record:** the greenfield AEGIS platform and `aegis` CLI (AEGIS-ADR-003), implementing the HATHOR agentic application framework. **Baseline system under study:** Communications (Hera) + `infraos-os` 9.3.0, retained as the migration/façade path per ADR-001/ADR-003.
