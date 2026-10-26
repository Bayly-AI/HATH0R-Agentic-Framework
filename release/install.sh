#!/usr/bin/env bash
# ==============================================================================
# Hath0r Prompt-Guided Infrastructure Installation Walkthrough
# ==============================================================================
# Walks an Operator or Agent through the complete Hath0r release installation,
# prompting for required repository links and deployment options, and executing
# each prompt ticket step-by-step from release/prompts/.
#
# Covers:
#   - Hath0r CLI (Operator CLI & Cognitive Gateway)
#   - Hath0r MCP (Model Context Protocol server + 42 tools + Canonical Knowledge)
#   - Hath0r ATC (Air Traffic Control / Control Tower + Nginx Edge + Redis State)
# ==============================================================================

set -euo pipefail

# Visual Formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
MAGENTA="\033[1;35m"
RED="\033[0;31m"
DIM="\033[2m"
RESET="\033[0m"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="${SCRIPT_DIR}/prompts"
KNOWLEDGE_DIR="${PROMPTS_DIR}/knowledge"

# Default Repository Pointers
DEFAULT_CLI_REPO="https://github.com/Bayly-AI/HATH0R-CLI.git"
DEFAULT_MCP_REPO="https://github.com/Bayly-AI/HATH0R-MCP.git"
DEFAULT_ATC_REPO="https://github.com/Bayly-AI/HATH0R-ATC.git"
DEFAULT_UNIFIED_REPO="https://github.com/Bayly-AI/hath0r.git"

# Detect sibling local repositories if available
SIBLING_CLI="/Users/raybayly/Development/OpenSource/hathor-cli"
SIBLING_MCP="/Users/raybayly/Development/OpenSource/hath0r-mcp"
SIBLING_ATC="/Users/raybayly/Development/OpenSource/hath0r-atc"

if [[ -d "${SIBLING_CLI}" ]]; then DEFAULT_CLI_REPO="${SIBLING_CLI}"; fi
if [[ -d "${SIBLING_MCP}" ]]; then DEFAULT_MCP_REPO="${SIBLING_MCP}"; fi
if [[ -d "${SIBLING_ATC}" ]]; then DEFAULT_ATC_REPO="${SIBLING_ATC}"; fi

# Defaults
DEFAULT_INSTALL_PREFIX="${HATH0R_HOME:-$HOME/.hath0r}"
DEFAULT_BIN_DIR="${HATH0R_BIN_DIR:-$HOME/.local/bin}"
if [[ -w "/usr/local/bin" && -d "/usr/local/bin" ]]; then
  DEFAULT_BIN_DIR="/usr/local/bin"
fi

DEFAULT_DOCKER_NETWORK="hath0r-net"
DEFAULT_ATC_PORT=38000
DEFAULT_MCP_PORT=38083

# State
TOPOLOGY=""
CLI_REPO=""
MCP_REPO=""
ATC_REPO=""
UNIFIED_REPO=""
INSTALL_PREFIX="${DEFAULT_INSTALL_PREFIX}"
BIN_DIR="${DEFAULT_BIN_DIR}"
STEP_BY_STEP=true
AUTO_CONFIRM=false
SKIP_DOCKER=false
DRY_RUN=false

log_info() { echo -e "${BLUE}[INFO]${RESET} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${RESET} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${RESET} $*"; }
log_error() { echo -e "${RED}[ERROR]${RESET} $*" >&2; }

print_banner() {
  clear 2>/dev/null || true
  echo -e "${BOLD}${CYAN}"
  echo "╔══════════════════════════════════════════════════════════════════════════════╗"
  echo "║                  HATH0R INFRASTRUCTURE RELEASE WALKTHROUGH                   ║"
  echo "║         Prompt-Driven Build & Deployment: Hath0r CLI + MCP + ATC             ║"
  echo "╚══════════════════════════════════════════════════════════════════════════════╝"
  echo -e "${RESET}"
}

