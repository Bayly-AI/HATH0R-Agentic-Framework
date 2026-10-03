import { execFile, execFileSync } from "child_process";
import { promisify } from "util";
import { existsSync } from "fs";
import { resolve } from "path";
import type {
  DoctorResult,
  PluginOptions,
  QualityGateResult,
  SecurityGateResult,
  AgentGraphQueryResult,
} from "./types.ts";

const execFileAsync = promisify(execFile);

export class Hath0rClient {
  public cliPath: string;
  public workspaceDir: string;
  public timeout: number;

  constructor(options: PluginOptions = {}) {
    this.workspaceDir = options.workspaceDir
      ? resolve(options.workspaceDir)
      : process.cwd();
    this.timeout = options.timeout || 30000;

    // Auto-detect CLI binary path
    if (options.cliPath) {
      this.cliPath = options.cliPath;
    } else if (process.env.HATH0R_CLI) {
      this.cliPath = process.env.HATH0R_CLI;
    } else {
      let curr = this.workspaceDir;
      let found: string | null = null;
      for (let i = 0; i < 5; i++) {
        const candidates = [
          resolve(curr, "release/python/cli/hath0r-darwin-arm64"),
          resolve(curr, "release/python/cli/hath0r-linux-x86_64"),
          resolve(curr, "release/python/cli/hath0r"),
          resolve(curr, "release/python/cli/hath0r-windows-x64.cmd"),
        ];
        for (const candidate of candidates) {
          if (existsSync(candidate)) {
            found = candidate;
            break;
          }
        }
        if (found) break;
        const parent = resolve(curr, "..");
        if (parent === curr) break;
        curr = parent;
      }
      this.cliPath = found || "hath0r";
    }
  }

  /**
   * Run CLI command asynchronously
   */
  public async runCommand(args: string[]): Promise<string> {
    try {
      const { stdout } = await execFileAsync(this.cliPath, args, {
        cwd: this.workspaceDir,
        timeout: this.timeout,
      });
      return stdout.trim();
    } catch (err: any) {
      const errMsg = err.stderr || err.stdout || err.message;
      throw new Error(`[Hath0r CLI Error] ${errMsg}`);
    }
  }

  /**
   * Run CLI command synchronously
   */
  public runCommandSync(args: string[]): string {
    try {
      return execFileSync(this.cliPath, args, {
        cwd: this.workspaceDir,
        encoding: "utf-8",
        timeout: this.timeout,
      }).trim();
    } catch (err: any) {
      const errMsg = err.stderr || err.stdout || err.message;
      throw new Error(`[Hath0r CLI Error] ${errMsg}`);
    }
  }

  /**
   * Query the unified AgentGraph substrate for rules, policies, and node connections.
   */
  public async queryAgentGraph(topic: string): Promise<AgentGraphQueryResult> {
    try {
      const output = await this.runCommand(["agentgraph", "query", topic, "--output", "json"]);
      return JSON.parse(output) as AgentGraphQueryResult;
    } catch {
      return {
        topic,
        matchedNodes: [],
        status: "query_executed_text_fallback",
      };
    }
  }

  /**
   * Enforce pre-execution RBAC tool security gate via AgentGraph
   */
  public async enforceGate(roleId: string, toolName: string): Promise<SecurityGateResult> {
    try {
      await this.runCommand([
        "agentgraph",
        "route",
        "--role",
        roleId,
        "--tool",
        toolName,
      ]);
      return { allowed: true, roleId, toolName, details: "AgentGraph RBAC Gate PASSED" };
    } catch (err: any) {
      return {
        allowed: false,
        roleId,
        toolName,
        error: err.message,
        details: "AgentGraph RBAC Gate DENIED",
      };
    }
  }

  /**
   * Run Hath0r doctor diagnostic checks.
   */
  public async checkHealth(): Promise<DoctorResult> {
    try {
      const output = await this.runCommand(["doctor", "--output", "json"]);
      return JSON.parse(output) as DoctorResult;
    } catch {
      return {
        status: "error",
        version: "0.3.0",
        checks: {},
      };
    }
  }

  /**
   * Run Hath0r preflight check.
   */
  public async runPreflight(): Promise<string> {
    return await this.runCommand(["preflight", "run"]);
  }

  /**
   * Run Hath0r quality gate suite.
   */
  public async runQualityGate(): Promise<QualityGateResult> {
    try {
      const output = await this.runCommand(["quality"]);
      return { success: true, output };
    } catch (err: any) {
      return { success: false, output: err.message };
    }
  }
}
