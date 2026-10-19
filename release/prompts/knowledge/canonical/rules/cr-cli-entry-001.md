# CR-CLI-ENTRY-001: Start with the CLI & Missing Capability Offer

**Classification**: Critical Organizational Invariant (`RULE`)  
**Scope**: Org-wide across all agents, bots, and operators  

---

## 📌 Rule Statement

1. **Start with the CLI (CRITICAL ENTRY GATE)**:
   When receiving ANY request or starting any task, agents **MUST ALWAYS START WITH THE OPERATOR CLI (`hath0r`)** rather than inventing ad-hoc scripts or direct unverified actions.

2. **Missing Capability Offer**:
   If the required connection, MCP tool, workflow, bot, or factory does not exist in `hath0r`, do **not** silently improvise. Offer to create or register the missing capability and use the original request as the immediate acceptance test.

3. **Docs Before Code**:
   Require formal procedure, strategy, playbook, or runbook documentation before scaffolding implementation.

4. **Shared Code in CLI**:
   Anything usable across multiple repositories or services MUST live in the Hath0r CLI and adhere to the canonical Artifact Hexad.
