from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "evaluate_challenge_predictions.py"
SPEC = importlib.util.spec_from_file_location("challenge_evaluator", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("cannot load challenge evaluator")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ChallengeEvaluatorTests(unittest.TestCase):
    def test_known_unknown_and_calibration_metrics(self) -> None:
        predictions = [
            {
                "sample_id": "k-a",
                "decision": "known",
                "top1_candidate": "A",
                "confidence": 0.8,
                "calibrated": True,
                "probabilities": {"A": 0.8, "B": 0.2},
            },
            {
                "sample_id": "k-b",
                "decision": "unknown",
                "top1_candidate": None,
            },
            {
                "sample_id": "u-1",
                "decision": "unknown",
                "top1_candidate": None,
            },
            {
                "sample_id": "u-2",
                "decision": "known",
                "top1_candidate": "A",
                "confidence": 0.7,
                "calibrated": True,
                "probabilities": {"A": 0.7, "B": 0.3},
            },
        ]
        labels = [
            {"sample_id": "k-a", "true_class": "A", "known_to_reference": True},
            {"sample_id": "k-b", "true_class": "B", "known_to_reference": True},
            {"sample_id": "u-1", "true_class": "HELD_OUT_X", "known_to_reference": False},
            {"sample_id": "u-2", "true_class": "HELD_OUT_X", "known_to_reference": False},
        ]

        report = MODULE.evaluate(predictions, labels, ece_bins=5)
        closed = report["closed_set_known_reference"]
        open_world = report["open_world_unknown_reference"]

        self.assertEqual(closed["top1_accuracy_with_abstentions_as_errors"], 0.5)
        self.assertEqual(closed["balanced_accuracy_with_abstentions_as_errors"], 0.5)
        self.assertEqual(closed["coverage_on_known_reference"], 0.5)
        self.assertEqual(closed["selective_accuracy_on_issued_known"], 1.0)
        self.assertEqual(closed["selective_risk_on_issued_known"], 0.0)
        self.assertEqual(open_world["unknown_rejection_rate"], 0.5)
        self.assertEqual(open_world["false_known_rate"], 0.5)
        self.assertEqual(report["calibration"]["multiclass_brier_known_reference"], 0.08)
        self.assertAlmostEqual(report["calibration"]["ece_known_issued_decisions"]["ece"], 0.2)

    def test_prediction_ground_truth_fields_are_rejected(self) -> None:
        prediction = {
            "sample_id": "x",
            "decision": "unknown",
            "top1_candidate": None,
            "true_class": "LEAK",
        }
        with self.assertRaisesRegex(ValueError, "ground-truth fields are forbidden"):
            MODULE.validate_prediction(prediction)

    def test_abstention_cannot_smuggle_candidate(self) -> None:
        prediction = {
            "sample_id": "x",
            "decision": "unknown",
            "top1_candidate": "A",
        }
        with self.assertRaisesRegex(ValueError, "must not carry top1_candidate"):
            MODULE.validate_prediction(prediction)

    def test_prediction_and_label_sets_must_match(self) -> None:
        predictions = [{"sample_id": "a", "decision": "unknown", "top1_candidate": None}]
        labels = [{"sample_id": "b", "true_class": "B", "known_to_reference": True}]
        with self.assertRaisesRegex(ValueError, "sample sets differ"):
            MODULE.evaluate(predictions, labels, ece_bins=10)

    def test_probabilities_require_calibrated_true(self) -> None:
        prediction = {
            "sample_id": "x",
            "decision": "known",
            "top1_candidate": "A",
            "confidence": 0.6,
            "calibrated": False,
            "probabilities": {"A": 0.6, "B": 0.4},
        }
        with self.assertRaisesRegex(ValueError, "probabilities require calibrated=true"):
            MODULE.validate_prediction(prediction)


if __name__ == "__main__":
    unittest.main()
