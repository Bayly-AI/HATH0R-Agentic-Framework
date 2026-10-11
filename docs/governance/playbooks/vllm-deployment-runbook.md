# Self-Hosted vLLM Deployment & Hath0r Gateway Integration Playbook

> **Status:** Active  
> **Parent Issues:** Bayly-AI/HATH0R-Agentic-Framework#245, #246, #247, #248  
> **Target Subsystems:** `src/hath0r_engine/gateway`, `cfg/gateway.yaml`, `contracts/`  
> **Updated:** 2026-10-11  

---

## 1. Overview & Architectural Role

This playbook provides operational procedures and production-grade configurations for deploying self-hosted **vLLM** inference clusters and connecting them to the **Hath0r AI Gateway** (`AIGatewayClient`).

Hath0r acts as the **cognitive control plane and governance substrate** (managing AgentGraph RAG, AST Guardrails, Durable Workflows, and FinOps), while self-hosted vLLM serves as the **high-throughput compute plane**. This decoupled architecture provides:

- **Complete Data Sovereignty:** Proprietary enterprise source code, schemas, and queries never leave the enterprise boundary.
- **Zero Cloud API Marginal Spend:** Compute is amortized across internal GPU infrastructure ($0.00 per-token cloud bill).
- **Sub-Second TTFT with Automatic Prefix Caching (APC):** Shared AgentGraph context and system prompts are cached in GPU KV memory across multi-turn agent loops.
- **Zero-Syntax Hallucinations:** vLLM's guided decoding engine natively enforces Hath0r JSON Schema contracts during token generation.

---

## 2. Hardware Sizing & Tensor Parallelism Matrix

Select the appropriate open-weights model tier based on task complexity and available hardware:

| Hath0r Tier | Target Open-Weights Model | Parameters | Min VRAM (FP16/BF16) | Quantized (AWQ/FP8) | Recommended GPU Configuration |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `LIGHT` | `Qwen/Qwen2.5-Coder-7B-Instruct` | 7.6B | ~16 GB | ~6 GB | 1x NVIDIA L4 (24GB) or RTX 4090 (24GB) |
| `STANDARD` | `meta-llama/Llama-3.3-70B-Instruct` | 70.6B | ~145 GB | ~42 GB | 2x or 4x NVIDIA H100 / A100 (80GB) |
| `REASONING` | `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` | 32.5B | ~68 GB | ~20 GB | 1x or 2x NVIDIA A100 (80GB) / H100 |

---

## 3. Production vLLM Launch Parameters

Launch the vLLM server with flags specifically tuned for Hath0r agentic execution:

```bash
python3 -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.3-70B-Instruct \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 32768 \
  --enable-prefix-caching \
  --guided-decoding-backend outlines \
  --host 0.0.0.0 \
  --port 8000
```

### Critical Flag Rationale:
- `--enable-prefix-caching`: **Mandatory for Hath0r.** Enables PagedAttention Automatic Prefix Caching (APC), allowing consecutive agent turns sharing common repository context and system prompts to bypass prefill latency.
- `--guided-decoding-backend outlines`: Enables native regex and JSON Schema constrained generation, directly integrated with Hath0r contract schemas.
- `--max-model-len 32768`: Accommodates deep repository AST graphs and multi-turn durability journals.

---

## 4. Containerized Deployments

### 4.1 Docker Compose Deployment

```yaml
version: "3.8"

services:
  vllm-standard:
    image: vllm/vllm-openai:latest
    container_name: hath0r-vllm-standard
    runtime: nvidia
    environment:
      - HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}
    ports:
      - "8000:8000"
    volumes:
      - /mnt/models:/root/.cache/huggingface
    ipc: host
    command: >
      --model meta-llama/Llama-3.3-70B-Instruct
      --tensor-parallel-size 4
      --gpu-memory-utilization 0.92
      --max-model-len 32768
      --enable-prefix-caching
      --guided-decoding-backend outlines
      --host 0.0.0.0
      --port 8000
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped
```

---

## 5. Hath0r Gateway Configuration

### 5.1 Declarative Configuration (`cfg/gateway.yaml`)

Define your vLLM cluster endpoint in `cfg/gateway.yaml`:

```yaml
version: "1.0"
default_provider: "vllm"

vllm:
  endpoint_url: "http://localhost:8000/v1"
  api_key: "" # Optional bearer token if behind enterprise API gateway
  timeout_seconds: 60.0
  enable_prefix_caching: true
  guided_decoding_backend: "outlines"
  models:
    light: "Qwen/Qwen2.5-Coder-7B-Instruct"
    standard: "meta-llama/Llama-3.3-70B-Instruct"
    reasoning: "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
  cost_per_1m:
    input: 0.00
    output: 0.00

fallback_chain:
  - "meta-llama/Llama-3.3-70B-Instruct"
  - "claude-3-5-sonnet"
  - "gpt-4o"
  - "mock-model"

cache:
  enabled: true
  similarity_threshold: 0.90
```

### 5.2 Python Client Usage

```python
from hath0r_engine.gateway import (
    AIGatewayClient,
    GatewayConfig,
    CompletionRequest,
    ComplexityTier,
    ModelProvider,
)

# 1. Initialize client using declarative YAML configuration
config = GatewayConfig.from_yaml()
client = AIGatewayClient(config=config)

# 2. Issue tiered completion routed to self-hosted vLLM
request = CompletionRequest(
    prompt="Audit this Python AST for security vulnerabilities...",
    tier=ComplexityTier.STANDARD,
)

response = client.complete(request)
print(f"Content: {response.content}")
print(f"Provider: {response.provider_used}")  # 'vllm'
print(f"Model: {response.model_used}")        # 'meta-llama/Llama-3.3-70B-Instruct'
print(f"Cost: ${response.cost_usd:.4f}")      # $0.0000
```

---

## 6. Schema-Constrained Generation via Contract IDs

Hath0r seamlessly links its JSON schema catalog (`contracts/`) to vLLM's guided decoding engine. Supply `contract_id` in `CompletionRequest` to enforce output schemas:

```python
# Request outputs strictly conforming to Hath0r Playwright test spec contract
request = CompletionRequest(
    prompt="Generate an end-to-end test case for the navigation flow.",
    contract_id="hath0r-playwright-test-spec-v1",
)

response = client.complete(request)
# response.content is guaranteed valid JSON matching contracts/hath0r-playwright-test-spec-v1.schema.json
```

---

## 7. Operational Health Checks & Diagnostics

### 7.1 Verify Cluster Reachability
```bash
curl -s http://localhost:8000/v1/models | jq .
```

### 7.2 Run Hath0r Gateway Diagnostic Suite
```bash
pytest tests/test_vllm_gateway.py tests/test_ai_gateway.py
```

### 7.3 Common Troubleshooting

| Symptom | Root Cause | Remediation |
| :--- | :--- | :--- |
| `URLError: Connection refused` | vLLM service not running or port 8000 blocked | Verify container state `docker ps` and firewall ingress. |
| `CUDA out of memory (OOM)` | KV cache allocation exceeded VRAM | Lower `--gpu-memory-utilization` to `0.85` or reduce `--max-model-len`. |
| `Guided decoding backend error` | Missing `outlines` in vLLM environment | Ensure vLLM Docker image contains `outlines>=0.0.40`. |
| High TTFT on repeated prompts | Prefix caching disabled | Add `--enable-prefix-caching` to vLLM server arguments. |
