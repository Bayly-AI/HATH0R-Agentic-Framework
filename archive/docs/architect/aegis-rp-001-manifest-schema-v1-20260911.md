# AEGIS Research Paper 001 — Bot Manifest Schema v1 & Contract-Negotiation Handshake

- **Document ID:** AEGIS-RP-001
- **Status:** DRAFT (research output — pending operator review)
- **Date:** 2026-09-11
- **Parent:** AEGIS-REQ-BOT-001 (§10 Q1)
- **Amended by:** AEGIS-RP-013 §6 (2026-09-13, operator-approved): canonicalization = RFC 8785 (JCS); signatures = Ed25519 in DSSE envelopes; key rotation/revocation/bootstrap via TUF (resolves §6 Q1)
- **Amended by:** AEGIS-RP-014 (2026-09-13, operator-approved): manifest schema **1.1.0** — additive, mandatory `governance` triad; `runtime.requires_capabilities`/`config_schema`/`executor_kind`; `AEG-MAN-007` gains the bot-governance refusal classes (no transition profile)
- **Author:** Oz (Agent), commissioned by Raymond Bayly

---

## 1. Problem Statement

AEG-BOT-ANA-002 mandates a machine-readable manifest for every bot, and AEG-BOT-ANA-003 mandates a versioned communication contract. Neither the exact JSON fields nor the negotiation handshake were defined. This paper specifies both.

Design constraints inherited from AEGIS-REQ-BOT-001:
- CLI is the sole control plane (TAX-006); the manifest is the CLI's routing and enforcement input.
- Code-agnostic executors (ANA-004): the manifest is the only conformance surface.
- Refuse-never-guess on contract mismatch (ANA-003).
- No credentials in manifests (ANA-002).

## 2. Manifest Schema v1

The manifest is a single JSON document, UTF-8, canonicalized per **RFC 8785 (JSON Canonicalization Scheme)** before digesting *(amended 2026-09-13 per RP-013 §6; previously ad hoc "sorted keys, no insignificant whitespace")*. Its **sha256 digest** is the bot's registration fingerprint (consumed by the registry — see AEGIS-RP-002 — and by the handshake below).

### 2.1 Top-level structure

```json
{
  "manifest_version": "1.1.0",
  "identity": { ... },
  "contract": { ... },
  "commands": [ ... ],
  "capabilities": [ ... ],
  "knowledge": { ... },
  "connections": [ ... ],
  "telemetry": { ... },
  "runtime": { ... },
  "governance": { ... }
}
```

Manifest v1.1.0 is additive over v1.0.0 (`AEGIS-RP-014`): the `governance` block (§2.10) is **mandatory**, and `runtime` gains `requires_capabilities`, `config_schema`, and `executor_kind` (§2.9). A 1.0.0 manifest without `governance` is refused at registration — no transition profile.

### 2.2 `identity` (all fields required)

```json
{
  "uuid": "8f2c9e1a-4b7d-4f3a-9c2e-1a7b3d5f8e0c",
  "name": "runbook-Bot",
  "family": "hierarchy",
  "tier": "runbook",
  "version": "1.4.2",
  "owner": "aegis-core",
  "provenance": {
    "builder": "aegis-forge",
    "source_repo": "aegis/hierarchy-chassis",
    "source_commit": "a1b2c3d",
    "built_at": "2026-09-11T10:00:00Z"
  }
}
```

- `family` ∈ `orchestration | hierarchy | observation` (TAX-002).
- `tier` required for hierarchy family (`procedure|strategy|playbook|runbook|workflow|checklist`), `null` otherwise.
- The signature is **not a field in the signed manifest payload**. A sibling `manifest.dsse.json` carries the Ed25519 **DSSE envelope** whose payload is the JCS-canonical `manifest.json` bytes *(amended 2026-09-13 per RP-013 §6)*. This removes circular representation and remains verifiable offline against TUF-distributed public keys (see AEGIS-RP-002).
- **Coverage limit:** schema 1.1.0 binds the manifest and the governance files referenced by digest, but it declares no executor/image/artifact digest. The envelope therefore MUST NOT be described as covering executor bytes until the executable-artifact binding in `PENDING-EDITS.md` R10 is frozen.

### 2.3 `contract`

```json
{
  "version": "1.2.0",
  "min_compatible": "1.0.0",
  "encoding": "json",
  "error_envelope_version": "1.0.0"
}
```

- Semver semantics: **major must match** between caller and bot; minor/patch negotiate downward (see §3).
- `error_envelope_version` pins the `{code, message, remediation, provenance, ttl}` shape (CMD-003).

### 2.4 `commands[]` (one entry per command; undeclared = refused, CMD-004)

