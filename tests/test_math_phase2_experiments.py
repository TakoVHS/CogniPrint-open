from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class MathPhase2ExperimentTests(unittest.TestCase):
    def test_human_paraphrase_generator_creates_seed_fixture_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            corpus_dir = root / "corpus"
            output_dir = root / "validation" / "human-paraphrase-v1"
            pairs_csv = output_dir / "pairs.csv"
            corpus_dir.mkdir()
            for index in range(4):
                (corpus_dir / f"sample-{index}.txt").write_text(
                    f"Corpus calibration text {index} with reproducible profile wording and bounded claims.",
                    encoding="utf-8",
                )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/generate_human_paraphrase_v1.py",
                    "--use-seed-fixtures",
                    "--pairs-csv",
                    str(pairs_csv),
                    "--corpus-dir",
                    str(corpus_dir),
                    "--output-dir",
                    str(output_dir),
                    "--random-pairs",
                    "12",
                    "--seed",
                    "5",
                ],
                check=True,
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                stdout=subprocess.PIPE,
            )

            self.assertIn("Human paraphrase v1 diagnostics written", result.stdout)
            summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["readiness_boundary"], "descriptive_only")
            self.assertFalse(summary["external_review_gate_satisfied"])
            self.assertEqual(summary["pair_count"], 12)
            self.assertIn("seed_fixture_synthetic_human_like", summary["pair_source_counts"])
            self.assertTrue((output_dir / "results.csv").exists())
            self.assertTrue((output_dir / "random-pair-distances.csv").exists())
            self.assertTrue((output_dir / "distribution.svg").exists())
            self.assertTrue((output_dir / "README.md").exists())

    def test_cross_genre_generator_creates_seed_fixture_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = root / "validation" / "cross-genre-v1"
            corpus_csv = output_dir / "corpus.csv"

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/generate_cross_genre_v1.py",
                    "--use-seed-fixtures",
                    "--corpus-csv",
                    str(corpus_csv),
                    "--output-dir",
                    str(output_dir),
                    "--permutations",
                    "25",
                    "--seed",
                    "5",
                ],
                check=True,
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                stdout=subprocess.PIPE,
            )

            self.assertIn("Cross-genre v1 diagnostics written", result.stdout)
            summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["readiness_boundary"], "descriptive_only")
            self.assertFalse(summary["external_review_gate_satisfied"])
            self.assertEqual(summary["text_count"], 12)
            self.assertEqual(summary["author_count"], 4)
            self.assertEqual(summary["genre_count"], 3)
            self.assertIn("seed_fixture_cross_genre", summary["corpus_source_counts"])
            self.assertTrue((output_dir / "results.csv").exists())
            self.assertTrue((output_dir / "genre-stability.svg").exists())
            self.assertTrue((output_dir / "README.md").exists())

    def test_cross_genre_generator_accepts_pan15_shaped_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = root / "validation" / "cross-genre-v1"
            corpus_csv = output_dir / "corpus.csv"
            output_dir.mkdir(parents=True)
            corpus_csv.write_text(
                "\n".join(
                    [
                        "text_id,author_id,genre,corpus_source,problem_id,language,pan_problem_type,truth_label,document_role,source_license,text",
                        "DU001-known01,pan15:DU001:known-author,known,pan15_author_verification,DU001,Dutch,cross_genre,Y,known,test-license,Known author sample with enough words for a stable profile.",
                        "DU001-unknown,pan15:DU001:known-author,questioned,pan15_author_verification,DU001,Dutch,cross_genre,Y,questioned,test-license,Questioned document from the same author with profile wording.",
                        "DU002-known01,pan15:DU002:known-author,known,pan15_author_verification,DU002,Dutch,cross_genre,N,known,test-license,Known control sample with compact mathematical wording.",
                        "DU002-unknown,pan15:DU002:questioned-author,questioned,pan15_author_verification,DU002,Dutch,cross_genre,N,questioned,test-license,Different author control document with another style.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/generate_cross_genre_v1.py",
                    "--corpus-csv",
                    str(corpus_csv),
                    "--output-dir",
                    str(output_dir),
                    "--max-pairs",
                    "10",
                    "--permutations",
                    "25",
                    "--seed",
                    "5",
                ],
                check=True,
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                stdout=subprocess.PIPE,
            )

            self.assertIn("Cross-genre v1 diagnostics written", result.stdout)
            summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["data_mode"], "real_public_pan15")
            self.assertEqual(summary["within_author_cross_genre_count"], 1)
            self.assertEqual(summary["inter_author_cross_genre_control_count"], 1)
            self.assertEqual(summary["readiness_boundary"], "descriptive_only")


if __name__ == "__main__":
    unittest.main()
