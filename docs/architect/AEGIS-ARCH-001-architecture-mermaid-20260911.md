---
id: AEGIS-ARCH-001
title: AEGIS — Architecture & Mermaid Reference
summary: Diagrams are Mermaid so they render in Warp, GitHub, and most Markdown surfaces. Every diagram carries a legend and points back to the requirement(s) it illustrates.
doc_type: ARCH
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
# AEGIS — Architecture & Mermaid Reference

- **Document ID:** AEGIS-ARCH-001
- **Status:** DRAFT v0 — visual companion to AEGIS-REQ-CORE-001
- **Date:** 2026-09-11
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Companion to:** `AEGIS-REQ-CORE-001-initial-requirements-20260911.md`, plan `AEGIS-PLAN-001` (`aegis-plan-001-platform-roadmap-20260913.md`)
- **Amended by (2026-09-13):** AEGIS-ADR-002/RP-009 (Orchestration Gateway — new §20; §15 grows to fifteen gates); AEGIS-ADR-003 (exit-code boundaries; Epic gate exit); AEGIS-ADR-004 (spool residency, environment naming); AEGIS-RP-007 (validation fabric — new §19); AEGIS-CANON-001 (canonical registries)
- **Purpose:** Provide a single visual reference for the AEGIS core platform — planes, bot families, container taxonomy, request flow, hierarchy chain resolution, knowledge and ticketing lifecycles, universal project layout, validation fabric, orchestration gateway, and deployment topology.

Diagrams are Mermaid so they render in Warp, GitHub, and most Markdown surfaces. Every diagram carries a legend and points back to the requirement(s) it illustrates.

---

## 1. Reading guide

| Diagram | Illustrates | Primary requirements |
|---|---|---|
| §2 System context | Actors, planes, tower | PLAT-001..003 |
| §3 Three-plane model | Registry / Knowledge / Ticketing over one CLI | PLAT-003 |
| §4 Bot families | Orchestration / Hierarchy / Observation rosters | BOT-002..006 |
| §5 Request-class routing | CLI/Proctor dispatch with optional Process, Hierarchy, Operator, and asynchronous Tower branches | BOT-003, RUN-001, RP-010 |
| §6 Hierarchy chain | Fan-out resolution across six tiers | HIE-001..006 |
| §7 Container taxonomy | Class A/B/C/D + broker symmetry | CNT-001..008 |
| §8 Universal Project Layout | `.aegis/` shape + AGENTS.md chain | UPL-001..005 |
| §9 Manifest handshake | HELLO / OFFER / BIND / VERIFY (+ fast path) | MAN-004 |
| §10 Registry states | MBI / TBR + verification states | REG-001..005 |
| §11 Telemetry spool-and-drain | Emit → spool → drain → children → Tower | TEL-001..007 |
| §12 Knowledge lifecycle | Draft → Verified → Disputed → Archived; tiered search | KNO-001..012 |
| §13 Ticketing plane | Contract, adapters, backup, reconciliation | TKT-001..013 |
| §14 Container lifecycle | Repo → lint → build → run → observe → DVO promote | CNT-001..007 |
| §15 Governance gates | The fifteen mechanical refusal points (registry: CANON-001 §2) | §14 gates |
| §16 Deployment topology | Local / dev / EKS / Tower | CNT-007, SEC-004 |
| §19 Validation fabric | Four immune altitudes (RP-007) | AEG-VAL-001..015 |
| §20 Orchestration Gateway | Events trigger · conductor decides · gateway enforces (RP-009) | AEG-GW-001..015 |

---

## 2. System context

