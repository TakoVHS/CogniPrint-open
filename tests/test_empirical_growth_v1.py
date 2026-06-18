import unittest
from pathlib import Path

from scripts.generate_empirical_growth_v1 import (
    EXTRA_TRANSFORMS,
    digest_text,
    metric_summary,
    transform_punctuation_strip,
    transform_sentence_order_rotate,
    transform_token_pair_swap,
    transform_token_stride_drop,
    transform_token_stride_duplicate,
)
from scripts.check_empirical_growth_v1 import validate


class EmpiricalGrowthV1Tests(unittest.TestCase):
    def test_extra_transform_family_is_locked_for_v1(self) -> None:
        self.assertEqual(
            sorted(EXTRA_TRANSFORMS),
            [
                "punctuation_strip",
                "sentence_order_rotate",
                "token_pair_swap",
                "token_stride_drop",
                "token_stride_duplicate",
            ],
        )

    def test_transforms_are_deterministic(self) -> None:
        text = "One two three four five six seven eight nine ten eleven twelve. Next sentence."
        outputs = [
            transform_token_pair_swap(text),
            transform_token_stride_drop(text),
            transform_token_stride_duplicate(text),
            transform_sentence_order_rotate(text),
            transform_punctuation_strip(text),
        ]

        self.assertEqual(outputs, [
            transform_token_pair_swap(text),
            transform_token_stride_drop(text),
            transform_token_stride_duplicate(text),
            transform_sentence_order_rotate(text),
            transform_punctuation_strip(text),
        ])

    def test_hash_normalizes_line_endings(self) -> None:
        self.assertEqual(digest_text("a\r\nb"), digest_text("a\nb"))

    def test_metric_summary_reports_count_and_mean(self) -> None:
        summary = metric_summary([1.0, 2.0, 3.0])

        self.assertEqual(summary["count"], 3)
        self.assertEqual(summary["mean"], 2.0)

    def test_public_layer_does_not_store_raw_text_fields(self) -> None:
        errors = validate(Path("evidence/empirical-growth-v1"))

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
