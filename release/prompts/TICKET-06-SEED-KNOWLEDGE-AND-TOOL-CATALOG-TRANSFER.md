# PROMPT TICKET 06: Seed Knowledge & Tool Catalog Transfer

**Ticket ID**: `HATH0R-RELEASE-006`  
**Role**: `KnowledgeArchitectAgent`  
**Scope**: Hydrate the basic set of canonical knowledge, tool specifications, schemas, and runbooks into Hath0r MCP, CLI, and ATC  

---

## 🎯 Task Objective

An Operator running solely from the `release/prompts/` folder must be able to populate the entire Hath0r infrastructure with the **basic set of canonical knowledge and tool definitions**.

This ticket transfers the bundled knowledge pack (`release/prompts/knowledge/`) into:
1. **Hath0r MCP**: As the authoritative knowledgebase directory, triggering full indexing so semantic tools (`kb_search`, `docs_read_content`, etc.) work immediately out of the box.
2. **Hath0r CLI**: Seed concept, rule, and fact nodes compounded into `.hath0r/memory/graph.json`.
3. **Hath0r ATC**: Runbook registry and routing configurations.

---

## 📥 Inputs & Sources

- **Knowledge Pack Source**: `${PROMPTS_ROOT}/knowledge/`
  - `tools/`: Tool catalogs for CLI, MCP (all 42 tools), and ATC
  - `contracts/`: JSON schemas (`hath0r-cli-response-v1`, `hath0r-mcp-servers-v1`, `hath0r-agentgraph-v1`, `exit-codes.yaml`)
  - `canonical/`: Architecture docs, core rules, runbooks, and strategies
- **MCP Destination**: `${HATH0R_HOME}/knowledgebase/canonical/` (mounted into `Hath0r-MCP`)
- **CLI Destination**: `${HATH0R_HOME}/.hath0r/memory/` and `${HATH0R_HOME}/contracts/`
- **ATC Destination**: `${HATH0R_HOME}/cfg/` and runbook registry

---

## 🛠️ Execution Steps

### Step 1: Copy Canonical Knowledge to MCP Mount
Transfer all canonical architecture, rules, runbooks, and strategies into the MCP knowledge directory:
```bash
PROMPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KNOWLEDGE_SRC="${PROMPTS_DIR}/knowledge"
MCP_KB_DIR="${HATH0R_HOME}/knowledgebase/canonical"

mkdir -p "${MCP_KB_DIR}"
cp -R "${KNOWLEDGE_SRC}/canonical/"* "${MCP_KB_DIR}/"
cp -R "${KNOWLEDGE_SRC}/tools/"* "${MCP_KB_DIR}/"
echo "✓ Hydrated canonical knowledgebase at ${MCP_KB_DIR}"
```

### Step 2: Trigger MCP Knowledgebase Re-Index
Notify the running Hath0r-MCP container to index the newly transferred knowledge:
```bash
if docker ps --format '{{.Names}}' | grep -q "Hath0r-MCP"; then
  echo "Indexing canonical knowledge inside Hath0r-MCP container..."
  docker exec Hath0r-MCP python -m knowledgebase.cli.main sync --force || true
  echo "✓ Knowledge indexing complete"
else
  echo "Hath0r-MCP container not running; files staged for container boot."
fi
```

### Step 3: Install Canonical Contracts & Schemas
Copy schema contracts to the active workspace:
```bash
TARGET_CONTRACTS="${HATH0R_HOME}/contracts"
mkdir -p "${TARGET_CONTRACTS}"
cp -R "${KNOWLEDGE_SRC}/contracts/"* "${TARGET_CONTRACTS}/"
echo "✓ Installed canonical contracts under ${TARGET_CONTRACTS}"
```

### Step 4: Seed Initial MemoryGraph Nodes (`CR-MEMORY-COMPOUND-001`)
Seed the memory graph with the transferred tool catalogs and core invariants:
```bash
hath0r memory compound \
  --id "concept:hathor-tools-catalog" \
  --type "concept" \
  --label "Hath0r Unified Tool Catalog" \
  --content "Seed tool definitions for Hath0r CLI, Hath0r MCP (42 tools), and Hath0r ATC Control Tower." \
  --tags "tools,catalog,cli,mcp,atc"

hath0r memory compound \
  --id "rule:cr-cli-entry-001" \
  --type "rule" \
  --label "CR-CLI-ENTRY-001: Start with CLI" \
  --content "Agents must always start with operator CLI (hath0r) and adhere to Artifact Hexad." \
  --tags "rule,governance,cli-first"
```

---

## ✅ Acceptance Criteria & Assertions

1. Canonical knowledge directory contains `INDEX.md`, architecture, rules, runbooks, and strategies.
2. Hath0r MCP `/ready` and `/health` endpoints are operational.
3. Schemas in `${HATH0R_HOME}/contracts/` validate against JSON schema draft-2020-12.
4. MemoryGraph in `${HATH0R_HOME}/.hath0r/memory/graph.json` contains seeded tool catalog and rule nodes.