```mermaid
flowchart LR
  H["Human operator<br/>(dev · DVO · curator)"] --> CLI["AEGIS CLI<br/><b>single control plane</b>"]
  AI["AI agent<br/>(any harness)"] --> CLI
  CLI --> Orch["Orchestration bots<br/>Proctor · Process · Operator"]
  Orch --> Hier["Hierarchy bots<br/>Procedure→Checklist"]
  Orch --> Obs["Observation bots<br/>task · benchmark · success-rate · retry · token"]
  Orch --> KP[("Knowledge Plane")]
  Orch --> TP[("Ticketing Plane")]
  Orch --> RP[("Registry Plane")]
  Obs --> Tower["Control Tower<br/>(authority · audit · rollup)"]
  KP -. reads/writes .- Tower
  TP -. reconciles .- Tower
  RP -. TBR authority .- Tower
  Orch --> Ext["External systems<br/>Jira · ADO · GitHub · Teams · Slack · MCPs"]
  Ext -. broker-only .- Orch
```

*Legend.* Solid arrows = active call path. Dotted = authority relationship. Everything crossing the boundary between actors and bots crosses the CLI.

---

## 3. Three-plane authority model (one control plane)

```mermaid
flowchart TB
  subgraph Control["Single Control Plane"]
    CLI[["AEGIS CLI"]]
  end
  CLI --> RP["Registry Plane<br/><i>which bots may run</i><br/>authority = TBR (Tower)"]
  CLI --> KP["Knowledge Plane<br/><i>what we know</i><br/>authority = verified records"]
  CLI --> TP["Ticketing Plane<br/><i>what work exists</i><br/>authority = ticket in provider"]
  RP -. bounded offline TTL .- Deg1["degraded: verified-local"]
  KP -. bounded offline TTL .- Deg2["degraded: draft-only reads on explicit opt-in"]
  TP -. bounded offline TTL .- Deg3["degraded: buffered writes to Backup TS"]
```

Every plane is authoritative over one domain, reached through the one CLI, and gracefully degradable within a bounded TTL. Past TTL, authority-originating actions refuse. [PLAT-003, PLAT-007]

---

## 4. Bot families

```mermaid
flowchart TB
  subgraph Orch["Orchestration family"]
    Proctor["Proctor-Bot<br/>contract validation · routing · gates"]
    Process["Process-Bot<br/>hierarchy resolution · run lifecycle"]
    Operator["Operator-Bot<br/><b>exclusive</b> external-connection broker"]
  end
  subgraph Hier["Information Hierarchy family (six identities, one chassis)"]
    PB["Procedure-Bot"] --> SB["Strategy-Bot"]
    SB --> PLB["Playbook-Bot"]
    PLB --> RB["Runbook-Bot"]
    RB --> WB["Workflow-Bot"]
    WB --> CB["Checklist-Bot"]
  end
  subgraph Obs["Observation family (passive)"]
    OB["Observation-Bot"] --> TB["task-Bot"]
    OB --> BB["benchmark-Bot"]
    OB --> SRB["success-rate-Bot"]
    OB --> RRB["retry-Bot"]
    OB --> TKB["token-Bot"]
  end
  Tower[["Control Tower<br/>authority · audit · rollup<br/><b>not a bot</b>"]]
  Orch -. reports .-> Tower
  Hier -. telemetry .-> Tower
  Obs -. rollups .-> Tower
```

Only Operator-Bot holds connection-pool access; only Proctor-Bot performs routing/gating; Process-Bot walks the hierarchy. Observation bots are strictly read-only. [BOT-002..006, HIE-001..003]

---

## 5. Request-class routing (not one universal chain)

