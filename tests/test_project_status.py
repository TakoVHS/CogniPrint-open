from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_project_status.py"
spec = importlib.util.spec_from_file_location("status", SCRIPT)
assert spec and spec.loader
status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(status)


class StatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "docs/external-review").mkdir(parents=True)
        self.payload = {
            "schema": "cogniprint-project-status-v1",
            "status_date": "2026-08-05",
            "canonical": {
                "repository": "TakoVHS/CogniPrint-open",
                "status_basis_commit": "d" * 40,
                "release": "0.1.2",
                "scientific_readiness": "descriptive_only",
                "research_mode": "PROOF_MODE",
                "canonical_freeze": "PRE-FREEZE",
                "stage_b": "NOT_AUTHORISED_TO_START",
                "github_actions": "NOT_EXECUTED",
                "main_exact_snapshot": "NOT_EXECUTED",
                "external_methodological_reviews": {"valid": 0, "required": 1},
                "doi": {
                    "reference": "10.5281/zenodo.20756421",
                    "verification": "PENDING_DIRECT_PUBLIC_VERIFICATION",
                },
            },
            "development_evidence": [
                {
                    "pull_request": 54,
                    "head": "a" * 40,
                    "tree": "b" * 40,
                    "state": "DRAFT",
                    "canonical_capability_change": False,
                    "evidence": {},
                }
            ],
            "policy": {
                "branch_evidence_changes_main_status": False,
                "not_executed_is_failure": False,
                "product_progress_unlocks_scientific_claims": False,
            },
        }
        (self.root / "docs/evidence-project-status.json").write_text(
            json.dumps(self.payload), encoding="utf-8"
        )
        review = {
            "schema": "cogniprint-external-review-status-v1",
            "status_date": "2026-08-05",
            "valid_review_count": 0,
            "minimum_required_valid_reviews": 1,
            "independent_external_review_present": False,
            "qualifying_evidence": [],
        }
        (self.root / "docs/external-review/status.json").write_text(
            json.dumps(review), encoding="utf-8"
        )
        files = {
            "README.md": "descriptive_only v0.1.2 pending direct public Zenodo verification",
            "docs/current-state-summary.md": (
                "Scientific readiness: `descriptive_only`\n"
                "Research mode: `PROOF_MODE`\n"
                "Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`\n"
                "CI evidence status: `NOT_EXECUTED`\n"
                "Release line: `v0.1.2`\n"
                "DOI: pending direct public Zenodo verification"
            ),
            "docs/trust.md": (
                "Current scientific readiness: `descriptive_only`\n"
                "Research mode: `PROOF_MODE`\n"
                "Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`\n"
                "`NOT_EXECUTED`"
            ),
            "docs/external-review.md": (
                "Scientific readiness: `descriptive_only`\n"
                "External methodological reviews: `0/1`\n"
                "Release line: `v0.1.2`"
            ),
            "CITATION.cff": 'version: "0.1.2"\ndescriptive_only',
            "pyproject.toml": 'version = "0.1.2"',
            "RESEARCH_FREEZE_001.md": "PRE-FREEZE\nNOT AUTHORISED TO START",
        }
        for name, content in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid(self) -> None:
        payload = status.load(self.root / status.STATUS)
        status.validate(payload)
        self.assertEqual(status.document_errors(self.root, payload), [])

    def test_scientific_escalation_rejected(self) -> None:
        payload = json.loads(json.dumps(self.payload))
        payload["canonical"]["scientific_readiness"] = "validated"
        with self.assertRaisesRegex(status.StatusError, "escalation"):
            status.validate(payload)

    def test_branch_cannot_change_main(self) -> None:
        payload = json.loads(json.dumps(self.payload))
        payload["development_evidence"][0]["canonical_capability_change"] = True
        with self.assertRaisesRegex(status.StatusError, "non-canonical"):
            status.validate(payload)

    def test_review_drift_detected(self) -> None:
        path = self.root / status.REVIEW
        value = json.loads(path.read_text(encoding="utf-8"))
        value["valid_review_count"] = 1
        path.write_text(json.dumps(value), encoding="utf-8")
        self.assertIn(
            "external review status does not match project status",
            status.document_errors(self.root, self.payload),
        )

    def test_doi_wording_drift_detected(self) -> None:
        (self.root / "README.md").write_text("descriptive_only v0.1.2", encoding="utf-8")
        self.assertTrue(
            any("Zenodo" in item for item in status.document_errors(self.root, self.payload))
        )

    def test_status_basis_sha_is_required(self) -> None:
        payload = json.loads(json.dumps(self.payload))
        payload["canonical"]["status_basis_commit"] = "main"
        with self.assertRaisesRegex(status.StatusError, "status basis"):
            status.validate(payload)


if __name__ == "__main__":
    unittest.main()
