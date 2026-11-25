from __future__ import annotations

import unittest

from cogniprint.stats.finite_sample_composition import (
    ProductGateCounts,
    fixed_product_gate_certificate,
    known_membership_risk,
    simultaneous_product_gate_certificates,
    worst_case_known_membership_risk,
)


class FiniteSampleCompositionTests(unittest.TestCase):
    def test_posterior_unknown_risk_formula(self) -> None:
        self.assertAlmostEqual(
            known_membership_risk(0.5, 0.95, 0.05) or 0.0,
            0.05,
        )

    def test_worst_case_is_monotone_corner(self) -> None:
        bound = worst_case_known_membership_risk(
            pi_upper=0.5,
            known_accept_lower=0.90,
            unknown_accept_upper=0.10,
        )
        self.assertAlmostEqual(bound, 0.10)

    def test_fixed_gate_certificate_is_nontrivial_with_validation_data(self) -> None:
        certificate = fixed_product_gate_certificate(
            ProductGateCounts(
                name="fixed",
                known_accept_count=475,
                known_total=500,
                unknown_accept_count=25,
                unknown_total=500,
            ),
            pi_upper=0.5,
            alpha=0.05,
        )
        self.assertGreater(certificate.known_accept_lower, 0.90)
        self.assertLess(certificate.unknown_accept_upper, 0.10)
        self.assertLess(certificate.risk_upper, 0.10)
        self.assertAlmostEqual(certificate.family_confidence, 0.95)

    def test_no_unknown_validation_sample_is_vacuous(self) -> None:
        certificate = fixed_product_gate_certificate(
            ProductGateCounts(
                name="no-unknown-data",
                known_accept_count=95,
                known_total=100,
                unknown_accept_count=0,
                unknown_total=0,
            ),
            pi_upper=0.5,
        )
        self.assertEqual(certificate.unknown_accept_upper, 1.0)
        self.assertGreater(certificate.risk_upper, 0.5)

    def test_unrestricted_unknown_prevalence_blocks_known_claim(self) -> None:
        certificate = fixed_product_gate_certificate(
            ProductGateCounts(
                name="pi-one",
                known_accept_count=950,
                known_total=1000,
                unknown_accept_count=1,
                unknown_total=1000,
            ),
            pi_upper=1.0,
        )
        self.assertEqual(certificate.risk_upper, 1.0)

    def test_simultaneous_family_uses_two_bounds_per_gate(self) -> None:
        gates = [
            ProductGateCounts("g1", 95, 100, 5, 100),
            ProductGateCounts("g2", 90, 100, 2, 100),
        ]
        certificates = simultaneous_product_gate_certificates(
            gates,
            pi_upper=0.3,
            family_alpha=0.04,
        )
        self.assertEqual(len(certificates), 2)
        for certificate in certificates:
            self.assertAlmostEqual(certificate.per_bound_alpha, 0.01)
            self.assertAlmostEqual(certificate.family_confidence, 0.96)


if __name__ == "__main__":
    unittest.main()
