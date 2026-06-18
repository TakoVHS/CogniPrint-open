#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def expect_equal(errors: list[str], actual: object, expected: object, label: str) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def require_dict(errors: list[str], value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        errors.append(f"docs/evidence-visibility-checks.json: {label} must be an object")
        return {}
    return value


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    checks = load_json(root / "docs/evidence-visibility-checks.json")
    empirical = load_json(root / "evidence/empirical-v1/counts.json")
    benchmark = load_json(root / "evidence/public-benchmark-v1.1/counts.json")
    growth = load_json(root / "evidence/empirical-growth-v1/counts.json")
    holdout = load_json(root / "evidence/independent-holdout-v1/counts.json")
    validation = load_json(root / "validation/wave005-descriptive-validation/counts.json")
    correction = load_json(root / "validation/statistical-validation-v1.2/counts.json")
    baseline = load_json(root / "validation/conventional-stylometry-baseline-v1/counts.json")
    readiness = load_json(root / "docs/statistical-readiness-status.json")
    external_review = load_json(root / "docs/external-review/status.json")

    errors: list[str] = []

    evidence_snapshot = require_dict(errors, checks.get("evidence_snapshot"), "evidence_snapshot")
    public_benchmark = require_dict(errors, checks.get("public_benchmark_v1_1"), "public_benchmark_v1_1")
    readiness_package = require_dict(errors, checks.get("readiness_package"), "readiness_package")
    validation_wave005 = require_dict(errors, checks.get("validation_wave005"), "validation_wave005")
    validation_v12 = require_dict(errors, checks.get("validation_v1_2"), "validation_v1_2")
    external_gate = require_dict(errors, checks.get("external_review_gate"), "external_review_gate")

    if errors:
        print("Evidence visibility check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    expect_equal(errors, evidence_snapshot.get("campaigns"), empirical.get("campaign_count"), "campaign count")
    expect_equal(errors, evidence_snapshot.get("comparison_rows"), empirical.get("comparison_row_count"), "local comparison row count")
    campaign_004 = empirical.get("campaign_004")
    expect_equal(
        errors,
        evidence_snapshot.get("campaign_004_rows"),
        campaign_004.get("comparison_row_count") if isinstance(campaign_004, dict) else None,
        "campaign-004 row count",
    )

    expect_equal(errors, public_benchmark.get("released_baselines"), benchmark.get("released_samples"), "v1.1 benchmark baselines")
    expect_equal(errors, public_benchmark.get("released_variants"), benchmark.get("released_variants"), "v1.1 benchmark variants")
    expect_equal(errors, public_benchmark.get("released_languages"), benchmark.get("released_languages"), "v1.1 benchmark languages")
    expect_equal(errors, public_benchmark.get("released_source_classes"), benchmark.get("released_source_classes"), "v1.1 benchmark source classes")
    expect_equal(errors, public_benchmark.get("released_perturbation_axes"), benchmark.get("released_perturbation_axes"), "v1.1 benchmark axes")

    readiness_counts = readiness.get("counts") if isinstance(readiness.get("counts"), dict) else {}
    expect_equal(errors, readiness_package.get("readiness"), readiness.get("decision"), "readiness decision")
    expect_equal(errors, readiness_package.get("local_campaign_rows"), readiness_counts.get("local_campaign_comparison_rows"), "readiness local rows")
    expect_equal(errors, readiness_package.get("public_growth_rows"), growth.get("comparison_row_count"), "public growth rows")
    expect_equal(errors, readiness_package.get("independent_holdout_rows"), holdout.get("comparison_row_count"), "holdout rows")
    expect_equal(errors, readiness_package.get("combined_readiness_rows"), readiness_counts.get("empirical_comparison_rows"), "combined readiness rows")
    expect_equal(errors, readiness_package.get("blocked_by"), readiness.get("blocked_by"), "readiness blockers")

    expect_equal(errors, validation_wave005.get("snapshot_id"), validation.get("snapshot_id"), "wave005 snapshot id")
    expect_equal(errors, validation_wave005.get("benchmark_baselines"), validation.get("benchmark_baseline_count"), "wave005 benchmark baselines")
    expect_equal(errors, validation_wave005.get("benchmark_variants"), validation.get("benchmark_variant_count"), "wave005 benchmark variants")
    expect_equal(errors, validation_wave005.get("benchmark_languages"), validation.get("benchmark_language_count"), "wave005 benchmark languages")
    expect_equal(errors, validation_wave005.get("benchmark_source_classes"), validation.get("benchmark_source_class_count"), "wave005 source classes")
    expect_equal(errors, validation_wave005.get("shared_bridge_axes"), validation.get("shared_bridge_axis_count"), "wave005 bridge axes")
    expect_equal(errors, validation_wave005.get("framing"), "descriptive", "wave005 framing")

    expect_equal(errors, validation_v12.get("correction_tests"), correction.get("correction_test_count"), "v1.2 correction tests")
    expect_equal(errors, validation_v12.get("holm_flagged_axes"), correction.get("holm_flagged_axis_count"), "v1.2 Holm flags")
    expect_equal(errors, validation_v12.get("bh_fdr_flagged_axes"), correction.get("bh_fdr_flagged_axis_count"), "v1.2 BH-FDR flags")
    expect_equal(errors, validation_v12.get("baseline_comparison_present"), correction.get("baseline_comparison_present"), "v1.2 baseline presence")
    expect_equal(errors, validation_v12.get("stylometry_baseline_axes"), baseline.get("axis_count"), "stylometry baseline axes")
    expect_equal(errors, validation_v12.get("framing"), "descriptive", "v1.2 framing")

    expect_equal(errors, external_gate.get("valid_reviews"), external_review.get("valid_review_count"), "external valid reviews")
    expect_equal(
        errors,
        external_gate.get("minimum_required_valid_reviews"),
        external_review.get("minimum_required_valid_reviews"),
        "minimum external review count",
    )
    expect_equal(
        errors,
        external_gate.get("independent_external_review_present"),
        external_review.get("independent_external_review_present"),
        "external review gate",
    )
    expect_equal(errors, external_gate.get("response_files"), external_review.get("response_file_count"), "external response files")

    guardrail = str(checks.get("guardrail", ""))
    if "descriptive" not in guardrail or "stronger attribution claim" not in guardrail:
        errors.append("guardrail text is missing expected descriptive/non-upgrade phrasing")

    if errors:
        print("Evidence visibility check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Evidence visibility check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
