# API Reference — hath0r-agentic-cli

## `Hath0rClient`

Class representing the low-level CLI bridge and AgentGraph interface.

### `constructor(options?: PluginOptions)`
- `options.cliPath`: Custom path to `hath0r` CLI binary (auto-discovered if omitted).
- `options.workspaceDir`: Target workspace directory (defaults to `process.cwd()`).
- `options.timeout`: Execution timeout in milliseconds (default: 30000).

### `queryAgentGraph(topic: string): Promise<AgentGraphQueryResult>`
Queries the quad-graph substrate for rules, policies, and nodes.

### `enforceGate(roleId: string, toolName: string): Promise<SecurityGateResult>`
Checks if `roleId` is authorized to execute `toolName`.

### `checkHealth(): Promise<DoctorResult>`
Runs Hath0r `doctor` diagnostics.

---

## `Hath0rAgenticPlugin`

High-level wrapper for AI Agent runtimes, LangChain JS, Vercel AI SDK, and Express.

### `wrapTool<T>(roleId: string, toolName: string, toolFn: () => Promise<T>): Promise<T>`
Enforces pre-execution RBAC security gating on function calls.

### `expressGateMiddleware(roleIdParam?: string, toolNameParam?: string)`
Express middleware for gating HTTP endpoints.
