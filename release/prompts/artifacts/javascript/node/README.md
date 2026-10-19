# @hath0r/node — Hath0r Agentic Framework Node.js SDK & Plugin

> **Canonical Release Directory:** `./release/javascript/node`  
> **Package Name:** `@hath0r/node`  
> **Version:** 0.3.0  

The `@hath0r/node` package provides native Node.js and TypeScript bindings for the **Hath0r Agentic Framework**. It connects Node applications directly to Hath0r's unified cognitive substrate, AgentGraph policies, and CLI orchestration engine.

---

## 📦 Installation

```sh
# Install from packaged release tarball
npm install ./release/javascript/node/hath0r-node-0.3.0.tgz

# Or via NPM registry (when published)
npm install @hath0r/node
```

---

## 🚀 Quick Start

### 1. Initialize Client & Query AgentGraph

```typescript
import { Hath0rNodeClient } from '@hath0r/node';

// Initialize client (defaults to 'hath0r' CLI on PATH and process.cwd())
const client = new Hath0rNodeClient({
  cliPath: 'hath0r',
  timeout: 30000,
});

// Check health diagnostics
const health = client.checkHealth();
console.log('Hath0r Operational Status:', health.status);

// Query AgentGraph quad-graph rules and policies
const graphResult = client.queryAgentGraph('release policies');
console.log('AgentGraph Query Result:', graphResult);
```

### 2. Run Preflight Checks

```typescript
// Run PR preflight quality gates
const preflightOutput = client.runPreflight();
console.log(preflightOutput);
```

---

## 🧪 Testing Suite

Execute the built-in Node test suite:

```sh
npm --prefix release/javascript/node test
```

Generate LCOV test coverage for SonarCloud / CI quality gates:

```sh
npm --prefix release/javascript/node run test:coverage
```

---

## 🔒 Security & Integrity Verification

Verify package integrity using the generated SHA256 checksums:

```sh
shasum -a 256 -c release/javascript/node/CHECKSUMS.sha256
```
