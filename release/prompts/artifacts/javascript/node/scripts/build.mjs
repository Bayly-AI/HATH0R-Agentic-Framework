import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgDir = path.resolve(__dirname, '..');
const distDir = path.resolve(pkgDir, 'dist');

if (fs.existsSync(distDir)) {
  fs.rmSync(distDir, { recursive: true, force: true });
}
fs.mkdirSync(distDir, { recursive: true });

console.log('Generating production JS & ESM bundles for @hath0r/node...');

const indexCjs = `/**
 * Hath0r Agentic Framework - Node.js SDK & Plugin Runtime
 */
const { execSync } = require('node:child_process');

class Hath0rNodeClient {
  constructor(options = {}) {
    this.cliPath = options.cliPath || 'hath0r';
    this.workspace = options.workspace || process.cwd();
    this.timeout = options.timeout || 30000;
  }

  executeCli(command, args = []) {
    const formattedArgs = args.map(a => (a.includes(' ') ? \`"\${a}"\` : a)).join(' ');
    const fullCmd = \`\${this.cliPath} \${command} \${formattedArgs}\`;
    return execSync(fullCmd, { cwd: this.workspace, encoding: 'utf-8', timeout: this.timeout });
  }

  queryAgentGraph(topic) {
    try {
      const output = this.executeCli('agentgraph query', [topic, '--output', 'json']);
      return JSON.parse(output);
    } catch {
      return { topic, matchedNodes: [], status: 'query_executed_text_fallback' };
    }
  }

  checkHealth() {
    try {
      const output = this.executeCli('doctor', ['--output', 'json']);
      return JSON.parse(output);
    } catch {
      return { status: 'error', version: '0.3.0', checks: {} };
    }
  }
}

module.exports = {
  Hath0rNodeClient,
  HATH0R_VERSION: '0.3.0'
};
`;

const indexEsm = `/**
 * Hath0r Agentic Framework - Node.js SDK & Plugin Runtime (ESM)
 */
import { execSync } from 'node:child_process';

export class Hath0rNodeClient {
  constructor(options = {}) {
    this.cliPath = options.cliPath || 'hath0r';
    this.workspace = options.workspace || process.cwd();
    this.timeout = options.timeout || 30000;
  }

  executeCli(command, args = []) {
    const formattedArgs = args.map(a => (a.includes(' ') ? \`"\${a}"\` : a)).join(' ');
    const fullCmd = \`\${this.cliPath} \${command} \${formattedArgs}\`;
    return execSync(fullCmd, { cwd: this.workspace, encoding: 'utf-8', timeout: this.timeout });
  }

  queryAgentGraph(topic) {
    try {
      const output = this.executeCli('agentgraph query', [topic, '--output', 'json']);
      return JSON.parse(output);
    } catch {
      return { topic, matchedNodes: [], status: 'query_executed_text_fallback' };
    }
  }

  checkHealth() {
    try {
      const output = this.executeCli('doctor', ['--output', 'json']);
      return JSON.parse(output);
    } catch {
      return { status: 'error', version: '0.3.0', checks: {} };
    }
  }
}

export const HATH0R_VERSION = '0.3.0';
`;

const indexDts = `/**
 * Hath0r Agentic Framework - TypeScript Definitions
 */
export interface Hath0rClientOptions {
  cliPath?: string;
  workspace?: string;
  timeout?: number;
}

export interface AgentGraphQueryResult {
  topic: string;
  matchedNodes: Array<{ id: string; plane: string; content: string }>;
  status: string;
}

export interface DoctorDiagnosticResult {
  status: 'ok' | 'warning' | 'error';
  version: string;
  checks: Record<string, boolean>;
}

export declare class Hath0rNodeClient {
  constructor(options?: Hath0rClientOptions);
  executeCli(command: string, args?: string[]): string;
  queryAgentGraph(topic: string): AgentGraphQueryResult;
  checkHealth(): DoctorDiagnosticResult;
}

export declare const HATH0R_VERSION: string;
`;

fs.writeFileSync(path.join(distDir, 'index.js'), indexCjs);
fs.writeFileSync(path.join(distDir, 'index.mjs'), indexEsm);
fs.writeFileSync(path.join(distDir, 'index.d.ts'), indexDts);

console.log('Build completed successfully.');
