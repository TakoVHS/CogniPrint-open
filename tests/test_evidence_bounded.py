from __future__ import annotations

import unittest

from cogniprint.stats.evidence_bounded import (
    certified_correctness_lower_bound,
    conformal_singleton_risk_upper_bound,
    coverage_lower_bound_from_mean_confidence,
    false_known_rate,
    finite_space_selective_summary,
    selective_risk_upper_bound,
    threshold_for_target_risk,
    uniform_calibration_defect,
)


class EvidenceBoundedTheoryTests(unittest.TestCase):
    def test_selective_risk_certificate(self) -> None:
        self.assertAlmostEqual(selective_risk_upper_bound(0.90, 0.03), 0.13)
        self.assertAlmostEqual(certified_correctness_lower_bound(0.90, 0.03), 0.87)
        self.assertAlmostEqual(threshold_for_target_risk(0.10, 0.03), 0.93)

    def test_certificate_can_be_infeasible_without_claiming_impossibility(self) -> None:
        self.assertIsNone(threshold_for_target_risk(0.05, 0.10))

    def test_mean_confidence_coverage_bound(self) -> None:
        self.assertAlmostEqual(
            coverage_lower_bound_from_mean_confidence(0.80, 0.75),
            0.20,
        )
        self.assertEqual(
            coverage_lower_bound_from_mean_confidence(0.50, 0.75),
            0.0,
        )

    def test_conformal_singleton_bound_scales_by_coverage(self) -> None:
        self.assertAlmostEqual(
            conformal_singleton_risk_upper_bound(0.10, 0.50),
            0.20,
        )
        self.assertIsNone(conformal_singleton_risk_upper_bound(0.10, 0.0))

    def test_uniform_defect_is_not_an_average(self) -> None:
        defect = uniform_calibration_defect(
            [0.95, 0.70, 0.55],
            [0.90, 0.72, 0.40],
        )
        self.assertAlmostEqual(defect, 0.15)

    def test_finite_space_exact_summary_respects_theorem(self) -> None:
        summary = finite_space_selective_summary(
            weights=[0.25, 0.25, 0.25, 0.25],
            confidences=[0.95, 0.90, 0.72, 0.40],
            correctness_probabilities=[0.92, 0.86, 0.70, 0.43],
            threshold=0.90,
        )
        self.assertAlmostEqual(summary.coverage, 0.50)
        self.assertIsNotNone(summary.selective_risk)
        assert summary.selective_risk is not None
        self.assertLessEqual(summary.selective_risk, summary.theorem_bound + 1e-12)

    def test_adversarial_unknown_mass_can_make_false_known_one(self) -> None:
        rate = false_known_rate(
            accepted=[True, True, False],
            is_unknown=[True, True, False],
        )
        self.assertEqual(rate, 1.0)


if __name__ == "__main__":
    unittest.main()
