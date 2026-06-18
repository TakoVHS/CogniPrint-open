#!/usr/bin/env python3
"""Generate validation v1.2 correction and baseline-comparison artifacts.

The v1.2 layer is deliberately conservative:

- multiple-comparison correction is applied to a fixed family of six shared
  benchmark/campaign perturbation-axis tests for Euclidean distance;
- the external-style baseline is a deterministic character n-gram stylometry
  baseline implemented with the Python standard library;
- outputs remain descriptive and do not upgrade project claims.
"""

from __future__ import annotations

import csv
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean, median
from typing import Any

from cogniprint.stats.bootstrap import bootstrap_mean_interval
from cogniprint.stats.validation import _build_benchmark_comparisons, _load_benchmark_rows, _load_campaign_rows


ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_ROOT = ROOT / "workspace" / "campaigns"
BENCHMARK_SAMPLES = ROOT / "datasets" / "public-benchmark-v1.1" / "metadata" / "sample-plan-template.csv"
WAVE005_DIR = ROOT / "validation" / "wave005-descriptive-validation"
V12_DIR = ROOT / "validation" / "statistical-validation-v1.2"
STYLO_DIR = ROOT / "validation" / "conventional-stylometry-baseline-v1"
NOTE_PATH = ROOT / "docs" / "validation-v1.2-results.md"
BASELINE_NOTE_PATH = ROOT / "docs" / "conventional-stylometry-baseline-results.md"

PRIMARY_METRIC = "euclidean_distance"
ALPHA = 0.05
PERMUTATION_RESAMPLES = 5000
PERMUTATION_SEED = 2605
RANDOM_BASELINE_DRAWS = 64
RANDOM_BASELINE_SEED = 2718
CHAR_NGRAM_RANGE = (3, 5)


def read_json(path: Path) -> dict[str, Any] | list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def metric_values(rows: list[dict[str, Any]], axis: str, metric: str) -> list[float]:
    return [float(row[metric]) for row in rows if row["axis"] == axis]


def permutation_p_value(left: list[float], right: list[float], *, seed: int, resamples: int) -> dict[str, Any]:
    if not left or not right:
        return {
            "raw_p_value": None,
            "reported_p_value": None,
            "exceedance_count": 0,
            "resamples": resamples,
            "reporting_note": "insufficient data",
        }
    rng = random.Random(seed)
    observed = abs(fmean(left) - fmean(right))
    combined = left + right
    left_size = len(left)
    exceed = 0
    for _ in range(resamples):
        shuffled = combined[:]
        rng.shuffle(shuffled)
        perm_left = shuffled[:left_size]
        perm_right = shuffled[left_size:]
        statistic = abs(fmean(perm_left) - fmean(perm_right))
        if statistic >= observed:
            exceed += 1
    raw = exceed / resamples
    floor = 1.0 / resamples
    reported = max(raw, floor)
    return {
        "observed_abs_mean_difference": round(observed, 6),
        "raw_p_value": round(raw, 6),
        "reported_p_value": round(reported, 6),
        "exceedance_count": exceed,
        "resamples": resamples,
        "reporting_note": (
            "reported_p_value uses a finite-resample floor of 1/resamples when no permutation draw "
            "matches or exceeds the observed statistic"
        ),
    }


def holm_adjust(rows: list[dict[str, Any]], p_key: str = "reported_p_value") -> dict[str, float]:
    sorted_rows = sorted(rows, key=lambda row: (float(row[p_key]), row["axis"]))
    m = len(sorted_rows)
    adjusted: dict[str, float] = {}
    running_max = 0.0
    for rank, row in enumerate(sorted_rows, start=1):
        value = min(1.0, (m - rank + 1) * float(row[p_key]))
        running_max = max(running_max, value)
        adjusted[row["axis"]] = round(running_max, 6)
    return adjusted


def benjamini_hochberg_adjust(rows: list[dict[str, Any]], p_key: str = "reported_p_value") -> dict[str, float]:
    sorted_rows = sorted(rows, key=lambda row: (float(row[p_key]), row["axis"]))
    m = len(sorted_rows)
    adjusted: dict[str, float] = {}
    running_min = 1.0
    for rank, row in reversed(list(enumerate(sorted_rows, start=1))):
        value = min(1.0, float(row[p_key]) * m / rank)
        running_min = min(running_min, value)
        adjusted[row["axis"]] = round(running_min, 6)
    return adjusted


