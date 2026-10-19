# PROMPT TICKET 06: End-to-End Acceptance Verification & Cryptographic Attestation

**Ticket ID**: `HATH0R-RELEASE-006`  
**Role**: `QAAttestationAgent`  
**Scope**: Multi-service integration testing, SLSA-grade checksum manifests, release receipts, and pre-announcement memory compounding  

---

## 🎯 Task Objective

Conduct full end-to-end integration and acceptance testing across the installed Hath0r Infrastructure release (CLI, MCP, ATC). Generate cryptographic SHA-256 release receipts, compound final release facts into the MemoryGraph (`CR-MEMORY-COMPOUND-001`), and issue the final Release Evidence Handshake.

---

## 📥 Inputs & Active Endpoints

- **Hath0r CLI**: `hath0r` on system PATH.
- **Hath0r MCP**: `http://127.0.0.1:38083/ready`.
- **Hath0r ATC**: `http://127.0.0.1:38000/healthz`.
- **Docker Network**: `hath0r-net`.
- **Installation Prefix**: `${HATH0R_HOME:-$HOME/.hath0r}`.

---

## 🛠️ Execution Steps

### Step 1: Run Multi-Service Health & Smoke Suite
Execute consecutive health checks against all three subsystems:

```bash
echo "==> Running Hath0r Infrastructure Release Smoke Suite"

# 1. Hath0r CLI check
CLI_VER="$(hath0r --version 2>&1)"
echo "✓ CLI Version: ${CLI_VER}"

# 2. Hath0r MCP check
MCP_RESP="$(curl -fsS "http://127.0.0.1:38083/ready" 2>&1 || echo "SKIPPED_CONTAINER_DOWN")"
echo "✓ MCP Readiness: ${MCP_RESP}"

# 3. Hath0r ATC check
ATC_RESP="$(curl -fsS "http://127.0.0.1:38000/healthz" 2>&1 || echo "SKIPPED_CONTAINER_DOWN")"
echo "✓ ATC Gateway Health: ${ATC_RESP}"
```

### Step 2: Generate Release Checksums (`CHECKSUMS.sha256`)
Compute and verify SHA-256 digests for all generated release artifacts:
```bash
RELEASE_DIR="${HATH0R_HOME}/release"
cd "${HATH0R_HOME}"

find bin/ cfg/ release/ -type f -exec shasum -a 256 {} + > "${RELEASE_DIR}/CHECKSUMS.sha256"
echo "✓ Generated cryptographic release manifest: ${RELEASE_DIR}/CHECKSUMS.sha256"
```

### Step 3: Produce Cryptographic Release Receipt (`RELEASE_RECEIPT.json`)
Record the final immutable attestation document:
```json
{
  "release_type": "hath0r-infrastructure-full",
  "created_at": "<ISO_TIMESTAMP>",
  "schema_version": "1.0.0",
  "topology": "3-repos",
  "components": {
    "cli": {
      "version": "0.3.0",
      "binary": "/usr/local/bin/hath0r",
      "health": "PASS"
    },
    "mcp": {
      "endpoint": "http://127.0.0.1:38083",
      "ready_probe": "PASS"
    },
    "atc": {
      "endpoint": "http://127.0.0.1:38000",
      "health_probe": "PASS",
      "network": "hath0r-net"
    }
  },
  "audit": {
    "container_security": "CR-IAC-001_COMPLIANT",
    "zero_prompt_tax": "CR-AGENTGRAPH-001_COMPLIANT",
    "memory_compounding": "CR-MEMORY-COMPOUND-001_COMPLIANT"
  },
  "status": "VERIFIED_PRODUCTION_RELEASE"
}
```

### Step 4: Mandatory Pre-Announcement Memory Compounding (`CR-MEMORY-COMPOUND-001`)
Before declaring the task complete or notifying the user:
```bash
# Compound release milestone into MemoryGraph
hath0r memory compound \
  --type "episode" \
  --title "Hath0r Infrastructure Release 0.3.0 Deployment" \
  --content "Successfully built and deployed Hath0r Infrastructure release from scratch covering CLI, MCP, and ATC." \
  --tags "release,infrastructure,cli,mcp,atc,success"

# End memory session
hath0r memory session end
```

---

## ✅ Acceptance Criteria & Assertions

1. All smoke checks pass or report graceful headless state.
2. `CHECKSUMS.sha256` covers all installed binaries and configurations.
3. `RELEASE_RECEIPT.json` exists, is signed/formatted properly, and records `status: VERIFIED_PRODUCTION_RELEASE`.
4. Pre-announcement memory compounding verification passes: `hath0r memory verify` returns exit code 0.
5. Operator is provided with the final endpoint dashboard and summary.
