"""Confidence interval helpers for lightweight validation summaries."""

from __future__ import annotations

import math


def percentile_interval(values: list[float], *, confidence: float = 0.95) -> tuple[float, float]:
    """Return a percentile interval without external dependencies."""

    if not values:
        raise ValueError("percentile_interval requires at least one value")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    ordered = sorted(float(value) for value in values)
    alpha = (1.0 - confidence) / 2.0
    lower = _quantile(ordered, alpha)
    upper = _quantile(ordered, 1.0 - alpha)
    return lower, upper


def _quantile(ordered: list[float], probability: float) -> float:
    if len(ordered) == 1:
        return ordered[0]
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction
