#!/usr/bin/env python3
"""Validate the public-benchmark-v1.1 registry and evidence summaries."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "datasets" / "public-benchmark-v1.1" / "metadata" / "sample-plan-template.csv"
COUNTS_PATH = ROOT / "evidence" / "public-benchmark-v1.1" / "counts.json"
MIN_BASELINES = 20
MIN_VARIANTS = 100


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_rows(rows: list[dict[str, str]], root: Path) -> list[str]:
    errors: list[str] = []
    released = [row for row in rows if row.get("release_status") == "released"]
    baselines = [row for row in released if row.get("relation_type") == "baseline"]
    variants = [row for row in released if row.get("relation_type") != "baseline"]
    baseline_ids = {row["sample_id"] for row in baselines}
    sample_ids = [row["sample_id"] for row in released]

    if len(sample_ids) != len(set(sample_ids)):
        errors.append("released sample IDs are not unique")
    if len(baselines) < MIN_BASELINES:
        errors.append(f"released baselines {len(baselines)} < {MIN_BASELINES}")
    if len(variants) < MIN_VARIANTS:
        errors.append(f"released variants {len(variants)} < {MIN_VARIANTS}")

    required_fields = [
        "sample_id",
        "relation_type",
        "sample_title",
        "file_path",
        "license",
        "source_url",
        "acquisition_date",
        "source_class",
        "language",
        "source_domain",
        "release_wave",
        "release_status",
    ]
    for row in released:
        row_id = row.get("sample_id", "<missing>")
        for field in required_fields:
            if not row.get(field):
                errors.append(f"{row_id}: missing {field}")
        path = root / row.get("file_path", "")
        if not path.exists():
            errors.append(f"{row_id}: missing file {row.get('file_path')}")
        elif not path.read_text(encoding="utf-8").strip():
            errors.append(f"{row_id}: empty file {row.get('file_path')}")
        if not row.get("source_url", "").startswith("https://"):
            errors.append(f"{row_id}: source_url must be https")
        if row.get("relation_type") == "baseline":
            if row.get("baseline_sample_id"):
                errors.append(f"{row_id}: baseline row must not have baseline_sample_id")
        else:
            parent = row.get("baseline_sample_id", "")
            if parent not in baseline_ids:
                errors.append(f"{row_id}: variant parent {parent} is not a released baseline")
            if "Derived benchmark variant" not in row.get("license", ""):
                errors.append(f"{row_id}: variant license should mark derived benchmark variant")
    return errors


def validate_counts(rows: list[dict[str, str]], counts_path: Path) -> list[str]:
    errors: list[str] = []
    counts = json.loads(counts_path.read_text(encoding="utf-8"))
    released = [row for row in rows if row.get("release_status") == "released"]
    baselines = [row for row in released if row.get("relation_type") == "baseline"]
    variants = [row for row in released if row.get("relation_type") != "baseline"]
    expected = {
        "released_samples": len(baselines),
        "released_variants": len(variants),
        "released_languages": len({row["language"] for row in released}),
        "released_source_classes": len({row["source_class"] for row in baselines}),
        "released_perturbation_axes": len({row["relation_type"] for row in variants}),
    }
    for key, value in expected.items():
        if counts.get(key) != value:
            errors.append(f"counts.json {key}={counts.get(key)} != registry {value}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    rows = load_rows(root / REGISTRY_PATH.relative_to(ROOT))
    errors = validate_rows(rows, root)
    errors.extend(validate_counts(rows, root / COUNTS_PATH.relative_to(ROOT)))
    if errors:
        print("public-benchmark-v1.1 check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    released = [row for row in rows if row.get("release_status") == "released"]
    baselines = [row for row in released if row.get("relation_type") == "baseline"]
    variants = [row for row in released if row.get("relation_type") != "baseline"]
    print(f"public-benchmark-v1.1 check passed: {len(baselines)} baselines / {len(variants)} variants.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
