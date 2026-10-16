# Model Context Protocol (MCP) Configuration Specification

> Product: **HATH0R Agentic Framework & Ecosystem**  
> Rule: **cr-mcp-priority-001**  
> Status: **Canonical Specification**  
> Updated: 2026-10-16

---

## 1. Overview & Core Rules

Hath0r orchestrates multiple Model Context Protocol (MCP) servers providing tool calls, knowledgebase lookups, and specialized actions. Every repository in the Hath0r ecosystem is required to maintain a canonical `.hath0r/mcp.json` configuration file (alongside optional `cfg/mcp.servers.json`) that uses the **Hath0r MCP** engine (`"engine": "hath0r-mcp"`, `"default_provider": "hath0r-mcp"`) by default.

### Canonical Group Hath0r MCP Endpoints (CRITICAL)

Every repository defaults to its group's canonical Hath0r MCP server as Priority #1 (`"scope": "project"`, `"priority": 1`):

| Group | Server ID | Default Base URL | Target Repositories |
|-------|-----------|------------------|---------------------|
| `hath0r-opensource` | `hath0r-mcp` | `https://mcp.hath0r-cli.com` | `/Users/raybayly/Development/OpenSource/*` |
| `bai` | `bai-mcp` | `https://mcp.baylyai.com` | `/Users/raybayly/Development/BAI/*`, `Bayly-AI` websites |
| `ray` | `ray-mcp` | `https://mcp.raymondbayly.com` | `/Users/raybayly/Development/Ray/*`, `Websites/Ray Bayly` |
| `1-nation` | `1-nation-mcp` | `https://mcp.1-nation.com` | `/Users/raybayly/Development/1-Nation/*` |

### Priority Ordering & Resolution Rule (CRITICAL)
- **Configuration Resolution Order**:
  1. `HATH0R_MCP_CONFIG` environment variable override (if set)
  2. `<repo_root>/.hath0r/mcp.json` (canonical per-repository Hath0r MCP file, un-ignored via `!.hath0r/mcp.json`)
  3. `<repo_root>/cfg/mcp.servers.json`
  4. `<group_root>/HATH0R-CLI/cfg/mcp.servers.json`
- **Project Default MCP is ALWAYS Priority #1**:
  - The repository's group default Hath0r MCP server (`hath0r-mcp`, `bai-mcp`, `ray-mcp`, or `1-nation-mcp`) is configured with `scope: "project"` and `priority: 1` in `.hath0r/mcp.json`.
  - Priority resolution strictly follows:
    1. Scope `project` (Priority 1)
    2. Scope `group`
    3. Scope `org`
    4. Scope `tools` / `design` / `user`
    5. Numeric `priority` ascending within matching scope.
- **Zero Secrets**: Secrets, API keys, and credentials must NEVER be placed in `.hath0r/mcp.json` or `cfg/mcp.servers.json`. Use `env_ref` pointing to `/Users/raybayly/Development/.credentials/<service>/.env`.

---

## 2. Configuration Schema (`.hath0r/mcp.json`)

```json
{
  "version": "1.0",
  "engine": "hath0r-mcp",
  "default_provider": "hath0r-mcp",
  "group": "hath0r-opensource",
  "default_server": "hath0r-mcp",
  "description": "Canonical Hath0r MCP configuration for this repository",
  "mcpServers": {
    "hath0r-mcp": {
      "type": "streamable-http",
      "url": "https://mcp.hath0r-cli.com/mcp",
      "engine": "hath0r-mcp",
      "group": "hath0r-opensource",
      "default": true
    }
  },
  "servers": [
    {
      "id": "hath0r-mcp",
      "name": "Hath0rMCP",
      "engine": "hath0r-mcp",
      "scope": "project",
      "group": "hath0r-opensource",
      "priority": 1,
      "enabled": true,
      "transport": "streamable-http",
      "base_url": "https://mcp.hath0r-cli.com",
      "mcp_endpoint": "/mcp",
      "health_endpoint": "/health",
      "ready_endpoint": "/ready"
    }
  ]
}
```

---

## 3. CLI Provisioning, Validation & Doctor Checks

1. **Provisioning & Fleet Sync**:
   - Initialize or refresh a single repository: `hath0r mcp init`
   - Provision and verify across all repositories: `hath0r mcp ensure-all --root /Users/raybayly/Development`
2. **Schema Compliance**: Validated against `contracts/hath0r-mcp-servers-v1.schema.json`.
3. **Gitignore Protection**: `.hath0r/mcp.json` must be explicitly un-ignored (`!.hath0r/mcp.json`) in every repository's `.gitignore`.
4. **Connectivity Probing**: `hath0r mcp check` verifies HTTP endpoints and tool discovery across all enabled servers.

