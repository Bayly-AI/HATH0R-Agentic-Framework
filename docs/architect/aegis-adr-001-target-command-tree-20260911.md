---
id: HATHOR-ADR-001
title: '03 — ADR: Target Command Tree (Domains + Hierarchy Lifecycle)'
summary: infraos-os` 9.3.0 exposes **79 top-level command groups** and **525+** inventory paths. Sampled Communications usage (report 01) concentrates on ~30 normalized invocation patterns, mostly Operator + Process paths, wit...
doc_type: ADR
diataxis: decision
audience: [architect, agent]
tags: []
version: 0.1.0
status: proposed
created: '2026-09-11'
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
# 03 — ADR: Target Command Tree (Domains + Hierarchy Lifecycle)

**Status:** Proposed (research only — no implementation authorized by this document)  
**Superseded in part (2026-09-13):** HATHOR-ADR-003 supersedes the `infraos-os`-rooted binary strategy and the "Greenfield AEGIS binary — rejected" alternative below. The platform of record is the greenfield `aegis` binary; this ADR's surface is retained as the InfraOS migration/façade path. The domain taxonomy, lifecycle rule, global flags, and exit-code table remain authoritative.  
**Date:** 2026-09-11  
**ADR ID:** HATHOR-ADR-001  
**Relates to:** InfraOS AD-001 (single entrypoint), AD-002 (plugin registry), AD-005 (connections vs MCP), baseline AEGIS CLI research report  
**Deciders:** Unassigned — this proposal remains unapproved; any future acceptance requires an explicitly designated BaylyAI operator.

---

## Context

`infraos-os` 9.3.0 exposes **79 top-level command groups** and **525+** inventory paths. Sampled Communications usage (report 01) concentrates on ~30 normalized invocation patterns, mostly Operator + Process paths, with one linked DVO deploy hierarchy chain found in the evidence.

AEGIS defines:
- CLI as sole agent control plane
- Bots: Process, Proctor, Operator, and Observation (with focused task/benchmark/success-rate/retry/token workers)
- Control Tower as the upward authority and visibility plane, not a worker bot
- Hierarchy: Procedure → Strategy → Playbook → Runbook → Workflow → Checklist

Industry guidance (clig.dev, CLI Spec, kubectl/gh/terraform patterns) favors:
- Progressive disclosure (≤2–3 nesting levels)
- Hybrid high-level actions + resource trees
- Stable machine contract separate from human help

## Decision (proposed)

Adopt a **façade command tree** over the existing plugin surface:

1. **Seven primary domains plus always-on meta commands** at root (stable, agent-documented).  
2. **Three bot namespaces plus the Control Tower authority surface** (`process`, `proctor`, `operator`, `tower`) among those domains, each wrapping existing handlers. Observation-Bot remains an internal telemetry network surfaced through `tower`, not an eighth public root.  
3. **One canonical hierarchy lifecycle resource** (`process runbook run`) that chains artifacts; existing plural roots remain compatibility aliases.  
4. **Global communication contract flags** on the root parser.  
5. Keep legacy top-level commands as **compatibility aliases** for ≥2 major versions (per AD-001/002 migration style).

This is a **taxonomy and contract ADR**, not a rewrite of services.

---

## Target root surface

```text
infraos-os
├── help | version | schema | doctor          # always-on meta
├── process …                                # Process-Bot
├── proctor …                                # Proctor-Bot
├── operator …                               # Operator-Bot
├── tower …                                  # Control Tower authority + Observation-Bot results
├── knowledge …                              # knowledge plane (existing)
├── repo …                                   # repository operations (existing)
├── delivery …                               # pr / quality / release façade
└── <legacy aliases> …                       # full 79-group compatibility
```

### Global flags (contract)
```text
--output, -o json|text|auto # default auto (TTY=text, pipe=json)
--profile <name>            # config profile
--quiet                     # suppress non-error telemetry
```
Command-scoped flags are declared only where meaningful: `--dry-run` and `--yes` for applicable mutations; `--fields`, `--limit`, and `--cursor` for data collections whose cardinality requires projection or pagination. `--format` may remain an alias only where compatibility requires it.

### Exit code contract (public API)
| Code | Meaning |
|------|---------|
| 0 | Success, including dry-run and idempotent no-op |
| 1 | Internal or otherwise unclassified runtime error |
| 2 | Usage / validation error |
| 3 | Not found |
| 4 | Auth / permission |
| 5 | Conflict / already exists |
| 6 | Dependency unhealthy (connections/mcp) |
| 7 | Confirmation required in a non-interactive context |

Non-error data states such as `degraded` or `changes_pending` must be declared separately as named outcomes with non-overlapping codes; they must not reuse the usage-error code.

---

## Domain trees

### 1. `process` — hierarchy + execution (Process-Bot)

```text
process
├── context set|show                         # was: context
├── orient                                   # was: orient; inherits global output
├── procedure list|show|create               # NEW thin resource (or map plans/initiatives)
├── strategy list|show                       # wrap strategies
├── playbook list|show|search
├── runbook list|show|search|run|status      # run = lifecycle entry
├── workflow list|describe|run|validate|status
├── checklist list|show|update|complete
└── handoff list|show                        # guides/handoffs
```

**Canonical lifecycle rule (normative):**
```text
process runbook run <id>
  1. load runbook + linked playbook/strategy/procedure metadata
  2. proctor.precheck (effects, env, write boundary)
  3. create durable run record + per-step idempotency keys
  4. execute linked workflow(s) in order
  5. checkpoint checklist items as verified steps complete
  6. reconcile any external effect whose response is ambiguous
  7. emit JSON result {run_id, workflow_runs[], checklist_id, status}
