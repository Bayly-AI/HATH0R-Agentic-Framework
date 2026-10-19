# Hath0r ATC (Air Traffic Control) Infrastructure Catalog

**Hath0r ATC** is the central Control Tower and observation stack that coordinates infrastructure, traffic routing, session states, and telemetry for all Hath0r agents and services.

Host Endpoint: `http://127.0.0.1:38000`  
Docker Network: `hath0r-net`  

---

## 🏛️ ATC Architecture & Subsystems

```text
[Operator / Agent] 
       │
       ▼
 [ Hath0r-Edge ] (Nginx 1.27 reverse proxy on port 38000)
       ├── /healthz        ──> Local Nginx Health Probe
       ├── /mcp/           ──> Hath0r-MCP:8083 (MCP Knowledge Server)
       └── /sessions/      ──> Hath0r-Sessions:6379 (Redis Session State)
       │
       ▼
 [ Hath0r-Sessions ] (Redis 7 AOF persistent state store)
       │
       ▼
 [ OpenTelemetry ] (Collector, Trace Exporter, Span Lineages)
```

---

## 🚦 Endpoints & Traffic Controls

### 1. Ingress Edge Router (`Hath0r-Edge`)
- **Container**: `Hath0r-Edge` (image: `nginx:1.27-alpine`)
- **Port Mapping**: `127.0.0.1:38000:80`
- **Routing Rules**:
  - `GET /healthz`: Returns HTTP 200 `OK - Edge Healthy`.
  - `ANY /mcp/*`: Reverse proxies to `http://Hath0r-MCP:8083/` preserving SSE and streaming headers.
  - `GET /nginx_status`: Stub status for traffic rate observation.
- **Verification Command**:
  ```bash
  curl -fsS "http://127.0.0.1:38000/healthz"
  ```

### 2. Session Coordinator (`Hath0r-Sessions`)
- **Container**: `Hath0r-Sessions` (image: `redis:7-alpine`)
- **Internal Port**: `6379`
- **Persistence**: Append-Only File (`appendonly yes`) on volume `hath0r_redis_data`
- **Role**:
  - Ephemeral session locking for concurrent subagent dispatches.
  - Letta-style active working memory buffer caching.
  - Event journal replay streams.
- **Verification Command**:
  ```bash
  docker exec Hath0r-Sessions redis-cli ping
  ```

---

## 📊 Observation & Telemetry Fabric

### OpenTelemetry Collector Config (`cfg/otel.json`)
ATC configures zero-drop telemetry collection for tracing span lineages and agent token expenditure:
- **Service Name**: `hath0r-infrastructure-release`
- **Protocols**: OTLP HTTP/protobuf on port 4318, OTLP gRPC on port 4317.
- **Span Sampler**: `always_on` for deterministic agent action audits.
- **Metrics Interval**: 10,000 ms.

---

## 🛡️ Control Tower Governance Commands

Control Tower commands are invoked via the Hath0r CLI or direct container controls:

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Inspect Topology** | `docker ps --filter "label=com.hath0r.project=hath0r-opensource"` | List active group containers |
| **Edge Smoke Test** | `./deploy/docker/smoke-test.sh` | Validate proxy routing & redis |
| **State Flush (Safe)** | `docker exec Hath0r-Sessions redis-cli bgsave` | Force sync session state to disk |
| **Network Inspection** | `docker network inspect hath0r-net` | Verify container IP allocations |
