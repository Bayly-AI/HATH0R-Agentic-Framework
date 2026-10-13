# Enterprise Hosting & Deployment Guide: HATH0R Ecosystem

> **Scope:** Enterprise Deployment Architecture, Local Virtualization, AWS EKS/ECS Fargate, and Azure AKS/Container Apps  
> **Governing Standards:** `CR-IAC-001`, `CR-CLI-ENTRY-001`, `CR-SUBSTRATE-001`, `CR-CICCCDCT-001`  
> **Suite:** HATH0R Agentic Framework, HATH0R-CLI, HATH0R-MCP, HATH0R-ATC  

---

## 🏛️ Executive Architecture: The Enterprise Cognitive Ecosystem

The **HATH0R Framework** is an enterprise-grade cognitive operating system and execution substrate engineered for high-assurance autonomous agent operations. Rather than running as a brittle monolithic script or unmanaged cloud function, Hath0r deploys as an integrated, self-governing **Enterprise System** designed with strict separation of concerns across four core components:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                  ENTERPRISE OPERATOR PLANE                             │
│                  (Developers • CI/CD Pipelines • Autonomous Orchestrators)             │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        HATH0R CLI (Standalone Control Plane)                           │
│        Single Entry Point • Substrate Router • FinOps Auditor • Governance Enforcement │
│                   Repository: https://github.com/Bayly-AI/HATH0R-CLI                   │
└───────────────┬───────────────────────────┬────────────────────────────┬───────────────┘
                │                           │                            │
                ▼                           ▼                            ▼
┌──────────────────────────────┐ ┌──────────────────────┐ ┌──────────────────────────────┐
│   HATH0R ATC (Air Traffic)   │ │  HATH0R MCP (Tools)  │ │  HATH0R FRAMEWORK (Cognitive)│
│ Observation & Group Control  │ │ Knowledge & Actions  │ │ Tri-Graph Substrate & FINOPS │
│   Bayly-AI/HATH0R-ATC        │ │  Bayly-AI/HATH0R-MCP │ │ Bayly-AI/HATH0R-Framework    │
└───────────────┬──────────────┘ └──────────┬───────────┘ └──────────────┬───────────────┘
                │                           │                            │
                └───────────────────────────┼────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               SHARED ENTERPRISE FABRIC                                 │
│          Redis (State Cache) • NGINX Reverse Proxy • Arize Phoenix Telemetry           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### The Enterprise Component Triad

To operate the Hath0r autonomous ecosystem in production or local development, the following components work in concert:

