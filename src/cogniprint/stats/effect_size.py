"""Effect-size helpers for CogniPrint validation summaries."""

from __future__ import annotations

import math
from statistics import fmean


def hedges_g(reference: list[float], comparison: list[float]) -> dict[str, float | int | None]:
    """Return a conservative Hedges' g estimate for two groups."""

    left = [float(value) for value in reference]
    right = [float(value) for value in comparison]
    if len(left) < 2 or len(right) < 2:
        return {"reference_count": len(left), "comparison_count": len(right), "value": None}

    left_mean = fmean(left)
    right_mean = fmean(right)
    pooled = _pooled_std(left, right)
    if pooled == 0:
        return {"reference_count": len(left), "comparison_count": len(right), "value": 0.0}
    cohen_d = (right_mean - left_mean) / pooled
    correction = 1.0 - (3.0 / (4.0 * (len(left) + len(right)) - 9.0))
    return {
        "reference_count": len(left),
        "comparison_count": len(right),
        "value": round(cohen_d * correction, 6),
    }


def _pooled_std(left: list[float], right: list[float]) -> float:
    left_var = _sample_variance(left)
    right_var = _sample_variance(right)
    numerator = ((len(left) - 1) * left_var) + ((len(right) - 1) * right_var)
    denominator = len(left) + len(right) - 2
    if denominator <= 0:
        return 0.0
    return math.sqrt(numerator / denominator)


def _sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = fmean(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)
