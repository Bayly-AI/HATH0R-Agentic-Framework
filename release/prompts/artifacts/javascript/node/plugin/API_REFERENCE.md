# hath0r-cli-node-plugin — API Reference Guide

## `Hath0rAgenticPlugin`

### `constructor(options?: PluginOptions)`
Initializes the Hath0r plugin runtime.

### `wrapTool<T>(roleId: string, toolName: string, toolFn: () => Promise<T>): Promise<T>`
Wraps an asynchronous tool execution with deterministic AgentGraph RBAC verification.

### `expressGateMiddleware(roleIdParam?: string, toolNameParam?: string)`
Express / Connect compatible route middleware that inspects `x-agent-role` headers or route parameters and halts unauthorized execution with HTTP 403.

---

## `Hath0rClient`

### `constructor(options?: PluginOptions)`
Options include:
- `cliPath?: string` — Override path to `hath0r` binary
- `workspaceDir?: string` — Target workspace root directory
- `timeout?: number` — Execution timeout in milliseconds (default: 30000)

### `queryAgentGraph(topic: string): Promise<AgentGraphQueryResult>`
Queries the quad-graph substrate (`RulesGraph`, `KnowledgeGraph`, `ContextGraph`, `MemoryGraph`) for relevant policies.

### `enforceGate(roleId: string, toolName: string): Promise<SecurityGateResult>`
Runs CLI `agentgraph route --role <roleId> --tool <toolName>` to verify execution permissions.

### `checkHealth(): Promise<DoctorResult>`
Runs CLI `doctor --output json` diagnostic checks.

### `runQualityGate(): Promise<QualityGateResult>`
Runs CLI `quality` suite.
