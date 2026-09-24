# JEV (System One) — portable reference

Canonical copies of the AegisCMCP JEV tool-guard client for reuse across Hath0r / BAI / 1-Nation.

| File | Purpose |
|------|---------|
| `jev_client.py` | Settings, stub/live HTTP client, tool-guard parsing |
| `jev_tool_guard.py` | Mutating MCP tool risk catalog + evaluate/format |
| `jev.json` | Operator reference config |

## Consumers

- `BAI/MCP` — production hook in `_execute_mcp_tool`
- `OpenSource/hath0r-mcp` — same hook + FastMCP `suite_info` / `kb_search` metadata
- `1-Nation/MCP` — same as hath0r-mcp

## Enable

```bash
export JEV_MODE=stub   # offline
# or
export JEV_MODE=live
export JEV_API_KEY=... # or TYPESAFE_API_KEY
```

Default remains `off`. See each MCP `docs/jev-tool-guard-poc.md`.
