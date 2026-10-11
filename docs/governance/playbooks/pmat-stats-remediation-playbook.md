# Playbook: PMAT Stats & High-Risk Remediation

> Canonical Remediation Playbook · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Remediation Trigger Protocol

When a file scores a Composite Hotspot Risk Index $R(f) \ge 0.75$:

```
[High Composite Risk Index] -> [Add Type Assertions] -> [Decouple AST Branches] -> [Re-evaluate Index]
```

1. **Add Type Invariant Assertions**: Increase formal provability $P(f)$ above $0.80$.
2. **Decouple AST Branching**: Reduce Cyclomatic complexity $K(f)$ below 15.
3. **Verify Defect Index**: Ensure $P_{\text{defect}} \le 0.15$.
