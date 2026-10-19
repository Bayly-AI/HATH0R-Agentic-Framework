# hath0r-agentic-cli — Node.js SDK & Plugin Runtime

> **Package Name:** `hath0r-agentic-cli`  
> **Target Release Directory:** `./release/javascript/node/cli`  
> **Version:** 0.3.0  

`hath0r-agentic-cli` provides native Node.js and TypeScript bindings for the **Hath0r Agentic Framework**. It connects Node applications directly to Hath0r's unified cognitive substrate, AgentGraph policies, and CLI orchestration engine.

---

## 📦 Installation

```sh
# Install from local release artifact
npm install ./release/javascript/node/cli/hath0r-agentic-cli-0.3.0.tgz

# Or from npm registry
npm install hath0r-agentic-cli
```

---

## 🚀 Quick Start

### 1. Initialize Client & AgentGraph

```typescript
import { Hath0rClient } from 'hath0r-agentic-cli';

const client = new Hath0rClient();

// Query AgentGraph quad-graph rules and policies
const graph = await client.queryAgentGraph('release policies');
console.log('Matched Nodes:', graph.matchedNodes);

// Check system health
const health = await client.checkHealth();
console.log('Status:', health.status);
```

### 2. Wrap Tool Execution with AgentGraph Pre-Execution Gate

```typescript
import { Hath0rAgenticPlugin } from 'hath0r-agentic-cli';

const plugin = new Hath0rAgenticPlugin();

// Enforce AgentGraph RBAC before tool execution
const result = await plugin.wrapTool('developer', 'runDeploy', async () => {
  return await executeDeploy();
});
```

---

## 🧪 Testing

Execute Node native tests:

```sh
npm test
```