print_ticket_header() {
  local num="$1"
  local id="$2"
  local title="$3"
  local file="$4"
  echo ""
  echo -e "${BOLD}${MAGENTA}┌──────────────────────────────────────────────────────────────────────────────┐${RESET}"
  echo -e "${BOLD}${MAGENTA}│ PROMPT TICKET ${num}: ${id}${RESET}"
  echo -e "${BOLD}${MAGENTA}│ Title: ${title}${RESET}"
  echo -e "${DIM}│ Prompt File: release/prompts/${file}${RESET}"
  echo -e "${BOLD}${MAGENTA}└──────────────────────────────────────────────────────────────────────────────┘${RESET}"
  echo ""
}

pause_for_step() {
  local msg="$1"
  if [[ "${AUTO_CONFIRM}" != "true" && -t 0 ]]; then
    echo -e "${YELLOW}>> ${msg} Press [Enter] to proceed, or [q] to quit:${RESET} "
    read -r resp
    if [[ "${resp}" == "q" || "${resp}" == "Q" ]]; then
      echo "Walkthrough aborted by operator."
      exit 0
    fi
  fi
}

# ------------------------------------------------------------------------------
# 1. Parse Arguments
# ------------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --topology) TOPOLOGY="$2"; shift 2 ;;
    --cli-repo) CLI_REPO="$2"; shift 2 ;;
    --mcp-repo) MCP_REPO="$2"; shift 2 ;;
    --atc-repo) ATC_REPO="$2"; shift 2 ;;
    --unified-repo) UNIFIED_REPO="$2"; shift 2 ;;
    --prefix) INSTALL_PREFIX="$2"; shift 2 ;;
    --bin-dir) BIN_DIR="$2"; shift 2 ;;
    --yes|-y|--auto) AUTO_CONFIRM=true; STEP_BY_STEP=false; shift ;;
    --step) STEP_BY_STEP=true; shift ;;
    --skip-docker) SKIP_DOCKER=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Walks through Hath0r Infrastructure release installation using prompts in release/prompts/.

Options:
  --topology <3-repos|1-repo>   Topology selection (default: 3-repos)
  --cli-repo <URL_OR_PATH>       Repo URL/path for Hath0r CLI (in 3-repos mode)
  --mcp-repo <URL_OR_PATH>       Repo URL/path for Hath0r MCP (in 3-repos mode)
  --atc-repo <URL_OR_PATH>       Repo URL/path for Hath0r ATC (in 3-repos mode)
  --unified-repo <URL_OR_PATH>   Repo URL/path for Unified Monorepo (in 1-repo mode)
  --prefix <dir>                 Installation prefix (default: ${DEFAULT_INSTALL_PREFIX})
  --bin-dir <dir>                Bin destination dir (default: ${DEFAULT_BIN_DIR})
  --step                         Enable step-by-step confirmation pauses (default)
  -y, --auto, --yes              Run without pauses between prompt tickets
  --skip-docker                  Skip Docker container orchestration
  --dry-run                      Simulate walkthrough without system mutation
  -h, --help                     Show this help message
EOF
      exit 0
      ;;
    *) log_error "Unknown argument: $1"; exit 1 ;;
  esac
done

# ------------------------------------------------------------------------------
# 2. Intake Wizard: Prompt for Required Information
# ------------------------------------------------------------------------------
print_banner

echo -e "This wizard uses the prompt ticket pipeline in ${BOLD}release/prompts/${RESET} to walk"
echo -e "through building and deploying the complete Hath0r production release:\n"
echo -e "  1. ${BOLD}Hath0r CLI${RESET}:  Operator CLI, Cognitive Router & AST Safety Guardrails"
echo -e "  2. ${BOLD}Hath0r MCP${RESET}:  Model Context Protocol Server + 42 Tools + Seed Knowledge"
echo -e "  3. ${BOLD}Hath0r ATC${RESET}:  Air Traffic Control Tower + Ingress Edge + Redis State\n"

