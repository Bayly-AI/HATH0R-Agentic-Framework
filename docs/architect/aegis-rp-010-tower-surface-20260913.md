---
id: HATHOR-RP-010
title: HATHOR-RP-010 — Control Tower Surface v1
summary: RFC 2119 keywords apply. Requirements use prefix `AEG-TWR-###`.
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
# HATHOR-RP-010 — Control Tower Surface v1

- **Document ID:** HATHOR-RP-010
- **Status:** ACCEPTED (design) — operator sign-off 2026-09-13 (PENDING-EDITS D5); open questions tracked in §7
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Resolves:** CORE-001 §17 Q3 (Tower service surface v1) at interface level; unblocks acceptance criteria CORE §16.5/§16.8 and `AEG-KPW-002` (curator registry)
- **Related:** RP-001 (signed manifests), RP-002 (TBR/MBI, reconciliation, trust TTL), RP-003 §3.4 (ingestion boundary), RP-004 §2.2 (curators), RP-013 (key distribution via TUF)
- **Scope rule:** research and interface design only. No implementation authorized.

RFC 2119 keywords apply. Requirements use prefix `AEG-TWR-###`.

---

## 1. Problem statement

The Tower is cited as authority in a dozen requirements (TBR, CRL, keys, curators, rollups) but has no surface specification, leaving several v1 acceptance criteria untestable. This paper fixes the **minimal v1 surface**: a small REST service plus signed distribution artifacts. The browser UI remains v2 (CORE §1.2).

## 2. Shape decision

**Tower v1 = one small REST service + offline-verifiable signed artifacts.** Not a message bus, not a UI, not a bot (`AEG-REQ-BOT-006`). Ordinary bot/capability dispatch never depends on Tower availability (RP-002 `AEG-REG-001`); reconciliation/distribution/ingest is asynchronous, while an explicit `aegis tower …` authority command or query is a direct authenticated Tower request.

**Access path.** The Tower is a *plane authority*, not an external provider: the CLI reaches it directly under `aegis tower …` using platform identity (see §5), **not** via Operator-Bot. Operator-Bot brokers third-party systems; brokering the platform's own authority through the external-connection broker would invert the trust relationship and make Operator a single point of authority compromise.

## 3. Surface v1 (five facets)

### 3.1 Registry authority (TBR) — write path
- `POST /v1/registrations` — submit `{bot_uuid, manifest_digest, manifest, dsse_envelope}`; the external DSSE payload is the JCS-canonical manifest bytes (RP-001 §2.2). Response: `pending | acknowledged | rejected{reason}` (family conflict, unknown key, revoked). Drives `verified-local → verified-tower` (RP-002 §3.2).
- `GET /v1/registrations/{digest}` — registration state for reconciliation.
- `POST /v1/revocations` — operator-only; adds a digest/key to the CRL.

### 3.2 Distribution — signed, cacheable, offline-verifiable
- `GET /v1/dist/keys` — signing-key bundle (TUF-role layout per RP-013 §6), each with validity/TTL.
- `GET /v1/dist/crl` — revocation list, signed, versioned, TTL-stamped.
- `GET /v1/dist/policy` — org policy pack (trust TTL values, strict-mode defaults, signed suites/graphs index).
All three are static-cacheable documents; a machine verifies them offline within TTL (`AEG-MAN-006`, `AEG-REG-004`).

### 3.3 Curator registry (RP-004 §2.2)
- `GET /v1/curators?domain=…` — who may promote org-tier knowledge per domain.
- `POST /v1/curators` — operator-only maintenance. Auditable; consumed by the Knowledge Promotion Gate (`AEG-KPW-002`).

### 3.4 Ingest — telemetry rollups
- `POST /v1/ingest/rollups` — batched envelopes from Observation-Bot (RP-003 §3.2); at-least-once, deduped on `event_id`; responds with high-water cursor so drains resume exactly.