```

### 2. `proctor` — policy, gates, safe mutation (Proctor-Bot)

```text
proctor
├── preflight agent|repo|secrets             # agent preflight, secrets doctor
├── gate pr|quality|qgates|review
├── policy explain|list                      # map policies/governance
├── branch validate|create                   # git branch governance
├── approve request|status                   # future human grant for non-dev writes
└── audit list|show                          # invocation audit (future)
```

### 3. `operator` — external systems (Operator-Bot)

```text
operator
├── connections list|show|health|test|probe|validate
├── mcp list|health|call
├── mcp-servers list|show|health|add|…
├── jira …
├── github …
├── teams …
├── confluence …
├── zendesk …
└── notify send                              # generic announce façade
```

### 4. `tower` — posture & control plane (Control Tower authority)

```text
tower
├── status [--group]                         # was: status
├── health
├── inventory commands|connections|workflows # bounded
├── observations task|benchmark|success-rate|retry|token
├── reports …                                # existing reports
├── observability …
└── version show                             # expand beyond tower version
```

### 5. `knowledge`
```text
knowledge
├── search <query> [--scope project|machine|organization|public]
├── get <id>
├── publish|update                           # small knowledge microbursts
├── verify <id>                              # Draft → Verified
├── provenance show <id>
└── index status|refresh                     # wrap vectra/knowledge backends
```
Default search follows Project → Machine → Organization → Public and returns an explicit no-confident-match result rather than silently selecting a weak result.

### 6. `repo`
```text
repo
├── init|inspect|refresh
├── layout validate                          # target universal layout
├── manifest show|validate
└── agents list|validate                     # scoped AGENTS.md chain
```
Keep existing `repo refresh|canonical-verify|…` behavior behind this domain (AD-00R). Migration from `.infraOS` to the outline's `.ai/aegis` target is a separate compatibility decision. *(2026-09-13: the canonical target is `.aegis/` per CORE-001 §7.1 and ADR-004 §2.3; `.ai/aegis` was the outline-era label.)*

### 7. `delivery`
```text
delivery
├── pr validate|quick|ai
├── release …
├── estimate …
└── eos …                                    # end-of-sprint style reports
```

### 8. Meta
```text
schema [path] [--domain process|proctor|operator|tower]
doctor                                       # umbrella: secrets + connections + mcp + agent
help                                         # MUST work (fix invalid choice)
```

---

## Mapping from today’s top 30

| Today | Target |
|-------|--------|
| connections * | operator connections * |
| workflows * | process workflow * |
| jira * | operator jira * |
| teams announce | operator notify/teams |
| secrets doctor | proctor preflight secrets |
| status | tower status |
| orient | process orient |
| agent preflight | proctor preflight agent |
| repo refresh | repo refresh (unchanged domain) |
| knowledge/vectra | knowledge * |
| mcp* | operator mcp* |
| pr/quality/review | proctor gate* / delivery pr |
| playbooks/runbooks/checklists | process playbook/runbook/checklist |
| commands inventory | tower inventory commands --domain … |
| context | process context |
| dvo-deploy workflow | process runbook run dvo-deploy-ticket |

---

## Hierarchy object model (minimal)

```yaml
# conceptual — not a shipped schema freeze
Procedure:
  id, title, outcome, strategy_ids[]