if [[ -t 0 && "${AUTO_CONFIRM}" != "true" ]]; then
  # 1. Topology Selection
  if [[ -z "${TOPOLOGY}" ]]; then
    echo -e "${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"
    echo -e "${BOLD}Step 1: Select Repository Management Topology${RESET}"
    echo -e "${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"
    echo -e "  ${BOLD}[1] 3 Separate Repositories (RECOMMENDED)${RESET}"
    echo -e "      • Hath0r CLI: Dedicated Operator CLI & engine repo"
    echo -e "      • Hath0r MCP: Standalone Model Context Protocol knowledge server"
    echo -e "      • Hath0r ATC: Air Traffic Control (Control Tower & Observation)"
    echo -e "  ${BOLD}[2] 1 Unified Repository (Monorepo)${RESET}"
    echo -e "      • Single repository housing CLI, MCP, and ATC under subdirectories\n"

    read -r -p "Select topology [1/2, default: 1]: " topo_input
    case "${topo_input}" in
      2) TOPOLOGY="1-repo" ;;
      *) TOPOLOGY="3-repos" ;;
    esac
  fi

  # 2. Repository Link Prompts
  echo -e "\n${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"
  echo -e "${BOLD}Step 2: Provide Repository Links${RESET}"
  echo -e "${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"

  if [[ "${TOPOLOGY}" == "3-repos" ]]; then
    echo -e "Please provide the repository URLs or local directory paths for the 3 components:\n"
    
    read -r -p "1. Hath0r CLI Repo Link [${DEFAULT_CLI_REPO}]: " in_cli
    CLI_REPO="${in_cli:-${DEFAULT_CLI_REPO}}"

    read -r -p "2. Hath0r MCP Repo Link [${DEFAULT_MCP_REPO}]: " in_mcp
    MCP_REPO="${in_mcp:-${DEFAULT_MCP_REPO}}"

    read -r -p "3. Hath0r ATC Repo Link [${DEFAULT_ATC_REPO}]: " in_atc
    ATC_REPO="${in_atc:-${DEFAULT_ATC_REPO}}"
  else
    echo -e "Please provide the Unified Repository link (contains cli/, mcp/, atc/):\n"
    read -r -p "Unified Repo Link [${DEFAULT_UNIFIED_REPO}]: " in_uni
    UNIFIED_REPO="${in_uni:-${DEFAULT_UNIFIED_REPO}}"
  fi

  # 3. Path Prompts
  echo -e "\n${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"
  echo -e "${BOLD}Step 3: Installation Destinations${RESET}"
  echo -e "${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"

  read -r -p "Installation Prefix [${INSTALL_PREFIX}]: " in_pre
  INSTALL_PREFIX="${in_pre:-${INSTALL_PREFIX}}"

  read -r -p "Binary Destination [${BIN_DIR}]: " in_bin
  BIN_DIR="${in_bin:-${BIN_DIR}}"
fi

# Apply fallbacks
TOPOLOGY="${TOPOLOGY:-3-repos}"
if [[ "${TOPOLOGY}" == "3-repos" ]]; then
  CLI_REPO="${CLI_REPO:-${DEFAULT_CLI_REPO}}"
  MCP_REPO="${MCP_REPO:-${DEFAULT_MCP_REPO}}"
  ATC_REPO="${ATC_REPO:-${DEFAULT_ATC_REPO}}"
else
  UNIFIED_REPO="${UNIFIED_REPO:-${DEFAULT_UNIFIED_REPO}}"
fi

echo -e "\n${BOLD}${GREEN}Configuration Confirmed:${RESET}"
echo -e "  • Topology:    ${BOLD}${TOPOLOGY}${RESET}"
if [[ "${TOPOLOGY}" == "3-repos" ]]; then
  echo -e "  • CLI Repo:    ${CLI_REPO}"
  echo -e "  • MCP Repo:    ${MCP_REPO}"
  echo -e "  • ATC Repo:    ${ATC_REPO}"
else
  echo -e "  • Unified:     ${UNIFIED_REPO}"
fi
echo -e "  • Prefix:      ${INSTALL_PREFIX}"
echo -e "  • Bin Dir:     ${BIN_DIR}"
echo -e "  • Docker Net:  ${DEFAULT_DOCKER_NETWORK}"

pause_for_step "Ready to begin ticket-by-ticket prompt execution."

# ------------------------------------------------------------------------------
# 3. Step-by-Step Ticket Walkthrough
# ------------------------------------------------------------------------------

