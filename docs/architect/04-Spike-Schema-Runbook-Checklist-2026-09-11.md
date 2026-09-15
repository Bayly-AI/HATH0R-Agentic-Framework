---
id: AEGIS-REPORT-004
title: '04 — Spike Design: Schema Dump + Runbook→Checklist Lifecycle'
summary: 'Playbook: security-devops / dvo-deploy-handoff Runbook: security-devops / dvo-deploy-ticket Checklist: security-devops / dvo-deploy-ticket Workflow: devops/dvo-deploy-request'
doc_type: REPORT
diataxis: how-to
audience: [architect, agent]
tags: []
version: 0.1.0
status: draft
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
# 04 — Spike Design: Schema Dump + Runbook→Checklist Lifecycle

**Date:** 2026-09-11  
**Type:** Spike / prototype design — **not production**, **no code landed in InfraOS by this task**  
**Goal:** Specify the smallest experiment that proves (a) bounded machine schema discovery and (b) one end-to-end runbook execution that updates a checklist.

---

## 1. Why this spike

From prior reports:
- Hierarchy commands today are **catalog-only**: `list|show|search|categories|tags|index` — **no `run`**.
- Sampled Communications assets contain one linked chain:

```text
Playbook:  security-devops / dvo-deploy-handoff
Runbook:   security-devops / dvo-deploy-ticket
Checklist: security-devops / dvo-deploy-ticket
Workflow:  devops/dvo-deploy-request
```

- `commands inventory` proves schema-ish data exists but is **~165KB / ~41k tokens** — unusable as default agent context.
- CLI Spec needs progressive schema plus `effects`, `output_kind`, and `cardinality` declarations. CLI Spec v0.3 remains a candidate, so the spike must pin the exact schema snapshot and checksum it tests.

---

## 2. Spike scope (in / out)

### In scope
1. **Schema dump v0** JSON document shape + filter semantics (positional command path, `--domain`, `--limit`, `--cursor`).  
2. **Runbook run v0** algorithm for `dvo-deploy-ticket` only, including `--dry-run`.  
3. **Checklist update v0** file or state write after each logical step (local, development-only).  
4. Success criteria and test cases.  
5. Throwaway reference implementation sketch (pseudocode / optional local script path under BaylyAI research — not product merge).

### Out of scope
- Full façade namespaces from ADR-001  
- All 79 command groups JSON parity  
- Production checklist store / multi-user locking  
- Non-dev environment writes  
- Automatic Jira/Teams side effects without `--yes` and proctor checks  

---

## 3. Spike A — Bounded schema dump

### 3.1 Command shape (proposed)
```bash
infraos-os -o json schema [command path ...] \
                  [--domain process|proctor|operator|tower|knowledge|repo|delivery|all] \
                  [--limit N] \
                  [--cursor <token>]
```

Compatibility spike without shipping CLI change: derive from existing:
```bash
infraos-os commands inventory > /tmp/inv.json
# filter with jq to schema v0
```

### 3.2 Schema v0 document

```json
{
  "clispec": "0.3",
  "name": "infraos-os",
  "version": "9.3.0",
  "output": {"tty": "text", "piped": "json"},
  "global_args": [
    {
      "name": "--output",
      "short": "-o",
      "type": "string",
      "enum": ["auto", "text", "json"],
      "default": "auto",
      "description": "Output format; auto detects TTY"
    }
  ],
  "commands": [
    {
      "name": "operator connections list",
      "description": "List connection definitions",
      "effects": "read_only",
      "output_kind": "data",
      "cardinality": "unbounded",
      "args": [
        {"name": "--definitions-dir", "type": "path", "required": false},
        {"name": "--fields", "type": "string", "required": false},
        {"name": "--limit", "type": "integer", "required": false, "default": 25},
        {"name": "--cursor", "type": "string", "required": false}
      ],
      "pagination": {
        "style": "cursor",
        "cursor_field": "next_cursor",
        "cursor_arg": "--cursor",
        "limit_arg": "--limit"
      },
      "fields_arg": "--fields",
      "stdout_schema": {},
      "example": {"args": ["--limit", "10"]}
    }
  ],
  "errors": [
    {"kind": "not_found", "exit_code": 3, "retryable": false, "description": "Requested command or resource does not exist"},
    {"kind": "dependency_unhealthy", "exit_code": 6, "retryable": true, "description": "A required integration is unhealthy"}
  ]
}
```

