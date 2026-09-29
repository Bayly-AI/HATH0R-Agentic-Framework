# CR-CLI-ENTRY-001: Start with the CLI (CRITICAL — Org-Wide & Suite-Wide)

> **Rule ID:** `CR-CLI-ENTRY-001` (also tracked as `cr-cli-first-001`)  
> **Status:** RATIFIED & MANDATORY ENTRY GATE  
> **Applies to:** All Agents, Workflows, Subagents, and Automation Scripts across HATH0R OpenSource & Enterprise Products.  
> **Effective Date:** 2026-09-28  

---

## 1. Main Entry Statement (CRITICAL ENTRY GATE)

> **Upon receiving ANY user request or initializing any task, agents MUST ALWAYS START WITH THE OPERATOR CLI (`hath0r`).**
>
> Ad-hoc shell scripting, direct file mutation without CLI discovery, or inventing custom pipelines when a canonical `hath0r` CLI subcommand, factory, bot, workflow, or MCP endpoint exists (or can be registered) is **STRICTLY FORBIDDEN**.

---

## 2. Core Directives

1. **CLI as Primary Operating Substrate:**
   - Always query, validate, inspect, and execute through `hath0r <subcommand>` (e.g. `hath0r kb ...`, `hath0r doctor`, `hath0r factory ...`, `hath0r workflow ...`, `hath0r mcp ...`, `hath0r context ...`).
   - The CLI is the control tower interface guaranteeing audit trails, JEV security validation, schema contract compliance, and telemetry recording.

2. **Missing Capability Offer (No Silent Improvisation):**
   - If the required command, workflow, connection, or factory does not exist in `hath0r`, agents **MUST NOT** silently invent non-standard scripts.
   - Agents must explicitly offer to build/register the missing capability in `hath0r` / `hath0r_cli`, and use the user's original request as the immediate acceptance test.

3. **Docs Before Code (Governance Chain):**
   - Before scaffolding new CLI capabilities or framework code, verify or establish the governance documentation chain:  
     `Procedure → Strategy → Playbook → Runbook → Checklist → Factory/Bot`.

4. **Structured Output & Contract Verification:**
   - Commands should leverage structured CLI payloads (`--format json`, contracts under `contracts/hath0r-*.schema.json`) for machine consumption.

---

## 3. Enforcement & Verification

- **Bootstrap Enforcement:** Every repository's `./bin/hath0r-bootstrap.sh` verifies `hath0r` availability and exit status `0`.
- **Pre-Execution Check:** Agents must check `hath0r --version` and relevant subsystem command availability before initiating deeper operations.
- **CI / Quality Gate:** PRs introducing workflows or automation that bypass `hath0r` CLI commands will fail the governance audit gate.
