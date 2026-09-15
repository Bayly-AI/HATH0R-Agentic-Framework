---
id: AEGIS-RP-005
title: 'AEGIS Research Paper 005 — Hierarchy Topology: Six Bots vs One Process-Bot with Six Tier Adapters'
summary: 'The boards draw six Information Hierarchy bots (Procedure → Strategy → Playbook → Runbook → Workflow → Checklist), each queried by Process-Bot. The open question: keep **six bots**, or consolidate into **one Process-B...'
doc_type: RP
diataxis: explanation
audience: [architect, agent]
tags: []
version: 0.1.0
status: draft
created: '2026-09-11'
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
# AEGIS Research Paper 005 — Hierarchy Topology: Six Bots vs One Process-Bot with Six Tier Adapters

- **Document ID:** AEGIS-RP-005
- **Status:** DRAFT (research output — pending operator review)
- **Date:** 2026-09-11
- **Parent:** AEGIS-REQ-BOT-001 (§10 Q5)
- **Related:** AEGIS-RP-001 (capability routing, fast path), AEGIS-RP-002 (per-bot registry entries), AEGIS-RP-003 (per-tier telemetry)
- **Amended by:** batch-dispatch primitive formalized 2026-09-13 (§4, `AEG-HIE-007`) — closes the PENDING-EDITS §3 item behind ARCH-001 §6's wave model
- **Author:** Oz (Agent), commissioned by Raymond Bayly

---

## 1. Problem Statement

The boards draw six Information Hierarchy bots (Procedure → Strategy → Playbook → Runbook → Workflow → Checklist), each queried by Process-Bot. The open question: keep **six bots**, or consolidate into **one Process-Bot with six internal tier adapters**? Per canonical rule, the boards' design stands unless consolidation *exceeds* it — the burden of proof is on consolidation.

## 2. Evaluation Criteria

Drawn from AEGIS-REQ-BOT-001: microbot purity (TAX-001), taxonomy integrity (TAX-004), chain traceability, per-tier observability (OBS-001), operational overhead (manifests, versions, registry entries), chain latency (RUN-001 request lifecycle), and failure isolation (RUN-003).

## 3. Options

### Option A — Six independent bots (boards as drawn)
- **For:** perfect TAX-001 fit (one bot, one tier); independent versioning — a checklist format change ships without touching procedure logic; per-tier telemetry and benchmarks fall out naturally (benchmark-Bot scores each tier separately); failure isolation — a broken Workflow-Bot leaves Procedure→Runbook resolution alive, enabling honest partial degradation; per-tier capability grants match the routing vocabulary (`hierarchy.resolve.<tier>@1`).
- **Against:** six manifests/versions/registry entries to maintain; naive chain resolution costs six sequential CLI hops; risk of the six drifting apart structurally (schema divergence between tiers).

### Option B — One Process-Bot with six internal tier adapters
- **For:** one manifest/version/deployment; no inter-tier hops (in-process); single schema authority.
- **Against:** violates TAX-001 (one bot, seven responsibilities: orchestration + six tiers); single failure domain — any tier defect degrades all resolution, and graceful *partial* degradation becomes internal simulation rather than architectural truth; telemetry loses its natural per-emitter granularity (must be re-invented via payload conventions); tier evolution is serialized through one release train; blurs Process-Bot's orchestration role with tier ownership, weakening the family boundaries (TAX-002/003). Consolidation must *exceed* the boards' design; saving five manifests does not outweigh losing isolation, granular observability, and taxonomy integrity. **Rejected as architecture.**

### Option C — Six identities, one chassis (RECOMMENDED)
Keep **six logical bots** — six manifests, six registry entries, six contract surfaces, six telemetry emitters — implemented from **one shared tier-bot chassis** (single codebase/template, parameterized per tier, per ANA-004 code-agnosticism this is an implementation freedom the architecture already grants).

This captures Option B's real benefits where they actually live (shared implementation: one schema engine, one test suite, structural anti-drift by construction) without surrendering any architectural property of Option A. The six bots can still version independently: chassis version is provenance (`source_repo: aegis/hierarchy-chassis`), while each identity's manifest/contract evolves on its own schedule.

## 4. The Latency Objection, Dissolved

The strongest argument for consolidation is six sequential hops. It is answered at the orchestration layer, not by merging bots:

