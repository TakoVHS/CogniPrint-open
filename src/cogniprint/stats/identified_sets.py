"""Identified-set claim-admissibility utilities.

This module implements exact finite/synthetic calculations for the theory
draft. It does not estimate unidentified quantities from RAID Stage A data.
"""

from __future__ import annotations

from dataclasses import dataclass


def _probability(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


@dataclass(frozen=True)
class RiskInterval:
    lower: float
    upper: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.lower <= self.upper <= 1.0:
            raise ValueError("risk interval must satisfy 0 <= lower <= upper <= 1")


def posterior_unknown_risk(
    unknown_fraction: float,
    known_accept_rate: float,
    unknown_accept_rate: float,
) -> float | None:
    """Return P(unknown | accepted) under a two-component mixture."""

    pi = _probability(unknown_fraction, "unknown_fraction")
    a_known = _probability(known_accept_rate, "known_accept_rate")
    a_unknown = _probability(unknown_accept_rate, "unknown_accept_rate")

    denominator = (1.0 - pi) * a_known + pi * a_unknown
    if denominator == 0.0:
        return None
    return pi * a_unknown / denominator


def identified_unknown_risk_interval(
    pi_lower: float,
    pi_upper: float,
    known_accept_rate: float,
    unknown_accept_rate: float,
) -> RiskInterval | None:
    """Exact identified interval induced by a prior interval for unknown mass.

    The acceptance rates are treated as fixed model/world-class assumptions.
    For non-negative acceptance rates, posterior unknown risk is monotone in pi,
    so endpoint evaluation gives the sharp interval whenever acceptance is
    defined at both endpoints.
    """

    lo = _probability(pi_lower, "pi_lower")
    hi = _probability(pi_upper, "pi_upper")
    if lo > hi:
        raise ValueError("pi_lower must not exceed pi_upper")

    low_risk = posterior_unknown_risk(
        lo,
        known_accept_rate,
        unknown_accept_rate,
    )
    high_risk = posterior_unknown_risk(
        hi,
        known_accept_rate,
        unknown_accept_rate,
    )

    if low_risk is None or high_risk is None:
        return None
    return RiskInterval(lower=low_risk, upper=high_risk)


def robust_claim_admissible(
    risk_interval: RiskInterval,
    delta: float,
) -> bool:
    """Return whether every risk in the identified set is <= delta."""

    delta = _probability(delta, "delta")
    return risk_interval.upper <= delta


def critical_unknown_fraction(
    delta: float,
    known_accept_rate: float,
    unknown_accept_rate: float,
) -> float | None:
    """Largest pi whose posterior unknown risk is at most delta.

    Solves
      pi*a_u / ((1-pi)*a_k + pi*a_u) <= delta.

    Returns:
    - 1 when unknowns are never accepted and knowns have positive acceptance;
    - None when no accepted population exists for any mixture;
    - otherwise the sharp boundary in [0,1].
    """

    delta = _probability(delta, "delta")
    a_known = _probability(known_accept_rate, "known_accept_rate")
    a_unknown = _probability(unknown_accept_rate, "unknown_accept_rate")

    if a_known == 0.0 and a_unknown == 0.0:
        return None
    if a_unknown == 0.0:
        return 1.0
    if a_known == 0.0:
        return 0.0 if delta < 1.0 else 1.0

    numerator = delta * a_known
    denominator = a_unknown * (1.0 - delta) + delta * a_known
    return min(1.0, max(0.0, numerator / denominator))


def product_channel_interval_is_refinement(
    coarse: RiskInterval,
    refined: RiskInterval,
) -> bool:
    """Check the interval consequence of exact channel refinement."""

    return coarse.lower <= refined.lower and refined.upper <= coarse.upper