```mermaid
sequenceDiagram
  autonumber
  participant Caller as Human / Agent / Bot
  participant CLI as AEGIS CLI
  participant Proctor as Proctor-Bot
  participant Process as Process-Bot
  participant Hier as Hierarchy Bot(s)
  participant Operator as Operator-Bot
  participant Ext as External system
  participant Spool as Local telemetry spool
  participant Obs as Observation-Bot
  participant Tower as Control Tower
  Caller->>CLI: intent + args (capability@major)
  CLI->>Proctor: HELLO (contract range)
  Proctor->>Proctor: verify manifest + provenance<br/>evaluate gates
  Proctor-->>CLI: OFFER (bot, digest, contract v)
  Caller->>CLI: BIND · dispatch
  alt conducted run
    CLI->>Process: dispatch under binding
    opt hierarchy resolution required
      Process->>Hier: resolve hierarchy chain (fan-out)
      Hier-->>Process: chain assembled
    end
    opt third-party effect required
      Process->>Operator: request brokered session/call
      Operator->>Ext: Class-1 proxy by default
      Ext-->>Operator: result + provider receipt
      Operator-->>Process: canonical result
    end
    Process-->>CLI: bot result + run-ledger references
  else direct bot capability
    CLI->>Proctor: dispatch admitted capability
    Proctor-->>CLI: bot result
  end
  CLI->>Spool: append telemetry
  CLI-->>Caller: stdout=data / stderr=telemetry
  Obs->>Spool: drain by cursor
  Obs->>Tower: batched rollup (async, at-least-once)
  opt tower authority command / reconciliation
    Caller->>CLI: aegis tower ...
    CLI->>Tower: authenticated direct request
    Tower-->>CLI: registry/distribution/audit result
    CLI-->>Caller: bounded response
  end
```

Bot dispatch always enters through CLI/Proctor. Process is present for conducted runs, Hierarchy only when chain work is needed, Operator only for third-party effects, and Tower calls are direct authenticated platform-authority operations rather than an Operator-brokered or universal terminal hop. Every refusal uses the structured error envelope; degradation follows command-specific CLI exit policy. [RUN-001, RP-010 §2, ADR-003 §2.3]

---

## 6. Hierarchy chain resolution (fan-out, not sequential)

```mermaid
flowchart LR
  Intent[["intent: hierarchy.resolve.runbook@1"]] --> Proc["Process-Bot"]
  subgraph W1["Wave 1 — root + direction"]
    P["Procedure-Bot"]
    S["Strategy-Bot"]
  end
  subgraph W2["Wave 2 — method"]
    PL["Playbook-Bot"]
    R["Runbook-Bot"]
  end
  subgraph W3["Wave 3 — execution + ledger"]
    W["Workflow-Bot"]
    C["Checklist-Bot"]
  end
  Proc --> W1 --> W2 --> W3
  W3 --> Result[["chain assembled<br/>procedure/strategy/playbook/runbook/workflow/checklist"]]
```

*Wave model (normative basis for NFR-004; corrected 2026-09-13).* Chains are **pre-linked assets**: each tier record stores its child links (ADR-001 object model), so steady-state resolution is parallel fetches of linked records batched into ≤ 3 dependency waves — wave 1 fetches the procedure and its linked strategy, wave 2 the playbook and runbook, wave 3 the workflow set and checklist. Each wave is a **batched fan-out**: one CLI round trip carrying that wave's sub-requests (RP-005 §4, `AEG-HIE-007`: `hierarchy.resolve.chain@1`) — a batch-dispatch primitive owned by the Process-Bot contract. Only *dynamic selection* (an unlinked tier requiring a runtime choice) forces an extra sequential hop, and each such hop is recorded on the run. Waves collapse to a digest comparison on the fast path. Cache is keyed on the participating manifests' digests; any tier redeploy invalidates affected chains. [HIE-004..007]

---

## 7. Container taxonomy + broker symmetry

```mermaid
flowchart TB
  subgraph A["Class A — Control Plane<br/><i>only Class A terminates agent traffic</i>"]
    CLIc["CLI container"]
    Proctorc["Proctor-Bot"]
    Processc["Process-Bot"]
    Operatorc["Operator-Bot"]
    Info["InfraMCP"]
    Know["KnowMCP"]
  end
  subgraph B["Class B — Knowledge<br/><i>stateful · backup-governed</i>"]
    Vec["VectorDB"]
    Emb["Embeddings / Ollama"]
    KBAPI["KB APIs"]
  end
  subgraph C["Class C — Worker / Bot-Host<br/><i>stateless · disposable · zero secrets</i>"]
    Hier1["Procedure-Bot"]
    Hier2["Strategy-Bot"]
    Hier3["Playbook-Bot"]
    Hier4["Runbook-Bot"]
    Hier5["Workflow-Bot"]
    Hier6["Checklist-Bot"]
  end
  subgraph D["Class D — Observation<br/><i>sole holder of telemetry backend creds</i>"]
    Col["OTel Collector"]
    Obs["Observation-Bot"]
  end
  Operatorc <-. brokered sessions .-> C
  Col <-. brokered egress .-> C
  Col --> Backend["OpenObserve / OTel backend"]
  Operatorc --> Ext["External systems"]
```

