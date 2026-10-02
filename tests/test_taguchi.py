"""Tests for HATH0R Taguchi Methods & Robust Design Subsystem."""

import pytest

from hath0r_engine.optimization import (
    ArrayType,
    ExperimentMatrix,
    ExperimentRun,
    Factor,
    FactorAnalysis,
    FactorLevelEffect,
    SNRType,
    TaguchiAnalysisResult,
    TaguchiEngine,
    TaguchiLossFunction,
    calculate_snr,
)


class TestOrthogonalArrayOrthogonality:
    """Mathematical verification that all built-in arrays satisfy strict Taguchi orthogonality."""

    @pytest.mark.parametrize("array_type", [
        ArrayType.L4,
        ArrayType.L8,
        ArrayType.L9,
        ArrayType.L12,
        ArrayType.L18,
    ])
    def test_builtin_arrays_are_orthogonal(self, array_type: ArrayType):
        spec = TaguchiEngine.get_orthogonal_array(array_type)
        matrix = spec["matrix"]
        capacities = spec["capacities"]
        assert len(matrix) == spec["runs"]
        assert TaguchiEngine.verify_orthogonality(matrix, capacities) is True

    def test_non_orthogonal_matrix_rejected(self):
        # A matrix where columns are completely correlated
        bad_matrix = [
            [0, 0],
            [0, 0],
            [1, 1],
            [1, 1],
        ]
        assert TaguchiEngine.verify_orthogonality(bad_matrix, [2, 2]) is False


class TestFactorDefinition:
    """Test Factor validation and properties."""

    def test_valid_factor(self):
        f = Factor(name="model", levels=["light", "standard", "reasoning"])
        assert f.name == "model"
        assert f.level_count == 3
        assert f.levels == ["light", "standard", "reasoning"]

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="Factor name cannot be empty"):
            Factor(name="", levels=["a", "b"])

    def test_insufficient_levels_raises(self):
        with pytest.raises(ValueError, match="must have at least 2 levels"):
            Factor(name="sandbox", levels=["local"])


class TestArraySelection:
    """Test automated selection of standard orthogonal arrays."""

    def test_select_l4_for_small_binary_matrix(self):
        factors = [
            Factor("cache", ["on", "off"]),
            Factor("strict", [True, False]),
        ]
        assert TaguchiEngine.select_best_array(factors) == ArrayType.L4

    def test_select_l8_for_medium_binary_matrix(self):
        factors = [Factor(f"f_{i}", [0, 1]) for i in range(5)]
        assert TaguchiEngine.select_best_array(factors) == ArrayType.L8

    def test_select_l12_for_large_binary_matrix(self):
        factors = [Factor(f"f_{i}", [0, 1]) for i in range(10)]
        assert TaguchiEngine.select_best_array(factors) == ArrayType.L12

    def test_select_l9_for_pure_3_level_matrix(self):
        factors = [
            Factor("model", ["light", "standard", "reasoning"]),
            Factor("sandbox", ["local", "daytona", "e2b"]),
            Factor("retrieval", ["bm25", "dense", "hybrid"]),
        ]
        assert TaguchiEngine.select_best_array(factors) == ArrayType.L9

    def test_select_l18_for_mixed_levels(self):
        factors = [
            Factor("cache", ["on", "off"]),
            Factor("model", ["light", "standard", "reasoning"]),
            Factor("sandbox", ["local", "daytona", "e2b"]),
            Factor("retrieval", ["bm25", "dense", "hybrid"]),
            Factor("guardrail", ["lenient", "standard", "strict"]),
        ]
        assert TaguchiEngine.select_best_array(factors) == ArrayType.L18

    def test_empty_factors_raises(self):
        with pytest.raises(ValueError, match="Cannot select array for empty"):
            TaguchiEngine.select_best_array([])

    def test_unsupported_level_count_raises(self):
        factors = [Factor("provider", ["a", "b", "c", "d"])]
        with pytest.raises(ValueError, match="exceed maximum standard capacity"):
            TaguchiEngine.select_best_array(factors)


class TestExperimentMatrixGeneration:
    """Test generating concrete experiment runs from factors."""

    def test_generate_l9_matrix(self):
        factors = [
            Factor("model", ["light", "standard", "reasoning"]),
            Factor("sandbox", ["local", "daytona", "e2b"]),
        ]
        matrix = TaguchiEngine.generate_matrix(factors, ArrayType.L9)
        assert matrix.array_type == ArrayType.L9
        assert matrix.run_count == 9
        assert len(matrix.runs) == 9

        # Check run 1 bindings
        r1 = matrix.runs[0]
        assert r1.run_index == 1
        assert "model" in r1.parameters
        assert "sandbox" in r1.parameters
        assert r1.parameters["model"] == "light"
        assert r1.parameters["sandbox"] == "local"

    def test_generate_l18_mixed_matrix(self):
        factors = [
            Factor("cache", ["disabled", "enabled"]),
            Factor("model", ["light", "standard", "reasoning"]),
            Factor("sandbox", ["local", "daytona", "e2b"]),
        ]
        matrix = TaguchiEngine.generate_matrix(factors)
        assert matrix.array_type == ArrayType.L18
        assert matrix.run_count == 18

        # In L18, 2-level factor cache has 9 runs disabled and 9 enabled
        disabled_count = sum(1 for r in matrix.runs if r.parameters["cache"] == "disabled")
        enabled_count = sum(1 for r in matrix.runs if r.parameters["cache"] == "enabled")
        assert disabled_count == 9
        assert enabled_count == 9


