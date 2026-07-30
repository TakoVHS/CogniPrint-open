from __future__ import annotations

import unittest

from cogniprint.benchmarks.development_methods import (
    ConformalModel,
    UNKNOWN_AMBIGUOUS,
    UNKNOWN_INSUFFICIENT_EVIDENCE,
    UNKNOWN_OOD,
    conformal_decision,
    evaluate_surface_baseline,
    fit_class_conditional_conformal,
    fit_temperature,
    surface_statistics,
)
from cogniprint.benchmarks.development_statistics import (
    evaluate_claim_narrowing,
    paired_group_bootstrap_delta,
    wilson_interval,
)


def vector(record: dict) -> list[float]:
    return list(record["_vector"])


def record(label: str, group: str, values: list[float]) -> dict:
    return {"model_family": label, "source_id": group, "_vector": values}


class StageADevelopmentMethodsTests(unittest.TestCase):
    def reference_and_calibration(self) -> tuple[list[dict], list[dict]]:
        reference = [
            record("a", "ar1", [2.0, 0.0]),
            record("a", "ar2", [1.8, 0.1]),
            record("b", "br1", [0.0, 2.0]),
            record("b", "br2", [0.1, 1.8]),
        ]
        calibration = [
            record("a", "ac1", [1.9, 0.0]),
            record("a", "ac2", [1.7, 0.1]),
            record("a", "ac3", [2.1, -0.1]),
            record("a", "ac4", [1.8, 0.0]),
            record("b", "bc1", [0.0, 1.9]),
            record("b", "bc2", [0.1, 1.7]),
            record("b", "bc3", [-0.1, 2.1]),
            record("b", "bc4", [0.0, 1.8]),
        ]
        return reference, calibration

    def test_surface_statistics_feature_map(self) -> None:
        values = surface_statistics("HELLO, world!\nLine 2.")
        self.assertEqual(values["word_count"], 4.0)
        self.assertEqual(values["sentence_count"], 2.0)
        self.assertGreater(values["uppercase_ratio"], 0.0)
        self.assertGreater(values["newline_ratio"], 0.0)

    def test_surface_baseline_is_transparent_and_metadata_only(self) -> None:
        reference: list[dict] = []
        test: list[dict] = []
        for index in range(8):
            reference.append(
                {
                    "model_family": "a",
                    "source_id": f"ar{index}",
                    "_text": (
                        "I remember this small story, and it felt personal. "
                        f"Item {index}."
                    ),
                }
            )
            reference.append(
                {
                    "model_family": "b",
                    "source_id": f"br{index}",
                    "_text": (
                        f"SECTION {index}: SYSTEMATIC RESULT; "
                        "VALUE 1234; CONCLUSION!"
                    ),
                }
            )
        for index in range(3):
            test.append(
                {
                    "model_family": "a",
                    "source_id": f"at{index}",
                    "_text": (
                        "I recall another ordinary moment, and it felt calm. "
                        f"Case {index}."
                    ),
                }
            )
            test.append(
                {
                    "model_family": "b",
                    "source_id": f"bt{index}",
                    "_text": (
                        f"SECTION {index}: FORMAL RESULT; "
                        "VALUE 9876; SUMMARY!"
                    ),
                }
            )
        result = evaluate_surface_baseline(reference, test)
        self.assertEqual(result["status"], "DEVELOPMENT_ONLY")
        self.assertFalse(result["scientific_claim_evidence"])
        self.assertFalse(result["raw_text_persisted"])
        self.assertGreaterEqual(result["metrics"]["accuracy"], 0.8)
        self.assertNotIn("I remember this small story", str(result))

    def test_conformal_known_ood_ambiguous_and_insufficient(self) -> None:
        reference, calibration = self.reference_and_calibration()
        model = fit_class_conditional_conformal(
            reference,
            calibration,
            vector,
            alpha=0.2,
        )
        known = conformal_decision(
            model,
            record("", "x1", [2.0, 0.0]),
            vector,
        )
        self.assertEqual(known["decision"], "a")
        unknown = conformal_decision(
            model,
            record("", "x2", [10.0, 10.0]),
            vector,
        )
        self.assertEqual(unknown["decision"], UNKNOWN_OOD)
        insufficient = conformal_decision(
            model,
            record("", "x3", [2.0, 0.0]),
            vector,
            evidence_sufficient=False,
        )
        self.assertEqual(
            insufficient["decision"],
            UNKNOWN_INSUFFICIENT_EVIDENCE,
        )
        ambiguous_model = ConformalModel(
            model.centroid_model,
            0.05,
            {label: (2.0,) for label in model.centroid_model.labels},
        )
        ambiguous = conformal_decision(
            ambiguous_model,
            record("", "x4", [1.0, 1.0]),
            vector,
        )
        self.assertEqual(ambiguous["decision"], UNKNOWN_AMBIGUOUS)

    def test_conformal_rejects_partition_leakage(self) -> None:
        reference = [
            record("a", "same", [2.0, 0.0]),
            record("b", "b1", [0.0, 2.0]),
        ]
        calibration = [
            record("a", "same", [1.9, 0.0]),
            record("b", "b2", [0.0, 1.9]),
        ]
        with self.assertRaisesRegex(ValueError, "both"):
            fit_class_conditional_conformal(reference, calibration, vector)

    def test_conformal_rejects_missing_calibration_class(self) -> None:
        reference, calibration = self.reference_and_calibration()
        calibration = [
            item for item in calibration if item["model_family"] == "a"
        ]
        with self.assertRaisesRegex(
            ValueError,
            "missing conformal calibration",
        ):
            fit_class_conditional_conformal(reference, calibration, vector)

    def test_temperature_calibration_is_deterministic_and_improves_nll(
        self,
    ) -> None:
        labels = ["a", "b"]
        truth = ["a", "a", "a", "b", "b", "b", "a", "b"]
        logits = [
            [8, 0],
            [7, 0],
            [0, 8],
            [0, 7],
            [0, 8],
            [8, 0],
            [6, 0],
            [0, 6],
        ]
        first = fit_temperature(logits, truth, labels)
        second = fit_temperature(logits, truth, labels)
        self.assertAlmostEqual(first.temperature, second.temperature, places=12)
        self.assertGreater(first.temperature, 1.0)
        self.assertLess(first.calibrated_nll, first.uncalibrated_nll)
        self.assertGreaterEqual(first.temperature, 0.05)
        self.assertLessEqual(first.temperature, 20.0)

    def test_temperature_calibration_rejects_invalid_logits(self) -> None:
        with self.assertRaisesRegex(ValueError, "width"):
            fit_temperature([[1.0], [2.0]], ["a", "b"], ["a", "b"])
        with self.assertRaisesRegex(ValueError, "finite"):
            fit_temperature(
                [[float("nan"), 0.0]],
                ["a"],
                ["a", "b"],
            )

    def test_wilson_interval(self) -> None:
        lower, upper = wilson_interval(18, 216)
        self.assertLess(lower, 18 / 216)
        self.assertGreater(upper, 18 / 216)
        self.assertAlmostEqual(lower, 0.0533, places=3)
        self.assertAlmostEqual(upper, 0.1280, places=3)

    def test_bootstrap_is_deterministic_and_grouped(self) -> None:
        truth = ["a", "a", "b", "b", "a", "b", "a", "b"]
        predictions_a = ["a", "a", "b", "b", "a", "b", "a", "b"]
        predictions_b = ["a", "b", "b", "a", "a", "a", "b", "b"]
        groups = ["g1", "g1", "g2", "g2", "g3", "g3", "g4", "g4"]
        first = paired_group_bootstrap_delta(
            truth,
            predictions_a,
            predictions_b,
            groups,
            resamples=500,
            seed=7,
        )
        second = paired_group_bootstrap_delta(
            truth,
            predictions_a,
            predictions_b,
            groups,
            resamples=500,
            seed=7,
        )
        self.assertEqual(first, second)
        self.assertGreater(first["point_delta"], 0)
        self.assertEqual(first["group_count"], 4)

    def test_bootstrap_rejects_unpaired_inputs(self) -> None:
        with self.assertRaisesRegex(ValueError, "equal length"):
            paired_group_bootstrap_delta(["a"], ["a"], [], ["g1"])

    def test_claim_matrix_triggers_exact_failures(self) -> None:
        metrics = {
            "held_out_false_known_point": 0.12,
            "held_out_false_known_wilson_upper": 0.17,
            "held_out_unknown_rejection": 0.88,
            "known_coverage": 0.55,
            "best_frozen_system_balanced_accuracy": 0.60,
            "best_frozen_system_macro_f1": 0.58,
            "cogniprint_vs_ngram_delta_macro_f1": -0.01,
            "cogniprint_vs_ngram_ci_lower": -0.04,
            "minimum_known_class_recall": 0.35,
            "ece": 0.12,
            "calibrated_nll": 0.9,
            "uncalibrated_nll": 0.8,
            "calibrated_brier": 0.4,
            "uncalibrated_brier": 0.35,
            "minimum_domain_balanced_accuracy": 0.38,
            "maximum_domain_gap": 0.18,
            "any_empty_primary_cell": True,
            "t1_balanced_accuracy_drop": 0.20,
            "t1_false_known_increase": 0.07,
        }
        result = evaluate_claim_narrowing(metrics)
        expected = {
            "OPEN_WORLD_FALSE_KNOWN",
            "UNKNOWN_REJECTION",
            "KNOWN_COVERAGE",
            "COGNIPRINT_VS_NGRAM",
            "PER_CLASS_COLLAPSE",
            "CALIBRATION_FAILURE",
            "DOMAIN_COLLAPSE",
            "STRATUM_REPLICATION",
            "T1_ROBUSTNESS",
        }
        self.assertFalse(result["all_claims_unlocked"])
        self.assertEqual(set(result["triggered_rule_ids"]), expected)
        self.assertEqual(result["status"], "DEVELOPMENT_ONLY")

    def test_claim_matrix_fails_closed_on_missing_metric(self) -> None:
        with self.assertRaisesRegex(ValueError, "incomplete"):
            evaluate_claim_narrowing({})


if __name__ == "__main__":
    unittest.main()
