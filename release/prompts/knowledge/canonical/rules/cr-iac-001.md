# CR-IAC-001: Mandatory Infrastructure as Code & Container Salting Standards

**Classification**: Critical Organizational Invariant (`RULE`)  
**Scope**: Org-wide across all services, bots, and containers  

---

## 📌 Rule Statement

1. **Mandatory Infrastructure as Code**:
   All services, MCP nodes, and background daemons must declare declarative IaC adhering to Hath0r schemas. Ad-hoc, imperative host deployments are strictly forbidden.

2. **Container Hardening Standards**:
   Every container image must adhere to multi-stage hardening:
   - Minimal slim/distroless/alpine runtime base image.
   - Non-root user execution (`UID 10001:GID 10001` or equivalent).
   - Explicit `HEALTHCHECK` directive.
   - Read-only root filesystem (`readOnlyRootFilesystem: true`) with tmpfs for temporary writes.
   - Dropped capabilities (`cap_drop: [ALL]`).

3. **Container Salting & Cryptographic Attestation**:
   Container images MUST NOT be deployed using mutable tags (e.g. `:latest`). Deployments must pin immutable cryptographic SHA-256 digests (`image@sha256:...`).
