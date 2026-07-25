#!/usr/bin/env python3
"""Validate CogniPrint model-fingerprint benchmark manifest records.

This validator intentionally checks only the repository's bounded M0 metadata
contract. It does not validate scientific attribution claims.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "benchmarks" / "model-fingerprint-v0.1" / "sample.example.json"

REQUIRED = {
    "sample_id",
    "origin_class",
    "language",
    "domain",
    "text_sha256",
    "release_status",
}

ORIGIN_CLASSES = {"human", "model", "mixed", "unknown"}
RELEASE_STATUSES = {"private_research", "releasable_metadata", "released"}
EDIT_INTENSITIES = {None, "none", "light", "medium", "high"}
TRANSFORMATIONS = {
    None,
    "paraphrase",
    "translation",
    "back_translation",
    "grammar_edit",
    "punctuation_edit",
    "compression",
    "expansion",
    "style_transfer",
    "sentence_reorder",
    "human_light_edit",
    "human_substantive_edit",
    "second_model_rewrite",
    "other",
}
PROVENANCE_TYPES = {
    "hash",
    "c2pa",
    "revision_history",
    "tool_log",
    "repository_history",
    "authenticated_approval",
    "other",
}
PROVENANCE_STATUSES = {"present", "absent", "withheld", "not_applicable"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def load_records(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
        return payload
    raise ValueError("manifest must be a JSON object or a list of JSON objects")


def validate_record(record: dict[str, object], index: int) -> list[str]:
    errors: list[str] = []
    prefix = str(record.get("sample_id") or f"record[{index}]")

    missing = sorted(field for field in REQUIRED if field not in record or record[field] in (None, ""))
    for field in missing:
        errors.append(f"{prefix}: missing required field {field}")

    if record.get("origin_class") not in ORIGIN_CLASSES:
        errors.append(f"{prefix}: invalid origin_class={record.get('origin_class')!r}")

    if record.get("release_status") not in RELEASE_STATUSES:
        errors.append(f"{prefix}: invalid release_status={record.get('release_status')!r}")

    sha = record.get("text_sha256")
    if not isinstance(sha, str) or not SHA256_RE.fullmatch(sha):
        errors.append(f"{prefix}: text_sha256 must be 64 hexadecimal characters")

    if record.get("human_edit_intensity") not in EDIT_INTENSITIES:
        errors.append(f"{prefix}: invalid human_edit_intensity={record.get('human_edit_intensity')!r}")

    if record.get("transformation_type") not in TRANSFORMATIONS:
        errors.append(f"{prefix}: invalid transformation_type={record.get('transformation_type')!r}")

    evidence = record.get("provenance_evidence", [])
    if not isinstance(evidence, list):
        errors.append(f"{prefix}: provenance_evidence must be a list")
    else:
        for item_index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"{prefix}: provenance_evidence[{item_index}] must be an object")
                continue
            if item.get("type") not in PROVENANCE_TYPES:
                errors.append(
                    f"{prefix}: provenance_evidence[{item_index}] invalid type={item.get('type')!r}"
                )
            if item.get("status") not in PROVENANCE_STATUSES:
                errors.append(
                    f"{prefix}: provenance_evidence[{item_index}] invalid status={item.get('status')!r}"
                )

    if record.get("origin_class") == "model" and not record.get("model_family"):
        errors.append(f"{prefix}: model-origin record should declare model_family when known")

    if record.get("origin_class") == "human" and record.get("model_family"):
        errors.append(f"{prefix}: human-origin record must not declare model_family")

    parent = record.get("parent_sample_id")
    transformation = record.get("transformation_type")
    if transformation is not None and not parent:
        errors.append(f"{prefix}: transformed record requires parent_sample_id")

    return errors


def validate_unique_ids(records: list[dict[str, object]]) -> list[str]:
    ids = [record.get("sample_id") for record in records if record.get("sample_id")]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    return [f"duplicate sample_id: {item}" for item in duplicates]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, default=[DEFAULT_PATH])
    args = parser.parse_args(argv)

    all_records: list[dict[str, object]] = []
    errors: list[str] = []

    for path in args.paths:
        resolved = path if path.is_absolute() else (ROOT / path)
        if not resolved.exists():
            errors.append(f"missing manifest file: {resolved}")
            continue
        try:
            records = load_records(resolved)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{resolved}: {exc}")
            continue
        for index, record in enumerate(records):
            errors.extend(validate_record(record, index))
        all_records.extend(records)

    errors.extend(validate_unique_ids(all_records))

    if errors:
        print("model-fingerprint manifest check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"model-fingerprint manifest check passed: {len(all_records)} record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