Two altitudes of the same principle: **N workers, zero secrets, one broker** — Operator-Bot brokers external connections, the Collector brokers telemetry egress. [CNT-001..008]

---

## 8. Universal Project Layout

```mermaid
flowchart TB
  Root(["<project>/"])
  Root --> Aegis[".aegis/<br/><i>hidden AEGIS metadata</i>"]
  Aegis --> Man["manifests/"]
  Aegis --> Rules["rules/"]
  Aegis --> State["state/"]
  State --> Runs["runs/"]
  State --> CL["checklists/"]
  State --> Spool["spool/  (telemetry)"]
  Aegis --> Know["knowledge/  (project tier)"]
  Root --> Cfg["cfg/"]
  Root --> Src["src/"]
  Root --> Lib["lib/"]
  Root --> Bin["bin/  (thin façade only)"]
  Root --> Dist["dist/"]
  Root --> Test["test/"]
  Root --> Docs["docs/"]
  Root --> Docker[".docker/"]
  Root --> Agents["AGENTS.md  (root scope)"]
  Root --> MK["Makefile  (optional façade)"]
  Docs --> DocA["docs/api/AGENTS.md"]
  Src --> SrcA["src/AGENTS.md"]
```

AGENTS.md resolves nearest-first as the CLI walks up from the working directory. `aegis repo validate` enforces the shape; `aegis repo init --from-infraos` converts legacy `.infraOS/` trees. [UPL-001..005]

---

## 9. Manifest handshake (HELLO / OFFER / BIND / VERIFY)

```mermaid
sequenceDiagram
  autonumber
  participant Caller
  participant CLI
  participant Proctor
  participant Registry as MBI (local index)
  participant Bot
  Caller->>CLI: HELLO {contract_range, intent=capability@major}
  CLI->>Proctor: resolve capability
  Proctor->>Registry: lookup capability → bot_uuid, manifest_digest, state
  alt state=quarantined OR expired
    Proctor-->>CLI: refusal PROVENANCE_UNVERIFIED (exit 4)
    CLI-->>Caller: structured error envelope
  else routable
    Proctor->>Proctor: version negotiation (major=match; pick highest overlap)
    Proctor-->>CLI: OFFER {bot, bot_uuid, manifest_digest, contract_version, args_schema_ref}
    CLI-->>Caller: OFFER (or cached digest match — fast path)
    Caller->>CLI: BIND (accept offer)
    CLI-->>Caller: binding_id + TTL
    opt VERIFY (optional, side-effect-free)
      Caller->>CLI: contract validate <payload>
      CLI->>Bot: args_schema check
      Bot-->>Caller: pass/fail (no side effects)
    end
    Caller->>CLI: dispatch under binding
    CLI->>Bot: execute
  end
```

Fast-path steady state is one digest comparison. Any manifest digest change invalidates the binding (`MANIFEST_DIGEST_STALE`). [MAN-004, RP-001 §3]

---

## 10. Registry (MBI + TBR) with verification states

```mermaid
stateDiagram-v2
  [*] --> InstallVerify: bot install/update
  InstallVerify --> verifiedLocal: signature ok · TBR pending/unreachable
  InstallVerify --> quarantined: signature invalid · structural violation
  verifiedLocal --> verifiedTower: Tower ack (reconciliation)
  verifiedTower --> verifiedLocal: Tower unreachable at reconcile (within TTL)
  verifiedLocal --> quarantined: trust TTL expired
  verifiedTower --> quarantined: CRL revocation
  quarantined --> verifiedLocal: rebuild + re-verify (operator action)
  quarantined --> [*]
  note right of verifiedTower: routable normally
  note right of verifiedLocal: routable within trust TTL<br/>runs flagged degraded (exit 2)
  note right of quarantined: NOT routable · Proctor refuses
```

