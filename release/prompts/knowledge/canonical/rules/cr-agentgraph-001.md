# CR-AGENTGRAPH-001: Mandatory AgentGraph Querying & Zero-Prompt-Tax Doctrine

**Classification**: Critical Organizational Invariant (`RULE`)  
**Scope**: Org-wide across all agents and subagents  

---

## 📌 Rule Statement

1. **No Context Stuffing & No Unbounded File Reading (CRITICAL)**:
   Agents, subagents, and workflows must **NEVER** load whole unbounded file trees, full `AGENTS.md` files, or complete rulebooks into prompt context. Use targeted line slices or pre-compiled graph nodes.

2. **Mandatory AgentGraph Retrieval**:
   Always query the **AgentGraph** substrate via CLI (`hath0r agentgraph query "<topic>"`, `hath0r agentgraph route --role <role>`, or `hath0r kb search -q "<topic>"`) to retrieve strictly contextual, scoped, and relevant data, rules, policies, and tool permissions.

3. **Deterministic Tool & Role RBAC**:
   Use `hath0r agentgraph route --role <role> [--tool <tool>]` to deterministically prune unauthorized tools before execution rather than relying on LLM self-governance.
