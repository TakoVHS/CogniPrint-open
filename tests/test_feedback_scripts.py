from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.synthesize_feedback import infer_category, infer_severity, synthesize_feedback

REPO_ROOT = Path(__file__).resolve().parents[1]


class FeedbackScriptsTests(unittest.TestCase):
    def test_infer_category_prefers_claims(self) -> None:
        self.assertEqual(infer_category("Category\nframing / claims\nThe wording is too strong."), "framing / claims")

    def test_infer_severity_finds_major(self) -> None:
        self.assertEqual(infer_severity("Severity\nmajor (should be fixed before the next release)"), "major")

    def test_synthesize_feedback_groups_issue(self) -> None:
        markdown = synthesize_feedback(
            [
                {
                    "number": 1,
                    "title": "Framing issue",
                    "body": "Category\nframing / claims\nSeverity\nmajor (should be fixed before the next release)\nDetails.",
                    "url": "https://example.test/1",
                    "state": "open",
                }
            ]
        )
        self.assertIn("## framing / claims (1)", markdown)
        self.assertIn("severity: `major`", markdown)


class BootstrapValidationScriptTests(unittest.TestCase):
    def test_script_emits_json_for_derived_tiers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "aggregate.csv"
            csv_path.write_text(
                "\n".join(
                    [
                        "study_id,study_name,variant_label,cosine_similarity,euclidean_distance,interpretation",
                        "s1,Study 1,edited.txt,0.999,0.2,low perturbation effect signal in this profile configuration",
                        "s2,Study 2,strongly-edited.txt,0.950,4.5,larger perturbation effect signal in this profile configuration",
                        "s3,Study 3,inline-1,0.998,0.4,moderate perturbation effect signal in this profile configuration",
                        "s4,Study 4,inline-2,0.940,5.0,larger perturbation effect signal in this profile configuration",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/bootstrap_validation.py",
                    "--csv",
                    str(csv_path),
                    "--json",
                    "--resamples",
                    "200",
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["group1"]["name"], "light")
            self.assertEqual(payload["group2"]["name"], "strong")
            self.assertIn("group1_minus_group2", payload["mean_difference"])


if __name__ == "__main__":
    unittest.main()
