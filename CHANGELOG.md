# Changelog

All notable changes to **HATH0R-Agentic-Framework** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.11.2] - 2026-10-30

### Fixed
- **`CICCCDTelemetryHook` crashed on import from a read-only working directory**: the module-level `agent_metrics_bot` singleton created `.hath0r/` under `Path.cwd()` at construction, so `hath0r mcp serve` launched by Claude (cwd `/`) died with `OSError: [Errno 30] Read-only file system: '/.hath0r'`. The state directory is now created lazily in `_save_state`, matching `TokenTelemetryLedger`.

## [1.11.1] - 2026-10-29

### Changed
- **Rule Harmonization, `CLAUDE.md` 1:1 Sync & Workflow Upgrade (`CR-CLAUDE-SYNC-001` · `CR-AGENTIC-SEC-001`)**:
  - Eliminated conflicting SemVer (`or none`) and branch-protection rules in `AGENTS.md`, synchronized `CLAUDE.md` 1:1 with `AGENTS.md`, initialized `THREATMODEL.md`, and updated `.agents/skills/clean-repos/SKILL.md` and `.agents/skills/orient/SKILL.md` to use the latest `hath0r` CLI workflows.

## [1.11.0] - 2026-10-29

### Added
- **OpenAnt Static Call-Graph Reachability Pruning & Constrained Attacker Persona (`hath0r_engine.analysis.ast_gnn`)** (#309):
  - Added decorator and entrypoint inspection (`cli_command`, `mcp_tool`, `http_route`, `public_entrypoint`) to `ASTGNNNode` and `ASTGraphNeuralNetwork._extract_ast_nodes_from_file`.
  - Added `ReachabilityPruneReport` and `ASTGraphNeuralNetwork.compute_external_reachability()` to prune non-reachable internal helper functions via forward BFS over `CALLS` edges (`arXiv:2606.19149`).
  - Added `ConstrainedExploitTrace`, `ConstrainedAttackerVerdict`, and `ASTGraphNeuralNetwork.verify_constrained_exploit_trace()` enforcing non-sycophantic 4-tuple exploit traces `(external_input, entrypoint_symbol, data_flow_hop_chain, sink_operation)` and rejecting `local_cli_only` or sanitized paths.

## [1.10.0] - 2026-10-29

### Added
- **SFT, LoRA, QLoRA, PEFT Subspace Engine & Post-Training Benchmark Evals (`hath0r_engine.training`)**:
  - Added [`src/hath0r_engine/training/peft_lora_sft.py`](src/hath0r_engine/training/peft_lora_sft.py) implementing `PEFTMethod` (`lora`, `qlora`, `sft`, `peft`), `LoRAConfig` / `PEFTConfig` (rank $r$, scaling $\alpha$, dropout, `use_rslora`, target modules, HuggingFace PEFT serialization), `NF4Quantizer` (4-bit NormalFloat quantization/dequantization with double quantization), `LoRALinearAdapter` ($W' = W_0 + \frac{\alpha}{r} B A$ with analytical gradient backprop), `SFTDatasetFormatter` (ChatML prompt masking with `-100`), and `SFTLoRATrainer` (multi-epoch optimization + `adapter_config.json`, `adapter_model.json`, and `.bin` checkpoint persistence).
  - Added `CandidateModelEvaluator.evaluate_trained_adapter()` in [`src/hath0r_engine/training/model_evaluator.py`](src/hath0r_engine/training/model_evaluator.py) comparing frozen base representations against fine-tuned LoRA/PEFT representations and running `GameshowJudge` evaluation cards.
  - Wired `ContinuousTrainingPipeline.execute_training_job` in [`src/hath0r_engine/training/training_pipeline.py`](src/hath0r_engine/training/training_pipeline.py) to execute `SFTLoRATrainer`, persist adapter weights, run post-training benchmark evaluations, and emit telemetry via `CICCCDCTTelemetryHook`.
  - Updated [`contracts/hath0r-training-job-v1.schema.json`](contracts/hath0r-training-job-v1.schema.json) and unit tests in [`tests/test_cicccdct_engine.py`](tests/test_cicccdct_engine.py).

## [1.9.3] - 2026-10-28

### Added
- **Automatic Task Evaluation Configuration (`CR-TASK-EVAL-001`)**: Added declarative `cfg/evals/task-eval.json` binding `HATH0R-Framework` to `TaskEvaluatorBot` (`hath0r evals run`) and `.hath0r/evals/` gitignore negation rules (#307).

## [1.9.2] - 2026-10-28

### Added
- CR-SEMVER-BUMP-001: every created or merged PR must create or bump the product's Semantic Version (`VERSION` is the source of truth).

## [1.9.1] - 2026-10-28

### Changed
- Added `CR-SONAR-PREANNOUNCE-001` to the agent instructions: confirm SonarCloud Quality Gate thresholds before announcing work Complete.

## [1.6.0] - 2026-10-13

### Added
- PagedAttention memory engine with LRU eviction and attention-weighted page compression.
- W3C OWL reasoning exports and dynamic rule verification via Description Logic.
- Token Tree Budget Guard and FinOps circuit breakers for recursive subagent trees.
