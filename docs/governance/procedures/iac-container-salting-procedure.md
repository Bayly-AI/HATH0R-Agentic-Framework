# Procedure: Container Hardening, Salting & Cryptographic Attestation

> **Document Type:** Standard Operating Procedure (SOP)  
> **Status:** Ratified  
> **Governing Standards:** `CR-IAC-001`, `CR-CLI-ENTRY-001`  
> **Target Subsystems:** Build & Packaging Subsystems, CI Workflows  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#260, Bayly-AI/HATH0R-CLI#442

---

## 1. Purpose & Scope

This procedure defines the step-by-step instructions for packaging applications into hardened container images, calculating immutable cryptographic digests, attaching digital supply-chain signatures (Cosign), and applying secret salting before deployment to AWS EKS Fargate.

---

## 2. Prerequisites

- HATH0R Operator CLI installed and aliased (`hath0r`).
- Docker build engine or BuildKit daemon active.
- AWS CLI configured with valid credentials in `~/.credentials/aws/`.
- Cosign installed (`cosign version >= 2.0.0`).

---

## 3. Execution Steps

### Step 1: Scaffold Standard Hardened Dockerfile
Run the operator CLI to generate the multi-stage Dockerfile tailored to the target technology stack:

```bash
hath0r iac init . --tech-stack <python|node|go|static> --app-name <service-name>
```

Verify that the generated Dockerfile includes:
- Non-root user directive: `USER hath0r` (`UID 10001`).
- Multi-stage build separation (`FROM ... AS builder` and `FROM ... AS runner`).
- Explicit `HEALTHCHECK` command.

### Step 2: Build Container Image
Execute the build using BuildKit:

```bash
DOCKER_BUILDKIT=1 docker build -t <registry>/<service-name>:build-tmp .
```

### Step 3: Salt the Container (Digest Pinning & Signing)
Run the salting coordinator via CLI:

```bash
hath0r iac salt <registry>/<service-name>:build-tmp
```

The salting engine executes:
1. Pushes image to Amazon Elastic Container Registry (ECR).
2. Retrieves the immutable sha256 repository digest:
   ```text
   <registry>/<service-name>@sha256:d8b248a851...
   ```
3. Generates the Cosign signature and uploads the signature manifest:
   ```bash
   cosign sign --yes <registry>/<service-name>@sha256:...
   ```
4. Attaches SLSA Level 3 Provenance predicate.
5. Emits `iac-salt-receipt.json` in `.hath0r/iac/`.

### Step 4: Verification & Gate Enforcement
Verify image signature prior to promoting to Kubernetes:

```bash
cosign verify <registry>/<service-name>@sha256:...
```

Verify that the output contains the verified issuer identity and subject without errors.
