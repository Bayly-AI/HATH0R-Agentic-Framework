import { Hath0rClient } from "./client.ts";
import type { PluginOptions, SecurityGateResult } from "./types.ts";

export type * from "./types.ts";
export { Hath0rClient } from "./client.ts";

/**
 * Main Hath0r Agentic Plugin class.
 */
export class Hath0rAgenticPlugin {
  public client: Hath0rClient;

  constructor(options: PluginOptions = {}) {
    this.client = new Hath0rClient(options);
  }

  /**
   * Wrap any tool execution function with AgentGraph pre-execution security gating.
   */
  public async wrapTool<T>(
    roleId: string,
    toolName: string,
    toolFn: () => Promise<T>
  ): Promise<T> {
    const gate = await this.client.enforceGate(roleId, toolName);
    if (!gate.allowed) {
      throw new Error(`[Hath0r Gate DENIED] Role '${roleId}' cannot execute tool '${toolName}': ${gate.error}`);
    }
    return await toolFn();
  }

  /**
   * Express / Connect middleware for security gating HTTP endpoints.
   */
  public expressGateMiddleware(roleIdParam: string = "roleId", toolNameParam: string = "toolName") {
    return async (req: any, res: any, next: any) => {
      const roleId = req.headers["x-agent-role"] || req.params[roleIdParam] || req.body[roleIdParam];
      const toolName = req.params[toolNameParam] || req.body[toolNameParam];

      if (!roleId || !toolName) {
        return res.status(400).json({ error: "Missing x-agent-role or toolName for Hath0r Gate" });
      }

      const gate = await this.client.enforceGate(roleId, toolName);
      if (!gate.allowed) {
        return res.status(403).json({
          error: "Hath0r Security Gate Intercepted Execution",
          roleId,
          toolName,
          details: gate.error
        });
      }

      next();
    };
  }
}
