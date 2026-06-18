#!/usr/bin/env python3
"""Generate pre-review inferential-v1 validation artifacts.

This script executes the frozen inferential-v1 protocol without upgrading
CogniPrint readiness. Outputs are reviewer-facing candidate artifacts only.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import random
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import fmean, median
from typing import Any

from cogniprint.stats.bootstrap import bootstrap_mean_interval
from cogniprint.stats.effect_size import hedges_g
from cogniprint.stats.validation import _load_campaign_rows


ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_ROOT = ROOT / "workspace" / "campaigns"
PUBLIC_GROWTH_ROWS = ROOT / "evidence" / "empirical-growth-v1" / "comparison-rows.csv"
HOLDOUT_ROWS = ROOT / "evidence" / "independent-holdout-v1" / "comparison-rows.csv"
INPUT_MANIFEST = ROOT / "validation" / "inferential-v1" / "input-manifest.json"
PERMUTATION_SPEC = ROOT / "validation" / "inferential-v1" / "permutation-spec.json"
OUTPUT_DIR = ROOT / "validation" / "inferential-v1"


def main() -> int:
    input_manifest = read_json(INPUT_MANIFEST)
    spec = read_json(PERMUTATION_SPEC)
    config = input_manifest["configuration"]

    local_rows = _load_campaign_rows(CAMPAIGN_ROOT)
    if not local_rows:
        print(f"No local campaign rows found under {CAMPAIGN_ROOT}", file=sys.stderr)
        return 1

    public_rows = load_csv_rows(PUBLIC_GROWTH_ROWS, source="public_growth")
    holdout_rows = load_csv_rows(HOLDOUT_ROWS, source="independent_holdout")
    metrics = list(config["primary_metrics"])
    primary_metric = str(spec["primary_metric"])
    seed = int(spec["random_seed"])
    bootstrap_resamples = int(config["bootstrap_resamples"])
    permutation_resamples = int(spec["resamples"])
    manifest_generated_at_utc = resolve_manifest_generated_at()
    command_log_generated_at_utc = resolve_command_log_generated_at()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    bootstrap_rows = build_bootstrap_rows(
        local_rows,
        public_rows,
        holdout_rows,
        metrics=metrics,
        seed=seed,
        resamples=bootstrap_resamples,
    )
    permutation_rows = build_permutation_rows(
        spec,
        local_rows,
        public_rows,
        seed=seed,
        resamples=permutation_resamples,
    )
    effect_rows = build_effect_rows(permutation_rows, local_rows, public_rows, metric=primary_metric)
    sensitivity_rows = build_sensitivity_rows(
        spec,
        local_rows,
        public_rows,
        metrics=list(spec.get("sensitivity_metrics", [])),
        seed=seed,
        resamples=permutation_resamples,
    )
    ablation_rows = build_ablation_rows(local_rows, public_rows, metrics=metrics)

    write_csv(OUTPUT_DIR / "bootstrap-summary.csv", bootstrap_rows, list(bootstrap_rows[0]))
    write_json(OUTPUT_DIR / "bootstrap-summary.json", {"rows": bootstrap_rows})
    write_csv(OUTPUT_DIR / "permutation-results.csv", permutation_rows, list(permutation_rows[0]))
    write_json(OUTPUT_DIR / "permutation-results.json", {"rows": permutation_rows})
    write_csv(OUTPUT_DIR / "effect-sizes.csv", effect_rows, list(effect_rows[0]))
    write_json(OUTPUT_DIR / "effect-sizes.json", {"rows": effect_rows})
    write_csv(OUTPUT_DIR / "sensitivity-results.csv", sensitivity_rows, list(sensitivity_rows[0]))
    write_json(OUTPUT_DIR / "sensitivity-results.json", {"rows": sensitivity_rows})
    write_csv(OUTPUT_DIR / "ablation-results.csv", ablation_rows, list(ablation_rows[0]))
    write_json(OUTPUT_DIR / "ablation-results.json", {"rows": ablation_rows})

    write_command_log(
        OUTPUT_DIR / "command-log.txt",
        input_manifest=input_manifest,
        spec=spec,
        row_counts={
            "local_campaign_rows": len(local_rows),
            "public_growth_rows": len(public_rows),
            "independent_holdout_rows": len(holdout_rows),
        },
        generated_at_utc=command_log_generated_at_utc,
    )
    write_results_report(OUTPUT_DIR / "results-report.md", permutation_rows, effect_rows, sensitivity_rows)
    write_limitations_report(OUTPUT_DIR / "limitations-report.md", local_rows, public_rows, holdout_rows)

    manifest = build_output_manifest(
        input_manifest=input_manifest,
        spec=spec,
        local_rows=local_rows,
        public_rows=public_rows,
        holdout_rows=holdout_rows,
        generated_at_utc=manifest_generated_at_utc,
    )
    write_json(OUTPUT_DIR / "output-manifest.json", manifest)
    write_checksum_manifest(OUTPUT_DIR / "checksum-manifest.txt")

    print(f"Inferential-v1 artifacts written to {OUTPUT_DIR.relative_to(ROOT)}")
    print("Readiness boundary remains descriptive_only.")
    return 0


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_csv_rows(path: Path, *, source: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for raw in csv.DictReader(handle):
            rows.append(
                {
                    **raw,
                    "source": source,
                    "campaign_id": raw.get("campaign_id") or source,
                    "variant_label": raw.get("variant_sample_id") or raw.get("variant_id") or raw.get("sample_id", ""),
                    "axis": raw["axis"],
                    "cosine_similarity": float(raw["cosine_similarity"]),
                    "euclidean_distance": float(raw["euclidean_distance"]),
                    "manhattan_distance": float(raw["manhattan_distance"]),
                }
            )
    return rows


def build_bootstrap_rows(
    local_rows: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    holdout_rows: list[dict[str, Any]],
    *,
    metrics: list[str],
    seed: int,
    resamples: int,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for source, rows in (
        ("local_campaign", local_rows),
        ("public_growth", public_rows),
        ("independent_holdout", holdout_rows),
    ):
        for row in rows:
            for metric in metrics:
                grouped[(source, row["axis"], metric)].append(float(row[metric]))

    output = []
    for index, ((source, axis, metric), values) in enumerate(sorted(grouped.items())):
        interval = bootstrap_mean_interval(values, seed=seed + index, resamples=resamples)
        output.append(
            {
                "source": source,
                "axis": axis,
                "metric": metric,
                "count": len(values),
                "mean": round(fmean(values), 6),
                "median": round(float(median(values)), 6),
                "bootstrap_confidence": interval["confidence"],
                "bootstrap_resamples": interval["resamples"],
                "bootstrap_seed": seed + index,
                "bootstrap_lower": interval["lower"],
                "bootstrap_upper": interval["upper"],
                "small_sample_note": "small local campaign n" if source == "local_campaign" and len(values) < 10 else "",
            }
        )
    return output


def build_permutation_rows(
    spec: dict[str, Any],
    local_rows: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    *,
    seed: int,
    resamples: int,
) -> list[dict[str, Any]]:
    rows = []
    for index, contrast in enumerate(spec["predeclared_contrasts"]):
        axis = extract_axis(contrast["left_group"])
        metric = contrast["metric"]
        left = metric_values(local_rows, axis, metric)
        right = metric_values(public_rows, axis, metric)
        result = permutation_test(left, right, seed=seed + index, resamples=resamples)
        rows.append(
            {
                "contrast_id": contrast["contrast_id"],
                "axis": axis,
                "metric": metric,
                "left_group": contrast["left_group"],
                "right_group": contrast["right_group"],
                "left_count": len(left),
                "right_count": len(right),
                "left_mean": round(fmean(left), 6) if left else None,
                "right_mean": round(fmean(right), 6) if right else None,
                "mean_difference_left_minus_right": round(fmean(left) - fmean(right), 6) if left and right else None,
                **result,
            }
        )
    add_p_value_corrections(rows)
    return rows


def build_effect_rows(
    permutation_rows: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    *,
    metric: str,
) -> list[dict[str, Any]]:
    output = []
    for row in permutation_rows:
        axis = row["axis"]
        left = metric_values(local_rows, axis, metric)
        right = metric_values(public_rows, axis, metric)
        output.append(
            {
                "contrast_id": row["contrast_id"],
                "axis": axis,
                "metric": metric,
                "left_count": len(left),
                "right_count": len(right),
                "median_difference_left_minus_right": round(float(median(left)) - float(median(right)), 6),
                "cliffs_delta_left_vs_right": cliffs_delta(left, right),
                "hedges_g_right_vs_left": hedges_g(left, right)["value"],
                "interpretation_note": "Observed dataset only; small local campaign n limits stability claims.",
            }
        )
    return output


def build_sensitivity_rows(
    spec: dict[str, Any],
    local_rows: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    *,
    metrics: list[str],
    seed: int,
    resamples: int,
) -> list[dict[str, Any]]:
    output = []
    for metric_index, metric in enumerate(metrics):
        rows = []
        for contrast_index, contrast in enumerate(spec["predeclared_contrasts"]):
            axis = extract_axis(contrast["left_group"])
            left = metric_values(local_rows, axis, metric)
            right = metric_values(public_rows, axis, metric)
            result = permutation_test(
                left,
                right,
                seed=seed + 1000 + (metric_index * 100) + contrast_index,
                resamples=resamples,
            )
            rows.append(
                {
                    "sensitivity_dimension": "metric_choice",
                    "metric": metric,
                    "axis": axis,
                    "left_count": len(left),
                    "right_count": len(right),
                    "left_mean": round(fmean(left), 6) if left else None,
                    "right_mean": round(fmean(right), 6) if right else None,
                    "mean_difference_left_minus_right": round(fmean(left) - fmean(right), 6) if left and right else None,
                    **result,
                }
            )
        add_p_value_corrections(rows)
        output.extend(rows)
    return output


def build_ablation_rows(
    local_rows: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    *,
    metrics: list[str],
) -> list[dict[str, Any]]:
    output = []
    axes = sorted({row["axis"] for row in local_rows} & {row["axis"] for row in public_rows})
    campaigns = sorted({row["campaign_id"] for row in local_rows})

    for metric in metrics:
        axis_deltas = {
            axis: fmean(metric_values(local_rows, axis, metric)) - fmean(metric_values(public_rows, axis, metric))
            for axis in axes
        }
        full_family_mean = fmean(axis_deltas.values())
        for axis in axes:
            remaining = [value for candidate, value in axis_deltas.items() if candidate != axis]
            output.append(
                {
                    "ablation_type": "axis_family_leave_one_axis_out",
                    "metric": metric,
                    "removed_unit": axis,
                    "full_family_mean_delta": round(full_family_mean, 6),
                    "ablated_family_mean_delta": round(fmean(remaining), 6) if remaining else None,
                    "delta_change": round(fmean(remaining) - full_family_mean, 6) if remaining else None,
                    "note": "Axis-family ablation only; feature-group ablation remains deferred.",
                }
            )

        for campaign_id in campaigns:
            remaining_local = [row for row in local_rows if row["campaign_id"] != campaign_id]
            remaining_axis_deltas = []
            for axis in axes:
                remaining_values = metric_values(remaining_local, axis, metric)
                public_values = metric_values(public_rows, axis, metric)
                if remaining_values and public_values:
                    remaining_axis_deltas.append(fmean(remaining_values) - fmean(public_values))
            output.append(
                {
                    "ablation_type": "local_campaign_leave_one_campaign_out",
                    "metric": metric,
                    "removed_unit": campaign_id,
                    "full_family_mean_delta": round(full_family_mean, 6),
                    "ablated_family_mean_delta": round(fmean(remaining_axis_deltas), 6) if remaining_axis_deltas else None,
                    "delta_change": round(fmean(remaining_axis_deltas) - full_family_mean, 6) if remaining_axis_deltas else None,
                    "note": "Campaign inclusion sensitivity; not a feature-group ablation.",
                }
            )
    output.append(
        {
            "ablation_type": "feature_group_ablation",
            "metric": "not_run",
            "removed_unit": "major_feature_groups",
            "full_family_mean_delta": None,
            "ablated_family_mean_delta": None,
            "delta_change": None,
            "note": "Deferred until profile-vector-level row schema exposes major feature-group recomputation.",
        }
    )
    return output


def metric_values(rows: list[dict[str, Any]], axis: str, metric: str) -> list[float]:
    return [float(row[metric]) for row in rows if row["axis"] == axis]


def extract_axis(group: str) -> str:
    marker = "_axis:"
    if marker not in group:
        raise ValueError(f"Cannot extract axis from group: {group}")
    return group.split(marker, 1)[1]


def permutation_test(left: list[float], right: list[float], *, seed: int, resamples: int) -> dict[str, Any]:
    if not left or not right:
        return {
            "observed_abs_mean_difference": None,
            "raw_p_value": None,
            "reported_p_value": None,
            "exceedance_count": 0,
            "permutation_resamples": resamples,
            "permutation_seed": seed,
            "reporting_note": "insufficient data",
        }

    observed = abs(fmean(left) - fmean(right))
    combined = left + right
    left_size = len(left)
    rng = random.Random(seed)
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
    reported = max(raw, 1.0 / resamples)
    return {
        "observed_abs_mean_difference": round(observed, 6),
        "raw_p_value": round(raw, 6),
        "reported_p_value": round(reported, 6),
        "exceedance_count": exceed,
        "permutation_resamples": resamples,
        "permutation_seed": seed,
        "reporting_note": "reported p-value uses finite-resample floor of 1/resamples",
    }


def add_p_value_corrections(rows: list[dict[str, Any]]) -> None:
    p_rows = [row for row in rows if row.get("reported_p_value") is not None]
    holm = holm_adjust(p_rows)
    bh = benjamini_hochberg_adjust(p_rows)
    for row in rows:
        key = row.get("contrast_id") or f"{row['metric']}:{row['axis']}"
        row["holm_adjusted_p_value"] = holm.get(key)
        row["bh_fdr_q_value"] = bh.get(key)
        row["holm_flag_at_0_05"] = row["holm_adjusted_p_value"] is not None and row["holm_adjusted_p_value"] <= 0.05
        row["bh_fdr_flag_at_0_05"] = row["bh_fdr_q_value"] is not None and row["bh_fdr_q_value"] <= 0.05


def holm_adjust(rows: list[dict[str, Any]]) -> dict[str, float]:
    sorted_rows = sorted(rows, key=lambda row: (float(row["reported_p_value"]), row.get("contrast_id") or row["axis"]))
    m = len(sorted_rows)
    adjusted: dict[str, float] = {}
    running_max = 0.0
    for rank, row in enumerate(sorted_rows, start=1):
        value = min(1.0, (m - rank + 1) * float(row["reported_p_value"]))
        running_max = max(running_max, value)
        adjusted[row.get("contrast_id") or f"{row['metric']}:{row['axis']}"] = round(running_max, 6)
    return adjusted


def benjamini_hochberg_adjust(rows: list[dict[str, Any]]) -> dict[str, float]:
    sorted_rows = sorted(rows, key=lambda row: (float(row["reported_p_value"]), row.get("contrast_id") or row["axis"]))
    m = len(sorted_rows)
    adjusted: dict[str, float] = {}
    running_min = 1.0
    for rank, row in reversed(list(enumerate(sorted_rows, start=1))):
        value = min(1.0, float(row["reported_p_value"]) * m / rank)
        running_min = min(running_min, value)
        adjusted[row.get("contrast_id") or f"{row['metric']}:{row['axis']}"] = round(running_min, 6)
    return adjusted


def cliffs_delta(left: list[float], right: list[float]) -> float | None:
    if not left or not right:
        return None
    more = 0
    less = 0
    for left_value in left:
        for right_value in right:
            if left_value > right_value:
                more += 1
            elif left_value < right_value:
                less += 1
    return round((more - less) / (len(left) * len(right)), 6)


def write_command_log(
    path: Path,
    *,
    input_manifest: dict[str, Any],
    spec: dict[str, Any],
    row_counts: dict[str, int],
    generated_at_utc: str,
) -> None:
    lines = [
        "# inferential-v1 command log",
        "",
        f"generated_at_utc: {generated_at_utc}",
        "command: PYTHONPATH=. .venv/bin/python scripts/generate_inferential_v1.py",
        f"python: {platform.python_version()}",
        f"platform: {platform.platform()}",
        f"input_manifest: {input_manifest['snapshot_id']}",
        f"permutation_spec: {spec['snapshot_id']}",
        f"readiness_boundary: {spec['readiness_boundary']}",
        "",
        "row_counts:",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(row_counts.items()))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_results_report(
    path: Path,
    permutation_rows: list[dict[str, Any]],
    effect_rows: list[dict[str, Any]],
    sensitivity_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# Inferential V1 Results Report",
        "",
        "Status: pre-review inferential candidate outputs.",
        "Readiness boundary: `descriptive_only`.",
        "",
        "These results execute the frozen local-campaign versus public-growth contrast family. They do not satisfy the external-review gate and do not upgrade CogniPrint readiness.",
        "",
        "## Primary contrasts",
        "",
    ]
    for row in permutation_rows:
        effect = next(item for item in effect_rows if item["contrast_id"] == row["contrast_id"])
        lines.append(
            "- `{axis}`: n={left_count}/{right_count}, mean delta={delta}, "
            "reported p={p}, Holm={holm}, Cliff's delta={cliff}, median delta={median_delta}".format(
                axis=row["axis"],
                left_count=row["left_count"],
                right_count=row["right_count"],
                delta=row["mean_difference_left_minus_right"],
                p=row["reported_p_value"],
                holm=row["holm_adjusted_p_value"],
                cliff=effect["cliffs_delta_left_vs_right"],
                median_delta=effect["median_difference_left_minus_right"],
            )
        )
    lines.extend(
        [
            "",
            "## Sensitivity",
            "",
            "Sensitivity rows rerun the same contrast family for `cosine_similarity` and `manhattan_distance`. They are diagnostic only and should be read alongside group sizes and limitations.",
            "",
            f"- sensitivity rows: {len(sensitivity_rows)}",
            "",
            "## Boundary",
            "",
            "Do not use these outputs to claim author identification, text provenance determination, legal conclusion, deterministic classification, or universal performance.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations_report(
    path: Path,
    local_rows: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    holdout_rows: list[dict[str, Any]],
) -> None:
    local_axis_counts = axis_counts(local_rows)
    lines = [
        "# Inferential V1 Limitations Report",
        "",
        "Status: pre-review limitations for inferential-v1 candidate outputs.",
        "Readiness boundary: `descriptive_only`.",
        "",
        "## Current limitations",
        "",
        "- Local campaign axis counts remain small; most shared axes have only three local campaign rows.",
        "- Public growth rows improve scale but are still corpus-bound and transformation-protocol-bound.",
        "- Independent holdout rows are source-separation context and are not included in the primary permutation family.",
        "- Feature-group ablation is deferred because the current comparison-row schema does not expose recomputed profile vectors after major feature-group removal.",
        "- P-values are reported with effect sizes and confidence intervals; they are not standalone validation claims.",
        "- External non-owner review is still required before any stronger readiness wording.",
        "",
        "## Counts",
        "",
        f"- local campaign rows: {len(local_rows)}",
        f"- public growth rows: {len(public_rows)}",
        f"- independent holdout rows: {len(holdout_rows)}",
        f"- minimum local axis count: {min(local_axis_counts.values()) if local_axis_counts else 0}",
        "",
        "## Non-claims",
        "",
        "CogniPrint is not an authorship system, provenance detector, legal tool, deterministic classifier, or final decision layer.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_manifest_generated_at() -> str:
    """Preserve the existing manifest timestamp so validation reruns stay stable."""

    output_manifest = OUTPUT_DIR / "output-manifest.json"
    if output_manifest.exists():
        try:
            existing = read_json(output_manifest)
        except json.JSONDecodeError:
            existing = {}
        value = existing.get("generated_at_utc")
        if isinstance(value, str) and value:
            return value
    return datetime.now(UTC).isoformat()


def resolve_command_log_generated_at() -> str:
    """Preserve the existing command-log timestamp so validation reruns stay stable."""

    command_log = OUTPUT_DIR / "command-log.txt"
    if command_log.exists():
        for line in command_log.read_text(encoding="utf-8").splitlines():
            if line.startswith("generated_at_utc: "):
                value = line.split(": ", 1)[1].strip()
                if value:
                    return value
    return datetime.now(UTC).isoformat()


def build_output_manifest(
    *,
    input_manifest: dict[str, Any],
    spec: dict[str, Any],
    local_rows: list[dict[str, Any]],
    public_rows: list[dict[str, Any]],
    holdout_rows: list[dict[str, Any]],
    generated_at_utc: str,
) -> dict[str, Any]:
    return {
        "snapshot_id": "inferential-v1-outputs-20260512",
        "status": "pre_review_inferential_candidate_outputs",
        "readiness_boundary": "descriptive_only",
        "input_manifest": "validation/inferential-v1/input-manifest.json",
        "permutation_spec": "validation/inferential-v1/permutation-spec.json",
        "generated_at_utc": generated_at_utc,
        "external_review_required_before_stronger_readiness": True,
        "stronger_readiness_allowed": False,
        "counts": {
            "local_campaign_rows": len(local_rows),
            "public_growth_rows": len(public_rows),
            "independent_holdout_rows": len(holdout_rows),
            "predeclared_contrasts": len(spec["predeclared_contrasts"]),
            "sensitivity_metrics": len(spec.get("sensitivity_metrics", [])),
        },
        "configuration": {
            "primary_metric": spec["primary_metric"],
            "sensitivity_metrics": spec.get("sensitivity_metrics", []),
            "random_seed": spec["random_seed"],
            "bootstrap_resamples": input_manifest["configuration"]["bootstrap_resamples"],
            "permutation_resamples": spec["resamples"],
            "correction_methods": spec["multiple_comparison_correction"],
        },
        "artifacts": artifact_entries(),
        "guardrail": (
            "These outputs execute the frozen protocol but do not satisfy external review and do not upgrade readiness."
        ),
    }


def artifact_entries() -> list[dict[str, str]]:
    names = [
        "bootstrap-summary.csv",
        "bootstrap-summary.json",
        "permutation-results.csv",
        "permutation-results.json",
        "effect-sizes.csv",
        "effect-sizes.json",
        "sensitivity-results.csv",
        "sensitivity-results.json",
        "ablation-results.csv",
        "ablation-results.json",
        "results-report.md",
        "limitations-report.md",
        "command-log.txt",
    ]
    entries = []
    for name in names:
        path = OUTPUT_DIR / name
        entries.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)})
    return entries


def write_checksum_manifest(path: Path) -> None:
    checksum_targets = [
        "bootstrap-summary.csv",
        "bootstrap-summary.json",
        "permutation-results.csv",
        "permutation-results.json",
        "effect-sizes.csv",
        "effect-sizes.json",
        "sensitivity-results.csv",
        "sensitivity-results.json",
        "ablation-results.csv",
        "ablation-results.json",
        "results-report.md",
        "limitations-report.md",
        "output-manifest.json",
        "command-log.txt",
    ]
    lines = [f"{sha256(OUTPUT_DIR / name)}  validation/inferential-v1/{name}" for name in checksum_targets]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def axis_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[row["axis"]] += 1
    return dict(counts)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
