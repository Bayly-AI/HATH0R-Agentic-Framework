# PROMPT TICKET 05: AgentGraph, MemoryGraph & Cognitive Substrate Wiring

**Ticket ID**: `HATH0R-RELEASE-005`  
**Role**: `CognitiveSubstrateArchitectAgent`  
**Scope**: Initialize `.hath0r/agentgraph/` and `.hath0r/memory/`, establish rule DAG, Letta memory paging, and AI Gateway router  

---

## 🎯 Task Objective

Integrate the **Hath0r Cognitive Substrate** with the newly deployed infrastructure. This wires the Operator CLI, MCP Server, and ATC Control Tower with the quad-graph architecture:
1. **KnowledgeGraph**: Static contracts, schemas, and specifications.
2. **ContextGraph**: Dynamic session state and span lineages.
3. **MemoryGraph**: Long-term temporal entity nodes and Letta-compatible memory paging.
4. **RulesGraph**: Deterministic rule inheritance DAG and tool RBAC pruning.

---

## 📥 Inputs & Dependencies

- **Hath0r CLI**: Deployed in Ticket 02 (`hath0r`).
- **MCP Server**: Deployed in Ticket 03 (`http://127.0.0.1:38083`).
- **ATC Control Tower**: Deployed in Ticket 04 (`http://127.0.0.1:38000`).
- **Target Substrate Directory**: `${HATH0R_HOME}/.hath0r/`.

---

## 🛠️ Execution Steps

### Step 1: Initialize MemoryGraph Structure (`CR-MEMORY-COMPOUND-001`)
Create the mandatory memory repository layout:
```bash
MEM_DIR="${HATH0R_HOME}/.hath0r/memory"
mkdir -p "${MEM_DIR}/sessions"

# Initialize memory graph if absent
if [[ ! -f "${MEM_DIR}/graph.json" ]]; then
  cat <<EOF > "${MEM_DIR}/graph.json"
{
  "version": "1.0",
  "schema_version": "1.0.0",
  "repository": "hath0r-release-infrastructure",
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "nodes": [
    {
      "id": "node-release-manifest",
      "type": "fact",
      "title": "Hath0r Infrastructure Release Fabric",
      "content": "Full Hath0r stack deployed with CLI, MCP, and ATC components.",
      "tags": ["release", "infrastructure", "active"],
      "confidence": 1.0
    }
  ],
  "edges": []
}
EOF
fi

# Initialize SHA-256 CAS hash registry
cat <<EOF > "${MEM_DIR}/hashes.json"
{
  "version": "1.0",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "files": {}
}
EOF
```

### Step 2: Initialize AgentGraph Snapshot & Substrate Route
Create the AgentGraph deployment snapshot under `${HATH0R_HOME}/.hath0r/agentgraph/snapshot.json`:
```json
{
  "version": "1.0",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "HEALTHY",
  "routes": {
    "cli": "hath0r",
    "mcp": "http://127.0.0.1:38083",
    "atc": "http://127.0.0.1:38000",
    "sessions": "redis://127.0.0.1:6379"
  },
  "rbac": {
    "default_role": "OperatorAgent",
    "pruning_policy": "deterministic"
  }
}
```

### Step 3: Verify Substrate Health via CLI
Execute Hath0r CLI memory and agentgraph commands:
```bash
# Start micro memory session
hath0r memory session start --task "release-integration-validation"

# Query agentgraph status
hath0r agentgraph status || true

# Verify memory graph integrity
hath0r memory hash verify || true
```

---

## ✅ Acceptance Criteria & Assertions

1. `.hath0r/memory/graph.json` and `.hath0r/memory/hashes.json` exist and validate.
2. `.hath0r/agentgraph/snapshot.json` contains active routes for CLI, MCP, and ATC.
3. `hath0r memory session start` completes successfully with size < 2048 bytes.
4. AgentGraph deterministic RBAC router prunes unauthorized tools prior to LLM dispatch.
