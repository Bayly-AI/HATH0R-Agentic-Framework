"""Automated Teleprompter and Few-Shot Prompt Compilers for Agent Pipelines."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from hath0r_engine.pipeline.module import PipelineModule
from hath0r_engine.pipeline.signature import Prediction


class BootstrapFewShotCompiler:
    """Discovers and compiles optimal few-shot demonstrations based on assertion metrics."""

    def __init__(
        self,
        metric: Callable[[Dict[str, Any], Prediction], bool],
        max_bootstrapped_demos: int = 4,
    ) -> None:
        self.metric = metric
        self.max_bootstrapped_demos = max_bootstrapped_demos

    def compile(
        self,
        student_module: PipelineModule,
        trainset: List[Dict[str, Any]],
    ) -> PipelineModule:
        """Run training set, validate against metric, and bootstrap successful demonstrations."""
        successful_demos: List[Dict[str, Any]] = []

        for example in trainset:
            if len(successful_demos) >= self.max_bootstrapped_demos:
                break

            try:
                pred = student_module(**example)
                if self.metric(example, pred):
                    demo = dict(example)
                    demo["prediction"] = pred.to_dict()
                    successful_demos.append(demo)
            except Exception:
                continue

        student_module.demonstrations = successful_demos
        return student_module
