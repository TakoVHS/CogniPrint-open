"""Pure-Python distance metrics for CogniPrint profile vectors."""

from __future__ import annotations

import math
from typing import Any


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def euclidean_distance(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def manhattan_distance(left: list[float], right: list[float]) -> float:
    return sum(abs(a - b) for a, b in zip(left, right))


def mahalanobis_distance(
    left: list[float],
    right: list[float],
    reference_vectors: list[list[float]] | None = None,
) -> dict[str, Any]:
    """Return a conservative diagonal Mahalanobis-style distance.

    A full covariance estimate is not stable for tiny local studies. This uses
    per-coordinate variance when at least three reference vectors exist, and
    otherwise falls back to identity covariance with a warning.
    """

    variances = _coordinate_variances(reference_vectors or [])
    warning = None
    if not variances or len(variances) != len(left):
        variances = [1.0 for _ in left]
        warning = "identity covariance fallback; use a larger corpus for stronger covariance estimates"
    total = 0.0
    for a, b, variance in zip(left, right, variances):
        scale = variance if variance > 1e-12 else 1.0
        total += ((a - b) ** 2) / scale
    return {"value": math.sqrt(total), "warning": warning}


def wasserstein_distance_1d(left: list[float], right: list[float]) -> float:
    ordered_left = sorted(left)
    ordered_right = sorted(right)
    size = min(len(ordered_left), len(ordered_right))
    if size == 0:
        return 0.0
    return sum(abs(ordered_left[index] - ordered_right[index]) for index in range(size)) / size


def jensen_shannon_divergence(left: list[float], right: list[float]) -> float:
    p = _positive_distribution(left)
    q = _positive_distribution(right)
    if not p or not q:
        return 0.0
    midpoint = [(a + b) / 2 for a, b in zip(p, q)]
    return (_kl_divergence(p, midpoint) + _kl_divergence(q, midpoint)) / 2


def selected_metric(
    metric: str,
    left: list[float],
    right: list[float],
    reference_vectors: list[list[float]] | None = None,
) -> dict[str, Any]:
    if metric == "cosine":
        return {"metric": "cosine", "value": cosine_similarity(left, right), "kind": "similarity"}
    if metric == "euclidean":
        return {"metric": "euclidean", "value": euclidean_distance(left, right), "kind": "distance"}
    if metric == "manhattan":
        return {"metric": "manhattan", "value": manhattan_distance(left, right), "kind": "distance"}
    if metric == "mahalanobis":
        result = mahalanobis_distance(left, right, reference_vectors)
        return {"metric": "mahalanobis", "value": result["value"], "kind": "distance", "warning": result["warning"]}
    if metric == "wasserstein":
        return {"metric": "wasserstein", "value": wasserstein_distance_1d(left, right), "kind": "distance"}
    if metric == "jensen-shannon":
        return {"metric": "jensen-shannon", "value": jensen_shannon_divergence(left, right), "kind": "divergence"}
    raise ValueError(f"Unsupported metric: {metric}")


def _coordinate_variances(vectors: list[list[float]]) -> list[float]:
    if len(vectors) < 3:
        return []
    width = len(vectors[0])
    if any(len(vector) != width for vector in vectors):
        return []
    variances = []
    for index in range(width):
        values = [vector[index] for vector in vectors]
        mean = sum(values) / len(values)
        variances.append(sum((value - mean) ** 2 for value in values) / (len(values) - 1))
    return variances


def _positive_distribution(values: list[float]) -> list[float]:
    shifted = [abs(value) + 1e-12 for value in values]
    total = sum(shifted)
    if total == 0:
        return []
    return [value / total for value in shifted]


def _kl_divergence(p: list[float], q: list[float]) -> float:
    return sum(a * math.log(a / b) for a, b in zip(p, q) if a > 0 and b > 0)
