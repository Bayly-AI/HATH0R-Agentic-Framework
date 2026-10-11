# Bot Specification: Infrastructure as Code Managing Bot

> **Document Type:** Bot Specification  
> **Status:** Ratified  
> **Governing Standards:** `CR-IAC-001`, `CR-CLI-FEATURE-STANDARD-001`  
> **Target Module:** `src/hath0r_cli/bots/iac_bot.py`  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#260, Bayly-AI/HATH0R-CLI#443

---

## 1. Identity & Role

- **Bot Name:** `IaCManagingBot`
- **Subsystem:** Control Tower Infrastructure as Code & Container Salting
- **Primary Mission:** Govern repository infrastructure compliance across `~/Development`: detect missing containerization, scaffold hardened multi-stage Dockerfiles, enforce cryptographic container salting, generate AWS EKS Fargate profiles and Kubernetes manifests, and prevent infrastructure drift.

---

## 2. Capabilities & Operational Methods

### `audit_workspace(path: Path, sweep: bool = False) -> Dict[str, Any]`
- Evaluates one or all repositories in `path`.
- Checks:
  - `has_dockerfile`: Validates existence and checks non-root user and multi-stage syntax.
  - `has_salting`: Checks presence of digest pins or signing receipts.
  - `has_fargate`: Checks `fargate-profile.yaml` and `k8s/` directory with valid ALB and resource requests.
- Returns comprehensive structured audit report.

### `init_iac(path: Path, tech_stack: Optional[str] = None, app_name: Optional[str] = None) -> Dict[str, Any]`
- Auto-detects technology stack (Python, Node/Vite, Go, Static).
- Generates:
  - Hardened multi-stage `Dockerfile`.
  - Production `.dockerignore`.
  - Canonical `fargate-profile.yaml` conforming to `contracts/hath0r-fargate-profile-v1.schema.json`.
  - Kubernetes resources in `k8s/` (`deployment.yaml`, `service.yaml`, `ingress.yaml`, `serviceaccount.yaml`).
  - Declarative IaC specification in `.hath0r/iac/spec.yaml` conforming to `contracts/hath0r-iac-spec-v1.schema.json`.

### `validate_iac(path: Path) -> Dict[str, Any]`
- Validates 3 pillars:
  1. **Container Security**: Non-root user (`UID >= 1000`), multi-stage syntax, explicit `HEALTHCHECK`.
  2. **Salting**: Digest pinning, signature verification hooks.
  3. **AWS Fargate Compatibility**: No `privileged: true`, no `hostPath`, resource limits matching Fargate sizing brackets, ALB Ingress target type set to `ip`.

### `salt_container(image: str, workspace: Optional[Path] = None) -> Dict[str, Any]`
- Computes SHA-256 digest of image.
- Creates Cosign signature attestation and records provenance receipt.

### `render_manifests(path: Path, environment: str = "development") -> Dict[str, Any]`
- Synthesizes parameterized manifests into `build/iac/<environment>/`.

---

## 3. RBAC & Security Boundaries

- Read access to local repository files.
- Write access restricted to: `Dockerfile`, `.dockerignore`, `fargate-profile.yaml`, `k8s/`, `.hath0r/iac/`, and `build/iac/`.
- No modification of application source logic or business contracts.
