"""Generate mathematical evidence diagnostics for CogniPrint v2.

This script creates a dependency-light evidence layer focused on the
mathematical behavior of the 12-dimensional cognitive fingerprint. Outputs are
diagnostic and pre-review; they do not upgrade scientific readiness.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
from collections import Counter
from itertools import combinations
from pathlib import Path
from statistics import fmean, median
from typing import Any

from cogniprint.fingerprint import FEATURE_NAMES, FINGERPRINT_VERSION, CognitiveFingerprint
from cogniprint.validation import DeterministicRandomVectorBaseline, SimpleTfidfBaseline, cohens_d

TOKEN_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+", re.UNICODE)
BASELINE_RE = re.compile(r"(?P<sample>.+)-baseline\.txt$")
VARIANT_RE = re.compile(r"(?P<sample>.+)-variant-(?P<variant>[a-z])\.txt$")


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    variant_dir = Path(args.variant_dir)
    holdout_dir = Path(args.holdout_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_rows = load_text_files(raw_dir)
    holdout_rows = load_text_files(holdout_dir) if holdout_dir.exists() else []
    variant_pairs = load_variant_pairs(raw_dir, variant_dir)
    if len(raw_rows) < 3:
        raise SystemExit(f"Need at least 3 baseline texts for mathematical evidence diagnostics: {raw_dir}")
    if not variant_pairs:
        raise SystemExit(f"No baseline/variant pairs found under {raw_dir} and {variant_dir}")

    matrix_rows = raw_rows + holdout_rows
    matrix = [fingerprint_vector(text) for _, text in matrix_rows]
    pca = pca_diagnostics(matrix)
    write_pca_outputs(output_dir, pca)

    length_rows, length_summary = length_stability_diagnostics(
        [text for _, text in matrix_rows],
        lengths=parse_lengths(args.lengths),
        seed=args.seed,
    )
    write_csv(
        output_dir / "min-text-length-stability.csv",
        ["length_tokens", "sample_count", "mean_deviation_from_centroid", "median_deviation_from_centroid", "max_deviation_from_centroid"],
        length_rows,
    )
    write_json(output_dir / "min-text-length-stability.json", length_summary)

    lipschitz_rows, lipschitz_summary, feature_sensitivity = lipschitz_diagnostics(variant_pairs)
    write_csv(
        output_dir / "lipschitz-pair-diagnostics.csv",
        [
            "sample_id",
            "variant_label",
            "baseline_tokens",
            "variant_tokens",
            "word_edit_distance",
            "euclidean_profile_delta",
            "cosine_profile_distance",
            "k_empirical_euclidean_per_word_edit",
        ],
        lipschitz_rows,
    )
    write_csv(
        output_dir / "feature-sensitivity.csv",
        ["feature", "mean_abs_delta", "median_abs_delta", "max_abs_delta"],
        feature_sensitivity,
    )
    write_json(output_dir / "lipschitz-summary.json", lipschitz_summary)

    baseline_rows, baseline_summary = baseline_contrast_diagnostics(
        raw_rows=raw_rows,
        variant_pairs=variant_pairs,
        max_random_pairs=args.max_random_pairs,
        seed=args.seed,
    )
    write_csv(
        output_dir / "baseline-comparison.csv",
        [
            "pair_type",
            "left_id",
            "right_id",
            "fingerprint_cosine_distance",
            "fingerprint_euclidean_distance",
            "tfidf_cosine_distance",
            "random_vector_distance",
        ],
        baseline_rows,
    )
    write_json(output_dir / "baseline-comparison-summary.json", baseline_summary)

    manifest = {
        "snapshot_id": "mathematical-evidence-v1",
        "status": "pre-review mathematical diagnostics",
        "readiness_boundary": "descriptive_only",
        "external_review_gate_satisfied": False,
        "fingerprint_version": FINGERPRINT_VERSION,
        "baseline_text_count": len(raw_rows),
        "holdout_text_count": len(holdout_rows),
        "variant_pair_count": len(variant_pairs),
        "feature_count": len(FEATURE_NAMES),
        "outputs": [
            "pca-summary.json",
            "pca-components.csv",
            "min-text-length-stability.json",
            "min-text-length-stability.csv",
            "lipschitz-summary.json",
            "lipschitz-pair-diagnostics.csv",
            "feature-sensitivity.csv",
            "baseline-comparison-summary.json",
            "baseline-comparison.csv",
            "README.md",
        ],
        "guardrail": (
            "These outputs characterize fingerprint geometry and sensitivity. "
            "They do not establish validation, authorship, provenance, AI detection, "
            "legal status, forensic status, or a universal threshold."
        ),
    }
    write_json(output_dir / "manifest.json", manifest)
    write_readme(output_dir, manifest, pca, length_summary, lipschitz_summary, baseline_summary)
    print(f"Mathematical evidence v1 written: {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", default="datasets/public-benchmark-v1.1/raw")
    parser.add_argument("--variant-dir", default="datasets/public-benchmark-v1.1/variants")
    parser.add_argument("--holdout-dir", default="datasets/independent-holdout-v1/raw")
    parser.add_argument("--output-dir", default="validation/mathematical-evidence-v1")
    parser.add_argument("--lengths", default="40,80,120,200,320,500,800")
    parser.add_argument("--max-random-pairs", type=int, default=250)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def load_text_files(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if not path.exists():
        return rows
    for item in sorted(path.glob("*.txt")):
        rows.append((item.stem, item.read_text(encoding="utf-8")))
    return rows


def load_variant_pairs(raw_dir: Path, variant_dir: Path) -> list[dict[str, str]]:
    baselines: dict[str, tuple[str, str]] = {}
    for item in sorted(raw_dir.glob("*.txt")):
        match = BASELINE_RE.match(item.name)
        if match:
            baselines[match.group("sample")] = (item.stem, item.read_text(encoding="utf-8"))
    pairs: list[dict[str, str]] = []
    for item in sorted(variant_dir.glob("*.txt")):
        match = VARIANT_RE.match(item.name)
        if not match:
            continue
        sample_id = match.group("sample")
        if sample_id not in baselines:
            continue
        baseline_label, baseline_text = baselines[sample_id]
        pairs.append(
            {
                "sample_id": sample_id,
                "variant_label": item.stem,
                "baseline_label": baseline_label,
                "baseline_text": baseline_text,
                "variant_text": item.read_text(encoding="utf-8"),
            }
        )
    return pairs


def parse_lengths(value: str) -> list[int]:
    lengths = sorted({int(part.strip()) for part in value.split(",") if part.strip()})
    return [length for length in lengths if length > 0]


def fingerprint_vector(text: str) -> list[float]:
    return CognitiveFingerprint(text).vector(normalized=True)


def pca_diagnostics(matrix: list[list[float]]) -> dict[str, Any]:
    standardized, means, stddevs = standardize_matrix(matrix)
    covariance = covariance_matrix(standardized)
    eigenvalues, eigenvectors = jacobi_eigen_symmetric(covariance)
    order = sorted(range(len(eigenvalues)), key=lambda index: eigenvalues[index], reverse=True)
    sorted_values = [max(0.0, eigenvalues[index]) for index in order]
    sorted_vectors = [[eigenvectors[row][index] for row in range(len(eigenvectors))] for index in order]
    total = sum(sorted_values)
    cumulative = 0.0
    components = []
    for rank, value in enumerate(sorted_values, start=1):
        ratio = value / total if total else 0.0
        cumulative += ratio
        components.append(
            {
                "component": rank,
                "eigenvalue": round(value, 8),
                "explained_variance_ratio": round(ratio, 8),
                "cumulative_variance_ratio": round(cumulative, 8),
                "loadings": {
                    feature: round(sorted_vectors[rank - 1][feature_index], 8)
                    for feature_index, feature in enumerate(FEATURE_NAMES)
                },
            }
        )
    values_squared = sum(value * value for value in sorted_values)
    participation_ratio = (total * total / values_squared) if values_squared else 0.0
    return {
        "sample_count": len(matrix),
        "feature_count": len(FEATURE_NAMES),
        "feature_means": {name: round(means[index], 8) for index, name in enumerate(FEATURE_NAMES)},
        "feature_stddevs": {name: round(stddevs[index], 8) for index, name in enumerate(FEATURE_NAMES)},
        "components": components,
        "components_for_90pct": components_needed(components, 0.90),
        "components_for_95pct": components_needed(components, 0.95),
        "effective_dimension_participation_ratio": round(participation_ratio, 6),
        "interpretive_note": (
            "PCA summarizes covariance geometry for the current corpus only. "
            "It is not a universal dimensionality proof."
        ),
    }


def standardize_matrix(matrix: list[list[float]]) -> tuple[list[list[float]], list[float], list[float]]:
    width = len(matrix[0])
    means = [fmean(row[index] for row in matrix) for index in range(width)]
    stddevs = []
    for index in range(width):
        variance = fmean((row[index] - means[index]) ** 2 for row in matrix)
        stddevs.append(math.sqrt(variance) or 1.0)
    standardized = [
        [(row[index] - means[index]) / stddevs[index] for index in range(width)]
        for row in matrix
    ]
    return standardized, means, stddevs


def covariance_matrix(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    width = len(matrix[0])
    denominator = max(1, n - 1)
    return [
        [
            sum(row[left] * row[right] for row in matrix) / denominator
            for right in range(width)
        ]
        for left in range(width)
    ]


def jacobi_eigen_symmetric(matrix: list[list[float]], *, max_iterations: int = 200, tolerance: float = 1e-10) -> tuple[list[float], list[list[float]]]:
    n = len(matrix)
    a = [row[:] for row in matrix]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_iterations):
        p, q, max_value = largest_off_diagonal(a)
        if max_value < tolerance:
            break
        if abs(a[p][p] - a[q][q]) < tolerance:
            angle = math.pi / 4.0
        else:
            angle = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
        c = math.cos(angle)
        s = math.sin(angle)
        app = c * c * a[p][p] - 2.0 * s * c * a[p][q] + s * s * a[q][q]
        aqq = s * s * a[p][p] + 2.0 * s * c * a[p][q] + c * c * a[q][q]
        a[p][p] = app
        a[q][q] = aqq
        a[p][q] = 0.0
        a[q][p] = 0.0
        for r in range(n):
            if r in (p, q):
                continue
            arp = c * a[r][p] - s * a[r][q]
            arq = s * a[r][p] + c * a[r][q]
            a[r][p] = a[p][r] = arp
            a[r][q] = a[q][r] = arq
        for r in range(n):
            vrp = c * v[r][p] - s * v[r][q]
            vrq = s * v[r][p] + c * v[r][q]
            v[r][p] = vrp
            v[r][q] = vrq
    return [a[index][index] for index in range(n)], v


def largest_off_diagonal(matrix: list[list[float]]) -> tuple[int, int, float]:
    n = len(matrix)
    best = (0, 1, abs(matrix[0][1]) if n > 1 else 0.0)
    for i in range(n):
        for j in range(i + 1, n):
            value = abs(matrix[i][j])
            if value > best[2]:
                best = (i, j, value)
    return best


def components_needed(components: list[dict[str, Any]], threshold: float) -> int:
    for row in components:
        if row["cumulative_variance_ratio"] >= threshold:
            return int(row["component"])
    return len(components)


def length_stability_diagnostics(texts: list[str], *, lengths: list[int], seed: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    tokens = tokenize(" ".join(texts))
    rows: list[dict[str, Any]] = []
    rng = random.Random(seed)
    for length in lengths:
        if len(tokens) < length:
            continue
        sample_count = min(30, max(3, len(tokens) // max(1, length)))
        starts = deterministic_starts(len(tokens), length, sample_count, rng)
        vectors = [fingerprint_vector(" ".join(tokens[start : start + length])) for start in starts]
        centroid = vector_mean(vectors)
        deviations = [euclidean(vector, centroid) for vector in vectors]
        rows.append(
            {
                "length_tokens": length,
                "sample_count": len(vectors),
                "mean_deviation_from_centroid": round(fmean(deviations), 6),
                "median_deviation_from_centroid": round(median(deviations), 6),
                "max_deviation_from_centroid": round(max(deviations), 6),
            }
        )
    best = min((row["mean_deviation_from_centroid"] for row in rows), default=None)
    plateau_length = None
    if best is not None:
        for row in rows:
            if row["mean_deviation_from_centroid"] <= best * 1.10:
                plateau_length = row["length_tokens"]
                break
    return rows, {
        "analysis": "minimum_text_length_stability",
        "readiness_boundary": "descriptive_only",
        "token_pool_count": len(tokens),
        "lengths_evaluated": [row["length_tokens"] for row in rows],
        "lowest_mean_deviation": best,
        "first_length_within_10pct_of_lowest_deviation": plateau_length,
        "guardrail": (
            "This is a corpus-specific stability diagnostic. It is not a universal minimum text length."
        ),
    }


def deterministic_starts(total_tokens: int, length: int, sample_count: int, rng: random.Random) -> list[int]:
    max_start = total_tokens - length
    if max_start <= 0:
        return [0]
    starts = {0, max_start}
    while len(starts) < sample_count:
        starts.add(rng.randint(0, max_start))
    return sorted(starts)


def lipschitz_diagnostics(pairs: list[dict[str, str]]) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    deltas_by_feature: dict[str, list[float]] = {name: [] for name in FEATURE_NAMES}
    for pair in pairs:
        left_vector = fingerprint_vector(pair["baseline_text"])
        right_vector = fingerprint_vector(pair["variant_text"])
        left_tokens = tokenize(pair["baseline_text"])
        right_tokens = tokenize(pair["variant_text"])
        edit_distance = word_edit_distance(left_tokens, right_tokens)
        euclidean_delta = euclidean(left_vector, right_vector)
        cosine_distance = CognitiveFingerprint.distance(left_vector, right_vector, metric="cosine")
        for index, feature in enumerate(FEATURE_NAMES):
            deltas_by_feature[feature].append(abs(right_vector[index] - left_vector[index]))
        rows.append(
            {
                "sample_id": pair["sample_id"],
                "variant_label": pair["variant_label"],
                "baseline_tokens": len(left_tokens),
                "variant_tokens": len(right_tokens),
                "word_edit_distance": edit_distance,
                "euclidean_profile_delta": round(euclidean_delta, 6),
                "cosine_profile_distance": round(cosine_distance, 6),
                "k_empirical_euclidean_per_word_edit": round(euclidean_delta / edit_distance, 8) if edit_distance else None,
            }
        )
    k_values = [row["k_empirical_euclidean_per_word_edit"] for row in rows if row["k_empirical_euclidean_per_word_edit"] is not None]
    summary = {
        "analysis": "empirical_lipschitz_sensitivity",
        "readiness_boundary": "descriptive_only",
        "pair_count": len(rows),
        "k_empirical_summary": numeric_summary(k_values),
        "profile_delta_summary": numeric_summary([row["euclidean_profile_delta"] for row in rows]),
        "edit_distance_summary": numeric_summary([row["word_edit_distance"] for row in rows]),
        "guardrail": (
            "K estimates are empirical on observed variants. They are not a formal global Lipschitz proof."
        ),
    }
    feature_sensitivity = [
        {
            "feature": feature,
            "mean_abs_delta": round(fmean(values), 8) if values else 0.0,
            "median_abs_delta": round(median(values), 8) if values else 0.0,
            "max_abs_delta": round(max(values), 8) if values else 0.0,
        }
        for feature, values in deltas_by_feature.items()
    ]
    feature_sensitivity.sort(key=lambda row: row["max_abs_delta"], reverse=True)
    return rows, summary, feature_sensitivity


def baseline_contrast_diagnostics(
    *,
    raw_rows: list[tuple[str, str]],
    variant_pairs: list[dict[str, str]],
    max_random_pairs: int,
    seed: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(seed)
    all_texts = [text for _, text in raw_rows]
    tfidf = SimpleTfidfBaseline(all_texts + [pair["variant_text"] for pair in variant_pairs])
    random_vector = DeterministicRandomVectorBaseline(seed=seed)
    rows: list[dict[str, Any]] = []

    for pair in variant_pairs:
        rows.append(
            baseline_row(
                "baseline_variant",
                pair["baseline_label"],
                pair["variant_label"],
                pair["baseline_text"],
                pair["variant_text"],
                tfidf,
                random_vector,
            )
        )

    random_pairs = list(combinations(raw_rows, 2))
    rng.shuffle(random_pairs)
    for (left_id, left_text), (right_id, right_text) in random_pairs[:max_random_pairs]:
        rows.append(
            baseline_row(
                "random_baseline_pair",
                left_id,
                right_id,
                left_text,
                right_text,
                tfidf,
                random_vector,
            )
        )

    by_type = {
        pair_type: [row for row in rows if row["pair_type"] == pair_type]
        for pair_type in ("baseline_variant", "random_baseline_pair")
    }
    summary = {
        "analysis": "baseline_contrast_diagnostics",
        "readiness_boundary": "descriptive_only",
        "row_count": len(rows),
        "baseline_variant_count": len(by_type["baseline_variant"]),
        "random_baseline_pair_count": len(by_type["random_baseline_pair"]),
        "metrics": {
            metric: {
                "baseline_variant": numeric_summary([row[metric] for row in by_type["baseline_variant"]]),
                "random_baseline_pair": numeric_summary([row[metric] for row in by_type["random_baseline_pair"]]),
                "cohens_d_random_minus_variant": round(
                    cohens_d(
                        [row[metric] for row in by_type["random_baseline_pair"]],
                        [row[metric] for row in by_type["baseline_variant"]],
                    ),
                    6,
                ),
            }
            for metric in (
                "fingerprint_cosine_distance",
                "fingerprint_euclidean_distance",
                "tfidf_cosine_distance",
                "random_vector_distance",
            )
        },
        "guardrail": (
            "Baseline contrasts compare descriptive distance distributions. They do not claim superiority "
            "or validated task performance."
        ),
    }
    return rows, summary


def baseline_row(
    pair_type: str,
    left_id: str,
    right_id: str,
    left_text: str,
    right_text: str,
    tfidf: SimpleTfidfBaseline,
    random_vector: DeterministicRandomVectorBaseline,
) -> dict[str, Any]:
    left_vector = fingerprint_vector(left_text)
    right_vector = fingerprint_vector(right_text)
    return {
        "pair_type": pair_type,
        "left_id": left_id,
        "right_id": right_id,
        "fingerprint_cosine_distance": round(CognitiveFingerprint.distance(left_vector, right_vector, metric="cosine"), 6),
        "fingerprint_euclidean_distance": round(euclidean(left_vector, right_vector), 6),
        "tfidf_cosine_distance": round(1.0 - tfidf.similarity(left_text, right_text), 6),
        "random_vector_distance": round(1.0 - random_vector.similarity(left_text, right_text), 6),
    }


def word_edit_distance(left: list[str], right: list[str]) -> int:
    if not left:
        return len(right)
    if not right:
        return len(left)
    previous = list(range(len(right) + 1))
    for i, left_token in enumerate(left, start=1):
        current = [i] + [0] * len(right)
        for j, right_token in enumerate(right, start=1):
            cost = 0 if left_token == right_token else 1
            current[j] = min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + cost)
        previous = current
    return previous[-1]


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def vector_mean(vectors: list[list[float]]) -> list[float]:
    width = len(vectors[0])
    return [fmean(vector[index] for vector in vectors) for index in range(width)]


def euclidean(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def numeric_summary(values: list[float | int | None]) -> dict[str, float | int | None]:
    numeric = [float(value) for value in values if value is not None]
    if not numeric:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None, "p95": None}
    ordered = sorted(numeric)
    p95_index = min(len(ordered) - 1, math.ceil(0.95 * len(ordered)) - 1)
    return {
        "count": len(numeric),
        "mean": round(fmean(numeric), 6),
        "median": round(median(numeric), 6),
        "min": round(min(numeric), 6),
        "max": round(max(numeric), 6),
        "p95": round(ordered[p95_index], 6),
    }


def write_pca_outputs(output_dir: Path, pca: dict[str, Any]) -> None:
    write_json(output_dir / "pca-summary.json", {key: value for key, value in pca.items() if key != "components"})
    rows = []
    for component in pca["components"]:
        row = {
            "component": component["component"],
            "eigenvalue": component["eigenvalue"],
            "explained_variance_ratio": component["explained_variance_ratio"],
            "cumulative_variance_ratio": component["cumulative_variance_ratio"],
        }
        row.update({f"loading_{name}": value for name, value in component["loadings"].items()})
        rows.append(row)
    write_csv(output_dir / "pca-components.csv", list(rows[0].keys()), rows)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_readme(
    output_dir: Path,
    manifest: dict[str, Any],
    pca: dict[str, Any],
    length_summary: dict[str, Any],
    lipschitz_summary: dict[str, Any],
    baseline_summary: dict[str, Any],
) -> None:
    text = f"""# Mathematical Evidence V1

