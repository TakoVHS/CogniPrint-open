#!/usr/bin/env python3
"""Prepare a balanced metadata-only CogniPrint pilot from the RAID dataset."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from cogniprint.benchmarks.evaluation import grouped_split, lineage_group
from cogniprint.benchmarks.raid import (
    RaidPilotConfig,
    canonical_attack,
    canonical_domain,
    canonical_model,
    collect_records,
    count_cells,
    feature_record,
    is_eligible_row,
    stable_selection_key,
    validate_source_columns,
)
from cogniprint.fingerprint import FINGERPRINT_VERSION


DATASET_ID = "liamdugan/raid"
DATASET_CONFIG = "raid"
DATASET_REVISION = "865cac74188466cb0c3b7574a10204007b57a459"
SOURCE_URL = "https://huggingface.co/datasets/liamdugan/raid"
SOURCE_PAPER = "https://aclanthology.org/2024.acl-long.674/"


csv.field_size_limit(sys.maxsize)


def parse_csv(value: str) -> tuple[str, ...]:
    items = tuple(item.strip().lower() for item in value.split(",") if item.strip())
    if not items:
        raise argparse.ArgumentTypeError("expected at least one comma-separated value")
    return items


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def git_output(repo_root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo_root, text=True).strip()


def repository_state(repo_root: Path) -> dict[str, str]:
    return {
        "repository_commit": git_output(repo_root, "rev-parse", "HEAD"),
        "repository_tree": git_output(repo_root, "rev-parse", "HEAD^{tree}"),
        "dirty_status": git_output(repo_root, "status", "--short"),
    }


def sample_row_metadata(row: dict[str, Any]) -> dict[str, Any]:
    prompt = row.get("prompt")
    generation = row.get("generation")
    title = row.get("title")
    return {
        "id": str(row.get("id") or ""),
        "source_id": str(row.get("source_id") or ""),
        "adv_source_id": str(row.get("adv_source_id") or ""),
        "model": str(row.get("model") or ""),
        "canonical_model": canonical_model(row.get("model")),
        "domain": str(row.get("domain") or ""),
        "canonical_domain": canonical_domain(row.get("domain")),
        "attack": str(row.get("attack") or ""),
        "canonical_attack": canonical_attack(row.get("attack")),
        "decoding": str(row.get("decoding") or ""),
        "repetition_penalty": str(row.get("repetition_penalty") or ""),
        "title_present": bool(str(title or "").strip()),
        "prompt_present": bool(str(prompt or "").strip()),
        "generation_characters": len(str(generation or "")),
    }


def bucket_file(bucket_dir: Path, model: str, domain: str) -> Path:
    return bucket_dir / f"{model}__{domain}.csv"


def duplicate_groups(records: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        value = str(record.get(field) or "").strip()
        if value:
            grouped[value].append(record)
    result = []
    for value, items in grouped.items():
        if len(items) > 1:
            result.append(
                {
                    "value": value,
                    "count": len(items),
                    "cells": sorted({f"{item['model_family']}/{item['domain']}" for item in items}),
                }
            )
    result.sort(key=lambda item: (-item["count"], item["value"]))
    return result


def build_duplicate_audit(
    records: list[dict[str, Any]],
    *,
    replacement_count: int,
    replacement_by_cell: dict[str, int],
    seed: int,
) -> dict[str, Any]:
    split_overlap_count: int | None = None
    split_partition_error: str | None = None
    try:
        train, test = grouped_split(records, seed=seed)
    except ValueError as exc:
        train = []
        test = []
        split_partition_error = str(exc)
    else:
        train_groups = {lineage_group(record) for record in train}
        test_groups = {lineage_group(record) for record in test}
        split_overlap_count = len(train_groups & test_groups)
    return {
        "schema": "cogniprint-raid-duplicate-lineage-audit-001",
        "selected_records": len(records),
        "unique_text_hashes": len({record["text_sha256"] for record in records}),
        "duplicate_text_groups": duplicate_groups(records, "text_sha256"),
        "duplicate_source_groups": duplicate_groups(records, "source_id"),
        "duplicate_prompt_groups": duplicate_groups(records, "prompt_sha256"),
        "replacement_count": replacement_count,
        "replacement_by_cell": dict(sorted(replacement_by_cell.items())),
        "final_cell_counts": count_cells(records),
        "split_overlap_count": split_overlap_count,
        "split_partition_error": split_partition_error,
    }


def stage_local_csv_candidates(
    input_file: Path,
    *,
    config: RaidPilotConfig,
    seed: int,
    bucket_dir: Path,
) -> tuple[dict[str, Any], int]:
    bucket_dir.mkdir(parents=True, exist_ok=True)
    handles: dict[tuple[str, str], tuple[Any, csv.DictWriter]] = {}
    model_values: set[str] = set()
    canonical_model_values: set[str] = set()
    domain_values: set[str] = set()
    canonical_domain_values: set[str] = set()
    attack_values: set[str] = set()
    canonical_attack_values: set[str] = set()
    decoding_values: set[str] = set()
    repetition_penalty_values: set[str] = set()
    raw_cell_counts: Counter[str] = Counter()
    eligible_cell_counts: Counter[str] = Counter()
    sample_rows: list[dict[str, Any]] = []
    scanned_rows = 0

    try:
        with input_file.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            missing = validate_source_columns(reader.fieldnames)
            if missing:
                raise ValueError(f"missing required CSV columns: {', '.join(missing)}")
            columns = list(reader.fieldnames or [])
            for row in reader:
                scanned_rows += 1
                if len(sample_rows) < 5:
                    sample_rows.append(sample_row_metadata(row))

                model_raw = str(row.get("model") or "")
                domain_raw = str(row.get("domain") or "")
                attack_raw = str(row.get("attack") or "")
                decoding_raw = str(row.get("decoding") or "")
                repetition_raw = str(row.get("repetition_penalty") or "")

                model_values.add(model_raw)
                domain_values.add(domain_raw)
                attack_values.add(attack_raw)
                decoding_values.add(decoding_raw)
                repetition_penalty_values.add(repetition_raw)

                canonical_model_value = canonical_model(model_raw)
                canonical_domain_value = canonical_domain(domain_raw)
                canonical_attack_value = canonical_attack(attack_raw)
                if canonical_model_value:
                    canonical_model_values.add(canonical_model_value)
                if canonical_domain_value:
                    canonical_domain_values.add(canonical_domain_value)
                if canonical_attack_value:
                    canonical_attack_values.add(canonical_attack_value)
                if canonical_model_value and canonical_domain_value:
                    raw_cell_counts[f"{canonical_model_value}/{canonical_domain_value}"] += 1

                if not is_eligible_row(row, config):
                    continue

                cell = (canonical_model_value, canonical_domain_value)
                eligible_cell_counts[f"{cell[0]}/{cell[1]}"] += 1
                generation = row.get("generation")
                if not isinstance(generation, str) or not generation.strip():
                    raise ValueError(f"row {scanned_rows} is missing non-empty generation text")
                prompt = row.get("prompt")
                prompt_text = prompt if isinstance(prompt, str) else ""
                payload = {
                    "id": row.get("id"),
                    "adv_source_id": row.get("adv_source_id"),
                    "source_id": row.get("source_id"),
                    "model": row.get("model"),
                    "decoding": row.get("decoding"),
                    "repetition_penalty": row.get("repetition_penalty"),
                    "attack": row.get("attack"),
                    "domain": row.get("domain"),
                    "prompt": prompt_text,
                    "generation": generation,
                    "_prompt_sha256": sha256_text(prompt_text) if prompt_text else None,
                    "_text_sha256": sha256_text(generation),
                    "_sort_key": stable_selection_key(row, seed),
                }
                if cell not in handles:
                    bucket_handle = bucket_file(bucket_dir, cell[0], cell[1]).open("w", encoding="utf-8", newline="")
                    writer = csv.DictWriter(bucket_handle, fieldnames=list(payload))
                    writer.writeheader()
                    handles[cell] = (bucket_handle, writer)
                handles[cell][1].writerow(payload)
    except csv.Error as exc:
        raise ValueError(f"malformed CSV: {exc}") from exc
    finally:
        for handle, _writer in handles.values():
            handle.close()

    return {
        "schema": "cogniprint-raid-source-schema-audit-001",
        "columns": columns,
        "row_sample_metadata": sample_rows,
        "model_values": sorted(model_values),
        "canonical_model_values": sorted(canonical_model_values),
        "domain_values": sorted(domain_values),
        "canonical_domain_values": sorted(canonical_domain_values),
        "attack_values": sorted(attack_values),
        "canonical_attack_values": sorted(canonical_attack_values),
        "decoding_values": sorted(decoding_values),
        "repetition_penalty_values": sorted(repetition_penalty_values),
        "raw_cell_counts": dict(sorted(raw_cell_counts.items())),
        "eligible_cell_counts": dict(sorted(eligible_cell_counts.items())),
    }, scanned_rows


def select_local_csv_records(
    bucket_dir: Path,
    *,
    config: RaidPilotConfig,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    selected_records: list[dict[str, Any]] = []
    selected_text_hashes: set[str] = set()
    replacement_count = 0
    replacement_by_cell: Counter[str] = Counter()
    missing: dict[str, int] = {}

    for model in config.models:
        for domain in config.domains:
            cell_key = f"{model}/{domain}"
            path = bucket_file(bucket_dir, model, domain)
            if not path.exists():
                missing[cell_key] = config.per_cell
                continue
            with path.open("r", encoding="utf-8", newline="") as handle:
                candidates = list(csv.DictReader(handle))
            candidates.sort(key=lambda item: (item["_sort_key"], str(item.get("id") or ""), item["_text_sha256"]))
            chosen = 0
            for candidate in candidates:
                if candidate["_text_sha256"] in selected_text_hashes:
                    replacement_count += 1
                    replacement_by_cell[cell_key] += 1
                    continue
                row = {
                    key: candidate.get(key)
                    for key in (
                        "id",
                        "adv_source_id",
                        "source_id",
                        "model",
                        "decoding",
                        "repetition_penalty",
                        "attack",
                        "domain",
                        "prompt",
                        "generation",
                    )
                }
                record = feature_record(row, config)
                selected_records.append(record)
                selected_text_hashes.add(record["text_sha256"])
                chosen += 1
                if chosen == config.per_cell:
                    break
            if chosen < config.per_cell:
                missing[cell_key] = config.per_cell - chosen

    if missing:
        raise RuntimeError(
            "RAID pilot quotas were not satisfied; missing counts: "
            + ", ".join(f"{cell}={remaining}" for cell, remaining in sorted(missing.items()))
        )

    return selected_records, {
        "replacement_count": replacement_count,
        "replacement_by_cell": dict(sorted(replacement_by_cell.items())),
    }


def summarize_local_csv_run(
    *,
    contract: dict[str, Any],
    contract_sha256: str,
    source_sha256: str,
    source_byte_size: int,
    scanned_rows: int,
    config: RaidPilotConfig,
    seed: int,
    records: list[dict[str, Any]],
    repo_state: dict[str, str],
    duplicate_audit: dict[str, Any],
) -> dict[str, Any]:
    return {
        "dataset_id": DATASET_ID,
        "dataset_config": DATASET_CONFIG,
        "dataset_revision": contract.get("source_repository_revision") or DATASET_REVISION,
        "dataset_license": contract.get("license") or "MIT",
        "source_name": contract.get("source_name") or "RAID train_none",
        "source_authority": contract.get("source_authority") or "https://github.com/liamdugan/raid",
        "source_landing_url": contract.get("landing_url") or SOURCE_URL,
        "source_download_url": contract.get("download_url"),
        "source_final_url": contract.get("final_url"),
        "source_repository_revision": contract.get("source_repository_revision"),
        "source_paper": SOURCE_PAPER,
        "source_sha256": source_sha256,
        "source_byte_size": source_byte_size,
        "source_contract_sha256": contract_sha256,
        "split": "train_none",
        "seed": seed,
        "shuffle_buffer": None,
        "scanned_rows": scanned_rows,
        "released_raw_text": False,
        "released_raw_prompts": False,
        "fingerprint_version": FINGERPRINT_VERSION,
        "readiness_boundary": "descriptive_only",
        "selection": {
            "models": list(config.models),
            "domains": list(config.domains),
            "per_cell": config.per_cell,
            "model_decoding": config.model_decoding,
            "repetition_penalty": config.repetition_penalty,
            "language": config.language,
            "attack": "none",
            "loader_path": "local_authoritative_csv_source_contract",
            "row_order_seed": seed,
        },
        "record_count": len(records),
        "cell_counts": count_cells(records),
        "duplicate_replacement_count": duplicate_audit["replacement_count"],
        "repository_commit": repo_state["repository_commit"],
        "repository_tree": repo_state["repository_tree"],
        "repository_dirty_status": repo_state["dirty_status"],
        "notes": [
            "This pilot emits features and hashes, not RAID source text.",
            "The local source contract pins the authoritative RAID clean-train CSV by URL, byte size, and SHA-256.",
            "Rows were selected deterministically by a stable hash over frozen identifiers and the fixed seed.",
            "No model-origin or authorship claim follows from this feature export alone.",
        ],
    }


def prepare_from_local_csv(args: argparse.Namespace, config: RaidPilotConfig, repo_root: Path) -> int:
    input_file = args.input_file
    if input_file is None:
        raise ValueError("--input-file is required for local CSV mode")
    if not input_file.exists():
        raise FileNotFoundError(input_file)
    if not args.expected_source_sha256:
        raise ValueError("--expected-source-sha256 is required for local CSV mode")
    if args.source_contract is None:
        raise ValueError("--source-contract is required for local CSV mode")

    actual_source_sha256 = sha256_file(input_file)
    if actual_source_sha256 != args.expected_source_sha256:
        raise ValueError(
            f"source SHA-256 mismatch: expected {args.expected_source_sha256}, got {actual_source_sha256}"
        )

    source_contract = json.loads(args.source_contract.read_text(encoding="utf-8"))
    if source_contract.get("sha256") and source_contract["sha256"] != actual_source_sha256:
        raise ValueError("source contract sha256 does not match the local source file")
    source_byte_size = input_file.stat().st_size
    if source_contract.get("byte_size") and int(source_contract["byte_size"]) != source_byte_size:
        raise ValueError("source contract byte_size does not match the local source file")
    source_contract_sha256 = sha256_file(args.source_contract)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    schema_audit_output = args.schema_audit_output or output_dir / "source-schema-audit.json"
    duplicate_audit_output = args.duplicate_audit_output or output_dir / "duplicate-lineage-audit.json"

    with tempfile.TemporaryDirectory(prefix="cogniprint-raid-pilot-") as temp_dir_name:
        bucket_dir = Path(temp_dir_name)
        schema_audit, scanned_rows = stage_local_csv_candidates(
            input_file,
            config=config,
            seed=args.seed,
            bucket_dir=bucket_dir,
        )
        schema_audit.update(
            {
                "status": "AUDITED",
                "source_name": source_contract.get("source_name") or input_file.name,
                "source_sha256": actual_source_sha256,
                "source_contract_sha256": source_contract_sha256,
                "source_byte_size": source_byte_size,
                "scanned_rows": scanned_rows,
            }
        )
        write_json(schema_audit_output, schema_audit)

        records, selection_info = select_local_csv_records(bucket_dir, config=config)
        for record in records:
            record["source_sha256"] = actual_source_sha256
            record["source_contract_sha256"] = source_contract_sha256
            record["selection_seed"] = args.seed

    duplicate_audit = build_duplicate_audit(
        records,
        replacement_count=selection_info["replacement_count"],
        replacement_by_cell=selection_info["replacement_by_cell"],
        seed=args.seed,
    )
    write_json(duplicate_audit_output, duplicate_audit)

    records_path = output_dir / "features.jsonl"
    summary_path = output_dir / "summary.json"
    with records_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    summary = summarize_local_csv_run(
        contract=source_contract,
        contract_sha256=source_contract_sha256,
        source_sha256=actual_source_sha256,
        source_byte_size=source_byte_size,
        scanned_rows=scanned_rows,
        config=config,
        seed=args.seed,
        records=records,
        repo_state=repository_state(repo_root),
        duplicate_audit=duplicate_audit,
    )
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"wrote {len(records)} records after scanning {scanned_rows} RAID rows")
    print(records_path)
    print(summary_path)
    print(schema_audit_output)
    print(duplicate_audit_output)
    return 0


def prepare_from_streaming_hf(args: argparse.Namespace, config: RaidPilotConfig) -> int:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit("Install the real-data extra first: pip install -e '.[real-data]'") from exc

    stream = load_dataset(
        DATASET_ID,
        DATASET_CONFIG,
        split=args.split,
        revision=args.revision,
        streaming=True,
    )
    stream = stream.shuffle(seed=args.seed, buffer_size=args.shuffle_buffer)
    records, scanned = collect_records(stream, config, max_scanned=args.max_scanned)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    records_path = output_dir / "features.jsonl"
    summary_path = output_dir / "summary.json"

    with records_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    summary = {
        "dataset_id": DATASET_ID,
        "dataset_config": DATASET_CONFIG,
        "dataset_revision": args.revision,
        "dataset_license": "MIT",
        "source_url": SOURCE_URL,
        "source_paper": SOURCE_PAPER,
        "split": args.split,
        "seed": args.seed,
        "shuffle_buffer": args.shuffle_buffer,
        "scanned_rows": scanned,
        "released_raw_text": False,
        "released_raw_prompts": False,
        "fingerprint_version": FINGERPRINT_VERSION,
        "readiness_boundary": "descriptive_only",
        "selection": {
            "models": list(config.models),
            "domains": list(config.domains),
            "per_cell": config.per_cell,
            "model_decoding": config.model_decoding,
            "repetition_penalty": config.repetition_penalty,
            "language": config.language,
            "attack": "none",
        },
        "record_count": len(records),
        "cell_counts": count_cells(records),
        "notes": [
            "This pilot emits features and hashes, not RAID source text.",
            "The default first pilot is English-only because CogniPrint v2 tokenization has not been validated for Czech/German diacritics.",
            "The default dataset revision is immutable and must be recorded with the exact CogniPrint commit SHA.",
            "No model-origin or authorship claim follows from this feature export alone.",
        ],
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"wrote {len(records)} records after scanning {scanned} RAID rows")
    print(records_path)
    print(summary_path)
    return 0


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", default="train")
    parser.add_argument(
        "--revision",
        default=DATASET_REVISION,
        help="Immutable Hugging Face dataset revision. Override only deliberately and record the replacement revision.",
    )
    parser.add_argument("--models", type=parse_csv, default=None)
    parser.add_argument("--domains", type=parse_csv, default=None)
    parser.add_argument("--per-cell", type=int, default=25)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--shuffle-buffer", type=int, default=10_000)
    parser.add_argument("--max-scanned", type=int, default=None)
    parser.add_argument("--input-file", type=Path, default=None)
    parser.add_argument("--expected-source-sha256", default=None)
    parser.add_argument("--source-contract", type=Path, default=None)
    parser.add_argument("--schema-audit-output", type=Path, default=None)
    parser.add_argument("--duplicate-audit-output", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("evidence/model-fingerprint-m1/raid-pilot"))
    args = parser.parse_args()

    if args.per_cell <= 0:
        parser.error("--per-cell must be positive")

    config_kwargs = {"per_cell": args.per_cell}
    if args.models is not None:
        config_kwargs["models"] = args.models
    if args.domains is not None:
        config_kwargs["domains"] = args.domains
    config = RaidPilotConfig(**config_kwargs)

    if args.input_file is not None:
        return prepare_from_local_csv(args, config, repo_root)
    return prepare_from_streaming_hf(args, config)


if __name__ == "__main__":
    raise SystemExit(main())