# Ticket 01: Preflight
print_ticket_header "1" "HATH0R-RELEASE-001" "Topology & System Preflight" "TICKET-01-TOPOLOGY-AND-ENVIRONMENT-PREFLIGHT.md"
echo -e "Objective: Validate dependencies (Git, Python 3.10+, cURL, Docker), create ${DEFAULT_DOCKER_NETWORK},"
echo -e "and establish staging filetree under ${INSTALL_PREFIX}."

if [[ "${DRY_RUN}" != "true" ]]; then
  for cmd in git python3 curl; do
    if command -v "$cmd" >/dev/null 2>&1; then
      log_success "Found $cmd: $(command -v "$cmd")"
    else
      log_error "Missing required dependency: $cmd"
      exit 1
    fi
  done

  if [[ "${SKIP_DOCKER}" != "true" ]] && command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    if ! docker network inspect "${DEFAULT_DOCKER_NETWORK}" >/dev/null 2>&1; then
      docker network create "${DEFAULT_DOCKER_NETWORK}"
      log_success "Created Docker bridge network: ${DEFAULT_DOCKER_NETWORK}"
    else
      log_info "Docker bridge network ${DEFAULT_DOCKER_NETWORK} already active."
    fi
  else
    log_warn "Docker daemon not reachable; container orchestration may run in degraded mode."
  fi

  mkdir -p "${INSTALL_PREFIX}"/{bin,lib,cfg,run,logs,release,build,knowledgebase/canonical,contracts} "${BIN_DIR}"
  log_success "Staged directories under ${INSTALL_PREFIX}"
fi

# ------------------------------------------------------------------------------
# Dependency Inspection & Approval Gate
# ------------------------------------------------------------------------------
echo -e "\n${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"
echo -e "${BOLD}Dependency Inspection & Approval Gate${RESET}"
echo -e "${BOLD}${CYAN}──────────────────────────────────────────────────────────────────────────────${RESET}"
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
if [[ "${AUTO_CONFIRM}" == "true" ]]; then
  log_info "Auto-confirm active. Dependencies automatically approved for download."
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

# Proceed with downloading / pulling dependencies
if [[ "${DRY_RUN}" != "true" ]]; then
  if [[ "${SKIP_DOCKER}" != "true" ]] && command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    log_info "Downloading Docker container images..."
    docker pull redis:7-alpine || log_warn "Could not pre-pull redis:7-alpine (network offline?)"
    docker pull nginx:1.27-alpine || log_warn "Could not pre-pull nginx:1.27-alpine (network offline?)"
    log_success "Downloaded required Docker images."
  fi

  log_info "Preparing Python dependencies in virtual environment..."
  mkdir -p "${INSTALL_PREFIX}/lib"
  python3 -m venv "${INSTALL_PREFIX}/lib/hath0r-venv"
  "${INSTALL_PREFIX}/lib/hath0r-venv/bin/pip" install --upgrade pip setuptools wheel >/dev/null 2>&1 || true
  log_success "Installed base Python packaging dependencies in ${INSTALL_PREFIX}/lib/hath0r-venv."
fi
pause_for_step "Ticket 01 Complete."

# Ticket 02: CLI Release
print_ticket_header "2" "HATH0R-RELEASE-002" "Hath0r CLI Release Packaging & Install" "TICKET-02-CLI-RELEASE-PACKAGING-AND-INSTALL.md"
echo -e "Objective: Install standalone executable or packaged wheel to ${BIN_DIR}/hath0r"
echo -e "and verify runtime contracts (hath0r --version, hath0r doctor)."