1. **Fan-out resolution:** Process-Bot issues tier queries as a **batched fan-out** (one CLI round trip carrying six sub-requests) rather than a sequential walk. Tiers whose inputs depend on a parent's output (Strategy needs the chosen Procedure) resolve in dependency waves — worst case 2–3 waves, not 6 hops.
2. **Handshake fast path:** per AEGIS-RP-001 §3.5, steady-state per-bot overhead is a digest comparison; there is no repeated negotiation cost across the chain.
3. **Chain caching:** resolved chains are cacheable keyed by (intent, project, manifests-digest-set) with TTL; repeat work on the same procedure re-resolves only invalidated links.

**Batch-dispatch primitive (formalized 2026-09-13).** The fan-out in item 1 is realized by a Process-Bot-owned capability **`hierarchy.resolve.chain@1`**: one CLI round trip carries a wave's sub-requests `[{tier, ref | selector}]`; the response returns per-entry results or per-entry structured refusals. Partial tier failure degrades the affected entry (AEG-HIE-005 semantics) — it never fails the wave. Fan-out to the tier bots happens inside Process-Bot via Proctor dispatch; callers never batch across unrelated runs. Normative form: `AEG-HIE-007` below.

With these, Option A/C latency approaches Option B's within noise for real workloads, while keeping every architectural property. (Benchmark-Bot should validate this empirically — see §7.)

## 5. Recommendation

**Adopt Option C.** The boards' six-bot taxonomy stands as the architecture (TAX-004 unchanged); the chassis is an implementation note recorded here so the six do not drift. Consolidation into one bot is rejected: it does not exceed the current design — it trades architectural properties for a convenience the chassis already provides.

## 6. Requirements (AEG-HIE)

### AEG-HIE-001 — Six logical identities
The Information Hierarchy comprises six registered bots with distinct UUIDs, manifests, contracts, and telemetry emitter identities.
**AC:** Registry (MBI/TBR) shows six entries; telemetry aggregates are queryable per tier with no payload-level disambiguation.

### AEG-HIE-002 — Shared chassis permitted, drift forbidden
Tier bots MAY share an implementation chassis; structural schema for tier records MUST be chassis-enforced.
**AC:** Cross-tier structural conformance tests pass from a single suite; chassis version appears in each bot's provenance.

### AEG-HIE-003 — Independent versioning
Each tier bot's manifest/contract versions evolve independently of the chassis and of sibling tiers.
**AC:** A Checklist-Bot contract bump ships with zero manifest changes to the other five.

### AEG-HIE-004 — Fan-out chain resolution
Process-Bot resolves chains via batched dependency-wave fan-out, not sequential per-tier hops.
**AC:** Chain resolution issues ≤3 CLI round-trip waves for a full six-tier chain; traces show wave structure.

### AEG-HIE-005 — Partial degradation honesty
A failed tier bot degrades only its tier and below; upstream resolution continues and the chain is reported as partial (exit 2 semantics).
**AC:** With Workflow-Bot quarantined, Procedure→Runbook resolution succeeds and the run carries an explicit partial-chain flag.

### AEG-HIE-006 — Chain cache with digest invalidation
Resolved chains are cacheable, keyed on the participating manifests' digests; any tier redeploy invalidates affected chains.
**AC:** No cached chain is served across a manifest digest change of any participating bot.

### AEG-HIE-007 — Batch-dispatch primitive *(added 2026-09-13)*
Chain resolution MUST expose a single-round-trip batch capability (`hierarchy.resolve.chain@1`, Process-Bot-owned) that carries one wave's sub-requests and returns per-entry results or structured refusals; partial tier failure degrades the entry, never the wave.
**AC:** A fully pre-linked chain resolves in ≤ 3 such calls (NFR-004); traces show one CLI round trip per wave; with one tier quarantined, sibling entries in the same wave still succeed and the chain reports partial (AEG-HIE-005).

## 7. Open Questions

1. Empirical latency validation: benchmark-Bot comparison of fan-out vs sequential resolution on representative chains (research task once a prototype exists — still within research-only scope if simulated).
2. Chain cache TTL and scope (per-project vs per-machine).
3. Whether Checklist-Bot's write-heavy profile (always-updated state, per the boards) warrants a chassis variant with different knowledge-write ergonomics.

## 8. Infra Adoption Decision Log

- **Infra monolithic CLI with internal service modules — Reject** as precedent for Option B; AEGIS's family/taxonomy boundaries are the point of the new system.
- **Infra "single codebase, many commands" maintenance economics — Adopt the economics** via the chassis (Option C), where it strengthens rather than erodes the taxonomy.

---

*Research output only. No implementation authorized.*
