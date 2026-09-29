---
id: cfg-subsystem
type: subsystem
title: Configuration Subsystem
depends_on: [contracts-subsystem]
governed_by: [cr-branch-gov-001, CR-CLI-ENTRY-001]
---
# Configuration Subsystem — AGENTS Context

> **Subsystem Role:** Declarative product, suite, observability, and knowledge tower configuration.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`cfg/knowledge-tower.yaml`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/cfg/knowledge-tower.yaml): Knowledge tower location and KnowledgeGraph/ContextGraph engine configuration.
- [`cfg/mcp.servers.json`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/cfg/mcp.servers.json): Configured MCP server endpoints.
- [`cfg/suite.yaml`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/cfg/suite.yaml): Suite orientation and group definitions.

## 2. Constraints & Rules
- Do not store raw secrets or bearer tokens in `cfg/`.
- Maintain canonical pointers to `HATH0R-CLI` control tower.
