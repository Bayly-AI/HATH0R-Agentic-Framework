"""Durable Agent Workflow Decorators and Context Utilities."""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

from hath0r_engine.orchestration.journal import EventJournal
from hath0r_engine.orchestration.state_machine import DurableWorkflowEngine

F = TypeVar("F", bound=Callable[..., Any])


def durable_task(workflow_id_param: str = "workflow_id", db_path: str = ":memory:") -> Callable[[F], F]:
    """Decorator converting an agent execution function into a durable, resumable workflow."""

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            wf_id = kwargs.get(workflow_id_param) or (args[0] if args else "default-wf")
            journal = kwargs.get("journal") or EventJournal(db_path)
            engine = DurableWorkflowEngine(workflow_id=str(wf_id), journal=journal)

            kwargs["workflow_engine"] = engine
            return fn(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
