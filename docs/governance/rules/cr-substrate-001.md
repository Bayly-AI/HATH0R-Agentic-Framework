---
id: rule:cr-substrate-001
type: rule_policy
title: "CR-SUBSTRATE-001: Mandatory Cognitive Substrate Technology Utilization"
priority: 4
priority_name: ORG_INVARIANT
target_scope: root
restricted_actions: []
governs_roles: [developer, architect, qa-engineer, release-manager]
---
# CR-SUBSTRATE-001: Mandatory Cognitive Substrate Technology Utilization (CRITICAL — Org-Wide)

> **Rule ID:** `CR-SUBSTRATE-001`  
> **Status:** RATIFIED & MANDATORY RUNTIME INVARIANT  
> **Applies to:** All Agents, Workflows, Subagents, Bots, and Autonomous Automation Scripts across HATH0R OpenSource & Enterprise Products.  
> **Effective Date:** 2026-10-04  

---

## 1. Main Entry Statement (CRITICAL INVARIANT)

> **All agents and workflows executing tasks within Hath0r MUST utilize our unified cognitive substrate modules (`src/hath0r_engine/`).**
>
> Bypassing standard cognitive substrate engines to invent ad-hoc memory, non-sandboxed execution, un-cached AI gateways, or custom prompt parsers is **STRICTLY FORBIDDEN**.

---

## 2. Mandatory Substrate Engine Modules

1. **Pre-Execution Safety & Guardrails:**
   - Apply `GuardrailsManager` and `SyntaxGuardrail` (AST/SQL validation) with in-flight `SchemaRepairEngine` parameter coercion before command execution.
2. **AI Gateway & FinOps Tiered Routing:**
   - Route completion requests through `AIGatewayClient` and `TieredRouter` (`LIGHT`, `STANDARD`, `REASONING`) with `SemanticCache` memoization and token ledger tracking.
3. **Durable Orchestration & Replayability:**
   - Execute multi-step flows via `DurableWorkflowEngine` and `EventJournal` to support replayability and `HumanHibernationGate` suspension.
4. **Declarative DSPy Pipelines:**
   - Build structured reasoning with `Signature`, `ChainOfThought`, programmatic `Assert`, and `BootstrapFewShotCompiler`.
5. **Generative UI & Evidence Handshake:**
   - Emit interactive diffs, sliders, and HMAC SHA-256 signatures via `HandshakeSession` and `UIComponentBuilder`.
6. **Playwright UI Testing & Test Catalog:**
   - Execute UI verification with `PlaywrightTestRunner` and maintain Playwright-compliant master test specifications via `PlaywrightMasterCatalogManager`.
7. **Zero-Trust Sandboxing:**
   - Run untrusted user commands inside isolated sandbox providers (`E2BSandboxProvider`, `DaytonaSandboxProvider`, `LocalSandboxProvider`).
8. **Robust Parameter Optimization:**
   - Apply Taguchi Methods (`TaguchiEngine`, `calculate_snr`, `TaguchiLossFunction`) for Orthogonal Array Testing Strategy (OATS) matrix reduction.

---

## 3. Enforcement & Verification

- **Automated Test Suite:** `pytest tests/test_agent_rules_governance.py` and substrate unit tests verify module compliance.
- **CI Enforcement:** Preflight checks verify that all engine extensions utilize canonical `src/hath0r_engine/` interfaces.
