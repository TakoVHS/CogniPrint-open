from __future__ import annotations

import hashlib
import json
import unittest

from cogniprint.benchmarks.evaluation import lineage_group
from cogniprint.benchmarks.raid_m2 import (
    DEFAULT_MACHINE_FAMILIES,
    M2RoleFractions,
    build_open_set_fold,
    evaluate_raid_m2,
    fit_probability_conformal,
    select_threshold_for_min_coverage,
)
from cogniprint.fingerprint import CognitiveFingerprint


def make_text(label: str, index: int) -> str:
    if label == "human":
        return (
            f"I remember walking home after school on day {index}. "
            "The weather changed, I noticed a small detail, and I wrote it down "
            "because the memory felt oddly personal."
        )
    if label == "chatgpt":
        return (
            f"Here is a clear explanation for example {index}. "
            "First, define the problem. Second, examine the main factors. "
            "Finally, summarize the practical conclusion in a balanced way."
        )
    if label == "gpt4":
        return (
            f"Technical analysis {index}: the system can be decomposed into "
            "three interacting components; assumptions, constraints, and "
            "evaluation criteria should be stated explicitly before inference."
        )
    if label == "llama-chat":
        return (
            f"Sure, example {index}! Let's explore the idea step by step. "
            "We can compare the options, note the trade-offs, and then choose "
            "a simple explanation that stays useful and concise."
        )
    if label == "mistral-chat":
        return (
            f"Concise response {index}. Key point: separate evidence from "
            "interpretation, verify the inputs, and avoid a stronger conclusion "
            "than the observations justify."
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


class RaidCalibrationM2Tests(unittest.TestCase):
    def test_fold_keeps_unknown_out_of_training_and_forces_shared_lineage_to_eval(self) -> None:
        records = make_records(120)
        shared = "shared-lineage"
        records[0]["source_id"] = shared
        unknown = next(
            record
            for record in records
            if record["model_family"] == "mistral-chat"
        )
        unknown["source_id"] = shared

        fold = build_open_set_fold(
            records,
            unknown_family="mistral-chat",
            seed=20261124,
            conformal_alpha=0.10,
        )
        self.assertEqual(fold["lineage_overlap_count"], 0)
        for role in (
            "train",
            "probability_calibration",
            "conformal_calibration",
            "threshold_development",
        ):
            self.assertNotIn(
                "mistral-chat",
                {record["model_family"] for record in fold["roles"][role]},
            )
        shared_roles = {
            row["role"]
            for row in fold["role_manifest"]
            if row["lineage_group"] == f"source_id:{shared}"
        }
        self.assertEqual(shared_roles, {"evaluation"})

        role_groups = {
            role: {lineage_group(record) for record in values}
            for role, values in fold["roles"].items()
        }
        for index, left in enumerate(role_groups):
            for right in list(role_groups)[index + 1 :]:
                self.assertFalse(role_groups[left] & role_groups[right])

    def test_probability_conformal_fails_closed_when_resolution_is_too_small(self) -> None:
        probabilities = [
            [0.9, 0.1],
            [0.8, 0.2],
            [0.1, 0.9],
            [0.2, 0.8],
        ]
        truth = ["a", "a", "b", "b"]
        with self.assertRaisesRegex(
            ValueError,
            "INSUFFICIENT DEVELOPMENT EVIDENCE",
        ):
            fit_probability_conformal(
                probabilities,
                truth,
                ["a", "b"],
                alpha=0.05,
            )

    def test_threshold_selection_uses_highest_tie_safe_cutoff_meeting_coverage(self) -> None:
        probabilities = [
            [0.95, 0.05],
            [0.90, 0.10],
            [0.90, 0.10],
            [0.70, 0.30],
            [0.60, 0.40],
        ]
        result = select_threshold_for_min_coverage(
            probabilities,
            min_coverage=0.60,
        )
        self.assertAlmostEqual(result["threshold"], 0.90)
        self.assertAlmostEqual(result["development_coverage"], 0.60)

    def test_full_m2_runs_four_predeclared_unknown_folds_without_raw_text_output(self) -> None:
        records = make_records(80)
        result = evaluate_raid_m2(
            records,
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
            bootstrap_resamples=100,
        )
        self.assertEqual(result["status"], "DEVELOPMENT_ONLY")
        self.assertFalse(result["scientific_claim_evidence"])
        self.assertEqual(result["stage_b_status"], "NOT_AUTHORISED_TO_START")
        self.assertEqual(
            [fold["unknown_family"] for fold in result["folds"]],
            list(DEFAULT_MACHINE_FAMILIES),
        )
        for fold in result["folds"]:
            self.assertEqual(fold["lineage_overlap_count"], 0)
            self.assertEqual(len(fold["representations"]), 3)
            for representation in fold["representations"].values():
                self.assertIn("calibrated_nll", representation["probability_quality"])
                self.assertIn("calibrated_brier", representation["probability_quality"])
                self.assertIn("aurc", representation["selective"])
                self.assertIn("false_known_rate", representation["open_set"])
                self.assertIn(
                    "unknown_false_known_rate",
                    representation["conformal"],
                )

        serialized = json.dumps(result, sort_keys=True)
        self.assertNotIn('"_text"', serialized)
        self.assertNotIn("I remember walking home", serialized)


if __name__ == "__main__":
    unittest.main()
