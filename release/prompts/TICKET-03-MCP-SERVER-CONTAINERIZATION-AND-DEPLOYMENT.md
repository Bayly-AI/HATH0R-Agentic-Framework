# PROMPT TICKET 03: Hath0r MCP Server Containerization & Tool Registration

**Ticket ID**: `HATH0R-RELEASE-003`  
**Role**: `MCPEngineerAgent`  
**Scope**: Build/deploy the hardened Hath0r MCP server container, mount canonical knowledgebase, join `hath0r-net`, and register MCP tool configuration  

---

## 🎯 Task Objective

Build and launch the **Hath0r MCP (Model Context Protocol)** server release. The server exposes canonical knowledgebase search, documentation retrieval, and infrastructure tools. It runs as a hardened non-root container attached to `hath0r-net` on port `38083` (internal `8083`).

---

## 📥 Inputs & Source Resolution

- **MCP Repository URL / Path**: Obtained from Ticket 01 (`MCP_REPO` or monorepo `UNIFIED_REPO/mcp`).
- **Network Bridge**: `hath0r-net` (established in Ticket 01).
- **Target Host Port**: `38083` (`HATH0R_MCP_HOST_PORT`).
- **Canonical Knowledgebase Path**: Mounted into container at `/app/knowledgebase/canonical:ro`.

---

## 🛠️ Execution Steps

### Step 1: Package Hardened MCP Container Image
Inspect the MCP source repository or packaging manifest:
```bash
cd "${MCP_SOURCE_DIR}"

# Build hardened container image with immutable tags
docker build \
  --build-arg GIT_SHA="$(git rev-parse --short HEAD 2>/dev/null || echo 'release')" \
  --build-arg BUILD_TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  -t hath0r/mcp:release \
  -f Dockerfile .
```

### Step 2: Deploy Container on `hath0r-net`
Run container adhering to Hath0r container standards (`CR-IAC-001`):
- Run as non-root user
- Read-only root filesystem with tmpfs `/tmp`
- Dropped all capabilities (`cap_drop: [ALL]`)
- Attached to network `hath0r-net`
- Explicit healthcheck on `/ready`

```bash
docker rm -f Hath0r-MCP >/dev/null 2>&1 || true

docker run -d \
  --name Hath0r-MCP \
  --network hath0r-net \
  --network-alias hath0r-mcp \
  --network-alias mcp \
  --restart unless-stopped \
  -p "127.0.0.1:38083:8083" \
  --read-only \
  --tmpfs /tmp \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --memory 512m \
  --cpus 1.0 \
  -v "${MCP_SOURCE_DIR}/knowledgebase:/app/knowledgebase:ro" \
  -e HATH0R_MCP_ENVIRONMENT=release \
  -e HATH0R_MCP_KNOWLEDGE_ROOT=/app/knowledgebase \
  hath0r/mcp:release
```

### Step 3: Register MCP Server Configuration
Create the client-facing MCP server configuration conforming to `contracts/hath0r-mcp-servers-v1.schema.json` under `${HATH0R_HOME}/cfg/mcp.servers.json`:
```json
{
  "version": "1.0",
  "engine": "hath0r-mcp",
  "default_provider": "hath0r-mcp",
  "group": "hath0r-opensource",
  "default_server": "hath0r-mcp",
  "servers": [
    {
      "id": "hath0r-mcp",
      "name": "Hath0rMCP",
      "engine": "hath0r-mcp",
      "scope": "project",
      "group": "hath0r-opensource",
      "priority": 1,
      "product_id": "hath0r-mcp",
      "transport": "streamable-http",
      "base_url": "http://127.0.0.1:38083",
      "mcp_endpoint": "/mcp",
      "health_endpoint": "/health",
      "ready_endpoint": "/ready",
      "description": "Hath0r OpenSource Suite MCP knowledge server and tools (Project MCP)",
      "enabled": true,
      "local_path": "${MCP_SOURCE_DIR}"
    }
  ]
}
```

### Step 4: Validate MCP Readiness Probes
```bash
# Verify ready probe
curl -fsS "http://127.0.0.1:38083/ready"

# Verify health probe
curl -fsS "http://127.0.0.1:38083/health"
```

---

## ✅ Acceptance Criteria & Assertions

1. `Hath0r-MCP` container is running and healthy on Docker network `hath0r-net`.
2. HTTP probe to `http://127.0.0.1:38083/ready` returns HTTP 200 with status `ok`.
3. Configuration file `${HATH0R_HOME}/cfg/mcp.servers.json` validates against schema.
4. MCP tools (`kb_search`, `docs_read_content`, `infraos_context`) are discoverable.
