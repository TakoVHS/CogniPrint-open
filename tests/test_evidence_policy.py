from __future__ import annotations

import unittest

from cogniprint.evidence_policy import (
    ClaimKind,
    ClaimLevel,
    EvidenceClass,
    EvidenceContext,
    LimitationCode,
    evaluate_claim,
)


class ClaimFirewallTests(unittest.TestCase):
    def test_descriptive_similarity_is_observed_not_attribution(self) -> None:
        decision = evaluate_claim(
            ClaimKind.SIMILARITY,
            EvidenceContext(
                strength=ClaimLevel.SIMILARITY_ONLY,
                minimum_evidence_met=True,
            ),
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.evidence_class, EvidenceClass.OBSERVED)
        self.assertIn("similarity is not source identity", decision.safe_statement)

    def test_model_family_is_blocked_while_descriptive_only(self) -> None:
        decision = evaluate_claim(
            ClaimKind.MODEL_FAMILY,
            EvidenceContext(
                strength=ClaimLevel.MODEL_FAMILY_CANDIDATE,
                minimum_evidence_met=True,
                in_distribution=True,
                calibrated=True,
                attribution_enabled=False,
            ),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.evidence_class, EvidenceClass.UNKNOWN)
        self.assertIn(LimitationCode.DESCRIPTIVE_ONLY, decision.limitations)

    def test_model_family_requires_minimum_evidence_distribution_and_calibration(self) -> None:
        decision = evaluate_claim(
            ClaimKind.MODEL_FAMILY,
            EvidenceContext(
                strength=ClaimLevel.MODEL_FAMILY_CANDIDATE,
                minimum_evidence_met=False,
                in_distribution=False,
                calibrated=False,
                attribution_enabled=True,
            ),
        )
        self.assertFalse(decision.allowed)
        self.assertIn(LimitationCode.INSUFFICIENT_EVIDENCE, decision.limitations)
        self.assertIn(LimitationCode.OUT_OF_DISTRIBUTION, decision.limitations)
        self.assertIn(LimitationCode.UNCALIBRATED_SCORE, decision.limitations)

    def test_model_family_can_be_inferred_only_after_explicit_gate(self) -> None:
        decision = evaluate_claim(
            ClaimKind.MODEL_FAMILY,
            EvidenceContext(
                strength=ClaimLevel.MODEL_FAMILY_CANDIDATE,
                minimum_evidence_met=True,
                in_distribution=True,
                calibrated=True,
                attribution_enabled=True,
            ),
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.evidence_class, EvidenceClass.INFERRED)

    def test_exact_model_is_not_inferred_from_content(self) -> None:
        decision = evaluate_claim(
            ClaimKind.EXACT_MODEL,
            EvidenceContext(
                strength=ClaimLevel.CALIBRATED_ATTRIBUTION_CANDIDATE,
                minimum_evidence_met=True,
                in_distribution=True,
                calibrated=True,
                attribution_enabled=True,
                validated_external_attestation=False,
            ),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.evidence_class, EvidenceClass.UNKNOWN)
        self.assertIn(LimitationCode.NO_EXTERNAL_PROVENANCE, decision.limitations)

    def test_exact_model_may_be_reported_only_as_validated_external_attestation(self) -> None:
        decision = evaluate_claim(
            ClaimKind.EXACT_MODEL,
            EvidenceContext(
                strength=ClaimLevel.ATTESTED_PROVENANCE,
                validated_external_attestation=True,
            ),
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.evidence_class, EvidenceClass.ATTESTED)
        self.assertIn("does not infer", decision.safe_statement)

    def test_high_stakes_identity_claims_are_denied_even_with_attestation(self) -> None:
        for kind in (
            ClaimKind.AUTHORSHIP,
            ClaimKind.ACTOR_OR_COMMISSIONER,
            ClaimKind.INTENT_OR_RESPONSIBILITY,
            ClaimKind.LEGAL_OR_FORENSIC_PROVENANCE,
        ):
            with self.subTest(kind=kind):
                decision = evaluate_claim(
                    kind,
                    EvidenceContext(
                        strength=ClaimLevel.ATTESTED_PROVENANCE,
                        minimum_evidence_met=True,
                        in_distribution=True,
                        calibrated=True,
                        attribution_enabled=True,
                        validated_external_attestation=True,
                    ),
                )
                self.assertFalse(decision.allowed)
                self.assertEqual(decision.evidence_class, EvidenceClass.UNKNOWN)
                self.assertIn(LimitationCode.UNSUPPORTED_CLAIM, decision.limitations)
                self.assertNotIn(LimitationCode.NO_EXTERNAL_PROVENANCE, decision.limitations)


if __name__ == "__main__":
    unittest.main()
