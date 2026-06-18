#!/usr/bin/env python3
"""Generate a provenance-clean public empirical growth layer.

This layer addresses the current scale critique without mixing in private
workspace inputs. It uses released public benchmark v1.1 baselines and variants,
then adds deterministic in-memory perturbations whose raw generated texts are
not published. Public artifacts record metrics, hashes, methods, and provenance.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import string
from collections import defaultdict
from pathlib import Path
from statistics import fmean, median
from typing import Any, Callable

from cogniprint.analysis import analyze_text, compare_profiles
from cogniprint.stats.bootstrap import bootstrap_mean_interval


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_SAMPLES = ROOT / "datasets" / "public-benchmark-v1.1" / "metadata" / "sample-plan-template.csv"
OUTPUT_DIR = ROOT / "evidence" / "empirical-growth-v1"

EXTRA_TRANSFORM_VERSION = "deterministic-public-growth-v1"


def write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (ROOT / path).resolve()


def digest_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def tokenize(text: str) -> list[str]:
    return re.findall(r"\S+", text, flags=re.UNICODE)


def transform_token_pair_swap(text: str) -> str:
    tokens = tokenize(text)
    for index in range(0, len(tokens) - 1, 10):
        tokens[index], tokens[index + 1] = tokens[index + 1], tokens[index]
    return " ".join(tokens)


def transform_token_stride_drop(text: str) -> str:
    tokens = tokenize(text)
    if len(tokens) < 6:
        return text
    return " ".join(token for index, token in enumerate(tokens, start=1) if index % 9 != 0)


def transform_token_stride_duplicate(text: str) -> str:
    tokens = tokenize(text)
    if len(tokens) < 6:
        return text
    output: list[str] = []
    for index, token in enumerate(tokens, start=1):
        output.append(token)
        if index % 12 == 0:
            output.append(token)
    return " ".join(output)


def transform_sentence_order_rotate(text: str) -> str:
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
    if len(parts) < 2:
        return text
    return " ".join(parts[1:] + parts[:1])


def transform_punctuation_strip(text: str) -> str:
    translation = str.maketrans("", "", string.punctuation + "«»“”„…—–")
    return re.sub(r"\s+", " ", text.translate(translation)).strip()


EXTRA_TRANSFORMS: dict[str, Callable[[str], str]] = {
    "token_pair_swap": transform_token_pair_swap,
    "token_stride_drop": transform_token_stride_drop,
    "token_stride_duplicate": transform_token_stride_duplicate,
    "sentence_order_rotate": transform_sentence_order_rotate,
    "punctuation_strip": transform_punctuation_strip,
}


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


def build_existing_variant_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    released = [row for row in rows if row.get("release_status") == "released"]
    baseline_rows = {row["sample_id"]: row for row in released if row["relation_type"] == "baseline"}
    variants = [row for row in released if row["relation_type"] != "baseline"]
    baseline_profiles = {
        sample_id: analyze_text(resolve_repo_path(row["file_path"]).read_text(encoding="utf-8"))
        for sample_id, row in baseline_rows.items()
    }
    output: list[dict[str, Any]] = []
    for variant in variants:
        baseline = baseline_rows[variant["baseline_sample_id"]]
        variant_text = resolve_repo_path(variant["file_path"]).read_text(encoding="utf-8")
        comparison = compare_profiles(baseline_profiles[baseline["sample_id"]], analyze_text(variant_text))
        output.append(
            row_payload(
                baseline=baseline,
                variant_id=variant["sample_id"],
                axis=variant["relation_type"],
                variant_source="public-benchmark-v1.1-released-variant",
                variant_text_sha256=digest_text(variant_text),
                transform_version="released-public-benchmark-v1.1",
                comparison=comparison,
            )
        )
    return output


def build_generated_variant_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    baselines = [
        row for row in rows
        if row.get("release_status") == "released" and row.get("relation_type") == "baseline"
    ]
    output: list[dict[str, Any]] = []
    for baseline in baselines:
        baseline_text = resolve_repo_path(baseline["file_path"]).read_text(encoding="utf-8")
        baseline_profile = analyze_text(baseline_text)
        for axis, transform in EXTRA_TRANSFORMS.items():
            variant_text = transform(baseline_text)
            comparison = compare_profiles(baseline_profile, analyze_text(variant_text))
            output.append(
                row_payload(
                    baseline=baseline,
                    variant_id=f"{baseline['sample_id']}-{axis}",
                    axis=axis,
                    variant_source="deterministic-in-memory-public-transform",
                    variant_text_sha256=digest_text(variant_text),
                    transform_version=EXTRA_TRANSFORM_VERSION,
                    comparison=comparison,
                )
            )
    return output


def row_payload(
    *,
    baseline: dict[str, str],
    variant_id: str,
    axis: str,
    variant_source: str,
    variant_text_sha256: str,
    transform_version: str,
    comparison: dict[str, Any],
) -> dict[str, Any]:
    return {
        "baseline_sample_id": baseline["sample_id"],
        "variant_sample_id": variant_id,
        "axis": axis,
        "language": baseline["language"],
        "source_class": baseline["source_class"],
        "source_domain": baseline["source_domain"],
        "source_url": baseline["source_url"],
        "baseline_text_sha256": digest_text(resolve_repo_path(baseline["file_path"]).read_text(encoding="utf-8")),
        "variant_text_sha256": variant_text_sha256,
        "variant_source": variant_source,
        "transform_version": transform_version,
        "cosine_similarity": float(comparison["cosine_similarity"]),
        "euclidean_distance": float(comparison["euclidean_distance"]),
        "manhattan_distance": float(comparison["manhattan_distance"]),
    }


def axis_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_axis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_axis[row["axis"]].append(row)
    output = []
    for axis, axis_rows in sorted(by_axis.items()):
        cosine = [float(row["cosine_similarity"]) for row in axis_rows]
        euclidean = [float(row["euclidean_distance"]) for row in axis_rows]
        manhattan = [float(row["manhattan_distance"]) for row in axis_rows]
        output.append(
            {
                "axis": axis,
                "row_count": len(axis_rows),
                "language_count": len({row["language"] for row in axis_rows}),
                "source_class_count": len({row["source_class"] for row in axis_rows}),
                "cosine_similarity": metric_summary(cosine),
                "euclidean_distance": metric_summary(euclidean),
                "manhattan_distance": metric_summary(manhattan),
                "euclidean_bootstrap": bootstrap_mean_interval(euclidean),
            }
        )
    return output


def overall_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "cosine_similarity": metric_summary([float(row["cosine_similarity"]) for row in rows]),
        "euclidean_distance": metric_summary([float(row["euclidean_distance"]) for row in rows]),
        "manhattan_distance": metric_summary([float(row["manhattan_distance"]) for row in rows]),
    }


def build_payloads() -> dict[str, Any]:
    registry_rows = load_rows(BENCHMARK_SAMPLES)
    released = [row for row in registry_rows if row.get("release_status") == "released"]
    baselines = [row for row in released if row["relation_type"] == "baseline"]
    existing_rows = build_existing_variant_rows(registry_rows)
    generated_rows = build_generated_variant_rows(registry_rows)
    rows = sorted(existing_rows + generated_rows, key=lambda row: (row["baseline_sample_id"], row["axis"], row["variant_sample_id"]))
    axes = axis_summary(rows)
    counts = {
        "snapshot_id": "empirical-growth-v1",
        "comparison_row_count": len(rows),
        "baseline_count": len(baselines),
        "released_benchmark_variant_rows": len(existing_rows),
        "generated_public_transform_rows": len(generated_rows),
        "axis_count": len(axes),
        "minimum_axis_row_count": min(row["row_count"] for row in axes) if axes else 0,
        "language_count": len({row["language"] for row in baselines}),
        "source_class_count": len({row["source_class"] for row in baselines}),
    }
    manifest = {
        "snapshot_id": "empirical-growth-v1",
        "status": "public controlled empirical growth layer",
        "source_registry": str(BENCHMARK_SAMPLES.relative_to(ROOT)),
        "raw_private_inputs_included": False,
        "raw_generated_texts_published": False,
        "comparison_row_count": counts["comparison_row_count"],
        "guardrail": (
            "This layer addresses controlled-row scale for descriptive manuscript support. "
            "It does not turn CogniPrint into a completed empirical study or inference system."
        ),
    }
    return {
        "manifest": manifest,
        "counts": counts,
        "rows": rows,
        "axis_summary": axes,
        "overall_summary": overall_summary(rows),
    }


def write_markdown(payloads: dict[str, Any]) -> None:
    counts = payloads["counts"]
    overall = payloads["overall_summary"]
    readme = [
        "# Empirical Growth v1",
        "",
        "This directory records a provenance-clean public controlled empirical growth layer.",
        "",
        f"- comparison rows: `{counts['comparison_row_count']}`",
        f"- public baselines: `{counts['baseline_count']}`",
        f"- perturbation axes: `{counts['axis_count']}`",
        f"- minimum rows per axis: `{counts['minimum_axis_row_count']}`",
        "",
        "The layer uses public benchmark v1.1 baselines and released variants plus deterministic in-memory transforms.",
        "Raw private workspace inputs are not included.",
        "",
    ]
    (OUTPUT_DIR / "README.md").write_text("\n".join(readme), encoding="utf-8")
    methods = [
        "# Empirical Growth v1 Methods",
        "",
        "Rows are generated from released public benchmark v1.1 baselines.",
        "The first part reuses released public benchmark variants. The second part applies deterministic text transforms in memory and stores only metrics, hashes, and provenance.",
        "",
        "Additional transform axes:",
        "",
        *[f"- `{axis}`" for axis in EXTRA_TRANSFORMS],
        "",
        "All comparisons use the existing CogniPrint profile extraction and profile comparison functions.",
        "",
    ]
    (OUTPUT_DIR / "methods-summary.md").write_text("\n".join(methods), encoding="utf-8")
    results = [
        "# Empirical Growth v1 Results",
        "",
        f"- comparison rows: `{counts['comparison_row_count']}`",
        f"- minimum rows per axis: `{counts['minimum_axis_row_count']}`",
        f"- mean cosine similarity: `{overall['cosine_similarity']['mean']}`",
        f"- mean Euclidean distance: `{overall['euclidean_distance']['mean']}`",
        f"- mean Manhattan distance: `{overall['manhattan_distance']['mean']}`",
        "",
        "These results are descriptive controlled-row summaries.",
        "",
    ]
    (OUTPUT_DIR / "results-summary.md").write_text("\n".join(results), encoding="utf-8")
    limitations = [
        "# Empirical Growth v1 Limitations",
        "",
        "- rows are derived from public benchmark baselines, so this is not an independent external corpus;",
        "- generated transforms are deterministic and controlled, not naturally occurring edits;",
        "- the layer improves scale and axis coverage but does not justify stronger claims;",
        "- manuscript wording must remain descriptive until independent review and broader corpus validation are complete.",
        "",
    ]
    (OUTPUT_DIR / "limitations-summary.md").write_text("\n".join(limitations), encoding="utf-8")
    provenance = [
        "# Empirical Growth v1 Provenance",
        "",
        f"- source registry: `{BENCHMARK_SAMPLES.relative_to(ROOT)}`",
        "- source texts: released public benchmark v1.1 baseline files;",
        "- generated variant texts: deterministic in-memory transforms;",
        "- published artifacts: metrics, hashes, summaries, and provenance only;",
        "- private workspace inputs: not used.",
        "",
    ]
    (OUTPUT_DIR / "provenance-summary.md").write_text("\n".join(provenance), encoding="utf-8")


def main() -> int:
    payloads = build_payloads()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "manifest.json", payloads["manifest"])
    write_json(OUTPUT_DIR / "counts.json", payloads["counts"])
    write_json(OUTPUT_DIR / "overall-summary.json", payloads["overall_summary"])
    write_json(OUTPUT_DIR / "axis-summary.json", payloads["axis_summary"])
    write_json(OUTPUT_DIR / "comparison-rows.json", payloads["rows"])
    write_csv(
        OUTPUT_DIR / "axis-summary.csv",
        payloads["axis_summary"],
        ["axis", "row_count", "language_count", "source_class_count"],
    )
    write_csv(
        OUTPUT_DIR / "comparison-rows.csv",
        payloads["rows"],
        [
            "baseline_sample_id",
            "variant_sample_id",
            "axis",
            "language",
            "source_class",
            "source_domain",
            "variant_source",
            "transform_version",
            "baseline_text_sha256",
            "variant_text_sha256",
            "cosine_similarity",
            "euclidean_distance",
            "manhattan_distance",
        ],
    )
    write_markdown(payloads)
    print(f"Empirical growth v1 written: {OUTPUT_DIR.relative_to(ROOT)}")
    print(f"Rows: {payloads['counts']['comparison_row_count']}")
    print(f"Minimum rows per axis: {payloads['counts']['minimum_axis_row_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
