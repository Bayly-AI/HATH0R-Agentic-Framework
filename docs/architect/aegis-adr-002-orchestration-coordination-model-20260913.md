---
id: HATHOR-ADR-002
title: HATHOR-ADR-002 — Orchestration Coordination Model
summary: RFC 2119 keywords apply where requirements are restated.
doc_type: ADR
diataxis: decision
audience: [architect, agent]
tags: []
version: 1.0.0
status: accepted
created: '2026-09-13'
updated: '2026-09-15'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: null, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# HATHOR-ADR-002 — Orchestration Coordination Model
## Event-Triggered Central Orchestration over Choreography (System-Native, No-Skip)

- **Document ID:** HATHOR-ADR-002
- **Status:** ACCEPTED — operator sign-off 2026-09-13 (approved with the corpus sign-off; PENDING-EDITS §1 D7)
- **Date:** 2026-09-13
- **Author:** Oz (Agent), commissioned by Raymond Bayly (BaylyAI)
- **Decision class:** Architecture Decision Record (coordination model)
- **Companion to:** HATHOR-RP-009 (Orchestration Gateway — the design that implements this decision); HATHOR-REQ-CORE-001; HATHOR-REQ-BOT-001; HATHOR-ARCH-001; HATHOR-RP-007 (CVS); HATHOR-TS-001; HATHOR-RP-003 (telemetry transport)
- **Scope rule:** decision record only. No implementation authorized by this document.

RFC 2119 keywords apply where requirements are restated.

> This ADR is the **companion analysis** referenced by HATHOR-RP-009 §2.1. RP-009 specifies *how* the Orchestration Gateway is built; this ADR records *why* the coordination model was chosen and *what alternatives were rejected*.

---

## 1. Context

### 1.1 The requirement

Bots exist to complete tasks under an orchestration. The operator requirement is absolute: **we cannot miss or skip a bot** — the full required set of bots, linters, and validators for a unit of work must execute, in order, every time — and this must be **system-native**, i.e. taken out of the direct hands of the agent.

### 1.2 The gap in the ratified corpus

AEGIS already has two of the three fabrics it needs, but not the third:

- A **detection** fabric — RP-007 Continuous Validation System (micro-linters, validator-bots, suites, claims, assumptions).
- A **guard** fabric — CORE §14, the ten mechanical gates.
- **Missing: a conductor** — a system-native owner of control flow.

Two ratified statements make the gap concrete:

- **RP-007 §6.1** makes validation the *agent's* responsibility ("Agents MUST … run `aegis validate change` … `aegis validate claim` …"). This is **voluntary compliance**.
- **ARCH-001 §15**: "the gate applies only when its precondition is present." Gates are **reactive guards** (refuse *if* reached), not a **proactive conductor** (guarantee the whole sequence runs).

Therefore an agent that reorders its work, never reaches a boundary, or forgets a step **silently skips mandatory execution**. Control-flow authority currently lives in the agent. This is the problem to be decided.

### 1.3 "Skip" is three distinct failure modes

Precision matters, because different coordination models address different subsets. A model that solves only one leaves the door open.

| Skip mode | What it looks like | What actually prevents it |
|---|---|---|
| **Omission** | A required unit never runs | Declarative required-set + a completeness reconciler |
| **Order violation** | A unit runs before its prerequisite | State-machine transitions + a dispatch gateway that consults run state |
| **False completion** | "Done" asserted without running the work | Evidence-gated completion (`val-evidence-Bot` + claim→tier) |

AEGIS has *already solved* false completion mechanically (RP-007/TS-001). This decision must additionally solve **omission** and **order violation** — and do so system-natively.

---

## 2. Decision drivers

1. **No-skip guarantee** must be *provable within the RP-013 cooperative-but-fallible trust model*, not emergent; adversarial-local integrity is detected/phased hardening.
2. **System-native** — control flow owned by the platform; the agent only fills step content.
3. **Single control plane** — no secondary control surface without ADR (`AEG-REQ-PLAT-001`).
4. **No machine-tier event bus** — already rejected in favor of spool-and-drain (`RP-003`).
5. **All bot traffic via Proctor** — bots never invoked directly (`BOT-TAX-006`).
6. **Refuse-never-guess** on the enforcement path; **never-fatal** on the observation path (`AEG-REQ-TEL-002`).
7. **Reuse over invention** — prefer existing families/discipline (Canonical Rule 4).
8. **Crash-safe & resumable** — a killed run must not lose or duplicate mandatory work.

---

## 3. Considered options

### Option A — Status quo: agent-driven work + reactive gates

The agent drives control flow and voluntarily invokes validation; gates refuse at chokepoints if reached.

