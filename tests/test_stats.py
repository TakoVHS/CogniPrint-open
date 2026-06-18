from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cogniprint.stats.bootstrap import bootstrap_mean_interval
from cogniprint.stats.effect_size import hedges_g


class StatsTests(unittest.TestCase):
    def test_bootstrap_mean_interval_returns_bounds(self) -> None:
        result = bootstrap_mean_interval([1.0, 2.0, 3.0, 4.0], resamples=500, seed=7)
        self.assertEqual(result["count"], 4)
        self.assertLessEqual(result["lower"], result["mean"])
        self.assertGreaterEqual(result["upper"], result["mean"])

    def test_hedges_g_returns_value_for_two_groups(self) -> None:
        result = hedges_g([1.0, 1.5, 2.0], [2.0, 2.5, 3.0])
        self.assertEqual(result["reference_count"], 3)
        self.assertEqual(result["comparison_count"], 3)
        self.assertIsNotNone(result["value"])

    def test_stats_validate_cli_creates_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "workspace"
            campaign_dir = workspace / "campaigns" / "demo-campaign"
            campaign_dir.mkdir(parents=True)
            benchmark_dir = root / "datasets" / "public-benchmark-v1" / "metadata"
            benchmark_dir.mkdir(parents=True)
            raw_dir = root / "raw"
            variant_dir = root / "variants"
            raw_dir.mkdir()
            variant_dir.mkdir()
            output_dir = root / "evidence" / "statistical-validation-v1"
            rows = [
                {
                    "series_name": "series-a",
                    "study_id": "study-a",
                    "variant_label": "edited.txt",
                    "cosine_similarity": 0.999,
                    "euclidean_distance": 0.2,
                    "manhattan_distance": 0.3,
                    "interpretation": "low perturbation effect signal in this profile configuration",
                },
                {
                    "series_name": "series-a",
                    "study_id": "study-a",
                    "variant_label": "01_punctuation_cleanup.txt",
                    "cosine_similarity": 0.995,
                    "euclidean_distance": 2.0,
                    "manhattan_distance": 2.4,
                    "interpretation": "moderate perturbation effect signal in this profile configuration",
                },
                {
                    "series_name": "series-a",
                    "study_id": "study-a",
                    "variant_label": "04_word_order_shift.txt",
                    "cosine_similarity": 0.990,
                    "euclidean_distance": 4.0,
                    "manhattan_distance": 4.8,
                    "interpretation": "larger perturbation effect signal in this profile configuration",
                },
            ]
            (campaign_dir / "campaign-results.json").write_text(
                json.dumps(
                    {
                        "campaign_id": "demo-campaign",
                        "name": "demo-campaign",
                        "series_count": 1,
                        "comparison_count": len(rows),
                        "rows": rows,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (raw_dir / "a.txt").write_text("A compact baseline text for benchmark validation.", encoding="utf-8")
            (variant_dir / "a1.txt").write_text("A compact benchmark variant with punctuation and wording shifts.", encoding="utf-8")
            (benchmark_dir / "samples.csv").write_text(
                "\n".join(
                    [
                        "sample_id,relation_type,baseline_sample_id,sample_title,file_path,source_candidate_id,license,source_url,acquisition_date,source_class,language,release_status,usage_note",
                        f"pbv1-sample-001-baseline,baseline,,Sample A,{raw_dir / 'a.txt'},pbv1-cand-001,public-domain,https://example.org/a,2026-04-29,public-domain literary text,en,released,test",
                        f"pbv1-sample-001-variant-a,punctuation_cleanup,pbv1-sample-001-baseline,Sample A punctuation,{variant_dir / 'a1.txt'},pbv1-cand-001,derived,https://example.org/a,2026-04-29,controlled public benchmark variant,en,released,test",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cogniprint",
                    "--workspace",
                    str(workspace),
                    "stats",
                    "validate",
                    "--campaign-root",
                    str(workspace / "campaigns"),
                    "--benchmark-samples",
                    str(benchmark_dir / "samples.csv"),
                    "--output-dir",
                    str(output_dir),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            self.assertIn("Statistical validation outputs written", result.stdout)
            self.assertTrue((output_dir / "manifest.json").exists())
            self.assertTrue((output_dir / "counts.json").exists())
            self.assertTrue((output_dir / "bootstrap-summary.json").exists())
            self.assertTrue((output_dir / "effect-size-summary.json").exists())
            self.assertTrue((output_dir / "axis-ablation-summary.csv").exists())
            self.assertTrue((output_dir / "random-baseline-summary.json").exists())
            self.assertTrue((output_dir / "random-baseline-summary.csv").exists())
            self.assertTrue((output_dir / "threshold-sensitivity.json").exists())
            self.assertTrue((output_dir / "threshold-sensitivity.csv").exists())
            self.assertTrue((output_dir / "benchmark-campaign-bridge.json").exists())
            self.assertTrue((output_dir / "benchmark-campaign-bridge-summary.md").exists())
            manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            counts = json.loads((output_dir / "counts.json").read_text(encoding="utf-8"))
            random_baseline = json.loads((output_dir / "random-baseline-summary.json").read_text(encoding="utf-8"))
            thresholds = json.loads((output_dir / "threshold-sensitivity.json").read_text(encoding="utf-8"))
            bridge = json.loads((output_dir / "benchmark-campaign-bridge.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "expanded descriptive statistical validation layer")
            self.assertEqual(manifest["snapshot_id"], "statistical-validation-v1.1")
            self.assertEqual(counts["empirical_campaign_count"], 1)
            self.assertEqual(counts["benchmark_baseline_count"], 1)
            self.assertEqual(counts["benchmark_axis_count"], 1)
            self.assertEqual(random_baseline["draw_count"], 0)
            self.assertIn("cosine_similarity", thresholds["metrics"])
            self.assertIn("euclidean_distance", thresholds["metrics"])
            self.assertIn("manhattan_distance", thresholds["metrics"])
            self.assertEqual(bridge["shared_axis_count"], 1)


if __name__ == "__main__":
    unittest.main()
