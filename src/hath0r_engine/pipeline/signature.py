"""Typed Declarative Signatures and Field Descriptors for Agent Pipelines."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type


@dataclass
class Field:
    """Base descriptor for signature inputs and outputs."""

    desc: str = ""
    default: Any = None
    is_input: bool = True
    type_hint: Optional[Type[Any]] = None


def InputField(desc: str = "", default: Any = None, type_hint: Optional[Type[Any]] = None) -> Field:
    """Declare an input field to the declarative signature."""
    return Field(desc=desc, default=default, is_input=True, type_hint=type_hint)


def OutputField(desc: str = "", default: Any = None, type_hint: Optional[Type[Any]] = None) -> Field:
    """Declare an expected output field from the declarative signature."""
    return Field(desc=desc, default=default, is_input=False, type_hint=type_hint)


class Prediction:
    """Structured container holding output fields produced by a pipeline module."""

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Prediction({attrs})"


class SignatureMeta(type):
    """Metaclass that collects InputField and OutputField attributes into signature schema."""

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> Any:
        inputs: Dict[str, Field] = {}
        outputs: Dict[str, Field] = {}

        for base in bases:
            if hasattr(base, "_inputs"):
                inputs.update(base._inputs)
            if hasattr(base, "_outputs"):
                outputs.update(base._outputs)

        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                if value.is_input:
                    inputs[key] = value
                else:
                    outputs[key] = value

        attrs["_inputs"] = inputs
        attrs["_outputs"] = outputs
        attrs["_doc"] = attrs.get("__doc__", "")
        return super().__new__(cls, name, bases, attrs)


class Signature(metaclass=SignatureMeta):
    """Declarative signature mapping input specifications to expected outputs."""

    _inputs: Dict[str, Field] = {}
    _outputs: Dict[str, Field] = {}
    _doc: str = ""

    @classmethod
    def get_inputs(cls) -> Dict[str, Field]:
        return dict(cls._inputs)

    @classmethod
    def get_outputs(cls) -> Dict[str, Field]:
        return dict(cls._outputs)
