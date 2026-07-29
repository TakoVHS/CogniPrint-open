from __future__ import annotations

import unittest

from cogniprint.benchmarks.evaluation import evaluate_pilot, grouped_split, lineage_group
from cogniprint.fingerprint import FEATURE_NAMES


def synthetic_records(group_count: int = 40) -> list[dict]:
    records: list[dict] = []
    for index in range(group_count):
        source_id = f"source-{index:03d}"
        for label, value in (("class-a", 0.0), ("class-b", 1.0)):
            records.append(
                {
                    "source_id": source_id,
                    "text_sha256": f"{index:064x}"[-64:],
                    "model_family": label,
                    "character_count": 500,
                    "token_count": 100,
                    "features_normalized": {name: value for name in FEATURE_NAMES},
                }
            )
    return records


class RaidPilotEvaluationTests(unittest.TestCase):
    def test_grouped_split_is_deterministic_and_has_no_lineage_overlap(self) -> None:
        records = synthetic_records()
        left_train, left_test = grouped_split(records, seed=20260725)
        right_train, right_test = grouped_split(records, seed=20260725)

        self.assertEqual(
            [record["source_id"] for record in left_train],
            [record["source_id"] for record in right_train],
        )
        self.assertEqual(
            [record["source_id"] for record in left_test],
            [record["source_id"] for record in right_test],
        )
        self.assertFalse(
            {lineage_group(record) for record in left_train}
            & {lineage_group(record) for record in left_test}
        )

    def test_grouped_split_uses_prompt_hash_when_source_id_is_missing(self) -> None:
        records = []
        for index in range(20):
            prompt_sha = f"prompt-{index:03d}"
            for label, value in (("class-a", 0.0), ("class-b", 1.0)):
                records.append(
                    {
                        "prompt_sha256": prompt_sha,
                        "text_sha256": f"{index:064x}"[-64:],
                        "model_family": label,
                        "character_count": 400,
                        "token_count": 80,
                        "features_normalized": {name: value for name in FEATURE_NAMES},
                    }
                )
        train, test = grouped_split(records, seed=20260725)
        self.assertFalse({lineage_group(record) for record in train} & {lineage_group(record) for record in test})

    def test_12d_baseline_beats_length_only_on_separable_synthetic_features(self) -> None:
        result = evaluate_pilot(synthetic_records(), seed=20260725)
        self.assertEqual(result["chance_accuracy_reference"], 0.5)
        self.assertEqual(result["cogniprint_12d_nearest_centroid"]["accuracy"], 1.0)
        self.assertEqual(result["cogniprint_12d_nearest_centroid"]["balanced_accuracy"], 1.0)
        self.assertEqual(result["length_only_nearest_centroid"]["accuracy"], 0.5)
        self.assertEqual(result["majority"]["accuracy"], 0.5)


if __name__ == "__main__":
    unittest.main()
