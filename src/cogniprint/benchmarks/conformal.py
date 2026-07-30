"""Development-only class-conditional split conformal UNKNOWN logic."""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from statistics import fmean
from typing import Any, Callable, Iterable, Sequence

Record = dict[str, Any]
VectorFn = Callable[[Record], list[float]]


def _finite_vector(vector: Sequence[float], *, name: str) -> list[float]:
    if not vector:
        raise ValueError(f"{name} must be non-empty")
    values = [float(value) for value in vector]
    if any(not math.isfinite(value) for value in values):
        raise ValueError(f"{name} must contain only finite values")
    return values


def _normalize(vector: Sequence[float]) -> list[float]:
    values = _finite_vector(vector, name="vector")
    norm = math.sqrt(sum(value * value for value in values))
    if norm <= 1e-15:
        raise ValueError("zero-norm vectors are invalid for cosine evaluation")
    return [value / norm for value in values]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("cosine vectors must be non-empty and equal width")
    left_n = _normalize(left)
    right_n = _normalize(right)
    return max(-1.0, min(1.0, sum(a * b for a, b in zip(left_n, right_n))))


@dataclass(frozen=True)
class ConformalModel:
    classes: tuple[str, ...]
    centroids: dict[str, tuple[float, ...]]
    calibration_scores: dict[str, tuple[float, ...]]
    alpha: float
    method: str = "class_conditional_split_conformal_on_cosine_nonconformity"

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "classes": list(self.classes),
            "calibration_counts": {
                label: len(self.calibration_scores[label]) for label in self.classes
            },
            "alpha": self.alpha,
            "method": self.method,
            "centroids_persisted": False,
            "calibration_scores_persisted": False,
        }


def _fit_centroids(
    records: Iterable[Record],
    vector_fn: VectorFn,
) -> dict[str, tuple[float, ...]]:
    by_class: dict[str, list[list[float]]] = defaultdict(list)
    width: int | None = None
    for record in records:
        label = str(record.get("model_family") or "").strip()
        if not label:
            raise ValueError("record is missing model_family")
        vector = _normalize(vector_fn(record))
        if width is None:
            width = len(vector)
        elif len(vector) != width:
            raise ValueError("inconsistent vector width")
        by_class[label].append(vector)
    if not by_class:
        raise ValueError("reference records are empty")

    centroids: dict[str, tuple[float, ...]] = {}
    for label in sorted(by_class):
        vectors = by_class[label]
        mean = [
            fmean(vector[index] for vector in vectors)
            for index in range(len(vectors[0]))
        ]
        centroids[label] = tuple(_normalize(mean))
    return centroids


def fit_class_conditional_conformal(
    reference: list[Record],
    calibration: list[Record],
    vector_fn: VectorFn,
    *,
    alpha: float = 0.05,
) -> ConformalModel:
    """Fit reference centroids and class-conditional calibration scores."""

    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0,1)")
    if not reference or not calibration:
        raise ValueError("reference and calibration must be non-empty")
    centroids = _fit_centroids(reference, vector_fn)
    scores: dict[str, list[float]] = {label: [] for label in centroids}
    for record in calibration:
        label = str(record.get("model_family") or "").strip()
        if label not in centroids:
            raise ValueError(f"calibration class absent from reference: {label!r}")
        score = 1.0 - cosine_similarity(vector_fn(record), centroids[label])
        scores[label].append(score)
    missing = [label for label, values in scores.items() if not values]
    if missing:
        raise ValueError(f"calibration has no records for classes: {missing}")
    return ConformalModel(
        classes=tuple(sorted(centroids)),
        centroids=centroids,
        calibration_scores={
            label: tuple(sorted(scores[label])) for label in sorted(scores)
        },
        alpha=float(alpha),
    )


def conformal_p_values(
    model: ConformalModel,
    vector: Sequence[float],
) -> dict[str, float]:
    candidate = _finite_vector(vector, name="candidate_vector")
    result: dict[str, float] = {}
    for label in model.classes:
        score = 1.0 - cosine_similarity(candidate, model.centroids[label])
        calibration = model.calibration_scores[label]
        tail = sum(value >= score for value in calibration)
        result[label] = (1.0 + tail) / (len(calibration) + 1.0)
    return result


def predict_conformal_unknown(
    model: ConformalModel,
    vector: Sequence[float],
    *,
    minimum_evidence_passed: bool,
) -> dict[str, Any]:
    """Return KNOWN or one of three explicit UNKNOWN outcomes."""

    if not minimum_evidence_passed:
        return {
            "decision": "UNKNOWN_INSUFFICIENT_EVIDENCE",
            "predicted_class": None,
            "p_values": {},
            "alpha": model.alpha,
            "calibrated_probability": False,
        }

    p_values = conformal_p_values(model, vector)
    accepted = sorted(
        label for label, p_value in p_values.items() if p_value > model.alpha
    )
    if len(accepted) == 1:
        decision = "KNOWN"
        predicted = accepted[0]
    elif not accepted:
        decision = "UNKNOWN_OOD"
        predicted = None
    else:
        decision = "UNKNOWN_AMBIGUOUS"
        predicted = None
    return {
        "decision": decision,
        "predicted_class": predicted,
        "p_values": {
            label: round(p_values[label], 12) for label in model.classes
        },
        "alpha": model.alpha,
        "calibrated_probability": False,
    }
