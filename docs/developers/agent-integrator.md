---
id: HATHOR-GUIDE-011
title: Agent Integrator Guide
summary: "As an Agent Integrator (or AI Agent), interact with HATHOR through the hath0r CLI, AGENTS.md, docs indexes, and .hath0r/ layout — never aegis or .aegis/."
doc_type: GUIDE
diataxis: how-to
audience: [developer, agent]
tags: [cli, agent, hath0r, upl]
version: 0.2.0
status: draft
created: '2026-09-14'
updated: '2026-09-19'
owner: Raymond Bayly (BaylyAI)
review: {trust: unverified, reviewed_by: null, reviewed_at: null, interval: 180d, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: [HATHOR-ADR-003, HATHOR-ADR-004, HATHOR-PLAYBOOK-001, HATHOR-CANON-001]
---
# Agent Integrator Guide

As an Agent Integrator (or AI Agent), you interact with the **HATHOR** platform as an active participant—building, verifying, and navigating project state.

**Operator binary:** `hath0r` (package `hath0r-cli`).  
**Do not** call `aegis`, create `.aegis/`, `.ai/`, or `.infraOS/` for framework metadata (`cr-hath0r-root-001`).

## 0. Shipped vs target surface (read this first)

| Layer | Status (CLI **0.2.x**) | Agent rule |
|-------|------------------------|------------|
| `hath0r --version` / `--help` / `--output json` | **Shipped** | Always prefer JSON envelopes for machine use |
| `hath0r doctor` | **Shipped** (suite-oriented; needs `HATH0R_GROUP_ROOT` for full suite) | Use to verify OpenSource control-tower health |
| `hath0r kb path` / `hath0r kb products` | **Shipped** (read discovery) | Use for KB hub path + suite product list |
| Product bootstrap scripts (`./bin/hath0r-bootstrap.sh`) | **Shipped** on initialized apps | Layout + optional doctor |
| Docs discovery (`docs/index.json`, tree `llms.txt`, `AGENTS.md`) | **Shipped** | Primary corpus navigation |
| `hath0r planes` / `hath0r schema` | **Shipped** | ADR-003 surface map with honest planned status |
| Domains from HATHOR-ADR-003 (`process`, `work`, `knowledge` write, `validate`, `repo`, …) | **Target / not fully shipped in 0.2** | Do **not** invent commands; follow product runbooks and git/host tooling until CLI grows behind contracts |

Private-era text that still says `aegis` is **stale**. Live document IDs are `HATHOR-*`.

## 1. The single control plane

The `hath0r` CLI is the **operator** control plane for orientation, health, and knowledge discovery. You do not talk past it to ad-hoc platform daemons when a CLI command exists.

```sh
hath0r --version
hath0r --output json --version
hath0r --output json doctor          # with HATH0R_GROUP_ROOT for suite
hath0r --output json kb path
hath0r --output json kb products
hath0r --output json planes
hath0r --output json schema --status shipped
```

Use `--output json` (or pipe auto-detection when implemented) for machine-readable envelopes. Canonical response schema: `hath0r.cli.response/1` (pinned under product `contracts/`).

### CLI exit codes (contract target)

Pinned in `contracts/exit-codes.yaml` / product contracts:

| Code | Meaning |
|------|---------|
| `0` | Success (including dry-run and idempotent no-op) |
| `1` | Runtime / internal failure |
| `2` | Usage / validation error |
| `3` | Not found |
| `4` | Auth / permission |
| `5` | Conflict / already exists |
| `6` | Dependency unhealthy |
| `7` | Confirmation required in non-interactive context |

Named non-error data states (`degraded`, etc.) belong in the **envelope**, not by overloading exit `2` (HATHOR-ADR-003).

## 2. Navigating the Universal Project Layout (UPL)

Every HATHOR-initialized project follows UPL:

* **`.hath0r/`** — sole hidden framework root (knowledgebase stub/pointer, future state). **Never** `.hath0r/`, `.ai/`, or `.infraOS/`.
* **`cfg/`** — non-secret product/suite/tower config (`product.yaml`, `suite.yaml`, `knowledge-tower.yaml`, …).
* **`contracts/`** — pinned CLI schemas + exit codes.
* **`AGENTS.md`** — root and nested; resolve **nearest-first**.
* **`docs/`** — runbook, indexes, playbooks/procedures/checklists/reports.
* **`bin/hath0r-bootstrap.sh`** — post-init checks when present.
* **`src/`**, **`lib/`**, **`test/`** or documented test home, **`dist/`** — app layout.

Init gate: **HATHOR-PLAYBOOK-001** / **CR-HATH0R-INIT-001** — playbook + same-tech runbook **before** scaffolding.

Standalone apps (e.g. marketing UXP) keep a **local** `.hath0r/knowledgebase` stub and are **not** listed in suite `kb products` unless promoted.

## 3. Documentation & task gates

1. Discover corpus via `docs/index.json` and per-tree `llms.txt` (framework) plus product `docs/llms.txt` / `INDEX.md` when present.
2. Cite by stable ID (`HATHOR-…` or product `BC-…`); honor `status`, `review.trust`, `stale` (HATHOR-CANON-001).
3. Before multi-step/ops work: if playbook/runbook/procedure/strategy/checklist/report is missing, **create it first** (product procedure pattern; see BC-PROCEDURE-001 on Bayly Consulting UXP as a worked example).
4. Do **not** add `hathor-doc@1` front matter to `AGENTS.md` / `WARP.md`.

## 4. Ticketing, promotion, and mutations (policy now; CLI later)

HATHOR policy still applies even when `hath0r work …` is not shipped:

* Prefer **issue-first** branches: `feature|fix|chore/<issue>-slug` from `development` (group AGENTS).
* **CR-BAI-001** promotion path: `local → development → testing → staging → master (Production)`.
  * PRs into `testing` only from `development`; `staging` from `testing`; `master` from `staging`.
* When ticketing-plane CLI lands, it will be `hath0r work …` (not `aegis work`). Until then use GitHub/Jira hosts per product runbook—do not bypass product quality gates.

## 5. Knowledge plane (today vs target)

**Today (0.2):**

* `hath0r kb path` → canonical group hub (with `HATH0R_GROUP_ROOT`).
* `hath0r kb products` → suite catalog.
* Project tier: files under `.hath0r/knowledgebase/` (often stub README only).

**Target (do not fake commands):**

* Tiered retrieval Project → Machine → Organization → Public.
* Microburst writes; draft → verified only after human review; no auto-promotion.
* Future CLI verbs will be under `hath0r` (historically drafted as `knowledge` domain)—never `.aegis/knowledge/`.

## 6. Runs, playbooks, and governance (target)

Target dispatch is `hath0r process …` / validation domains per HATHOR-ADR-003—**not shipped as a full surface in 0.2**.

Until then:

* Execute hierarchy work from **documented** playbook → runbook → checklist chains in `docs/`.
* Use `--dry-run` / plan-first patterns when a command supports them.
* Read JSON `remediation` fields on refusal; fix and retry.
* Never bypass micro-linters or product `yarn pr` / equivalent Q Gates.

## 7. Quick orientation recipe

```text
1. Read nearest AGENTS.md
2. hath0r --output json --version
3. If product has bin/hath0r-bootstrap.sh → run it
4. Open docs/llms.txt or framework docs/index.json
5. Follow runbook; create missing task docs before large changes
6. Never introduce aegis binary or .aegis/ roots
```
