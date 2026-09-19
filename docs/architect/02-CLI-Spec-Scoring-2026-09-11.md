---
id: HATHOR-REPORT-003
title: 02 — CLI Spec Scoring (`infraos-os` vs clispec.dev)
summary: 'Principles (CLI Spec): 1. **Structured Output** — explicit JSON; prefer structured when piped; structured failures 2. **Schema Introspection** — discover commands/args/output/errors at runtime 3. **Stderr/Stdout Separ...'
doc_type: REPORT
diataxis: reference
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
# 02 — CLI Spec Scoring (`infraos-os` vs clispec.dev)

**Date:** 2026-09-11  
**Spec references:** [CLI Spec](https://clispec.dev/) v0.2 (frozen) / v0.3 candidate (Aug 2026); supporting: [Command Line Interface Guidelines](https://clig.dev/)  
**Method:** For each high-use command from report 01, inspect `--help` for machine-contract flags and sample live stdout size/exit behavior. Scores are provisional: a flag's presence does not prove structured failures, clean streams, safe retry semantics, or non-interactive behavior.

### Scoring rubric (per principle)
| Score | Meaning |
|-------|---------|
| 0 | Absent / hostile to agents |
| 1 | Partial, inconsistent, or not fully verified |
| 2 | Meets spirit of principle |

Principles (CLI Spec):
1. **Structured Output** — explicit JSON; prefer structured when piped; structured failures  
2. **Schema Introspection** — discover commands/args/output/errors at runtime  
3. **Stderr/Stdout Separation** — data on stdout, rest on stderr  
4. **Non-Interactive by Default** — never block without TTY  
5. **Safe Retries** — declare effects; safe re-run guidance  
6. **Bounded Output** — limit/fields/pagination controls  

Plus two scored practical extras: **dry-run** and **semantic exit codes**. Long-flag clarity is discussed qualitatively but is not a ninth scored axis.

---

## 1. Flag matrix (help-text probe, live CLI)

| Command | `--json` | `--format`/`-o` | `--dry-run` | `--yes` | schema mention |
|---------|----------|-----------------|-------------|---------|----------------|
| status | Y | - | - | - | - |
| health | Y | - | - | - | - |
| orient | Y | - | - | - | - |
| connections / list / health / test | - | - | - | - | - |
| workflows / list / run / describe / validate | - | - | - | - | - |
| knowledge list | Y | - | - | - | - |
| knowledge push | Y | - | Y | - | - |
| vectra search | - | - | - | - | - |
| vectra indices | Y | - | - | - | - |
| mcp list / health / call | Y | - | - | - | - |
| mcp-servers list | Y | - | - | - | - |
| agent preflight | Y | - | - | - | - |
| tower / tower version | - | - | - | - | - |
| orchestration list | Y | - | - | - | - |
| playbooks/runbooks/checklists list | - | - | - | - | - |
| strategies list | - | Y | - | - | - |
| pr validate | Y | - | - | Y | - |
| quality check | Y | - | - | - | - |
| repo refresh | Y | - | Y | - | - |
| secrets | Y | - | - | - | Y |
| secrets doctor | - | - | - | - | - |
| jira / github / teams / review / context | - | - | - | - | - |
| commands inventory | Y | - | - | - | - |
| version scan | Y | - | - | - | - |
| git branch | - | - | - | - | - |

**Headline:** JSON is **opt-in and uneven**. No global `--output`/`--format` contract. Dry-run is rare. Hierarchy catalogs lack machine output. Highest-use Operator commands (`connections *`, `jira`, `teams`) largely **unscored on structured output**.

---

## 2. Scores for top inventory commands

| # | Command | P1 Out | P2 Schema | P3 I/O | P4 Non-int | P5 Retry | P6 Bound | Dry-run | Exit codes | **Total /16** |
|---|---------|--------|-----------|------------|------------|----------|----------|---------|------------|---------------|
| 1 | connections list | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 2 | workflows list | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 3 | jira connect | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | **4** |
| 4 | workflows run jira-ticket-linked | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | **4** |
| 5 | workflows run dvo-deploy-request | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | **4** |
| 6 | secrets doctor | 0 | 1 | 1 | 2 | 1 | 0 | 0 | 1 | **6** |
| 7 | status [--json] | 2 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **7** |
| 8 | orient [--json] | 2 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **7** |
| 9 | connections health | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 10 | connections test-service | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 11 | agent preflight [--json] | 2 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **7** |
| 12 | repo refresh | 2 | 0 | 1 | 2 | 1 | 0 | 2 | 1 | **9** |
| 13 | knowledge push | 2 | 0 | 1 | 2 | 1 | 0 | 2 | 1 | **9** |
| 14 | vectra search | 0 | 0 | 1 | 2 | 1 | 1 | 0 | 1 | **6** |
| 15 | vectra indices | 2 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **7** |
| 16 | mcp list [--json] | 2 | 1 | 1 | 2 | 1 | 0 | 0 | 1 | **8** |
| 17 | mcp-servers list | 2 | 1 | 1 | 2 | 1 | 0 | 0 | 1 | **8** |
| 18 | jira issue | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | **5** |
| 19 | jira create | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | **3** |
| 20 | jira list-projects | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 21 | jira transition | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | **3** |
| 22 | teams announce | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | **3** |
| 23 | git branch validate/create | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 24 | review | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | **4** |
| 25 | pr validate | 2 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **7** |
| 26 | quality check | 2 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **7** |
| 27 | context | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 28 | workflows run universal-orientation | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | **4** |
| 29 | playbooks/runbooks/checklists * | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 1 | **5** |
| 30 | commands inventory | 2 | 1 | 1 | 2 | 1 | 0 | 0 | 1 | **8** |

**Average total = 170/30 ≈ 5.7 / 16 (~35%).** Read-only behavior can make retries operationally safe, but without declared `effects` it does not earn full CLI Spec v0.3 credit.

---

## 3. Principle-level findings

### P1 Structured Output — **Weak / inconsistent**
- Good: `status`, `health`, `orient`, `mcp *`, `repo refresh`, `knowledge list/push`, `commands inventory`.
- Bad: **entire connections tree**, **workflows tree**, **hierarchy catalogs**, most **jira/teams**.
- No global `--output`/`--format` contract and no declared piped default.
- A corpus-wide probe has not established that every structured failure is a one-line error envelope on stderr; JSON success flags alone are insufficient.

### P2 Schema Introspection — **Partial**
- `commands inventory` is a real JSON catalog (**525+ command paths**, ~165KB / ~41k tokens) — too large to inject wholesale.
- No progressive `infraos-os schema <path>` or filtered inventory by domain.
- `secrets` mentions schema in help (env schema), not command schema.
- Root `infraos-os help` is **invalid** (`invalid choice: 'help'`) — breaks agent discovery habit.

### P3 Stdout/Stderr — **Unknown / likely weak**
- Not fully instrumented per command; every row therefore receives the provisional score 1 rather than a compliance pass.
- CLI Spec requires universal separation; treat as debt until proven.

### P4 Non-Interactive — **Mostly OK for reads; risky for writes**
- List/status/orient complete without prompts.
- Mutation paths (`jira create/transition`, `teams announce`, workflow runs) need explicit audit for hidden prompts; `--yes` only confirmed on `pr validate`.

### P5 Safe Retries / effects — **Mostly undeclared**
- No `effects: read_only|idempotent|non_idempotent` on help or inventory.
- `knowledge push` and `repo refresh` offer `--dry-run` (good outliers).
- Jira create/transition and teams announce are classic non-idempotent ops without dry-run.

### P6 Bounded Output — **Poor**
- `mcp list` ~11KB / ~2.8k tokens for integration posture.
- `status --json` ~7KB / ~1.7k tokens even when rc≠0.
- `commands inventory` ~165KB / ~41k tokens — agent footgun.
- No `--fields`, `--limit` consistency (vectra search has `-n` only).

### Exit codes — **Binary-ish, overloaded**
Observed live:
| Command | rc | Note |
|---------|----|------|
| status / status --json | 2 | degraded posture encoded as failure |
| connections health | 1 | unhealthy deps |
| agent preflight | 1 | not fully ready |
| commands inventory | 1 | odd non-zero on successful-looking dump |
| secrets doctor --json | 2 | doctor issues |
| healthy reads (workflows list, etc.) | 0 | OK |

No documented stable mapping (auth vs validation vs dependency vs usage).

---

## 4. CLI Spec v0.3 axes (effects / output_kind / cardinality)

If adopting v0.3 declarations, recommended defaults for top commands:

| Command | effects | output_kind | cardinality |
|---------|---------|-------------|-------------|
| connections list | read_only | data | unbounded (paginate) |
| connections health | read_only | data | unbounded (paginate or return a declared single summary) |
| workflows list | read_only | data | unbounded (paginate) |
| workflows run | non_idempotent (usually) | data | single |
| status/orient | read_only | data | single |
| jira create/transition | non_idempotent | data | single |
| jira issue get | read_only | data | single |
| teams announce | non_idempotent | data | single |
| knowledge push | idempotent (ideal) | data | single |
| repo refresh | idempotent | data | single |
| commands inventory | read_only | data | unbounded |
| mcp list | read_only | data | unbounded |
| process runbook run (future) | non_idempotent unless end-to-end idempotency is proven | data | single |
| checklists show | read_only | data | single |

---

## 5. Priority remediation order (research recommendation only)

1. **Global contract:** canonical `--output/-o json|text|auto`, stdout/stderr policy, exit-code/error-kind table, fix `help`.  
2. **Top-30 JSON parity:** connections, workflows, jira, teams, hierarchy catalogs.  
3. **Effects + dry-run** on all mutations in top 30.  
4. **Bounded discovery:** `schema --domain operator|process|proctor|tower` and `commands inventory --domain … --limit`.  
5. **Agent skill pack** (~800 tokens) documenting the top 15 commands — cheaper than inventory dump (industry CLI+Skills finding).

Because CLI Spec v0.3 is still a candidate, pin the exact schema snapshot and checksum used for any spike; do not present a production contract as permanently v0.3-compatible until the version freezes.

---

## 6. Summary scorecard

| Area | Grade | Comment |
|------|-------|---------|
| Human operability | B | Large surface, Make wrappers, works for power users |
| Agent operability (CLI Spec) | D+ | Uneven JSON, no effects, huge discovery payloads |
| Hierarchy HATHOR readiness | D | Catalog-only; no run lifecycle machine contract |
| Operator plane | C- | High use, weak machine I/O |
| Proctor plane | C | Gates exist but not unified/dry-runnable |
| Manifest / schema | C+ | inventory exists but unbounded |

**Bottom line:** `infraos-os` is closer to a human multi-tool than to a CLI Spec–grade agent control plane. Closing the gap is mostly **contract consistency on the existing top 30**, not new features.
