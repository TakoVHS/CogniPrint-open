#!/usr/bin/env python3
"""Exploratory bootstrap validation for aggregate CogniPrint study CSV exports."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path
from statistics import fmean, median

from cogniprint.stats.bootstrap import bootstrap_mean_interval


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, type=Path, help="Aggregate CSV produced by `cogniprint report --aggregate`.")
    parser.add_argument("--group-col", default="perturbation_tier", help="Grouping column. Defaults to a derived tier if missing.")
    parser.add_argument("--value-col", default="cosine_similarity", help="Metric column to compare.")
    parser.add_argument("--group1", default="light", help="Reference group.")
    parser.add_argument("--group2", default="strong", help="Comparison group.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument("--resamples", type=int, default=2000, help="Bootstrap and permutation resample count.")
    parser.add_argument("--seed", type=int, default=1729, help="Deterministic random seed.")
    args = parser.parse_args()

    rows = load_rows(args.csv)
    if not rows:
        raise SystemExit(f"No rows found in {args.csv}")
    enriched = attach_derived_tiers(rows)
    left = [float(row[args.value_col]) for row in enriched if row.get(args.group_col) == args.group1 and row.get(args.value_col) not in ("", None)]
    right = [float(row[args.value_col]) for row in enriched if row.get(args.group_col) == args.group2 and row.get(args.value_col) not in ("", None)]
    if not left or not right:
        available = sorted({row.get(args.group_col, "") for row in enriched})
        raise SystemExit(f"Could not build both groups from `{args.group_col}`. Available groups: {available}")

    summary = summarize_groups(left, right, metric=args.value_col, group1=args.group1, group2=args.group2, resamples=args.resamples, seed=args.seed)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))
    return 0


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def attach_derived_tiers(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    enriched = []
    for row in rows:
        derived = dict(row)
        derived["perturbation_tier"] = infer_tier(row)
        enriched.append(derived)
    return enriched


def infer_tier(row: dict[str, str]) -> str:
    label = (row.get("variant_label") or "").lower()
    interpretation = (row.get("interpretation") or "").lower()
    if "strong" in label or "larger perturbation effect signal" in interpretation or "inline-2" in label:
        return "strong"
    if any(token in label for token in ("01_", "02_", "punctuation_cleanup", "minor_lexical", "light", "edited.txt", "inline-1")):
        return "light"
    if "moderate perturbation effect signal" in interpretation or any(token in label for token in ("03_", "sentence_split_merge", "04_", "word_order_shift")):
        return "moderate"
    return "other"


def summarize_groups(
    left: list[float],
    right: list[float],
    *,
    metric: str,
    group1: str,
    group2: str,
    resamples: int,
    seed: int,
) -> dict[str, object]:
    diff = fmean(left) - fmean(right)
    diff_interval = bootstrap_difference_interval(left, right, resamples=resamples, seed=seed)
    hedges = hedges_g(left, right)
    cliffs = cliffs_delta(left, right)
    p_value = permutation_p_value(left, right, resamples=resamples, seed=seed)
    return {
        "metric": metric,
        "group1": {"name": group1, "count": len(left), "mean": round(fmean(left), 6), "median": round(median(left), 6), "bootstrap_mean": bootstrap_mean_interval(left, resamples=resamples, seed=seed)},
        "group2": {"name": group2, "count": len(right), "mean": round(fmean(right), 6), "median": round(median(right), 6), "bootstrap_mean": bootstrap_mean_interval(right, resamples=resamples, seed=seed + 1)},
        "mean_difference": {
            "group1_minus_group2": round(diff, 6),
            "lower": round(diff_interval[0], 6),
            "upper": round(diff_interval[1], 6),
        },
        "hedges_g": round(hedges, 6) if hedges is not None else None,
        "cliffs_delta": round(cliffs, 6) if cliffs is not None else None,
        "permutation_p_value": round(p_value, 6),
        "guardrail": "Exploratory descriptive validation on the current aggregate study export. Treat wide intervals or near-zero effect sizes as signals to expand the benchmark rather than to strengthen claims.",
    }


def bootstrap_difference_interval(left: list[float], right: list[float], *, resamples: int, seed: int, confidence: float = 0.95) -> tuple[float, float]:
    rng = random.Random(seed)
    diffs = []
    for _ in range(resamples):
        draw_left = [rng.choice(left) for _ in range(len(left))]
        draw_right = [rng.choice(right) for _ in range(len(right))]
        diffs.append(fmean(draw_left) - fmean(draw_right))
    alpha = (1.0 - confidence) / 2.0
    diffs.sort()
    lower_index = max(0, int(alpha * len(diffs)) - 1)
    upper_index = min(len(diffs) - 1, int((1.0 - alpha) * len(diffs)) - 1)
    return diffs[lower_index], diffs[upper_index]


def hedges_g(left: list[float], right: list[float]) -> float | None:
    if len(left) < 2 or len(right) < 2:
        return None
    pooled = pooled_std(left, right)
    if pooled == 0:
        return 0.0
    raw = (fmean(left) - fmean(right)) / pooled
    correction = 1.0 - (3.0 / (4.0 * (len(left) + len(right)) - 9.0))
    return raw * correction


def cliffs_delta(left: list[float], right: list[float]) -> float | None:
    if not left or not right:
        return None
    score = 0.0
    for lhs in left:
        for rhs in right:
            if lhs > rhs:
                score += 1.0
            elif lhs < rhs:
                score -= 1.0
    return score / (len(left) * len(right))


def permutation_p_value(left: list[float], right: list[float], *, resamples: int, seed: int) -> float:
    rng = random.Random(seed)
    observed = abs(hedges_g(left, right) or 0.0)
    combined = left + right
    left_size = len(left)
    exceed = 0
    for _ in range(resamples):
        shuffled = combined[:]
        rng.shuffle(shuffled)
        perm_left = shuffled[:left_size]
        perm_right = shuffled[left_size:]
        stat = abs(hedges_g(perm_left, perm_right) or 0.0)
        if stat >= observed:
            exceed += 1
    return exceed / resamples if resamples else math.nan


def pooled_std(left: list[float], right: list[float]) -> float:
    left_var = sample_variance(left)
    right_var = sample_variance(right)
    denominator = len(left) + len(right) - 2
    if denominator <= 0:
        return 0.0
    return math.sqrt((((len(left) - 1) * left_var) + ((len(right) - 1) * right_var)) / denominator)


def sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean_value = fmean(values)
    return sum((value - mean_value) ** 2 for value in values) / (len(values) - 1)


def render_text(summary: dict[str, object]) -> str:
    group1 = summary["group1"]
    group2 = summary["group2"]
    diff = summary["mean_difference"]
    return "\n".join(
        [
            f"Group 1 ({group1['name']}): n={group1['count']}",
            f"Group 2 ({group2['name']}): n={group2['count']}",
            f"Mean difference ({group1['name']} - {group2['name']}): {diff['group1_minus_group2']:.6f} (95% CI: [{diff['lower']:.6f}, {diff['upper']:.6f}])",
            f"Hedges' g: {summary['hedges_g']}",
            f"Cliff's delta: {summary['cliffs_delta']}",
            f"Permutation p-value: {summary['permutation_p_value']}",
            f"Guardrail: {summary['guardrail']}",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