```json
{
  "name": "status",
  "summary": "Grouped deep checks",
  "args_schema": { "$schema": "https://json-schema.org/draft/2020-12/schema", "...": "..." },
  "output_schema": { "...": "..." },
  "exit_codes": [0, 1, 2],
  "side_effects": "none",
  "requires_connections": [],
  "timeout_ms": 5000,
  "dry_run": true
}
```

- `side_effects` ∈ `none | local | knowledge | external`. Proctor uses this to decide whether Operator-Bot brokering and hierarchy attachment are required before dispatch.
- `args_schema` / `output_schema` are embedded JSON Schema (2020-12). The CLI validates both directions; a bot returning schema-invalid output is a contract violation (exit 1, envelope code `CONTRACT_OUTPUT_INVALID`).
- `exit_codes` MUST be a subset of `[0,1,2]` (CMD-002).

### 2.5 `capabilities[]`

Flat, versioned capability strings used for routing and capability negotiation:

```json
[ "hierarchy.resolve.runbook@1", "knowledge.microburst.write@1" ]
```

Capabilities are the routing vocabulary: Proctor matches request intents to capabilities, never to bot names, so bots can be replaced without breaking callers.

### 2.6 `knowledge`

```json
{
  "reads": ["project", "machine", "organization"],
  "writes": ["project"],
  "microburst_only": true
}
```

- `microburst_only` MUST be `true` in v1 (KNO-003). Field exists so a future operator-authorized bulk tool is representable without a schema break.

### 2.7 `connections[]` (names only, never credentials)

```json
[ { "name": "jira", "purpose": "ticket sync", "required": false, "degraded_fallback": "queue-local" } ]
```

### 2.8 `telemetry`

```json
{
  "events_emitted": ["task.start", "task.end", "retry", "tokens"],
  "schema_version": "1.0.0"
}
```

Event names come from the uniform event vocabulary (AEGIS-RP-003 §4).

### 2.9 `runtime`

```json
{
  "resident": false,
  "health_budget_ms": 250,
  "stateless": true,
  "executor_kind": "mechanical",
  "requires_capabilities": [ "validation.evidence.verify@1" ],
  "config_schema": { "$schema": "https://json-schema.org/draft/2020-12/schema", "...": "..." }
}
```

- `resident: true` obligates `drain|stop` (CMD-019); the CLI enforces presence of those commands at registration time.
- `stateless` MUST be `true` in v1 (RUN-002); representable for future exceptions via ADR only.
- `executor_kind` ∈ `mechanical | agent-backed`, default `mechanical`. Agent-backed is the exception and is gated by explicit recorded authorization (ADR or a ticketed owner — RP-014 §3.3); it never changes who owns control flow.
- `requires_capabilities[]` declares collaborators by capability, never bot name; resolved late (RP-014 §3.2).
- `config_schema` is the JSON Schema (2020-12) that per-bot config is validated against (RP-014 §3.6). *(These three fields are added by RP-014, manifest 1.1.0.)*

### 2.10 `governance` (mandatory — added by RP-014, manifest 1.1.0)

```json
{
  "directive":  { "path": "DIRECTIVE.md",    "digest": "sha256:…", "version": 1, "budget_tokens": 1000 },
  "rules":      { "path": "rules.yaml",      "digest": "sha256:…", "count": 4 },
  "principles": { "path": "principles.yaml", "digest": "sha256:…", "platform_set": "aegis-principles@1" }
}
```

The governance triad (directive, rules, principles) is specified in **AEGIS-RP-014 §3**. Its three file digests are manifest fields, so the external DSSE envelope over the JCS-canonical manifest (RP-013 §6) covers the manifest and governance triad; editing any governance file changes the manifest digest (`MANIFEST_DIGEST_STALE`). Executor-byte coverage is excluded pending R10. `rules.count` equals the rule-set size; `platform_set` is `aegis-principles@1`. `governance` is **mandatory**—a manifest without it is refused (RP-014 §3.2).

## 3. Contract-Negotiation Handshake

Four phases, all mediated by the CLI. The handshake is cheap by design: for repeat callers it collapses to a digest comparison (§3.5).

### 3.1 Phase 1 — HELLO (caller → CLI)

Caller (agent or bot) sends its supported contract range and the intent (capability, not bot name):

```json
{
  "hello": {
    "caller_id": "<uuid>",
    "contract_range": { "min": "1.0.0", "max": "1.3.0" },
    "intent": "hierarchy.resolve.runbook@1"
  }
}
```

### 3.2 Phase 2 — OFFER (Proctor → caller)

Proctor resolves the capability to a bot (via the registry, AEGIS-RP-002), verifies provenance (SEC-003), and returns:

```json
{
  "offer": {
    "bot": "runbook-Bot",
    "bot_uuid": "8f2c…",
    "manifest_digest": "sha256:…",
    "contract_version": "1.2.0",
    "command": "resolve",
    "args_schema_ref": "manifest#/commands/resolve/args_schema"
  }
}
```

