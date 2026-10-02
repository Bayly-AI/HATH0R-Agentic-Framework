"""Generative UI Component Builders for Hath0r Dashboard."""

from __future__ import annotations

import uuid
from typing import Optional

from hath0r_engine.ui.protocol import EvidenceComponent, EvidenceType


class UIComponentBuilder:
    """Constructs standardized EvidenceComponent instances."""

    @staticmethod
    def build_diff_viewer(
        file_path: str,
        old_code: str,
        new_code: str,
        language: str = "python",
        title: Optional[str] = None,
    ) -> EvidenceComponent:
        """Construct interactive diff viewer component."""
        return EvidenceComponent(
            component_id=f"diff-{uuid.uuid4().hex[:8]}",
            type=EvidenceType.DIFF_VIEWER,
            title=title or f"Diff: {file_path}",
            props={
                "file_path": file_path,
                "old_code": old_code,
                "new_code": new_code,
                "language": language,
            },
        )

    @staticmethod
    def build_test_badge(
        suite_name: str,
        passed: int,
        failed: int,
        coverage_pct: float,
        title: Optional[str] = None,
    ) -> EvidenceComponent:
        """Construct test execution badge component."""
        return EvidenceComponent(
            component_id=f"badge-{uuid.uuid4().hex[:8]}",
            type=EvidenceType.TEST_BADGE,
            title=title or f"Test Results: {suite_name}",
            props={
                "suite_name": suite_name,
                "passed": passed,
                "failed": failed,
                "coverage_pct": round(coverage_pct, 2),
                "status": "PASS" if failed == 0 else "FAIL",
            },
        )

    @staticmethod
    def build_parameter_slider(
        param_key: str,
        min_val: float,
        max_val: float,
        current_val: float,
        step: float = 1.0,
        label: Optional[str] = None,
    ) -> EvidenceComponent:
        """Construct parameter tuning slider component."""
        return EvidenceComponent(
            component_id=f"slider-{uuid.uuid4().hex[:8]}",
            type=EvidenceType.PARAMETER_SLIDER,
            title=label or f"Tune: {param_key}",
            props={
                "param_key": param_key,
                "min": min_val,
                "max": max_val,
                "current": current_val,
                "step": step,
            },
        )

    @staticmethod
    def build_crypto_signoff_card(
        gate_name: str,
        required_role: str = "release_manager",
        prompt: str = "Sign off to promote release",
    ) -> EvidenceComponent:
        """Construct cryptographic sign-off authorization card."""
        return EvidenceComponent(
            component_id=f"signoff-{uuid.uuid4().hex[:8]}",
            type=EvidenceType.CRYPTO_SIGNOFF_CARD,
            title=f"Authorization Gate: {gate_name}",
            props={
                "gate_name": gate_name,
                "required_role": required_role,
                "prompt": prompt,
            },
        )
