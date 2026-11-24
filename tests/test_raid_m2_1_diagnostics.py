from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cogniprint.benchmarks.raid_m2 import (
    DEFAULT_MACHINE_FAMILIES,
    M2RoleFractions,
    fit_probability_conformal,
)
from cogniprint.benchmarks.raid_m2_1 import (
    M2_1_COVERAGE_TARGETS,
    M2_1_TEMPERATURE_GRID,
    conformal_outcome_decomposition,
    evaluate_raid_m2_1,
    selective_risk_at_frozen_threshold,
    selective_risk_at_targets,
    summarize_score_scale,
    temperature_sensitivity_profile,
)
from cogniprint.fingerprint import CognitiveFingerprint

REPO_ROOT = Path(__file__).resolve().parents[1]
M2_1_SCRIPT = REPO_ROOT / "scripts" / "analyze_raid_m2_1_diagnostics.py"


def make_text(label: str, index: int) -> str:
    if label == "human":
        return (
            f"Personal note {index}. I walked home, noticed the weather, "
            "remembered a small detail, and wrote it down in my own words."
        )
    if label == "chatgpt":
        return (
            f"Example {index}. First define the question, then consider the "
            "main factors, and finally summarize the conclusion clearly."
        )
    if label == "gpt4":
        return (
            f"Technical example {index}: assumptions, constraints, evidence, "
            "and evaluation criteria should be separated before inference."
        )
    if label == "llama-chat":
        return (
            f"Sure, example {index}! We can compare the options step by step, "
            "note the trade-offs, and choose a concise practical explanation."
        )
    if label == "mistral-chat":
        return (
            f"Concise example {index}. Separate observation from interpretation, "
            "verify inputs, and avoid claims stronger than the evidence."
        )
    raise ValueError(label)


