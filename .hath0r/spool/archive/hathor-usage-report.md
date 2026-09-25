# Hath0r Framework Usage Report

**Scan root:** `/Users/raybayly/Development`  
**Generated:** 2026-09-23  
**Method:** Enumerated git repos under Development; classified by `.hath0r/` presence, Hath0r layout markers (`cfg`, `AGENTS.md`, `contracts`, bootstrap scripts), and explicit framework/CLI references.

## Executive summary

- **11 git repositories** were found under Development.
- **8 repos** are using or implementing the Hath0r Framework:
  - **4 product/consumer repos** (mostly UXP apps)
  - **4 OpenSource ecosystem components** (ATC, MCP, POC, CLI)
- **3 repos** share Hath0r-adjacent layout but are **not fully adopted** (no `.hath0r/`).
- The canonical framework root `OpenSource/hath0r` exists but is **empty** (not a git repo / no checked-out corpus).

## Repositories inventory

| Path | Git repo? | Hath0r status |
|------|-----------|---------------|
| `OpenSource/hath0r` | No (empty dir) | Intended framework root; not populated |
| `OpenSource/hath0r-atc` | Yes | Framework ecosystem |
| `OpenSource/hath0r-mcp` | Yes | Framework ecosystem |
| `OpenSource/hath0r-poc` | Yes | Framework ecosystem |
| `OpenSource/hathor-cli` | Yes | Framework ecosystem (operator CLI) |
| `1-Nation/UXP` | Yes | Consumer — full adoption |
| `1-Nation/ATC` | Yes | Adjacent — not fully adopted |
| `1-Nation/MCP` | Yes | Adjacent — not fully adopted |
| `BAI/UXP` | Yes | Consumer — full adoption |
| `BAI/UXP/BAI-BaylyAI` | Yes | Consumer — full adoption (nested) |
| `BAI/MCP` | Yes | Adjacent — not fully adopted |
| `Websites/bayly-consulting/UXP` | Yes | Consumer — full adoption |
| `Websites/doctor-sleep` | No | Not using Hath0r |
| `Websites/knithappens` | No | Not using Hath0r |
| `Websites/docs` | No | Not using Hath0r |
| `BAI/docs` | No | Not using Hath0r |

## Using the Hath0r Framework

### Product / consumer repos

These have a `.hath0r/` directory plus framework conventions (contracts, bootstrap, KB/docs wiring).

| Repo | Evidence |
|------|----------|
| `1-Nation/UXP` | `.hath0r/`, contracts, `hath0r-bootstrap.sh`, knowledgebase/docs |
| `BAI/UXP` | `.hath0r/`, contracts, bootstrap, framework references |
| `BAI/UXP/BAI-BaylyAI` | Nested app under BAI/UXP with the same Hath0r markers |
| `Websites/bayly-consulting/UXP` | `.hath0r/`, contracts, bootstrap |

### Framework ecosystem repos

These implement or support the Hath0r stack rather than being end-product apps alone. Docs consistently point at `../hath0r` as the canonical framework/docs root and at `hathor-cli` for the `hath0r` operator CLI.

| Repo | Role |
|------|------|
| `OpenSource/hath0r-atc` | Control-tower / ATC for the framework |
| `OpenSource/hath0r-mcp` | MCP server for the framework |
| `OpenSource/hath0r-poc` | Agentic POC built on the framework |
| `OpenSource/hathor-cli` | Operator CLI (`hath0r doctor`, KB commands, etc.) |

## Related layout, not fully on Hath0r

These share some Hath0r-style structure (`cfg`, `AGENTS.md`, docs) but **lack `.hath0r/`** and have little or no active framework initialization.

| Repo | Notes |
|------|-------|
| `1-Nation/ATC` | Docs mention Hath0r requirements and patterns; not initialized with `.hath0r/` |
| `1-Nation/MCP` | Generic layout markers only; no meaningful Hath0r wiring found |
| `BAI/MCP` | Some tooling awareness of `.hath0r` paths; not initialized as a Hath0r app |

## Not using Hath0r

- `OpenSource/hath0r` — empty placeholder for the framework corpus
- `Websites/doctor-sleep`
- `Websites/knithappens`
- `Websites/docs`
- `BAI/docs`

## Classification signals used

A repo was treated as **using Hath0r** when it showed strong signals such as:

- Presence of `.hath0r/`
- Hath0r bootstrap scripts (e.g. `hath0r-bootstrap.sh`)
- Contracts/schemas tied to `hath0r-cli`
- Explicit references to the HATH0R / Hath0r Framework, `OpenSource/hath0r`, or `hath0r doctor`
- Shared control-tower style markers (`cfg`, `AGENTS.md`, `WARP.md`, docs/KB layout) **in combination with** the above

Layout-only markers without `.hath0r/` or framework wiring were classified as **adjacent**, not full adoption.

## Bottom line

**8 repositories** under Development are on the Hath0r Framework:

1. `1-Nation/UXP`
2. `BAI/UXP`
3. `BAI/UXP/BAI-BaylyAI`
4. `Websites/bayly-consulting/UXP`
5. `OpenSource/hath0r-atc`
6. `OpenSource/hath0r-mcp`
7. `OpenSource/hath0r-poc`
8. `OpenSource/hathor-cli`

**3** MCP/ATC siblings (`1-Nation/ATC`, `1-Nation/MCP`, `BAI/MCP`) are Hath0r-adjacent but not fully adopted. The intended framework corpus at `OpenSource/hath0r` is not checked out yet.
