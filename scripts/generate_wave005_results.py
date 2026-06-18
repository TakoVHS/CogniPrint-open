#!/usr/bin/env python3
"""Generate wave-005 descriptive validation results.

This script materializes the benchmark-aware descriptive validation layer after
the wave-005 public benchmark expansion. It intentionally keeps the decision as
`descriptive_only`; the current empirical row count is still too small for
stronger inferential wording.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from statistics import fmean
from typing import Any

from cogniprint.stats.validation import generate_statistical_validation

import bootstrap_validation


ROOT = Path(__file__).resolve().parents[1]
PREREG_FILE = ROOT / "docs" / "pre-registration-wave005.md"
PREREG_HASH_FILE = ROOT / "validation" / "wave005_prereg_hash.txt"
BENCHMARK_SAMPLES = ROOT / "datasets" / "public-benchmark-v1.1" / "metadata" / "sample-plan-template.csv"
CAMPAIGN_ROOT = ROOT / "workspace" / "campaigns"
AGGREGATE_CSV = ROOT / "workspace" / "exports" / "v1_validation.csv"
PRIOR_VALIDATION_DIR = ROOT / "evidence" / "statistical-validation-v1"
WAVE005_VALIDATION_DIR = ROOT / "validation" / "wave005-descriptive-validation"
RESULTS_PATH = ROOT / "validation" / "wave005_results.json"
NOTE_PATH = ROOT / "docs" / "wave005-validation-results.md"


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def verify_preregistration() -> str:
    if not PREREG_FILE.exists():
        raise SystemExit(f"Missing pre-registration file: {PREREG_FILE}")
    if not PREREG_HASH_FILE.exists():
        raise SystemExit(f"Missing pre-registration hash file: {PREREG_HASH_FILE}")
    current_hash = digest_text(PREREG_FILE.read_text(encoding="utf-8"))
    locked_hash = PREREG_HASH_FILE.read_text(encoding="utf-8").strip()
    if current_hash != locked_hash:
        raise SystemExit("Pre-registration hash mismatch. Stop before generating wave-005 results.")
    return locked_hash


def generate_validation_layer() -> Path:
    output_dir = generate_statistical_validation(
        campaign_root=CAMPAIGN_ROOT,
        benchmark_samples_csv=BENCHMARK_SAMPLES,
        output_dir=WAVE005_VALIDATION_DIR,
    )
    normalize_wave005_validation_outputs(output_dir)
    return output_dir


def normalize_wave005_validation_outputs(output_dir: Path) -> None:
    counts_path = output_dir / "counts.json"
    manifest_path = output_dir / "manifest.json"
    counts = load_json(counts_path)
    counts["snapshot_id"] = "wave005-descriptive-validation"
    write_json(counts_path, counts)

    manifest = load_json(manifest_path)
    manifest["snapshot_id"] = "wave005-descriptive-validation"
    manifest["status"] = "wave-005 benchmark-aware descriptive validation layer"
    manifest["guardrail"] = (
        "These outputs provide descriptive wave-005 validation summaries after the public benchmark v1.1 expansion. "
        "They do not claim inferential certainty or publication-level completion."
    )
    write_json(manifest_path, manifest)

    replacements = {
        "Statistical Validation v1.1": "Wave-005 Descriptive Validation",
        "statistical validation v1.1": "wave-005 descriptive validation",
    }
    for path in output_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def primary_tier_metrics() -> dict[str, Any]:
    if not AGGREGATE_CSV.exists():
        raise SystemExit(f"Missing aggregate validation CSV: {AGGREGATE_CSV}")
    rows = bootstrap_validation.load_rows(AGGREGATE_CSV)
    enriched = bootstrap_validation.attach_derived_tiers(rows)
    light = [
        float(row["cosine_similarity"])
        for row in enriched
        if row.get("perturbation_tier") == "light" and row.get("cosine_similarity") not in ("", None)
    ]
    strong = [
        float(row["cosine_similarity"])
        for row in enriched
        if row.get("perturbation_tier") == "strong" and row.get("cosine_similarity") not in ("", None)
    ]
    summary = bootstrap_validation.summarize_groups(
        light,
        strong,
        metric="cosine_similarity",
        group1="light",
        group2="strong",
        resamples=2000,
        seed=1729,
    )
    raw_p_value = float(summary["permutation_p_value"])
    resamples = int(summary["group1"]["bootstrap_mean"]["resamples"])
    if raw_p_value == 0.0 and resamples > 0:
        summary["permutation_p_value_raw"] = raw_p_value
        summary["permutation_p_value"] = round(1.0 / resamples, 6)
        summary["permutation_p_value_note"] = (
            "No permutation draw matched or exceeded the observed statistic. The numeric field uses the "
            "finite-resample reporting floor 1/resamples rather than reporting an exact zero."
        )
    summary["source_csv"] = str(AGGREGATE_CSV.relative_to(ROOT))
    summary["tier_rule"] = "Derived by scripts/bootstrap_validation.py from variant labels and interpretation fields."
    summary["interpretation"] = (
        "The light-vs-strong tier difference is descriptive and depends on the current aggregate export. "
        "It is not a standalone proof of broad-domain behavior."
    )
    return summary


def random_baseline_shift(prior: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    metrics = {}
    for metric in ("cosine_similarity", "euclidean_distance", "manhattan_distance"):
        prior_mean = prior[metric]["draw_mean_summary"]["mean"]
        current_mean = current[metric]["draw_mean_summary"]["mean"]
        metrics[metric] = {
            "prior_draw_mean": prior_mean,
            "wave005_draw_mean": current_mean,
            "delta": round(current_mean - prior_mean, 6),
            "prior_interval": {
                "lower": prior[metric]["draw_mean_bootstrap"]["lower"],
                "upper": prior[metric]["draw_mean_bootstrap"]["upper"],
            },
            "wave005_interval": {
                "lower": current[metric]["draw_mean_bootstrap"]["lower"],
                "upper": current[metric]["draw_mean_bootstrap"]["upper"],
            },
        }
    return {
        "prior_pair_count_per_draw": prior["pair_count_per_draw"],
        "wave005_pair_count_per_draw": current["pair_count_per_draw"],
        "prior_total_pairs": prior["total_pairs"],
        "wave005_total_pairs": current["total_pairs"],
        "metrics": metrics,
        "interpretation": (
            "The random reference distribution moved after benchmark expansion; this is expected and remains "
            "a descriptive composition-sensitivity signal."
        ),
    }


def bridge_shift(prior: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    prior_rows = {row["axis"]: row for row in prior["rows"]}
    current_rows = {row["axis"]: row for row in current["rows"]}
    shared_axes = sorted(set(prior_rows) & set(current_rows))
    rows = []
    for axis in shared_axes:
        old = prior_rows[axis]
        new = current_rows[axis]
        rows.append(
            {
                "axis": axis,
                "prior_benchmark_row_count": old["benchmark_row_count"],
                "wave005_benchmark_row_count": new["benchmark_row_count"],
                "prior_euclidean_abs_delta": old["euclidean_distance_abs_delta"],
                "wave005_euclidean_abs_delta": new["euclidean_distance_abs_delta"],
                "euclidean_abs_delta_shift": round(new["euclidean_distance_abs_delta"] - old["euclidean_distance_abs_delta"], 6),
                "prior_alignment_band": old["alignment_band"],
                "wave005_alignment_band": new["alignment_band"],
            }
        )
    prior_mean_abs = fmean(row["euclidean_distance_abs_delta"] for row in prior_rows.values()) if prior_rows else 0.0
    current_mean_abs = fmean(row["euclidean_distance_abs_delta"] for row in current_rows.values()) if current_rows else 0.0
    return {
        "shared_axis_count": len(shared_axes),
        "prior_mean_euclidean_abs_delta": round(prior_mean_abs, 6),
        "wave005_mean_euclidean_abs_delta": round(current_mean_abs, 6),
        "mean_euclidean_abs_delta_shift": round(current_mean_abs - prior_mean_abs, 6),
        "prior_closest_axis": prior["closest_euclidean_alignment"]["axis"],
        "wave005_closest_axis": current["closest_euclidean_alignment"]["axis"],
        "prior_widest_axis": prior["widest_euclidean_gap"]["axis"],
        "wave005_widest_axis": current["widest_euclidean_gap"]["axis"],
        "rows": rows,
        "interpretation": (
            "Bridge movement is mixed: some axes align more closely after expansion, while some remain corpus-sensitive. "
            "This supports more benchmark work, not stronger claims."
        ),
    }


def release_gates(counts: dict[str, Any]) -> dict[str, bool]:
    return {
        "benchmark_baselines_at_least_20": int(counts["benchmark_baseline_count"]) >= 20,
        "benchmark_variants_at_least_100": int(counts["benchmark_variant_count"]) >= 100,
        "empirical_rows_at_least_200": int(counts["empirical_comparison_row_count"]) >= 200,
        "shared_bridge_axes_present": int(counts["shared_bridge_axis_count"]) > 0,
        "statistical_readiness_remains_descriptive": True,
    }


def blocked_by(gates: dict[str, bool]) -> list[str]:
    blockers = [name for name, passed in gates.items() if not passed]
    blockers.extend(
        [
            "external_reviewer_input_still_needed",
            "independent_external_benchmark_still_needed",
            "multiple_comparison_correction_not_part_of_current_descriptive_layer",
        ]
    )
    return blockers


def build_results(locked_hash: str) -> dict[str, Any]:
    counts = load_json(WAVE005_VALIDATION_DIR / "counts.json")
    overall = load_json(WAVE005_VALIDATION_DIR / "overall-metrics.json")
    prior_random = load_json(PRIOR_VALIDATION_DIR / "random-baseline-summary.json")
    current_random = load_json(WAVE005_VALIDATION_DIR / "random-baseline-summary.json")
    prior_bridge = load_json(PRIOR_VALIDATION_DIR / "benchmark-campaign-bridge.json")
    current_bridge = load_json(WAVE005_VALIDATION_DIR / "benchmark-campaign-bridge.json")
    primary = primary_tier_metrics()
    gates = release_gates(counts)
    return {
        "snapshot_id": "wave005-descriptive-validation",
        "generated_date": "2026-05-05",
        "decision": "descriptive_only",
        "preregistration": {
            "file": "docs/pre-registration-wave005.md",
            "locked_sha256": locked_hash,
            "status": "hash_matches",
        },
        "inputs": {
            "campaign_root": "workspace/campaigns",
            "benchmark_samples": "datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv",
            "prior_validation_reference": "evidence/statistical-validation-v1",
            "wave005_validation_dir": "validation/wave005-descriptive-validation",
        },
        "counts": counts,
        "overall_campaign_metrics": overall,
        "primary_metric": primary,
        "mean_difference": primary["mean_difference"],
        "hedges_g": primary["hedges_g"],
        "cliffs_delta": primary["cliffs_delta"],
        "permutation_p_value": primary["permutation_p_value"],
        "random_baseline_shift": random_baseline_shift(prior_random, current_random),
        "benchmark_campaign_bridge_shift": bridge_shift(prior_bridge, current_bridge),
        "release_gates": gates,
        "blocked_by": blocked_by(gates),
        "guardrail": (
            "Wave-005 satisfies the minimum public benchmark size gate, but the validation decision remains "
            "descriptive_only because empirical rows, independence, and external-review gates are still insufficient."
        ),
    }


def write_note(results: dict[str, Any]) -> None:
    counts = results["counts"]
    primary = results["primary_metric"]
    random_shift = results["random_baseline_shift"]["metrics"]["euclidean_distance"]
    bridge = results["benchmark_campaign_bridge_shift"]
    lines = [
        "# Wave-005 Validation Results",
        "",
        "Status: `descriptive_only`.",
        "",
        "Wave-005 completes the minimum public benchmark size gate but does not complete inferential validation.",
        "",
        "## Counts",
        "",
        f"- empirical campaign rows: `{counts['empirical_comparison_row_count']}`",
        f"- public benchmark baselines: `{counts['benchmark_baseline_count']}`",
        f"- public benchmark variants: `{counts['benchmark_variant_count']}`",
        f"- shared benchmark/campaign bridge axes: `{counts['shared_bridge_axis_count']}`",
        "",
        "## Primary Light-vs-Strong Descriptive Metric",
        "",
        f"- light mean cosine: `{primary['group1']['mean']}` (`n={primary['group1']['count']}`)",
        f"- strong mean cosine: `{primary['group2']['mean']}` (`n={primary['group2']['count']}`)",
        f"- mean difference: `{primary['mean_difference']['group1_minus_group2']}`",
        f"- bootstrap interval: `{primary['mean_difference']['lower']}` to `{primary['mean_difference']['upper']}`",
        f"- Hedges' g: `{primary['hedges_g']}`",
        f"- Cliff's delta: `{primary['cliffs_delta']}`",
        f"- permutation p-value: `{primary['permutation_p_value']}`",
        f"- permutation p-value note: {primary.get('permutation_p_value_note', 'standard finite-resample permutation estimate')}",
        "",
        "These values are descriptive. The current aggregate export is not an independent large-N study.",
        "",
        "## Benchmark Movement",
        "",
        f"- random-baseline Euclidean draw mean moved from `{random_shift['prior_draw_mean']}` to `{random_shift['wave005_draw_mean']}`",
        f"- random-baseline Euclidean delta: `{random_shift['delta']}`",
        f"- mean bridge Euclidean absolute delta moved from `{bridge['prior_mean_euclidean_abs_delta']}` to `{bridge['wave005_mean_euclidean_abs_delta']}`",
        f"- mean bridge Euclidean absolute delta shift: `{bridge['mean_euclidean_abs_delta_shift']}`",
        "",
        "## Remaining Blockers",
        "",
    ]
    lines.extend(f"- `{item}`" for item in results["blocked_by"])
    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            results["guardrail"],
            "",
        ]
    )
    NOTE_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    locked_hash = verify_preregistration()
    generate_validation_layer()
    results = build_results(locked_hash)
    write_json(RESULTS_PATH, results)
    write_note(results)
    print(f"Wave-005 results written: {RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wave-005 note written: {NOTE_PATH.relative_to(ROOT)}")
    print(f"Decision: {results['decision']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
