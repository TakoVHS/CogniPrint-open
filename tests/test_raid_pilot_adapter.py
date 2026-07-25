from __future__ import annotations

import hashlib
import unittest

from cogniprint.benchmarks.raid import RaidPilotConfig, collect_records, feature_record, is_eligible_row
from cogniprint.fingerprint import FEATURE_NAMES, FINGERPRINT_VERSION


class RaidPilotAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = RaidPilotConfig(models=("human", "gpt4"), domains=("abstracts",), per_cell=1)

    def test_model_row_requires_frozen_generation_settings(self) -> None:
        good = {
            "model": "gpt4",
            "domain": "abstracts",
            "attack": "none",
            "decoding": "sampling",
            "repetition_penalty": "no",
        }
        bad = {**good, "decoding": "greedy"}
        self.assertTrue(is_eligible_row(good, self.config))
        self.assertFalse(is_eligible_row(bad, self.config))

    def test_human_control_does_not_require_decoding_fields(self) -> None:
        row = {"model": "human", "domain": "abstracts", "attack": "none"}
        self.assertTrue(is_eligible_row(row, self.config))

    def test_feature_record_omits_raw_text_and_prompt(self) -> None:
        text = "This is a compact human-readable benchmark sample for deterministic testing."
        prompt = "Write a compact benchmark sample."
        row = {
            "id": "row-1",
            "source_id": "source-1",
            "model": "gpt4",
            "domain": "abstracts",
            "attack": "none",
            "decoding": "sampling",
            "repetition_penalty": "no",
            "generation": text,
            "prompt": prompt,
        }
        record = feature_record(row, self.config)
        self.assertNotIn("generation", record)
        self.assertNotIn("prompt", record)
        self.assertEqual(record["text_sha256"], hashlib.sha256(text.encode("utf-8")).hexdigest())
        self.assertEqual(record["fingerprint_version"], FINGERPRINT_VERSION)
        self.assertEqual(set(record["features_raw"]), set(FEATURE_NAMES))
        self.assertEqual(set(record["features_normalized"]), set(FEATURE_NAMES))

    def test_collect_records_balances_requested_cells(self) -> None:
        rows = [
            {
                "id": "wrong-setting",
                "model": "gpt4",
                "domain": "abstracts",
                "attack": "none",
                "decoding": "greedy",
                "repetition_penalty": "no",
                "generation": "This row should be ignored because decoding is not frozen to sampling.",
            },
            {
                "id": "human-1",
                "model": "human",
                "domain": "abstracts",
                "attack": "none",
                "generation": "A human control passage provides the comparison class for this small unit test.",
            },
            {
                "id": "gpt4-1",
                "model": "gpt4",
                "domain": "abstracts",
                "attack": "none",
                "decoding": "sampling",
                "repetition_penalty": "no",
                "generation": "A generated passage provides the second balanced cell for this small unit test.",
            },
        ]
        records, scanned = collect_records(rows, self.config)
        self.assertEqual(scanned, 3)
        self.assertEqual(len(records), 2)
        self.assertEqual({record["model_family"] for record in records}, {"human", "gpt4"})


if __name__ == "__main__":
    unittest.main()