def make_records(per_class: int = 80) -> list[dict]:
    records: list[dict] = []
    labels = ("human", *DEFAULT_MACHINE_FAMILIES)
    for label in labels:
        for index in range(per_class):
            text = make_text(label, index)
            fingerprint = CognitiveFingerprint(text, language="en")
            records.append(
                {
                    "source_record_id": f"{label}-{index}",
                    "source_id": f"source-{label}-{index}",
                    "model_family": label,
                    "domain": "news",
                    "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "prompt_sha256": None,
                    "features_normalized": fingerprint.normalized_feature_dict(),
                    "_text": text,
                }
            )
    return records


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selection_manifest_sha256(records: list[dict]) -> str:
    selection = [
        {
            "source_record_id": record.get("source_record_id"),
            "source_id": record.get("source_id"),
            "model_family": record.get("model_family"),
            "domain": record.get("domain"),
            "text_sha256": record.get("text_sha256"),
            "prompt_sha256": record.get("prompt_sha256"),
            "lineage_id": record.get("lineage_id"),
        }
        for record in sorted(
            records,
            key=lambda item: str(item.get("source_record_id") or ""),
        )
    ]
    encoded = json.dumps(
        selection,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_cli_fixture(root: Path, per_class: int = 80) -> tuple[Path, Path, Path, str]:
    labels = ("human", *DEFAULT_MACHINE_FAMILIES)
    rows: list[dict[str, str]] = []
    features: list[dict] = []
    for label in labels:
        for index in range(per_class):
            text = make_text(label, index)
            prompt = "" if label == "human" else f"Explain diagnostic example {index}"
            source_id = f"source-{label}-{index}"
            row = {
                "id": f"{label}-{index}",
                "adv_source_id": f"adv-{label}-{index}",
                "source_id": source_id,
                "model": label,
                "decoding": "" if label == "human" else "sampling",
                "repetition_penalty": "" if label == "human" else "no",
                "attack": "none",
                "domain": "news",
                "prompt": prompt,
                "generation": text,
            }
            rows.append(row)
            fingerprint = CognitiveFingerprint(text, language="en")
            features.append(
                {
                    "source_record_id": row["id"],
                    "source_id": source_id,
                    "adv_source_id": row["adv_source_id"],
                    "model_family": label,
                    "domain": "news",
                    "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "prompt_sha256": (
                        hashlib.sha256(prompt.encode("utf-8")).hexdigest()
                        if prompt else None
                    ),
                    "lineage_id": f"source_id:{source_id}",
                    "character_count": len(text),
                    "token_count": len(fingerprint.words),
                    "features_normalized": fingerprint.normalized_feature_dict(),
                    "readiness_boundary": "descriptive_only",
                }
            )

    source = root / "source.csv"
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    feature_path = root / "features.jsonl"
    feature_path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in features),
        encoding="utf-8",
    )
    contract = root / "contract.json"
    contract.write_text(
        json.dumps(
            {
                "sha256": sha256_file(source),
                "byte_size": source.stat().st_size,
                "intended_use": "STAGE_A_DEVELOPMENT_ONLY",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return source, feature_path, contract, selection_manifest_sha256(features)


def run_m2_1_cli(
    source: Path,
    features: Path,
    contract: Path,
    selection_sha256: str,
    output_dir: Path,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        f"{REPO_ROOT / 'src'}{os.pathsep}{env.get('PYTHONPATH', '')}"
    ).rstrip(os.pathsep)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            str(M2_1_SCRIPT),
            "--features",
            str(features),
            "--input-file",
            str(source),
            "--expected-source-sha256",
            sha256_file(source),
            "--expected-features-sha256",
            sha256_file(features),
            "--expected-selection-manifest-sha256",
            selection_sha256,
            "--source-contract",
            str(contract),
            "--output-dir",
            str(output_dir),
            "--conformal-alpha",
            "0.20",
            "--char-dimensions",
            "512",
            "--word-dimensions",
            "256",
        ],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


class RaidM21DiagnosticsTests(unittest.TestCase):
    def test_selective_grid_uses_first_tie_safe_point_at_or_above_target(self) -> None:
        truth = ["a", "b", "a", "b"]
        predictions = ["a", "a", "a", "b"]
        confidences = [0.9, 0.9, 0.6, 0.2]
        rows = selective_risk_at_targets(
            truth,
            predictions,
            confidences,
            targets=[0.25, 0.50, 0.75, 1.00],
        )
        self.assertEqual(rows[0]["achieved_coverage"], 0.50)
        self.assertEqual(rows[0]["accepted"], 2)
        self.assertEqual(rows[1]["achieved_coverage"], 0.50)
        self.assertEqual(rows[2]["achieved_coverage"], 0.75)
        self.assertEqual(rows[3]["achieved_coverage"], 1.00)

    def test_frozen_threshold_risk_reports_accepted_errors_and_coverage(self) -> None:
        result = selective_risk_at_frozen_threshold(
            ["a", "b", "a", "b"],
            ["a", "a", "a", "b"],
            [0.95, 0.90, 0.70, 0.20],
            threshold=0.70,
        )
        self.assertEqual(result["accepted"], 3)
        self.assertEqual(result["errors"], 1)
        self.assertAlmostEqual(result["coverage"], 0.75)
        self.assertAlmostEqual(result["selective_risk"], 1 / 3)

    def test_conformal_decomposition_separates_empty_ambiguous_and_false_known(self) -> None:
        calibration_probabilities = (
            [[0.90, 0.10]] * 8
            + [[0.85, 0.15]] * 8
            + [[0.10, 0.90]] * 8
            + [[0.15, 0.85]] * 8
        )
        calibration_truth = ["a"] * 16 + ["b"] * 16
        model = fit_probability_conformal(
            calibration_probabilities,
            calibration_truth,
            ["a", "b"],
            alpha=0.20,
        )
        evaluation_probabilities = [
            [0.95, 0.05],
            [0.50, 0.50],
            [0.05, 0.95],
            [0.01, 0.99],
        ]
        truth = ["a", "a", "unknown", "unknown"]
        result = conformal_outcome_decomposition(
            model,
            evaluation_probabilities,
            truth,
        )
        self.assertEqual(result["known"]["total"], 2)
        self.assertEqual(result["unknown"]["total"], 2)
        self.assertAlmostEqual(
            result["unknown"]["empty_set_rate"]
            + result["unknown"]["ambiguous_set_rate"]
            + result["unknown"]["singleton_false_known_rate"],
            1.0,
        )

    def test_score_scale_and_temperature_profile_are_finite_and_frozen(self) -> None:
        scores = [
            [2.0, 0.0],
            [1.5, 0.2],
            [0.1, 1.8],
            [0.0, 2.1],
        ]
        truth = ["a", "a", "b", "b"]
        summary = summarize_score_scale(scores)
        self.assertEqual(summary["records"], 4)
        self.assertEqual(summary["classes"], 2)
        self.assertGreater(summary["margin_median"], 0.0)

        profile = temperature_sensitivity_profile(
            scores,
            truth,
            ["a", "b"],
        )
        self.assertEqual(
            [point["temperature"] for point in profile["grid"]],
            list(M2_1_TEMPERATURE_GRID),
        )
        self.assertIn(
            profile["best_grid_temperature"],
            M2_1_TEMPERATURE_GRID,
        )

    def test_cli_is_deterministic_and_does_not_persist_raw_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, contract, selection_sha = write_cli_fixture(root)
            output_dir = root / "out"
            completed = run_m2_1_cli(
                source,
                features,
                contract,
                selection_sha,
                output_dir,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=completed.stdout + completed.stderr,
            )
            result = json.loads(
                (output_dir / "m2-1-diagnostics.json").read_text()
            )
            reproducibility = json.loads(
                (output_dir / "m2-1-reproducibility.json").read_text()
            )
            self.assertEqual(result["status"], "POST_RESULT_EXPLORATORY")
            self.assertTrue(reproducibility["match"])
            self.assertFalse(result["raw_text_persisted"])
            self.assertFalse(result["raw_prompt_persisted"])

            serialized = "\n".join(
                path.read_text(encoding="utf-8")
                for path in output_dir.iterdir()
                if path.is_file()
            )
            self.assertNotIn('"_text"', serialized)
            self.assertNotIn('"generation"', serialized)
            self.assertNotIn('"prompt"', serialized)
            self.assertNotIn("Personal note", serialized)

    def test_full_m2_1_is_four_fold_exploratory_and_raw_text_free(self) -> None:
        result = evaluate_raid_m2_1(
            make_records(80),
            seed=20261124,
            fractions=M2RoleFractions(
                train=0.35,
                probability_calibration=0.15,
                conformal_calibration=0.30,
                threshold_development=0.10,
                evaluation=0.10,
            ),
            conformal_alpha=0.20,
            minimum_known_coverage=0.60,
            char_dimensions=512,
            word_dimensions=256,
        )
        self.assertEqual(result["status"], "POST_RESULT_EXPLORATORY")
        self.assertFalse(result["scientific_claim_evidence"])
        self.assertEqual(result["stage_b_status"], "NOT_AUTHORISED_TO_START")
        self.assertEqual(result["coverage_targets"], list(M2_1_COVERAGE_TARGETS))
        self.assertEqual(len(result["folds"]), 4)
        for fold in result["folds"]:
            self.assertEqual(fold["lineage_overlap_count"], 0)
            self.assertEqual(len(fold["representations"]), 3)
            for representation in fold["representations"].values():
                self.assertEqual(
                    len(representation["selective_risk_grid"]),
                    len(M2_1_COVERAGE_TARGETS),
                )
                self.assertIn(
                    "unknown",
                    representation["conformal_decomposition"],
                )
                self.assertIn(
                    "probability_calibration",
                    representation["score_scale"],
                )
                self.assertIn(
                    "grid",
                    representation["temperature_sensitivity"],
                )

        serialized = json.dumps(result, sort_keys=True)
        self.assertNotIn('"_text"', serialized)
        self.assertNotIn("Personal note", serialized)


if __name__ == "__main__":
    unittest.main()
