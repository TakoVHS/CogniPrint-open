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

from cogniprint.benchmarks.evaluation import grouped_split, lineage_group
from cogniprint.benchmarks.ngram import (
    char_config,
    evaluate_hashed_ngram,
    fit_idf,
    hashed_counts,
    normalize_text,
    predict_cosine_nearest_centroid,
    transform_tfidf,
    word_config,
    word_tokens,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "analyze_raid_ngrams.py"
SEED = 20260725
TEST_FRACTION = 0.30


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for label, prompt_prefix, text_prefix in (
        ("human", "", "Human essay"),
        ("gpt4", "prompt", "Generated technical summary"),
    ):
        for index in range(40):
            text = (
                f"{text_prefix} {index}. Structured benchmark sentence with "
                f"deterministic lexical cues for {label}."
            )
            rows.append(
                {
                    "id": f"{label}-{index}",
                    "adv_source_id": f"adv-{label}-{index}",
                    "source_id": f"source-{label}-{index}",
                    "model": label,
                    "decoding": "" if label == "human" else "sampling",
                    "repetition_penalty": "" if label == "human" else "no",
                    "attack": "none",
                    "domain": "news",
                    "prompt": "" if label == "human" else f"{prompt_prefix} {index}",
                    "generation": text,
                }
            )
    return rows


def write_source(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def selected_records_from_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for row in rows:
        prompt_hash = sha256_text(row["prompt"]) if row["prompt"] else None
        records.append(
            {
                "source_record_id": row["id"],
                "source_id": row["source_id"],
                "adv_source_id": row["adv_source_id"],
                "model_family": row["model"],
                "domain": row["domain"],
                "text_sha256": sha256_text(row["generation"]),
                "prompt_sha256": prompt_hash,
                "lineage_id": f"source_id:{row['source_id']}",
                "readiness_boundary": "descriptive_only",
            }
        )
    return records


def write_features(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def empty_metrics(labels: list[str]) -> dict[str, object]:
    confusion = {actual: {predicted: 0 for predicted in labels} for actual in labels}
    return {
        "accuracy": 0.0,
        "balanced_accuracy": 0.0,
        "macro_f1": 0.0,
        "per_class": {
            label: {
                "support": 0,
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
            }
            for label in labels
        },
        "confusion_matrix": confusion,
    }


def write_prior(path: Path, records: list[dict[str, object]]) -> dict[str, object]:
    train, test = grouped_split(records, seed=SEED, test_fraction=TEST_FRACTION)
    labels = sorted({str(record["model_family"]) for record in records})
    metric = empty_metrics(labels)
    payload = {
        "seed": SEED,
        "test_fraction": TEST_FRACTION,
        "train_records": len(train),
        "test_records": len(test),
        "train_groups": len({lineage_group(record) for record in train}),
        "test_groups": len({lineage_group(record) for record in test}),
        "chance_accuracy_reference": 0.5,
        "majority": metric,
        "length_only_nearest_centroid": metric,
        "cogniprint_12d_nearest_centroid": metric,
    }
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def write_contract(
    path: Path,
    source: Path,
    *,
    sha256_override: str | None = None,
    byte_size_override: int | None = None,
) -> None:
    payload = {
        "sha256": sha256_override or sha256_file(source),
        "byte_size": byte_size_override if byte_size_override is not None else source.stat().st_size,
        "intended_use": "STAGE_A_DEVELOPMENT_ONLY",
    }
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def setup_fixture(
    root: Path,
) -> tuple[Path, Path, Path, Path, list[dict[str, str]], list[dict[str, object]], dict[str, object]]:
    rows = source_rows()
    source = root / "source.csv"
    write_source(source, rows)
    records = selected_records_from_rows(rows)
    features = root / "features.jsonl"
    write_features(features, records)
    prior = root / "prior.json"
    prior_payload = write_prior(prior, records)
    contract = root / "contract.json"
    write_contract(contract, source)
    return source, features, prior, contract, rows, records, prior_payload


def run_script(
    source: Path,
    features: Path,
    prior: Path,
    contract: Path,
    out: Path,
    *,
    expected_sha: str | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{REPO_ROOT / 'src'}{os.pathsep}{env.get('PYTHONPATH', '')}".rstrip(os.pathsep)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--features",
            str(features),
            "--baseline-metrics",
            str(prior),
            "--input-file",
            str(source),
            "--expected-source-sha256",
            expected_sha or sha256_file(source),
            "--source-contract",
            str(contract),
            "--output-dir",
            str(out),
            "--char-dimensions",
            "1024",
            "--word-dimensions",
            "512",
        ],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


class RaidNgramBaselineTests(unittest.TestCase):
    def test_normalization_and_word_tokens_are_deterministic(self) -> None:
        self.assertEqual(normalize_text("  HéLLo\tWORLD  "), "héllo world")
        self.assertEqual(word_tokens("Don't stop, 42 times."), ["don't", "stop", "42", "times"])

    def test_hashed_counts_are_deterministic_and_nonnegative(self) -> None:
        config = char_config(128)
        first = hashed_counts("A deterministic sentence.", config)
        second = hashed_counts("A deterministic sentence.", config)
        self.assertEqual(first, second)
        self.assertTrue(first)
        self.assertTrue(all(index >= 0 and count > 0 for index, count in first.items()))

    def test_train_only_idf_and_unseen_bucket_handling(self) -> None:
        config = word_config(128)
        train_counts = [hashed_counts("alpha alpha beta", config), hashed_counts("alpha gamma", config)]
        idf, unseen_idf, occupied = fit_idf(train_counts)
        self.assertGreater(occupied, 0)
        unseen_counts = hashed_counts("delta", config)
        unseen_vector = transform_tfidf(unseen_counts, idf, unseen_idf)
        self.assertTrue(unseen_vector)
        self.assertTrue(all(value > 0 for value in unseen_vector.values()))
        self.assertGreater(unseen_idf, 1.0)

    def test_cosine_tie_break_is_lexicographic(self) -> None:
        predictions = predict_cosine_nearest_centroid({"alpha": {}, "beta": {}}, [{}])
        self.assertEqual(predictions, ["alpha"])

    def test_toy_ngram_baselines_execute(self) -> None:
        records: list[dict[str, object]] = []
        for label, prefix in (("human", "personal memory story"), ("gpt4", "systematic technical synthesis")):
            for index in range(30):
                records.append(
                    {
                        "model_family": label,
                        "source_id": f"{label}-{index}",
                        "text_sha256": sha256_text(f"{label}-{index}"),
                        "_text": f"{prefix} example {index} {prefix}",
                    }
                )
        train, test = grouped_split(records, seed=SEED, test_fraction=TEST_FRACTION)
        char_result = evaluate_hashed_ngram(train, test, char_config(1024))
        word_result = evaluate_hashed_ngram(train, test, word_config(512))
        self.assertGreaterEqual(char_result["metrics"]["accuracy"], 0.8)
        self.assertGreaterEqual(word_result["metrics"]["accuracy"], 0.8)
        self.assertGreater(char_result["occupied_training_hash_bins"], 0)
        self.assertGreater(word_result["occupied_training_hash_bins"], 0)
        self.assertFalse(char_result["persisted_vocabulary"])
        self.assertFalse(word_result["raw_text_persisted"])

    def test_script_rehydrates_exact_selection_and_persists_no_raw_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, rows, records, prior_payload = setup_fixture(root)
            out = root / "out"
            result = run_script(source, features, prior, contract, out)
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            metrics = json.loads((out / "ngram-baseline-metrics.json").read_text())
            audit = json.loads((out / "ngram-source-rehydration-audit.json").read_text())
            reproducibility = json.loads((out / "ngram-reproducibility-check.json").read_text())
            self.assertEqual(audit["rehydrated_records"], len(rows))
            self.assertEqual(audit["selected_records"], len(rows))
            self.assertEqual(audit["unique_source_record_ids"], len(rows))
            self.assertEqual(audit["unique_text_hashes"], len(rows))
            self.assertTrue(audit["all_text_hashes_verified"])
            self.assertTrue(audit["all_prompt_hashes_verified"])
            self.assertTrue(audit["all_model_families_verified"])
            self.assertTrue(audit["all_domains_verified"])
            self.assertTrue(audit["all_source_ids_verified"])
            self.assertEqual(metrics["train_records"], prior_payload["train_records"])
            self.assertEqual(metrics["test_records"], prior_payload["test_records"])
            self.assertEqual(metrics["train_groups"], prior_payload["train_groups"])
            self.assertEqual(metrics["test_groups"], prior_payload["test_groups"])
            self.assertEqual(metrics["lineage_overlap_count"], 0)
            self.assertEqual(reproducibility["run_1_metrics_sha256"], reproducibility["run_2_metrics_sha256"])
            self.assertEqual(reproducibility["run_1_rehydration_audit_sha256"], reproducibility["run_2_rehydration_audit_sha256"])
            serialized = json.dumps([metrics, audit, reproducibility], sort_keys=True)
            for forbidden in ('"generation"', '"prompt"', '"raw_text"', '"raw_prompt"', '"_text"', '"vocabulary"', '"tokens"'):
                self.assertNotIn(forbidden, serialized)

    def test_repeated_runs_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, *_ = setup_fixture(root)
            out1 = root / "out-1"
            out2 = root / "out-2"
            first = run_script(source, features, prior, contract, out1)
            second = run_script(source, features, prior, contract, out2)
            self.assertEqual(first.returncode, 0, msg=first.stderr + first.stdout)
            self.assertEqual(second.returncode, 0, msg=second.stderr + second.stdout)
            for filename in (
                "ngram-baseline-metrics.json",
                "ngram-source-rehydration-audit.json",
                "ngram-reproducibility-check.json",
            ):
                self.assertEqual(sha256_file(out1 / filename), sha256_file(out2 / filename))

    def test_source_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, *_ = setup_fixture(root)
            result = run_script(source, features, prior, contract, root / "out", expected_sha="0" * 64)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source SHA-256 mismatch", result.stderr + result.stdout)

    def test_source_contract_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, *_ = setup_fixture(root)
            write_contract(contract, source, byte_size_override=1)
            result = run_script(source, features, prior, contract, root / "out")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source contract byte_size does not match the local source", result.stderr + result.stdout)

    def test_selected_text_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            records[0]["text_sha256"] = "0" * 64
            write_features(features, records)
            result = run_script(source, features, prior, contract, root / "out")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("text SHA-256 mismatch", result.stderr + result.stdout)

    def test_prompt_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            for record in records:
                if record["prompt_sha256"] is not None:
                    record["prompt_sha256"] = "f" * 64
                    break
            write_features(features, records)
            result = run_script(source, features, prior, contract, root / "out")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("prompt SHA-256 mismatch", result.stderr + result.stdout)

    def test_duplicate_selected_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            records.append(dict(records[0]))
            write_features(features, records)
            result = run_script(source, features, prior, contract, root / "out")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate source_record_id", result.stderr + result.stdout)

    def test_missing_selected_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            write_source(source, [row for row in rows if row["id"] != "gpt4-0"])
            write_contract(contract, source)
            result = run_script(source, features, prior, contract, root / "out")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("failed to rehydrate", result.stderr + result.stdout)

    def test_model_domain_and_source_id_mismatch_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            records[0]["model_family"] = "human" if records[0]["model_family"] == "gpt4" else "gpt4"
            write_features(features, records)
            result = run_script(source, features, prior, contract, root / "out")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("model mismatch", result.stderr + result.stdout)

            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            records[0]["domain"] = "wiki"
            write_features(features, records)
            result = run_script(source, features, prior, contract, root / "out-domain")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("domain mismatch", result.stderr + result.stdout)

            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            records[0]["source_id"] = "wrong-source-id"
            write_features(features, records)
            result = run_script(source, features, prior, contract, root / "out-source")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source_id mismatch", result.stderr + result.stdout)

    def test_forbidden_persisted_fields_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source, features, prior, contract, rows, records, _ = setup_fixture(root)
            records[0]["generation"] = "forbidden"
            write_features(features, records)
            result = run_script(source, features, prior, contract, root / "out")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("persisted raw/recoverable fields present", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
