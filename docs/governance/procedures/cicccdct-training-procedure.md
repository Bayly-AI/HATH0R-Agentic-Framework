# Procedure: Continuous Training Execution & Dataset Curation (CIC³DCT / CIC{qubed}DCT)

> **Document Type:** Procedure  
> **Status:** Ratified  
> **Governing Standards:** `CR-CICCCDCT-001`, `CR-CLI-ENTRY-001`  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#255, #258

---

## 1. Purpose & Scope

This procedure defines the end-to-end execution steps for curating training datasets from agent execution traces, executing continuous fine-tuning (LoRA/QLoRA on local SLMs or DSPy MIPROv2 compilation), and evaluating candidate models.

---

## 2. Step-by-Step Procedure

### Step 1: Ingest & Curate Production Traces
1. Extract OTel span journals and `EventJournal` logs where assertions succeeded:
   ```bash
   hath0r cicccdct dataset curate --min-reward 0.70 --max-samples 1000 --output-file .hath0r/training_datasets/latest_curated.jsonl
   ```
2. Verify token statistics and class balance:
   ```bash
   hath0r cicccdct dataset stats --dataset .hath0r/training_datasets/latest_curated.jsonl
   ```

### Step 2: Trigger Continuous Training Job
1. Execute training with specified target architecture and epochs:
   ```bash
   hath0r cicccdct train run --target reasoning_slm --method lora --dataset .hath0r/training_datasets/latest_curated.jsonl --epochs 3 --lr 0.0002
   ```
2. The orchestrator:
   - Sets up training splits.
   - Computes Taguchi loss optimization parameters.
   - Saves model weights/adapters to `.hath0r/training_artifacts/`.
   - Logs experiment parameters and run metrics to the MLflow container.

### Step 3: Candidate Benchmark Evaluation
1. Run golden benchmark evaluation against baseline:
   ```bash
   hath0r cicccdct model eval --candidate-run <mlflow_run_id>
   ```
2. Verify candidate passes the improvement invariant ($R_{\text{candidate}} \ge R_{\text{production}} + 0.02$).

### Step 4: Model Registry Promotion
1. Transition verified model version in MLflow Model Registry:
   ```bash
   hath0r cicccdct model promote --model-name reasoning_slm --version 1 --stage Staging
   ```
2. Verify with gate audit:
   ```bash
   hath0r cicccdct validate
   ```