1. **[HATH0R CLI (`HATH0R-CLI`)](https://github.com/Bayly-AI/HATH0R-CLI)**:
   - **Role:** Standalone operator control plane, execution gateway, and CI/CD quality gatekeeper.
   - **Capabilities:** Manages repositories via `hath0r init`, validates policies via `hath0r agentgraph`, enforces FinOps budgets via `hath0r finops`, and controls container stacks via `hath0r docker`.
   - **Zero-Dependency:** Distributed as self-contained standalone binaries for macOS (ARM64/x86_64), Linux (ARM64/x86_64), and Windows (x64), or via npm (`@hath0r/node`) and pipx (`hath0r-cli`).

2. **[HATH0R MCP Server (`HATH0R-MCP`)](https://github.com/Bayly-AI/HATH0R-MCP)**:
   - **Role:** Model Context Protocol (MCP) server providing standard JSON-RPC tools and knowledge ingestion.
   - **Capabilities:** Exposes `kb_search`, `kb_get_document`, and `suite_info` tools over streamable HTTP transport (`/mcp`) for IDEs (VS Code, Cursor, Antigravity) and autonomous subagents.

3. **[HATH0R ATC Controller (`HATH0R-ATC`)](https://github.com/Bayly-AI/HATH0R-ATC)**:
   - **Role:** Air Traffic Control / Agent Traffic Controller, observation tower, and Docker-group orchestrator.
   - **Capabilities:** Orchestrates inter-agent network topologies, tracks active agent span lineages, coordinates multi-agent consensus evaluations, and manages shared edge gateways.

4. **[HATH0R Agentic Framework (`HATH0R-Agentic-Framework`)](https://github.com/Bayly-AI/HATH0R-Agentic-Framework)**:
   - **Role:** Core cognitive substrate library, Tri-Graph memory engine (KnowledgeGraph, ContextGraph, MemoryGraph), deterministic AST guardrails, Gameshow calibration engine, and FinOps Tokenizer Tax auditor.

---

## 💻 1. Local Deployment (Workstation & Air-Gapped On-Premise)

Hath0r is designed from the ground up for **100% local, offline, and air-gapped** execution. It requires no mandatory cloud subscription, database daemon, or outbound internet access for local development.

### Option A: Standalone CLI Operator (Native Workstation)

Install and run the standalone Hath0r CLI binary directly without configuring Docker or virtual environments:

```bash
# 1. Download or copy the platform binary (e.g., macOS Apple Silicon)
chmod +x ./release/python/cli/hath0r-darwin-arm64
sudo cp ./release/python/cli/hath0r-darwin-arm64 /usr/local/bin/hath0r

# 2. Verify system health and operational readiness
hath0r doctor

# 3. Initialize cognitive governance in any repository
cd /path/to/enterprise-repo
hath0r init

# 4. Execute pre-flight audit and verify local memory
hath0r preflight
hath0r quality
hath0r memory search "governance policies"
```

### Option B: Local Containerized Stack (Docker & Docker Compose)

For multi-agent coordination, tool execution, and local caching, run the canonical container group on Docker network `hath0r-net`:

#### 1. Network & Directory Preparation
```bash
# Create shared bridge network
docker network create hath0r-net 2>/dev/null || true

# Prepare credential environment (never hardcode in compose files)
mkdir -p /Users/raybayly/Development/.credentials/hath0r
cat << 'EOF' > /Users/raybayly/Development/.credentials/hath0r/.env
HATH0R_ENV=development
HATH0R_NGINX_HOST_PORT=38000
HATH0R_MCP_HOST_PORT=38083
HATH0R_ATC_HOST_PORT=38084
REDIS_HOST=redis
REDIS_PORT=6379
EOF
```

#### 2. Local `docker-compose.yml` Stack
```yaml
version: "3.8"

networks:
  hath0r-net:
    external: true

services:
  # Shared In-Memory Cache & Lock Store
  redis:
    image: redis:7-alpine
    container_name: HATH0R-Redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    networks:
      - hath0r-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  # Reverse Proxy & Edge Ingress
  nginx:
    image: nginx:alpine
    container_name: HATH0R-NGINX
    restart: unless-stopped
    ports:
      - "${HATH0R_NGINX_HOST_PORT:-38000}:80"
    volumes:
      - ./cfg/docker/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - hath0r-net

  # Model Context Protocol (MCP) Server
  mcp:
    image: hath0r/mcp:local
    container_name: HATH0R-MCP
    restart: unless-stopped
    environment:
      - HATH0R_ENV=development
      - REDIS_URL=redis://redis:6379/0
      - MCP_PORT=8083
    ports:
      - "${HATH0R_MCP_HOST_PORT:-38083}:8083"
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - hath0r-net
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:8083/health"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Air Traffic Controller (ATC)
  atc:
    image: hath0r/atc:local
    container_name: HATH0R-ATC
    restart: unless-stopped
    environment:
      - HATH0R_ENV=development
      - REDIS_URL=redis://redis:6379/0
      - ATC_PORT=8084
    ports:
      - "${HATH0R_ATC_HOST_PORT:-38084}:8084"
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - hath0r-net
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:8084/health"]
      interval: 10s
      timeout: 3s
      retries: 3
```

#### 3. Operating the Stack
```bash
# Start state store and edge gateway
docker compose up -d redis nginx

# Launch application layer (ATC & MCP)
docker compose up -d atc mcp

# Verify MCP tool registration and health
hath0r mcp check --endpoint http://127.0.0.1:38083/mcp
```

---

## ☁️ 2. AWS Cloud Deployment (Serverless EKS Fargate & ECS)

In enterprise AWS environments, Hath0r enforces the **`CR-IAC-001`** standard:
- **Serverless Compute:** Workloads deploy on **AWS EKS Fargate** or **Amazon ECS Fargate**, completely eliminating EC2 node patch management and host-level privilege escalation.
- **Hardened Multi-Stage Containers:** All containers execute as non-root user (`UID 10001:GID 10001`) with read-only root filesystems (`readOnlyRootFilesystem: true`).
- **Cryptographic Supply-Chain Salting:** Images are pinned to immutable SHA-256 digests signed with Cosign and attested with SLSA provenance predicates.
- **Least-Privilege Identity:** AWS IAM Roles for Service Accounts (IRSA) eliminates hardcoded credentials. Secrets are injected at runtime via AWS Secrets Manager.

### AWS EKS Fargate Architecture

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AWS INTERNET GATEWAY                                 │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        AWS APPLICATION LOAD BALANCER (ALB)                             │
│                  alb.ingress.kubernetes.io/target-type: ip                             │
└───────────────────────┬─────────────────────────────────────────┬──────────────────────┘
                        │                                         │
                        ▼ (Direct Private ENI)                    ▼ (Direct Private ENI)
┌───────────────────────────────────────────────┐ ┌──────────────────────────────────────┐
│        AWS FARGATE POD: HATH0R-MCP            │ │      AWS FARGATE POD: HATH0R-ATC     │
│ • Non-Root UID 10001:GID 10001                │ │ • Non-Root UID 10001:GID 10001       │
│ • readOnlyRootFilesystem: true                │ │ • readOnlyRootFilesystem: true       │
│ • Memory: 1GiB | CPU: 0.5 vCPU                │ │ • Memory: 1GiB | CPU: 0.5 vCPU       │
│ • IRSA: arn:aws:iam::...:role/Hath0rMcpRole   │ │ • IRSA: arn:aws:iam::...:role/Hath0r │
└───────────────────────┬───────────────────────┘ └──────────────────┬───────────────────┘
                        │                                            │
                        └─────────────────────┬──────────────────────┘
                                              ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                  MANAGED AWS SERVICES                                  │
│   Amazon ElastiCache Redis • AWS Secrets Manager • Arize Phoenix / Amazon CloudWatch   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 1: EKS Fargate Profile Manifest (`iac/fargate-profile.yaml`)

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: hath0r-enterprise-cluster
  region: us-east-1
  version: "1.30"

fargateProfiles:
  - name: fp-hath0r-core
    selectors:
      - namespace: hath0r-system
        labels:
          app.kubernetes.io/part-of: hath0r-ecosystem
```

### Step 2: Kubernetes Deployment Manifest (`k8s/hath0r-mcp-deployment.yaml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hath0r-mcp
  namespace: hath0r-system
  labels:
    app.kubernetes.io/name: hath0r-mcp
    app.kubernetes.io/part-of: hath0r-ecosystem
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: hath0r-mcp
  template:
    metadata:
      labels:
        app.kubernetes.io/name: hath0r-mcp
        app.kubernetes.io/part-of: hath0r-ecosystem
    spec:
      serviceAccountName: hath0r-mcp-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
      containers:
        - name: mcp-engine
          # Pinned immutable salted digest (CR-IAC-001)
          image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/hath0r/mcp@sha256:4a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b
          imagePullPolicy: IfNotPresent
          securityContext:
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
          ports:
            - containerPort: 8083
              name: http-mcp
          resources:
            requests:
              cpu: "500m"
              memory: "1024Mi"
            limits:
              cpu: "500m"
              memory: "1024Mi"
          env:
            - name: HATH0R_ENV
              value: "production"
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: hath0r-secrets
                  key: REDIS_URL
          volumeMounts:
            - name: tmp-volume
              mountPath: /tmp
          livenessProbe:
            httpGet:
              path: /health
              port: 8083
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /ready
              port: 8083
            initialDelaySeconds: 5
            periodSeconds: 10
      volumes:
        - name: tmp-volume
          emptyDir: {}
```

### Step 3: AWS Application Load Balancer Ingress (`k8s/ingress.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hath0r-ingress
  namespace: hath0r-system
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip  # REQUIRED FOR AWS FARGATE
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:123456789012:certificate/abc-123
spec:
  rules:
    - host: mcp.enterprise.internal
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: hath0r-mcp
                port:
                  number: 8083
```

---

## 🔷 3. Azure Cloud Deployment (AKS & Azure Container Apps)

For Microsoft Azure environments, Hath0r provides first-class support for **Azure Kubernetes Service (AKS)** and serverless **Azure Container Apps (ACA)**:

### Option A: Serverless Azure Container Apps (ACA)

Azure Container Apps provides a fully managed, serverless microservice runtime built on Kubernetes, KEDA, and Envoy.

#### 1. Resource Group & Container Apps Environment
```bash
# 1. Create Azure resource group and environment
az group create --name rg-hath0r-prod --location eastus
az containerapp env create \
  --name env-hath0r-prod \
  --resource-group rg-hath0r-prod \
  --location eastus

# 2. Deploy Azure Container App for HATH0R-MCP
az containerapp create \
  --name hath0r-mcp \
  --resource-group rg-hath0r-prod \
  --environment env-hath0r-prod \
  --image myregistry.azurecr.io/hath0r/mcp:1.6.0 \
  --target-port 8083 \
  --ingress external \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 5 \
  --env-vars \
    HATH0R_ENV=production \
    REDIS_HOST=redis-hath0r.redis.cache.windows.net
```

### Option B: Azure Kubernetes Service (AKS) Enterprise Architecture

For full cluster deployments, deploy onto AKS utilizing Azure CNI and Azure Key Vault Secrets Store CSI driver:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hath0r-atc
  namespace: hath0r-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hath0r-atc
  template:
    metadata:
      labels:
        app: hath0r-atc
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: hath0r-workload-identity-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
      containers:
        - name: atc-controller
          image: myregistry.azurecr.io/hath0r/atc:1.6.0
          securityContext:
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
          ports:
            - containerPort: 8084
          resources:
            requests:
              cpu: "500m"
              memory: "1024Mi"
            limits:
              cpu: "1000m"
              memory: "2048Mi"
          volumeMounts:
            - name: secrets-store-inline
              mountPath: "/mnt/secrets-store"
              readOnly: true
            - name: tmp-dir
              mountPath: "/tmp"
      volumes:
        - name: tmp-dir
          emptyDir: {}
        - name: secrets-store-inline
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: "azure-keyvault-hath0r"
```

---

## 🛡️ Enterprise Security, FinOps & Compliance Matrix

| Security / Governance Dimension | Standard | Implementation Mechanism |
| :--- | :--- | :--- |
| **Non-Root Execution** | `CR-IAC-001` | Enforced `UID 10001:GID 10001` in all container images. |
| **Filesystem Immutability** | `CR-IAC-001` | `readOnlyRootFilesystem: true` with ephemeral `/tmp` emptyDir scratch storage. |
| **Supply Chain Attestation** | `CR-IAC-001` | Pinned SHA-256 digests; Cosign signatures verified against transparency log. |
| **Secrets Isolation** | `CR-CLI-FEATURE-STANDARD-001` | No secrets baked in images; dynamic resolution via AWS Secrets Manager / Azure Key Vault. |
| **Pre-Execution Safety** | `CR-SUBSTRATE-001` | Deterministic AST Guardrail blocks unauthorized bash drops, SQL deletions, and privilege escalation. |
| **FinOps Token Spending Cap** | `CR-SUBSTRATE-001` | Recursive subagent circuit breaker capped at $0.25 / 50k tokens (`hath0r finops budget`). |
| **Audit Trails & Evidence** | `CR-SUBSTRATE-001` | HMAC SHA-256 cryptographic signatures bind human sign-offs to execution artifacts. |

---

## 🛠️ Verification & Operational Runbook

After deploying Hath0r locally or in cloud environments, verify cluster health using the Hath0r CLI:

```bash
# 1. Probe local or remote MCP endpoints
hath0r mcp check --endpoint https://mcp.your-domain.com/mcp

# 2. Run Tri-Graph validation
hath0r agentgraph validate

# 3. Execute Continuous Calibration telemetry sanity check
hath0r cicccd calibrate

# 4. Run automated preflight compliance audit
hath0r preflight
```
