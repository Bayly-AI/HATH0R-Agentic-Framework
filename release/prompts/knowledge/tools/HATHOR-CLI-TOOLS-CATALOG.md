# Hath0r CLI Tools & Commands Catalog

The **Hath0r CLI** (`hath0r`) is the primary operator command-line interface, governance gateway, and cognitive agent orchestrator for the Hath0r ecosystem.

All agents must adhere to **`CR-CLI-ENTRY-001`**: Start with the CLI rather than inventing unverified ad-hoc shell scripts.

---

## 🛠️ Core Command Reference

### 1. Repository Lifecycle & Health

#### `hath0r init`
- **Description**: Initializes a repository with the canonical Hath0r member layout (`.hath0r/`, `cfg/`, `contracts/`, `AGENTS.md`, and micro-memory substrate).
- **Usage**: `hath0r init [--template <name>] [--force]`
- **Outputs**: Generates `.hath0r/memory/graph.json`, `.hath0r/memory/hashes.json`, `cfg/suite.yaml`, and registers repo in group control tower.

#### `hath0r doctor`
- **Description**: Runs comprehensive environmental and structural health checks across the workspace.
- **Usage**: `hath0r doctor [--json]`
- **Checks**: Git cleanliness, prohibited legacy roots (`.ai/`, `.customerSystem/`, `.infraOS/`), contract pins, calibration freshness, Docker daemon, and memory graph integrity.
- **Exit Code**: `0` on healthy, `1` on warning/advisory, `2` on blocking failure.

---

### 2. Cognitive Memory & Session Substrate (`CR-MEMORY-COMPOUND-001`)

#### `hath0r memory session start`
- **Description**: Begins a compact (<2KB) micro memory working session.
- **Usage**: `hath0r memory session start --task "<task-slug>"`
- **Effect**: Initializes `.hath0r/memory/sessions/current.json` and records entry in session lineage.

#### `hath0r memory session read`
- **Description**: Reads current micro memory session state and recent recalled entity nodes without prompt stuffing.
- **Usage**: `hath0r memory session read [--format json|text]`

#### `hath0r memory session write`
- **Description**: Writes an incremental micro-entry into the active working session.
- **Usage**: `hath0r memory session write "<summary-message>"`

#### `hath0r memory session end`
- **Description**: Closes the active session, computes session delta, and prepares for compounding.
- **Usage**: `hath0r memory session end`

#### `hath0r memory compound`
- **Description**: Compounds verified task knowledge (episode, insight, decision, rule, fact) into `.hath0r/memory/graph.json` before task announcement.
- **Usage**:
  ```bash
  hath0r memory compound \
    --id "<type>:<slug>" \
    --type <episode|decision|fact|insight|rule|concept> \
    --label "<Short Title>" \
    --content "<Detailed knowledge content>" \
    --tags "<comma,separated,tags>" \
    [--source-file "<path>"] \
    [--relation <DERIVES_FROM|RESOLVES|RELATES_TO|SUPERSEDES|ENFORCES|PRECEDES>]
  ```

#### `hath0r memory verify`
- **Description**: Verifies pre-announcement memory compounding compliance (`read_count >= 1`, `write_count >= 1`, `compounded_nodes_count >= 1`, `hashes_verified: True`).
- **Usage**: `hath0r memory verify`

#### `hath0r memory hash verify`
- **Description**: Performs SHA-256 CAS verification across all tracked memory files and source files against `.hath0r/memory/hashes.json`.
- **Usage**: `hath0r memory hash verify`

---

### 3. AgentGraph Governance & RBAC Router (`CR-AGENTGRAPH-001`)

#### `hath0r agentgraph query`
- **Description**: Queries the AgentGraph substrate for relevant rules, policies, and role definitions without prompt stuffing.
- **Usage**: `hath0r agentgraph query "<topic-or-rule-id>"`

#### `hath0r agentgraph route`
- **Description**: Deterministically prunes unauthorized tools and resolves permissible actions for a given agent role.
- **Usage**: `hath0r agentgraph route --role <role-name> [--tool <tool-name>]`

#### `hath0r agentgraph status`
- **Description**: Displays current AgentGraph synchronization status, active node counts, and snapshot age.
- **Usage**: `hath0r agentgraph status`

#### `hath0r agentgraph validate`
- **Description**: Validates all rule nodes and edge inheritance DAGs against `contracts/hath0r-agentgraph-v1.schema.json`.
- **Usage**: `hath0r agentgraph validate`

---

### 4. Contracts & Governance Verification

#### `hath0r contracts validate`
- **Description**: Validates JSON/YAML manifests against canonical Hath0r schema contracts under `contracts/`.
- **Usage**: `hath0r contracts validate [--schema <path>] [--target <file>]`

#### `hath0r branch validate`
- **Description**: Verifies that git branch names conform to the issue-driven convention (`<type>/<issue-number>-<slug>`).
- **Usage**: `hath0r branch validate <branch-name>`

---

### 5. Infrastructure as Code & Container Salting (`CR-IAC-001`)

#### `hath0r iac audit`
- **Description**: Audits Dockerfiles, compose stacks, and k8s manifests for container hardening, non-root user execution, and immutable SHA-256 digests.
- **Usage**: `hath0r iac audit [--strict]`

#### `hath0r iac salt`
- **Description**: Salts container manifests by replacing mutable tags (e.g. `:latest`) with cryptographically verified SHA-256 digest pins.
- **Usage**: `hath0r iac salt --manifest <path>`
