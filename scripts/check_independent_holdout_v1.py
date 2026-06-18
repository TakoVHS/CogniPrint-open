#!/usr/bin/env python3
"""Validate the independent-holdout-v1 dataset and evidence layer."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "datasets" / "independent-holdout-v1"
EVIDENCE_DIR = ROOT / "evidence" / "independent-holdout-v1"
BENCHMARK_V11_SOURCES = ROOT / "datasets" / "public-benchmark-v1.1" / "metadata" / "sample-plan-template.csv"
MIN_BASELINES = 8
MIN_ROWS = 40
MIN_AXIS_ROWS = 5
FORBIDDEN_RAW_TEXT_KEYS = {"text", "baseline_text", "variant_text", "raw_text", "generated_text"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_sources(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(dataset_dir: Path, evidence_dir: Path) -> list[str]:
    errors: list[str] = []
    sources_path = dataset_dir / "metadata" / "sources.csv"
    if not sources_path.exists():
        return [f"missing {sources_path}"]
    sources = load_sources(sources_path)
    if len(sources) < MIN_BASELINES:
        errors.append(f"holdout baselines {len(sources)} < {MIN_BASELINES}")
    source_urls = [row.get("source_url", "") for row in sources]
    if len(source_urls) != len(set(source_urls)):
        errors.append("source_url values must be unique")
    if BENCHMARK_V11_SOURCES.exists():
        benchmark_urls = {
            row.get("source_url", "")
            for row in load_sources(BENCHMARK_V11_SOURCES)
            if row.get("release_status") == "released"
        }
        overlap = sorted(set(source_urls) & benchmark_urls)
        if overlap:
            errors.append(f"holdout source URLs overlap public benchmark v1.1: {overlap}")
    for row in sources:
        sample_id = row.get("sample_id", "<missing>")
        raw_path = ROOT / row.get("file_path", "")
        if not raw_path.exists():
            errors.append(f"{sample_id}: missing raw excerpt {row.get('file_path')}")
        elif not raw_path.read_text(encoding="utf-8").strip():
            errors.append(f"{sample_id}: empty raw excerpt")
        if "gutenberg.org" not in row.get("source_url", ""):
            errors.append(f"{sample_id}: source_url must be a Project Gutenberg URL")
        if "gutenberg.org" not in row.get("license_url", ""):
            errors.append(f"{sample_id}: license_url must reference Project Gutenberg policy")

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
    missing = [name for name in required if not (evidence_dir / name).exists()]
    errors.extend(f"missing {name}" for name in missing)
    if missing:
        return errors

    manifest = load_json(evidence_dir / "manifest.json")
    counts = load_json(evidence_dir / "counts.json")
    rows = load_json(evidence_dir / "comparison-rows.json")
    if manifest.get("raw_private_inputs_included") is not False:
        errors.append("manifest must set raw_private_inputs_included=false")
    if manifest.get("generated_variant_texts_published") is not False:
        errors.append("manifest must set generated_variant_texts_published=false")
    if counts.get("baseline_count") != len(sources):
        errors.append(f"counts baseline_count={counts.get('baseline_count')} != sources {len(sources)}")
    if counts.get("comparison_row_count") != len(rows):
        errors.append(f"counts comparison_row_count={counts.get('comparison_row_count')} != rows {len(rows)}")
    if len(rows) < MIN_ROWS:
        errors.append(f"holdout rows {len(rows)} < {MIN_ROWS}")
    axis_counts = Counter(row.get("axis") for row in rows)
    if axis_counts and min(axis_counts.values()) < MIN_AXIS_ROWS:
        errors.append(f"minimum axis rows {min(axis_counts.values())} < {MIN_AXIS_ROWS}")
    for index, row in enumerate(rows):
        raw_keys = FORBIDDEN_RAW_TEXT_KEYS & set(row)
        if raw_keys:
            errors.append(f"row {index} contains raw text keys: {sorted(raw_keys)}")
        for key in ("baseline_text_sha256", "variant_text_sha256"):
            if len(str(row.get(key, ""))) != 64:
                errors.append(f"row {index} has invalid {key}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=DATASET_DIR)
    parser.add_argument("--evidence-dir", type=Path, default=EVIDENCE_DIR)
    args = parser.parse_args(argv)
    errors = validate(args.dataset_dir.resolve(), args.evidence_dir.resolve())
    if errors:
        print("independent-holdout-v1 check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    counts = load_json(args.evidence_dir.resolve() / "counts.json")
    print(
        "independent-holdout-v1 check passed: "
        f"{counts['baseline_count']} baselines / {counts['comparison_row_count']} rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
