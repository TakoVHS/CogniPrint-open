from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from cogniprint.multi_principal_evidence import (
    structural_field_ablation,
    verify_multi_principal_bundle,
    with_bundle_integrity,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "challenge-schmidt-q1" / "fixtures" / "synthetic-3-principal-happy-path.json"


class SchmidtQ1PreawardTests(unittest.TestCase):
    def load_fixture(self) -> dict:
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_happy_path_verifies_and_reconstructs_delegation(self) -> None:
        result = verify_multi_principal_bundle(self.load_fixture())
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["principal_count"], 3)
        self.assertEqual(
            result["delegation_edges"],
            [["principal-a", "principal-b"], ["principal-b", "principal-c"]],
        )
        self.assertEqual(result["research_status"], "DEVELOPMENT_ONLY_PREAWARD")

    def test_mutated_event_fails_integrity(self) -> None:
        bundle = self.load_fixture()
        bundle["events"][1]["authorization_scope"] = ["research.admin"]
        bundle = with_bundle_integrity(bundle)
        result = verify_multi_principal_bundle(bundle)
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "event integrity mismatch")

    def test_unknown_parent_fails_closed(self) -> None:
        bundle = self.load_fixture()
        event = bundle["events"][4]
        event["parent_event_ids"] = ["missing-event"]
        # Preserve the old event hash deliberately: either event-integrity rejection
        # or later parent rejection is an acceptable fail-closed outcome.
        bundle = with_bundle_integrity(bundle)
        self.assertFalse(verify_multi_principal_bundle(bundle)["ok"])

    def test_two_principal_fixture_is_rejected(self) -> None:
        bundle = self.load_fixture()
        bundle["principals"] = bundle["principals"][:2]
        bundle = with_bundle_integrity(bundle)
        result = verify_multi_principal_bundle(bundle)
        self.assertFalse(result["ok"])
        self.assertIn("3 to 6 principals", result["reason"])

    def test_research_status_cannot_be_upgraded(self) -> None:
        bundle = self.load_fixture()
        bundle["research_status"] = "Q1_MILESTONE_COMPLETE"
        bundle = with_bundle_integrity(bundle)
        result = verify_multi_principal_bundle(bundle)
        self.assertFalse(result["ok"])
        self.assertIn("DEVELOPMENT_ONLY_PREAWARD", result["reason"])

    def test_required_field_structural_ablation_fails_closed(self) -> None:
        outcomes = structural_field_ablation(self.load_fixture())
        self.assertTrue(outcomes)
        self.assertTrue(all(outcomes.values()), outcomes)

    def test_bundle_hash_detects_top_level_mutation(self) -> None:
        bundle = self.load_fixture()
        mutated = deepcopy(bundle)
        mutated["case_id"] = "silently-changed-case-id"
        result = verify_multi_principal_bundle(mutated)
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "bundle integrity mismatch")


if __name__ == "__main__":
    unittest.main()
