export interface PluginOptions {
  cliPath?: string;
  workspaceDir?: string;
  timeout?: number;
}

export interface SecurityGateResult {
  allowed: boolean;
  roleId: string;
  toolName: string;
  details?: string;
  error?: string;
}

export interface DoctorResult {
  status: string;
  version: string;
  checks: Record<string, any>;
}

export interface QualityGateResult {
  success: boolean;
  output: string;
}

export interface AgentGraphQueryResult {
  topic: string;
  matchedNodes: Array<{
    id: string;
    type: string;
    description?: string;
    policy?: string;
    metadata?: Record<string, any>;
  }>;
  status: string;
}
