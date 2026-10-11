"""Dataset Curator for Continuous Training (CT) in Hath0r Cognitive Substrate."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


@dataclass
class DatasetCurator:
    """Extracts, filters, and formats production agent execution traces into training datasets."""

    output_dir: Path = field(default_factory=lambda: Path.cwd() / ".hath0r" / "training_datasets")

    def __post_init__(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def curate_from_traces(
        self,
        traces: Sequence[Dict[str, Any]],
        min_reward: float = 0.70,
        max_samples: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Filter execution traces by reward threshold and assertion status to build high-quality exemplars."""
        curated: List[Dict[str, Any]] = []

        for trace in traces:
            # Check if trace met assertion constraints
            assertions_passed = trace.get("assertions_passed", True)
            if not assertions_passed:
                continue

            reward = float(trace.get("reward", trace.get("score", 1.0)))
            if reward < min_reward:
                continue

            # Format into standardized prompt-completion pair
            prompt = trace.get("prompt") or trace.get("input")
            completion = trace.get("completion") or trace.get("output") or trace.get("expected_output")

            if not prompt or not completion:
                continue

            sample = {
                "input": prompt,
                "target": completion,
                "task_type": trace.get("task_type", "agent_reasoning"),
                "reward": reward,
                "metadata": {
                    "span_id": trace.get("span_id"),
                    "tokens_used": trace.get("tokens_used", 0),
                    "model": trace.get("model", "default"),
                },
            }
            curated.append(sample)

            if max_samples and len(curated) >= max_samples:
                break

        return curated

    def save_dataset(
        self,
        dataset: List[Dict[str, Any]],
        dataset_name: str = "curated_training_set",
    ) -> Path:
        """Save curated dataset as a newline-delimited JSON (JSONL) file."""
        target_path = self.output_dir / f"{dataset_name}.jsonl"
        with open(target_path, "w", encoding="utf-8") as f:
            for item in dataset:
                f.write(json.dumps(item) + "\n")
        return target_path

    def load_dataset(self, dataset_path: Path | str) -> List[Dict[str, Any]]:
        """Load JSONL dataset from disk."""
        path = Path(dataset_path)
        if not path.is_file():
            return []
        records: List[Dict[str, Any]] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    def compute_statistics(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute summary statistics for a dataset."""
        if not dataset:
            return {"samples_count": 0, "mean_reward": 0.0, "total_estimated_tokens": 0}

        total_reward = sum(d.get("reward", 1.0) for d in dataset)
        estimated_tokens = sum(
            len(str(d.get("input", "")).split()) + len(str(d.get("target", "")).split())
            for d in dataset
        )

        task_types: Dict[str, int] = {}
        for d in dataset:
            t = d.get("task_type", "unknown")
            task_types[t] = task_types.get(t, 0) + 1

        return {
            "samples_count": len(dataset),
            "mean_reward": round(total_reward / len(dataset), 4),
            "total_estimated_tokens": estimated_tokens,
            "task_distribution": task_types,
        }
