/**
 * Hath0r Agentic Framework - Node.js SDK & Plugin Runtime
 * 
 * Provides native Node.js bindings, AgentGraph querying, CLI orchestration,
 * and cognitive substrate integrations for Hath0r agents.
 */

import { execSync, ExecSyncOptions } from 'node:child_process';

export interface Hath0rClientOptions {
  cliPath?: string;
  workspace?: string;
  timeout?: number;
}

export interface AgentGraphQueryResult {
  topic: string;
  matchedNodes: Array<{
    id: string;
    plane: string;
    content: string;
  }>;
  status: string;
}

export interface DoctorDiagnosticResult {
  status: 'ok' | 'warning' | 'error';
  version: string;
  checks: Record<string, boolean>;
}

export class Hath0rNodeClient {
  private cliPath: string;
  private workspace: string;
  private timeout: number;

  constructor(options: Hath0rClientOptions = {}) {
    this.cliPath = options.cliPath || 'hath0r';
    this.workspace = options.workspace || process.cwd();
    this.timeout = options.timeout || 30000;
  }

  /**
   * Execute a raw command on the Hath0r operator CLI.
   */
  public executeCli(command: string, args: string[] = []): string {
    const opts: ExecSyncOptions = {
      cwd: this.workspace,
      encoding: 'utf-8',
      timeout: this.timeout,
    };
    const formattedArgs = args.map(a => (a.includes(' ') ? `"${a}"` : a)).join(' ');
    const fullCmd = `${this.cliPath} ${command} ${formattedArgs}`;
    return execSync(fullCmd, opts) as string;
  }

  /**
   * Query the unified AgentGraph substrate for rules, policies, and node connections.
   */
  public queryAgentGraph(topic: string): AgentGraphQueryResult {
    try {
      const output = this.executeCli('agentgraph query', [topic, '--output', 'json']);
      return JSON.parse(output) as AgentGraphQueryResult;
    } catch {
      return {
        topic,
        matchedNodes: [],
        status: 'query_executed_text_fallback',
      };
    }
  }

  /**
   * Run Hath0r doctor diagnostic checks.
   */
  public checkHealth(): DoctorDiagnosticResult {
    try {
      const output = this.executeCli('doctor', ['--output', 'json']);
      return JSON.parse(output) as DoctorDiagnosticResult;
    } catch {
      return {
        status: 'error',
        version: '0.3.0',
        checks: {},
      };
    }
  }

  /**
   * Run Hath0r preflight checks before PR creation.
   */
  public runPreflight(): string {
    return this.executeCli('preflight', []);
  }
}

export const HATH0R_VERSION = '0.3.0';
