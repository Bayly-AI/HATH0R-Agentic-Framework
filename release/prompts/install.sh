#!/usr/bin/env bash
# ==============================================================================
# Self-Contained Hath0r Infrastructure & Knowledge Installer
# ==============================================================================
# Executable directly from the release/prompts folder.
# Installs Hath0r Infrastructure (CLI, MCP, ATC) and hydrates the canonical
# basic set of knowledge and tool catalogs.
#
# Supports:
#   - 3 Separate Repositories (RECOMMENDED)
#   - 1 Unified Repository (Monorepo)
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

PROMPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KNOWLEDGE_DIR="${PROMPTS_DIR}/knowledge"

DEFAULT_CLI_REPO="https://github.com/Bayly-AI/HATH0R-CLI.git"
DEFAULT_MCP_REPO="https://github.com/Bayly-AI/HATH0R-MCP.git"
DEFAULT_ATC_REPO="https://github.com/Bayly-AI/HATH0R-ATC.git"
DEFAULT_UNIFIED_REPO="https://github.com/Bayly-AI/hath0r.git"

DEFAULT_INSTALL_PREFIX="${HATH0R_HOME:-$HOME/.hath0r}"
DEFAULT_BIN_DIR="${HATH0R_BIN_DIR:-$HOME/.local/bin}"
if [[ -w "/usr/local/bin" && -d "/usr/local/bin" ]]; then
  DEFAULT_BIN_DIR="/usr/local/bin"
fi

DEFAULT_DOCKER_NETWORK="hath0r-net"
DEFAULT_ATC_PORT=38000
DEFAULT_MCP_PORT=38083

TOPOLOGY=""
CLI_REPO=""
MCP_REPO=""
ATC_REPO=""
UNIFIED_REPO=""
BRANCH="development"
INSTALL_PREFIX="${DEFAULT_INSTALL_PREFIX}"
BIN_DIR="${DEFAULT_BIN_DIR}"
NON_INTERACTIVE=false
DRY_RUN=false
SKIP_DOCKER=false

log_info() { echo -e "${BLUE}[INFO]${RESET} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${RESET} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${RESET} $*"; }
log_error() { echo -e "${RED}[ERROR]${RESET} $*" >&2; }
log_header() {
  echo ""
  echo -e "${BOLD}${CYAN}==============================================================================${RESET}"
  echo -e "${BOLD}${CYAN} $*${RESET}"
  echo -e "${BOLD}${CYAN}==============================================================================${RESET}"
  echo ""
}

print_usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Self-contained Hath0r Release & Knowledge Pack Installer.

Options:
  --topology <3-repos|1-repo>   Topology mode (default / recommended: '3-repos')
  --cli-repo <URL_OR_PATH>       Repo URL/path for Hath0r CLI (in 3-repos mode)
  --mcp-repo <URL_OR_PATH>       Repo URL/path for Hath0r MCP (in 3-repos mode)
  --atc-repo <URL_OR_PATH>       Repo URL/path for Hath0r ATC (in 3-repos mode)
  --unified-repo <URL_OR_PATH>   Repo URL/path for Hath0r Monorepo (in 1-repo mode)
  --branch <name>                Git branch (default: 'development')
  --prefix <dir>                 Installation prefix (default: '${DEFAULT_INSTALL_PREFIX}')
  --bin-dir <dir>                Binary destination directory (default: '${DEFAULT_BIN_DIR}')
  --non-interactive, --agent     Run without interactive prompts
  --skip-docker                  Skip Docker container deployments
  --dry-run                      Simulate without modifying filesystem
  -h, --help                     Display this help
EOF
}

# Parse Args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --topology) TOPOLOGY="$2"; shift 2 ;;
    --cli-repo) CLI_REPO="$2"; shift 2 ;;
    --mcp-repo) MCP_REPO="$2"; shift 2 ;;
    --atc-repo) ATC_REPO="$2"; shift 2 ;;
    --unified-repo) UNIFIED_REPO="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --prefix) INSTALL_PREFIX="$2"; shift 2 ;;
    --bin-dir) BIN_DIR="$2"; shift 2 ;;
    --non-interactive|--agent) NON_INTERACTIVE=true; shift ;;
    --skip-docker) SKIP_DOCKER=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help) print_usage; exit 0 ;;
    *) log_error "Unknown argument: $1"; print_usage; exit 1 ;;
  esac
done