Runtime resolution is always MBI-only; TBR governs registration, keys, revocation. [REG-001..005]

---

## 11. Telemetry: spool-and-drain

```mermaid
flowchart LR
  Bot["Bot execution<br/>(stateless, short-lived)"] --> CLIT["CLI telemetry primitive"]
  CLIT -->|append JSONL| Spool[("Local append-only spool<br/>.aegis/state/spool/")]
  Spool -->|tail + cursor| Drain["Observation-Bot<br/>(resident)"]
  Drain --> Task["task-Bot"]
  Drain --> Bench["benchmark-Bot"]
  Drain --> SR["success-rate-Bot"]
  Drain --> Retry["retry-Bot"]
  Drain --> Tok["token-Bot"]
  Drain -->|batched rollup| Tower["Control Tower<br/>ingest"]
  Spool -. bounded quota .- Ladder["warn 80% · shed debug 90% · hard stop 100%"]
  Drain -. at-least-once<br/>dedupe on event_id (UUIDv7) .- Task
```

Emit path is a local file append — no network I/O, no Observation-Bot dependency, never fatal. [TEL-001..007]

---

## 12. Knowledge lifecycle & tiered search

### 12.1 Tiered retrieval order

```mermaid
flowchart LR
  Q["Query"] --> P["Project tier<br/>.aegis/knowledge/ + project MCP"]
  P -->|hit| Ans1["Result"]
  P -->|miss| M["Machine tier<br/>CLI knowledge + local vector"]
  M -->|hit| Ans2["Result"]
  M -->|miss| O["Organization tier<br/>org MCP"]
  O -->|hit| Ans3["Result"]
  O -->|miss| Pu["Public tier<br/>external reference"]
  Pu -->|hit or none| Ans4["Result or<br/>NO_CONFIDENT_MATCH"]
```

Retrieval honesty: expired TTL is flagged per record, never silently served. [KNO-001, KNO-005]

### 12.2 Draft → Verified lifecycle

```mermaid
stateDiagram-v2
  [*] --> draft: write (microburst)
  draft --> verified: human review + mechanical gates pass
  draft --> archived: expire · reject · 2× SLA
  verified --> stale: TTL lapse
  stale --> verified: re-review passes
  stale --> draft: content changed, needs review
  stale --> archived: no re-review
  verified --> disputed: operator/bot dispute + evidence
  disputed --> verified: re-review passes
  disputed --> draft: re-review needs re-work
  disputed --> archived: rejected
  verified --> archived: superseded (linkage retained)
  archived --> [*]
  note right of verified: default retrievable
  note right of draft: retrievable only via --include-drafts
  note right of disputed: excluded from default retrieval
```

No auto-promotion, ever. [KNO-007..012]

---

## 13. Ticketing Plane — canonical contract, adapters, reconciliation

### 13.1 Overview

```mermaid
flowchart LR
  Agent["Agent / worker bot"] --> CLI["AEGIS CLI"]
  H["Human"] --> CLI
  CLI --> Op["Operator-Bot<br/>(exclusive broker)"]
  Op --> AJ["Adapter: Jira"] --> J[("Jira")]
  Op --> AA["Adapter: Azure DevOps"] --> A[("Azure DevOps Boards")]
  Op --> AG["Adapter: GitHub"] --> G[("GitHub Issues/Projects")]
  Op --> AB["Adapter: Backup TS"] --> B[("Backup Ticketing System")]
  CLI -. canonical Ticket Contract v1 only .- Agent
  CLI -. canonical Ticket Contract v1 only .- H
```

### 13.2 Reconciliation

