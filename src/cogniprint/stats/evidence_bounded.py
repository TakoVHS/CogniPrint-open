"""Evidence-Bounded Inference theory utilities.

These helpers implement algebraic certificates from the theory draft. They do
not estimate calibration quality, fit models, or authorize scientific claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


def _probability(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def selective_risk_upper_bound(threshold: float, epsilon: float) -> float:
    """Return min(1, 1 - threshold + epsilon).

    The certificate requires a uniform top-label calibration defect epsilon.
    ECE is not a valid substitute for epsilon.
    """

    threshold = _probability(threshold, "threshold")
    epsilon = _probability(epsilon, "epsilon")
    return min(1.0, max(0.0, 1.0 - threshold + epsilon))


def certified_correctness_lower_bound(threshold: float, epsilon: float) -> float:
    """Return the certified correctness lower bound max(0, threshold-epsilon)."""

    threshold = _probability(threshold, "threshold")
    epsilon = _probability(epsilon, "epsilon")
    return max(0.0, threshold - epsilon)


def threshold_for_target_risk(delta: float, epsilon: float) -> float | None:
    """Return a sufficient threshold for target selective risk delta.

    Returns None when the certificate would require a threshold above one.
    This means the theorem cannot certify the target risk; it does not prove
    the model's actual risk exceeds delta.
    """

    delta = _probability(delta, "delta")
    epsilon = _probability(epsilon, "epsilon")
    required = 1.0 - delta + epsilon
    return required if required <= 1.0 else None


def coverage_lower_bound_from_mean_confidence(
    mean_confidence: float,
    threshold: float,
) -> float:
    """Lower-bound P(confidence >= threshold) from E[confidence].

    For threshold < 1:
        coverage >= max(0, (mean_confidence-threshold)/(1-threshold)).
    At threshold == 1, mean confidence 1 implies coverage 1; otherwise the
    mean alone gives no positive lower bound.
    """

    mean_confidence = _probability(mean_confidence, "mean_confidence")
    threshold = _probability(threshold, "threshold")
    if threshold == 1.0:
        return 1.0 if mean_confidence == 1.0 else 0.0
    return max(0.0, (mean_confidence - threshold) / (1.0 - threshold))


def conformal_singleton_risk_upper_bound(
    alpha: float,
    singleton_coverage: float,
) -> float | None:
    """Bound singleton selective risk from marginal conformal validity.

    If marginal miscoverage is at most alpha and singleton acceptance coverage
    is kappa > 0, then selective risk is at most min(1, alpha/kappa).
    Returns None when kappa == 0 because selective risk is undefined.
    """

    alpha = _probability(alpha, "alpha")
    singleton_coverage = _probability(singleton_coverage, "singleton_coverage")
    if singleton_coverage == 0.0:
        return None
    return min(1.0, alpha / singleton_coverage)


def uniform_calibration_defect(
    confidences: Sequence[float],
    correctness_probabilities: Sequence[float],
) -> float:
    """Exact finite-space L-infinity defect between confidence and correctness."""

    if len(confidences) != len(correctness_probabilities):
        raise ValueError("confidences and correctness_probabilities must align")
    if not confidences:
        raise ValueError("at least one state is required")
    defects = []
    for confidence, correctness in zip(confidences, correctness_probabilities):
        confidence = _probability(confidence, "confidence")
        correctness = _probability(correctness, "correctness_probability")
        defects.append(abs(confidence - correctness))
    return max(defects)


@dataclass(frozen=True)
class FiniteSelectiveSummary:
    coverage: float
    selective_risk: float | None
    calibration_defect: float
    theorem_bound: float


def finite_space_selective_summary(
    weights: Sequence[float],
    confidences: Sequence[float],
    correctness_probabilities: Sequence[float],
    threshold: float,
) -> FiniteSelectiveSummary:
    """Evaluate the theorem exactly on a finite probability space."""

    if not (len(weights) == len(confidences) == len(correctness_probabilities)):
        raise ValueError("weights, confidences, and correctness probabilities must align")
    if not weights:
        raise ValueError("at least one state is required")

    threshold = _probability(threshold, "threshold")
    checked_weights = [float(weight) for weight in weights]
    if any(weight < 0.0 for weight in checked_weights):
        raise ValueError("weights must be non-negative")
    total = sum(checked_weights)
    if total <= 0.0:
        raise ValueError("weights must have positive total mass")
    norm_weights = [weight / total for weight in checked_weights]

    checked_conf = [_probability(value, "confidence") for value in confidences]
    checked_corr = [
        _probability(value, "correctness_probability")
        for value in correctness_probabilities
    ]

    epsilon = uniform_calibration_defect(checked_conf, checked_corr)
    accepted_mass = 0.0
    accepted_error_mass = 0.0
    for weight, confidence, correctness in zip(
        norm_weights,
        checked_conf,
        checked_corr,
    ):
        if confidence >= threshold:
            accepted_mass += weight
            accepted_error_mass += weight * (1.0 - correctness)

    risk = None
    if accepted_mass > 0.0:
        risk = accepted_error_mass / accepted_mass

    return FiniteSelectiveSummary(
        coverage=accepted_mass,
        selective_risk=risk,
        calibration_defect=epsilon,
        theorem_bound=selective_risk_upper_bound(threshold, epsilon),
    )


def false_known_rate(
    accepted: Iterable[bool],
    is_unknown: Iterable[bool],
) -> float | None:
    """Compute P(accepted | unknown) from aligned boolean sequences."""

    accepted_values = list(accepted)
    unknown_values = list(is_unknown)
    if len(accepted_values) != len(unknown_values):
        raise ValueError("accepted and is_unknown must align")

    unknown_count = sum(bool(value) for value in unknown_values)
    if unknown_count == 0:
        return None
    false_known = sum(
        bool(a) and bool(u) for a, u in zip(accepted_values, unknown_values)
    )
    return false_known / unknown_count
