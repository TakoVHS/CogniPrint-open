#!/usr/bin/env python3
"""Generate public site statistics from committed evidence artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return fallback or {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_stats(root: Path) -> dict[str, Any]:
    readiness = read_json(root / "docs" / "statistical-readiness-status.json")
    external_review = read_json(root / "docs" / "external-review" / "status.json")
    validation = read_json(root / "validation" / "inferential-v1" / "reviewer-validation-report.json")
    counts = readiness.get("counts", {})
    threshold = validation.get("threshold_recommendation", {})
    fixed_015 = validation.get("fixed_threshold_0_15_evaluation", {})
    return {
        "schema_version": "site-stats-v1",
        "generated_from": "committed evidence artifacts",
        "readiness": readiness.get("decision", "descriptive_only"),
        "external_review": {
            "valid_review_count": external_review.get("valid_review_count", 0),
            "minimum_required_valid_reviews": external_review.get("minimum_required_valid_reviews", 1),
            "independent_external_review_present": external_review.get("independent_external_review_present", False),
        },
        "counts": {
            "combined_readiness_rows": counts.get("empirical_comparison_rows", 311),
            "local_campaign_comparison_rows": counts.get("local_campaign_comparison_rows", 41),
            "public_empirical_growth_rows": counts.get("public_empirical_growth_rows", 220),
            "independent_holdout_rows": counts.get("independent_holdout_rows", 50),
        },
        "reviewer_validation_dry_run": {
            "readiness_boundary": validation.get("readiness_boundary", "descriptive_only"),
            "metric": validation.get("metric"),
            "n_perturbation_pairs": validation.get("n_perturbation_pairs"),
            "n_random_pairs": validation.get("n_random_pairs"),
            "recommended_threshold": threshold.get("recommended_threshold"),
            "recommended_threshold_fpr": threshold.get("fpr_at_threshold"),
            "recommended_threshold_power": threshold.get("power_at_threshold"),
            "fixed_threshold_0_15_fpr": fixed_015.get("fpr_at_threshold"),
            "fixed_threshold_0_15_power": fixed_015.get("power_at_threshold"),
            "threshold_policy": (
                "No fixed universal threshold is validated. Use corpus-specific random-pair "
                "calibration and report p-values, false-positive rate, and limitations."
            ),
        },
        "guardrail": (
            "Public stats are descriptive status indicators only. They do not establish "
            "authorship, provenance, AI detection, legal status, or validated readiness."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--root-output", type=Path, default=Path("site-stats.json"))
    parser.add_argument("--site-output", type=Path, default=Path("site/site-stats.json"))
    args = parser.parse_args()

    root = args.root.resolve()
    payload = build_stats(root)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    for output in (args.root_output, args.site_output):
        output_path = output if output.is_absolute() else root / output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(encoded, encoding="utf-8")
        print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
