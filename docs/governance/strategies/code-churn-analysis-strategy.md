# Strategy: Code Churn & Architectural Hotspot Analysis

> Canonical Strategy Specification · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Executive Summary & Vision

Software systems suffer from localized erosion where frequently modified files with high cyclomatic complexity become primary drivers of regressions, security vulnerabilities, and deployment failures. The **PMAT Code Churn & Architectural Hotspot Analysis** strategy defines a proactive, automated cognitive methodology for identifying, measuring, and mitigating code volatility across the BaylyAI open-source ecosystem without incurring prompt tax.

---

## 2. Mathematical Volatility Model

Hath0r calculates file volatility score $V(f) \in [0.0, 1.0]$ using a multi-dimensional weighted normalization:

$$V(f) = \min\left(1.0, 0.40 \cdot \frac{C_f}{C_{\max}} + 0.30 \cdot \frac{L_f}{L_{\max}} + 0.30 \cdot \frac{K_f}{K_{\max}}\right)$$

Where:
- $C_f$: Commit count modifying file $f$ within the evaluation time window (default 30 days, $C_{\max} = 15$).
- $L_f$: Total churn volume in lines (lines added + lines deleted, $L_{\max} = 600$).
- $K_f$: Cyclomatic / syntactic branching complexity score ($K_{\max} = 30$).

### Risk Classification Tiers

| Volatility Score | Risk Tier | Reasoning Escalation | PR Merge Policy |
| :--- | :--- | :--- | :--- |
| $\ge 0.75$ | **CRITICAL** | `REASONING` (`o3-mini`, `deepseek-r1`) | Requires senior architectural sign-off |
| $\ge 0.50$ | **HIGH** | `REASONING` (`o3-mini`) | Mandatory automated test verification |
| $\ge 0.25$ | **MEDIUM** | `STANDARD` (`claude-3-5-sonnet`) | Standard CI/CD passing gates |
| $< 0.25$ | **LOW** | `LIGHT` (`claude-3-5-haiku`) | Fast-track merge eligible |

---

## 3. Cognitive Substrate Integration

1. **Zero-Prompt-Tax Extraction**: Raw commit histories and AST branches are analyzed directly in the `PmatAdapter` substrate before any LLM invocations occur.
2. **AgentGraph Context & Knowledge Planes**: Churn scores and co-change dependency edges (`CO_CHANGES_WITH`) are populated as structured graph entities, allowing autonomous bots to inspect hotspots deterministically.
3. **Dynamic Tier Escalation**: When generating code or reviewing PRs touching high-volatility files, `TieredRouter` automatically routes queries to high-capability reasoning models.
