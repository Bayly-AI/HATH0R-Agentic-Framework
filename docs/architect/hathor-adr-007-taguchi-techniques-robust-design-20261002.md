---
id: HATHOR-ADR-007
title: "HATHOR-ADR-007 — Taguchi Techniques for Robust Design, Orthogonal Array Testing, and Quality Loss Optimization"
summary: "Adopts Taguchi Methods (Orthogonal Array Testing Strategy / OATS, Robust Parameter Design, Signal-to-Noise Ratio optimization, and Quality Loss Function) across the HATH0R ecosystem to optimize test matrices and agentic pipeline hyperparameters."
doc_type: ADR
diataxis: decision
audience: [architect, agent, developer, qa]
tags: [architecture, taguchi, oats, robust-design, optimization, dspy, finops, testing]
version: 1.0.0
status: accepted
created: '2026-10-02'
updated: '2026-10-02'
owner: Raymond Bayly (BaylyAI)
review: {trust: verified, reviewed_by: 'Raymond Bayly', reviewed_at: '2026-10-02', interval: null, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# HATHOR-ADR-007 — Taguchi Techniques for Robust Design, Orthogonal Array Testing, and Quality Loss Optimization

## Status
**ACCEPTED** (2026-10-02)

## Decision Class
Architecture Decision Record (Cognitive Substrate, Quality Engineering & CLI Surface)

---

## 1. Context & Problem Statement

As the HATH0R ecosystem expands across multi-agent orchestration, declarative DSPy pipelines, zero-trust sandboxes (`Local`, `Daytona`, `E2B`), generative UI components, and tiered FinOps routing, two architectural bottlenecks emerge:

1. **Combinatorial Explosion in Verification**:
   Full factorial matrix testing of CLI configurations, UI components (browsers $\times$ viewports $\times$ themes $\times$ states), and runtime flags requires hundreds or thousands of test runs per commit ($L^k$), creating unacceptable CI latency and prohibitive API costs.
2. **Stochastic Noise in Agentic Pipelines**:
   LLM non-determinism, network latency drift, dirty context chunks, and token throttling act as uncontrollable "noise factors". Traditional hyperparameter tuning optimizes against static, ideal environments and degrades under real-world runtime fluctuations.
3. **Binary QA Fallacy**:
   Conventional pass/fail thresholds (e.g. latency $< 2000\text{ms}$) fail to quantify the economic and operational loss incurred when system responses drift away from target nominal values.

---

## 2. Decision

**ADOPT Taguchi Methods** across the HATH0R ecosystem and cognitive substrate:

1. **Orthogonal Array Testing Strategy (OATS)**:
   Use standard orthogonal arrays ($L_4, L_8, L_9, L_{12}, L_{18}$) to construct mathematically balanced, pairwise-complete test matrices that reduce combinatorial test volume by $85\text{–}95\%$ while maintaining full two-factor interaction coverage.
2. **Robust Parameter Design (Inner/Outer Array Architecture)**:
   In Declarative DSPy pipelines and Tri-Graph RAG routing, separate controllable factors (prompt variants, few-shot exemplar counts, temperatures, schema pruning ratios) from uncontrollable noise factors (latency jitter, noisy context retrieval, token pressure). Maximize the **Signal-to-Noise Ratio (SNR)** to identify configurations resilient to environmental noise.
3. **Taguchi Quality Loss Function ($L(y)$)**:
   Implement continuous quadratic loss modeling for FinOps budgets, latency SLOs, and schema repair churn, penalizing drift away from target values rather than evaluating flat step-function thresholds.
4. **Lightweight, Zero-Heavy-Dependency Engine Substrate**:
   Implement standard orthogonal array lookup tables, factor mapping logic, SNR evaluators, and loss calculators in `src/hath0r_engine/optimization/taguchi.py` using pure Python standard library.

```
                          HATH0R Substrate Optimization
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
Orthogonal Array (OATS)      Robust Parameter Design        Quality Loss Function
• Minimal balanced matrices  • Inner Array (Control Factors)• Continuous quadratic drift
• L4, L8, L9, L12, L18       • Outer Array (Noise Factors)  • FinOps & latency SLO loss
• 85-95% test reduction      • Signal-to-Noise Maximization • L(y) = k(y - m)^2
        │                               │                               │
        └───────────────────────────────┼───────────────────────────────┘
                                        ▼
                            HATH0R-CLI Command Surface
                     (`hath0r test matrix`, `hath0r optimize`)
```

---

## 3. Mathematical Specifications

### 3.1 Orthogonal Array Catalog
Standard orthogonal arrays denote $L_N(s^k)$, where $N$ is the number of experimental runs, $s$ is the number of levels per factor, and $k$ is the maximum number of factors:

| Array | Run Count ($N$) | Factor Capacity | Primary Use Case in HATH0R |
| :--- | :--- | :--- | :--- |
| **$L_4(2^3)$** | 4 | Up to 3 factors at 2 levels | Lightweight CLI binary flag pairing |
| **$L_8(2^7)$** | 8 | Up to 7 factors at 2 levels | Comprehensive binary feature toggle matrices |
| **$L_9(3^4)$** | 9 | Up to 4 factors at 3 levels | Tiered routing: 3 models $\times$ 3 sandboxes $\times$ 3 cache modes $\times$ 3 retrieval depths |
| **$L_{12}(2^{11})$** | 12 | Up to 11 factors at 2 levels | Preflight gate & environment checks |
| **$L_{18}(2^1 \times 3^7)$** | 18 | 1 factor at 2 levels + 7 factors at 3 levels | Playwright UI & Generative widget cross-browser/viewport matrices |

### 3.2 Signal-to-Noise (S/N) Ratio Formulations

1. **Smaller-the-Better (STB)** — Minimizing cost, latency, or error rates:
   $$\eta = -10 \log_{10} \left( \frac{1}{n} \sum_{i=1}^n y_i^2 \right)$$
2. **Larger-the-Better (LTB)** — Maximizing benchmark accuracy or eval pass rates:
   $$\eta = -10 \log_{10} \left( \frac{1}{n} \sum_{i=1}^n \frac{1}{y_i^2} \right)$$
3. **Nominal-the-Best (NTB)** — Maintaining strict target nominal outputs with minimal variance:
   $$\eta = 10 \log_{10} \left( \frac{\bar{y}^2}{s^2} \right)$$
   where $\bar{y} = \frac{1}{n} \sum y_i$ and $s^2 = \frac{1}{n-1} \sum (y_i - \bar{y})^2$.

### 3.3 Quality Loss Function (QLF)

The loss incurred when a quality characteristic $y$ drifts from target nominal value $m$:
$$L(y) = k (y - m)^2$$
Where the quality loss coefficient $k$ is calculated from customer/operator tolerance $\Delta_0$ and associated loss cost $A_0$:
$$k = \frac{A_0}{\Delta_0^2}$$

---

## 4. Integration Touchpoints & CLI Surface

1. **Substrate Engine**:
   - `src/hath0r_engine/optimization/taguchi.py`: Core data structures (`OrthogonalArray`, `Factor`, `ExperimentMatrix`, `SNRMetric`) and pure-Python matrix generator.
2. **CLI Surface**:
   - `hath0r test matrix --oats`: CLI test harness to generate or execute balanced test matrices.
   - `hath0r optimize --taguchi`: Parameter optimization utility for agent pipelines.
3. **Playwright UI Integration**:
   - Feeds into `PlaywrightMasterCatalogManager` to construct cross-browser and responsive layout test matrices without linear factor multiplication.

---

## 5. Consequences & Implementation Guidance

* **Efficiency**: Eliminates test matrix explosion; CI suites complete orders of magnitude faster.
* **Zero Heavy Dependencies**: Pure Python implementation guarantees no bloat (e.g. no mandatory NumPy/SciPy requirement for core runtime).
* **Limitations**: When strong 3-way or higher interactions dominate (rare in parameter tuning), Bayesian optimization or full factorial sub-arrays must supplement OATS.