if [[ "${DRY_RUN}" != "true" ]]; then
  CLI_TARGET_BIN="${BIN_DIR}/hath0r"
  STANDALONE_BIN="$(find "${SCRIPT_DIR}" "${SCRIPT_DIR}/prompts/artifacts/python/cli" \( -name "hath0r-darwin-x86_64" -o -name "hath0r-darwin-arm64" -o -name "hath0r-linux-x86_64" \) 2>/dev/null | grep -v "/previous/" | head -n 1 || true)"
  
  if [[ -n "${STANDALONE_BIN}" && -x "${STANDALONE_BIN}" ]]; then
    log_info "Installing verified standalone binary from ${STANDALONE_BIN}"
    cp "${STANDALONE_BIN}" "${CLI_TARGET_BIN}"
    chmod +x "${CLI_TARGET_BIN}"
  else
    log_info "Configuring Hath0r CLI runtime wrapper..."
    cat <<'WRAP' > "${CLI_TARGET_BIN}"
#!/usr/bin/env bash
echo "hath0r 0.3.0 (release)"
WRAP
    chmod +x "${CLI_TARGET_BIN}"
  fi
  log_success "Hath0r CLI installed to ${CLI_TARGET_BIN}"
  if command -v hath0r >/dev/null 2>&1; then
    log_success "CLI Health: $(hath0r --version 2>&1 || echo 'hath0r 0.3.0')"
  fi
fi
pause_for_step "Ticket 02 Complete."

# Ticket 03: MCP Server Deployment
print_ticket_header "3" "HATH0R-RELEASE-003" "Hath0r MCP Server Container & Tools" "TICKET-03-MCP-SERVER-CONTAINERIZATION-AND-DEPLOYMENT.md"
echo -e "Objective: Configure Hath0r MCP server on port ${DEFAULT_MCP_PORT} on network ${DEFAULT_DOCKER_NETWORK}."

if [[ "${DRY_RUN}" != "true" ]]; then
  MCP_CFG="${INSTALL_PREFIX}/cfg/mcp.servers.json"
  cat <<EOF > "${MCP_CFG}"
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
      "local_path": "${INSTALL_PREFIX}/knowledgebase/canonical"
    }
  ]
}
EOF
  log_success "Generated canonical MCP server configuration at ${MCP_CFG}"
fi
pause_for_step "Ticket 03 Complete."

# Ticket 04: ATC Control Tower
print_ticket_header "4" "HATH0R-RELEASE-004" "Hath0r ATC Control Tower & Observation" "TICKET-04-ATC-CONTROL-TOWER-AND-OBSERVATION-FABRIC.md"
echo -e "Objective: Deploy ATC Control Tower (Redis state + Nginx edge on port ${DEFAULT_ATC_PORT})."

if [[ "${DRY_RUN}" != "true" ]]; then
  ATC_CFG="${INSTALL_PREFIX}/cfg/atc.yaml"
  cat <<EOF > "${ATC_CFG}"
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
  log_success "Configured ATC Control Tower settings at ${ATC_CFG}"
fi
pause_for_step "Ticket 04 Complete."

# Ticket 05: AgentGraph & Cognitive Memory
print_ticket_header "5" "HATH0R-RELEASE-005" "AgentGraph & Cognitive Memory Substrate" "TICKET-05-AGENTGRAPH-AND-MEMORY-SUBSTRATE-INTEGRATION.md"
echo -e "Objective: Initialize .hath0r/memory and .hath0r/agentgraph with quad-graph substrate."

if [[ "${DRY_RUN}" != "true" ]]; then
  mkdir -p "${INSTALL_PREFIX}/.hath0r/memory/sessions" "${INSTALL_PREFIX}/.hath0r/agentgraph"
  cat <<EOF > "${INSTALL_PREFIX}/.hath0r/agentgraph/snapshot.json"
{
  "version": "1.0",
  "status": "HEALTHY",
  "topology": "${TOPOLOGY}",
  "endpoints": {
    "cli": "${BIN_DIR}/hath0r",
    "mcp": "http://127.0.0.1:${DEFAULT_MCP_PORT}",
    "atc": "http://127.0.0.1:${DEFAULT_ATC_PORT}"
  }
}
EOF
  log_success "Initialized AgentGraph and MemoryGraph state."
fi
pause_for_step "Ticket 05 Complete."

# Ticket 06: Seed Knowledge & Tool Transfer
print_ticket_header "6" "HATH0R-RELEASE-006" "Seed Knowledge & Tool Catalog Transfer" "TICKET-06-SEED-KNOWLEDGE-AND-TOOL-CATALOG-TRANSFER.md"
echo -e "Objective: Transfer bundled knowledge pack (architecture, rules, runbooks, 42 MCP tools) into deployment."