The example targets the v0.3 candidate shape as of 2026-09-11. Because the candidate can change, the spike must vendor the schema and record its SHA-256. Legacy aliases that remain invocable must appear as their own command entries in the complete, unfiltered schema; a filtered façade view may omit them and must identify itself as filtered through an `x-` extension.

### 3.3 Filter rules
| Input | Behavior |
|-------|----------|
| no filter | Complete CLI Spec document containing every invocable canonical and compatibility command; intended for validation/tooling, not routine agent context |
| `--domain operator` | Only connections/jira/teams/mcp* family |
| positional `workflows run` | Single command detail |
| `--limit 25` | Hard cap; `truncated=true` if more |
| `--cursor <token>` | Continue a truncated filtered result |
| filtered query default | Façade entries first, page size chosen to keep each response ≤8KB; response declares `x-filtered=true` |

### 3.4 Acceptance tests (spike)
| ID | Test | Pass |
|----|------|------|
| S1 | Full inventory chars ≫ one filtered schema page | each default filtered page ≤ 8KB (~2k-token proxy) |
| S2 | Complete unfiltered schema includes every invocable command; every top-15 path also appears through a filtered query | yes |
| S3 | Each data command has `effects`, `output_kind`, and `cardinality` | yes |
| S4 | Unknown positional command path → exit 3; one-line JSON error envelope is last line of stderr | yes |
| S5 | `schema` works without config/auth and performs no writes | yes |
| S6 | Complete output validates against the vendored v0.3 candidate snapshot/checksum; runtime test verifies command completeness | yes |

### 3.5 Reference filter (throwaway)

```python
# research-only sketch
DOMAINS = {
  "operator": ["connections", "jira", "teams", "mcp", "mcp-servers", "github"],
  "process": ["workflows", "orient", "context", "playbooks", "runbooks", "checklists"],
  "proctor": ["secrets", "agent", "pr", "quality", "git", "review"],
  "tower": ["status", "health", "commands", "reports", "tower"],
}
```

---

## 4. Spike B — Runbook run updates checklist

### 4.1 Command shape (proposed)
```bash
infraos-os -o json process runbook run dvo-deploy-ticket \
  --context pr_url=... \
  --context change=... \
  --context product_epic=... \
  --dry-run
```

Today’s stand-in (manual composition):
```bash
infraos-os runbooks show dvo-deploy-ticket
infraos-os checklists show dvo-deploy-ticket
infraos-os playbooks show dvo-deploy-handoff
infraos-os workflows describe devops/dvo-deploy-request
# then workflows run ... and hand-edit checklist — proves gap
```

### 4.2 State files (local spike)
```text
.infraOS/state/runs/<run_id>.json
.infraOS/state/checklists/dvo-deploy-ticket.json   # runtime overlay
# source catalogs remain the markdown/yaml definitions
```

The spike deliberately uses the current Communications `.infraOS` convention. The outline's target `.ai/aegis` layout and migration/compatibility rules are ADR work, not part of this throwaway experiment. Local JSON updates use write-to-temp + atomic rename; this protects the file, not external side effects.

### 4.3 Run algorithm

```text
function runbook_run(id, ctx, dry_run):
  rb = load_runbook(id)
  cl = load_checklist(rb.checklist_id)
  pb = load_playbook(rb.playbook_id)            # optional
  proctor_precheck(rb.effects, env=development) # refuse non-dev writes

  plan = []
  for step in rb.steps or workflows_from(rb):
    plan.append({step, workflow_id, checklist_item_ids})

  if dry_run:
    return {dry_run: true, status: "planned", plan, exit: 0}

  run = create_run(rb, ctx)
  for step in plan:
    key = idempotency_key(run.id, step.id)
    checkpoint(run, step, key, "pending")
    mark_checklist(cl, step.checklist_item_ids, "in_progress")
    result = workflows_run(step.workflow_id, ctx, idempotency_key=key)
    if result.failed:
      mark_checklist(..., "failed", evidence=result)
      finalize_run(failed); return exit 1
    if result.ambiguous:
      checkpoint(run, step, key, "reconciliation_required")
      return exit 1
    mark_checklist(..., "done", evidence=result)
    checkpoint(run, step, key, "done")
  finalize_run(succeeded); return exit 0
```

