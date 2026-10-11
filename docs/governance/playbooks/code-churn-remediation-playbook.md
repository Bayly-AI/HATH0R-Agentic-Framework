# Playbook: Code Churn & Hotspot Remediation

> Canonical Remediation Playbook · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Scenario: Critical Hotspot Remediation

When a file enters the `CRITICAL` risk tier (volatility score $\ge 0.75$), follow these remediation steps:

```
[Hotspot Detected] -> [Co-Change Dependency Graphing] -> [Modular Decoupling] -> [Playwright / Unit Verification]
```

### Remediation Protocol
1. **Analyze Co-Change Clustered Files**: Run `hath0r churn hotspots --file <path>` to identify companion files that are frequently committed alongside the target.
2. **Apply Structural Decoupling**:
   - Extract sprawling conditional branches into distinct strategy classes or dispatch tables.
   - Introduce Facade or Event Bus patterns for modules with $>3$ co-changing dependents.
3. **Execute Unit & Visual Testing**:
   - Run `pytest` to verify zero regression.
   - Run `pytest tests/test_playwright_testing.py` for UI modules.
4. **Re-evaluate Volatility**:
   - Confirm file cyclomatic complexity is reduced below 15.
