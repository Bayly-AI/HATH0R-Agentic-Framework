# AEGIS-ADR-005 — Backup Ticketing System: Build vs Adopt

- **Document ID:** AEGIS-ADR-005
- **Status:** ACCEPTED — operator sign-off 2026-09-13 (PENDING-EDITS D3)
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Resolves:** RP-006 Q3 / CORE §17 Q6 (Backup TS implementation choice) — on the v1 acceptance path (CORE §16.8)
- **Related:** RP-006 §5 (doctrine: buffer + read-cache, never competing truth), RP-011 (Operator adapter), RP-013 (auth)
- **Scope rule:** decision record only. No implementation authorized.

---

## 1. Context

RP-006 §5 defines the Backup TS by four properties: implements Ticket Contract v1 verbatim; deliberately *small* (list/get/create/update/link — no sprints, boards, workflow engine); network-reachable so a multi-agent fleet shares one buffered view; and doctrinally a buffer/read-cache with `sync.state` semantics (`buffered → reconciled`), never a competing source of truth.

## 2. Options

| Option | Assessment |
|---|---|
| **A — Adopt Gitea Issues** | Self-hostable and mature, but drags a full forge (repos, PRs, users) for a buffer; no native `canonical_id`/`sync.state`/pre-image digest semantics — the adapter must bolt AEGIS's reconcile model onto labels/custom fields; its workflow surface invites exactly the "second competing tracker" RP-006 forbids. |
| **B — Adopt Redmine (light)** | Same shape of mismatch plus a heavier operational footprint (RDBMS, Rails) than the job warrants. |
| **C — Greenfield `aegis-backup-ts` (RECOMMENDED)** | A minimal service that stores Ticket Contract v1 documents natively: five endpoints (`list/get/create/update/link`), temporary `canonical_id` issuance, `sync.state` + pre-image digests as first-class columns, single-binary + embedded storage (SQLite), Class B container. The contract *is* the schema — zero translation beyond the standard adapter shape. |

## 3. Decision

**Build Option C — `aegis-backup-ts`.** Per Canonical Rule 4 the burden is on adoption to *exceed* a from-scratch design; here both adoption candidates subtract (translation debt, workflow surface, footprint) rather than add. The service is deliberately boring:

1. **Surface:** the five Ticket Contract operations over HTTP + health/version endpoints (CNT-005). Nothing else — no boards, no workflow engine, no notifications (RP-006 §5.2's "deliberately small" is a requirement, not a mood).
2. **Storage:** single-binary Go service, SQLite file, WAL mode; a Class B container with backup governance.
3. **Semantics:** `canonical_id` issuance for buffered tickets; `sync.state` transitions and pre-image digests exactly per RP-006 §5.3/§6 — reconciliation logic stays in the CLI/Operator, not in the backup.
4. **Auth:** machine identity per RP-010 §5 within the org boundary; no anonymous writes; multi-project scoping by project key.
5. **Reachability:** reached only via Operator-Bot's `backup` adapter (`provider.kind: backup`), like any provider (AEG-TKT-003).

## 4. Consequences

- **Positive:** contract round-trip (CORE §16.8) testable without translation shims; the buffer cannot grow into a second tracker because it has no features to grow into.
- **Negative:** one more first-party service to maintain — accepted; it is ~5 endpoints over a contract that must exist anyway.
- **Queued edits:** RP-006 §10 Q3 marked resolved-by-ADR-005; PLAN-001 WS5 carries the build (estimate included in WS5 line).

## 5. Compliance

Buffer-never-authority (RP-006 §5.4) preserved; deploy authority still requires a *reconciled* DVO ticket (`AEG-TKT-011`); provider-absent environments may declare the backup authoritative only via explicit config/ADR (RP-006 §5.3), unchanged.

---

*Decision record — ACCEPTED 2026-09-13. No implementation authorized by this document.*
