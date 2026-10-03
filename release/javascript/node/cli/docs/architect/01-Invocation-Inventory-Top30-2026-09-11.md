---
id: HATHOR-REPORT-002
title: 01 — Top 30 Real `infraos-os` Invocations (Communications)
summary: These are heuristic analytical tags, not a mutually exclusive partition; chain-labelled rows can represent more than one layer.
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
# 01 — Top 30 Real `infraos-os` Invocations (Communications)

**Date:** 2026-09-11  
**CLI:** `infraos-os` 9.3.0 (`/opt/homebrew/bin/infraos-os`)  
**Repo:** Communications (Hera) — `Products/Remediation/Communications`  
**Method:** Union of (1) zsh history frequency, (2) Makefile `$(CLI)` / `infraos-os` references, (3) `.infraOS/workflows/**` command strings, (4) canonical AGENTS.md / README start sequences. Ranked by combined operational importance, not raw count alone.

### Evidence base
| Source | Volume |
|--------|--------|
| Shell history lines containing `infraos-os` | **378** |
| Distinct history command keys (first 3 tokens) | ~45+ with count ≥1 |
| Makefile binding hits | multi-target (orient, secrets, repo refresh, status, connections, workflows, review) |
| Workflow file references | connections/workflows/jira/vectra/mcp-servers/knowledge/dvo heavily |
| Docs canonical | AGENTS start sequence + README orient block |

### HATHOR classification keys
**Hierarchy layer:** Procedure · Strategy · Playbook · Runbook · Workflow · Checklist · (Meta/Utility outside hierarchy)  
**Bot role:** Process-Bot · Proctor-Bot · Operator-Bot · Observation-Bot · Control Tower authority · (Human/Agent direct)

---

## Top 30 inventory

| # | Invocation (normalized) | Primary evidence | Hierarchy layer | Bot role | Why it ranks |
|---|-------------------------|------------------|-----------------|----------|--------------|
| 1 | `infraos-os connections list` | history×10, workflows×8, AGENTS, README | Meta (integration catalog) | Operator-Bot | Universal bootstrap; every orient/agent path |
| 2 | `infraos-os workflows list` | history×6, workflows×5, AGENTS, README | Workflow | Process-Bot | Discovery before run; agent orientation |
| 3 | `infraos-os jira connect` | history×12, workflows×4, AGENTS | Meta (auth plane) | Operator-Bot | Highest human history count; prerequisite for Jira ops |
| 4 | `infraos-os workflows run ai/jira-ticket-linked` | history×7, AGENTS critical rule | Procedure→Workflow | Process-Bot | Ticket-linked agent entry workflow |
| 5 | `infraos-os workflows run devops/dvo-deploy-request` | AGENTS, workflows×2, playbook chain | Procedure→Runbook→Workflow | Process-Bot + Proctor-Bot | Post-PR deploy governance path |
| 6 | `infraos-os secrets doctor` | Makefile, AGENTS pr-ai preflight | Checklist-adjacent gate | Proctor-Bot | Blocks blind pr-ai when SSO/secrets broken |
| 7 | `infraos-os status` / `status --json` / `status -g F -g H` | Makefile, AGENTS preflight | Control-plane posture | Control-Tower | Health of connections/groups before work |
| 8 | `infraos-os orient` / `orient --json` | Makefile×2, README | Procedure (repo orientation) | Process-Bot | Canonical “make orient” backend |
| 9 | `infraos-os connections health` | README | Meta (integration posture) | Operator-Bot + Control-Tower | Deeper than list; slow/noisy today |
| 10 | `infraos-os connections test` / `test-service <name>` | README, AGENTS | Meta | Operator-Bot | Service-level probe (knowmcp, infraos-kb) |
| 11 | `infraos-os agent preflight` | live CLI surface | Procedure gate | Proctor-Bot | Agent readiness check before autonomy |
| 12 | `infraos-os repo refresh` (`--profile default\|ci\|fast`) | Makefile×3, AGENTS | Workflow/Runbook (repo ops) | Process-Bot | Centralized refresh (AD-00R) |
| 13 | `infraos-os knowledge push` / `push-multi` | history, workflows×2 | Knowledge plane (not hierarchy) | Process-Bot | KB sync after work |
| 14 | `infraos-os vectra search knowledgebase …` | workflows×4–6 | Knowledge retrieval | Process-Bot | Agent context retrieval |
| 15 | `infraos-os vectra indices` / `index-kb` | Makefile/docs | Knowledge infra | Process-Bot | Index maintenance |
| 16 | `infraos-os mcp list` / `mcp health` | live ops, workflows | MCP plane | Operator-Bot | Tool transport posture |
| 17 | `infraos-os mcp-servers list` / `health` | workflows×2 | MCP registry | Operator-Bot | Registry vs runtime split (AD-005) |
| 18 | `infraos-os jira issue <KEY>` | history×7+ | External work item | Operator-Bot | Read ticket state |
| 19 | `infraos-os jira create` | history×5, workflows×2 | External mutation | Operator-Bot (+ Proctor) | Create issues/deploy tickets |
| 20 | `infraos-os jira list-projects` | history×6 | External discovery | Operator-Bot | Project lookup |
| 21 | `infraos-os jira transition <KEY>` | history (AMD-1289) | External mutation | Operator-Bot (+ Proctor) | Status changes |
| 22 | `infraos-os teams announce …` | history×10 | External notification | Operator-Bot | Engineering channel announcements |
| 23 | `infraos-os git branch validate` / `create` | history, workflows | Repo governance | Proctor-Bot | Branch naming / Q-gate |
| 24 | `infraos-os review` | Makefile (“Running infraos-os review…”) | Quality gate | Proctor-Bot | Review step in Make |
| 25 | `infraos-os pr validate` / `pr-ai` path | product gates | Checklist/Workflow | Proctor-Bot | PR compliance contract |
| 26 | `infraos-os quality check` / sonar path | gates | Quality | Proctor-Bot | Validation domain |
| 27 | `infraos-os context "Communications …"` | AGENTS #1 start step | Procedure framing | Process-Bot | Intent capture before work |
| 28 | `infraos-os workflows run ai/universal-orientation` | workflows, config | Procedure→Workflow | Process-Bot | Preferred orientation workflow id |
| 29 | `infraos-os playbooks/runbooks/checklists list\|show` | hierarchy surface (dvo-deploy-*) | Playbook/Runbook/Checklist | Process-Bot | Only populated hierarchy chain found |
| 30 | `infraos-os commands inventory` | agent discovery attempts | Meta/manifest | Control-Tower / Agent | Full command manifest (very large) |

