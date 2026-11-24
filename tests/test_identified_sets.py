from __future__ import annotations

import unittest

from cogniprint.stats.identified_sets import (
    RiskInterval,
    critical_unknown_fraction,
    identified_unknown_risk_interval,
    posterior_unknown_risk,
    product_channel_interval_is_refinement,
    robust_claim_admissible,
)


class IdentifiedSetTheoryTests(unittest.TestCase):
    def test_pure_camouflage_risk_equals_unknown_fraction(self) -> None:
        for pi in (0.0, 0.1, 0.5, 0.9, 1.0):
            risk = posterior_unknown_risk(pi, 0.6, 0.6)
            self.assertIsNotNone(risk)
            self.assertAlmostEqual(risk or 0.0, pi)

    def test_camouflage_identified_interval_equals_pi_interval(self) -> None:
        interval = identified_unknown_risk_interval(
            0.0,
            0.5,
            known_accept_rate=0.6,
            unknown_accept_rate=0.6,
        )
        self.assertEqual(interval, RiskInterval(0.0, 0.5))
        assert interval is not None
        self.assertFalse(robust_claim_admissible(interval, 0.1))

    def test_refining_channel_can_shrink_identified_interval(self) -> None:
        coarse = identified_unknown_risk_interval(
            0.0,
            0.5,
            known_accept_rate=0.5,
            unknown_accept_rate=0.5,
        )
        refined = identified_unknown_risk_interval(
            0.0,
            0.5,
            known_accept_rate=0.95,
            unknown_accept_rate=0.05,
        )
        assert coarse is not None
        assert refined is not None
        self.assertAlmostEqual(refined.upper, 0.05)
        self.assertTrue(product_channel_interval_is_refinement(coarse, refined))
        self.assertTrue(robust_claim_admissible(refined, 0.1))

    def test_critical_unknown_fraction_for_refining_channel(self) -> None:
        critical = critical_unknown_fraction(
            delta=0.1,
            known_accept_rate=0.95,
            unknown_accept_rate=0.05,
        )
        self.assertIsNotNone(critical)
        self.assertAlmostEqual(critical or 0.0, 0.6785714285714286)

    def test_redundant_channel_does_not_shrink_interval(self) -> None:
        coarse = RiskInterval(0.0, 0.5)
        redundant = RiskInterval(0.0, 0.5)
        self.assertTrue(product_channel_interval_is_refinement(coarse, redundant))
        self.assertEqual(coarse, redundant)


if __name__ == "__main__":
    unittest.main()
