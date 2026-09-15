---
id: AEGIS-GUIDE-014
title: Platform Engineer Guide
summary: 'Platform Engineers build the core AEGIS platform: the CLI, the Go chassis, the orchestration bots, the validation fabric, and the Control Tower API.'
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: []
version: 0.1.0
status: draft
created: '2026-09-14'
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
# Platform Engineer Guide

Platform Engineers build the core AEGIS platform: the CLI, the Go chassis, the orchestration bots, the validation fabric, and the Control Tower API.

## 1. CLI and Core Chassis (Go)

AEGIS is a greenfield implementation written primarily in Go 1.23+. 
* **Exit-Code Boundaries:** The CLI enforces the canonical 0-7 exit codes. Any deviation must be caught during development.
* **CLI Spec:** All top-level commands must support `--output json|text|auto`, `--profile`, `--quiet`, and pagination (`--fields`, `--limit`, `--cursor`).
* **Schema Introspection:** Must expose a bounded schema surface (`aegis schema --domain <x>`) mapped to the CLI Spec error envelope and bounded to ≤ 8 KB per page default.
* **Routing:** `Proctor-Bot` handles capability-based routing (e.g., `domain.noun.verb@major`). The CLI negotiates the HELLO/OFFER/BIND/VERIFY handshake via the Machine-Local Index (MBI).

## 2. Orchestration Gateway

The Orchestration Gateway consists of three distinct layers:
1. **Events Trigger:** External actions (e.g., file writes, git staging, step completion) append to `events.jsonl`.
2. **Conductor Decides:** `Process-Bot` acts as the saga state machine, folding the run log. The plan is treated as data, and `Process-Bot` alone advances the run state.
3. **Gateway Enforces:** `Proctor-Bot` and the Sequence/Barrier Gates refuse unlawful dispatch based on the 15 Governance Gates (AEGIS-CANON-001 §2).

## 3. Validation Fabric (Four Altitudes)

Build out the immune system across four altitudes:
1. **Build-Time (1):** Micro-linters (pure, exit 0|2). Un-linted images must fail the build.
2. **Change-Time (2):** Micro-linters + Validator bots (`val-*`). They refuse changes, assumptions, or claims.
3. **Dispatch-Time (3):** Proctor gates (G01-G09). Refuse unlawful dispatch.
4. **Runtime (4):** Observation family. Record only (never refuse).

## 4. Ticketing and Knowledge Planes

* **Ticketing Plane:** Implement and maintain adapters for Jira, ADO, GitHub, and the Backup TS. Ensure strict adherence to the Ticket Contract v1. Deal with authority reconciliation (upstream wins) and buffered states (`degraded: true`).
* **Knowledge Plane:** Maintain the local vector server and CLI knowledge indexing. Ensure the draft-to-verified promotion queue functions strictly as a view, with no auto-promotion logic whatsoever. All state must live on the record.

## 5. Control Tower Authority

The Control Tower is the authoritative, asynchronous backend for the registry, policy, identity, revocation, ingest, and audit query. 
* **Not a Bot:** It is not a bot, does not execute jobs, and is not the terminus of every request.
* **Lean API:** Keep its API surface lean (REST service with 5 facets).
* **Offline Verification:** Artifacts it distributes (keys, manifests) must be verifiable offline.
* **Bounded Degradation:** Guarantee that disconnected clients can operate within their trust TTL (`verified-local`), securely degrading to `PROVENANCE_UNVERIFIED` when the TTL expires.
