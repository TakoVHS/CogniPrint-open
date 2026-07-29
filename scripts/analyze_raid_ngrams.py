#!/usr/bin/env python3
"""Rehydrate the pinned RAID Pilot A selection and evaluate hashed n-gram baselines."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from cogniprint.benchmarks.evaluation import grouped_split, lineage_group
from cogniprint.benchmarks.ngram import char_config, evaluate_hashed_ngram, word_config
from cogniprint.benchmarks.raid import canonical_domain, canonical_model, validate_source_columns

csv.field_size_limit(sys.maxsize)
FORBIDDEN_PERSISTED_KEYS = {
    "generation",
    "prompt",
    "raw_text",
    "raw_prompt",
    "_text",
    "tokens",
    "vocabulary",
    "ngrams",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def assert_safe_payload(payload: Any, path: str = "root") -> None:
    if isinstance(payload, dict):
        forbidden = FORBIDDEN_PERSISTED_KEYS & payload.keys()
        if forbidden:
            raise AssertionError(
                f"forbidden persisted keys at {path}: {sorted(forbidden)}"
            )
        for key, value in payload.items():
            assert_safe_payload(value, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            assert_safe_payload(value, f"{path}[{index}]")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            forbidden = FORBIDDEN_PERSISTED_KEYS & payload.keys()
            if forbidden:
                raise ValueError(
                    f"{path}:{line_number}: persisted raw/recoverable fields present: "
                    f"{sorted(forbidden)}"
                )
            records.append(payload)
    if not records:
        raise ValueError(f"{path}: no records found")
    return records


def selection_manifest(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
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


def selection_manifest_sha256(records: list[dict[str, Any]]) -> str:
    return sha256_json(selection_manifest(records))


def verify_source_contract(
    contract: dict[str, Any],
    source_sha256: str,
    source_size: int,
) -> None:
    if contract.get("sha256") != source_sha256:
        raise ValueError("source contract SHA-256 does not match the local source")
    if int(contract.get("byte_size") or -1) != source_size:
        raise ValueError("source contract byte_size does not match the local source")
    if contract.get("intended_use") != "STAGE_A_DEVELOPMENT_ONLY":
        raise ValueError(
            "source contract intended_use is not STAGE_A_DEVELOPMENT_ONLY"
        )


def validate_selected_records(selected: list[dict[str, Any]]) -> None:
    seen_ids: set[str] = set()
    for index, record in enumerate(selected, 1):
        record_id = str(record.get("source_record_id") or "").strip()
        if not record_id:
            raise ValueError(f"selected evidence record {index} is missing source_record_id")
        if record_id in seen_ids:
            raise ValueError(f"duplicate source_record_id in selected evidence: {record_id}")
        seen_ids.add(record_id)
        for key in ("model_family", "domain", "text_sha256", "lineage_id"):
            if not str(record.get(key) or "").strip():
                raise ValueError(f"selected evidence record {record_id} is missing {key}")


def rehydrate_selected_records(
    source_path: Path,
    selected: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    validate_selected_records(selected)
    by_id: dict[str, dict[str, Any]] = {
        str(record["source_record_id"]): record for record in selected
    }

    hydrated: dict[str, dict[str, Any]] = {}
    scanned_rows = 0
    verified_prompt_hashes = 0
    with source_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        missing_columns = validate_source_columns(reader.fieldnames)
        if missing_columns:
            raise ValueError(
                f"missing required CSV columns: {', '.join(missing_columns)}"
            )
        for row in reader:
            scanned_rows += 1
            record_id = str(row.get("id") or "").strip()
            expected = by_id.get(record_id)
            if expected is None:
                continue
            if record_id in hydrated:
                raise ValueError(f"source contains duplicate selected id: {record_id}")
            generation = row.get("generation")
            if not isinstance(generation, str) or not generation.strip():
                raise ValueError(f"selected source row {record_id} has no generation")
            actual_text_sha256 = hashlib.sha256(generation.encode("utf-8")).hexdigest()
            if actual_text_sha256 != expected.get("text_sha256"):
                raise ValueError(f"selected source row {record_id} text SHA-256 mismatch")
            expected_model = str(expected.get("model_family") or "")
            actual_model = canonical_model(row.get("model"))
            if actual_model != expected_model:
                raise ValueError(f"selected source row {record_id} model mismatch")
            expected_domain = str(expected.get("domain") or "")
            actual_domain = canonical_domain(row.get("domain"))
            if actual_domain != expected_domain:
                raise ValueError(f"selected source row {record_id} domain mismatch")
            expected_source_id = str(expected.get("source_id") or "")
            actual_source_id = str(row.get("source_id") or "")
            if actual_source_id != expected_source_id:
                raise ValueError(f"selected source row {record_id} source_id mismatch")
            prompt = row.get("prompt")
            prompt_text = prompt if isinstance(prompt, str) else ""
            actual_prompt_hash = (
                hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
                if prompt_text
                else None
            )
            if actual_prompt_hash != expected.get("prompt_sha256"):
                raise ValueError(f"selected source row {record_id} prompt SHA-256 mismatch")
            if actual_prompt_hash is not None:
                verified_prompt_hashes += 1
            copy = dict(expected)
            copy["_text"] = generation
            hydrated[record_id] = copy
            if len(hydrated) == len(by_id):
                break

    missing_ids = sorted(set(by_id) - set(hydrated))
    if missing_ids:
        raise ValueError(
            f"failed to rehydrate {len(missing_ids)} selected records; "
            f"first missing id: {missing_ids[0]}"
        )
    ordered = [hydrated[str(record["source_record_id"])] for record in selected]
    audit = {
        "schema": "cogniprint-raid-ngram-source-rehydration-audit-001",
        "status": "PASS",
        "selected_records": len(selected),
        "rehydrated_records": len(ordered),
        "scanned_source_rows": scanned_rows,
        "unique_source_record_ids": len(by_id),
        "unique_text_hashes": len({record["text_sha256"] for record in ordered}),
        "unique_prompt_hashes": len(
            {record["prompt_sha256"] for record in ordered if record.get("prompt_sha256")}
        ),
        "selection_manifest_sha256": selection_manifest_sha256(selected),
        "duplicate_selected_ids_detected": 0,
        "missing_selected_ids": 0,
        "all_text_hashes_verified": True,
        "all_prompt_hashes_verified": True,
        "verified_prompt_hash_count": verified_prompt_hashes,
        "all_model_families_verified": True,
        "all_domains_verified": True,
        "all_source_ids_verified": True,
        "raw_text_persisted": False,
        "raw_prompt_persisted": False,
    }
    return ordered, audit


def validate_prior_baseline(
    prior: dict[str, Any],
    train: list[dict[str, Any]],
    test: list[dict[str, Any]],
    seed: int,
    test_fraction: float,
) -> None:
    expected = {
        "seed": seed,
        "test_fraction": test_fraction,
        "train_records": len(train),
        "test_records": len(test),
        "train_groups": len({lineage_group(record) for record in train}),
        "test_groups": len({lineage_group(record) for record in test}),
    }
    for key, value in expected.items():
        if prior.get(key) != value:
            raise ValueError(
                f"prior baseline {key} mismatch: expected {value!r}, got {prior.get(key)!r}"
            )


def metrics_payload(
    records: list[dict[str, Any]],
    prior: dict[str, Any],
    *,
    seed: int,
    test_fraction: float,
    char_dimensions: int,
    word_dimensions: int,
    source_sha256: str,
    source_contract_sha256: str,
    features_sha256: str,
    prior_baseline_sha256: str,
) -> dict[str, Any]:
    train, test = grouped_split(records, seed=seed, test_fraction=test_fraction)
    validate_prior_baseline(prior, train, test, seed, test_fraction)
    overlap = {lineage_group(record) for record in train} & {
        lineage_group(record) for record in test
    }
    if overlap:
        raise AssertionError("lineage overlap detected")
    return {
        "schema": "cogniprint-raid-ngram-baselines-001",
        "protocol": "m1-raid-pilot-ngram-baselines-v1",
        "readiness_boundary": "descriptive_only",
        "research_mode": "PROOF_MODE",
        "research_status": "PRE-FREEZE",
        "stage_a_status": "DEVELOPMENT",
        "stage_b_status": "NOT_AUTHORISED_TO_START",
        "scientific_claim_evidence": False,
        "seed": seed,
        "test_fraction": test_fraction,
        "source_sha256": source_sha256,
        "source_contract_sha256": source_contract_sha256,
        "selected_features_sha256": features_sha256,
        "selection_manifest_sha256": selection_manifest_sha256(records),
        "prior_baseline_sha256": prior_baseline_sha256,
        "train_records": len(train),
        "test_records": len(test),
        "train_groups": len({lineage_group(record) for record in train}),
        "test_groups": len({lineage_group(record) for record in test}),
        "lineage_overlap_count": 0,
        "train_class_counts": dict(
            sorted(Counter(str(record["model_family"]) for record in train).items())
        ),
        "test_class_counts": dict(
            sorted(Counter(str(record["model_family"]) for record in test).items())
        ),
        "chance_accuracy_reference": prior["chance_accuracy_reference"],
        "majority": prior["majority"],
        "length_only_nearest_centroid": prior["length_only_nearest_centroid"],
        "cogniprint_12d_nearest_centroid": prior["cogniprint_12d_nearest_centroid"],
        "character_3_5_hashed_tfidf": evaluate_hashed_ngram(
            train,
            test,
            char_config(char_dimensions),
        ),
        "word_1_2_hashed_tfidf": evaluate_hashed_ngram(
            train,
            test,
            word_config(word_dimensions),
        ),
        "calibration_note": (
            "All classifiers emit uncalibrated labels. No confidence, probability, "
            "OOD, or UNKNOWN threshold is inferred here."
        ),
        "privacy_note": (
            "Raw RAID text, prompts, tokens, n-gram strings, and vocabulary are not persisted."
        ),
    }


def markdown_report(result: dict[str, Any]) -> str:
    rows = [
        ("Chance reference", None),
        ("Majority", result["majority"]),
        ("Length-only nearest centroid", result["length_only_nearest_centroid"]),
        ("CogniPrint 12D nearest centroid", result["cogniprint_12d_nearest_centroid"]),
        ("Character 3–5 hashed TF-IDF", result["character_3_5_hashed_tfidf"]["metrics"]),
        ("Word 1–2 hashed TF-IDF", result["word_1_2_hashed_tfidf"]["metrics"]),
    ]
    lines = [
        "# CogniPrint M1 RAID pilot — privacy-preserving n-gram baselines",
        "",
        f"Readiness boundary: `{result['readiness_boundary']}`",
        f"Research mode: `{result['research_mode']}`",
        f"Stage B: `{result['stage_b_status']}`",
        f"Train/test records: {result['train_records']} / {result['test_records']}",
        f"Train/test lineage groups: {result['train_groups']} / {result['test_groups']}",
        f"Chance accuracy reference: {result['chance_accuracy_reference']:.6f}",
        "",
        "| Baseline | Accuracy | Balanced accuracy | Macro F1 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, metrics in rows:
        if metrics is None:
            lines.append(
                f"| {name} | {result['chance_accuracy_reference']:.6f} | n/a | n/a |"
            )
            continue
        lines.append(
            f"| {name} | {metrics['accuracy']:.6f} | {metrics['balanced_accuracy']:.6f} | {metrics['macro_f1']:.6f} |"
        )
    lines += [
        "",
        "## Interpretation boundary",
        "",
        result["calibration_note"],
        result["privacy_note"],
        (
            "This comparison is a Stage A benchmark diagnostic, not proof of exact model "
            "identity, AI origin, authorship, actor identity, or forensic provenance."
        ),
        "",
    ]
    return "\n".join(lines)


def write_json(path: Path, payload: Any) -> None:
    assert_safe_payload(payload)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--baseline-metrics", type=Path, required=True)
    parser.add_argument("--input-file", type=Path, required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--source-contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--test-fraction", type=float, default=0.30)
    parser.add_argument("--char-dimensions", type=int, default=262_144)
    parser.add_argument("--word-dimensions", type=int, default=131_072)
    args = parser.parse_args()

    actual_source_sha256 = sha256_file(args.input_file)
    if actual_source_sha256 != args.expected_source_sha256:
        raise ValueError(
            f"source SHA-256 mismatch: expected {args.expected_source_sha256}, got {actual_source_sha256}"
        )
    source_contract = load_json(args.source_contract)
    verify_source_contract(source_contract, actual_source_sha256, args.input_file.stat().st_size)
    selected = load_jsonl(args.features)
    prior = load_json(args.baseline_metrics)
    features_sha256 = sha256_file(args.features)
    source_contract_sha256 = sha256_file(args.source_contract)
    prior_baseline_sha256 = sha256_file(args.baseline_metrics)

    first_hydrated, first_audit = rehydrate_selected_records(args.input_file, selected)
    second_hydrated, second_audit = rehydrate_selected_records(args.input_file, selected)
    for audit in (first_audit, second_audit):
        audit.update(
            {
                "source_sha256": actual_source_sha256,
                "source_byte_size": args.input_file.stat().st_size,
                "source_contract_sha256": source_contract_sha256,
                "selected_features_sha256": features_sha256,
                "prior_baseline_sha256": prior_baseline_sha256,
            }
        )

    first = metrics_payload(
        first_hydrated,
        prior,
        seed=args.seed,
        test_fraction=args.test_fraction,
        char_dimensions=args.char_dimensions,
        word_dimensions=args.word_dimensions,
        source_sha256=actual_source_sha256,
        source_contract_sha256=source_contract_sha256,
        features_sha256=features_sha256,
        prior_baseline_sha256=prior_baseline_sha256,
    )
    second = metrics_payload(
        second_hydrated,
        prior,
        seed=args.seed,
        test_fraction=args.test_fraction,
        char_dimensions=args.char_dimensions,
        word_dimensions=args.word_dimensions,
        source_sha256=actual_source_sha256,
        source_contract_sha256=source_contract_sha256,
        features_sha256=features_sha256,
        prior_baseline_sha256=prior_baseline_sha256,
    )
    first_metrics_sha = sha256_json(first)
    second_metrics_sha = sha256_json(second)
    first_audit_sha = sha256_json(first_audit)
    second_audit_sha = sha256_json(second_audit)
    if first_metrics_sha != second_metrics_sha or first_audit_sha != second_audit_sha:
        raise AssertionError("deterministic n-gram execution rerun mismatch")

    reproducibility = {
        "schema": "cogniprint-raid-ngram-reproducibility-check-001",
        "status": "PASS",
        "match": True,
        "run_1_metrics_sha256": first_metrics_sha,
        "run_2_metrics_sha256": second_metrics_sha,
        "run_1_rehydration_audit_sha256": first_audit_sha,
        "run_2_rehydration_audit_sha256": second_audit_sha,
        "source_sha256": actual_source_sha256,
        "source_contract_sha256": source_contract_sha256,
        "selected_features_sha256": features_sha256,
        "selection_manifest_sha256": selection_manifest_sha256(selected),
        "prior_baseline_sha256": prior_baseline_sha256,
        "seed": args.seed,
        "test_fraction": args.test_fraction,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "ngram-baseline-metrics.json", first)
    write_json(args.output_dir / "ngram-source-rehydration-audit.json", first_audit)
    write_json(args.output_dir / "ngram-reproducibility-check.json", reproducibility)
    (args.output_dir / "ngram-baseline-report.md").write_text(markdown_report(first), encoding="utf-8")
    print(args.output_dir / "ngram-baseline-metrics.json")
    print(args.output_dir / "ngram-baseline-report.md")
    print(args.output_dir / "ngram-source-rehydration-audit.json")
    print(args.output_dir / "ngram-reproducibility-check.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
