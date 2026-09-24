# AEGIS-RP-011 — Operator-Bot Brokering Model

- **Document ID:** AEGIS-RP-011
- **Status:** ACCEPTED (design) — operator sign-off 2026-09-13 (PENDING-EDITS D5); open questions tracked in §7
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Resolves:** the undefined mechanism behind "brokered sessions" (`AEG-BOT-ANA-006`, `AEG-REQ-SEC-002`, `AEG-REQ-TKT-003`) — the corpus's most load-bearing unspecified phrase
- **Related:** RP-001 §2.7 (connection names), RP-006 §4 (adapters), RP-008 §5 (adapter roster), TS-002 §5.3 (idempotency keys), RP-013 (threat model)
- **Scope rule:** research and interface design only. No implementation authorized.

RFC 2119 keywords apply. Requirements use prefix `AEG-OPB-###`.

---

## 1. Problem statement

Every security invariant in the corpus leans on "worker bots receive brokered sessions; they never resolve or hold credentials" — but *brokered session* is never defined. Two materially different mechanisms hide behind the phrase:

- **Proxy:** the worker's external call is executed *inside* Operator-Bot; the worker sees only the canonical result. Credentials never exist outside the broker.
- **Token handoff:** Operator-Bot mints a scoped, short-lived credential and hands it to the worker, which calls the provider itself. The worker transiently *does* hold a credential.

These differ in secrecy strength, throughput, failure domain, and auditability. Leaving the choice implicit invites the weakest interpretation.

## 2. Decision: proxy-by-default, scoped-token escape hatch

### 2.1 Class 1 (default) — full proxy
All capability-mediated external calls (`work.ticket.*`, notifications, API reads/writes) execute inside Operator-Bot. The worker submits a canonical request via Proctor; Operator resolves the connection, applies credentials, performs the call, and returns the canonical result.

- **Secrecy:** the invariant "secrets never appear in a worker's config, logs, or memory" (`AEG-BOT-ANA-006` AC) is *structural*, not behavioral — there is nothing to leak.
- **Audit:** one chokepoint records every external side effect with intent + idempotency key (`AEG-REQ-SEC-006`).
- **Throughput/failure domain:** acceptable at v1 volumes (per-run, human-scale side effects); Operator is resident with `drain|stop` (`AEG-BOT-CMD-019`) and its outage degrades exactly the paths that need external systems — which RP-006's buffering already tolerates.

### 2.2 Class 2 (exception) — scoped short-lived token
Only for protocols where proxying is impractical (bulk/streaming transports, e.g. `git` over HTTPS, large artifact up/downloads). Operator mints a credential that is **scoped** (narrowest provider scope that satisfies the request), **short-lived** (TTL ≤ session TTL, default ≤ 15 min), **bound** to `{run_id, capability, connection}`, **audited** (mint + expiry records in the Operator audit ledger), and **never persisted** by the worker (memory-only; writing it anywhere is a `ml-secrets-diff`/`ml-broker-symmetry` violation).

Class 2 usage is declared per connection entry (§3) — a worker cannot request a token for a Class 1 connection.

## 3. Connection pool schema (v1)

```yaml
# operator pool entry (names only — credentials stay in the secrets manager)
- name: jira
  kind: atlassian
  class: 1                       # 1 = proxy-only, 2 = token-eligible
  auth_ref: sm://org/jira/api    # secrets-manager path (SEC-001 order applies)
  scopes: [tickets.read, tickets.write]
  rate_limit: { rps: 5, burst: 10 }
  circuit: { failure_threshold: 5, cooldown: 60s }
  degraded_fallback: queue-local # RP-001 §2.7 hint honored
  health_probe: { interval: 300s, budget_ms: 2000 }
```

A **session** is `{session_id, connection, capability, run_id, ttl, idempotency_namespace}` — the handle a worker holds. For Class 1 it authorizes proxied calls; for Class 2 it scopes the minted token. Sessions are validated/reused before creation (`AEG-BOT-ANA-006` AC).

## 4. Idempotency, rate limiting, degradation

- **Idempotency-key store:** external side effects carry keys derived from `(run_id, node_id, attempt)` (TS-002 §5.3); Operator persists seen keys per connection (bounded window ≥ trust TTL) and returns the recorded result on replay — resume never double-commits (ARCH §17, `AEG-GW-004`).
- **Rate limiting + circuit breaking:** per pool entry; breaker-open surfaces as `dependency unhealthy` (exit 6) with the standard envelope, and eligible writes route to the degraded path (Backup TS buffering, RP-006 §5).
- **Degradation:** provider unreachable → honor `degraded_fallback`; runs flagged `degraded: true` (ADR-003 §2.3); bounded by trust TTL (`AEG-REQ-TKT-009`).

## 5. Adapter interface

Adapters remain non-bots (`AEG-MBL-003`): in-process modules behind a single interface `(canonical_request) → canonical_result` mirroring the TS-001 §9.1 capability seam, invoked only by Operator-Bot. Org-distributed adapters ship as signed packs (RP-013 §7). The out-of-proc upgrade path reuses the TS-001 §14 seam.

## 6. Requirements (AEG-OPB)

### AEG-OPB-001 — Proxy is the default brokering class
All external capabilities default to Class 1; the worker never receives provider credentials or endpoints.
**AC:** Static + runtime checks show zero credential material in any worker process for Class 1 flows.

### AEG-OPB-002 — Token escape hatch is declared, scoped, short-lived
Class 2 is available only for connections declared `class: 2`; tokens are scoped, TTL-bounded, run-bound, audited, never persisted.
**AC:** Token mint/expiry audit records exist for every Class 2 session; a persisted token is detected by linters and refused.

### AEG-OPB-003 — Pool schema with names only
Pool entries carry `auth_ref` paths, never credential values; resolution follows SEC-001 order.
**AC:** Pool file contains zero secrets; `ml-secrets-diff` clean.

### AEG-OPB-004 — Session validate-and-reuse
Operator MUST validate/reuse pool sessions before creating new ones.
**AC:** Session-churn metric visible; duplicate concurrent sessions per (connection, run) do not occur.

### AEG-OPB-005 — Idempotent external effects
Every mutating external call carries an idempotency key; replay returns the recorded result.
**AC:** Kill-and-resume test produces exactly one provider-side effect.

### AEG-OPB-006 — Rate limits and circuit breaking per connection
Breaker state surfaces as exit 6 with remediation; eligible writes take the degraded path.
**AC:** Provider brownout test shows no unbounded retry storm (interacts with `AEG-BOT-RUN-004` cap).

### AEG-OPB-007 — Single audit chokepoint
Every external side effect is recorded with capability, run, ticket, connection, and key.
**AC:** Tower can enumerate all external effects for a run (`AEG-REQ-TEL-007` extension).

### AEG-OPB-008 — Adapters are signed, non-autonomous modules
Adapters carry no manifest identity, are invoked only by Operator-Bot, and org-distributed adapters are signature-verified.
**AC:** MBI shows no adapter entries; unsigned org adapter refuses to load.

## 7. Open questions

1. Class 2 catalog: which v1 connections genuinely need tokens (lean: git transport only).
2. Operator HA: single resident per machine (lean, v1) vs shared per team — ties to Backup TS coordination.
3. Per-provider rate policy defaults; provider-specific retry taxonomies.
4. Result-size limits for proxied calls (streaming threshold that forces Class 2).

---

*ACCEPTED (design) 2026-09-13. No implementation authorized by this document; open interface details remain tracked in §7.*