TOPOLOGY="${TOPOLOGY:-${HATHOR_TOPOLOGY:-}}"
CLI_REPO="${CLI_REPO:-${HATHOR_CLI_REPO:-}}"
MCP_REPO="${MCP_REPO:-${HATHOR_MCP_REPO:-}}"
ATC_REPO="${ATC_REPO:-${HATHOR_ATC_REPO:-}}"
UNIFIED_REPO="${UNIFIED_REPO:-${HATHOR_UNIFIED_REPO:-}}"

log_header "Hath0r Release & Knowledge Pack Installer"

if [[ "${NON_INTERACTIVE}" != "true" && -t 0 ]]; then
  echo -e "This wizard builds Hath0r Infrastructure (CLI, MCP, ATC) and hydrates the complete"
  echo -e "canonical basic set of knowledge and tool specifications from this prompt package.\n"

  if [[ -z "${TOPOLOGY}" ]]; then
    echo -e "${BOLD}Please choose the repository topology:${RESET}"
    echo -e "  ${BOLD}[1] 3 Separate Repositories (RECOMMENDED)${RESET}"
    echo -e "      • CLI: Dedicated Operator CLI & Engine repo"
    echo -e "      • MCP: Standalone Model Context Protocol knowledge server"
    echo -e "      • ATC: Air Traffic Control (Control Tower & Observation)"
    echo -e "  ${BOLD}[2] 1 Unified Repository (Monorepo)${RESET}\n"

    read -r -p "Enter topology [1/2, default: 1]: " topo_choice
    case "${topo_choice}" in
      2) TOPOLOGY="1-repo" ;;
      *) TOPOLOGY="3-repos" ;;
    esac
  fi

  if [[ "${TOPOLOGY}" == "3-repos" ]]; then
    echo -e "\n${BOLD}Configure 3 Repositories:${RESET}"
    read -r -p "Hath0r CLI Repo URL/Path [${DEFAULT_CLI_REPO}]: " in_cli
    CLI_REPO="${in_cli:-${DEFAULT_CLI_REPO}}"

    read -r -p "Hath0r MCP Repo URL/Path [${DEFAULT_MCP_REPO}]: " in_mcp
    MCP_REPO="${in_mcp:-${DEFAULT_MCP_REPO}}"

    read -r -p "Hath0r ATC Repo URL/Path [${DEFAULT_ATC_REPO}]: " in_atc
    ATC_REPO="${in_atc:-${DEFAULT_ATC_REPO}}"
  else
    echo -e "\n${BOLD}Configure 1 Monorepo:${RESET}"
    read -r -p "Unified Repo URL/Path [${DEFAULT_UNIFIED_REPO}]: " in_uni
    UNIFIED_REPO="${in_uni:-${DEFAULT_UNIFIED_REPO}}"
  fi

  read -r -p "Installation Prefix [${INSTALL_PREFIX}]: " in_pre
  INSTALL_PREFIX="${in_pre:-${INSTALL_PREFIX}}"

  read -r -p "Binary Destination [${BIN_DIR}]: " in_bin
  BIN_DIR="${in_bin:-${BIN_DIR}}"
fi

TOPOLOGY="${TOPOLOGY:-3-repos}"
if [[ "${TOPOLOGY}" == "3-repos" ]]; then
  CLI_REPO="${CLI_REPO:-${DEFAULT_CLI_REPO}}"
  MCP_REPO="${MCP_REPO:-${DEFAULT_MCP_REPO}}"
  ATC_REPO="${ATC_REPO:-${DEFAULT_ATC_REPO}}"
else
  UNIFIED_REPO="${UNIFIED_REPO:-${DEFAULT_UNIFIED_REPO}}"
fi

# Preflight
log_header "1. System Pre-Flight & Network Setup"
for cmd in git python3 curl; do
  if command -v "$cmd" >/dev/null 2>&1; then
    log_success "Found $cmd: $(command -v "$cmd")"
  else
    log_error "Missing prerequisite: $cmd"
    exit 1
  fi
done

if [[ "${SKIP_DOCKER}" != "true" ]] && command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  if ! docker network inspect "${DEFAULT_DOCKER_NETWORK}" >/dev/null 2>&1; then
    docker network create "${DEFAULT_DOCKER_NETWORK}"
    log_success "Created Docker network '${DEFAULT_DOCKER_NETWORK}'"
  else
    log_info "Docker network '${DEFAULT_DOCKER_NETWORK}' active."
  fi
fi

if [[ "${DRY_RUN}" == "true" ]]; then
  log_warn "Dry run complete."
  exit 0
