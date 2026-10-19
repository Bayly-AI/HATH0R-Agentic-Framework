# Zero-Prompt-Tax Retrieval Strategy

**Strategy ID**: `STRAT-ZERO-PROMPT-TAX-001`  
**Classification**: Performance & FinOps Doctrine  

---

## 🎯 The Doctrine of Zero Prompt Tax

Loading unbounded context, giant markdown rulebooks, or entire source trees into LLM prompts causes severe degradation:
1. **Context Smearing**: Key instructions get lost in middle token positions.
2. **FinOps Inefficiency**: Cost scales quadratically or linearly with large context inputs on every turn.
3. **Latency Inflation**: Time-to-first-token increases significantly.

### 🛡️ Core Rules of Zero Prompt Tax
1. **Deterministic Pre-pruning**: Prune unauthorized tools using `hath0r agentgraph route --role <role>` BEFORE invoking the model.
2. **Targeted Knowledge Slices**: Query semantic nodes via `hath0r kb search` or `hath0r agentgraph query` instead of reading entire rulebooks.
3. **Micro Memory Paging**: Limit active working memory to Letta-style pages (<2KB).
