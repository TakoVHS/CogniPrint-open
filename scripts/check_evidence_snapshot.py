#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FILES = {
    "evidence/empirical-v1": {
        "manifest.json",
        "counts.json",
        "methods-summary.md",
        "results-summary.md",
        "limitations-summary.md",
        "evidence-table.md",
        "provenance-summary.md",
        "README.md",
    },
    "evidence/public-benchmark-v1": {
        "manifest.json",
        "counts.json",
        "methods-summary.md",
        "results-summary.md",
        "limitations-summary.md",
        "evidence-table.md",
        "provenance-summary.md",
        "coverage-summary.md",
        "README.md",
    },
    "evidence/public-benchmark-v1.1": {
        "manifest.json",
        "counts.json",
        "methods-summary.md",
        "results-summary.md",
        "limitations-summary.md",
        "evidence-table.md",
        "provenance-summary.md",
        "README.md",
    },
    "evidence/statistical-validation-v1": {
        "manifest.json",
        "counts.json",
        "methods-summary.md",
        "results-summary.md",
        "limitations-summary.md",
        "benchmark-campaign-bridge-summary.md",
        "README.md",
    },
}


def validate_empirical(root: Path, errors: list[str]) -> None:
    manifest = json.loads((root / "evidence/empirical-v1/manifest.json").read_text(encoding="utf-8"))
    counts = json.loads((root / "evidence/empirical-v1/counts.json").read_text(encoding="utf-8"))
    if manifest.get("campaign_count") != 5:
        errors.append("evidence/empirical-v1 manifest campaign_count != 5")
    if manifest.get("comparison_row_count") != 41:
        errors.append("evidence/empirical-v1 manifest comparison_row_count != 41")
    campaign_004 = manifest.get("campaign_004", {})
    if campaign_004.get("comparison_row_count") != 11:
        errors.append("evidence/empirical-v1 manifest campaign_004 comparison_row_count != 11")
    if counts.get("campaign_count") != 5 or counts.get("comparison_row_count") != 41:
        errors.append("evidence/empirical-v1 counts.json does not match expected 5 campaigns / 41 rows")


def validate_benchmark(root: Path, errors: list[str]) -> None:
    manifest = json.loads((root / "evidence/public-benchmark-v1/manifest.json").read_text(encoding="utf-8"))
    counts = json.loads((root / "evidence/public-benchmark-v1/counts.json").read_text(encoding="utf-8"))
    if manifest.get("snapshot_id") != "public-benchmark-v1":
        errors.append("evidence/public-benchmark-v1 snapshot_id mismatch")
    for key in ("released_samples", "released_variants", "released_languages", "released_source_classes", "released_perturbation_axes"):
        if key not in manifest:
            errors.append(f"evidence/public-benchmark-v1 manifest missing {key}")
    for key in ("released_samples", "released_variants", "released_languages", "released_source_classes", "released_perturbation_axes"):
        if key not in counts:
            errors.append(f"evidence/public-benchmark-v1 counts.json missing {key}")

    manifest_v11 = json.loads((root / "evidence/public-benchmark-v1.1/manifest.json").read_text(encoding="utf-8"))
    counts_v11 = json.loads((root / "evidence/public-benchmark-v1.1/counts.json").read_text(encoding="utf-8"))
    if manifest_v11.get("snapshot_id") != "public-benchmark-v1.1":
        errors.append("evidence/public-benchmark-v1.1 snapshot_id mismatch")
    for key in ("released_samples", "released_variants", "released_languages", "released_source_classes", "released_perturbation_axes"):
        if key not in manifest_v11:
            errors.append(f"evidence/public-benchmark-v1.1 manifest missing {key}")
        if key not in counts_v11:
            errors.append(f"evidence/public-benchmark-v1.1 counts.json missing {key}")


def validate_statistical(root: Path, errors: list[str]) -> None:
    manifest = json.loads((root / "evidence/statistical-validation-v1/manifest.json").read_text(encoding="utf-8"))
    counts = json.loads((root / "evidence/statistical-validation-v1/counts.json").read_text(encoding="utf-8"))
    if not str(manifest.get("snapshot_id", "")).startswith("statistical-validation-v1"):
        errors.append("evidence/statistical-validation-v1 snapshot_id mismatch")
    for key in ("empirical_campaign_count", "empirical_comparison_row_count", "benchmark_baseline_count", "benchmark_variant_count"):
        if key not in counts:
            errors.append(f"evidence/statistical-validation-v1 counts.json missing {key}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    errors: list[str] = []

    for rel_dir, files in REQUIRED_FILES.items():
        dir_path = root / rel_dir
        if not dir_path.exists():
            errors.append(f"missing directory: {rel_dir}")
            continue
        for file_name in files:
            if not (dir_path / file_name).exists():
                errors.append(f"missing file: {rel_dir}/{file_name}")

    if not errors:
        validate_empirical(root, errors)
        validate_benchmark(root, errors)
        validate_statistical(root, errors)

    if errors:
        print("Evidence snapshot integrity check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Evidence snapshot integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
