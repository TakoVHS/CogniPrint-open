from __future__ import annotations

import hashlib
import json
import unittest

from cogniprint.benchmarks.raid_m2 import (
    DEFAULT_MACHINE_FAMILIES,
    M2RoleFractions,
    fit_probability_conformal,
)
from cogniprint.benchmarks.raid_m2_1 import (
    M2_1_COVERAGE_TARGETS,
    M2_1_TEMPERATURE_GRID,
    conformal_outcome_decomposition,
    evaluate_raid_m2_1,
    selective_risk_at_frozen_threshold,
    selective_risk_at_targets,
    summarize_score_scale,
    temperature_sensitivity_profile,
)
from cogniprint.fingerprint import CognitiveFingerprint


def make_text(label: str, index: int) -> str:
    if label == "human":
        return (
            f"Personal note {index}. I walked home, noticed the weather, "
            "remembered a small detail, and wrote it down in my own words."
        )
    if label == "chatgpt":
        return (
            f"Example {index}. First define the question, then consider the "
            "main factors, and finally summarize the conclusion clearly."
        )
    if label == "gpt4":
        return (
            f"Technical example {index}: assumptions, constraints, evidence, "
            "and evaluation criteria should be separated before inference."
        )
    if label == "llama-chat":
        return (
            f"Sure, example {index}! We can compare the options step by step, "
            "note the trade-offs, and choose a concise practical explanation."
        )
    if label == "mistral-chat":
        return (
            f"Concise example {index}. Separate observation from interpretation, "
            "verify inputs, and avoid claims stronger than the evidence."
        )
    raise ValueError(label)


def make_records(per_class: int = 80) -> list[dict]:
    records: list[dict] = []
    labels = ("human", *DEFAULT_MACHINE_FAMILIES)
    for label in labels:
        for index in range(per_class):
            text = make_text(label, index)
            fingerprint = CognitiveFingerprint(text, language="en")
            records.append(
                {
                    "source_record_id": f"{label}-{index}",
                    "source_id": f"source-{label}-{index}",
                    "model_family": label,
                    "domain": "news",
                    "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "prompt_sha256": None,
                    "features_normalized": fingerprint.normalized_feature_dict(),
                    "_text": text,
                }
            )
    return records


class RaidM21DiagnosticsTests(unittest.TestCase):
    def test_selective_grid_uses_first_tie_safe_point_at_or_above_target(self) -> None:
        truth = ["a", "b", "a", "b"]
        predictions = ["a", "a", "a", "b"]
        confidences = [0.9, 0.9, 0.6, 0.2]
        rows = selective_risk_at_targets(
            truth,
            predictions,
            confidences,
            targets=[0.25, 0.50, 0.75, 1.00],
        )
        self.assertEqual(rows[0]["achieved_coverage"], 0.50)
        self.assertEqual(rows[0]["accepted"], 2)
        self.assertEqual(rows[1]["achieved_coverage"], 0.50)
        self.assertEqual(rows[2]["achieved_coverage"], 0.75)
        self.assertEqual(rows[3]["achieved_coverage"], 1.00)

    def test_frozen_threshold_risk_reports_accepted_errors_and_coverage(self) -> None:
        result = selective_risk_at_frozen_threshold(
            ["a", "b", "a", "b"],
            ["a", "a", "a", "b"],
            [0.95, 0.90, 0.70, 0.20],
            threshold=0.70,
        )
        self.assertEqual(result["accepted"], 3)
        self.assertEqual(result["errors"], 1)
        self.assertAlmostEqual(result["coverage"], 0.75)
        self.assertAlmostEqual(result["selective_risk"], 1 / 3)

    def test_conformal_decomposition_separates_empty_ambiguous_and_false_known(self) -> None:
        calibration_probabilities = (
            [[0.90, 0.10]] * 8
            + [[0.85, 0.15]] * 8
            + [[0.10, 0.90]] * 8
            + [[0.15, 0.85]] * 8
        )
        calibration_truth = ["a"] * 16 + ["b"] * 16
        model = fit_probability_conformal(
            calibration_probabilities,
            calibration_truth,
            ["a", "b"],
            alpha=0.20,
        )
        evaluation_probabilities = [
            [0.95, 0.05],
            [0.50, 0.50],
            [0.05, 0.95],
            [0.01, 0.99],
        ]
        truth = ["a", "a", "unknown", "unknown"]
        result = conformal_outcome_decomposition(
            model,
            evaluation_probabilities,
            truth,
        )
        self.assertEqual(result["known"]["total"], 2)
        self.assertEqual(result["unknown"]["total"], 2)
        self.assertAlmostEqual(
            result["unknown"]["empty_set_rate"]
            + result["unknown"]["ambiguous_set_rate"]
            + result["unknown"]["singleton_false_known_rate"],
            1.0,
        )

    def test_score_scale_and_temperature_profile_are_finite_and_frozen(self) -> None:
        scores = [
            [2.0, 0.0],
            [1.5, 0.2],
            [0.1, 1.8],
            [0.0, 2.1],
        ]
        truth = ["a", "a", "b", "b"]
        summary = summarize_score_scale(scores)
        self.assertEqual(summary["records"], 4)
        self.assertEqual(summary["classes"], 2)
        self.assertGreater(summary["margin_median"], 0.0)

        profile = temperature_sensitivity_profile(
            scores,
            truth,
            ["a", "b"],
        )
        self.assertEqual(
            [point["temperature"] for point in profile["grid"]],
            list(M2_1_TEMPERATURE_GRID),
        )
        self.assertIn(
            profile["best_grid_temperature"],
            M2_1_TEMPERATURE_GRID,
        )

    def test_full_m2_1_is_four_fold_exploratory_and_raw_text_free(self) -> None:
        result = evaluate_raid_m2_1(
            make_records(80),
            seed=20261124,
            fractions=M2RoleFractions(
                train=0.35,
                probability_calibration=0.15,
                conformal_calibration=0.30,
                threshold_development=0.10,
                evaluation=0.10,
            ),
            conformal_alpha=0.20,
            minimum_known_coverage=0.60,
            char_dimensions=512,
            word_dimensions=256,
        )
        self.assertEqual(result["status"], "POST_RESULT_EXPLORATORY")
        self.assertFalse(result["scientific_claim_evidence"])
        self.assertEqual(result["stage_b_status"], "NOT_AUTHORISED_TO_START")
        self.assertEqual(result["coverage_targets"], list(M2_1_COVERAGE_TARGETS))
        self.assertEqual(len(result["folds"]), 4)
        for fold in result["folds"]:
            self.assertEqual(fold["lineage_overlap_count"], 0)
            self.assertEqual(len(fold["representations"]), 3)
            for representation in fold["representations"].values():
                self.assertEqual(
                    len(representation["selective_risk_grid"]),
                    len(M2_1_COVERAGE_TARGETS),
                )
                self.assertIn(
                    "unknown",
                    representation["conformal_decomposition"],
                )
                self.assertIn(
                    "probability_calibration",
                    representation["score_scale"],
                )
                self.assertIn(
                    "grid",
                    representation["temperature_sensitivity"],
                )

        serialized = json.dumps(result, sort_keys=True)
        self.assertNotIn('"_text"', serialized)
        self.assertNotIn("Personal note", serialized)


if __name__ == "__main__":
    unittest.main()
