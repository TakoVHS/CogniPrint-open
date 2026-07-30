from __future__ import annotations

import copy
import json
import unittest

from cogniprint.benchmarks.calibration import (
    expected_calibration_error,
    fit_temperature_scaling,
    multiclass_nll,
    temperature_softmax,
)
from cogniprint.benchmarks.claims import (
    assert_aggregate_output_safe,
    evaluate_claim_narrowing,
)
from cogniprint.benchmarks.conformal import (
    fit_class_conditional_conformal,
    predict_conformal_unknown,
)
from cogniprint.benchmarks.surface import (
    SURFACE_FEATURE_NAMES,
    evaluate_surface_baseline,
    surface_statistics_vector,
)
from cogniprint.benchmarks.uncertainty import (
    paired_group_bootstrap_delta,
    wilson_interval,
)


def vector(record: dict) -> list[float]:
    return list(record["vector"])


def passing_claim_values() -> dict[str, float | int]:
    return {
        "held_out_false_known_point": 0.08,
        "held_out_false_known_wilson_upper": 0.14,
        "held_out_unknown_rejection": 0.92,
        "known_coverage": 0.70,
        "best_system_balanced_accuracy": 0.60,
        "best_system_macro_f1": 0.60,
        "cogniprint_vs_ngram_delta_macro_f1": 0.03,
        "cogniprint_vs_ngram_ci_lower": 0.01,
        "minimum_known_class_recall": 0.50,
        "ece": 0.08,
        "calibrated_nll": 0.70,
        "uncalibrated_nll": 0.80,
        "calibrated_brier": 0.30,
        "uncalibrated_brier": 0.35,
        "minimum_domain_balanced_accuracy": 0.50,
        "maximum_domain_drop": 0.10,
        "empty_primary_cells": 0,
        "t1_balanced_accuracy_drop": 0.10,
        "t1_false_known_increase": 0.03,
    }


class SurfaceBaselineTests(unittest.TestCase):
    def test_surface_feature_semantics(self) -> None:
        text = "Hello, WORLD!\n42 cats."
        values = surface_statistics_vector({"_text": text})
        self.assertEqual(len(values), len(SURFACE_FEATURE_NAMES))
        self.assertEqual(values[0], 4.0)
        self.assertEqual(values[1], 14.0)
        self.assertEqual(values[2], 2.0)
        self.assertAlmostEqual(values[3], 4.0)
        self.assertEqual(values[4], 1.0)
        self.assertAlmostEqual(values[6], 6 / 14)
        self.assertAlmostEqual(values[7], 1 / len(text))

    def test_surface_baseline_executes_without_persisting_text(self) -> None:
        train = []
        test = []
        for index in range(20):
            train.append(
                {
                    "model_family": "human",
                    "_text": f"I remember this day, and it felt real! {index}",
                }
            )
            train.append(
                {
                    "model_family": "model",
                    "_text": f"Structured summary: item {index}; conclusion: complete.",
                }
            )
        for index in range(8):
            test.append(
                {
                    "model_family": "human",
                    "_text": f"I recall a place, and I smiled! {index}",
                }
            )
            test.append(
                {
                    "model_family": "model",
                    "_text": f"Formal analysis: point {index}; result: verified.",
                }
            )
        result = evaluate_surface_baseline(train, test)
        self.assertGreaterEqual(result["metrics"]["accuracy"], 0.75)
        self.assertFalse(result["raw_text_persisted"])
        serialized = json.dumps(result)
        self.assertNotIn("I remember", serialized)
        assert_aggregate_output_safe(result)


class ConformalUnknownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        reference = []
        calibration = []
        for index in range(12):
            reference.append(
                {"model_family": "a", "vector": [1.0, 0.01 * index]}
            )
            reference.append(
                {"model_family": "b", "vector": [0.01 * index, 1.0]}
            )
        for index in range(19):
            calibration.append(
                {"model_family": "a", "vector": [1.0, 0.005 * index]}
            )
            calibration.append(
                {"model_family": "b", "vector": [0.005 * index, 1.0]}
            )
        calibration.append(
            {"model_family": "a", "vector": [0.707, 0.707]}
        )
        calibration.append(
            {"model_family": "b", "vector": [0.707, 0.707]}
        )
        cls.model = fit_class_conditional_conformal(
            reference,
            calibration,
            vector,
            alpha=0.05,
        )

    def test_known_decision(self) -> None:
        result = predict_conformal_unknown(
            self.model,
            [0.99, 0.03],
            minimum_evidence_passed=True,
        )
        self.assertEqual(result["decision"], "KNOWN")
        self.assertEqual(result["predicted_class"], "a")

    def test_ood_decision(self) -> None:
        result = predict_conformal_unknown(
            self.model,
            [-1.0, -1.0],
            minimum_evidence_passed=True,
        )
        self.assertEqual(result["decision"], "UNKNOWN_OOD")

    def test_ambiguous_decision(self) -> None:
        result = predict_conformal_unknown(
            self.model,
            [0.707, 0.707],
            minimum_evidence_passed=True,
        )
        self.assertEqual(result["decision"], "UNKNOWN_AMBIGUOUS")

    def test_insufficient_evidence_decision(self) -> None:
        result = predict_conformal_unknown(
            self.model,
            [1.0, 0.0],
            minimum_evidence_passed=False,
        )
        self.assertEqual(
            result["decision"],
            "UNKNOWN_INSUFFICIENT_EVIDENCE",
        )
        self.assertEqual(result["p_values"], {})


