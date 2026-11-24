from __future__ import annotations

import unittest

from cogniprint.stats.evidence_bounded import (
    certified_correctness_lower_bound,
    clopper_pearson_upper,
    conformal_singleton_risk_upper_bound,
    coverage_lower_bound_from_mean_confidence,
    false_known_rate,
    finite_space_selective_summary,
    fixed_threshold_risk_certificate,
    select_max_coverage_certified_threshold,
    selective_risk_upper_bound,
    simultaneous_threshold_certificates,
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


    def test_clopper_pearson_zero_error_closed_form(self) -> None:
        alpha = 0.05
        trials = 29
        expected = 1.0 - alpha ** (1.0 / trials)
        self.assertAlmostEqual(
            clopper_pearson_upper(0, trials, alpha),
            expected,
            places=12,
        )

    def test_clopper_pearson_edge_cases(self) -> None:
        self.assertIsNone(clopper_pearson_upper(0, 0, 0.05))
        self.assertEqual(clopper_pearson_upper(8, 8, 0.05), 1.0)

    def test_fixed_threshold_certificate_counts_accepted_errors(self) -> None:
        certificate = fixed_threshold_risk_certificate(
            confidences=[0.99, 0.94, 0.91, 0.70, 0.40],
            correct=[True, True, False, False, True],
            threshold=0.90,
            alpha=0.05,
        )
        self.assertEqual(certificate.accepted_count, 3)
        self.assertEqual(certificate.error_count, 1)
        self.assertAlmostEqual(certificate.empirical_risk or 0.0, 1.0 / 3.0)
        self.assertIsNotNone(certificate.upper_risk_bound)
        assert certificate.upper_risk_bound is not None
        self.assertGreaterEqual(certificate.upper_risk_bound, 1.0 / 3.0)

    def test_simultaneous_grid_uses_bonferroni_alpha(self) -> None:
        certificates = simultaneous_threshold_certificates(
            confidences=[0.99, 0.95, 0.91, 0.87, 0.72, 0.40],
            correct=[True, True, True, True, False, False],
            thresholds=[0.70, 0.85, 0.90],
            family_alpha=0.06,
        )
        self.assertEqual(len(certificates), 3)
        for certificate in certificates:
            self.assertAlmostEqual(certificate.per_threshold_alpha, 0.02)
            self.assertAlmostEqual(certificate.confidence_level, 0.98)

    def test_data_dependent_selection_from_simultaneous_grid(self) -> None:
        confidences = [0.99] * 30 + [0.90] * 20 + [0.70] * 20
        correct = [True] * 30 + [True] * 18 + [False] * 2 + [False] * 20
        certificates = simultaneous_threshold_certificates(
            confidences=confidences,
            correct=correct,
            thresholds=[0.99, 0.90, 0.70],
            family_alpha=0.05,
        )
        selected = select_max_coverage_certified_threshold(
            certificates,
            target_risk=0.20,
            min_accepted=20,
        )
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertIn(selected.threshold, {0.99, 0.90})
        self.assertLessEqual(selected.upper_risk_bound or 1.0, 0.20)


if __name__ == "__main__":
    unittest.main()
