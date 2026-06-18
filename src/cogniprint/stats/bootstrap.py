"""Bootstrap utilities for lightweight CogniPrint validation summaries."""

from __future__ import annotations

import random
from statistics import fmean

from .confidence_intervals import percentile_interval


def bootstrap_mean_interval(
    values: list[float],
    *,
    confidence: float = 0.95,
    resamples: int = 2000,
    seed: int = 1729,
) -> dict[str, float | int | None]:
    """Return a percentile bootstrap interval for the sample mean."""

    cleaned = [float(value) for value in values]
    if not cleaned:
        return {
            "count": 0,
            "mean": None,
            "confidence": confidence,
            "resamples": resamples,
            "lower": None,
            "upper": None,
        }

    rng = random.Random(seed)
    samples = []
    for _ in range(resamples):
        draw = [rng.choice(cleaned) for _ in range(len(cleaned))]
        samples.append(fmean(draw))
    lower, upper = percentile_interval(samples, confidence=confidence)
    return {
        "count": len(cleaned),
        "mean": round(fmean(cleaned), 6),
        "confidence": confidence,
        "resamples": resamples,
        "lower": round(lower, 6),
        "upper": round(upper, 6),
    }
