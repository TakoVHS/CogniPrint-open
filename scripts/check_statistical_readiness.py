#!/usr/bin/env python3
"""Check whether the current statistical validation layer is still descriptive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


VALIDATION_FILES = {
    "counts": "evidence/statistical-validation-v1/counts.json",
    "bootstrap": "evidence/statistical-validation-v1/bootstrap-summary.json",
    "effect_size": "evidence/statistical-validation-v1/effect-size-summary.json",
    "variance": "evidence/statistical-validation-v1/variance-summary.json",
    "random_baseline": "evidence/statistical-validation-v1/random-baseline-summary.json",
    "bridge": "evidence/statistical-validation-v1/benchmark-campaign-bridge.json",
    "threshold_sensitivity": "evidence/statistical-validation-v1/threshold-sensitivity.json",
}

STATIC_REQUIRED_FILES = {
    "protocol": "docs/statistical-readiness-protocol.md",
}

PREFERRED_VALIDATION_DIR = "validation/wave005-descriptive-validation"
FALLBACK_VALIDATION_DIR = "evidence/statistical-validation-v1"
EMPIRICAL_GROWTH_COUNTS = "evidence/empirical-growth-v1/counts.json"
INDEPENDENT_HOLDOUT_COUNTS = "evidence/independent-holdout-v1/counts.json"
EXTERNAL_REVIEW_STATUS = "docs/external-review/status.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("docs/statistical-readiness-status.json"))
    parser.add_argument("--validation-dir", type=Path, default=None, help="Validation artifact directory to inspect.")
    parser.add_argument("--check", action="store_true", help="Fail if the output file is stale.")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    validation_dir = resolve_validation_dir(root, args.validation_dir)
    report = build_report(root, validation_dir)
    output_path = (root / args.output).resolve()
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    if args.check:
        if not output_path.exists():
            print(f"Missing statistical readiness report: {output_path}")
            return 1
        current = output_path.read_text(encoding="utf-8")
        if current != rendered:
            print(f"Stale statistical readiness report: {output_path}")
            print("Run: python scripts/check_statistical_readiness.py --output docs/statistical-readiness-status.json")
            return 1
        print("Statistical readiness report is current.")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Statistical readiness report written: {output_path}")
    print(f"Decision: {report['decision']}")
    return 0


def resolve_validation_dir(root: Path, explicit: Path | None) -> Path:
    if explicit:
        return (root / explicit).resolve() if not explicit.is_absolute() else explicit.resolve()
    preferred = root / PREFERRED_VALIDATION_DIR
    if preferred.exists():
        return preferred.resolve()
    return (root / FALLBACK_VALIDATION_DIR).resolve()


def validation_required_files(validation_dir: Path) -> dict[str, Path]:
    return {
        key: validation_dir / Path(rel_path).name
        for key, rel_path in VALIDATION_FILES.items()
    }


def build_report(root: Path, validation_dir: Path) -> dict[str, Any]:
    required_files = validation_required_files(validation_dir)
    required_files.update({name: root / rel_path for name, rel_path in STATIC_REQUIRED_FILES.items()})
    missing = [name for name, path in required_files.items() if not path.exists()]
    counts = load_json(required_files["counts"]) if "counts" not in missing else {}
    effect_size = load_json(required_files["effect_size"]) if "effect_size" not in missing else {}
    growth_counts = load_json(root / EMPIRICAL_GROWTH_COUNTS) if (root / EMPIRICAL_GROWTH_COUNTS).exists() else {}
    holdout_counts = load_json(root / INDEPENDENT_HOLDOUT_COUNTS) if (root / INDEPENDENT_HOLDOUT_COUNTS).exists() else {}

    per_axis_counts = extract_axis_counts(effect_size)
    campaign_min_axis_count = min(per_axis_counts.values()) if per_axis_counts else 0
    public_growth_min_axis_count = int(growth_counts.get("minimum_axis_row_count", 0))
    independent_holdout_min_axis_count = int(holdout_counts.get("minimum_axis_row_count", 0))
    readiness_min_axis_count = max(campaign_min_axis_count, public_growth_min_axis_count)
    campaign_rows = int(counts.get("empirical_comparison_row_count", 0))
    public_growth_rows = int(growth_counts.get("comparison_row_count", 0))
    independent_holdout_rows = int(holdout_counts.get("comparison_row_count", 0))
    combined_empirical_rows = campaign_rows + public_growth_rows + independent_holdout_rows

    gates = {
        "required_files_present": not missing,
        "empirical_rows_at_least_200": combined_empirical_rows >= 200,
        "benchmark_baselines_at_least_20": int(counts.get("benchmark_baseline_count", 0)) >= 20,
        "benchmark_variants_at_least_100": int(counts.get("benchmark_variant_count", 0)) >= 100,
        "axis_counts_at_least_5": readiness_min_axis_count >= 5,
        "bootstrap_intervals_present": "bootstrap" not in missing,
        "effect_sizes_present": "effect_size" not in missing,
        "variance_decomposition_present": "variance" not in missing,
        "random_reference_present": "random_baseline" not in missing,
        "benchmark_campaign_bridge_present": "bridge" not in missing,
        "threshold_sensitivity_present": "threshold_sensitivity" not in missing,
        "p_value_layer_preregistered": wave005_p_value_layer_preregistered(root),
        "multiple_comparison_correction_applied": multiple_comparison_correction_applied(root),
        "baseline_comparison_present": baseline_comparison_present(root),
        "independent_external_review_present": independent_external_review_present(root),
        "independent_holdout_corpus_present": independent_holdout_corpus_present(root),
    }
    inferential_ready = all(gates.values())

    return {
        "snapshot_id": counts.get("snapshot_id", "unknown"),
        "validation_dir": str(validation_dir.relative_to(root)) if validation_dir.is_relative_to(root) else str(validation_dir),
        "decision": "inferential_candidate" if inferential_ready else "descriptive_only",
        "missing_required_files": missing,
        "counts": {
            "empirical_comparison_rows": combined_empirical_rows,
            "local_campaign_comparison_rows": campaign_rows,
            "public_empirical_growth_rows": public_growth_rows,
            "independent_holdout_rows": independent_holdout_rows,
            "benchmark_baselines": counts.get("benchmark_baseline_count", 0),
            "benchmark_variants": counts.get("benchmark_variant_count", 0),
            "campaign_axes": counts.get("campaign_axis_count", 0),
            "benchmark_axes": counts.get("benchmark_axis_count", 0),
            "shared_bridge_axes": counts.get("shared_bridge_axis_count", 0),
        },
        "minimum_axis_comparison_count": readiness_min_axis_count,
        "minimum_local_campaign_axis_comparison_count": campaign_min_axis_count,
        "minimum_public_growth_axis_comparison_count": public_growth_min_axis_count,
        "minimum_independent_holdout_axis_comparison_count": independent_holdout_min_axis_count,
        "gates": gates,
        "blocked_by": [name for name, passed in gates.items() if not passed],
        "guardrail": (
            "Keep validation wording descriptive until all gates pass. Public empirical growth improves controlled-row "
            "scale, and independent holdout validation improves source separation, but external review is still required."
        ),
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def wave005_p_value_layer_preregistered(root: Path) -> bool:
    prereg_path = root / "docs" / "pre-registration-wave005.md"
    hash_path = root / "validation" / "wave005_prereg_hash.txt"
    results_path = root / "validation" / "wave005_results.json"
    if not (prereg_path.exists() and hash_path.exists() and results_path.exists()):
        return False
    current_hash = hashlib.sha256(prereg_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    if current_hash != hash_path.read_text(encoding="utf-8").strip():
        return False
    results = load_json(results_path)
    return "permutation_p_value" in results and "mean_difference" in results


def multiple_comparison_correction_applied(root: Path) -> bool:
    path = root / "validation" / "statistical-validation-v1.2" / "multiple-comparison-correction.json"
    if not path.exists():
        return False
    payload = load_json(path)
    correction_methods = payload.get("correction_methods", [])
    rows = payload.get("rows", [])
    return (
        int(payload.get("test_count", 0)) >= 1
        and bool(rows)
        and "Holm-Bonferroni family-wise correction" in correction_methods
        and "Benjamini-Hochberg false-discovery-rate correction" in correction_methods
    )


def baseline_comparison_present(root: Path) -> bool:
    baseline_dir = root / "validation" / "conventional-stylometry-baseline-v1"
    manifest_path = baseline_dir / "manifest.json"
    bridge_path = baseline_dir / "cogniprint-bridge.json"
    if not (manifest_path.exists() and bridge_path.exists()):
        return False
    manifest = load_json(manifest_path)
    bridge = load_json(bridge_path)
    return (
        manifest.get("method") == "character n-gram TF cosine similarity"
        and int(bridge.get("shared_axis_count", 0)) >= 1
    )


def independent_holdout_corpus_present(root: Path) -> bool:
    counts_path = root / "evidence" / "independent-holdout-v1" / "counts.json"
    manifest_path = root / "evidence" / "independent-holdout-v1" / "manifest.json"
    if not (counts_path.exists() and manifest_path.exists()):
        return False
    counts = load_json(counts_path)
    manifest = load_json(manifest_path)
    return (
        manifest.get("raw_private_inputs_included") is False
        and int(counts.get("baseline_count", 0)) >= 8
        and int(counts.get("comparison_row_count", 0)) >= 40
        and int(counts.get("minimum_axis_row_count", 0)) >= 5
    )


def independent_external_review_present(root: Path) -> bool:
    status_path = root / EXTERNAL_REVIEW_STATUS
    if not status_path.exists():
        return False
    status = load_json(status_path)
    return (
        status.get("independent_external_review_present") is True
        and int(status.get("valid_review_count", 0)) >= int(status.get("minimum_required_valid_reviews", 1))
    )


def extract_axis_counts(effect_size: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in effect_size.get("comparisons", []):
        axis = str(item.get("axis", "unknown"))
        values = []
        for key in ("cosine_similarity_hedges_g", "euclidean_distance_hedges_g"):
            metric = item.get(key) or {}
            if "comparison_count" in metric:
                values.append(int(metric["comparison_count"]))
        if values:
            counts[axis] = min(values)
    return counts


if __name__ == "__main__":
    raise SystemExit(main())
