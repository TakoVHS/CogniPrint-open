import unittest

from scripts.generate_validation_v12 import (
    benjamini_hochberg_adjust,
    char_ngram_profile,
    cosine_similarity,
    holm_adjust,
    metric_summary,
)


class ValidationV12Tests(unittest.TestCase):
    def test_holm_adjustment_is_monotone_by_sorted_p_values(self) -> None:
        rows = [
            {"axis": "a", "reported_p_value": 0.01},
            {"axis": "b", "reported_p_value": 0.03},
            {"axis": "c", "reported_p_value": 0.04},
        ]

        adjusted = holm_adjust(rows)

        self.assertEqual(adjusted["a"], 0.03)
        self.assertEqual(adjusted["b"], 0.06)
        self.assertEqual(adjusted["c"], 0.06)

    def test_bh_adjustment_uses_reverse_cumulative_minimum(self) -> None:
        rows = [
            {"axis": "a", "reported_p_value": 0.01},
            {"axis": "b", "reported_p_value": 0.03},
            {"axis": "c", "reported_p_value": 0.2},
        ]

        adjusted = benjamini_hochberg_adjust(rows)

        self.assertEqual(adjusted["a"], 0.03)
        self.assertEqual(adjusted["b"], 0.045)
        self.assertEqual(adjusted["c"], 0.2)

    def test_character_ngram_cosine_is_identical_for_same_text(self) -> None:
        profile = char_ngram_profile("Compact profile stability.")

        self.assertAlmostEqual(cosine_similarity(profile, profile), 1.0)

    def test_metric_summary_is_stable_for_small_values(self) -> None:
        summary = metric_summary([0.1, 0.2, 0.3])

        self.assertEqual(summary["count"], 3)
        self.assertEqual(summary["mean"], 0.2)
        self.assertEqual(summary["median"], 0.2)


if __name__ == "__main__":
    unittest.main()
