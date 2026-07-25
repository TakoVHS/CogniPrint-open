#!/usr/bin/env python3
"""Materialize public-benchmark-v1.1 as a Stage-A-only blinded manifest.

This script does not perform attribution or evaluate model families. It hashes
already-released benchmark files and emits only development-visible records for
Challenge 001. The resulting samples are permanently quarantined from sealed
Stage B by the Development Exposure Registry.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


SCHEMA = "cogniprint-challenge-001-blinded-sample-v1"
DEFAULT_METADATA = Path("datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_hash(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def materialize(root: Path, metadata_csv: Path) -> list[dict[str, object]]:
    metadata_path = metadata_csv if metadata_csv.is_absolute() else root / metadata_csv
    rows: list[dict[str, object]] = []
    seen_ids: set[str] = set()

    with metadata_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "sample_id",
            "baseline_sample_id",
            "file_path",
            "source_url",
            "acquisition_date",
            "release_status",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"metadata CSV missing required columns: {sorted(missing)}")

        for line_number, source in enumerate(reader, 2):
            if source.get("release_status") != "released":
                continue
            sample_id = (source.get("sample_id") or "").strip()
            if not sample_id:
                raise ValueError(f"metadata line {line_number}: empty sample_id")
            if sample_id in seen_ids:
                raise ValueError(f"metadata line {line_number}: duplicate sample_id {sample_id}")
            seen_ids.add(sample_id)

            relative = Path((source.get("file_path") or "").strip())
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"metadata line {line_number}: unsafe file_path {relative}")
            target = (root / relative).resolve(strict=True)
            try:
                target.relative_to(root.resolve())
            except ValueError as exc:
                raise ValueError(f"metadata line {line_number}: file escapes repository root") from exc
            if not target.is_file() or target.is_symlink():
                raise ValueError(f"metadata line {line_number}: file_path must resolve to a regular non-symlink file")

            baseline_id = (source.get("baseline_sample_id") or "").strip() or sample_id
            source_url = (source.get("source_url") or "").strip()
            acquisition_date = (source.get("acquisition_date") or "").strip()
            lineage_group_hash = stable_hash(f"public-benchmark-v1.1:{baseline_id}")
            origin_record_hash = stable_hash(
                json.dumps(
                    {
                        "sample_id": sample_id,
                        "baseline_sample_id": baseline_id,
                        "source_url": source_url,
                        "acquisition_date": acquisition_date,
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                )
            )

            rows.append(
                {
                    "schema": SCHEMA,
                    "sample_id": sample_id,
                    "content_sha256": sha256_file(target),
                    "stage": "STAGE_A_DEVELOPMENT",
                    "lineage_group_hash": lineage_group_hash,
                    "origin_record_hash": origin_record_hash,
                    "reference_set_membership": "DEVELOPMENT_ONLY",
                    "development_visibility": True,
                    "evaluation_visibility": False,
                    "collection_window": acquisition_date or "UNKNOWN",
                    "notes_public": "public-benchmark-v1.1; permanently development-visible for Challenge 001",
                }
            )

    if not rows:
        raise ValueError("no released benchmark rows were materialized")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("challenge-001/development/stage-a/public-benchmark-v1.1.manifest.jsonl"),
    )
    args = parser.parse_args()

    rows = materialize(args.root, args.metadata)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), "records": len(rows), "stage": "STAGE_A_DEVELOPMENT"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
