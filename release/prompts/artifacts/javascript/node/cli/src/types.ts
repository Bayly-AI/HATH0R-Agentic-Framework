export interface PluginOptions {
  cliPath?: string;
  workspaceDir?: string;
  timeout?: number;
}

export interface SecurityGateResult {
  allowed: boolean;
  roleId: string;
  toolName: string;
  error?: string;
  details?: string;
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

export interface DoctorResult {
  status: 'ok' | 'warning' | 'error';
  version: string;
  checks: Record<string, boolean>;
}

export interface QualityGateResult {
  success: boolean;
  output: string;
}
