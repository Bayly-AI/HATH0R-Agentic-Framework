# hath0r-cli-node-plugin — Hath0r CLI Node.js Plugin & SDK

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](#)

> **Package Name:** `hath0r-cli-node-plugin`  
> **Target Release Directory:** `./release/javascript/node/plugin`  
> **Version:** 0.3.0  

`hath0r-cli-node-plugin` provides native Node.js and TypeScript bindings for the **Hath0r Agentic Framework**. It connects Node applications directly to Hath0r's unified cognitive substrate, AgentGraph policies, and CLI orchestration engine.

---

## 📦 Installation

```sh
# Install from npm registry
npm install hath0r-cli-node-plugin

# Or install from local release artifact
npm install ./release/javascript/node/plugin/hath0r-cli-node-plugin-0.3.0.tgz
```

---

## 🚀 Quick Start

### 1. Initialize Client & Query AgentGraph

```typescript
import { Hath0rClient } from 'hath0r-cli-node-plugin';

const client = new Hath0rClient();

// Query AgentGraph quad-graph rules and policies
const graph = await client.queryAgentGraph('release policies');
console.log('Matched Nodes:', graph.matchedNodes);

// Check system health
const health = await client.checkHealth();
console.log('Status:', health.status);
```

### 2. Wrap Tool Execution with Pre-Execution Security Gate

```typescript
import { Hath0rAgenticPlugin } from 'hath0r-cli-node-plugin';

const plugin = new Hath0rAgenticPlugin();

// Enforce AgentGraph RBAC before tool execution
const result = await plugin.wrapTool('developer', 'runDeploy', async () => {
  return await executeDeploy();
});
```

### 3. Express HTTP Middleware

```typescript
import express from 'express';
import { Hath0rAgenticPlugin } from 'hath0r-cli-node-plugin';

const app = express();
const plugin = new Hath0rAgenticPlugin();

app.post('/api/tools/:toolName', plugin.expressGateMiddleware(), (req, res) => {
  res.json({ status: 'allowed' });
});
```

---

## 🧪 Testing

Execute Node native tests:

```sh
npm test
```