- **No-skip:** ✗ Omission and order-violation both possible (agent simply doesn't reach a boundary or reorders).
- **System-native:** ✗ Authority is in the agent.
- **Verdict:** **Rejected.** This is precisely the gap in §1.2.

### Option B — Pure event-driven choreography (event bus; bots react to each other's events)

No central authority; each bot emits events, others subscribe and react. Superficially matches the operator's "event-driven gateway" instinct.

- **No-skip:** ✗ Completeness is **emergent, not provable**. No single place knows the full required set; a downed subscriber, dropped event, or unwired new step silently truncates the chain. Guaranteeing exhaustiveness requires bolting on a central reconciler — at which point choreography has been abandoned for orchestration.
- **Single control plane:** ✗ A machine-tier pub/sub bus is a *second control surface* (contra `AEG-REQ-PLAT-001`) and directly contradicts the ratified `RP-003` decision to reject an event bus at the machine tier.
- **Direct invocation:** ✗ Bots reacting to each other's events violates `BOT-TAX-006` (all bot-to-bot traffic must traverse Proctor).
- **Verdict:** **Rejected as the authority model.** Choreography is strong for extensibility, weak for guaranteed-exhaustive ordered execution — the opposite of this requirement.

### Option C — Central orchestration: a conductor (saga state machine)

A single durable conductor holds run state and drives the sequence; the plan is data.

- **No-skip:** ✓ A durable, ordered state machine with explicit transitions is the canonical way to guarantee exhaustive, ordered, resumable execution.
- **System-native:** ✓ The conductor, not the agent, advances the run.
- **Fit:** ✓ CORE §12 already records the intent ("Orchestration lifecycle, persisted state → feeds Process-Bot state machine"); Process-Bot already owns "run lifecycle, step-boundary orchestration" (RP-008).
- **Gap:** Needs an enforcement point so out-of-order/skip-ahead *dispatches* are refused, not just un-scheduled.
- **Verdict:** **Chosen as the core**, refined by Option D.

### Option D (chosen) — Event-**triggered** central orchestration with an enforcing gateway

The synthesis: **events trigger, the conductor decides, the gateway enforces.**

- **Events** (`fs.write`, `git.stage`, `claim.step.done`, `ci.*`, `run.finalize`) are *triggers* that wake the conductor — delivered as CLI-mediated appends to a run-scoped event log (spool-and-drain applied to control flow), **not** a bus.
- **Conductor** (Process-Bot) is a durable, event-sourced saga state machine; only it advances run state.
- **Gateway** (Proctor) consults live run state on every dispatch and refuses skip/out-of-order actions (a new **Sequence/Barrier Gate**).
- **No-skip:** ✓ All three skip modes closed (declarative required-set + reconciler; barrier/join gate; evidence-gated completion).
- **Single control plane:** ✓ No new surface; reached via `aegis process`/`aegis proctor`. **No bus.**
- **Verdict:** **Accepted.** Specified in full by HATHOR-RP-009.

---

## 4. Decision

**AEGIS adopts event-triggered central orchestration with an enforcing gateway (Option D)** as the coordination model for all bot and linter execution:

1. **Plan as data.** The required set and ordering are declared in an executable process graph over the hierarchy assets (Runbook/Workflow/Checklist), resolved by the system — never agent intent.
2. **Conductor.** Process-Bot becomes a durable, event-sourced saga state machine. Only Process-Bot advances run state; the agent's "done" is a *request*, evaluated by the system.
3. **Enforcing gateway.** Proctor applies the Sequence/Barrier Gate (G03 in CANON-001's fifteen-gate registry) and consults run state on every dispatch.
4. **Events trigger only.** Triggers append to a run-scoped event log (event-sourced, deduped on `event_id`); no machine-tier bus, no secondary control surface.
5. **No-skip is mechanical within the v1 trust boundary.** Enforced by declarative required-set + barrier/join semantics + evidence-gated completion + a finalize-time completeness reconciler (`val-completeness-Bot`) that diffs the required set against authoritative run/evidence ledgers with telemetry correlation.

Per accepted RP-013 `AEG-THR-001`, these prevention claims apply to cooperative-but-fallible agents. An adversarial local process can rewrite workspace files; hash-chain anchoring and Tower/CI attestation are the phased integrity controls.

The full component design, schemas, requirements (`AEG-GW-001..015`), and phasing are in **HATHOR-RP-009**.

---

## 5. Terminology: the two senses of "event-driven gateway"

The operator's phrase is correct but overloaded; this decision separates the two senses so they are never conflated again:

| Sense | Meaning | Disposition |
|---|---|---|
| **Coordination-model sense** — "gateway" = an event bus / choreography hub through which bots self-coordinate | The *authority* model | **Rejected** (Option B): cannot guarantee no-skip; violates PLAT-001 / RP-003 / BOT-TAX-006 |
| **Enforcement sense** — "gateway" = a single policy chokepoint (Proctor) that admits/refuses each action | The *enforcement* mechanism | **Adopted** (Option D) |
| **Modeling primitive** — BPMN "event-based gateway" = a branch node that waits for one of N events | A node type *inside* the process graph | **Adopted** as `gateway.event` (with a mandatory `timeout` branch), alongside `gateway.xor` / `gateway.and` |

Events are the right **trigger** and a useful **branch primitive**; they are the wrong **authority**.

---

## 6. Comparison matrix

| Criterion | A · Agent + guards | B · Choreography | C/D · Orchestration (chosen) |
|---|---|---|---|
| Prevents omission | ✗ | ✗ (emergent) | ✓ (required-set + reconciler) |
| Prevents order violation | ✗ | ~ (best-effort) | ✓ (barrier/join gate) |
| Prevents false completion | ✓ (at façades only) | ✗ | ✓ (evidence-gated, every node) |
| System-native (agent out of control flow) | ✗ | ~ | ✓ |
| Single control plane (PLAT-001) | ✓ | ✗ (adds a bus) | ✓ |
| Honors RP-003 (no machine-tier bus) | ✓ | ✗ | ✓ |
| Honors BOT-TAX-006 (via Proctor) | ✓ | ✗ | ✓ (strengthened) |
| Crash-safe / resumable | ✗ | ~ | ✓ (durable event-sourced state) |
| Reuses existing families | ✓ | ✗ | ✓ |

---

## 7. Consequences

### 7.1 Positive

- Within the RP-013 v1 trust boundary, no-skip becomes a **provable, mechanical property**, not a behavioral hope.
- Control flow is **deterministic and system-owned**; the LLM is out of the control-flow loop (it produces step *content* only).
- Crash-safety and no-skip become **the same property** (durable state cannot forget a mandatory node).
- Nothing new to learn operationally: reuses Proctor, Process-Bot, hierarchy assets, CVS, spool-and-drain, Checklist, Tower.

### 7.2 Negative / costs

- Process-Bot gains real complexity (durable state machine, resume, barriers) vs. today's thinner role.
- Proctor does more per dispatch (folds run state) — mitigated by the same result/state caching discipline used by the CVS runner.
- Process graphs must be authored/derived and kept correct — mitigated by a new `ml-graph-integrity` linter gating the graph itself.

### 7.3 Changes ratified with this ADR

1. **Inverts RP-007 §6.1** — validation shifts from "agent MUST call" to "system calls on event."
2. **Promotes `AEG-VAL-015`** (runbook-declared validation) from opt-in/P4 to a mandatory default per node.
3. **Registers the Sequence/Barrier Gate as G03** in the canonical fifteen-gate registry (CANON-001 §2); CORE §14 and ARCH-001 point to that registry.
4. **Specifies Process-Bot as a durable saga state machine** (realizing the CORE §12 adoption-log intent).

### 7.4 Neutral

- No new authority plane and no new top-level CLI domain (folds under `process`/`proctor`, ≤ 9 domains per `AEG-REQ-PLAT-008` as revised by ADR-003 §2.2).
- Validators/linters are unchanged in nature; only their *invocation authority* moves to the conductor.

---

## 8. Compliance with ratified decisions

| Ratified decision | This ADR |
|---|---|
| `AEG-REQ-PLAT-001` single control plane | ✓ no new surface |
| `RP-003` no machine-tier event bus | ✓ event-sourced log, spool-and-drain |
| `BOT-TAX-006` all traffic via Proctor | ✓ strengthened (orchestration chokepoint) |
| `AEG-REQ-TEL-002` telemetry never fatal | ✓ enforcement fails closed; observation fails open |
| `AEG-VAL-005` human-only waiver | ✓ mandatory units waivable by humans only |
| Canonical Rule 4 (reuse over invention) | ✓ reuses existing families/discipline |

---

## 9. Related documents

- **HATHOR-RP-009** — Orchestration Gateway (the design implementing this decision).
- **HATHOR-RP-007 / TS-001** — CVS (the detection fabric this orchestrates; §6.1 inverted here).
- **HATHOR-REQ-CORE-001** — §12 (persisted-state orchestration intent), §14 (canonical gate-registry pointer), §16 (acceptance).
- **HATHOR-RP-003** — telemetry transport (the no-bus precedent this decision honors).
- **HATHOR-ARCH-001** — §5 request-class routing, §15 canonical gates, §20 Orchestration Gateway.

---

## 10. Follow-on work (not authorized by this ADR)

- **Applied:** `AEG-VAL-015` promotion and the G03 Sequence/Barrier registration are reflected through CANON-001, CORE §14, RP-009, and ARCH-001.
- **Approved plan:** PLAN-003 places RP-009 phases P0–P5 and the remaining validators.
- **Draft implementation detail:** TS-002 specifies the state machine, admission predicate, and reconciler; its unresolved implementation questions remain review items.

---

*Decision record — ACCEPTED 2026-09-13. No implementation authorized by this document.*