```mermaid
flowchart LR
  Write["ticket create/update"] --> Reach{"provider reachable?"}
  Reach -->|no| Buf["write Backup TS<br/>sync.state=buffered<br/>run flagged degraded (exit 2)"]
  Reach -->|yes| Auth["write authoritative provider<br/>sync.state=authoritative"]
  Buf --> Recon["on reconnect: reconcile"]
  Recon --> Cmp{"digest conflict?"}
  Cmp -->|no| Push["create/update upstream<br/>back-fill provider.ref<br/>sync.state=reconciled"]
  Cmp -->|yes| Res["conflict resolution:<br/>provider wins as authority"]
  Res --> Rep["replay buffered delta as update"]
  Res --> Ref["OR structured refusal<br/>TICKET_RECONCILE_CONFLICT"]
```

Buffered-beyond-TTL surfaces as degraded and cannot originate deploy authority. [TKT-008..011]

### 13.3 Work + hierarchy + telemetry linkage

```mermaid
flowchart LR
  Ticket["Ticket (Jira/ADO/GH/Backup)"] -->|authorizes| Runbook["Runbook run"]
  Runbook --> Chain["Hierarchy chain"]
  Runbook --> Tel["Telemetry events"]
  Runbook --> PR["PR / branch"]
  PR --> Ticket
  Tel --> Tower["Control Tower"]
  Chain --> Tower
  Ticket -. via canonical_id .- Tower
```

Every run reports `ticket_ref` alongside chain + telemetry — the Tower can enumerate every artifact for a given ticket. [TKT-012]

---

## 14. Container lifecycle

```mermaid
flowchart LR
  Repo["Repo + micro-bots"] --> Lint["Micro-linters<br/>(build-time immune system)"]
  Lint -->|pass| Build["Image build<br/>+ CVS metadata + OCI labels"]
  Build --> Reg["Container registry (ECR)"]
  Reg --> Run["AEGIS Container running<br/>(bot + CLI + contracts)"]
  Run --> Ver["/version + /health<br/>content negotiation"]
  Run --> Col["OTel Collector (Class D)"]
  Col --> Backend["OpenObserve / OTel backend"]
  Run -. reports .-> Tower["Control Tower"]
  Col -. reports .-> Tower
  DVO["DVO deploy ticket<br/>(human-executed)"] -->|only lawful promotion| Run
  Lint -. refusal on any violation .-> Repo
```

**Nothing un-linted gets containerized.** The DVO ticket is the sole lawful arrow into promotion. [CNT-001..007, TKT-011]

---

## 15. Governance gates — the fifteen refusal points

> **Registry note (2026-09-13):** the canonical registry is **AEGIS-CANON-001 §2** (G01–G15): the ten below plus the four validation gates (RP-007 §5.2) and the Sequence/Barrier Gate (RP-009 §4.2). Canonical dispatch-path order is **Provenance → Contract → Sequence/Barrier → domain gates** — the traversal drawn below is illustrative, not an ordering contract.

```mermaid
flowchart TB
  In(["Caller intent"]) --> G1["No-Ticket Gate<br/><i>exit 7 → 2</i>"]
  G1 -->|pass| G2["Epic-Linkage Gate<br/><i>exit 2</i>"]
  G2 -->|pass| G3["PR-Ticket Bind Gate<br/><i>exit 2</i>"]
  G3 -->|pass| G4["Estimation Gate<br/><i>exit 2</i>"]
  G4 -->|pass| G5["Provenance Gate<br/><i>exit 4</i>"]
  G5 -->|pass| G6["Contract Gate<br/><i>exit 2</i>"]
  G6 -->|pass| G7["Development-Only Gate<br/><i>exit 4</i>"]
  G7 -->|pass| G8["Deploy-Ticket Gate<br/><i>exit 4 (only on promote)</i>"]
  G8 -->|pass| G9["Micro-Linter Gate<br/><i>exit 2 (build time only)</i>"]
  G9 -->|pass| G10["Knowledge Promotion Gate<br/><i>exit 2 (on knowledge promote)</i>"]
  G10 -->|pass| Exec[["Dispatch to bot"]]
  G1 & G2 & G3 & G4 & G5 & G6 & G7 & G8 & G9 & G10 -->|refuse| Refuse[["Structured error envelope<br/>{code, message, remediation, provenance, ttl}"]]
```