class TestSignalToNoiseRatio:
    """Test Signal-to-Noise Ratio (SNR) formulations."""

    def test_smaller_the_better_lower_is_better(self):
        # Latency of 100ms vs 200ms
        snr_fast = calculate_snr([100.0, 105.0], SNRType.SMALLER_THE_BETTER)
        snr_slow = calculate_snr([200.0, 210.0], SNRType.SMALLER_THE_BETTER)
        # For STB, higher SNR (less negative dB) is better
        assert snr_fast > snr_slow

    def test_larger_the_better_higher_is_better(self):
        # Accuracy of 95% vs 80%
        snr_high = calculate_snr([0.95, 0.96], SNRType.LARGER_THE_BETTER)
        snr_low = calculate_snr([0.80, 0.81], SNRType.LARGER_THE_BETTER)
        assert snr_high > snr_low

    def test_nominal_the_best_lower_variance_is_better(self):
        # Target nominal: low variance vs high variance around same mean
        snr_stable = calculate_snr([10.0, 10.05, 9.95], SNRType.NOMINAL_THE_BEST)
        snr_noisy = calculate_snr([10.0, 12.0, 8.0], SNRType.NOMINAL_THE_BEST)
        assert snr_stable > snr_noisy

    def test_empty_or_zero_values_handled_safely(self):
        assert calculate_snr([], SNRType.SMALLER_THE_BETTER) == 0.0
        # Zero response does not divide by zero or log(0) crash
        snr_zero = calculate_snr([0.0, 0.0], SNRType.SMALLER_THE_BETTER)
        assert isinstance(snr_zero, float)


class TestTaguchiLossFunction:
    """Test Quality Loss Function modeling."""

    def test_loss_is_zero_at_target(self):
        loss_fn = TaguchiLossFunction(target=100.0, k=0.5)
        assert loss_fn.evaluate(100.0) == 0.0

    def test_loss_scales_quadratically(self):
        loss_fn = TaguchiLossFunction(target=100.0, k=2.0)
        # Delta = 5 -> loss = 2 * 25 = 50
        loss_5 = loss_fn.evaluate(105.0)
        assert loss_5 == 50.0

        # Delta = 10 -> loss = 2 * 100 = 200 (4x)
        loss_10 = loss_fn.evaluate(110.0)
        assert loss_10 == 200.0
        assert loss_10 == 4 * loss_5

    def test_from_tolerance_factory(self):
        # Target = 50ms, tolerance = 10ms, cost = $20
        # k = 20 / (10^2) = 0.2
        loss_fn = TaguchiLossFunction.from_tolerance(target=50.0, tolerance=10.0, cost_at_tolerance=20.0)
        assert loss_fn.k == 0.2
        assert loss_fn.evaluate(60.0) == 20.0
        assert loss_fn.evaluate(40.0) == 20.0

    def test_evaluate_batch(self):
        loss_fn = TaguchiLossFunction(target=10.0, k=1.0)
        batch = [10.0, 12.0, 8.0]
        results = loss_fn.evaluate_batch(batch)
        assert results["mean"] == 10.0
        assert results["total_loss"] == 0.0 + 4.0 + 4.0
        assert results["average_loss"] == 8.0 / 3.0


class TestFullOptimizationAnalysis:
    """Test full Taguchi ANOVA / Main Effects analysis on experimental results."""

    def test_analyze_results_identifies_best_levels(self):
        factors = [
            Factor("temperature", ["low", "medium", "high"]),
            Factor("chunk_size", ["small", "medium", "large"]),
        ]
        matrix = TaguchiEngine.generate_matrix(factors, ArrayType.L9)

        # Synthetic responses: temperature='low' gives high accuracy, 'high' gives low accuracy
        responses = []
        for run in matrix.runs:
            temp = run.parameters["temperature"]
            chunk = run.parameters["chunk_size"]
            score = 50.0
            if temp == "low":
                score += 30.0
            elif temp == "medium":
                score += 15.0
            if chunk == "large":
                score += 10.0
            responses.append(score)

        analysis = TaguchiEngine.analyze_results(matrix, responses, SNRType.LARGER_THE_BETTER)
        assert isinstance(analysis, TaguchiAnalysisResult)
        assert analysis.optimal_configuration["temperature"] == "low"
        assert analysis.optimal_configuration["chunk_size"] == "large"

        # Check factor ranking: temperature had larger delta than chunk_size
        top_factor = analysis.factor_analyses[0]
        assert top_factor.factor_name == "temperature"
        assert top_factor.rank == 1

    def test_analyze_results_with_repetitions_noise(self):
        factors = [
            Factor("cache", ["on", "off"]),
            Factor("retries", ["1", "3"]),
        ]
        matrix = TaguchiEngine.generate_matrix(factors, ArrayType.L4)

        # 3 repetitions per run simulating latency under noise
        responses = [
            [120.0, 125.0, 122.0],  # run 1
            [250.0, 240.0, 260.0],  # run 2
            [140.0, 145.0, 138.0],  # run 3
            [300.0, 310.0, 320.0],  # run 4
        ]
        analysis = TaguchiEngine.analyze_results(matrix, responses, SNRType.SMALLER_THE_BETTER)
        assert analysis.optimal_configuration["cache"] is not None
        assert analysis.overall_mean_snr < 0.0  # STB dB is negative for latencies > 1
