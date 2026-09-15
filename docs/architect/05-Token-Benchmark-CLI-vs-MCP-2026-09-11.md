---
id: AEGIS-REPORT-005
title: '05 — Token / Payload Baseline: `infraos-os`, InfraMCP Health, and MCP Catalog Proxies'
summary: 1. Not a multi-run statistical benchmark (n=1 per command).
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
# 05 — Token / Payload Baseline: `infraos-os`, InfraMCP Health, and MCP Catalog Proxies

**Date:** 2026-09-11  
**Environment:** Communications repo; `infraos-os` 9.3.0; local InfraMCP `:3001` healthy; KnowMCP `:48080` **unreachable** during run  
**Method:** Wall-clock latency + output size; **token estimate = `floor(chars/4)`** (rough UTF-8 proxy, not a billable tokenizer). This measures return-payload size, not full LLM turns, tool-schema preload, input tokens, or billable usage. It is **not** a controlled head-to-head CLI-vs-MCP benchmark because no equivalent MCP path was available for most tasks.

### Important caveats
1. Not a multi-run statistical benchmark (n=1 per command).  
2. KnowMCP HTTP search could not be compared live (connection failure). A prior local observation reported a missing `vectra-orientation` index, but this run did not independently validate that root cause.  
3. `infraos-os mcp list` is the closest local proxy for “MCP tool catalog tax.”  
4. Industry MCP-vs-CLI studies measure full agent sessions with schema injection; these local numbers are only **lower-bound payload sizes** for the paths that could be measured.

---

## 1. Five intended comparison tasks

| ID | Task (agent intent) | CLI modality | MCP/HTTP modality |
|----|---------------------|--------------|-------------------|
| T1 | Health / version posture | `infraos-os --version`, `mcp health` | `GET InfraMCP /health`, `GET KnowMCP /health` |
| T2 | Integrations posture | `connections list/health`, `mcp list`, `mcp-servers list` | MCP catalog via `mcp list` (proxy) |
| T3 | Knowledge discovery | `knowledge list`, `vectra indices`, `vectra search -n 5` | KnowMCP search (unavailable) |
| T4 | Workflow inventory | `workflows list` | n/a local MCP tool equivalent |
| T5 | Agent readiness | `agent preflight`, `orient --json`, `status --json`, `commands inventory` | n/a (CLI control plane) |

---

## 2. Raw measurements

| Task | Modality | Command | rc | secs | chars | est_tokens |
|------|----------|---------|----|------|-------|------------|
| T1 | CLI | `infraos-os --version` | 0 | 0.50 | 17 | **4** |
| T1 | CLI | `infraos-os mcp health` | 0 | 0.35 | 79 | **19** |
| T1 | HTTP-InfraMCP | `GET :3001/health` | 200 | 0.01 | 246 | **61** |
| T1 | HTTP-KnowMCP | `GET :48080/health` | -1 | 0.00 | 45 | 11 (error) |
| T2 | CLI | `connections list` | 0 | 0.33 | 330 | **82** |
| T2 | CLI | `connections health` | 1 | 3.93 | 5053 | **1263** |
| T2 | CLI | `mcp list` | 0 | 0.36 | 11246 | **2811** |
| T2 | CLI | `mcp-servers list` | 0 | 0.36 | 198 | **49** |
| T3 | CLI | `knowledge list` | 0 | 0.43 | 2700 | **675** |
| T3 | CLI | `vectra indices` | 0 | 0.33 | 86 | **21** |
| T3 | CLI | `vectra search -n 5 …` | 0 | 0.40 | 700 | **175** |
| T4 | CLI | `workflows list` | 0 | 0.34 | 2430 | **607** |
| T5 | CLI | `agent preflight` | 1 | 0.74 | 3236 | **809** |
| T5 | CLI | `orient --json` | 0 | 1.93 | 2865 | **716** |
| T5 | CLI | `status --json` | 2 | 1.33 | 6952 | **1738** |
| T5 | CLI | `commands inventory` | 1 | 0.43 | 164817 | **41204** |

---

## 3. Task-level synthesis

### T1 — Health / version
| Approach | Tokens | Latency | Notes |
|----------|--------|---------|-------|
| CLI version | 4 | 0.5s | Cheapest possible |
| CLI mcp health | 19 | 0.35s | Concise |
| InfraMCP HTTP health | 61 | **0.01s** | Fastest; slightly larger JSON |
| KnowMCP HTTP | fail | — | Service down / wrong port |

**Result for this run:** CLI health/version calls succeeded and were compact; InfraMCP HTTP health was fastest; KnowMCP was unavailable. With n=1 and non-equivalent paths, this is not a general reliability ranking.  
**Agent guidance:** prefer `infraos-os mcp health` + `infraos-os --version` over loading any tool schema.

### T2 — Integrations posture
| Approach | Tokens | Latency | Notes |
|----------|--------|---------|-------|
| connections list | 82 | 0.33s | Good default |
| mcp-servers list | 49 | 0.36s | Registry only |
| connections health | 1263 | 3.93s | Verbose + slow; rc=1 |
| mcp list | **2811** | 0.36s | **Catalog tax** |

**Leanest posture pair:** CLI `connections list` + `mcp-servers list` (~131 tokens combined) versus the CLI-exposed `mcp list` catalog proxy (~2811).  
**Ratio:** `mcp list` is **~21.5×** heavier than the combined 131-token posture pair; it is **34.3×** heavier than `connections list` alone.  
This demonstrates local catalog-payload cost. It does not measure MCP tool-definition preload and therefore cannot, by itself, validate an industry “MCP schema tax” claim.