Not every command traverses every gate; the gate applies only when its precondition is present (e.g. Deploy-Ticket Gate only on promotion). Gates are *reactive guards*; the guarantee that every mandatory unit actually runs is owned by the Orchestration Gateway's conductor (§20, ADR-002). [Requirements §14, CANON-001 §2]

---

## 16. Deployment topology

```mermaid
flowchart LR
  Dev["Developer machine<br/>Docker Compose<br/>MBI · spool · project .aegis/"]
  Dev -->|push branch + open PR| GitHub[("GitHub / GitLab")]
  Dev -->|write draft ticket via CLI| Op["Operator-Bot"]
  Op --> Providers[("Jira · ADO · GitHub · Backup TS")]
  Dev -. telemetry rollup .- TowerIngest["Control Tower ingestion<br/>(collector + backends)"]
  DevopsHuman["DVO human operator"] -->|authorizes deploy ticket| Providers
  Providers -->|DVO ticket 'Done' triggers| EKS["EKS cluster<br/>Class A/B/C/D<br/>IRSA · secret mounts"]
  EKS -. telemetry rollup .- TowerIngest
  EKS -. MBI + verified-tower .- TowerAuth["Control Tower authority<br/>TBR · keys · CRL · curators"]
  Dev -. verified-local within TTL · degraded reports .- TowerAuth
```

Local + development are agent-writable; testing/staging/production run in EKS and are DVO-only. `verified-local` bots continue during a Tower outage within trust TTL, honestly reporting the degradation. [CNT-007, SEC-004, PLAT-007]

---

## 17. End-to-end run trace (worked example: DVO deploy request)

```mermaid
sequenceDiagram
  autonumber
  participant Dev as Developer / Agent
  participant CLI as aegis CLI
  participant Proctor as Proctor-Bot
  participant Work as Work (Ticketing)
  participant Process as Process-Bot
  participant Hier as Hierarchy chain
  participant Op as Operator-Bot
  participant Ext as Jira (DVO project) + Teams
  participant Obs as Observation-Bot
  participant Tower as Control Tower
  Dev->>CLI: aegis process runbook run dvo-deploy-ticket --context pr_url=… --dry-run
  CLI->>Proctor: gates (No-Ticket, Provenance, Dev-Only, Contract)
  Proctor-->>CLI: OK (dry-run bypasses live mutation)
  CLI->>Process: dispatch
  Process->>Hier: resolve chain (Playbook dvo-deploy-handoff → Runbook dvo-deploy-ticket → Workflow devops/dvo-deploy-request → Checklist)
  Hier-->>Process: chain assembled
  Process-->>CLI: dry_run=true JSON plan (exit 0)
  Note over Dev,CLI: developer reviews plan, drops --dry-run
  Dev->>CLI: aegis process runbook run dvo-deploy-ticket … --yes
  CLI->>Proctor: gates + Estimation + Epic + PR-Ticket-Bind
  Proctor-->>CLI: OK
  CLI->>Process: dispatch live
  Process->>Op: Jira create + Teams announce (brokered, idempotency-keyed)
  Op->>Ext: side effects
  Ext-->>Op: results
  Op-->>Process: results
  Process->>CLI: checklist updates + result envelope (exit 0)
  Process->>Obs: telemetry (task.end · tokens · retries · work.ticket.status_change)
  Obs->>Tower: rollup (batched)
  Note over Tower: Deploy-Ticket Gate closed — human DVO operator now executes; agent never deploys.
```

This is the concrete "Ticketing Plane → Container promotion" arrow enforced by AEGIS: builder + verifier (agent), operator (human). [TKT-011, CNT-007]

