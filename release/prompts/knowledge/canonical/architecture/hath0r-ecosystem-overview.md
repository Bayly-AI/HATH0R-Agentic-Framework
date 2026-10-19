# Hath0r Ecosystem Overview: Framework, CLI, MCP & ATC

The **Hath0r Ecosystem** is a production-grade cognitive infrastructure designed for autonomous agent swarms, deterministic safety, and enterprise governance.

---

## 🏛️ Tripartite Infrastructure Architecture

The core infrastructure consists of three decoupled yet interdependent nodes:

```text
               ┌──────────────────────────────┐
               │    Hath0r CLI (Operator)     │
               │   - Cognitive Router         │
               │   - AST / Syntax Guardrails  │
               │   - Session Compounding      │
               └──────────────┬───────────────┘
                              │
                    Docker Network: hath0r-net
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│  Hath0r MCP (Knowledge Hub)  │ │   Hath0r ATC (Control Tower) │
│ - Semantic Vector Search     │ │ - Hath0r-Edge (Nginx proxy)  │
│ - Runbook Prompt Synthesizer │ │ - Hath0r-Sessions (Redis)    │
│ - 42 Standardized Tools      │ │ - OpenTelemetry Observability│
└──────────────────────────────┘ └──────────────────────────────┘
```

1. **Hath0r CLI (`HATH0R-CLI`)**:
   - The primary command-line tool (`hath0r`) used by both human operators and autonomous agents.
   - Houses the unified cognitive engine: FinOps tiered routing, pre-execution safety guardrails, Letta-compatible memory paging, and durable workflow event journaling.

2. **Hath0r MCP (`HATH0R-MCP`)**:
   - Implements the Model Context Protocol (MCP) to provide agents with verified organizational knowledge, official documentation, environment inspection, and parameterized runbooks.
   - Operates as a hardened container on port `38083` attached to `hath0r-net`.

3. **Hath0r ATC (`HATH0R-ATC`)**:
   - Serves as the Air Traffic Controller and Control Tower.
   - Coordinates multi-agent dispatches, manages shared persistent session state (`Hath0r-Sessions` Redis), controls ingress routing (`Hath0r-Edge` Nginx on port `38000`), and streams telemetry spans via OpenTelemetry.
