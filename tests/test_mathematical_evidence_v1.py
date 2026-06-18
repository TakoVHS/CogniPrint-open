from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class MathematicalEvidenceV1Tests(unittest.TestCase):
    def test_generator_creates_dependency_light_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            raw_dir = root / "raw"
            variant_dir = root / "variants"
            holdout_dir = root / "holdout"
            output_dir = root / "validation" / "mathematical-evidence-v1"
            raw_dir.mkdir()
            variant_dir.mkdir()
            holdout_dir.mkdir()

            samples = {
                "pbv11-sample-001": "CogniPrint measures compact statistical profiles for reproducible text research and bounded comparison.",
                "pbv11-sample-002": "A second baseline describes evidence packages, reviewer boundaries, and conservative interpretation.",
                "pbv11-sample-003": "This sample uses different vocabulary about entropy, vectors, and calibrated random-pair contrasts.",
                "pbv11-sample-004": "Another public text discusses validation limits, bootstrap intervals, and descriptive readiness.",
                "pbv11-sample-005": "The final baseline adds genre variation, punctuation, numbers 12 and 42, and scientific caution.",
            }
            for sample_id, text in samples.items():
                (raw_dir / f"{sample_id}-baseline.txt").write_text(text, encoding="utf-8")
                (variant_dir / f"{sample_id}-variant-a.txt").write_text(
                    text.replace("bounded", "documented").replace("profiles", "profile signals"),
                    encoding="utf-8",
                )
            for index in range(3):
                (holdout_dir / f"holdout-{index}.txt").write_text(
                    f"Independent holdout text {index} with separate wording for covariance diagnostics.",
                    encoding="utf-8",
                )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/generate_mathematical_evidence_v1.py",
                    "--raw-dir",
                    str(raw_dir),
                    "--variant-dir",
                    str(variant_dir),
                    "--holdout-dir",
                    str(holdout_dir),
                    "--output-dir",
                    str(output_dir),
                    "--lengths",
                    "5,10,20",
                    "--max-random-pairs",
                    "6",
                    "--seed",
                    "7",
                ],
                check=True,
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                stdout=subprocess.PIPE,
            )

            self.assertIn("Mathematical evidence v1 written", result.stdout)
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            pca = json.loads((output_dir / "pca-summary.json").read_text(encoding="utf-8"))
            lipschitz = json.loads((output_dir / "lipschitz-summary.json").read_text(encoding="utf-8"))
            baseline = json.loads((output_dir / "baseline-comparison-summary.json").read_text(encoding="utf-8"))

            self.assertEqual(manifest["readiness_boundary"], "descriptive_only")
            self.assertFalse(manifest["external_review_gate_satisfied"])
            self.assertEqual(manifest["variant_pair_count"], 5)
            self.assertEqual(pca["feature_count"], 12)
            self.assertIn("components_for_90pct", pca)
            self.assertEqual(lipschitz["pair_count"], 5)
            self.assertEqual(baseline["baseline_variant_count"], 5)
            self.assertTrue((output_dir / "pca-components.csv").exists())
            self.assertTrue((output_dir / "min-text-length-stability.csv").exists())
            self.assertTrue((output_dir / "feature-sensitivity.csv").exists())
            self.assertTrue((output_dir / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
