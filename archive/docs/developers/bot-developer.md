# Bot Developer Guide

As a Bot Developer, your role is to build and maintain the single-role micro-bots that provide capabilities to the AEGIS platform. All bots strictly adhere to the HATHOR operating model.

## 1. Bot Taxonomy & Roles

Every bot belongs to exactly one family and serves a single purpose.
* **Orchestration:** (Platform-owned) Proctor-Bot, Process-Bot, Operator-Bot.
* **Hierarchy:** Procedure-Bot, Strategy-Bot, Playbook-Bot, Runbook-Bot, Workflow-Bot, Checklist-Bot (these share a common Go chassis).
* **Observation:** Observation-Bot and its children (task, benchmark, success-rate, retry, token).

*Note: You will typically be building or extending specific capability worker bots that interact with the Hierarchy or extend the CLI's domain functionality.*

## 2. The Seven-Block Anatomy

Every bot you build MUST carry the following seven architectural blocks:
1. **Identity:** A unique UUID and capability registration.
2. **Manifest (v1):** A canonical JSON manifest defining capabilities, `args_schema`, `output_schema` (using JSON Schema 2020-12), and a detached signature verifiable offline.
3. **Contract:** Implementation of the standard command set (`health`, `status`, `version`, `manifest`, `contract`, `config`, `selftest`, `knowledge`, `report`).
4. **Executor:** The core business logic, conforming strictly to the AEGIS exit-code boundary (0, 1, or 2 where 2=degraded).
5. **Knowledge Interface:** Standardized access to read/write Knowledge Plane microbursts.
6. **Connection Interface:** Brokered interactions for external effects (MUST go through Operator-Bot).
7. **Telemetry Surface:** Standardized JSONL output to the local spool.

## 3. Implementation Rules

* **Statelessness (v1):** Bots must be stateless between invocations. Do not store state in memory or local disk across runs. Use the authoritative run ledger and Knowledge Plane.
* **Zero Secrets:** Never bake credentials into your bot, and never request them directly via provider SDKs. External API calls must be brokered by the Operator-Bot.
* **Exit-Code Contract:**
  Your bot executable must return `0` (Success), `1` (Runtime/Internal error), or `2` (Degraded). The AEGIS CLI maps this to the broader CLI exit-code contract and structured JSON error envelopes.
* **Telemetry:** Emit telemetry as JSONL to `stderr` (or a designated descriptor) using the Event Envelope v1 (`event_id`, `schema_version`, `event`, `emitter`, `run`, `severity`, `payload`). It must never block the primary execution.
* **Bounded Retry:** Transient failures must retry ≤ 5 times with backoff; retries are recorded by retry-Bot. Exhaustion produces a failure report.

## 4. Containerization (Class C)

Your worker bots will be packaged as **Class C Containers**:
* **Stateless & Disposable:** No durable local state.
* **Zero secrets:** Any secrets needed must be provided at runtime via Operator-Bot brokering.
* **Endpoints:** Must expose `/version` and `/health` endpoints.
* **Pre-requisite:** Must pass all build-time Micro-Linters before the image is built.