Status: pre-review mathematical diagnostics.
Readiness boundary: `descriptive_only`.

This folder summarizes corpus-specific geometry and sensitivity behavior for
the CogniPrint v2 feature map. It does not satisfy the external review gate and
does not establish validation, authorship, provenance, AI detection, legal
status, forensic status, deterministic classification, or a universal
threshold.

## Inputs

- baseline texts: {manifest["baseline_text_count"]}
- independent holdout texts: {manifest["holdout_text_count"]}
- baseline/variant pairs: {manifest["variant_pair_count"]}
- fingerprint version: `{manifest["fingerprint_version"]}`

## Diagnostics

- PCA effective dimension: {pca["effective_dimension_participation_ratio"]}
- PCA components for 90% variance: {pca["components_for_90pct"]}
- PCA components for 95% variance: {pca["components_for_95pct"]}
- First evaluated length within 10% of the lowest mean deviation: {length_summary["first_length_within_10pct_of_lowest_deviation"]}
- Empirical K max over observed variants: {lipschitz_summary["k_empirical_summary"]["max"]}
- Baseline/variant rows: {baseline_summary["baseline_variant_count"]}
- Random baseline-pair rows: {baseline_summary["random_baseline_pair_count"]}

## Interpretation

These outputs are intended to make the mathematical evidence base more
auditable:

1. PCA describes covariance geometry of the 12 coordinates on the current
   corpus.
2. Length stability estimates how fragment size changes profile dispersion on
   the current token pool.
3. Empirical Lipschitz diagnostics estimate observed sensitivity per word edit.
4. Baseline contrasts compare CogniPrint distances with TF-IDF and deterministic
   random-vector baselines.

All interpretation remains descriptive until a valid non-owner methodological
review is archived and the manuscript validation plan is updated.
"""
    (output_dir / "README.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
