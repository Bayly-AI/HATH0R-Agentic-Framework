# AEGIS Research Paper 003 — Telemetry Transport

- **Document ID:** AEGIS-RP-003
- **Status:** DRAFT (research output — pending operator review)
- **Date:** 2026-09-11
- **Parent:** AEGIS-REQ-BOT-001 (§10 Q3)
- **Related:** AEGIS-RP-001 (telemetry manifest block), AEGIS-RP-002 (reconciliation events)
- **Amended by:** AEGIS-ADR-004 §2.2 (spool residency: project-tier canonical, machine-indexed — amends §3.1); event vocabulary extended by CORE-001 §10.1, RP-007 §8, TS-002 §11 — canonical registry: AEGIS-CANON-001 §3
- **Author:** Oz (Agent), commissioned by Raymond Bayly

---

## 1. Problem Statement

Every bot emits standardized telemetry (ANA-007, OBS-001) consumed by the Observation family and rolled up to the Control Tower (OBS-002). Undecided: transport. Candidates were **a machine-local event bus** vs **CLI-mediated push to Observation-Bot**. Constraints:

- Bots are stateless and mostly short-lived (RUN-002) — they cannot retry deliveries after exit.
- Telemetry must survive Observation-Bot downtime and Tower outages (RUN-003).
- Export must never fail or block business work (boards' doctrine; also Infra cr-observability-001's "export is asynchronous and MUST NOT fail business requests").
- No new resident daemons unless they demonstrably exceed simpler options.

## 2. Options

### Option A — Machine-local event bus (broker daemon)
A resident broker (NATS-like) on every machine; bots publish, Observation subscribes.
- Decoupled, buffered, proven pattern at scale.
- Cost: a new mandatory daemon on every AEGIS machine — a second control plane beside the CLI, its own health/upgrade/port surface (and port-registry governance burden), and a hard dependency for every bot run. For per-run, low-rate machine telemetry this is capacity we don't need at the machine tier. **Rejected for v1 machine tier.**

### Option B — Synchronous CLI-mediated push to Observation-Bot
Bot emits events through the CLI directly to Observation-Bot in the request path.
- No new infrastructure; consistent with CLI-as-control-plane.
- Cost: Observation-Bot availability becomes a business-path dependency — a down Observation-Bot blocks or loses telemetry from a finishing stateless bot. Violates the never-block constraint. **Rejected as sole mechanism.**

### Option C — Spool-and-drain: CLI-mediated write to a local append-only spool, drained by Observation-Bot (RECOMMENDED)
Bots emit events via the CLI, which appends them to a machine-local, append-only JSONL spool. Observation-Bot (resident) drains the spool asynchronously, fans events to its children (task/benchmark/success-rate/retry/token), and forwards rollups to the Tower.

Why it wins: emission is a local file append (microseconds, never blocks, works offline); durability is decoupled from every consumer; no broker daemon; replay is free (the spool is the buffer); and the CLI remains the single control plane. It is Option B's simplicity with Option A's buffering, minus the daemon.

## 3. Recommended Design

### 3.1 Emission path

1. Bot calls the CLI telemetry primitive (internally used by `report` and by lifecycle instrumentation).
2. CLI stamps the event (see §4), appends to the active spool segment under the project spool (`.aegis/state/spool/<date>/<segment>.jsonl`; non-project fallback and machine indexing per ADR-004 §2.2).
3. Append succeeds → bot proceeds. Append fails (disk full etc.) → bot logs locally and continues; `status --group telemetry` reports degraded (exit 2). Business work never fails on telemetry (ANA-007 note inverted: *disabled* telemetry is degraded, but telemetry failure is never fatal).

### 3.2 Drain path

- Observation-Bot tails spool segments with a persisted cursor (offset per segment), fans out to children, acknowledges by advancing the cursor.
- Delivery semantics: **at-least-once**, deduplicated by `event_id` (UUIDv7) at every consumer. Consumers MUST be idempotent.
- Tower forwarding: Observation-Bot batches rollups; Tower outage just leaves the cursor behind — nothing is lost within retention.

### 3.3 Retention & backpressure

- Spool segments rotate by size/day; retention default 7 days or drained+age>24h, whichever later.
- Disk-pressure ladder: warn (degraded) at 80% of spool quota → drop `debug`-severity events at 90% → hard stop appends at 100% with `TELEMETRY_SPOOL_FULL` degraded status. Never blocks the emitting bot.

