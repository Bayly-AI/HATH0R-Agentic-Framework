# CR-AGENTGRAPH-001: Mandatory AgentGraph Querying & Zero-Prompt-Tax Context Retrieval (CRITICAL — Org-Wide)

> **Rule ID:** `CR-AGENTGRAPH-001` (incorporates and supersedes legacy `CR-RAG-RETRIEVAL-001`)  
> **Status:** RATIFIED & MANDATORY RUNTIME INVARIANT  
> **Applies to:** All Agents, Workflows, Subagents, Bots, and Autonomous Automation Scripts across HATH0R OpenSource & Enterprise Products.  
> **Effective Date:** 2026-10-03  

---

## 1. Main Entry Statement (CRITICAL INVARIANT)

> **Agents, subagents, and automated workflows MUST NEVER load entire `AGENTS.md` files, full rulebooks, or unbounded knowledgebase directory trees directly into prompt context.**
>
> All retrieval of rules, governance policies, role constraints, tool authorizations, and contextual knowledge **MUST ROUTE THROUGH THE AGENTGRAPH SUBSTRATE** via the `hath0r agentgraph` CLI control plane.

Raw text dumps, full file scans, and probabilistic context-stuffing waste token budget, dilute reasoning attention, and compromise security guardrails.

---

## 2. Core Directives

### 2.1. No Unbounded File Ingestion (Zero-Prompt-Tax)
- **Forbidden:** Calling `view_file` or catting entire `AGENTS.md` files, entire rule directories, or unindexed doc trees into the context window.
- **Mandatory:** When viewing files for reference, agents must specify tight, targeted line slices (`StartLine`, `EndLine`) or retrieve pre-compiled snippets through AgentGraph.

### 2.2. Deterministic Rule & Role RBAC Resolution
- Before an agent or subagent executes an action, its role boundaries and authorized tool manifest must be resolved deterministically:
  ```bash
  hath0r agentgraph route --role <role-name> [--tool <tool-name>]
  ```
- **Rule Precedence Hierarchy:**
  $$\text{ORG\_INVARIANT (Tier 4)} \succ \text{REPO\_STANDARD (Tier 3)} \succ \text{SUBSYSTEM\_RULE (Tier 2)} \succ \text{ROLE\_GUIDELINE (Tier 1)}$$
- If a tool or action is not explicitly authorized for the active role, it is denied pre-execution.

### 2.3. Scoped Topical Knowledge & Context Queries
- Rather than scanning folders or broad globbing, agents must query the unified quad-graph planes:
  ```bash
  # Query rules, knowledge, and memory for a specific topic
  hath0r agentgraph query "<topic or query>"

  # Targeted lexical/BM25 knowledge search
  hath0r kb search -q "<topic>"
  ```
- Retrieval returns targeted, scored entity nodes with specific source URIs and bitemporal validity checks (`is_valid_at(as_of)`).

### 2.4. Workspace Topology Synchronization
- Whenever rules, roles, contracts, or subsystem documents are added or updated, agents must synchronize and validate the local AgentGraph snapshot before submitting PRs:
  ```bash
  hath0r agentgraph sync
  hath0r agentgraph validate
  ```
- Validation guarantees zero cyclic dependencies and zero contradictory directives across the rule inheritance DAG.

---

## 3. Enforcement & Verification

1. **Preflight Guardrail:** `hath0r preflight run` and test suite `pytest tests/test_agent_rules_governance.py` verify that `CR-AGENTGRAPH-001` is codified in root and subsystem governance files.
2. **Context Window Audit:** Token consumption monitors flag and reject agent traces that load complete policy files (> 500 lines) into context.
3. **PR Gate:** Any workflow or tool invocation bypassing AgentGraph role RBAC will fail the continuous validation and security gates.
