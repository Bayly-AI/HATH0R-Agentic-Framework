"""Declarative Pipeline Modules and ChainOfThought Predictors."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple, Type

from hath0r_engine.pipeline.assertions import Assert, SchemaAssertionError
from hath0r_engine.pipeline.signature import Prediction, Signature


class PipelineModule:
    """Base class for all executable declarative agent pipeline modules."""

    def __init__(self, signature: Type[Signature]) -> None:
        self.signature = signature
        self.assertions: List[Tuple[Callable[[Prediction], bool], str]] = []
        self.demonstrations: List[Dict[str, Any]] = []

    def add_assertion(self, check_fn: Callable[[Prediction], bool], error_msg: str) -> None:
        """Register a programmatic assertion that must pass for predictions."""
        self.assertions.append((check_fn, error_msg))

    def forward(self, **kwargs: Any) -> Prediction:
        """Subclasses implement prediction logic."""
        raise NotImplementedError

    def __call__(self, max_retries: int = 2, **kwargs: Any) -> Prediction:
        """Execute the module with automatic assertion checking and retry loops."""
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                pred = self.forward(**kwargs)
                # Verify assertions
                for check_fn, error_msg in self.assertions:
                    Assert(check_fn(pred), f"{error_msg} (Attempt {attempt + 1})")
                return pred
            except SchemaAssertionError as err:
                last_error = err
                continue

        if last_error:
            raise last_error
        raise RuntimeError("Pipeline module execution failed.")


class Predictor(PipelineModule):
    """Direct declarative predictor generating output fields for a signature."""

    def forward(self, **kwargs: Any) -> Prediction:
        output_values: Dict[str, Any] = {}
        outputs = self.signature.get_outputs()

        # Format demonstrations or defaults for execution
        for out_name, out_field in outputs.items():
            if out_name in kwargs:
                output_values[out_name] = kwargs[out_name]
            elif out_field.default is not None:
                output_values[out_name] = out_field.default
            else:
                output_values[out_name] = f"Generated {out_name} for input {kwargs}"

        return Prediction(**output_values)


class ChainOfThought(PipelineModule):
    """Predictor that automatically injects a rationale/reasoning step before outputs."""

    def __init__(self, signature: Type[Signature]) -> None:
        super().__init__(signature)

    def forward(self, **kwargs: Any) -> Prediction:
        output_values: Dict[str, Any] = {}
        outputs = self.signature.get_outputs()

        # Inject reasoning step
        output_values["rationale"] = (
            f"Step-by-step reasoning for inputs: {', '.join(f'{k}={v}' for k, v in kwargs.items())}"
        )

        for out_name, out_field in outputs.items():
            if out_name == "rationale":
                continue
            if out_name in kwargs:
                output_values[out_name] = kwargs[out_name]
            elif out_field.default is not None:
                output_values[out_name] = out_field.default
            else:
                output_values[out_name] = f"Result of {out_name}"

        return Prediction(**output_values)
