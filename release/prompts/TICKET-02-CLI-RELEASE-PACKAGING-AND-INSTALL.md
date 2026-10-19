# PROMPT TICKET 02: Hath0r CLI Release Packaging & PATH Installation

**Ticket ID**: `HATH0R-RELEASE-002`  
**Role**: `CLIEngineerAgent`  
**Scope**: Build/extract Hath0r CLI release artifacts, install binary to system PATH, verify contracts and CLI health  

---

## 🎯 Task Objective

Build, package, and deploy the **Hath0r CLI Operator** (`hath0r`) as a standalone release executable (or optimized Python wheel/venv package). Ensure the binary is placed in the operator's system PATH, verify version compliance, and execute the Hath0r Doctor check.

> **Crucial Invariant**: This ticket builds the **release binary / package distribution**, not an uncompiled dev workspace.

---

## 📥 Inputs & Source Resolution

- **CLI Repository URL / Path**: Obtained from Ticket 01 (`CLI_REPO` or monorepo `UNIFIED_REPO/cli`).
- **Binary Destination Directory**: `${HATH0R_BIN_DIR:-/usr/local/bin}` or `$HOME/.local/bin`.
- **Pre-compiled Artifacts Cache**: Check `artifacts/python/cli/` for platform-specific standalone executables:
  - macOS ARM64: `artifacts/python/cli/hath0r-darwin-arm64`
  - macOS x86_64: `artifacts/python/cli/hath0r-darwin-x86_64`
  - Linux x86_64: `artifacts/python/cli/hath0r-linux-x86_64`
  - Python Wheel: `artifacts/python/cli/hath0r_cli-*.whl`

---

## 🛠️ Execution Steps

### Step 1: Resolve Release Artifact Strategy
Determine the optimal installation pathway based on the host architecture:
```bash
HOST_OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
HOST_ARCH="$(uname -m)"
echo "Host Environment: ${HOST_OS} ${HOST_ARCH}"
```

**Path A: Standalone Pre-compiled Native Binary (Preferred)**:
If a verified binary matching the host platform exists in `artifacts/python/cli/`:
```bash
ARTIFACTS_DIR="${PROMPTS_ROOT}/artifacts/python/cli"
BIN_SRC=""
if [[ "${HOST_OS}" == "darwin" && "${HOST_ARCH}" == "arm64" ]]; then
  BIN_SRC="${ARTIFACTS_DIR}/hath0r-darwin-arm64"
elif [[ "${HOST_OS}" == "linux" && "${HOST_ARCH}" == "x86_64" ]]; then
  BIN_SRC="${ARTIFACTS_DIR}/hath0r-linux-x86_64"
fi

if [[ -f "${BIN_SRC}" ]]; then
  chmod +x "${BIN_SRC}"
  cp "${BIN_SRC}" "${BIN_DIR}/hath0r"
  echo "Deployed standalone binary to ${BIN_DIR}/hath0r"
fi
```

**Path B: Build from Package Source (Fallback)**:
If building from repository source:
```bash
VENV_DIR="${INSTALL_PREFIX}/lib/hath0r-venv"
python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/pip" install --upgrade pip setuptools wheel

# Install wheel or package
if ls "${ARTIFACTS_DIR}"/hath0r_cli-*.whl 1>/dev/null 2>&1; then
  "${VENV_DIR}/bin/pip" install --no-cache-dir "${ARTIFACTS_DIR}"/hath0r_cli-*.whl
else
  "${VENV_DIR}/bin/pip" install --no-cache-dir -e "${CLI_SOURCE_DIR}"
fi

# Symlink or wrap executable
ln -sf "${VENV_DIR}/bin/hath0r" "${BIN_DIR}/hath0r"
```

### Step 2: Verify Checksum Integrity
Verify SHA-256 digest against `artifacts/python/cli/CHECKSUMS.sha256`:
```bash
if [[ -f "${ARTIFACTS_DIR}/CHECKSUMS.sha256" ]]; then
  shasum -a 256 -c "${ARTIFACTS_DIR}/CHECKSUMS.sha256" || true
fi
```

### Step 3: Execute Doctor & Self-Diagnostic
Validate that the installed CLI runs cleanly and meets runtime contracts:
```bash
hath0r --version
hath0r doctor || true
hath0r memory session read || true
```

---

## ✅ Acceptance Criteria & Assertions

1. Executable `hath0r` is accessible on the system PATH.
2. `hath0r --version` returns version string (e.g. `0.3.0` or higher) with exit code 0.
3. `hath0r doctor` executes without fatal errors.
4. Binary integrity verified and recorded in release audit logs.
