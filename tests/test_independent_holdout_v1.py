import unittest
from pathlib import Path

from scripts.check_independent_holdout_v1 import validate
from scripts.generate_independent_holdout_v1 import (
    TRANSFORMS,
    digest_text,
    metric_summary,
    punctuation_strip,
    sentence_rotate,
    token_pair_swap,
    token_stride_drop,
    token_stride_duplicate,
)


class IndependentHoldoutV1Tests(unittest.TestCase):
    def test_transform_family_is_locked_for_v1(self) -> None:
        self.assertEqual(
            sorted(TRANSFORMS),
            [
                "holdout_punctuation_strip",
                "holdout_sentence_rotate",
                "holdout_token_pair_swap",
                "holdout_token_stride_drop",
                "holdout_token_stride_duplicate",
            ],
        )

    def test_transforms_are_deterministic(self) -> None:
        text = "One two three four five six seven eight. Next sentence follows here."
        outputs = [
            punctuation_strip(text),
            sentence_rotate(text),
            token_pair_swap(text),
            token_stride_drop(text),
            token_stride_duplicate(text),
        ]

        self.assertEqual(outputs, [
            punctuation_strip(text),
            sentence_rotate(text),
            token_pair_swap(text),
            token_stride_drop(text),
            token_stride_duplicate(text),
        ])

    def test_hash_normalizes_line_endings(self) -> None:
        self.assertEqual(digest_text("a\r\nb"), digest_text("a\nb"))

    def test_metric_summary_reports_mean(self) -> None:
        self.assertEqual(metric_summary([2.0, 4.0])["mean"], 3.0)

    def test_public_layer_is_valid_when_generated(self) -> None:
        evidence_dir = Path("evidence/independent-holdout-v1")
        if not evidence_dir.exists():
            self.skipTest("independent holdout evidence has not been generated")
        self.assertEqual(validate(Path("datasets/independent-holdout-v1"), evidence_dir), [])


if __name__ == "__main__":
    unittest.main()