---

## Distribution summary

### By hierarchy layer
These are heuristic analytical tags, not a mutually exclusive partition; chain-labelled rows can represent more than one layer.
| Layer | Count in top 30 | Notes |
|-------|-----------------|-------|
| Procedure | 5 | context, orient, jira-ticket-linked, dvo-deploy, universal-orientation |
| Strategy | 0 | `strategies list` exists but **not** in real top usage |
| Playbook | 1 | dvo-deploy-handoff (catalog) |
| Runbook | 1 | dvo-deploy-ticket (catalog) |
| Workflow | 6 | list/run orientation, jira-linked, dvo, refresh |
| Checklist | 2 | secrets doctor / pr validate as *de facto* checklists; dvo checklist catalog |
| Outside hierarchy (integrations/knowledge/notify) | 15 | connections, jira, teams, mcp, vectra, knowledge dominate |

**Finding:** Real usage is **Operator/Process-heavy**, not hierarchy-lifecycle-heavy. The sampled evidence contains only one linked DVO deploy chain.

### By bot role
| Role | Count | Dominant verbs |
|------|-------|----------------|
| Operator-Bot | 11 | connections, jira, teams, mcp |
| Process-Bot | 11 | workflows run/list, orient, knowledge, vectra, hierarchy show |
| Proctor-Bot | 9 | secrets doctor, git branch, review, pr/quality, agent preflight, dvo path |
| Observation-Bot | 0 | No explicit observation/benchmark/retry/token worker path appears in the top 30 |
| Control Tower authority | 3 | status, commands inventory, connections health |

**Note:** the listed role counts sum to 34 because #5, #9, #19, and #21 each map to two listed roles. The alternative “Agent direct” label on #30 is not included in the role totals.

**Finding:** Operator-Bot and Process-Bot jointly dominate the sampled paths. Proctor exists as scattered gates, not one surface. The Control Tower surface is thin, and no explicit Observation-Bot path appears.

---

## Observed hierarchy chain (only one found in the sampled evidence)

```
Playbook:  security-devops/dvo-deploy-handoff
Runbook:   security-devops/dvo-deploy-ticket
Checklist: security-devops/dvo-deploy-ticket
Workflow:  devops/dvo-deploy-request
```

This is the strongest natural spike target for step 4 (runbook run → checklist update).

---

## Human vs agent invocation patterns

| Pattern | Human history | Agent/docs/Make |
|---------|---------------|-----------------|
| Jira connect / issue / transition | Very high | Medium (ticket-linked workflow) |
| teams announce | Very high | Medium (DVO handoff) |
| connections list | High | Critical (start sequence) |
| workflows run specific ids | Medium | Critical |
| secrets doctor / status groups | Low in history | Critical in pr-ai preflight |
| commands inventory | Rare | Attractive to agents, costly |
| playbooks/runbooks/checklists | Rare | Almost unused operationally |

---

## Implications for HATHOR design
1. Any hierarchy UX must **wrap** the already-dominant Operator + Workflow paths, not replace them on day one.
2. Proctor should front the high-risk Operator mutations already in top 30: `jira create/transition`, `teams announce`, deploy workflows, secrets, repo refresh.
3. `commands inventory` must not be the default agent discovery path (see report 05 — ~41k tokens).
4. Promote the DVO triplet as the reference implementation of Procedure→…→Checklist.

---

## Limitations
- History is machine-local (this developer), not fleet-wide; normalized command groups and role counts are not raw invocation-frequency totals.
- Makefile regex captured some prose (“not found”) as false positives; ranking manually cleaned.
- Some agent runs invoke Make targets that wrap CLI; those still count as CLI-backed.
- Token/latency not part of this doc (see 05).
