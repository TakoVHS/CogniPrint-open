from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cogniprint.validation import (
    DeterministicRandomVectorBaseline,
    SimpleTfidfBaseline,
    permutation_test_against_random,
    run_validation_suite,
)


class ValidationDryRunTests(unittest.TestCase):
    def test_baselines_and_permutation_are_deterministic(self) -> None:
        corpus = [
            "A compact baseline text about reproducible evidence.",
            "A different public text about model evaluation.",
            "Another unrelated note about benchmark design.",
        ]
        tfidf = SimpleTfidfBaseline(corpus)
        random_baseline = DeterministicRandomVectorBaseline(seed=7)

        self.assertGreater(tfidf.similarity(corpus[0], corpus[0]), tfidf.similarity(corpus[0], corpus[1]))
        self.assertAlmostEqual(
            random_baseline.similarity(corpus[0], corpus[1]),
            random_baseline.similarity(corpus[0], corpus[1]),
        )
        self.assertLess(
            permutation_test_against_random(0.01, [0.2, 0.3, 0.4], alternative="less"),
            0.5,
        )

    def test_validation_suite_preserves_descriptive_boundary(self) -> None:
        report = run_validation_suite(
            corpus_texts=[
                "A public corpus text about reproducible research.",
                "A separate sample about statistical evaluation.",
                "A third text with different content and style.",
            ],
            original_text="CogniPrint studies stable statistical profiles.",
            variant_texts=["CogniPrint studies stable text profiles."],
            variant_labels=["variant.txt"],
            n_permutations=8,
            seed=3,
        )

        self.assertEqual(report["readiness_boundary"], "descriptive_only")
        self.assertFalse(report["external_review_gate_satisfied"])
        self.assertEqual(report["n_perturbation_pairs"], 1)
        self.assertEqual(report["n_random_pairs"], 8)
        self.assertEqual(report["variant_results"][0]["variant_label"], "variant.txt")

    def test_validate_cli_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            corpus_dir = root / "corpus"
            campaign_dir = root / "campaign"
            variants_dir = campaign_dir / "variants"
            corpus_dir.mkdir()
            variants_dir.mkdir(parents=True)
            for index in range(4):
                (corpus_dir / f"sample-{index}.txt").write_text(
                    f"Corpus sample {index} with distinct wording for random contrasts.",
                    encoding="utf-8",
                )
            (campaign_dir / "original.txt").write_text(
                "CogniPrint studies bounded profile stability under controlled edits.",
                encoding="utf-8",
            )
            (variants_dir / "variant-a.txt").write_text(
                "CogniPrint studies bounded profile stability with controlled edits.",
                encoding="utf-8",
            )
            output = root / "validation-report.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "validate",
                    "--corpus-dir",
                    str(corpus_dir),
                    "--campaign-dir",
                    str(campaign_dir),
                    "--n-permutations",
                    "8",
                    "--output",
                    str(output),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )

            self.assertIn("Validation dry-run report written", result.stdout)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["readiness_boundary"], "descriptive_only")
            self.assertEqual(report["corpus_file_count"], 4)
            self.assertEqual(report["n_random_pairs"], 8)
            self.assertTrue(output.with_name("validation-report-pvalues.csv").is_file())
            self.assertTrue(output.with_name("validation-report-summary.csv").is_file())


if __name__ == "__main__":
    unittest.main()
