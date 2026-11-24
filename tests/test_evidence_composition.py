from __future__ import annotations

import unittest

from cogniprint.stats.evidence_composition import (
    FiniteCompositionWorld,
    composition_report,
    conditionally_redundant,
    delta_separating,
    robustly_admissible,
)


class EvidenceCompositionTheoryTests(unittest.TestCase):
    def test_strict_composition_eliminates_unsafe_worlds(self) -> None:
        worlds = [
            FiniteCompositionWorld("safe", 0.04, "z", "k_obs"),
            FiniteCompositionWorld("unsafe-a", 0.35, "z", "k_a"),
            FiniteCompositionWorld("unsafe-b", 0.60, "z", "k_b"),
        ]
        report = composition_report(worlds, "z", "k_obs")
        self.assertEqual(report.coarse_risks, (0.04, 0.35, 0.60))
        self.assertEqual(report.product_risks, (0.04,))
        self.assertTrue(report.strict_shrink)
        self.assertTrue(report.strict_worst_case_gain)
        self.assertFalse(robustly_admissible(report.coarse_upper, 0.10))
        self.assertTrue(robustly_admissible(report.product_upper, 0.10))
        self.assertTrue(delta_separating(worlds, "z", "k_obs", 0.10))

    def test_redundant_channel_does_not_shrink_risk_set(self) -> None:
        worlds = [
            FiniteCompositionWorld("safe", 0.04, "z", "same"),
            FiniteCompositionWorld("unsafe-a", 0.35, "z", "same"),
            FiniteCompositionWorld("unsafe-b", 0.60, "z", "same"),
        ]
        report = composition_report(worlds, "z", "same")
        self.assertEqual(report.coarse_risks, report.product_risks)
        self.assertFalse(report.strict_shrink)
        self.assertFalse(report.strict_worst_case_gain)
        self.assertTrue(conditionally_redundant(worlds, "z"))
        self.assertFalse(delta_separating(worlds, "z", "same", 0.10))

    def test_partial_refinement_can_shrink_without_crossing_tolerance(self) -> None:
        worlds = [
            FiniteCompositionWorld("safe", 0.04, "z", "k_obs"),
            FiniteCompositionWorld("mid", 0.18, "z", "k_obs"),
            FiniteCompositionWorld("unsafe", 0.60, "z", "k_bad"),
        ]
        report = composition_report(worlds, "z", "k_obs")
        self.assertEqual(report.product_risks, (0.04, 0.18))
        self.assertTrue(report.strict_shrink)
        self.assertTrue(report.strict_worst_case_gain)
        self.assertFalse(robustly_admissible(report.product_upper, 0.10))
        self.assertFalse(delta_separating(worlds, "z", "k_obs", 0.10))

    def test_different_channel_name_is_not_information_gain(self) -> None:
        worlds = [
            FiniteCompositionWorld("w1", 0.05, "score", ("derived", 1)),
            FiniteCompositionWorld("w2", 0.40, "score", ("derived", 1)),
        ]
        self.assertTrue(conditionally_redundant(worlds, "score"))


if __name__ == "__main__":
    unittest.main()
