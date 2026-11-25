from __future__ import annotations

import unittest

from cogniprint.stats.claim_promotion import (
    blackwell_garbling_counterexample,
    camouflaged_mixture_selective_risk,
    claim_family_is_down_closed,
    equal_prior_binary_bayes_error,
    total_variation,
)


class ClaimPromotionTheoryTests(unittest.TestCase):
    def test_observational_equivalence_has_half_bayes_error(self) -> None:
        law = {"z1": 0.5, "z2": 0.5}
        tv = total_variation(law, law)
        self.assertEqual(tv, 0.0)
        self.assertEqual(equal_prior_binary_bayes_error(tv), 0.5)

    def test_camouflage_risk_formula(self) -> None:
        risk = camouflaged_mixture_selective_risk(
            unknown_fraction=0.30,
            known_selective_risk=0.02,
        )
        self.assertAlmostEqual(risk, 0.314)

    def test_camouflage_risk_approaches_one(self) -> None:
        risk = camouflaged_mixture_selective_risk(
            unknown_fraction=0.999,
            known_selective_risk=0.0,
        )
        self.assertAlmostEqual(risk, 0.999)

    def test_blackwell_counterexample_loses_all_binary_information(self) -> None:
        example = blackwell_garbling_counterexample()
        self.assertEqual(example.full_tv, 1.0)
        self.assertEqual(example.channel_tv, 0.0)
        self.assertEqual(example.full_bayes_error, 0.0)
        self.assertEqual(example.channel_bayes_error, 0.5)

    def test_claim_downset_requires_weaker_claims(self) -> None:
        edges = [
            ("KNOWN", "EXACT_GPT4"),
            ("AI", "ATTESTED_AI_PROVENANCE"),
        ]
        self.assertTrue(
            claim_family_is_down_closed(
                ["KNOWN", "EXACT_GPT4"],
                edges,
            )
        )
        self.assertFalse(
            claim_family_is_down_closed(
                ["EXACT_GPT4"],
                edges,
            )
        )


if __name__ == "__main__":
    unittest.main()