---

## 18. Cross-cutting invariants (one-page summary)

| Invariant | Enforced by | Requirement |
|---|---|---|
| Only the CLI terminates agent traffic | Container Class A design; static analysis | PLAT-001, CNT-001 |
| Refuse-never-guess on any contract mismatch | Proctor gates + manifest validation | PLAT-004, MAN-002 |
| Provenance verified before dispatch | Proctor + MBI verification states | SEC-003, REG-003 |
| Zero baked secrets | Operator-Bot broker + Collector broker | SEC-002, CNT-004, CNT-008 |
| No auto-promotion (knowledge or work) | Knowledge Promotion Gate + Deploy-Ticket Gate | KNO-009, TKT-011 |
| Bounded offline trust | Trust TTL on MBI, spool, backup TS | PLAT-007, REG-004, TEL-005, TKT-009 |
| Telemetry never fatal | Spool-and-drain never blocks emitters | TEL-002 |
| Hierarchy chain traceable end-to-end | `hierarchy_chain` on every event, ticket link | TEL-007, TKT-012 |
| Universal project shape | `.aegis/` + AGENTS.md chain + `aegis repo validate` | UPL-001..004 |
| Nothing un-linted gets containerized | Micro-Linter Gate at build time | CNT-006 |

---

## 19. Validation fabric — four immune altitudes (RP-007)

```mermaid
flowchart LR
  A1["1 · Build-time<br/>micro-linters<br/><i>refuse image entry</i>"] --> A2["2 · Change-time<br/>micro-linters + validator bots<br/><i>refuse changes · assumptions · claims</i>"]
  A2 --> A3["3 · Dispatch-time<br/>Proctor gates G01–G09<br/><i>refuse unlawful dispatch</i>"]
  A3 --> A4["4 · Runtime<br/>Observation family<br/><i>record only — never refuse</i>"]
```

Build-time and change-time share the same micro-linter binaries; only the trigger scope differs. Change-time units: micro-linters (pure, exit 0|2), validator bots (`val-*`, Proctor-owned), suites, and the run-scoped assumption ledger. Enforcement fails closed; observation fails open. [AEG-VAL-001..015, RP-007 §1–§5]

---

## 20. Orchestration Gateway — three layers (RP-009, per ADR-002)

```mermaid
flowchart LR
  E["EVENTS trigger<br/>fs.write · git.stage · claim.step.done<br/>ci.* · run.finalize"] -->|append to events.jsonl| CD["CONDUCTOR decides<br/>Process-Bot saga state machine<br/><i>state = fold of run log</i>"]
  CD -->|admissible?| GW["GATEWAY enforces<br/>Proctor · Sequence/Barrier Gate (G03)<br/>+ existing gates"]
  GW -->|admit / refuse| CD
  CD --> WK["Linters · validators · worker bots<br/><i>auto-invoked on events</i>"]
  WK -->|verdicts + evidence| CD
  CD -->|run.finalize| RC["val-completeness-Bot<br/>required-set vs executed-set"]
  RC -->|gap| REF[["REFUSE run.complete<br/>COMPLETENESS_GAP"]]
  RC -->|clean| FIN(["run.finalized ✓"])
```

**Events trigger, the conductor decides, the gateway enforces.** The plan is data (a graph over Runbook/Workflow/Checklist assets); the agent fills step content and *requests* completion—only Process-Bot advances run state. Within RP-013's cooperative-but-fallible trust model, finalize checks the graph-derived required set against the authoritative run/evidence ledgers with telemetry correlation; adversarial-local integrity requires the phased hash-chain/Tower hardening. No bus, no new plane, no new top-level domain. [AEG-GW-001..015, ADR-002, TS-002, AEG-THR-001]

---

*Draft v0 — visual companion to AEGIS-REQ-CORE-001 (amended 2026-09-13 per ADR-002/003/004, RP-007/009, CANON-001). Diagrams are non-normative; the numbered requirements are authoritative. Amend as designs evolve.*
