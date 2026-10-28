# Changelog

All notable changes to **HATH0R-Agentic-Framework** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