### 3.5 Query — read APIs (v1 minimal)
- `GET /v1/query/runs/{run_id}` — reconstructed run (chain, tickets, findings, waivers) per `AEG-REQ-TEL-007`.
- `GET /v1/query/validation?class=…` — pass-rates by class (RP-007 P5), suite latency vs budget, waiver audit, skipped-unit/completeness-gap MTTR (TS-002 §14.2).
Bounded per `AEG-REQ-CLI-003` semantics (`limit/cursor/fields` query params).

## 4. Reconciliation contract (normative restatement)

On connect and on schedule, the CLI: pushes pending registrations (§3.1) → pulls keys/CRL/policy (§3.2) → quarantines revoked digests **before next dispatch** (`AEG-REG-005`) → emits `registry.state_change` telemetry. Trust TTLs on cached artifacts bound offline autonomy (`AEG-REQ-PLAT-007`).

## 5. Identity & authn (v1)

- **Machine identity:** per-machine keypair enrolled at first reconciliation (TUF-rooted trust per RP-013; resolves RP-002 Q3 bootstrap). Requests signed; no long-lived bearer tokens.
- **Human identity:** operators/curators authenticate via org IdP (OIDC) to obtain short-lived Tower-signed identity tokens — the same tokens RP-013 §5 requires for human-only waivers and deploy-critical operations.

## 6. Requirements (AEG-TWR)

### AEG-TWR-001 — Minimal REST surface v1
Tower v1 MUST expose exactly the five facets in §3; no UI, no bus, no request-path dependency.
**AC:** All CORE §16.5/§16.8 acceptance tests are executable against this surface; no ordinary bot/capability-dispatch trace contains a Tower call, while explicit `aegis tower …` traces do.

### AEG-TWR-002 — Offline-verifiable distribution
Keys, CRL, and policy MUST be signed documents verifiable offline within their TTL.
**AC:** A machine offline since its last pull verifies manifests and refuses expired trust with no Tower connectivity.

### AEG-TWR-003 — Registration acknowledgement flow
Registration MUST be asynchronous with explicit `pending/acknowledged/rejected` states driving MBI verification states.
**AC:** State transitions in RP-002 §3.2 map 1:1 to API responses.

### AEG-TWR-004 — CRL precedence
A pulled CRL MUST quarantine matching digests before any further dispatch on that machine.
**AC:** Post-reconcile, a revoked bot receives zero requests (`AEG-REG-005` AC restated at the surface).

### AEG-TWR-005 — Curator registry as the promotion authority source
The Knowledge Promotion Gate MUST resolve org-tier reviewer authority from §3.3, cached with TTL.
**AC:** Promotion by a non-registered identity is refused offline within TTL and online always.

### AEG-TWR-006 — Idempotent ingest
Ingest MUST be at-least-once safe: replaying a batch produces zero double-counting.
**AC:** Replay test of a full rollup batch changes no aggregate.

### AEG-TWR-007 — Bounded query contract
Query endpoints MUST support limit/cursor/fields with the same defaults as the CLI contract.
**AC:** No default query response exceeds 8 KB.

### AEG-TWR-008 — Signed human identity issuance
Tower MUST issue short-lived, verifiable human identity tokens for waiver/deploy-authority operations (consumed per RP-013 §5).
**AC:** A waiver record carries a verifiable human token reference, not a TTY inference.

## 7. Open questions

1. Multi-org tenancy: one Tower per org (lean) vs multi-tenant service.
2. Storage backend (any durable KV/RDBMS; out of scope for the surface contract).
3. Ingest scale-out: when does the ingestion boundary justify the RP-003 §3.4 pipeline (Tower-internal; revisit at P5 volumes).
4. IdP specifics (OIDC provider per org) and token lifetime defaults.

---

*ACCEPTED (design) 2026-09-13. No implementation authorized by this document; open interface details remain tracked in §7.*
