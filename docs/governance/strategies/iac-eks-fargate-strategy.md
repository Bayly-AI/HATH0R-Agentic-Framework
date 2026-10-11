# Strategy: Infrastructure as Code (IaC), Container Salting & AWS EKS Fargate Deployment

> **Document Type:** Strategy  
> **Status:** Ratified  
> **Governing Standards:** `CR-IAC-001`, `CR-CLI-ENTRY-001`, `CR-CLI-FEATURE-STANDARD-001`  
> **Target Subsystems:** Control Tower (`HATH0R-CLI`), Cognitive Engine, Suite Repositories (`~/Development`)  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#260, Bayly-AI/HATH0R-CLI#441

---

## 1. Executive Summary & Vision

The HATH0R Infrastructure as Code (IaC) doctrine mandates that all software deliverables across `~/Development`—spanning agentic MCP servers, cognitive runtime backends, UXP web applications, and autonomous CLI bots—are strictly declared, built, cryptographically salted, and deployed via code. Imperative, unversioned server mutations and raw VM configurations are completely prohibited.

Our strategy rests on three unified, immutable pillars:
1. **Hardened Multi-Stage Containerization**: Every service packages its runtime inside a minimal, non-root container image with zero unnecessary compilers or attack surfaces.
2. **Cryptographic Container Salting & Supply-Chain Attestation**: Container images are bound to immutable SHA-256 digests, digitally signed using Cosign/Sigstore, and accompanied by verifiable SLSA provenance attestations.
3. **Serverless AWS EKS Fargate Deployment**: Workloads deploy into managed Amazon Elastic Kubernetes Service (EKS) clusters utilizing AWS Fargate serverless profiles, completely eliminating node lifecycle overhead, patch management, and cross-tenant privilege escalation.

---

## 2. Pillar 1: Hardened Containerization Architecture

### Multi-Stage Build Pipeline
Containers are constructed using a two-stage pattern:
- **Build Stage**: Installs package managers, compilers, build wheels, and TypeScript bundlers.
- **Runtime Stage**: Copies strictly compiled artifacts into a lightweight, hardened base image (e.g. `python:3.11-slim`, `node:20-alpine`, or Google `distroless/static`).

### Least Privilege Execution
- **Non-Root User**: Every container assigns a non-root UID/GID (`hath0r` with `UID 10001:GID 10001`).
- **Read-Only Root Filesystem**: Pods run with `readOnlyRootFilesystem: true`, restricting writable disk space to explicit ephemeral `emptyDir` volumes mounted under `/tmp`.
- **Health Probing**: Every container provides active `livenessProbe` and `readinessProbe` HTTP/command hooks.

---

## 3. Pillar 2: Container Salting & Cryptographic Supply Chain

Mutable Docker tags (e.g., `:latest`, `:dev`, `:v1.0.0`) present a catastrophic supply chain risk where identical tag identifiers point to different image binaries over time.

### The Salting Process
1. **Digest Pinning**: The CI pipeline builds the container and derives its exact cryptographic SHA-256 content digest:
   $$\text{Salted Digest} = \text{SHA256}(\text{Image Manifest Layer Bundle})$$
2. **Cosign Attestation & Keyless Signing**: The CI runner signs the digest using OpenID Connect (OIDC) identity tokens and Sigstore transparency logs (Rekor).
3. **SLSA Provenance Attestation**: An in-toto provenance predicate is attached to the image digest containing the exact Git commit SHA, workflow execution ID, and builder parameters.
4. **Secret Salting & Separation**: Production secrets and database credentials are never baked into image layers. Secrets are dynamically resolved and injected into the runtime via AWS Secrets Manager or Parameter Store using IAM Roles for Service Accounts (IRSA).

---

## 4. Pillar 3: AWS EKS / Fargate Serverless Delivery

### Fargate Architectural Guardrails
AWS Fargate abstracts underlying EC2 compute nodes by executing each Kubernetes pod in an isolated, dedicated MicroVM. To run reliably on Fargate, deployments must conform to the following invariants:
1. **No DaemonSets**: Workloads requiring host-level agents (like log collectors) must run as sidecars.
2. **No Privileged Containers**: `securityContext.privileged: true` is rejected by the Fargate admission controller.
3. **No Host Networking**: Pods receive private Elastic Network Interfaces (ENIs) directly in the VPC.
4. **Resource Sizing Compliance**: Pod CPU and memory `requests` and `limits` must match AWS Fargate resource allocation tables (e.g., 0.25 vCPU with 0.5–2 GB RAM; 1.0 vCPU with 2–8 GB RAM).
5. **ALB Ingress with IP Target Mode**: Ingress objects must declare `alb.ingress.kubernetes.io/target-type: ip` so the AWS Application Load Balancer routes directly to the Fargate pod ENIs.

---

## 5. Governance & Operator Interface

All IaC operations are orchestrated exclusively through the `hath0r iac` operator command suite:
- `hath0r iac audit`: Sweeps repositories in `~/Development` and flags containerization and IaC drift.
- `hath0r iac init`: Scaffolds standard Dockerfiles, `.dockerignore`, `k8s/` manifests, and `fargate-profile.yaml`.
- `hath0r iac validate`: Performs static AST validation, Dockerfile linting, and Fargate compatibility checks.
- `hath0r iac salt`: Computes SHA-256 digest pins and writes attestation receipts.
- `hath0r iac render`: Compiles parameterized manifests targeting canonical environments (`development`, `testing`, `staging`, `master`).
