# PROMPT TICKET 01: Topology Selection, Repo URL Intake & System Preflight

**Ticket ID**: `HATH0R-RELEASE-001`  
**Role**: `InfrastructureDevOpsAgent`  
**Scope**: Prerequisite validation, repository linkage, Docker network bridge, and staging directory preparation  

---

## 🎯 Task Objective

Prompt the Operator for the repository link(s) (either 3 separate repositories or 1 unified repository), validate all system runtime prerequisites, establish the shared bridge network `hath0r-net`, and prepare the release staging directory tree.

---

## 📥 Inputs & Intake Protocol

### 1. Topology Resolution
Prompt or check for:
- **Topology Preference**:
  - `3-repos` (**RECOMMENDED**): Enables independent versioning, minimal blast radius, and clean separation between CLI, MCP, and ATC.
  - `1-repo`: Single monorepo housing all components.

### 2. Repository Link Intake
If `3-repos` is selected, collect:
- **Hath0r CLI Repo**: Link to repository containing Hath0r CLI (Default: `https://github.com/Bayly-AI/HATH0R-CLI.git` or local path `/Users/raybayly/Development/OpenSource/hathor-cli`).
- **Hath0r MCP Repo**: Link to repository containing Hath0r MCP (Default: `https://github.com/Bayly-AI/HATH0R-MCP.git` or local path `/Users/raybayly/Development/OpenSource/hath0r-mcp`).
- **Hath0r ATC Repo**: Link to repository containing Hath0r ATC (Default: `https://github.com/Bayly-AI/HATH0R-ATC.git` or local path `/Users/raybayly/Development/OpenSource/hath0r-atc`).

If `1-repo` is selected, collect:
- **Unified Repo**: Link to single repository containing CLI, MCP, and ATC (Default: `https://github.com/Bayly-AI/hath0r.git` or local path).
- Subdirectory paths: `cli/`, `mcp/`, `atc/`.

---

## 🛠️ Execution Steps

### Step 1: System Prerequisite Check
Verify the following CLI tools exist and have compatible versions:
```bash
# Verify Git
git --version || { echo "Git required"; exit 1; }

# Verify Python >= 3.10
python3 -c "import sys; assert sys.version_info >= (3, 10), 'Python >= 3.10 required'"

# Verify cURL
curl --version

# Verify Docker runtime
docker info >/dev/null 2>&1 || echo "WARNING: Docker daemon not reachable. Container deployment may be deferred."
```

### Step 2: Dependency Inspection & Mandatory Operator Approval Gate
Before downloading or installing any external dependencies, the agent MUST present the list of required dependencies to the Operator and obtain explicit approval:

```text
Dependencies Requiring Approval:
1. Docker Container Images:
   - redis:7-alpine (ATC session state store: Hath0r-Sessions)
   - nginx:1.27-alpine (ATC ingress reverse proxy edge: Hath0r-Edge)
   - python:3.11-slim (MCP server container base image)
2. Python Packages & Tools:
   - pip, setuptools, wheel
   - hath0r-cli distribution / wheel
   - fastapi, uvicorn, pydantic, mcp (for MCP standalone mode)
```

Prompt the Operator:
`"Do you approve downloading and installing all required dependencies listed above? [y/N]"`

> ⚠️ **Hard Gate**: If the Operator declines, do NOT attempt to download packages or pull container images. Halt or operate in dry-run mode.

### Step 3: Download & Install Approved Dependencies
Upon receiving Operator approval:
```bash
# Pull container images
if docker info >/dev/null 2>&1; then
  docker pull redis:7-alpine
  docker pull nginx:1.27-alpine
  echo "✓ Successfully downloaded required Docker images."
fi

# Prepare Python dependencies
python3 -m venv "${INSTALL_PREFIX}/lib/hath0r-venv"
"${INSTALL_PREFIX}/lib/hath0r-venv/bin/pip" install --upgrade pip setuptools wheel
echo "✓ Successfully installed base Python packaging dependencies."
```

### Step 4: Establish the Shared Docker Bridge Network
All Hath0r containers (`Hath0r-Sessions`, `Hath0r-Edge`, `Hath0r-MCP`) communicate over `hath0r-net`.
```bash
if ! docker network inspect hath0r-net >/dev/null 2>&1; then
  docker network create hath0r-net
  echo "Created bridge network: hath0r-net"
else
  echo "Bridge network hath0r-net already active"
fi
```

### Step 3: Create Release Staging Filetree
Prepare the target release directory structure:
```bash
INSTALL_PREFIX="${HATH0R_HOME:-$HOME/.hath0r}"
mkdir -p "${INSTALL_PREFIX}"/{bin,lib,cfg,run,logs,release,build}
```

### Step 4: Write Preflight Manifest
Create `${INSTALL_PREFIX}/release/preflight-report.json`:
```json
{
  "topology": "3-repos",
  "repos": {
    "cli": "<CLI_REPO_URL>",
    "mcp": "<MCP_REPO_URL>",
    "atc": "<ATC_REPO_URL>"
  },
  "network": "hath0r-net",
  "timestamp": "<ISO_TIMESTAMP>",
  "preflight_status": "PASSED"
}
```

---

## ✅ Acceptance Criteria & Assertions

1. `docker network inspect hath0r-net` returns exit code 0.
2. Target directories `${INSTALL_PREFIX}/{bin,lib,cfg,run,logs,release}` exist and are writable.
3. `preflight-report.json` is generated with valid JSON syntax conforming to schema standards.