Strategy:
  id, procedure_ids[], title, playbook_ids[]
Playbook:
  id, strategy_ids[], title, runbook_ids[]
Runbook:
  id, playbook_id, title, workflow_ids[], checklist_id, effects
Workflow:
  id, steps[]   # existing .infraOS/workflows assets
Checklist:
  id, items[{id, title, status, evidence}]
Run:
  id, runbook_id, actor, intent, environment, status, idempotency_keys[], workflow_run_ids[], checklist_snapshot
```

**Compatibility:** Existing flat catalogs remain readable. Linking fields may start as frontmatter in markdown assets (DVO triplet first).

---

## Consequences

### Positive
- Agents learn **7 domains** (including 3 bot namespaces and the Tower authority surface) plus meta commands, not 79 roots.
- Matches AEGIS diagram language without discarding InfraOS services.
- Enables CLI Spec scoring recovery on the hot path first.
- DVO deploy becomes reference lifecycle.

### Negative / risks
- Dual tree during alias period (docs debt).
- Plugin registry must support multi-name registration (AD-002 extension).
- Teams may keep using legacy paths forever without deprecation discipline.

### Non-goals (explicit)
- No removal of legacy commands in v1 of façade.
- No mandatory daemon.
- No replacement of MCP plane (AD-005 stands).
- No agent production deploys (cr-deploy-gov-001 stands); proctor encodes it.

---

## Migration sketch (informational)

| Phase | Work |
|-------|------|
| 0 | ADR acceptance |
| 1 | Global flags + `help` fix + exit code doc |
| 2 | Add process/proctor/operator/tower façades over existing handlers |
| 3 | JSON parity on top 30 |
| 4 | `process runbook run` lifecycle for DVO only; retain `runbooks run` as a compatibility alias if needed |
| 5 | `schema --domain` bounded inventory |
| 6 | Deprecation warnings on unused roots |

---

## Alternatives considered

| Alternative | Why rejected (for now) |
|------------|-------------------------|
| Greenfield AEGIS binary | ~~Splits control plane; violates AD-001 spirit~~ **Superseded by HATHOR-ADR-003 (2026-09-13):** greenfield `aegis` adopted; this façade becomes the InfraOS migration path |
| Makefile-only hierarchy | Not agent-native; dual plane worsens |
| MCP-only agent API | Weak local-dev ergonomics plus the local payload baseline (report 05) and cited industry benchmark |
| Action-first only (`get/run` everywhere) | Fights existing resource-ish jira/connections habits |
| Leave 79 roots + skills only | Skills help, but discovery/hallucination remain high |

---

## Validation criteria (when implementation is authorized)

1. Agent can orient + connections health + run one workflow using only `process`/`operator`/`proctor`/`tower` docs ≤800 tokens.  
2. `infraos-os -o json process runbook run dvo-deploy-ticket --dry-run` returns a JSON plan without side effects (exit 0 and `"dry_run": true`).  
3. `commands inventory` default path is domain-filtered; full dump opt-in.  
4. CLI Spec average score on top 30 ≥ 12/16.  
5. Legacy aliases remain green for CI Make targets.

---

## References
- AEGIS-CLI-Research-Report-2026-09-11.md  
- 01-Invocation-Inventory-Top30-2026-09-11.md  
- 02-CLI-Spec-Scoring-2026-09-11.md  
- InfraOS docs/architecture/decision-log.md (AD-001–AD-008)  
- clispec.dev · clig.dev
