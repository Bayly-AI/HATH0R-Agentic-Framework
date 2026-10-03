# CLI-first & missing capability offer (framework)

> Issue: #46 · Canonical: [HATH0R-CLI cli-first-rules.md](https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/cli-first-rules.md)  
> Binding agent rule: root `AGENTS.md` (**cr-cli-first-001**)

## Rules

1. **CLI-first** — For connections, MCP, workflows, factories, Docker workflows, KB path, or suite orientation, invoke **`hath0r`** instead of ad-hoc scripts.
2. **Missing capability offer** — If the required connection/MCP/workflow/factory does not exist, do **not** silently improvise. Offer to create/register it and use the original request as the acceptance test.
3. **Docs before code** — Procedure/strategy/playbook/runbook before scaffolding new implementation (see workflow documentation standard).
4. **Session start** — Prefer control-tower checklist:  
   https://github.com/Bayly-AI/HATH0R-CLI/blob/development/docs/governance/checklists/agent-session-start.md

## Example offer language

> The project MCP connection is not registered. I can align `cfg/mcp.servers.json` (project MCP priority 1), validate with `hath0r mcp check`, then re-run your original request as the acceptance test. Proceed?