Version selection rule: highest version satisfying `caller.min ≤ v ≤ caller.max` AND `bot.min_compatible ≤ v ≤ bot.contract.version` AND equal major. No intersection → structured refusal `CONTRACT_NO_OVERLAP` with both ranges in the envelope (never a best-effort guess).

### 3.3 Phase 3 — BIND (caller → CLI)

Caller accepts the offer and receives a **session binding**: `{binding_id, manifest_digest, contract_version, ttl}`. All subsequent requests under this binding skip Phases 1–2. A binding is invalidated the moment the bot's manifest digest changes.

### 3.4 Phase 4 — VERIFY (optional)

`contract validate <payload>` (CMD-014) pre-flights a concrete request against `args_schema` with zero side effects. Recommended for agents before first real dispatch and after any refusal.

### 3.5 Fast path

Callers cache `{capability → binding}`. On each request the CLI compares the cached `manifest_digest` against the registry; on match, dispatch proceeds directly. This makes the steady-state overhead one digest comparison, satisfying microbot latency goals (relevant to the chain-latency concern in AEGIS-RP-005).

### 3.6 Refusal codes (handshake-specific)

- `CONTRACT_NO_OVERLAP` — no common version; envelope carries both ranges.
- `CONTRACT_MAJOR_MISMATCH` — major versions differ.
- `MANIFEST_DIGEST_STALE` — binding refers to superseded manifest; caller must re-HELLO.
- `PROVENANCE_UNVERIFIED` — signature/registry check failed (SEC-003); reported to Tower.
- `CAPABILITY_UNKNOWN` — no registered bot offers the intent.

## 4. Requirements (AEG-MAN)

### AEG-MAN-001 — Canonical manifest
Every bot ships exactly one manifest conforming to schema v1; the canonicalized sha256 digest is its registration fingerprint.
**AC:** `manifest` command output re-digests to the registered fingerprint; any mismatch fails `selftest`.

### AEG-MAN-002 — Embedded schemas
Every command declares `args_schema` and `output_schema` (JSON Schema 2020-12); the CLI validates both directions.
**AC:** Schema-invalid input never reaches the bot; schema-invalid output yields `CONTRACT_OUTPUT_INVALID`.

### AEG-MAN-003 — Capability-based routing
Callers address capabilities, not bot names; Proctor performs resolution.
**AC:** Replacing a bot with another exposing the same capability requires zero caller changes.

### AEG-MAN-004 — Version negotiation
Handshake selects the highest mutually supported contract version; equal-major required; no intersection → structured refusal.
**AC:** Negotiation is deterministic and reproducible from the two declared ranges alone.

### AEG-MAN-005 — Binding invalidation
Session bindings are invalidated on manifest digest change.
**AC:** A redeployed bot never serves a request under a stale binding; caller receives `MANIFEST_DIGEST_STALE`.

### AEG-MAN-006 — Signed provenance
Each manifest is accompanied by an external DSSE envelope verifiable offline against Tower-distributed keys; the envelope payload is exactly the JCS-canonical manifest bytes.
**AC:** Verification succeeds with no Tower connectivity, using locally cached keys within their TTL; no signature field is embedded in the signed payload.

### AEG-MAN-007 — Registration-time enforcement
The CLI refuses to register manifests that violate structural rules (resident without drain/stop, exit codes outside 0/1/2, microburst_only=false, embedded credentials) **and**, per RP-014 (manifest 1.1.0), missing/mismatched `governance` digests, a directive missing a required section or over `budget_tokens`, a rule schema/`kind` violation, a removed family-default rule, a principle-constraint violation, an invalid `config_schema`, or a malformed `requires_capabilities`/`executor_kind`.
**AC:** Each violation class has a registration test that fails closed (RP-014 `AEG-BOT-LIF-003`).

## 5. Infra Adoption Decision Log

- **Infra `cfg/mcp-servers.json`-style flat config — Reject.** No per-command schemas, no signatures, no negotiation; manifest v1 exceeds it.
- **JSON Schema 2020-12 as validation vocabulary — Adopt (industry standard).** Exceeds inventing an AEGIS-only schema language.

## 6. Open Questions

1. ~~Signature algorithm and key rotation cadence~~ **Resolved (2026-09-13):** Ed25519 in DSSE envelopes; rotation/revocation/bootstrap via TUF roles served by the Tower (RP-013 §6, RP-010 §3.2).
2. Whether OFFER should support multi-bot candidate lists for capability ties (load choice at Proctor vs caller).
3. Binding TTL default (proposed: 24h or manifest change, whichever first).

---

*Research output only. No implementation authorized.*
