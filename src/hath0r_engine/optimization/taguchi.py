"""Taguchi Methods for Robust Design, Orthogonal Array Testing, and Quality Loss.

Provides standard Orthogonal Arrays (L4, L8, L9, L12, L18), factor-to-matrix mapping,
Signal-to-Noise Ratio (SNR) evaluation, and Taguchi Quality Loss modeling.
Zero external scientific dependencies (pure Python standard library).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Sequence


class ArrayType(str, Enum):
    """Standard Taguchi Orthogonal Arrays."""

    L4 = "L4"      # L4(2^3): 4 runs, up to 3 factors at 2 levels
    L8 = "L8"      # L8(2^7): 8 runs, up to 7 factors at 2 levels
    L9 = "L9"      # L9(3^4): 9 runs, up to 4 factors at 3 levels
    L12 = "L12"    # L12(2^11): 12 runs, up to 11 factors at 2 levels
    L18 = "L18"    # L18(2^1 x 3^7): 18 runs, 1 factor at 2 levels, 7 factors at 3 levels


class SNRType(str, Enum):
    """Signal-to-Noise Ratio objective types."""

    SMALLER_THE_BETTER = "smaller_the_better"  # Minimize latency, cost, error rate
    LARGER_THE_BETTER = "larger_the_better"    # Maximize accuracy, eval score, throughput
    NOMINAL_THE_BEST = "nominal_the_best"      # Match target nominal value with minimal variance


# Standard Orthogonal Array definition tables (0-indexed integer levels)
_ORTHOGONAL_ARRAYS: dict[ArrayType, dict[str, Any]] = {
    ArrayType.L4: {
        "runs": 4,
        "capacities": [2, 2, 2],
        "matrix": [
            [0, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ],
    },
    ArrayType.L8: {
        "runs": 8,
        "capacities": [2, 2, 2, 2, 2, 2, 2],
        "matrix": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 1, 1, 1, 1, 0, 0],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 0, 1, 1, 0],
            [1, 1, 0, 1, 0, 0, 1],
        ],
    },
    ArrayType.L9: {
        "runs": 9,
        "capacities": [3, 3, 3, 3],
        "matrix": [
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 2, 2, 2],
            [1, 0, 1, 2],
            [1, 1, 2, 0],
            [1, 2, 0, 1],
            [2, 0, 2, 1],
            [2, 1, 0, 2],
            [2, 2, 1, 0],
        ],
    },
    ArrayType.L12: {
        "runs": 12,
        "capacities": [2] * 11,
        "matrix": [
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
            [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    },
    ArrayType.L18: {
        "runs": 18,
        "capacities": [2, 3, 3, 3, 3, 3, 3, 3],
        "matrix": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 2, 2, 2, 2, 2, 2],
            [0, 1, 0, 0, 1, 1, 2, 2],
            [0, 1, 1, 1, 2, 2, 0, 0],
            [0, 1, 2, 2, 0, 0, 1, 1],
            [0, 2, 0, 1, 0, 2, 1, 2],
            [0, 2, 1, 2, 1, 0, 2, 0],
            [0, 2, 2, 0, 2, 1, 0, 1],
            [1, 0, 0, 2, 2, 1, 1, 0],
            [1, 0, 1, 0, 0, 2, 2, 1],
            [1, 0, 2, 1, 1, 0, 0, 2],
            [1, 1, 0, 1, 2, 0, 2, 1],
            [1, 1, 1, 2, 0, 1, 0, 2],
            [1, 1, 2, 0, 1, 2, 1, 0],
            [1, 2, 0, 2, 1, 2, 0, 1],
            [1, 2, 1, 0, 2, 0, 1, 2],
            [1, 2, 2, 1, 0, 1, 2, 0],
        ],
    },
}


@dataclass(frozen=True)
class Factor:
    """Represents a controllable or experimental factor with discrete levels."""

    name: str
    levels: Sequence[Any]

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Factor name cannot be empty.")
        if len(self.levels) < 2:
            raise ValueError(f"Factor '{self.name}' must have at least 2 levels.")

    @property
    def level_count(self) -> int:
        return len(self.levels)


@dataclass
class ExperimentRun:
    """A single execution run with resolved parameter bindings."""

    run_index: int
    parameters: dict[str, Any]
    matrix_row: list[int]


@dataclass
class ExperimentMatrix:
    """Complete balanced experimental design matrix."""

    array_type: ArrayType
    factors: list[Factor]
    runs: list[ExperimentRun]
    factor_column_map: dict[str, int]

    @property
    def run_count(self) -> int:
        return len(self.runs)


@dataclass
class FactorLevelEffect:
    """Statistical effect metrics for a single factor level."""

    level: Any
    level_index: int
    count: int
    mean_response: float
    mean_snr: float


@dataclass
class FactorAnalysis:
    """Factor-level sensitivity and ANOVA/Delta ranking."""

    factor_name: str
    effects: list[FactorLevelEffect]
    optimal_level: Any
    delta_snr: float
    rank: int = 0


@dataclass
class TaguchiAnalysisResult:
    """Full Taguchi Design of Experiments evaluation summary."""

    array_type: ArrayType
    snr_type: SNRType
    factor_analyses: list[FactorAnalysis]
    optimal_configuration: dict[str, Any]
    overall_mean_response: float
    overall_mean_snr: float


class TaguchiLossFunction:
    """Taguchi Quality Loss Function evaluator: L(y) = k * (y - m)^2."""

    def __init__(self, target: float, k: float) -> None:
        if k < 0:
            raise ValueError("Quality loss coefficient k must be non-negative.")
        self.target = float(target)
        self.k = float(k)

    @classmethod
    def from_tolerance(
        cls, target: float, tolerance: float, cost_at_tolerance: float
    ) -> TaguchiLossFunction:
        """Construct loss function from operator tolerance and maximum tolerated cost.

        Args:
            target: Nominal desired value (m).
            tolerance: Maximum allowable deviation before rework/failure (Delta_0).
            cost_at_tolerance: Financial/operational loss at tolerance boundary (A_0).
        """
        if tolerance <= 0:
            raise ValueError("Tolerance must be strictly positive.")
        if cost_at_tolerance < 0:
            raise ValueError("Cost at tolerance must be non-negative.")
        k = cost_at_tolerance / (tolerance**2)
        return cls(target=target, k=k)

    def evaluate(self, value: float) -> float:
        """Calculate quadratic loss for an individual response."""
        deviation = float(value) - self.target
        return self.k * (deviation**2)

    def evaluate_batch(self, values: Sequence[float]) -> dict[str, float]:
        """Calculate average loss, variance loss, and deviation loss for a sample batch."""
        if not values:
            return {
                "average_loss": 0.0,
                "total_loss": 0.0,
                "mean": self.target,
                "variance": 0.0,
                "deviation_from_target": 0.0,
            }

        n = len(values)
        mean_val = sum(values) / n
        variance = sum((v - mean_val) ** 2 for v in values) / (n - 1) if n > 1 else 0.0
        total_loss = sum(self.evaluate(v) for v in values)
        avg_loss = total_loss / n

        return {
            "average_loss": avg_loss,
            "total_loss": total_loss,
            "mean": mean_val,
            "variance": variance,
            "deviation_from_target": abs(mean_val - self.target),
        }


def calculate_snr(values: Sequence[float], snr_type: SNRType | str) -> float:
    """Calculate Taguchi Signal-to-Noise Ratio (SNR) in decibels (dB).

    Args:
        values: Observed experimental response values across repetitions/noise.
        snr_type: One of Smaller-the-Better, Larger-the-Better, Nominal-the-Best.

    Returns:
        Signal-to-Noise ratio in dB.
    """
    if not values:
        return 0.0

    mode = SNRType(snr_type)
    n = len(values)
    eps = 1e-12

    if mode == SNRType.SMALLER_THE_BETTER:
        # eta = -10 * log10((1/n) * sum(y_i^2))
        mean_sq = sum(float(y) ** 2 for y in values) / n
        safe_mean_sq = max(mean_sq, eps)
        return -10.0 * math.log10(safe_mean_sq)

    elif mode == SNRType.LARGER_THE_BETTER:
        # eta = -10 * log10((1/n) * sum(1 / (y_i^2)))
        inv_sq_sum = 0.0
        for y in values:
            val = float(y)
            safe_val = max(abs(val), eps)
            inv_sq_sum += 1.0 / (safe_val**2)
        mean_inv_sq = inv_sq_sum / n
        return -10.0 * math.log10(max(mean_inv_sq, eps))

    elif mode == SNRType.NOMINAL_THE_BEST:
        # eta = 10 * log10(mean^2 / variance)
        mean_val = sum(values) / n
        if n <= 1:
            return 10.0 * math.log10(max(mean_val**2, eps) / eps)
        var = sum((y - mean_val) ** 2 for y in values) / (n - 1)
        safe_var = max(var, eps)
        ratio = (mean_val**2) / safe_var
        return 10.0 * math.log10(max(ratio, eps))

    raise ValueError(f"Unsupported SNR mode: {snr_type}")


class TaguchiEngine:
    """Core Taguchi Orthogonal Array generator and analysis engine."""

    @staticmethod
    def get_orthogonal_array(array_type: ArrayType | str) -> dict[str, Any]:
        """Retrieve raw specification table for an orthogonal array."""
        arr_type = ArrayType(array_type)
        if arr_type not in _ORTHOGONAL_ARRAYS:
            raise KeyError(f"Array {arr_type} not found in catalog.")
        return _ORTHOGONAL_ARRAYS[arr_type]

    @staticmethod
    def verify_orthogonality(matrix: list[list[int]], capacities: list[int]) -> bool:
        """Verify that every pair of columns has balanced combinations."""
        n_runs = len(matrix)
        n_factors = len(capacities)
        for i in range(n_factors):
            for j in range(i + 1, n_factors):
                counts: dict[tuple[int, int], int] = {}
                for row in matrix:
                    pair = (row[i], row[j])
                    counts[pair] = counts.get(pair, 0) + 1
                expected_combinations = capacities[i] * capacities[j]
                if len(counts) != expected_combinations:
                    return False
                expected_freq = n_runs // expected_combinations
                if not all(c == expected_freq for c in counts.values()):
                    return False
        return True

    @classmethod
    def select_best_array(cls, factors: Sequence[Factor]) -> ArrayType:
        """Automatically select the smallest orthogonal array that can accommodate the factors.

        Evaluates factor count and required levels:
        - Up to 3 factors at 2 levels -> L4
        - Up to 7 factors at 2 levels -> L8
        - Up to 4 factors at 3 levels -> L9
        - Up to 11 factors at 2 levels -> L12
        - 1 factor at 2 levels + up to 7 factors at 3 levels -> L18
        """
        if not factors:
            raise ValueError("Cannot select array for empty factor list.")

        level_counts = [f.level_count for f in factors]
        max_level = max(level_counts)
        if max_level > 3:
            raise ValueError(
                f"Factors with {max_level} levels exceed maximum standard capacity (3 levels). "
                "Consider grouping levels into 2 or 3 bins."
            )

        two_level_count = sum(1 for c in level_counts if c == 2)
        three_level_count = sum(1 for c in level_counts if c == 3)

        # Pure 2-level cases
        if three_level_count == 0:
            if two_level_count <= 3:
                return ArrayType.L4
            if two_level_count <= 7:
                return ArrayType.L8
            if two_level_count <= 11:
                return ArrayType.L12
            raise ValueError(
                f"Count of 2-level factors ({two_level_count}) exceeds standard array capacity (11)."
            )

        # Pure 3-level cases
        if two_level_count == 0 and three_level_count <= 4:
            return ArrayType.L9

        # Mixed 2-level and 3-level or large 3-level cases
        if two_level_count <= 1 and three_level_count <= 7:
            return ArrayType.L18

        raise ValueError(
            f"No standard orthogonal array fits combination: {two_level_count} 2-level factors "
            f"and {three_level_count} 3-level factors."
        )

    @classmethod
    def generate_matrix(
        cls, factors: Sequence[Factor], array_type: ArrayType | str | None = None
    ) -> ExperimentMatrix:
        """Construct an orthogonal experiment matrix mapped to real-world factors.

        Args:
            factors: List of Factor descriptors.
            array_type: Specific array type, or None for automatic selection.
        """
        factors_list = list(factors)
        target_array = (
            cls.select_best_array(factors_list)
            if array_type is None
            else ArrayType(array_type)
        )
        spec = cls.get_orthogonal_array(target_array)
        capacities: list[int] = spec["capacities"]
        raw_matrix: list[list[int]] = spec["matrix"]

        # Sort factors to match column capacities (2-level columns first if mixed like L18)
        two_level_factors = [f for f in factors_list if f.level_count == 2]
        three_level_factors = [f for f in factors_list if f.level_count == 3]

        factor_col_map: dict[str, int] = {}
        assigned_cols: list[int] = []

        if target_array == ArrayType.L18:
            # Col 0 is 2-level, cols 1..7 are 3-level
            if two_level_factors:
                f2 = two_level_factors[0]
                factor_col_map[f2.name] = 0
                assigned_cols.append(0)
            col_idx = 1
            for f3 in three_level_factors:
                if col_idx >= len(capacities):
                    break
                factor_col_map[f3.name] = col_idx
                assigned_cols.append(col_idx)
                col_idx += 1
        else:
            for idx, f in enumerate(factors_list):
                if idx >= len(capacities):
                    raise ValueError(
                        f"Factor '{f.name}' exceeds array column capacity ({len(capacities)})."
                    )
                if f.level_count > capacities[idx]:
                    raise ValueError(
                        f"Factor '{f.name}' has {f.level_count} levels, but column {idx} "
                        f"only supports {capacities[idx]}."
                    )
                factor_col_map[f.name] = idx
                assigned_cols.append(idx)

        # Build execution runs
        runs: list[ExperimentRun] = []
        for r_idx, row in enumerate(raw_matrix):
            params: dict[str, Any] = {}
            for f in factors_list:
                col = factor_col_map[f.name]
                level_idx = row[col]
                # Modulo clamp in case factor has fewer levels than column capacity
                mapped_level_idx = level_idx % f.level_count
                params[f.name] = f.levels[mapped_level_idx]
            runs.append(
                ExperimentRun(
                    run_index=r_idx + 1,
                    parameters=params,
                    matrix_row=[row[c] for c in assigned_cols],
                )
            )

        return ExperimentMatrix(
            array_type=target_array,
            factors=factors_list,
            runs=runs,
            factor_column_map=factor_col_map,
        )

    @classmethod
    def analyze_results(
        cls,
        matrix: ExperimentMatrix,
        responses: Sequence[float | Sequence[float]],
        snr_type: SNRType | str = SNRType.LARGER_THE_BETTER,
    ) -> TaguchiAnalysisResult:
        """Perform Taguchi ANOVA / Main Effects analysis on experimental results.

        Args:
            matrix: The ExperimentMatrix that was executed.
            responses: List of scalar responses per run, or list of sample repetitions per run.
            snr_type: S/N ratio formulation (STB, LTB, NTB).
        """
        if len(responses) != matrix.run_count:
            raise ValueError(
                f"Response count ({len(responses)}) must match matrix run count ({matrix.run_count})."
            )

        mode = SNRType(snr_type)

        # Normalize responses into (mean_val, snr_val) per run
        run_stats: list[tuple[float, float]] = []
        for r in responses:
            if isinstance(r, (list, tuple)):
                vals = [float(v) for v in r]
                m_val = sum(vals) / len(vals)
                snr_val = calculate_snr(vals, mode)
            else:
                scalar = float(r)
                m_val = scalar
                snr_val = calculate_snr([scalar], mode)
            run_stats.append((m_val, snr_val))

        total_mean_response = sum(s[0] for s in run_stats) / len(run_stats)
        total_mean_snr = sum(s[1] for s in run_stats) / len(run_stats)

        factor_analyses: list[FactorAnalysis] = []
        optimal_config: dict[str, Any] = {}

        for factor in matrix.factors:
            level_effects: list[FactorLevelEffect] = []

            for l_idx, level_val in enumerate(factor.levels):
                matching_indices = [
                    i
                    for i, r in enumerate(matrix.runs)
                    if r.parameters[factor.name] == level_val
                ]
                if not matching_indices:
                    continue
                cnt = len(matching_indices)
                avg_resp = sum(run_stats[i][0] for i in matching_indices) / cnt
                avg_snr = sum(run_stats[i][1] for i in matching_indices) / cnt

                level_effects.append(
                    FactorLevelEffect(
                        level=level_val,
                        level_index=l_idx,
                        count=cnt,
                        mean_response=avg_resp,
                        mean_snr=avg_snr,
                    )
                )

            # Determine optimal level (highest SNR)
            best_effect = max(level_effects, key=lambda e: e.mean_snr)
            optimal_config[factor.name] = best_effect.level

            # Delta SNR (max - min) measures factor importance
            snr_values = [e.mean_snr for e in level_effects]
            delta = max(snr_values) - min(snr_values)

            factor_analyses.append(
                FactorAnalysis(
                    factor_name=factor.name,
                    effects=level_effects,
                    optimal_level=best_effect.level,
                    delta_snr=delta,
                )
            )

        # Rank factors by delta SNR descending
        factor_analyses.sort(key=lambda fa: fa.delta_snr, reverse=True)
        for rank_idx, fa in enumerate(factor_analyses):
            fa.rank = rank_idx + 1

        return TaguchiAnalysisResult(
            array_type=matrix.array_type,
            snr_type=mode,
            factor_analyses=factor_analyses,
            optimal_configuration=optimal_config,
            overall_mean_response=total_mean_response,
            overall_mean_snr=total_mean_snr,
        )