def generate_multiple_comparison_layer() -> dict[str, Any]:
    campaign_rows = _load_campaign_rows(CAMPAIGN_ROOT)
    benchmark_rows = _load_benchmark_rows(BENCHMARK_SAMPLES)
    benchmark_comparisons = _build_benchmark_comparisons(BENCHMARK_SAMPLES, benchmark_rows)
    shared_axes = sorted({row["axis"] for row in campaign_rows} & {row["axis"] for row in benchmark_comparisons})
    correction_rows: list[dict[str, Any]] = []
    for index, axis in enumerate(shared_axes):
        campaign_values = metric_values(campaign_rows, axis, PRIMARY_METRIC)
        benchmark_values = metric_values(benchmark_comparisons, axis, PRIMARY_METRIC)
        permutation = permutation_p_value(
            campaign_values,
            benchmark_values,
            seed=PERMUTATION_SEED + index,
            resamples=PERMUTATION_RESAMPLES,
        )
        correction_rows.append(
            {
                "axis": axis,
                "metric": PRIMARY_METRIC,
                "campaign_count": len(campaign_values),
                "benchmark_count": len(benchmark_values),
                "campaign_mean": round(fmean(campaign_values), 6),
                "benchmark_mean": round(fmean(benchmark_values), 6),
                "mean_difference_campaign_minus_benchmark": round(fmean(campaign_values) - fmean(benchmark_values), 6),
                **permutation,
            }
        )
    holm = holm_adjust(correction_rows)
    bh = benjamini_hochberg_adjust(correction_rows)
    for row in correction_rows:
        row["holm_adjusted_p_value"] = holm[row["axis"]]
        row["bh_fdr_q_value"] = bh[row["axis"]]
        row["holm_flag_at_0_05"] = row["holm_adjusted_p_value"] <= ALPHA
        row["bh_fdr_flag_at_0_05"] = row["bh_fdr_q_value"] <= ALPHA
    payload = {
        "snapshot_id": "statistical-validation-v1.2",
        "status": "descriptive multiple-comparison correction layer",
        "test_family": "shared benchmark/campaign perturbation axes",
        "primary_metric": PRIMARY_METRIC,
        "alpha": ALPHA,
        "p_value_method": "two-sided permutation test for axis-level mean difference",
        "correction_methods": ["Holm-Bonferroni family-wise correction", "Benjamini-Hochberg false-discovery-rate correction"],
        "resamples": PERMUTATION_RESAMPLES,
        "seed": PERMUTATION_SEED,
        "test_count": len(correction_rows),
        "rows": correction_rows,
        "guardrail": (
            "Correction flags are diagnostic only. Small campaign-side per-axis counts keep this layer descriptive."
        ),
    }
    write_json(V12_DIR / "multiple-comparison-correction.json", payload)
    write_csv(
        V12_DIR / "multiple-comparison-correction.csv",
        correction_rows,
        [
            "axis",
            "metric",
            "campaign_count",
            "benchmark_count",
            "campaign_mean",
            "benchmark_mean",
            "mean_difference_campaign_minus_benchmark",
            "observed_abs_mean_difference",
            "raw_p_value",
            "reported_p_value",
            "holm_adjusted_p_value",
            "bh_fdr_q_value",
            "holm_flag_at_0_05",
            "bh_fdr_flag_at_0_05",
        ],
    )
    return payload


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def char_ngram_profile(text: str, n_min: int = CHAR_NGRAM_RANGE[0], n_max: int = CHAR_NGRAM_RANGE[1]) -> Counter[str]:
    normalized = f" {normalize_text(text)} "
    counts: Counter[str] = Counter()
    for n in range(n_min, n_max + 1):
        if len(normalized) < n:
            continue
        for index in range(0, len(normalized) - n + 1):
            counts[normalized[index : index + n]] += 1
    return counts


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    overlap = set(left) & set(right)
    dot = sum(left[key] * right[key] for key in overlap)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def metric_summary(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": round(fmean(values), 6),
        "median": round(float(median(values)), 6),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
    }


def load_released_benchmark_rows() -> list[dict[str, str]]:
    rows = _load_benchmark_rows(BENCHMARK_SAMPLES)
    return [row for row in rows if row.get("release_status") == "released"]


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (ROOT / path).resolve()


