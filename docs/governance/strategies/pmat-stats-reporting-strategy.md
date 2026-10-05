# Strategy: PMAT Multi-Dimensional Stats & Provability Reporting

> Canonical Strategy Specification · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Executive Summary & Core Objectives

Software maintenance and quality governance require holistic insight beyond simple line counts. The **PMAT Multi-Dimensional Stats & Provability Reporting** strategy establishes a formal mathematical and cognitive framework for quantifying:
1. **Code Churn Volatility**: Temporal decay and commit frequency.
2. **Formal Provability Score**: Type invariant safety, assertion density, and defect probability ($P_{\text{defect}} = 1 - S_{\text{provability}}$).
3. **AST Complexity Score**: Cyclomatic complexity, Cognitive complexity, AST nesting depth, and Halstead volume.
4. **Hotspot Risk Index**: Composite evaluation combining churn volatility, AST complexity, and inverse provability ($R = \text{Churn} \times \text{Complexity} \times (1 - \text{Provability})$).

---

## 2. Mathematical Formulation

$$\text{Composite Hotspot Risk Index } R(f) = C(f) \cdot \left(\frac{K(f)}{10}\right) \cdot (1 - P(f) + 0.1)$$

Where:
- $C(f) \in [0.0, 1.0]$: Time-windowed commit churn score.
- $K(f) \ge 1.0$: Cyclomatic / Cognitive AST complexity score.
- $P(f) \in [0.0, 1.0]$: Formal provability score derived from invariant annotations and defect bounds.

---

## 3. Cognitive Substrate & Zero-Prompt-Tax Integration

1. **AgentGraph Ingestion**: Stats reports populate `pmat_stats` nodes in `KnowledgePlane` and `ContextPlane`.
2. **FinOps Escalation**: High-risk modules ($R(f) \ge 0.75$) trigger automatic routing escalation in `TieredRouter` to `ComplexityTier.REASONING` (`o3-mini`).
