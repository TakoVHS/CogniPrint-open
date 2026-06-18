from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_inline_run_creates_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "workspace"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "run",
                    "--run-id",
                    "test-inline-run",
                    "--text",
                    "CogniPrint studies compact statistical profiles of text.",
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            self.assertIn("Run bundle written", result.stdout)
            run_dir = workspace / "runs" / "test-inline-run"
            self.assertTrue((run_dir / "manifest.json").exists())
            self.assertTrue((run_dir / "results.json").exists())
            self.assertTrue((run_dir / "summary.md").exists())
            self.assertTrue((run_dir / "export.csv").exists())

            results = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertGreater(results["profiles"][0]["metrics"]["word_count"], 0)
            self.assertIn("not legal conclusions", results["disclaimer"])
            self.assertEqual(manifest["input_mode"], "inline")
            self.assertIn("cli_args", manifest)
            self.assertIn("environment", manifest)

    def test_compare_creates_comparison_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            baseline = temp_path / "baseline.txt"
            variant = temp_path / "variant.txt"
            baseline.write_text("A short research note with stable wording.", encoding="utf-8")
            variant.write_text("A substantially revised research note with different structure and added detail.", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "compare",
                    "--run-id",
                    "test-compare-run",
                    "--baseline-file",
                    str(baseline),
                    "--variant-file",
                    str(variant),
                ],
                check=True,
            )
            run_dir = workspace / "runs" / "test-compare-run"
            comparisons = json.loads((run_dir / "comparisons.json").read_text(encoding="utf-8"))
            self.assertTrue(comparisons["comparisons"])
            self.assertIn("cosine_similarity", comparisons["comparisons"][0])

    def test_study_creates_aggregated_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            baseline = temp_path / "baseline.txt"
            variant = temp_path / "variant.txt"
            baseline.write_text("A baseline note for controlled perturbation analysis.", encoding="utf-8")
            variant.write_text("A revised baseline note for controlled perturbation analysis with added context.", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "study",
                    "--name",
                    "test perturbation study",
                    "--study-id",
                    "test-study",
                    "--baseline-file",
                    str(baseline),
                    "--variant-file",
                    str(variant),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            self.assertIn("Study bundle written", result.stdout)
            study_dir = workspace / "studies" / "test-study"
            self.assertTrue((study_dir / "study-manifest.json").exists())
            self.assertTrue((study_dir / "aggregated-results.json").exists())
            self.assertTrue((study_dir / "aggregated-results.csv").exists())
            self.assertTrue((study_dir / "study-summary.md").exists())
            self.assertTrue((study_dir / "manuscript-note.md").exists())

            aggregated = json.loads((study_dir / "aggregated-results.json").read_text(encoding="utf-8"))
            self.assertEqual(aggregated["variant_count"], 1)
            self.assertIn("perturbation effect", aggregated["comparison_rows"][0]["interpretation"])

    def test_profile_corpus_report_and_experiment_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            input_dir = workspace / "input"
            variants_dir = input_dir / "variants"
            variants_dir.mkdir(parents=True)
            original = input_dir / "original.txt"
            edited = input_dir / "edited.txt"
            variant = variants_dir / "strong.txt"
            original.write_text("A baseline research text for profile persistence.", encoding="utf-8")
            edited.write_text("A lightly edited research text for profile persistence checks.", encoding="utf-8")
            variant.write_text("A stronger variant changes length, punctuation, and local structure.", encoding="utf-8")

            profile_out = temp_path / "profile.json"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "profile",
                    "--file",
                    str(original),
                    "--output",
                    str(profile_out),
                    "--save",
                    "--label",
                    "original",
                ],
                check=True,
            )
            self.assertTrue(profile_out.exists())
            self.assertTrue(list((workspace / "profiles").glob("*.json")))

            corpus_out = temp_path / "corpus"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "corpus",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(corpus_out),
                    "--pattern",
                    "*.txt",
                ],
                check=True,
            )
            self.assertTrue((corpus_out / "corpus-manifest.json").exists())
            self.assertTrue((corpus_out / "original.profile.json").exists())

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "compare",
                    "--run-id",
                    "metric-compare",
                    "--baseline-file",
                    str(original),
                    "--variant-file",
                    str(edited),
                    "--metric",
                    "mahalanobis",
                ],
                check=True,
            )
            comparison = json.loads((workspace / "runs" / "metric-compare" / "comparisons.json").read_text(encoding="utf-8"))
            self.assertEqual(comparison["comparisons"][0]["selected_metric"]["metric"], "mahalanobis")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "study",
                    "--name",
                    "report study",
                    "--study-id",
                    "report-study",
                    "--baseline-file",
                    str(original),
                    "--variant-file",
                    str(edited),
                    "--variant-folder",
                    str(variants_dir),
                ],
                check=True,
            )
            study_dir = workspace / "studies" / "report-study"
            report_md = temp_path / "report.md"
            report_pdf = temp_path / "report.pdf"
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "report", "--study-dir", str(study_dir), "--format", "md", "--output", str(report_md)],
                check=True,
            )
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "report", "--study-dir", str(study_dir), "--format", "pdf", "--output", str(report_pdf)],
                check=True,
            )
            self.assertIn("CogniPrint Research Report", report_md.read_text(encoding="utf-8"))
            self.assertTrue(report_pdf.read_bytes().startswith(b"%PDF-"))

            config = temp_path / "experiment.yml"
            config.write_text(
                "\n".join(
                    [
                        "name: yaml experiment",
                        f"baseline_file: {original}",
                        "variant_files:",
                        f"  - {edited}",
                        f"variant_folder: {variants_dir}",
                        f"output_dir: {temp_path / 'experiments'}",
                    ]
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "experiment", "run", "--config", str(config)],
                check=True,
            )
            self.assertTrue((temp_path / "experiments" / "yaml-experiment" / "experiment-manifest.json").exists())

    def test_stability_test_command_writes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            variants_dir = temp_path / "variants"
            variants_dir.mkdir()
            baseline = temp_path / "baseline.txt"
            variant = variants_dir / "variant.txt"
            output = temp_path / "stability.json"
            baseline.write_text("CogniPrint studies bounded profile stability under controlled edits.", encoding="utf-8")
            variant.write_text("CogniPrint studies bounded profile stability with controlled edits.", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "stability-test",
                    "--baseline-file",
                    str(baseline),
                    "--perturbed-folder",
                    str(variants_dir),
                    "--output",
                    str(output),
                ],
                check=True,
            )

            summary = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["variant_count"], 1)
            self.assertEqual(summary["metric"], "cosine")
            self.assertEqual(summary["readiness_boundary"], "descriptive_only")
            self.assertIn("distances", summary)

    def test_perturb_notes_dataset_and_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            input_dir = workspace / "input"
            variants_dir = input_dir / "variants"
            variants_dir.mkdir(parents=True)
            original = input_dir / "original.txt"
            light = input_dir / "light.txt"
            strong = variants_dir / "strong.txt"
            sources = temp_path / "SOURCES.md"
            original.write_text("A baseline text for perturbation lab testing.", encoding="utf-8")
            light.write_text("A lightly edited baseline text for perturbation lab testing.", encoding="utf-8")
            strong.write_text("A strongly edited sample changes length, structure, and several metrics.", encoding="utf-8")
            sources.write_text(
                "\n".join(
                    [
                        "# Sources",
                        "",
                        "## source-id: test-self-authored",
                        "",
                        "- source_name: Test self-authored note",
                        "- source_ref: local/test",
                        "- source_class: self-authored",
                        "- license: self-authored local research use",
                        "- acquisition_date: 2026-04-22",
                        "- usage_note: Test fixture provenance.",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "perturb",
                    "--name",
                    "test perturbation lab",
                    "--perturbation-id",
                    "test-perturbation",
                    "--baseline-file",
                    str(original),
                    "--light-file",
                    str(light),
                    "--variant-folder",
                    str(variants_dir),
                ],
                check=True,
            )
            perturb_dir = workspace / "perturbations" / "test-perturbation"
            self.assertTrue((perturb_dir / "perturbation-manifest.json").exists())
            self.assertTrue((perturb_dir / "stability-summary.md").exists())
            self.assertTrue((perturb_dir / "perturbation-summary.csv").exists())
            study_dir = perturb_dir / "study"
            self.assertTrue((study_dir / "aggregated-results.json").exists())

            notes_dir = temp_path / "notes"
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "notes", "--study-dir", str(study_dir), "--output-dir", str(notes_dir)],
                check=True,
            )
            self.assertTrue((notes_dir / "empirical-note.md").exists())
            self.assertTrue((notes_dir / "methods-note.md").exists())
            self.assertTrue((notes_dir / "result-summary.md").exists())

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "dataset",
                    "--name",
                    "test dataset",
                    "--description",
                    "Local dataset scaffold for tests.",
                    "--baseline-file",
                    str(original),
                    "--variant-file",
                    str(light),
                    "--sources-file",
                    str(sources),
                ],
                check=True,
            )
            dataset_dir = workspace / "datasets" / "test-dataset"
            self.assertTrue((dataset_dir / "dataset-manifest.json").exists())
            self.assertTrue((dataset_dir / "metadata" / "samples.csv").exists())
            self.assertTrue((dataset_dir / "metadata" / "variants.csv").exists())
            self.assertTrue((dataset_dir / "metadata" / "SOURCES.md").exists())
            dataset_manifest = json.loads((dataset_dir / "dataset-manifest.json").read_text(encoding="utf-8"))
            self.assertIn("source_policy", dataset_manifest)
            samples_csv = (dataset_dir / "metadata" / "samples.csv").read_text(encoding="utf-8")
            variants_csv = (dataset_dir / "metadata" / "variants.csv").read_text(encoding="utf-8")
            self.assertIn("sha256", samples_csv)
            self.assertIn("baseline_sample_id", variants_csv)
            self.assertIn("controlled_variant", variants_csv)

            aggregate_md = temp_path / "aggregate.md"
            aggregate_csv = temp_path / "aggregate.csv"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "report",
                    "--study-dir",
                    str(workspace / "studies"),
                    "--aggregate",
                    "--output",
                    str(aggregate_md),
                    "--csv-output",
                    str(aggregate_csv),
                ],
                check=True,
            )
            self.assertIn("Aggregate Study Summary", aggregate_md.read_text(encoding="utf-8"))
            self.assertTrue(aggregate_csv.exists())

    def test_campaign_run_and_summarize(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace = temp_path / "workspace"
            input_dir = workspace / "input"
            variants_dir = input_dir / "variants"
            variants_dir.mkdir(parents=True)
            original = input_dir / "original.txt"
            light = input_dir / "light.txt"
            strong = variants_dir / "strong.txt"
            original.write_text("A baseline campaign text for empirical synthesis.", encoding="utf-8")
            light.write_text("A lightly edited campaign text for empirical synthesis.", encoding="utf-8")
            strong.write_text("A strongly edited campaign variant changes length and structure.", encoding="utf-8")
            config = temp_path / "campaign.yml"
            config.write_text(
                "\n".join(
                    [
                        "name: test campaign",
                        "campaign_id: test-campaign",
                        "description: Test campaign synthesis.",
                        "series:",
                        "  - name: series one",
                        f"    baseline_file: {original}",
                        f"    light_file: {light}",
                        f"    variant_folder: {variants_dir}",
                        "  - name: series two",
                        f"    baseline_file: {original}",
                        f"    light_file: {light}",
                    ]
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "campaign", "run", "--config", str(config)],
                check=True,
            )
            campaign_dir = workspace / "campaigns" / "test-campaign"
            self.assertTrue((campaign_dir / "manifest.json").exists())
            self.assertTrue((campaign_dir / "campaign-summary.md").exists())
            self.assertTrue((campaign_dir / "campaign-results.json").exists())
            self.assertTrue((campaign_dir / "campaign-results.csv").exists())
            self.assertTrue((campaign_dir / "manuscript-appendix.md").exists())
            self.assertTrue((campaign_dir / "latex" / "campaign-summary-table.tex").exists())
            self.assertTrue((campaign_dir / "reports" / "methods-section-draft.md").exists())

            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "campaign", "summarize", "--campaign-dir", str(campaign_dir)],
                check=True,
            )
            payload = json.loads((campaign_dir / "campaign-results.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(payload["comparison_count"], 2)

            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "campaign", "summarize-all"],
                check=True,
            )
            self.assertTrue((workspace / "reports" / "multi-campaign-summary.md").exists())
            self.assertTrue((workspace / "reports" / "multi-campaign-appendix.md").exists())
            self.assertTrue((workspace / "reports" / "multi-campaign-limitations.md").exists())
            self.assertTrue((workspace / "exports" / "multi-campaign-summary.csv").exists())
            self.assertTrue((workspace / "exports" / "multi-campaign-summary.json").exists())

            share_dir = workspace / "share" / "test-pack"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "campaign",
                    "share-pack",
                    "--campaign-dir",
                    str(campaign_dir),
                    "--output-dir",
                    str(share_dir),
                ],
                check=True,
            )
            self.assertTrue((share_dir / "README.md").exists())
            self.assertTrue((share_dir / "project-summary.md").exists())
            self.assertTrue((share_dir / "campaign-summary.md").exists())
            self.assertTrue((share_dir / "manuscript-appendix.md").exists())
            self.assertTrue((share_dir / "empirical-note.md").exists())
            self.assertTrue((share_dir / "latex-summary-table.tex").exists())
            self.assertTrue((share_dir / "interpretation-note.md").exists())

            paper2_dir = workspace / "reports" / "paper-2"
            subprocess.run(
                [sys.executable, "-m", "cogniprint", "--workspace", str(workspace), "campaign", "paper2", "--output-dir", str(paper2_dir)],
                check=True,
            )
            for filename in [
                "title-options.md",
                "abstract-notes.md",
                "introduction-notes.md",
                "methods-section-draft.md",
                "results-section-draft.md",
                "limitations-section-draft.md",
                "conclusion-notes.md",
                "appendix-draft.md",
                "candidate-tables.md",
                "candidate-figures.md",
            ]:
                self.assertTrue((paper2_dir / filename).exists())


if __name__ == "__main__":
    unittest.main()
