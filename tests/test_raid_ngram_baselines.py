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
    hashed_counts,
    normalize_text,
    word_config,
    word_tokens,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "analyze_raid_ngrams.py"
SEED = 20260725


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for label in ("human", "gpt4"):
        for index in range(40):
            if label == "human":
                text = (
                    f"Human essay {index}. Personal narrative with varied rhythm "
                    "and an ordinary lived example."
                )
            else:
                text = (
                    f"Generated technical summary {index}. Structured synthesis "
                    "presents systematic conclusions and formal transitions."
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
                    "prompt": "" if label == "human" else f"prompt {index}",
                    "generation": text,
                }
            )
    return rows


def write_source(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_features(path: Path, rows: list[dict[str, str]]) -> list[dict]:
    records: list[dict] = []
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
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    return records


def empty_metrics(labels: list[str]) -> dict:
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


def write_prior(path: Path, records: list[dict]) -> None:
    train, test = grouped_split(records, seed=SEED, test_fraction=0.30)
    labels = sorted({record["model_family"] for record in records})
    metric = empty_metrics(labels)
    payload = {
        "seed": SEED,
        "test_fraction": 0.30,
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


def write_contract(path: Path, source: Path) -> None:
    payload = {
        "sha256": sha256_file(source),
        "byte_size": source.stat().st_size,
        "intended_use": "STAGE_A_DEVELOPMENT_ONLY",
    }
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def run_script(
    source: Path,
    features: Path,
    prior: Path,
    contract: Path,
    out: Path,
    expected_sha: str | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        f"{REPO_ROOT / 'src'}{os.pathsep}{env.get('PYTHONPATH', '')}"
    ).rstrip(os.pathsep)
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
        self.assertEqual(
            word_tokens("Don't stop, 42 times."),
            ["don't", "stop", "42", "times"],
        )

    def test_hashed_counts_are_deterministic_and_nonnegative(self) -> None:
        config = char_config(128)
        first = hashed_counts("A deterministic sentence.", config)
        second = hashed_counts("A deterministic sentence.", config)
        self.assertEqual(first, second)
        self.assertTrue(first)
        self.assertTrue(all(index >= 0 and count > 0 for index, count in first.items()))

    def test_toy_ngram_baselines_execute(self) -> None:
        records: list[dict] = []
        for label, prefix in (
            ("human", "personal story memory"),
            ("gpt4", "systematic technical synthesis"),
        ):
            for index in range(30):
                records.append(
                    {
                        "model_family": label,
                        "source_id": f"{label}-{index}",
                        "text_sha256": sha256_text(f"{label}-{index}"),
                        "_text": f"{prefix} example {index} {prefix}",
                    }
                )
        train, test = grouped_split(records, seed=SEED, test_fraction=0.30)
        char_result = evaluate_hashed_ngram(train, test, char_config(1024))
        word_result = evaluate_hashed_ngram(train, test, word_config(512))
        self.assertGreaterEqual(char_result["metrics"]["accuracy"], 0.8)
        self.assertGreaterEqual(word_result["metrics"]["accuracy"], 0.8)
        self.assertFalse(char_result["persisted_vocabulary"])
        self.assertFalse(word_result["raw_text_persisted"])

    def test_script_rehydrates_exact_selection_and_persists_no_raw_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            rows = source_rows()
            source = root / "source.csv"
            write_source(source, rows)
            features = root / "features.jsonl"
            records = write_features(features, rows)
            prior = root / "prior.json"
            write_prior(prior, records)
            contract = root / "contract.json"
            write_contract(contract, source)
            out = root / "out"
            result = run_script(source, features, prior, contract, out)
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            metrics = json.loads(
                (out / "ngram-baseline-metrics.json").read_text()
            )
            audit = json.loads(
                (out / "ngram-source-rehydration-audit.json").read_text()
            )
            reproducibility = json.loads(
                (out / "ngram-reproducibility-check.json").read_text()
            )
            self.assertEqual(audit["rehydrated_records"], 80)
            self.assertTrue(audit["all_text_hashes_verified"])
            self.assertTrue(reproducibility["match"])
            serialized = json.dumps([metrics, audit, reproducibility])
            for forbidden in (
                '"generation"',
                '"prompt"',
                '"raw_text"',
                '"_text"',
                '"vocabulary"',
                '"tokens"',
            ):
                self.assertNotIn(forbidden, serialized)

    def test_source_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            rows = source_rows()
            source = root / "source.csv"
            write_source(source, rows)
            features = root / "features.jsonl"
            records = write_features(features, rows)
            prior = root / "prior.json"
            write_prior(prior, records)
            contract = root / "contract.json"
            write_contract(contract, source)
            result = run_script(
                source,
                features,
                prior,
                contract,
                root / "out",
                expected_sha="0" * 64,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "source SHA-256 mismatch",
                result.stderr + result.stdout,
            )

    def test_selected_text_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            rows = source_rows()
            source = root / "source.csv"
            write_source(source, rows)
            features = root / "features.jsonl"
            records = write_features(features, rows)
            records[0]["text_sha256"] = "0" * 64
            features.write_text(
                "".join(json.dumps(record) + "\n" for record in records),
                encoding="utf-8",
            )
            prior = root / "prior.json"
            write_prior(prior, records)
            contract = root / "contract.json"
            write_contract(contract, source)
            result = run_script(
                source,
                features,
                prior,
                contract,
                root / "out",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "text SHA-256 mismatch",
                result.stderr + result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