def build_stylometry_comparisons(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    baseline_rows = {row["sample_id"]: row for row in rows if row["relation_type"] == "baseline"}
    profiles = {
        row["sample_id"]: char_ngram_profile(resolve_repo_path(row["file_path"]).read_text(encoding="utf-8"))
        for row in rows
    }
    comparisons = []
    for row in rows:
        if row["relation_type"] == "baseline":
            continue
        baseline_id = row["baseline_sample_id"]
        baseline = baseline_rows[baseline_id]
        similarity = cosine_similarity(profiles[baseline_id], profiles[row["sample_id"]])
        comparisons.append(
            {
                "baseline_sample_id": baseline_id,
                "variant_sample_id": row["sample_id"],
                "axis": row["relation_type"],
                "language": baseline["language"],
                "source_domain": baseline["source_domain"],
                "char_ngram_cosine_similarity": round(similarity, 6),
                "char_ngram_cosine_distance": round(1.0 - similarity, 6),
            }
        )
    return comparisons


def axis_summary(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_axis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in comparisons:
        by_axis[row["axis"]].append(row)
    rows = []
    for axis, axis_rows in sorted(by_axis.items()):
        distances = [row["char_ngram_cosine_distance"] for row in axis_rows]
        similarities = [row["char_ngram_cosine_similarity"] for row in axis_rows]
        rows.append(
            {
                "axis": axis,
                "row_count": len(axis_rows),
                "mean_char_ngram_cosine_similarity": round(fmean(similarities), 6),
                "mean_char_ngram_cosine_distance": round(fmean(distances), 6),
                "distance_bootstrap": bootstrap_mean_interval(distances),
            }
        )
    return rows


def stylometry_random_baseline(rows: list[dict[str, str]], *, draws: int = RANDOM_BASELINE_DRAWS, seed: int = RANDOM_BASELINE_SEED) -> dict[str, Any]:
    baseline_rows = [row for row in rows if row["relation_type"] == "baseline"]
    variant_rows = [row for row in rows if row["relation_type"] != "baseline"]
    baseline_profiles = {
        row["sample_id"]: char_ngram_profile(resolve_repo_path(row["file_path"]).read_text(encoding="utf-8"))
        for row in baseline_rows
    }
    variant_profiles = {
        row["sample_id"]: char_ngram_profile(resolve_repo_path(row["file_path"]).read_text(encoding="utf-8"))
        for row in variant_rows
    }
    baseline_ids = [row["sample_id"] for row in baseline_rows]
    draw_means = []
    pooled_distances = []
    pair_count_per_draw = 0
    for draw_index in range(draws):
        rng = random.Random(seed + draw_index)
        draw_distances = []
        for row in variant_rows:
            foreign_ids = [sample_id for sample_id in baseline_ids if sample_id != row["baseline_sample_id"]]
            foreign_id = rng.choice(foreign_ids)
            similarity = cosine_similarity(variant_profiles[row["sample_id"]], baseline_profiles[foreign_id])
            distance = 1.0 - similarity
            draw_distances.append(distance)
            pooled_distances.append(distance)
        pair_count_per_draw = len(draw_distances)
        draw_means.append(fmean(draw_distances))
    return {
        "mode": "repeatable character-ngram cross-baseline reference distribution",
        "seed": seed,
        "draw_count": len(draw_means),
        "pair_count_per_draw": pair_count_per_draw,
        "total_pairs": len(pooled_distances),
        "char_ngram_cosine_distance": {
            "pooled_summary": metric_summary(pooled_distances),
            "draw_mean_summary": metric_summary(draw_means),
            "draw_mean_bootstrap": bootstrap_mean_interval(draw_means),
        },
    }


def average_ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    index = 0
    while index < len(indexed):
        end = index + 1
        while end < len(indexed) and indexed[end][1] == indexed[index][1]:
            end += 1
        rank = (index + 1 + end) / 2.0
        for original_index, _value in indexed[index:end]:
            ranks[original_index] = rank
        index = end
    return ranks


def pearson_correlation(left: list[float], right: list[float]) -> float | None:
    if len(left) != len(right) or len(left) < 2:
        return None
    left_mean = fmean(left)
    right_mean = fmean(right)
    numerator = sum((lhs - left_mean) * (rhs - right_mean) for lhs, rhs in zip(left, right))
    left_denominator = math.sqrt(sum((lhs - left_mean) ** 2 for lhs in left))
    right_denominator = math.sqrt(sum((rhs - right_mean) ** 2 for rhs in right))
    if left_denominator == 0.0 or right_denominator == 0.0:
        return None
    return numerator / (left_denominator * right_denominator)


def spearman_correlation(left: list[float], right: list[float]) -> float | None:
    return pearson_correlation(average_ranks(left), average_ranks(right))


def stylometry_cogniprint_bridge(stylometry_axis_rows: list[dict[str, Any]]) -> dict[str, Any]:
    cogniprint_axis_rows = read_json(WAVE005_DIR / "benchmark-axis-summary.json")
    assert isinstance(cogniprint_axis_rows, list)
    cogniprint_by_axis = {row["axis"]: row for row in cogniprint_axis_rows}
    stylo_by_axis = {row["axis"]: row for row in stylometry_axis_rows}
    shared_axes = sorted(set(cogniprint_by_axis) & set(stylo_by_axis))
    rows = []
    cogniprint_values = []
    stylometry_values = []
    for axis in shared_axes:
        cog_value = float(cogniprint_by_axis[axis]["mean_euclidean_distance"])
        stylo_value = float(stylo_by_axis[axis]["mean_char_ngram_cosine_distance"])
        cogniprint_values.append(cog_value)
        stylometry_values.append(stylo_value)
        rows.append(
            {
                "axis": axis,
                "cogniprint_mean_euclidean_distance": round(cog_value, 6),
                "stylometry_mean_char_ngram_distance": round(stylo_value, 6),
            }
        )
    spearman = spearman_correlation(cogniprint_values, stylometry_values)
    pearson = pearson_correlation(cogniprint_values, stylometry_values)
    return {
        "shared_axis_count": len(shared_axes),
        "rows": rows,
        "spearman_axis_rank_correlation": round(spearman, 6) if spearman is not None else None,
        "pearson_axis_mean_correlation": round(pearson, 6) if pearson is not None else None,
        "guardrail": "CogniPrint and character n-gram distances are on different scales; only axis-level pattern comparison is reported.",
    }


def generate_stylometry_baseline() -> dict[str, Any]:
    rows = load_released_benchmark_rows()
    comparisons = build_stylometry_comparisons(rows)
    axis_rows = axis_summary(comparisons)
    random_baseline = stylometry_random_baseline(rows)
    bridge = stylometry_cogniprint_bridge(axis_rows)
    baseline_rows = [row for row in rows if row["relation_type"] == "baseline"]
    variant_rows = [row for row in rows if row["relation_type"] != "baseline"]
    manifest = {
        "snapshot_id": "conventional-stylometry-baseline-v1",
        "status": "deterministic character-ngram stylometry baseline comparison",
        "method": "character n-gram TF cosine similarity",
        "ngram_range": list(CHAR_NGRAM_RANGE),
        "benchmark_baseline_count": len(baseline_rows),
        "benchmark_variant_count": len(variant_rows),
        "guardrail": "This is a comparison baseline, not a replacement for external validation.",
    }
    counts = {
        "snapshot_id": "conventional-stylometry-baseline-v1",
        "baseline_count": len(baseline_rows),
        "variant_count": len(variant_rows),
        "axis_count": len(axis_rows),
        "language_count": len({row["language"] for row in baseline_rows}),
    }
    write_json(STYLO_DIR / "manifest.json", manifest)
    write_json(STYLO_DIR / "counts.json", counts)
    write_json(STYLO_DIR / "axis-summary.json", axis_rows)
    write_json(STYLO_DIR / "random-baseline-summary.json", random_baseline)
    write_json(STYLO_DIR / "cogniprint-bridge.json", bridge)
    write_csv(
        STYLO_DIR / "axis-summary.csv",
        axis_rows,
        [
            "axis",
            "row_count",
            "mean_char_ngram_cosine_similarity",
            "mean_char_ngram_cosine_distance",
        ],
    )
    write_csv(
        STYLO_DIR / "cogniprint-bridge.csv",
        bridge["rows"],
        ["axis", "cogniprint_mean_euclidean_distance", "stylometry_mean_char_ngram_distance"],
    )
    write_csv(
        STYLO_DIR / "comparison-rows.csv",
        comparisons,
        [
            "baseline_sample_id",
            "variant_sample_id",
            "axis",
            "language",
            "source_domain",
            "char_ngram_cosine_similarity",
            "char_ngram_cosine_distance",
        ],
    )
    write_stylometry_markdown(manifest, counts, axis_rows, random_baseline, bridge)
    return {"manifest": manifest, "counts": counts, "bridge": bridge}


def write_stylometry_markdown(
    manifest: dict[str, Any],
    counts: dict[str, Any],
    axis_rows: list[dict[str, Any]],
    random_baseline: dict[str, Any],
    bridge: dict[str, Any],
) -> None:
    strongest = max(axis_rows, key=lambda row: row["mean_char_ngram_cosine_distance"])
    mildest = min(axis_rows, key=lambda row: row["mean_char_ngram_cosine_distance"])
    readme = [
        "# Conventional Stylometry Baseline v1",
        "",
        "This directory records a deterministic character n-gram stylometry baseline for the public benchmark v1.1 layer.",
        "",
        f"- method: `{manifest['method']}`",
        f"- baselines: `{counts['baseline_count']}`",
        f"- variants: `{counts['variant_count']}`",
        f"- axes: `{counts['axis_count']}`",
        "",
        "The baseline is intentionally lightweight and dependency-free. It is used as a reference comparison, not as a competing claim system.",
        "",
    ]
    (STYLO_DIR / "README.md").write_text("\n".join(readme), encoding="utf-8")
    methods = [
        "# Conventional Stylometry Baseline Methods",
        "",
        "The baseline lowercases text, builds character n-gram term-frequency profiles, and reports cosine distance between each baseline excerpt and its controlled variants.",
        "",
        f"Character n-gram range: `{CHAR_NGRAM_RANGE[0]}` to `{CHAR_NGRAM_RANGE[1]}`.",
        "",
        "Axis-level means are compared against CogniPrint benchmark axis means only as pattern summaries because the metrics use different scales.",
        "",
    ]
    (STYLO_DIR / "methods-summary.md").write_text("\n".join(methods), encoding="utf-8")
    results = [
        "# Conventional Stylometry Baseline Results",
        "",
        f"- largest mean character n-gram distance axis: `{strongest['axis']}` at `{strongest['mean_char_ngram_cosine_distance']}`",
        f"- smallest mean character n-gram distance axis: `{mildest['axis']}` at `{mildest['mean_char_ngram_cosine_distance']}`",
        f"- random baseline draw-mean distance: `{random_baseline['char_ngram_cosine_distance']['draw_mean_summary']['mean']}`",
        f"- Spearman axis-rank correlation with CogniPrint benchmark means: `{bridge['spearman_axis_rank_correlation']}`",
        "",
        "These are descriptive baseline-comparison values.",
        "",
    ]
    (STYLO_DIR / "results-summary.md").write_text("\n".join(results), encoding="utf-8")
    limitations = [
        "# Conventional Stylometry Baseline Limitations",
        "",
        "- character n-gram distances are not on the same scale as CogniPrint distances;",
        "- the comparison uses the controlled public benchmark, not a fully independent external corpus;",
        "- multilingual excerpts make simple character n-gram interpretation uneven across scripts;",
        "- this baseline is useful for sanity checking, not for general-purpose evaluation claims.",
        "",
    ]
    (STYLO_DIR / "limitations-summary.md").write_text("\n".join(limitations), encoding="utf-8")
    note = [
        "# Conventional Stylometry Baseline Results",
        "",
        "A dependency-free character n-gram stylometry baseline has been added as a first comparison point.",
        "",
        f"- benchmark baselines: `{counts['baseline_count']}`",
        f"- benchmark variants: `{counts['variant_count']}`",
        f"- random baseline draw-mean distance: `{random_baseline['char_ngram_cosine_distance']['draw_mean_summary']['mean']}`",
        f"- Spearman axis-rank correlation with CogniPrint benchmark means: `{bridge['spearman_axis_rank_correlation']}`",
        "",
        "Interpretation: this is a sanity-check baseline. The next stronger comparison should use either a larger conventional stylometry toolkit or a frozen embedding model under a separate preregistered protocol.",
        "",
    ]
    BASELINE_NOTE_PATH.write_text("\n".join(note), encoding="utf-8")


def write_v12_summaries(correction: dict[str, Any], stylometry: dict[str, Any]) -> None:
    counts = read_json(WAVE005_DIR / "counts.json")
    assert isinstance(counts, dict)
    flagged_holm = [row for row in correction["rows"] if row["holm_flag_at_0_05"]]
    flagged_bh = [row for row in correction["rows"] if row["bh_fdr_flag_at_0_05"]]
    manifest = {
        "snapshot_id": "statistical-validation-v1.2",
        "status": "descriptive correction and baseline-comparison layer",
        "depends_on": "validation/wave005-descriptive-validation",
        "multiple_comparison_correction": "validation/statistical-validation-v1.2/multiple-comparison-correction.json",
        "baseline_comparison": "validation/conventional-stylometry-baseline-v1",
        "decision": "descriptive_only",
        "guardrail": "v1.2 adds correction and one baseline comparison, but it does not resolve small empirical row counts.",
    }
    v12_counts = {
        "snapshot_id": "statistical-validation-v1.2",
        "empirical_comparison_rows": counts["empirical_comparison_row_count"],
        "benchmark_baselines": counts["benchmark_baseline_count"],
        "benchmark_variants": counts["benchmark_variant_count"],
        "correction_test_count": correction["test_count"],
        "holm_flagged_axis_count": len(flagged_holm),
        "bh_fdr_flagged_axis_count": len(flagged_bh),
        "baseline_comparison_present": True,
    }
    write_json(V12_DIR / "manifest.json", manifest)
    write_json(V12_DIR / "counts.json", v12_counts)
    methods = [
        "# Statistical Validation v1.2 Methods Summary",
        "",
        "v1.2 adds two conservative checks on top of the wave-005 descriptive validation layer:",
        "",
        "- fixed-family multiple-comparison correction across shared perturbation axes;",
        "- one deterministic conventional stylometry baseline based on character n-gram cosine distance.",
        "",
        "The correction family uses Euclidean distance as the primary metric for six shared benchmark/campaign axes.",
        "Both Holm-Bonferroni and Benjamini-Hochberg adjusted values are reported.",
        "",
        "No claim wording is upgraded by this layer.",
        "",
    ]
    (V12_DIR / "methods-summary.md").write_text("\n".join(methods), encoding="utf-8")
    results = [
        "# Statistical Validation v1.2 Results Summary",
        "",
        f"- correction tests: `{correction['test_count']}`",
        f"- Holm-flagged axes at alpha 0.05: `{len(flagged_holm)}`",
        f"- BH-FDR-flagged axes at alpha 0.05: `{len(flagged_bh)}`",
        f"- baseline comparison: `{stylometry['manifest']['method']}`",
        f"- baseline Spearman axis-rank correlation: `{stylometry['bridge']['spearman_axis_rank_correlation']}`",
        "",
        "These outputs improve auditability but keep the readiness decision at `descriptive_only`.",
        "",
    ]
    (V12_DIR / "results-summary.md").write_text("\n".join(results), encoding="utf-8")
    limitations = [
        "# Statistical Validation v1.2 Limitations Summary",
        "",
        "- empirical campaign rows remain below the 200-row readiness gate;",
        "- campaign-side per-axis counts remain small;",
        "- correction is applied to a fixed diagnostic family, not a full inferential study design;",
        "- the stylometry baseline is lightweight and should be followed by an independent external baseline.",
        "",
    ]
    (V12_DIR / "limitations-summary.md").write_text("\n".join(limitations), encoding="utf-8")
    note = [
        "# Validation v1.2 Results",
        "",
        "Status: `descriptive_only`.",
        "",
        "v1.2 adds multiple-comparison correction and one conventional stylometry baseline comparison.",
        "",
        f"- correction tests: `{correction['test_count']}`",
        f"- Holm-flagged axes at alpha 0.05: `{len(flagged_holm)}`",
        f"- BH-FDR-flagged axes at alpha 0.05: `{len(flagged_bh)}`",
        f"- conventional baseline: `{stylometry['manifest']['method']}`",
        f"- baseline Spearman axis-rank correlation: `{stylometry['bridge']['spearman_axis_rank_correlation']}`",
        "",
        "Remaining blockers: empirical rows below 200 and small campaign-side per-axis counts.",
        "",
    ]
    NOTE_PATH.write_text("\n".join(note), encoding="utf-8")


def main() -> int:
    if not WAVE005_DIR.exists():
        raise SystemExit("Missing validation/wave005-descriptive-validation. Run make wave005-results first.")
    correction = generate_multiple_comparison_layer()
    stylometry = generate_stylometry_baseline()
    write_v12_summaries(correction, stylometry)
    print(f"Validation v1.2 artifacts written: {V12_DIR.relative_to(ROOT)}")
    print(f"Stylometry baseline artifacts written: {STYLO_DIR.relative_to(ROOT)}")
    print("Decision: descriptive_only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
