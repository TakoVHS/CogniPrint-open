from __future__ import annotations

import unittest

from cogniprint.provenance_conflict import (
    AttestationStatus,
    ConflictStatus,
    classify_conflict,
)


class ProvenanceConflictTests(unittest.TestCase):
    def test_agreement_remains_two_evidence_classes(self) -> None:
        result = classify_conflict(
            inferred_label="family-a",
            inference_allowed=True,
            attested_label="Family-A",
            attestation_status=AttestationStatus.VALIDATED,
        )
        self.assertEqual(result.status, ConflictStatus.CONSISTENT)
        self.assertIn("does not merge", result.note)

    def test_disagreement_is_reported_as_conflict(self) -> None:
        result = classify_conflict(
            inferred_label="family-a",
            inference_allowed=True,
            attested_label="family-b",
            attestation_status=AttestationStatus.VALIDATED,
        )
        self.assertEqual(result.status, ConflictStatus.PROVENANCE_CONFLICT)
        self.assertIn("must not silently choose", result.note)

    def test_unverified_attestation_does_not_override_statistical_evidence(self) -> None:
        result = classify_conflict(
            inferred_label="family-a",
            inference_allowed=True,
            attested_label="family-b",
            attestation_status=AttestationStatus.PRESENT_UNVERIFIED,
        )
        self.assertEqual(result.status, ConflictStatus.STATISTICAL_EVIDENCE_ONLY)

    def test_validated_attestation_can_exist_without_authorised_inference(self) -> None:
        result = classify_conflict(
            inferred_label="family-a",
            inference_allowed=False,
            attested_label="provider-model-x",
            attestation_status=AttestationStatus.VALIDATED,
        )
        self.assertEqual(result.status, ConflictStatus.ATTESTED_EVIDENCE_ONLY)

    def test_no_usable_sources_returns_insufficient_evidence(self) -> None:
        result = classify_conflict(
            inferred_label=None,
            inference_allowed=False,
            attested_label=None,
            attestation_status=AttestationStatus.ABSENT,
        )
        self.assertEqual(result.status, ConflictStatus.INSUFFICIENT_EVIDENCE)


if __name__ == "__main__":
    unittest.main()
