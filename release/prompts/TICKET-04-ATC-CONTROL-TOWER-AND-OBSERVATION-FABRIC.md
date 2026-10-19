# PROMPT TICKET 04: Hath0r ATC (Control Tower) Infrastructure & Observation Fabric

**Ticket ID**: `HATH0R-RELEASE-004`  
**Role**: `InfrastructureDevOpsAgent`  
**Scope**: Deploy Control Tower compose stack, configure Redis session state, Nginx reverse proxy edge, and OpenTelemetry telemetry collectors  

---

## 🎯 Task Objective

Build and provision **Hath0r ATC (Air Traffic Control / Control Tower)**. ATC serves as the central control plane, reverse-proxy ingress gateway, session state coordinator, and observation telemetry hub for the entire Hath0r infrastructure.

---

## 📥 Inputs & Source Resolution

- **ATC Repository URL / Path**: Obtained from Ticket 01 (`ATC_REPO` or monorepo `UNIFIED_REPO/atc`).
- **Network Bridge**: `hath0r-net` (established in Ticket 01).
- **Control Tower Host Port**: `38000` (`HATH0R_NGINX_HOST_PORT`).
- **Shared State Storage**: Redis 7 (`Hath0r-Sessions`).
- **Edge Reverse Proxy**: Nginx 1.27 (`Hath0r-Edge`).

---

## 🛠️ Execution Steps

### Step 1: Deploy ATC Docker Compose Stack
Navigate to the ATC deployment directory and launch the core infrastructure services:
```bash
cd "${ATC_SOURCE_DIR}/deploy/docker"

# Launch Redis session store and Nginx reverse proxy edge
docker compose up -d redis nginx

# Verify container statuses
docker ps --filter "label=com.hath0r.project=hath0r-opensource"
```

### Step 2: Configure Edge Reverse Proxy Routes
Ensure Nginx is properly configured to proxy requests across `hath0r-net`:
- Route `/healthz` -> Local health check
- Route `/mcp/` -> Proxy to `http://Hath0r-MCP:8083/`
- Route `/sessions/` -> Managed via Redis API / backend

Verify the Nginx configuration:
```bash
docker exec Hath0r-Edge nginx -t
```

### Step 3: Configure OpenTelemetry Observability Fabric
Verify or configure OpenTelemetry spans collector under `${HATH0R_HOME}/cfg/otel.json`:
```json
{
  "service_name": "hath0r-infrastructure-release",
  "endpoint": "http://127.0.0.1:4318",
  "protocol": "http/protobuf",
  "spans": {
    "sampler": "always_on",
    "export_interval_millis": 5000
  },
  "metrics": {
    "export_interval_millis": 10000
  }
}
```

### Step 4: Validate Edge Health and Connectivity
Run the ATC smoke test:
```bash
# Smoke test edge proxy
curl -fsS "http://127.0.0.1:38000/healthz"

# Verify Redis ping from container
docker exec Hath0r-Sessions redis-cli ping
```

---

## ✅ Acceptance Criteria & Assertions

1. `Hath0r-Sessions` (Redis) is running, healthy, and responds `PONG` to `redis-cli ping`.
2. `Hath0r-Edge` (Nginx) is running, healthy, and exposes `http://127.0.0.1:38000/healthz`.
3. Inter-service connectivity on `hath0r-net` is established (`Hath0r-Edge` can reach `Hath0r-MCP` and `Hath0r-Sessions`).
4. Observation telemetry configuration is initialized and valid.
