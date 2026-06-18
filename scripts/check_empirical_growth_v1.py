#!/usr/bin/env python3
"""Validate the empirical-growth-v1 public evidence layer."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LAYER_DIR = ROOT / "evidence" / "empirical-growth-v1"
MIN_ROWS = 200
MIN_AXIS_ROWS = 5
FORBIDDEN_RAW_TEXT_KEYS = {"text", "baseline_text", "variant_text", "raw_text", "generated_text"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(layer_dir: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "manifest.json",
        "counts.json",
        "comparison-rows.json",
        "axis-summary.json",
        "methods-summary.md",
        "results-summary.md",
        "limitations-summary.md",
        "provenance-summary.md",
    ]
    missing = [name for name in required if not (layer_dir / name).exists()]
    if missing:
        errors.extend(f"missing {name}" for name in missing)
        return errors

    manifest = load_json(layer_dir / "manifest.json")
    counts = load_json(layer_dir / "counts.json")
    rows = load_json(layer_dir / "comparison-rows.json")
    axis_summary = load_json(layer_dir / "axis-summary.json")

    if manifest.get("raw_private_inputs_included") is not False:
        errors.append("manifest must set raw_private_inputs_included=false")
    if manifest.get("raw_generated_texts_published") is not False:
        errors.append("manifest must set raw_generated_texts_published=false")
    if counts.get("comparison_row_count") != len(rows):
        errors.append(f"counts comparison_row_count={counts.get('comparison_row_count')} != rows {len(rows)}")
    if len(rows) < MIN_ROWS:
        errors.append(f"comparison rows {len(rows)} < {MIN_ROWS}")

    axis_counts = Counter(row.get("axis") for row in rows)
    if counts.get("axis_count") != len(axis_counts):
        errors.append(f"counts axis_count={counts.get('axis_count')} != observed {len(axis_counts)}")
    if axis_counts and min(axis_counts.values()) < MIN_AXIS_ROWS:
        errors.append(f"minimum axis rows {min(axis_counts.values())} < {MIN_AXIS_ROWS}")
    if counts.get("minimum_axis_row_count") != (min(axis_counts.values()) if axis_counts else 0):
        errors.append("counts minimum_axis_row_count does not match observed rows")
    if len(axis_summary) != len(axis_counts):
        errors.append(f"axis-summary rows {len(axis_summary)} != observed axis count {len(axis_counts)}")

    for index, row in enumerate(rows):
        raw_keys = FORBIDDEN_RAW_TEXT_KEYS & set(row)
        if raw_keys:
            errors.append(f"row {index} contains raw text keys: {sorted(raw_keys)}")
        for key in ("baseline_text_sha256", "variant_text_sha256"):
            value = str(row.get(key, ""))
            if len(value) != 64:
                errors.append(f"row {index} has invalid {key}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layer-dir", type=Path, default=LAYER_DIR)
    args = parser.parse_args(argv)
    errors = validate(args.layer_dir.resolve())
    if errors:
        print("empirical-growth-v1 check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    counts = load_json(args.layer_dir.resolve() / "counts.json")
    print(
        "empirical-growth-v1 check passed: "
        f"{counts['comparison_row_count']} rows / min axis {counts['minimum_axis_row_count']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
