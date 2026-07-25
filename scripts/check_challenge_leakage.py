#!/usr/bin/env python3
"""Compare Stage A and Stage B manifests and emit a machine-readable leakage audit.

This checker is deliberately narrow. It blocks freeze on exact sample-id or
content-hash overlap. Prompt overlap is reported separately because some study
designs intentionally reuse prompt families; whether exact prompt overlap is
allowed must be fixed in the frozen protocol.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_manifest(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: row must be an object")
            for field in ("sample_id", "content_sha256"):
                value = row.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"{path}:{line_number}: {field} must be a non-empty string")
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: manifest is empty")
    return rows


def duplicates(rows: list[dict[str, Any]], field: str) -> list[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for row in rows:
        value = row.get(field)
        if not isinstance(value, str) or not value:
            continue
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return sorted(repeated)


def values(rows: list[dict[str, Any]], field: str) -> set[str]:
    return {
        value
        for row in rows
        if isinstance((value := row.get(field)), str) and value.strip()
    }


def audit(stage_a: list[dict[str, Any]], stage_b: list[dict[str, Any]]) -> dict[str, Any]:
    a_ids, b_ids = values(stage_a, "sample_id"), values(stage_b, "sample_id")
    a_hashes, b_hashes = values(stage_a, "content_sha256"), values(stage_b, "content_sha256")
    a_prompts, b_prompts = values(stage_a, "prompt_hash"), values(stage_b, "prompt_hash")

    sample_overlap = sorted(a_ids & b_ids)
    content_overlap = sorted(a_hashes & b_hashes)
    prompt_overlap = sorted(a_prompts & b_prompts)

    duplicate_ids_a = duplicates(stage_a, "sample_id")
    duplicate_ids_b = duplicates(stage_b, "sample_id")
    duplicate_hashes_a = duplicates(stage_a, "content_sha256")
    duplicate_hashes_b = duplicates(stage_b, "content_sha256")

    blocking_reasons: list[str] = []
    if sample_overlap:
        blocking_reasons.append("SAMPLE_ID_OVERLAP")
    if content_overlap:
        blocking_reasons.append("CONTENT_HASH_OVERLAP")
    if duplicate_ids_a or duplicate_ids_b:
        blocking_reasons.append("DUPLICATE_SAMPLE_ID_WITHIN_STAGE")
    if duplicate_hashes_a or duplicate_hashes_b:
        blocking_reasons.append("DUPLICATE_CONTENT_HASH_WITHIN_STAGE")

    return {
        "schema": "cogniprint-leakage-audit-001",
        "stage_a_samples": len(stage_a),
        "stage_b_samples": len(stage_b),
        "sample_id_overlap": len(sample_overlap),
        "content_hash_overlap": len(content_overlap),
        "prompt_hash_overlap": len(prompt_overlap),
        "sample_id_overlap_values": sample_overlap,
        "content_hash_overlap_values": content_overlap,
        "prompt_hash_overlap_values": prompt_overlap,
        "duplicates": {
            "stage_a_sample_ids": duplicate_ids_a,
            "stage_b_sample_ids": duplicate_ids_b,
            "stage_a_content_hashes": duplicate_hashes_a,
            "stage_b_content_hashes": duplicate_hashes_b,
        },
        "prompt_overlap_policy": "REPORT_ONLY_UNTIL_PROTOCOL_FREEZE",
        "freeze_gate": "BLOCKED" if blocking_reasons else "PASS",
        "blocking_reasons": blocking_reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage-a", required=True, type=Path)
    parser.add_argument("--stage-b", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    report = audit(load_manifest(args.stage_a), load_manifest(args.stage_b))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["freeze_gate"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
