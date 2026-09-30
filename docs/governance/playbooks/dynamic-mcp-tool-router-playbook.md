# Dynamic MCP Tool Router & Schema Pruning Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#127  
> **Target Subsystem:** `src/hath0r_engine/mcp`

---

## 1. Overview

This playbook describes how to configure, index, and execute dynamic MCP tool routing and schema pruning within Hath0r agent execution loops.

---

## 2. Quickstart

### 2.1 Indexing Tools and Semantic Retrieval

```python
from hath0r_engine.mcp import DynamicToolRouter, PruningMode, CallerIdentity

# 1. Initialize router and register tools
router = DynamicToolRouter()
router.register_tool(
    server_id="github-mcp",
    name="create_issue",
    description="Creates a new issue in a GitHub repository with title, body, and labels.",
    parameters={
        "type": "object",
        "properties": {
            "repo": {"type": "string", "description": "Repository in owner/name format"},
            "title": {"type": "string", "description": "Title of the issue"},
            "body": {"type": "string", "description": "Markdown body content"},
        },
        "required": ["repo", "title"],
    },
)

# 2. Retrieve top-k tools for a prompt
selected_tools = router.route_tools("file a bug report on the auth module", top_k=3)

# 3. Prune schemas for LLM injection
pruned_schemas = router.get_pruned_tools_for_llm(
    query="file a bug report on the auth module",
    mode=PruningMode.STANDARD,
    top_k=3,
)
```

### 2.2 Telemetry & Token Optimization Inspection

```python
stats = router.get_telemetry_summary()
print(f"Total tokens saved: {stats['total_tokens_saved']}")
print(f"Average token reduction: {stats['avg_reduction_pct']}%")
```
