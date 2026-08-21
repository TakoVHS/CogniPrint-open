from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_challenge_001_freeze_candidate as checker  # noqa: E402


class Challenge001FreezeCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(checker.DECISIONS.read_text(encoding="utf-8"))
        cls.canonical = checker.CANONICAL.read_text(encoding="utf-8")
        cls.candidate = checker.CANDIDATE.read_text(encoding="utf-8")

    def errors(self, data: dict) -> list[str]:
        return checker.validate_decisions(
            data,
            canonical_text=self.canonical,
            candidate_text=self.candidate,
        )

    def test_current_candidate_passes(self) -> None:
        self.assertEqual([], self.errors(copy.deepcopy(self.data)))

    def test_status_escalation_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["status"] = "FROZEN"
        data["scientific_state"]["research_freeze"] = "FROZEN"
        self.assertTrue(self.errors(data))

    def test_external_registration_claim_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["scientific_state"]["external_registration"] = "REGISTERED"
        data["custody_boundary"]["external_registration_submitted"] = True
        self.assertTrue(self.errors(data))

    def test_stage_b_artifact_creation_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["custody_boundary"]["stage_b_artifacts_created"] = True
        data["custody_boundary"]["sealed_labels_created"] = True
        self.assertTrue(self.errors(data))

    def test_sample_arithmetic_drift_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["sample_design"]["counts"]["clean_total"] = 1945
        self.assertTrue(self.errors(data))

    def test_unpinned_model_revision_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["source_registry_candidate"]["known_classes"][1]["revision"] = "main"
        self.assertTrue(self.errors(data))

    def test_conformal_alpha_drift_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["ood_unknown"]["alpha"] = 0.20
        self.assertTrue(self.errors(data))

    def test_minimum_evidence_drift_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["minimum_evidence"]["minimum_words"] = 64
        self.assertTrue(self.errors(data))

    def test_claim_rule_removal_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["stop_and_claim_narrowing"]["rules"].pop()
        self.assertTrue(self.errors(data))


if __name__ == "__main__":
    unittest.main()
