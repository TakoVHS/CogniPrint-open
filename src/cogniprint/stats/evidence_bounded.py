"""Evidence-Bounded Inference theory utilities.

These helpers implement algebraic certificates from the theory draft. They do
not estimate calibration quality, fit models, or authorize scientific claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, lgamma, log
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


@dataclass(frozen=True)
class ThresholdRiskCertificate:
    """Finite-sample selective-risk certificate for one fixed threshold."""

    threshold: float
    accepted_count: int
    error_count: int
    empirical_risk: float | None
    upper_risk_bound: float | None
    confidence_level: float
    per_threshold_alpha: float


def _logsumexp(values: Sequence[float]) -> float:
    """Stable log(sum(exp(values))) for a non-empty sequence."""

    if not values:
        raise ValueError("values must be non-empty")
    maximum = max(values)
    if maximum == float("-inf"):
        return maximum
    return maximum + log(sum(exp(value - maximum) for value in values))


def _binomial_logpmf(k: int, n: int, probability: float) -> float:
    """Stable log PMF for Binomial(n, probability)."""

    probability = _probability(probability, "probability")
    if k < 0 or k > n:
        return float("-inf")
    if probability == 0.0:
        return 0.0 if k == 0 else float("-inf")
    if probability == 1.0:
        return 0.0 if k == n else float("-inf")

    return (
        lgamma(n + 1)
        - lgamma(k + 1)
        - lgamma(n - k + 1)
        + k * log(probability)
        + (n - k) * log(1.0 - probability)
    )


def _binomial_tail_probability(
    start: int,
    stop: int,
    n: int,
    probability: float,
) -> float:
    """Stable inclusive binomial probability over integer range [start, stop]."""

    if start > stop:
        return 0.0
    logs = [
        _binomial_logpmf(k, n, probability)
        for k in range(start, stop + 1)
    ]
    log_total = _logsumexp(logs)
    if log_total == float("-inf"):
        return 0.0
    return min(1.0, max(0.0, exp(log_total)))


def _binomial_cdf(errors: int, trials: int, probability: float) -> float:
    """Return P[X <= errors] for X ~ Binomial(trials, probability).

    The implementation chooses the numerically smaller tail and evaluates it
    in log space. This avoids overflow from explicit binomial coefficients at
    validation sizes in the thousands.
    """

    if errors < 0:
        return 0.0
    if errors >= trials:
        return 1.0
    probability = _probability(probability, "probability")
    if probability == 0.0:
        return 1.0
    if probability == 1.0:
        return 0.0

    mean = trials * probability
    if errors < mean:
        return _binomial_tail_probability(
            0,
            errors,
            trials,
            probability,
        )

    upper_tail = _binomial_tail_probability(
        errors + 1,
        trials,
        n=trials,
        probability=probability,
    )
    return min(1.0, max(0.0, 1.0 - upper_tail))


def clopper_pearson_upper(
    error_count: int,
    trial_count: int,
    alpha: float = 0.05,
) -> float | None:
    """Exact one-sided Clopper-Pearson upper confidence bound.

    For E ~ Binomial(n, r), returns U such that the one-sided confidence
    statement r <= U has coverage at least 1-alpha.

    Returns None when trial_count == 0 because selective risk is undefined
    without accepted calibration observations.
    """

    if not isinstance(error_count, int) or not isinstance(trial_count, int):
        raise TypeError("error_count and trial_count must be integers")
    if trial_count < 0:
        raise ValueError("trial_count must be non-negative")
    if error_count < 0 or error_count > trial_count:
        raise ValueError("error_count must lie in [0, trial_count]")
    alpha = _probability(alpha, "alpha")
    if alpha in (0.0, 1.0):
        raise ValueError("alpha must lie strictly between 0 and 1")
    if trial_count == 0:
        return None
    if error_count == trial_count:
        return 1.0
    if error_count == 0:
        return 1.0 - alpha ** (1.0 / trial_count)

    # Solve P_{p=U}(X <= error_count) = alpha.
    # The binomial CDF is monotone decreasing in p for fixed error_count < n.
    low = 0.0
    high = 1.0
    for _ in range(80):
        mid = (low + high) / 2.0
        cdf = _binomial_cdf(error_count, trial_count, mid)
        if cdf > alpha:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0



def clopper_pearson_lower(
    success_count: int,
    trial_count: int,
    alpha: float = 0.05,
) -> float | None:
    """Exact one-sided Clopper-Pearson lower confidence bound.

    For X ~ Binomial(n, p), returns L such that the one-sided confidence
    statement p >= L has coverage at least 1-alpha.

    Returns None when trial_count == 0 because no nontrivial lower bound can
    be learned from an empty sample.
    """

    if not isinstance(success_count, int) or not isinstance(trial_count, int):
        raise TypeError("success_count and trial_count must be integers")
    if trial_count < 0:
        raise ValueError("trial_count must be non-negative")
    if success_count < 0 or success_count > trial_count:
        raise ValueError("success_count must lie in [0, trial_count]")
    alpha = _probability(alpha, "alpha")
    if alpha in (0.0, 1.0):
        raise ValueError("alpha must lie strictly between 0 and 1")
    if trial_count == 0:
        return None
    if success_count == 0:
        return 0.0
    if success_count == trial_count:
        return alpha ** (1.0 / trial_count)

    # Solve P_{p=L}(X >= success_count) = alpha.
    # The binomial survival probability is monotone increasing in p.
    low = 0.0
    high = 1.0
    for _ in range(80):
        mid = (low + high) / 2.0
        survival = 1.0 - _binomial_cdf(
            success_count - 1,
            trial_count,
            mid,
        )
        if survival < alpha:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0

def fixed_threshold_risk_certificate(
    confidences: Sequence[float],
    correct: Sequence[bool],
    threshold: float,
    alpha: float = 0.05,
) -> ThresholdRiskCertificate:
    """Certify selective risk for a threshold fixed before calibration data.

    Assumptions:
    - the predictor and threshold are fixed independently of this calibration
      sample;
    - calibration examples are i.i.d. from the target distribution;
    - correctness is evaluated against the target label.

    Conditional on the number of accepted calibration examples, accepted
    errors are binomial with success probability equal to the population
    selective risk of the fixed acceptance rule.
    """

    if len(confidences) != len(correct):
        raise ValueError("confidences and correct must align")
    threshold = _probability(threshold, "threshold")
    alpha = _probability(alpha, "alpha")
    if alpha in (0.0, 1.0):
        raise ValueError("alpha must lie strictly between 0 and 1")

    accepted_count = 0
    error_count = 0
    for confidence, is_correct in zip(confidences, correct):
        confidence = _probability(confidence, "confidence")
        if confidence >= threshold:
            accepted_count += 1
            error_count += int(not bool(is_correct))

    empirical_risk = None
    if accepted_count:
        empirical_risk = error_count / accepted_count

    return ThresholdRiskCertificate(
        threshold=threshold,
        accepted_count=accepted_count,
        error_count=error_count,
        empirical_risk=empirical_risk,
        upper_risk_bound=clopper_pearson_upper(
            error_count,
            accepted_count,
            alpha=alpha,
        ),
        confidence_level=1.0 - alpha,
        per_threshold_alpha=alpha,
    )


def simultaneous_threshold_certificates(
    confidences: Sequence[float],
    correct: Sequence[bool],
    thresholds: Sequence[float],
    family_alpha: float = 0.05,
) -> list[ThresholdRiskCertificate]:
    """Simultaneous finite-grid certificates via Bonferroni control.

    The threshold grid must be specified before looking at the calibration
    labels. Each threshold receives alpha/m, so with probability at least
    1-family_alpha every returned population selective-risk upper bound is
    valid simultaneously. A threshold may then be selected data-dependently
    from this fixed grid without invalidating that simultaneous statement.
    """

    if len(confidences) != len(correct):
        raise ValueError("confidences and correct must align")
    family_alpha = _probability(family_alpha, "family_alpha")
    if family_alpha in (0.0, 1.0):
        raise ValueError("family_alpha must lie strictly between 0 and 1")
    if not thresholds:
        raise ValueError("at least one threshold is required")

    checked = [_probability(value, "threshold") for value in thresholds]
    if len(set(checked)) != len(checked):
        raise ValueError("threshold grid must not contain duplicates")

    per_alpha = family_alpha / len(checked)
    return [
        fixed_threshold_risk_certificate(
            confidences,
            correct,
            threshold,
            alpha=per_alpha,
        )
        for threshold in checked
    ]


def select_max_coverage_certified_threshold(
    certificates: Sequence[ThresholdRiskCertificate],
    target_risk: float,
    min_accepted: int = 1,
) -> ThresholdRiskCertificate | None:
    """Select the empirically highest-coverage threshold with certified risk.

    This selector is valid when the certificates were constructed
    simultaneously over a threshold grid fixed independently of calibration
    labels.
    """

    target_risk = _probability(target_risk, "target_risk")
    if min_accepted < 1:
        raise ValueError("min_accepted must be at least 1")

    eligible = [
        certificate
        for certificate in certificates
        if certificate.accepted_count >= min_accepted
        and certificate.upper_risk_bound is not None
        and certificate.upper_risk_bound <= target_risk
    ]
    if not eligible:
        return None

    # More accepted calibration examples approximates higher retained coverage.
    # On ties, prefer the lower threshold, then the smaller risk bound.
    return max(
        eligible,
        key=lambda certificate: (
            certificate.accepted_count,
            -certificate.threshold,
            -float(certificate.upper_risk_bound),
        ),
    )
