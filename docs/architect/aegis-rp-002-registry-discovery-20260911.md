---
id: AEGIS-RP-002
title: AEGIS Research Paper 002 — Bot Registry & Discovery Model
summary: 'Proctor-Bot routes requests by capability (AEG-MAN-003) and must verify provenance before dispatch (SEC-003). Question: does Proctor discover bots via the **Control Tower registry**, a **machine-local manifest scan**,...'
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
# AEGIS Research Paper 002 — Bot Registry & Discovery Model

- **Document ID:** AEGIS-RP-002
- **Status:** DRAFT (research output — pending operator review)
- **Date:** 2026-09-11
- **Parent:** AEGIS-REQ-BOT-001 (§10 Q2)
- **Related:** AEGIS-RP-001 (manifest digest, signed provenance)
- **Amended by:** AEGIS-ADR-003 §2.3 (exit-code boundaries — §3.3's "degraded (exit 2)" reads as envelope `degraded:true`; exit 2 applies at the bot boundary only); AEGIS-RP-013 §6 (2026-09-13, operator-approved: key distribution/rotation/revocation via TUF roles served by the Tower — resolves §6 Q3)
- **Author:** Oz (Agent), commissioned by Raymond Bayly

---

## 1. Problem Statement

Proctor-Bot routes requests by capability (AEG-MAN-003) and must verify provenance before dispatch (SEC-003). Question: does Proctor discover bots via the **Control Tower registry**, a **machine-local manifest scan**, or **both**? The answer must satisfy two constraints that pull in opposite directions:

- **Graceful degradation (RUN-003):** a machine must keep working when the Tower is unreachable.
- **Provenance verification (SEC-003):** unverified bots must never receive work.

## 2. Options

### Option A — Tower registry only
Every capability lookup and provenance check is a Tower round-trip.
- Single source of truth; instant org-wide revocation.
- Fails the degradation constraint outright: Tower outage halts every machine. Adds per-request latency. Rejected.

### Option B — Machine-local manifest scan only
The CLI scans installed bots, indexes their manifests, routes locally.
- Fast, fully offline.
- No org-wide authority: a tampered or revoked bot remains routable; no cross-machine consistency; provenance reduces to self-attestation. Rejected.

### Option C — Hybrid: local index as router, Tower as authority (RECOMMENDED)
Signed manifests (AEG-MAN-006) make the hybrid safe: verification is cryptographic and local, authority and revocation are central and asynchronous.

## 3. Recommended Design

### 3.1 Two artifacts

1. **Machine Bot Index (MBI)** — built and owned by the CLI. Created at bot install/update time (not by scanning at request time). Maps `capability → {bot_uuid, manifest_digest, verification_state, verified_at}`. Stored machine-local; queryable via `aegis bots list`.
2. **Tower Bot Registry (TBR)** — org-wide authority. Holds registered manifest digests, signing keys, revocation list (CRL), and family/tier assignments (enforces TAX-002's "no bot in two families").

### 3.2 Registration flow

1. Bot installed on machine → CLI canonicalizes + digests manifest (AEG-MAN-001), verifies signature against cached Tower keys, applies structural checks (AEG-MAN-007).
2. On success: entry added to MBI as `verified-local`; registration event queued to Tower.
3. Tower acknowledges → entry becomes `verified-tower`. Tower rejection (unknown digest, revoked key, family conflict) → entry quarantined, Proctor refuses routing (`PROVENANCE_UNVERIFIED`), operator alerted.

### 3.3 Runtime resolution (Proctor)

- Lookup is **always MBI-only** — no Tower call in the request path. Steady-state routing cost is one local index hit plus the digest comparison from the handshake fast path (AEGIS-RP-001 §3.5).
- Trust rules by verification state:
  - `verified-tower` → route normally.
  - `verified-local` (Tower ack pending/unreachable) → route, but mark the run **degraded** (exit 2 semantics propagate to `status`), and cap at a trust TTL.
  - `quarantined` / expired trust TTL → refuse.

### 3.4 Reconciliation loop

- CLI ↔ Tower sync on connect and on schedule: push pending registrations, pull CRL + key updates, demote revoked digests to `quarantined` immediately. Key/CRL/policy distribution uses the TUF role layout with client rollback protection (RP-013 §6, RP-010 §3.2).
- **Trust TTL:** `verified-local` entries and cached keys/CRL carry a TTL (proposed: 72h). Beyond it, unreconciled entries stop routing — bounded offline autonomy, not indefinite drift.
- All reconciliation outcomes are telemetry events (AEGIS-RP-003) rolled up to the Tower (OBS-002).

### 3.5 Failure modes

- **Tower unreachable:** routing continues on `verified-tower` + in-TTL `verified-local`; degraded flags surface honestly. Matches the boards' graceful-degradation doctrine.
- **Manifest drift (binary changed, manifest didn't):** `selftest`/digest mismatch fails closed (AEG-MAN-001); MBI entry quarantined.
- **Revocation while offline:** bounded by trust TTL; on reconnect CRL wins immediately.
- **Two bots claim one capability:** both listed; Proctor picks by (verification state, contract version, benchmark score from benchmark-Bot). Tie-break policy is Proctor-owned (AEGIS-RP-001 open question 2).

## 4. Requirements (AEG-REG)

### AEG-REG-001 — Hybrid registry
Discovery uses the machine-local MBI for all runtime resolution; the Tower TBR is the sole authority for registration, keys, and revocation.
**AC:** No Tower round-trip appears in any request-path trace; revocations propagate on next reconciliation.

### AEG-REG-002 — Install-time indexing
The MBI is updated at install/update time, never by request-time filesystem scanning.
**AC:** Request-path latency is independent of the number of installed bots' manifest sizes.

### AEG-REG-003 — Verification states
Every MBI entry is exactly one of `verified-tower | verified-local | quarantined`; only the first two are routable, and `verified-local` only within trust TTL.
**AC:** State transitions are logged as telemetry events; refusals carry `PROVENANCE_UNVERIFIED`.

### AEG-REG-004 — Bounded offline trust
`verified-local` routing and cached key/CRL validity expire at trust TTL (default 72h, Tower-configurable).
**AC:** A machine offline beyond TTL refuses new-bot routing while continuing `verified-tower` bots; `status --group contract` reports the condition as degraded.

### AEG-REG-005 — Immediate revocation on reconcile
CRL entries quarantine matching MBI digests before any further dispatch.
**AC:** Post-reconciliation, a revoked bot cannot receive a single request.

### AEG-REG-006 — Registry introspection
`aegis bots list` exposes the MBI (identity, capabilities, state, digests) in JSON and human form.
**AC:** Output is sufficient to diagnose any routing refusal without Tower access.

## 5. Infra Adoption Decision Log

- **Infra canonical registry pattern (`cfg/gen3-port-registry.yaml`: central file = truth, running state = ground truth, drift = fix-the-repo) — Adopt the doctrine, not the mechanism.** The TBR-as-authority / MBI-as-runtime split with drift quarantine is the same governance idea; a YAML file without signatures or revocation would not exceed requirements, so the mechanism is new.
- **Infra MCP-health-first connectivity checks (cr-docker-ports-001 §MCP failures) — Adopt.** "Confirm canonical source before declaring a service down" maps directly to §3.5 failure handling.

## 6. Open Questions

1. Trust TTL default: 72h proposed — validate against real offline patterns (field data needed).
2. Whether the MBI should be per-machine or per-project-workspace when multiple AEGIS projects coexist on one machine (boards' Universal Project Layout suggests machine-level with project overlays).
3. ~~Key distribution bootstrap~~ **Resolved (2026-09-13):** TUF root of trust pre-provisioned with the CLI install; machine enrollment at first reconciliation per RP-010 §5 (RP-013 §6).

---

*Research output only. No implementation authorized.*
