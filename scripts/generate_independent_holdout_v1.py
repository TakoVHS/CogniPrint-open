#!/usr/bin/env python3
"""Generate independent holdout validation artifacts."""

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
DATASET_DIR = ROOT / "datasets" / "independent-holdout-v1"
SOURCES_CSV = DATASET_DIR / "metadata" / "sources.csv"
OUTPUT_DIR = ROOT / "evidence" / "independent-holdout-v1"


def write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_sources() -> list[dict[str, str]]:
    with SOURCES_CSV.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (ROOT / path).resolve()


def digest_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def tokens(text: str) -> list[str]:
    return re.findall(r"\S+", text, flags=re.UNICODE)


def punctuation_strip(text: str) -> str:
    translation = str.maketrans("", "", string.punctuation + "«»“”„…—–")
    return re.sub(r"\s+", " ", text.translate(translation)).strip()


def token_pair_swap(text: str) -> str:
    output = tokens(text)
    for index in range(0, len(output) - 1, 9):
        output[index], output[index + 1] = output[index + 1], output[index]
    return " ".join(output)


def token_stride_drop(text: str) -> str:
    output = tokens(text)
    return " ".join(token for index, token in enumerate(output, start=1) if index % 8 != 0)


def token_stride_duplicate(text: str) -> str:
    output: list[str] = []
    for index, token in enumerate(tokens(text), start=1):
        output.append(token)
        if index % 10 == 0:
            output.append(token)
    return " ".join(output)


def sentence_rotate(text: str) -> str:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
    if len(sentences) < 2:
        return text
    return " ".join(sentences[1:] + sentences[:1])


