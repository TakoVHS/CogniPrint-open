from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cogniprint.case_manifest import build_case_manifest, verify_case_manifest


class CaseManifestTests(unittest.TestCase):
    def test_manifest_is_deterministic_and_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "EVIDENCE").mkdir()
            (root / "RESULTS").mkdir()
            (root / "EVIDENCE" / "observations.json").write_text(
                json.dumps({"value": 1}), encoding="utf-8"
            )
            (root / "RESULTS" / "limitations.json").write_text(
                json.dumps(["DESCRIPTIVE_ONLY"]), encoding="utf-8"
            )

            left = build_case_manifest(root, case_id="case-001")
            right = build_case_manifest(root, case_id="case-001")

            self.assertEqual(left, right)
            result = verify_case_manifest(root, left)
            self.assertTrue(result["ok"])
            self.assertEqual(result["signature_status"], "UNSIGNED")

    def test_file_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "REPORT").mkdir()
            report = root / "REPORT" / "summary.txt"
            report.write_text("original", encoding="utf-8")
            manifest = build_case_manifest(root, case_id="case-002")

            report.write_text("changed", encoding="utf-8")
            result = verify_case_manifest(root, manifest)
            self.assertFalse(result["ok"])
            self.assertEqual(result["reason"], "file hash mismatch")

    def test_unexpected_file_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CASE.json").write_text("{}", encoding="utf-8")
            manifest = build_case_manifest(root, case_id="case-003")
            (root / "EXTRA.txt").write_text("unexpected", encoding="utf-8")

            result = verify_case_manifest(root, manifest)
            self.assertFalse(result["ok"])
            self.assertEqual(result["reason"], "case file set mismatch")

    def test_manifest_and_signatures_directory_are_excluded_from_payload_hash_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SIGNATURES").mkdir()
            (root / "SIGNATURES" / "placeholder.sig").write_text("not-a-real-signature", encoding="utf-8")
            (root / "MANIFEST.json").write_text("{}", encoding="utf-8")
            (root / "CASE.json").write_text("{}", encoding="utf-8")

            manifest = build_case_manifest(root, case_id="case-004")
            paths = [entry["path"] for entry in manifest["files"]]
            self.assertEqual(paths, ["CASE.json"])


if __name__ == "__main__":
    unittest.main()
