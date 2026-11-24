"""Finite-sample composition certificates for a fixed product gate.

The certificate is exact up to Bonferroni coverage of two one-sided binomial
bounds. It is intentionally narrow: the known and unknown validation samples
must represent the corresponding components of the declared deployment world
class, and the deployment unknown prevalence must satisfy pi <= pi_upper.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from cogniprint.stats.evidence_bounded import (
    clopper_pearson_lower,
    clopper_pearson_upper,
)


def _probability(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def known_membership_risk(
    pi: float,
    known_accept_rate: float,
    unknown_accept_rate: float,
) -> float | None:
    """Return P(unknown | product gate accepts)."""

    pi = _probability(pi, "pi")
    a_known = _probability(known_accept_rate, "known_accept_rate")
    a_unknown = _probability(unknown_accept_rate, "unknown_accept_rate")

    numerator = pi * a_unknown
    denominator = numerator + (1.0 - pi) * a_known
    if denominator == 0.0:
        return None
    return numerator / denominator


def worst_case_known_membership_risk(
    pi_upper: float,
    known_accept_lower: float,
    unknown_accept_upper: float,
) -> float:
    """Conservative upper bound over pi<=pi_upper and acceptance-rate bounds.

    The posterior unknown risk is increasing in pi and unknown acceptance and
    decreasing in known acceptance. If the corner has zero accepted mass, the
    function returns 1.0 because no nontrivial conditional-risk certificate is
    available at that corner.
    """

    pi_upper = _probability(pi_upper, "pi_upper")
    a_known = _probability(known_accept_lower, "known_accept_lower")
    a_unknown = _probability(unknown_accept_upper, "unknown_accept_upper")

    risk = known_membership_risk(pi_upper, a_known, a_unknown)
    return 1.0 if risk is None else risk


@dataclass(frozen=True)
class ProductGateCounts:
    name: str
    known_accept_count: int
    known_total: int
    unknown_accept_count: int
    unknown_total: int

    def __post_init__(self) -> None:
        for count_name, count, total_name, total in (
            (
                "known_accept_count",
                self.known_accept_count,
                "known_total",
                self.known_total,
            ),
            (
                "unknown_accept_count",
                self.unknown_accept_count,
                "unknown_total",
                self.unknown_total,
            ),
        ):
            if not isinstance(count, int) or not isinstance(total, int):
                raise TypeError(f"{count_name} and {total_name} must be integers")
            if total < 0 or count < 0 or count > total:
                raise ValueError(f"{count_name} must lie in [0, {total_name}]")


@dataclass(frozen=True)
class ProductGateCertificate:
    name: str
    known_accept_lower: float
    unknown_accept_upper: float
    pi_upper: float
    risk_upper: float
    family_confidence: float
    per_bound_alpha: float
    known_accept_count: int
    known_total: int
    unknown_accept_count: int
    unknown_total: int

    @property
    def admissible_at_10_percent(self) -> bool:
        return self.risk_upper <= 0.10


def fixed_product_gate_certificate(
    counts: ProductGateCounts,
    pi_upper: float,
    alpha: float = 0.05,
) -> ProductGateCertificate:
    """Certify a fixed product gate at family confidence 1-alpha.

    Two one-sided confidence events are needed:
    a_known >= L_known and a_unknown <= U_unknown.
    Each receives alpha/2. By the union bound the joint event has probability
    at least 1-alpha; independence between the two confidence events is not
    required.

    Empty validation samples yield the vacuous bounds L_known=0 and/or
    U_unknown=1.
    """

    pi_upper = _probability(pi_upper, "pi_upper")
    alpha = _probability(alpha, "alpha")
    if alpha in (0.0, 1.0):
        raise ValueError("alpha must lie strictly between 0 and 1")

    per_bound_alpha = alpha / 2.0

    lower = clopper_pearson_lower(
        counts.known_accept_count,
        counts.known_total,
        per_bound_alpha,
    )
    upper = clopper_pearson_upper(
        counts.unknown_accept_count,
        counts.unknown_total,
        per_bound_alpha,
    )

    known_accept_lower = 0.0 if lower is None else lower
    unknown_accept_upper = 1.0 if upper is None else upper

    risk_upper = worst_case_known_membership_risk(
        pi_upper,
        known_accept_lower,
        unknown_accept_upper,
    )

    return ProductGateCertificate(
        name=counts.name,
        known_accept_lower=known_accept_lower,
        unknown_accept_upper=unknown_accept_upper,
        pi_upper=pi_upper,
        risk_upper=risk_upper,
        family_confidence=1.0 - alpha,
        per_bound_alpha=per_bound_alpha,
        known_accept_count=counts.known_accept_count,
        known_total=counts.known_total,
        unknown_accept_count=counts.unknown_accept_count,
        unknown_total=counts.unknown_total,
    )


def simultaneous_product_gate_certificates(
    gates: Iterable[ProductGateCounts],
    pi_upper: float,
    family_alpha: float = 0.05,
) -> list[ProductGateCertificate]:
    """Simultaneous certificates for a predeclared finite family of gates.

    For m gates there are 2m one-sided binomial bounds. Each receives
    family_alpha/(2m), giving joint coverage at least 1-family_alpha by the
    union bound. A gate may then be selected from this fixed family after the
    validation data are observed without invalidating the simultaneous event.
    """

    gates = list(gates)
    if not gates:
        raise ValueError("at least one gate is required")

    pi_upper = _probability(pi_upper, "pi_upper")
    family_alpha = _probability(family_alpha, "family_alpha")
    if family_alpha in (0.0, 1.0):
        raise ValueError("family_alpha must lie strictly between 0 and 1")

    if len({gate.name for gate in gates}) != len(gates):
        raise ValueError("gate names must be unique")

    per_bound_alpha = family_alpha / (2.0 * len(gates))
    certificates = []

    for counts in gates:
        lower = clopper_pearson_lower(
            counts.known_accept_count,
            counts.known_total,
            per_bound_alpha,
        )
        upper = clopper_pearson_upper(
            counts.unknown_accept_count,
            counts.unknown_total,
            per_bound_alpha,
        )
        known_accept_lower = 0.0 if lower is None else lower
        unknown_accept_upper = 1.0 if upper is None else upper
        certificates.append(
            ProductGateCertificate(
                name=counts.name,
                known_accept_lower=known_accept_lower,
                unknown_accept_upper=unknown_accept_upper,
                pi_upper=pi_upper,
                risk_upper=worst_case_known_membership_risk(
                    pi_upper,
                    known_accept_lower,
                    unknown_accept_upper,
                ),
                family_confidence=1.0 - family_alpha,
                per_bound_alpha=per_bound_alpha,
                known_accept_count=counts.known_accept_count,
                known_total=counts.known_total,
                unknown_accept_count=counts.unknown_accept_count,
                unknown_total=counts.unknown_total,
            )
        )

    return certificates
