# JavaScript & Node.js Developer Guide

> **Canonical Release Directory:** `./release/javascript/node`  
> **Package Name:** `@hath0r/node`  

This document provides complete developer documentation for the `@hath0r/node` SDK and Node plugin package.

---

## 1. Installation & Setup

Install the packaged Node release tarball:

```sh
npm install ./release/javascript/node/hath0r-node-0.3.0.tgz
```

---

## 2. API & Usage

```typescript
import { Hath0rNodeClient } from '@hath0r/node';

const client = new Hath0rNodeClient({ cliPath: 'hath0r' });

// Diagnostic Health
const health = client.checkHealth();
console.log('Status:', health.status);

// Query AgentGraph
const graph = client.queryAgentGraph('release policies');
console.log('Matched Nodes:', graph.matchedNodes);
```

---

## 3. Testing & Building

To run the Node test suite and generate coverage reports:

```sh
npm --prefix release/javascript/node test
npm --prefix release/javascript/node run test:coverage
```

To build and package `@hath0r/node`:

```sh
python3 scripts/build_node_release.py --out-dir release/javascript/node --rotate
```

Verify SHA256 integrity:

```sh
shasum -a 256 -c release/javascript/node/CHECKSUMS.sha256
```