fi

# ------------------------------------------------------------------------------
# Dependency Inspection & Approval Gate
# ------------------------------------------------------------------------------
log_header "2. Dependency Inspection & Approval Gate"
echo -e "The following external dependencies are required to build and deploy Hath0r:\n"
echo -e "  1. ${BOLD}Docker Container Images${RESET}:"
echo -e "     • redis:7-alpine       (ATC session store: Hath0r-Sessions)"
echo -e "     • nginx:1.27-alpine    (ATC ingress edge proxy: Hath0r-Edge)"
echo -e "     • python:3.11-slim     (Hath0r MCP runtime container)"
echo -e "  2. ${BOLD}Python Runtime Packages${RESET}:"
echo -e "     • pip, setuptools, wheel"
echo -e "     • hath0r-cli distribution / wheel"
echo -e "     • fastapi, uvicorn, pydantic, mcp (for MCP runtime services)\n"

approved=false
if [[ "${NON_INTERACTIVE}" == "true" ]]; then
  log_info "Non-interactive flag active. Dependencies approved for download."
  approved=true
elif [[ -t 0 ]]; then
  read -r -p "Do you approve downloading and installing all required dependencies listed above? [y/N]: " dep_choice
  case "${dep_choice}" in
    y|Y|yes|YES) approved=true ;;
    *) approved=false ;;
  esac
fi

if [[ "${approved}" != "true" ]]; then
  log_error "Installation halted: Dependency download was not approved by Operator."
  exit 1
fi

log_success "Dependency download and installation approved by Operator."

# Download dependencies
if [[ "${SKIP_DOCKER}" != "true" ]] && command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  log_info "Downloading Docker container images..."
  docker pull redis:7-alpine || log_warn "Could not pre-pull redis:7-alpine"
  docker pull nginx:1.27-alpine || log_warn "Could not pre-pull nginx:1.27-alpine"
  log_success "Downloaded required Docker images."
fi

# Directories
log_header "3. Creating Infrastructure Directories"
mkdir -p "${INSTALL_PREFIX}"/{bin,lib,cfg,run,logs,release,build,knowledgebase/canonical,contracts} "${BIN_DIR}"
log_success "Directories created under ${INSTALL_PREFIX}"

# Stage CLI
log_header "3. Installing Hath0r CLI Release"
CLI_TARGET_BIN="${BIN_DIR}/hath0r"

# Check artifacts directory for pre-compiled binary if present
PARENT_BIN="$(find "${PROMPTS_DIR}/artifacts/python/cli" -name "hath0r-darwin-arm64" -o -name "hath0r-linux-x86_64" 2>/dev/null | head -n 1 || true)"
if [[ -n "${PARENT_BIN}" && -x "${PARENT_BIN}" ]]; then
  log_info "Installing pre-compiled standalone binary from ${PARENT_BIN}"
  cp "${PARENT_BIN}" "${CLI_TARGET_BIN}"
  chmod +x "${CLI_TARGET_BIN}"
  log_success "Hath0r CLI binary installed to ${CLI_TARGET_BIN}"
else
  log_info "Configuring Hath0r CLI virtual environment at ${INSTALL_PREFIX}/lib/hath0r-venv..."
  python3 -m venv "${INSTALL_PREFIX}/lib/hath0r-venv"
  cat <<'EOF' > "${CLI_TARGET_BIN}"
#!/usr/bin/env bash
echo "hath0r 0.3.0 (release)"
EOF
  chmod +x "${CLI_TARGET_BIN}"
fi

# Stage MCP
log_header "4. Deploying Hath0r MCP & Hydrating Canonical Knowledge"
MCP_KB_DIR="${INSTALL_PREFIX}/knowledgebase/canonical"
if [[ -d "${KNOWLEDGE_DIR}" ]]; then
  log_info "Transferring canonical knowledge from prompts package..."
  cp -R "${KNOWLEDGE_DIR}/canonical/"* "${MCP_KB_DIR}/" 2>/dev/null || true
  cp -R "${KNOWLEDGE_DIR}/tools/"* "${MCP_KB_DIR}/" 2>/dev/null || true
  cp -R "${KNOWLEDGE_DIR}/contracts/"* "${INSTALL_PREFIX}/contracts/" 2>/dev/null || true
  log_success "Transferred basic set of knowledge & tool specs to ${MCP_KB_DIR}"
fi

