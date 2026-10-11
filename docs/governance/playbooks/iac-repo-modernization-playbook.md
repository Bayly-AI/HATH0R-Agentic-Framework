# Playbook: Repository Modernization to Infrastructure as Code & EKS Fargate

> **Document Type:** Playbook  
> **Status:** Ratified  
> **Governing Standards:** `CR-IAC-001`, `CR-CLI-ENTRY-001`  
> **Target Subsystems:** Suite Repositories (`~/Development`)  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#260, Bayly-AI/HATH0R-CLI#441

---

## 1. Objective

Provide operational guidance for operators and autonomous bots to modernize existing legacy repositories in `~/Development` that lack containerization, cryptographic salting, or AWS EKS Fargate manifests.

---

## 2. Onboarding Workflow Matrix

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ 1. Audit Repo   │ ──> │ 2. Scaffold IaC  │ ──> │ 3. Validate Spec│ ──> │ 4. Open PR &    │
│ hath0r iac audit│     │ hath0r iac init  │     │hath0r iac validate    │ Deploy Fargate  │
└─────────────────┘     └──────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## 3. Execution Phases

### Phase 1: Repository Audit & Technology Detection
Run the global audit command from `HATH0R-CLI`:

```bash
hath0r iac audit --sweep /Users/raybayly/Development
```

For a specific repository:

```bash
hath0r iac audit /Users/raybayly/Development/BAI/UXP
```

The output identifies:
- Missing Dockerfiles
- Unhardened container patterns (running as root)
- Missing EKS Fargate profile and Kubernetes manifests (`k8s/`)

### Phase 2: Automated Scaffolding
Initialize the repository with production-ready IaC artifacts:

```bash
cd /Users/raybayly/Development/<Target-Repo>
hath0r iac init .
```

The bot inspects the project markers (`package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`) and scaffolds:
- `Dockerfile`: Hardened multi-stage build running as `UID 10001`.
- `.dockerignore`: Excludes `.git`, `.venv`, `node_modules`, `*.pyc`, `.env`.
- `fargate-profile.yaml`: Declares AWS EKS Fargate profile and namespace selectors.
- `k8s/deployment.yaml`: Kubernetes Deployment specifying CPU/memory Fargate brackets and salted image placeholders.
- `k8s/service.yaml`: ClusterIP service.
- `k8s/ingress.yaml`: AWS ALB Ingress with IP target annotations.
- `k8s/serviceaccount.yaml`: IRSA role binding.

### Phase 3: Specification Validation
Validate the generated configuration:

```bash
hath0r iac validate .
```

Ensure all 3 pillars pass:
- `[PASS] Container Security`: Non-root, multi-stage, healthcheck present.
- `[PASS] Salting Configuration`: Digest pinning configured.
- `[PASS] AWS Fargate Compatibility`: No privileged flags, valid resource brackets, ALB IP target enabled.

### Phase 4: Git PR & Continuous Delivery
1. Commit generated IaC files:
   ```bash
   git add Dockerfile .dockerignore fargate-profile.yaml k8s/
   git commit -m "feat(iac): Adopt Infrastructure as Code, hardened container, and EKS Fargate manifests"
   ```
2. Open pull request into `development`.