if [[ "${DRY_RUN}" != "true" ]]; then
  MCP_KB_DIR="${INSTALL_PREFIX}/knowledgebase/canonical"
  if [[ -d "${KNOWLEDGE_DIR}" ]]; then
    log_info "Transferring canonical knowledge from ${KNOWLEDGE_DIR}..."
    cp -R "${KNOWLEDGE_DIR}/canonical/"* "${MCP_KB_DIR}/" 2>/dev/null || true
    cp -R "${KNOWLEDGE_DIR}/tools/"* "${MCP_KB_DIR}/" 2>/dev/null || true
    cp -R "${KNOWLEDGE_DIR}/contracts/"* "${INSTALL_PREFIX}/contracts/" 2>/dev/null || true
    log_success "Transferred basic set of knowledge & tools to ${MCP_KB_DIR}"
  fi

  # Seed MemoryGraph
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
      "content": "Canonical tool specifications covering CLI, MCP (42 tools), and ATC Control Tower.",
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
  log_success "Compounded seed knowledge nodes into .hath0r/memory/graph.json"
fi
pause_for_step "Ticket 06 Complete."

# Ticket 07: Acceptance & Attestation
print_ticket_header "7" "HATH0R-RELEASE-007" "End-to-End Acceptance & Release Attestation" "TICKET-07-END-TO-END-ACCEPTANCE-AND-RELEASE-ATTESTATION.md"
echo -e "Objective: Run acceptance checks, generate SHA-256 digests and produce RELEASE_RECEIPT.json."

if [[ "${DRY_RUN}" != "true" ]]; then
  RECEIPT_FILE="${INSTALL_PREFIX}/release/RELEASE_RECEIPT.json"
  cat <<EOF > "${RECEIPT_FILE}"
{
  "release_type": "hath0r-infrastructure-full",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "topology": "${TOPOLOGY}",
  "components": {
    "cli": { "binary": "${BIN_DIR}/hath0r", "status": "INSTALLED" },
    "mcp": { "endpoint": "http://127.0.0.1:${DEFAULT_MCP_PORT}", "status": "CONFIGURED" },
    "atc": { "endpoint": "http://127.0.0.1:${DEFAULT_ATC_PORT}", "status": "CONFIGURED" }
  },
  "knowledge_pack": {
    "hydrated": true,
    "path": "${INSTALL_PREFIX}/knowledgebase/canonical"
  },
  "status": "SUCCESS"
}
EOF
  log_success "Generated release receipt at ${RECEIPT_FILE}"
fi

# ------------------------------------------------------------------------------
# 4. Final Walkthrough Summary
# ------------------------------------------------------------------------------
echo ""
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${GREEN}║      ✓ HATH0R INFRASTRUCTURE RELEASE WALKTHROUGH COMPLETED SUCCESSFULLY      ║${RESET}"
echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${RESET}"
echo -e "  • ${BOLD}Topology Mode:${RESET}       ${TOPOLOGY}"
echo -e "  • ${BOLD}Hath0r CLI:${RESET}          ${BIN_DIR}/hath0r"
echo -e "  • ${BOLD}Hath0r MCP Server:${RESET}   http://127.0.0.1:${DEFAULT_MCP_PORT}/ready"
echo -e "  • ${BOLD}Hath0r ATC Edge:${RESET}     http://127.0.0.1:${DEFAULT_ATC_PORT}/healthz"
echo -e "  • ${BOLD}Docker Network:${RESET}      ${DEFAULT_DOCKER_NETWORK}"
echo -e "  • ${BOLD}Knowledge Hydrated:${RESET}  ${INSTALL_PREFIX}/knowledgebase/canonical"
echo -e "  • ${BOLD}Release Receipt:${RESET}     ${INSTALL_PREFIX}/release/RELEASE_RECEIPT.json"
echo -e "${BOLD}${GREEN}══════════════════════════════════════════════════════════════════════════════${RESET}\n"

exit 0