### 3.4 Org tier

At the **Tower ingestion boundary** (many machines fanning in), a real bus/pipeline is justified and expected. That is Tower-internal design, out of scope here; the machine-tier contract is only "Observation-Bot delivers batched rollups at-least-once."

## 4. Event Envelope v1

```json
{
  "event_id": "01a0b6a4-…-uuidv7",
  "schema_version": "1.0.0",
  "event": "task.end",
  "occurred_at": "2026-09-11T11:58:00.123Z",
  "emitter": { "bot_uuid": "8f2c…", "name": "runbook-Bot", "family": "hierarchy", "manifest_digest": "sha256:…" },
  "run": { "run_id": "…", "binding_id": "…", "hierarchy_chain": "proc:…/strat:…/play:…/run:…", "project": "…", "machine": "…" },
  "severity": "info",
  "payload": { "outcome": "success", "duration_ms": 412, "tokens": { "in": 1200, "out": 300 }, "retries": 0 }
}
```

Core vocabulary (extensible per manifest `telemetry.events_emitted`): `task.start`, `task.end`, `retry`, `tokens`, `benchmark`, `contract.refused`, `registry.state_change`, `knowledge.microburst`, `degraded`.

UUIDv7 gives time-ordered IDs — cheap dedupe and ordering without a coordination service.

## 5. Requirements (AEG-TEL)

### AEG-TEL-001 — Spool-and-drain transport
Machine-tier telemetry uses CLI-mediated append to a local append-only spool, drained asynchronously by Observation-Bot. No broker daemon at machine tier in v1.
**AC:** Emitting bot's critical path contains no network I/O and no Observation-Bot dependency.

### AEG-TEL-002 — Never fatal
Telemetry failure never fails or blocks business work; it degrades `status` instead.
**AC:** With spool unwritable, a bot run still completes with correct business exit code; `status --group telemetry` returns 2.

### AEG-TEL-003 — At-least-once with idempotent consumers
Delivery is at-least-once end to end; every consumer dedupes on `event_id`.
**AC:** Replaying an entire spool segment produces zero double-counting in success-rate/token/benchmark aggregates.

### AEG-TEL-004 — Envelope conformance
All events conform to envelope v1; `event` names must appear in the emitter's manifest.
**AC:** Envelope-invalid or undeclared events are quarantined to a dead-letter segment and reported, never silently dropped.

### AEG-TEL-005 — Offline durability
Events survive Observation-Bot downtime and Tower outages within retention limits.
**AC:** A 24h Observation-Bot outage loses zero events given spool quota headroom; cursor resumes exactly.

### AEG-TEL-006 — Bounded disk usage
Spool obeys quota with the warn/shed/stop ladder; shedding order is severity-based, never business-outcome events first.
**AC:** `task.end` outcome events are the last class shed; quota breach is visible in `status` before any shedding starts.

### AEG-TEL-007 — Hierarchy traceability
Every event carries the hierarchy chain reference, satisfying RUN-001's traceability through telemetry.
**AC:** Spool/Tower data can reconstruct the telemetry view (chain, retries, tokens, outcome) and correlate it with the authoritative run/evidence ledgers and provider receipts; telemetry alone is not asserted as run-state authority.

## 6. Infra Adoption Decision Log

- **cr-observability-001 doctrine (async export, never fail business requests; collector owns routing/credentials) — Adopt the doctrine.** Observation-Bot plays the "collector" role at machine tier: it alone owns Tower forwarding; emitting bots know nothing about backends.
- **OTel Collector as the machine-tier transport — Reject for v1 machine tier.** A full collector+pipeline per machine is Option A by another name; exceeds need for per-run bot telemetry. Revisit at Tower ingestion, where the OTel→(collector)→backend pattern likely *does* exceed a homegrown pipeline and should be evaluated in the Tower design paper.
- **W3C-style context propagation (trace/run correlation) — Adopt the idea** via `run_id` + `hierarchy_chain` in the envelope rather than full W3C traceparent in v1; upgrade path stays open since envelope is versioned.

## 7. Open Questions

1. Spool quota default per machine (proposed 512 MB) — needs field sizing data.
2. Whether `contract.refused` events should also be surfaced synchronously to the caller's session log (UX question, not transport).
3. Severity taxonomy: is `debug` needed at all in v1, given shedding rules?

---

*Research output only. No implementation authorized.*
