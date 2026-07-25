from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "evaluate_challenge_predictions.py"
GOLDEN_DIR = ROOT / "tests" / "golden" / "challenge-evaluator"

SPEC = importlib.util.spec_from_file_location("challenge_evaluator", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("cannot load challenge evaluator")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ChallengeEvaluatorGoldenTests(unittest.TestCase):
    def test_golden_cases(self) -> None:
        fixtures = sorted(GOLDEN_DIR.glob("*.json"))
        self.assertGreaterEqual(len(fixtures), 8)

        for path in fixtures:
            with self.subTest(fixture=path.name):
                fixture = json.loads(path.read_text(encoding="utf-8"))
                report = MODULE.evaluate(fixture["predictions"], fixture["labels"], ece_bins=5)
                expected = fixture["expected"]
                closed = report["closed_set_known_reference"]
                open_world = report["open_world_unknown_reference"]

                mapping = {
                    "top1_accuracy": closed["top1_accuracy_with_abstentions_as_errors"],
                    "balanced_accuracy": closed["balanced_accuracy_with_abstentions_as_errors"],
                    "macro_f1": closed["macro_f1_with_abstentions_as_errors"],
                    "coverage": closed["coverage_on_known_reference"],
                    "selective_accuracy": closed["selective_accuracy_on_issued_known"],
                    "selective_risk": closed["selective_risk_on_issued_known"],
                    "unknown_rejection_rate": open_world["unknown_rejection_rate"],
                    "false_known_rate": open_world["false_known_rate"],
                }

                for key, expected_value in expected.items():
                    if key == "per_class":
                        for class_name, class_expected in expected_value.items():
                            actual = closed["per_class"][class_name]
                            for metric_name, metric_expected in class_expected.items():
                                self.assertEqual(actual[metric_name], metric_expected)
                    else:
                        self.assertEqual(mapping[key], expected_value)


if __name__ == "__main__":
    unittest.main()