class CalibrationTests(unittest.TestCase):
    def test_temperature_scaling_reduces_nll_on_overconfident_fixture(self) -> None:
        logits = [
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [0.0, 8.0],
            [0.0, 8.0],
        ]
        truth = ["a", "a", "a", "a", "b", "b", "b", "b"]
        result = fit_temperature_scaling(
            logits,
            truth,
            ("a", "b"),
            ece_bins=4,
        )
        self.assertGreater(result.temperature, 1.0)
        self.assertLess(result.nll_after, result.nll_before)
        self.assertLess(result.brier_after, result.brier_before)

    def test_equal_frequency_ece_reference(self) -> None:
        probabilities = [
            [0.9, 0.1],
            [0.8, 0.2],
            [0.4, 0.6],
            [0.3, 0.7],
        ]
        truth = ["a", "b", "b", "b"]
        ece = expected_calibration_error(
            probabilities,
            truth,
            ("a", "b"),
            bins=2,
        )
        self.assertAlmostEqual(ece, 0.35)

    def test_softmax_is_normalized(self) -> None:
        probabilities = temperature_softmax([2.0, 1.0, -1.0], 2.0)
        self.assertAlmostEqual(sum(probabilities), 1.0)
        self.assertTrue(all(0.0 < value < 1.0 for value in probabilities))

    def test_invalid_probability_rows_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            multiclass_nll(
                [[0.8, 0.8]],
                ["a"],
                ("a", "b"),
            )


class UncertaintyTests(unittest.TestCase):
    def test_wilson_reference_interval(self) -> None:
        lower, upper = wilson_interval(10, 100)
        self.assertAlmostEqual(lower, 0.055229, places=5)
        self.assertAlmostEqual(upper, 0.174366, places=5)

    def test_group_bootstrap_is_deterministic_and_paired(self) -> None:
        truth = ["a"] * 8 + ["b"] * 8
        groups = [f"a-{i // 2}" for i in range(8)] + [
            f"b-{i // 2}" for i in range(8)
        ]
        better = [
            "a", "a", "a", "a", "a", "a", "b", "a",
            "b", "b", "b", "b", "b", "b", "a", "b",
        ]
        worse = [
            "a", "b", "a", "b", "a", "b", "b", "a",
            "b", "a", "b", "a", "b", "a", "a", "b",
        ]
        first = paired_group_bootstrap_delta(
            truth,
            better,
            worse,
            groups,
            resamples=500,
            seed=20260730,
        )
        second = paired_group_bootstrap_delta(
            truth,
            better,
            worse,
            groups,
            resamples=500,
            seed=20260730,
        )
        self.assertEqual(first, second)
        self.assertGreater(first["point_delta"], 0.0)
        self.assertEqual(first["group_count"], 8)


class ClaimMatrixTests(unittest.TestCase):
    def test_all_clear_fixture(self) -> None:
        result = evaluate_claim_narrowing(passing_claim_values())
        self.assertTrue(result["all_gates_clear"])
        self.assertEqual(result["triggered_rule_ids"], [])
        self.assertFalse(result["stage_b_authorised"])

    def test_each_failure_gate_is_executable(self) -> None:
        mutations = {
            "OPEN_WORLD_FALSE_KNOWN": (
                "held_out_false_known_point",
                0.11,
            ),
            "UNKNOWN_REJECTION": ("held_out_unknown_rejection", 0.89),
            "KNOWN_COVERAGE": ("known_coverage", 0.59),
            "KNOWN_SIGNAL": ("best_system_macro_f1", 0.49),
            "COGNIPRINT_VS_NGRAM": (
                "cogniprint_vs_ngram_ci_lower",
                0.0,
            ),
            "PER_CLASS_COLLAPSE": ("minimum_known_class_recall", 0.39),
            "CALIBRATION_FAILURE": ("ece", 0.11),
            "DOMAIN_COLLAPSE": (
                "minimum_domain_balanced_accuracy",
                0.39,
            ),
            "STRATUM_REPLICATION": ("empty_primary_cells", 1),
            "T1_ROBUSTNESS": ("t1_balanced_accuracy_drop", 0.16),
        }
        for expected_rule, (key, value) in mutations.items():
            with self.subTest(rule=expected_rule):
                inputs = passing_claim_values()
                inputs[key] = value
                result = evaluate_claim_narrowing(inputs)
                self.assertIn(
                    expected_rule,
                    result["triggered_rule_ids"],
                )

    def test_aggregate_privacy_guard(self) -> None:
        safe = evaluate_claim_narrowing(passing_claim_values())
        assert_aggregate_output_safe(safe)
        unsafe = copy.deepcopy(safe)
        unsafe["raw_text"] = "not allowed"
        with self.assertRaises(ValueError):
            assert_aggregate_output_safe(unsafe)


if __name__ == "__main__":
    unittest.main()
