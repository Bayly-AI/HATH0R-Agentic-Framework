# ATC (Air Traffic Control) Control Tower Design

Hath0r ATC acts as the central group controller and observation plane for the Hath0r suite.

---

## 🏗️ Architectural Topology

Hath0r ATC runs as a containerized stack attached to the shared bridge network `hath0r-net`:

1. **`Hath0r-Edge` (Reverse Proxy & Ingress)**:
   - Base image: `nginx:1.27-alpine`
   - Binds to host port `38000` (or `HATH0R_NGINX_HOST_PORT`)
   - Functions:
     - Health monitoring endpoint: `/healthz`
     - SSE / streaming reverse proxy to `Hath0r-MCP:8083`
     - Reverse proxy routing for future backend APIs
     - SSL termination (when deployed in staging/production)

2. **`Hath0r-Sessions` (Shared State & Locking)**:
   - Base image: `redis:7-alpine`
   - Binds to internal port `6379`
   - Functions:
     - Append-Only File (`AOF`) persistence mounted on volume `hath0r_redis_data`
     - Distributed lock management for concurrent agent tasks
     - Ephemeral cache for Letta memory pages

3. **Telemetry & Observation (`OpenTelemetry`)**:
   - Ingests traces, spans, and token expenditure metrics
   - Enforces zero data loss on agent invocation audits