### 4.4 JSON result envelope

```json
{
  "run_id": "run_20260911_01",
  "runbook_id": "dvo-deploy-ticket",
  "playbook_id": "dvo-deploy-handoff",
  "checklist_id": "dvo-deploy-ticket",
  "dry_run": false,
  "status": "succeeded",
  "steps": [
    {
      "workflow_id": "devops/dvo-deploy-request",
      "status": "succeeded",
      "checklist_items": ["create-ticket", "estimate", "announce"]
    }
  ],
  "checklist": {
    "id": "dvo-deploy-ticket",
    "items": [
      {"id": "create-ticket", "status": "done"},
      {"id": "estimate", "status": "done"},
      {"id": "announce", "status": "done"}
    ]
  }
}
```

### 4.5 Proctor constraints (mandatory in spike)
- `effects` on runbook default `non_idempotent`.  
- `--dry-run` never calls Jira/Teams.  
- A non-interactive live run with non-idempotent effects must refuse without `--yes` (exit 7, `confirmation_required`); a human TTY may confirm interactively. Development-only boundaries still apply; **no** testing/staging/prod.  
- Every external step receives a stable idempotency key and is checkpointed before invocation; an ambiguous response enters reconciliation instead of blind retry.  
- Record actor (`human|agent`) and cwd product id in run record.

### 4.6 Acceptance tests

| ID | Test | Pass |
|----|------|------|
| R1 | `run --dry-run` prints plan, no workflow side effects, exit 0, `dry_run=true` | |
| R2 | Missing context keys → exit 2 structured error | |
| R3 | Simulated workflow success flips checklist items to done | |
| R4 | Simulated workflow fail leaves item failed, run failed | |
| R5 | Re-show checklist reflects overlay state | |
| R6 | Does not require loading full commands inventory | |
| R7 | Crash/retry with the same run id does not duplicate an Operator side effect | |
| R8 | Non-TTY live mutation without `--yes` refuses safely instead of prompting or proceeding | |

---

## 5. Suggested throwaway harness layout (optional local only)

If a disposable script is written later under BaylyAI research (not product):

```text
BaylyAI/AEGIS/spikes/2026-09-11/
  README.md
  schema_filter.py      # inventory → schema v0
  runbook_sim.py        # dry-run lifecycle simulator
  fixtures/
    dvo-deploy-ticket.runbook.yaml
    dvo-deploy-ticket.checklist.yaml
```

**This task did not create production InfraOS code.** Harness may be added in a follow-up explicit request.

---

## 6. Instrumentation plan

| Metric | How |
|--------|-----|
| Schema payload tokens | `chars/4` on filtered JSON |
| Dry-run latency | wall clock |
| Checklist mutations | count of status transitions |
| Safety | assert no network calls in dry-run (mock operator) |

Compare against baseline manual path token cost (report 05).

---

## 7. Risks

| Risk | Mitigation |
|------|------------|
| DVO assets lack machine-readable links | Spike frontmatter convention |
| Workflow run is heavy/side-effecting | Dry-run + mock executor first |
| Checklist source is markdown only | Runtime overlay JSON |
| External effects and local checklist cannot be one atomic transaction | Per-step idempotency keys, durable checkpoints, and reconciliation state |
| Scope creep to full façade | Hard stop after DVO + schema filter |

---

## 8. Exit criteria for “spike done”

1. Written schema v0 example validated against inventory sample.  
2. Dry-run lifecycle JSON for dvo-deploy-ticket produced (even if simulated).  
3. Checklist before/after states documented.  
4. Findings folded into ADR-001 phase 4 notes.  
5. Explicit decision: promote to implementation backlog **or** revise model.

---

## 9. Immediate findings already available (pre-code)

| Finding | Evidence |
|---------|----------|
| Catalog commands cannot run lifecycle | `runbooks --help` has no `run` |
| One linked chain was found in sampled Communications evidence | playbooks/runbooks/checklists list → dvo-deploy-* |
| Workflow executor already exists and is documented | AD-003/004; use it rather than inventing a second executor |
| Schema source exists but unbounded | commands inventory ~41k tokens |
| Operator mutations must stay behind proctor | top-30 jira/teams usage |

**Conclusion:** Spike is feasible with high leverage and low surface area; DVO triplet is the correct pilot.
