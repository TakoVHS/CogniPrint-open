from __future__ import annotations

import unittest

from cogniprint.stats.certificate_scope import (
    FiniteCertificate,
    FiniteClaim,
    certificate_compatible_worlds,
    compose_same_target,
    composed_confidence_budget,
    direct_static_compatible,
    find_heterogeneous_composition_witness,
    find_nonpromotion_witness,
    heterogeneous_compatible_worlds,
    runtime_direct_promotion_allowed,
    sharp_finite_claim_bound_under_certificates,
    worst_claim_risk_under_certificate,
)


class CertificateScopeJudgmentTests(unittest.TestCase):
    def test_direct_compatible_promotion(self) -> None:
        risks = {"safe": 0.03, "edge": 0.08}
        certificate = FiniteCertificate(
            name="class-risk",
            target="known-family-error",
            scope=frozenset(risks),
            risk_by_world=risks,
            bound=0.09,
            alpha=0.05,
        )
        claim = FiniteClaim(
            name="same-target-claim",
            target="known-family-error",
            scope=frozenset(risks),
            risk_by_world=risks,
            delta=0.10,
        )
        self.assertTrue(direct_static_compatible(certificate, claim))
        self.assertTrue(runtime_direct_promotion_allowed(certificate, claim))
        self.assertIsNone(find_nonpromotion_witness(certificate, claim))

    def test_target_mismatch_produces_counterworld(self) -> None:
        certificate = FiniteCertificate(
            name="closed-set",
            target="known-family-error",
            scope=frozenset({"d0", "dpi"}),
            risk_by_world={"d0": 0.05, "dpi": 0.05},
            bound=0.08,
            alpha=0.05,
        )
        claim = FiniteClaim(
            name="known-membership",
            target="unknown-contamination",
            scope=frozenset({"d0", "dpi"}),
            risk_by_world={"d0": 0.00, "dpi": 0.35},
            delta=0.10,
        )
        self.assertFalse(direct_static_compatible(certificate, claim))
        self.assertEqual(find_nonpromotion_witness(certificate, claim), "dpi")
        worst = worst_claim_risk_under_certificate(certificate, claim)
        self.assertIsNotNone(worst)
        assert worst is not None
        self.assertAlmostEqual(worst, 0.35)


    def test_single_certificate_scope_gap_fails_closed(self) -> None:
        certificate = FiniteCertificate(
            "partial-single",
            "source-risk",
            frozenset({"covered"}),
            {"covered": 0.02},
            0.05,
            0.02,
        )
        claim = FiniteClaim(
            "deployment",
            "claim-risk",
            frozenset({"covered", "uncovered"}),
            {"covered": 0.00, "uncovered": 0.90},
            0.10,
        )

        for operation in (
            lambda: certificate_compatible_worlds(certificate, claim),
            lambda: find_nonpromotion_witness(certificate, claim),
            lambda: worst_claim_risk_under_certificate(certificate, claim),
        ):
            with self.assertRaisesRegex(ValueError, "does not cover claim worlds"):
                operation()

    def test_single_certificate_and_heterogeneous_paths_agree_when_covered(self) -> None:
        certificate = FiniteCertificate(
            "covered",
            "source-risk",
            frozenset({"w1", "w2"}),
            {"w1": 0.02, "w2": 0.03},
            0.05,
            0.02,
        )
        claim = FiniteClaim(
            "deployment",
            "claim-risk",
            frozenset({"w1", "w2"}),
            {"w1": 0.04, "w2": 0.40},
            0.10,
        )

        self.assertEqual(
            certificate_compatible_worlds(certificate, claim),
            heterogeneous_compatible_worlds((certificate,), claim),
        )
        single_worst = worst_claim_risk_under_certificate(certificate, claim)
        heterogeneous_worst = sharp_finite_claim_bound_under_certificates(
            (certificate,), claim
        )
        self.assertEqual(single_worst, heterogeneous_worst)

    def test_same_target_composition_uses_min_bound_and_alpha_sum(self) -> None:
        risks = {"w": 0.07}
        first = FiniteCertificate(
            "a", "risk", frozenset({"w"}), risks, 0.10, 0.02
        )
        second = FiniteCertificate(
            "b", "risk", frozenset({"w"}), risks, 0.08, 0.03
        )
        composed = compose_same_target(first, second)
        self.assertEqual(composed.bound, 0.08)
        self.assertAlmostEqual(composed.alpha, 0.05)

    def test_same_target_composition_need_not_strictly_improve(self) -> None:
        risks = {"w": 0.04}
        first = FiniteCertificate(
            "a", "risk", frozenset({"w"}), risks, 0.08, 0.025
        )
        second = FiniteCertificate(
            "b", "risk", frozenset({"w"}), risks, 0.08, 0.025
        )
        composed = compose_same_target(first, second)
        self.assertEqual(composed.bound, 0.08)

    def test_heterogeneous_composition_still_requires_warrant(self) -> None:
        first = FiniteCertificate(
            "family", "family-risk", frozenset({"w1", "w2"}),
            {"w1": 0.02, "w2": 0.02}, 0.05, 0.02
        )
        second = FiniteCertificate(
            "ood", "ood-score-risk", frozenset({"w1", "w2"}),
            {"w1": 0.03, "w2": 0.03}, 0.05, 0.03
        )
        claim = FiniteClaim(
            "provenance", "provenance-risk", frozenset({"w1", "w2"}),
            {"w1": 0.04, "w2": 0.40}, 0.10
        )
        self.assertEqual(
            find_heterogeneous_composition_witness((first, second), claim),
            "w2",
        )
        self.assertAlmostEqual(
            composed_confidence_budget((first, second)),
            0.05,
        )


    def test_heterogeneous_scope_gap_fails_closed(self) -> None:
        certificate = FiniteCertificate(
            "partial",
            "source-risk",
            frozenset({"covered"}),
            {"covered": 0.02},
            0.05,
            0.02,
        )
        claim = FiniteClaim(
            "deployment",
            "claim-risk",
            frozenset({"covered", "uncovered"}),
            {"covered": 0.04, "uncovered": 0.90},
            0.10,
        )
        with self.assertRaisesRegex(ValueError, "does not cover claim worlds"):
            heterogeneous_compatible_worlds((certificate,), claim)
        with self.assertRaisesRegex(ValueError, "does not cover claim worlds"):
            find_heterogeneous_composition_witness((certificate,), claim)
        with self.assertRaisesRegex(ValueError, "does not cover claim worlds"):
            sharp_finite_claim_bound_under_certificates((certificate,), claim)

    def test_sharp_finite_quantitative_warrant_bound(self) -> None:
        first = FiniteCertificate(
            "family",
            "family-risk",
            frozenset({"w1", "w2", "w3"}),
            {"w1": 0.02, "w2": 0.02, "w3": 0.30},
            0.05,
            0.02,
        )
        second = FiniteCertificate(
            "ood",
            "ood-risk",
            frozenset({"w1", "w2", "w3"}),
            {"w1": 0.03, "w2": 0.03, "w3": 0.01},
            0.05,
            0.03,
        )
        claim = FiniteClaim(
            "provenance",
            "provenance-risk",
            frozenset({"w1", "w2", "w3"}),
            {"w1": 0.04, "w2": 0.09, "w3": 0.80},
            0.10,
        )
        sharp = sharp_finite_claim_bound_under_certificates((first, second), claim)
        self.assertIsNotNone(sharp)
        assert sharp is not None
        self.assertAlmostEqual(sharp, 0.09)
        self.assertIsNone(
            find_heterogeneous_composition_witness((first, second), claim)
        )

    def test_empty_compatible_set_is_unresolved_not_zero_bound(self) -> None:
        certificate = FiniteCertificate(
            "impossible-realized-bound",
            "risk",
            frozenset({"w"}),
            {"w": 0.20},
            0.10,
            0.05,
        )
        claim = FiniteClaim(
            "claim",
            "claim-risk",
            frozenset({"w"}),
            {"w": 0.01},
            0.10,
        )
        self.assertIsNone(
            sharp_finite_claim_bound_under_certificates((certificate,), claim)
        )


if __name__ == "__main__":
    unittest.main()