### T3 — Knowledge
| Approach | Tokens | Latency |
|----------|--------|---------|
| vectra indices | 21 | 0.33s |
| vectra search top5 | 175 | 0.40s |
| knowledge list | 675 | 0.43s |
| KnowMCP search | n/a | failed ecosystem |

**Measured result:** local CLI vectra search was the smallest targeted retrieval path.  
**Note:** `knowledge list` is 3.9× the top-five search payload. No live KnowMCP result was available, so there is no cross-modality winner.

### T4 — Workflows
| Approach | Tokens | Latency |
|----------|--------|---------|
| workflows list | 607 | 0.34s |

Acceptable. Needs JSON + `--limit` (report 02) to stay bounded as workflow count grows.

### T5 — Agent readiness
| Approach | Tokens | Latency | rc |
|----------|--------|---------|-----|
| agent preflight | 809 | 0.74s | 1 |
| orient --json | 716 | 1.93s | 0 |
| status --json | 1738 | 1.33s | 2 |
| **commands inventory** | **41204** | 0.43s | 1 |

**Combined sensible readiness pack:** preflight + orient ≈ **1525 tokens**, 2.7s.  
**Inventory mistake:** +41k tokens for discovery — **~27×** the readiness pack.

---

## 4. Comparative ratios (payload)

| Comparison | Lighter | Heavier | Factor |
|------------|---------|---------|--------|
| connections list vs mcp list | 82 | 2811 | **34.3×** |
| mcp-servers list vs mcp list | 49 | 2811 | **57.4×** |
| orient+preflight vs commands inventory | 1525 | 41204 | **27.0×** |
| vectra search top5 vs knowledge list | 175 | 675 | **3.9×** |
| CLI mcp health vs InfraMCP HTTP health | 19 | 61 | 3.2× (HTTP larger body) |

---

## 5. Comparison with published MCP-vs-CLI findings

External comparison source: [ScaleKit's 75-run MCP-vs-CLI benchmark](https://www.scalekit.com/blog/mcp-vs-cli-use). Its GitHub/Claude Sonnet 4 setup is not equivalent to this local InfraOS payload run.

| Published claim | What this local baseline does or does not show |
|-----------------|----------------------------------------------|
| Large schemas/catalogs consume context | Consistent at the payload level: `mcp list` is 2.8k tokens and command inventory 41k; schema preload itself was not measured |
| CLI is efficient for familiar local/dev tools | Measured CLI paths were compact and fast, but equivalent MCP task paths were unavailable |
| MCP helps with remote SaaS auth/governance | Not tested; KnowMCP was unavailable |
| Use a hybrid architecture | Qualitatively compatible, but this run establishes no fixed CLI/MCP ratio |
| CLI+Skills avoids bulk discovery | An ~800-token skill document would be ~50× smaller than the 41k inventory payload before task output; end-to-end agent sessions were not measured |

---

## 6. Agent playbook (recommended defaults)

```text
# Cheap orientation pack (~1.5–2.5k tokens of tool output)
infraos-os --version
infraos-os agent preflight --json          # non-zero when readiness checks fail
infraos-os orient --json
infraos-os connections list                # NOT health unless needed
infraos-os mcp-servers list                # NOT mcp list
infraos-os workflows list                  # then describe one id
infraos-os vectra search -n 5 knowledgebase "<query>"

# Avoid by default
infraos-os commands inventory              # 41k tokens
infraos-os mcp list                        # 2.8k tool dump
infraos-os connections health              # unless diagnosing; 1.2k + 4s
infraos-os status --json                   # unless tower posture required
```

---

## 7. Implications for AEGIS design

1. **Operator-Bot list endpoints must stay tiny** — connections list is the gold pattern.  
2. **Tower inventory must be domain-filtered** — never default full command dump.  
3. **MCP plane is complementary**, but `mcp list` is not a posture API; split `mcp health` (tiny) from `mcp tools catalog` (heavy, paginated).  
4. **Process-Bot workflow list** should grow JSON+limit before workflow count explodes.  
5. Fix KnowMCP (port + `vectra-orientation` index) before any fair remote KB benchmark v2.

---

## 8. Proposed benchmark v2 (when KnowMCP healthy)

| Task | CLI | MCP |
|------|-----|-----|
| Search “orientation” | vectra search | kb_search |
| Fetch compliance report meta | knowledge show | kb get |
| List integrations | connections list | tools/list filtered |
| Full agent session: orient repo | skill+CLI | MCP tool soup |

Measure: input tokens (schemas) + output tokens + wall time + success rate over 10 runs.

---

## 9. Bottom line

For the five local control-plane tasks sampled from Communications agent bootstrap, measured CLI payloads were generally compact, except for **catalog dumps** (`mcp list`, `commands inventory`) and **verbose diagnostics** (`connections health`, fat `status --json`).

The highest-ROI AEGIS/CLI Spec moves are therefore:
1. Prevent catalog dumps as defaults.  
2. Add bounded schema domains (spike 04).  
3. Ship a short agent skill for the top 15 commands (report 01).  
4. Restore KnowMCP, define semantically equivalent task outputs, and run multiple trials before claiming CLI/MCP parity or superiority.

**Rough cost narrative:** an agent that runs the “sensible readiness pack” once pays ~1.5k output tokens; an agent that also dumps inventory pays ~43k — before it does any real work.