TRANSFORMS: dict[str, Callable[[str], str]] = {
    "holdout_punctuation_strip": punctuation_strip,
    "holdout_token_pair_swap": token_pair_swap,
    "holdout_token_stride_drop": token_stride_drop,
    "holdout_token_stride_duplicate": token_stride_duplicate,
    "holdout_sentence_rotate": sentence_rotate,
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


def build_rows(sources: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in sources:
        baseline_path = resolve_repo_path(source["file_path"])
        baseline_text = baseline_path.read_text(encoding="utf-8")
        baseline_profile = analyze_text(baseline_text)
        for axis, transform in TRANSFORMS.items():
            variant_text = transform(baseline_text)
            comparison = compare_profiles(baseline_profile, analyze_text(variant_text))
            rows.append(
                {
                    "sample_id": source["sample_id"],
                    "variant_id": f"{source['sample_id']}-{axis}",
                    "axis": axis,
                    "language": source["language"],
                    "source_class": source["source_class"],
                    "source_domain": source["source_domain"],
                    "source_url": source["source_url"],
                    "license_url": source["license_url"],
                    "baseline_text_sha256": digest_text(baseline_text),
                    "variant_text_sha256": digest_text(variant_text),
                    "variant_source": "deterministic-in-memory-holdout-transform",
                    "cosine_similarity": float(comparison["cosine_similarity"]),
                    "euclidean_distance": float(comparison["euclidean_distance"]),
                    "manhattan_distance": float(comparison["manhattan_distance"]),
                }
            )
    return sorted(rows, key=lambda row: (row["sample_id"], row["axis"]))


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


def write_markdown(counts: dict[str, Any], overall: dict[str, Any]) -> None:
    (OUTPUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Independent Holdout v1",
                "",
                "This directory records a separate holdout validation layer built from Project Gutenberg excerpts that do not overlap with the public benchmark v1.1 registry.",
                "",
                f"- holdout baselines: `{counts['baseline_count']}`",
                f"- comparison rows: `{counts['comparison_row_count']}`",
                f"- transform axes: `{counts['axis_count']}`",
                "",
                "The layer is descriptive and does not replace external review.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "methods-summary.md").write_text(
        "\n".join(
            [
                "# Independent Holdout v1 Methods",
                "",
                "The holdout uses short Project Gutenberg excerpts stored under `datasets/independent-holdout-v1/raw/` with source metadata in `datasets/independent-holdout-v1/metadata/sources.csv`.",
                "",
                "For each excerpt, five deterministic transforms are applied in memory. Generated variant texts are not published; only hashes and comparison metrics are stored.",
                "",
                "Comparison metrics use the same CogniPrint profile extraction and comparison functions as the rest of the evidence package.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "results-summary.md").write_text(
        "\n".join(
            [
                "# Independent Holdout v1 Results",
                "",
                f"- comparison rows: `{counts['comparison_row_count']}`",
                f"- minimum rows per axis: `{counts['minimum_axis_row_count']}`",
                f"- mean cosine similarity: `{overall['cosine_similarity']['mean']}`",
                f"- mean Euclidean distance: `{overall['euclidean_distance']['mean']}`",
                f"- mean Manhattan distance: `{overall['manhattan_distance']['mean']}`",
                "",
                "These are descriptive holdout summaries.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "limitations-summary.md").write_text(
        "\n".join(
            [
                "# Independent Holdout v1 Limitations",
                "",
                "- the holdout is English-only in the current v1 layer;",
                "- sources are public-domain literary excerpts and do not cover operational or modern private writing;",
                "- generated transforms are controlled perturbations rather than naturally occurring revisions;",
                "- results remain descriptive until independent reviewer feedback is recorded.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "provenance-summary.md").write_text(
        "\n".join(
            [
                "# Independent Holdout v1 Provenance",
                "",
                "- source family: Project Gutenberg;",
                "- source metadata: `datasets/independent-holdout-v1/metadata/sources.csv`; ",
                "- raw baseline excerpts: `datasets/independent-holdout-v1/raw/`; ",
                "- generated variants: in-memory only, not published;",
                "- public artifacts: metrics, hashes, and summaries.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    if not SOURCES_CSV.exists():
        raise SystemExit("Missing independent holdout sources. Run scripts/fetch_independent_holdout_v1_sources.py first.")
    sources = load_sources()
    rows = build_rows(sources)
    axes = axis_summary(rows)
    overall = overall_summary(rows)
    counts = {
        "snapshot_id": "independent-holdout-v1",
        "baseline_count": len(sources),
        "comparison_row_count": len(rows),
        "axis_count": len(axes),
        "minimum_axis_row_count": min(axis["row_count"] for axis in axes) if axes else 0,
        "language_count": len({source["language"] for source in sources}),
        "source_family": "Project Gutenberg",
    }
    manifest = {
        "snapshot_id": "independent-holdout-v1",
        "status": "descriptive independent holdout validation layer",
        "source_metadata": str(SOURCES_CSV.relative_to(ROOT)),
        "raw_private_inputs_included": False,
        "generated_variant_texts_published": False,
        "guardrail": "This layer supplies an independent holdout source family but remains descriptive until external review is present.",
    }
    write_json(OUTPUT_DIR / "manifest.json", manifest)
    write_json(OUTPUT_DIR / "counts.json", counts)
    write_json(OUTPUT_DIR / "overall-summary.json", overall)
    write_json(OUTPUT_DIR / "axis-summary.json", axes)
    write_json(OUTPUT_DIR / "comparison-rows.json", rows)
    write_csv(OUTPUT_DIR / "axis-summary.csv", axes, ["axis", "row_count"])
    write_csv(
        OUTPUT_DIR / "comparison-rows.csv",
        rows,
        [
            "sample_id",
            "variant_id",
            "axis",
            "language",
            "source_class",
            "source_domain",
            "variant_source",
            "baseline_text_sha256",
            "variant_text_sha256",
            "cosine_similarity",
            "euclidean_distance",
            "manhattan_distance",
        ],
    )
    write_markdown(counts, overall)
    print(f"Independent holdout v1 written: {OUTPUT_DIR.relative_to(ROOT)}")
    print(f"Rows: {counts['comparison_row_count']}")
    print(f"Minimum rows per axis: {counts['minimum_axis_row_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