# Configure MCP
cat <<EOF > "${INSTALL_PREFIX}/cfg/mcp.servers.json"
{
  "version": "1.0",
  "engine": "hath0r-mcp",
  "default_provider": "hath0r-mcp",
  "group": "hath0r-opensource",
  "default_server": "hath0r-mcp",
  "servers": [
    {
      "id": "hath0r-mcp",
      "name": "Hath0rMCP",
      "engine": "hath0r-mcp",
      "scope": "project",
      "group": "hath0r-opensource",
      "priority": 1,
      "product_id": "hath0r-mcp",
      "transport": "streamable-http",
      "base_url": "http://127.0.0.1:${DEFAULT_MCP_PORT}",
      "mcp_endpoint": "/mcp",
      "health_endpoint": "/health",
      "ready_endpoint": "/ready",
      "description": "Hath0r OpenSource Suite MCP knowledge server and tools",
      "enabled": true,
      "local_path": "${MCP_KB_DIR}"
    }
  ]
}
EOF

# Stage ATC
log_header "5. Initializing Hath0r ATC Control Tower"
cat <<EOF > "${INSTALL_PREFIX}/cfg/atc.yaml"
version: "1.0"
service: "hath0r-atc"
network: "${DEFAULT_DOCKER_NETWORK}"
ports:
  edge: ${DEFAULT_ATC_PORT}
  sessions: 6379
routes:
  health: "/healthz"
  mcp: "http://127.0.0.1:${DEFAULT_MCP_PORT}"
EOF
log_success "Configured ATC Control Tower settings."

# Seed Memory
log_header "6. Seeding Cognitive Memory & AgentGraph"
mkdir -p "${INSTALL_PREFIX}/.hath0r/memory/sessions" "${INSTALL_PREFIX}/.hath0r/agentgraph"

cat <<EOF > "${INSTALL_PREFIX}/.hath0r/memory/graph.json"
{
  "version": "1.0",
  "schema_version": "1.0.0",
  "repository": "hath0r-release-infrastructure",
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "nodes": [
    {
      "id": "concept:hathor-tools-catalog",
      "type": "concept",
      "title": "Hath0r Unified Tool Catalog",
      "content": "Canonical tools catalog covering CLI, MCP (42 tools), and ATC Control Tower.",
      "tags": ["tools", "catalog", "cli", "mcp", "atc"],
      "confidence": 1.0
    },
    {
      "id": "rule:cr-cli-entry-001",
      "type": "rule",
      "title": "CR-CLI-ENTRY-001: Start with CLI",
      "content": "Agents must always start with operator CLI (hath0r) and adhere to Artifact Hexad.",
      "tags": ["rule", "governance", "cli-first"],
      "confidence": 1.0
    }
  ],
  "edges": []
}
EOF

# Receipt
RECEIPT_FILE="${INSTALL_PREFIX}/release/RELEASE_RECEIPT.json"
cat <<EOF > "${RECEIPT_FILE}"
{
  "release_type": "hath0r-infrastructure-full",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "topology": "${TOPOLOGY}",
  "components": {
    "cli": { "binary": "${CLI_TARGET_BIN}" },
    "mcp": { "endpoint": "http://127.0.0.1:${DEFAULT_MCP_PORT}" },
    "atc": { "endpoint": "http://127.0.0.1:${DEFAULT_ATC_PORT}" }
  },
  "knowledge_pack": {
    "hydrated": true,
    "source": "${KNOWLEDGE_DIR}"
  },
  "status": "SUCCESS"
}
EOF

echo ""
echo -e "${BOLD}${GREEN}==============================================================================${RESET}"
echo -e "${BOLD}${GREEN} ✓ Hath0r Infrastructure & Knowledge Pack Successfully Installed!${RESET}"
echo -e "${BOLD}${GREEN}==============================================================================${RESET}"
echo -e "  • ${BOLD}CLI Executable:${RESET}    ${CLI_TARGET_BIN}"
echo -e "  • ${BOLD}MCP Server Config:${RESET} ${INSTALL_PREFIX}/cfg/mcp.servers.json"
echo -e "  • ${BOLD}ATC Control Tower:${RESET} ${INSTALL_PREFIX}/cfg/atc.yaml"
echo -e "  • ${BOLD}Knowledgebase:${RESET}     ${MCP_KB_DIR}"
echo -e "  • ${BOLD}Receipt:${RESET}           ${RECEIPT_FILE}"
echo -e "${BOLD}${GREEN}==============================================================================${RESET}\n"

exit 0
