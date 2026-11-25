"""Finite-world prototype of Certificate Scope Judgment.

This module is a machine-checkable prototype for the candidate interface. It
does not establish novelty and does not replace the population-level theory.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


def _probability(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def _validate_scope_map(
    scope: frozenset[str],
    values: Mapping[str, float],
    name: str,
) -> None:
    missing = scope.difference(values)
    if missing:
        raise ValueError(f"{name} missing worlds: {sorted(missing)}")
    for world in scope:
        _probability(float(values[world]), f"{name}[{world}]")


@dataclass(frozen=True)
class FiniteCertificate:
    """A realized upper-bound certificate over a finite world class."""

    name: str
    target: str
    scope: frozenset[str]
    risk_by_world: Mapping[str, float]
    bound: float
    alpha: float

    def __post_init__(self) -> None:
        _probability(self.bound, "bound")
        _probability(self.alpha, "alpha")
        _validate_scope_map(self.scope, self.risk_by_world, "risk_by_world")


@dataclass(frozen=True)
class FiniteClaim:
    """A downstream claim with its own target risk and tolerance."""

    name: str
    target: str
    scope: frozenset[str]
    risk_by_world: Mapping[str, float]
    delta: float

    def __post_init__(self) -> None:
        _probability(self.delta, "delta")
        _validate_scope_map(self.scope, self.risk_by_world, "risk_by_world")


@dataclass(frozen=True)
class SameTargetComposition:
    target: str
    scope: frozenset[str]
    bound: float
    alpha: float


def direct_static_compatible(
    certificate: FiniteCertificate,
    claim: FiniteClaim,
) -> bool:
    """Check direct target/scope compatibility.

    Direct compatibility is deliberately strict:
    - the claim scope must be contained in the certificate scope;
    - the target identifiers must match;
    - finite-world target values must agree throughout the claim scope.
    """

    if not claim.scope.issubset(certificate.scope):
        return False
    if certificate.target != claim.target:
        return False
    return all(
        float(certificate.risk_by_world[world])
        == float(claim.risk_by_world[world])
        for world in claim.scope
    )


def runtime_direct_promotion_allowed(
    certificate: FiniteCertificate,
    claim: FiniteClaim,
) -> bool:
    """Return whether the realized direct promotion discharges its threshold."""

    return (
        direct_static_compatible(certificate, claim)
        and certificate.bound <= claim.delta
    )


def certificate_compatible_worlds(
    certificate: FiniteCertificate,
    claim: FiniteClaim,
) -> frozenset[str]:
    """Claim worlds satisfying the realized certificate inequality.

    Fails closed on a scope gap. The single-certificate API delegates to the
    same coverage-checked implementation used by heterogeneous composition so
    the two paths cannot silently drift apart.
    """

    return heterogeneous_compatible_worlds((certificate,), claim)

def find_nonpromotion_witness(
    certificate: FiniteCertificate,
    claim: FiniteClaim,
) -> str | None:
    """Return one compatible world where the downstream claim is unsafe.

    Fails closed on a scope gap through the heterogeneous implementation.
    """

    return find_heterogeneous_composition_witness((certificate,), claim)

def worst_claim_risk_under_certificate(
    certificate: FiniteCertificate,
    claim: FiniteClaim,
) -> float | None:
    """Finite-world supremum used by the witness characterization.

    Returns None when no compatible world remains and fails closed on a scope
    gap through the heterogeneous implementation.
    """

    return sharp_finite_claim_bound_under_certificates((certificate,), claim)

def compose_same_target(
    first: FiniteCertificate,
    second: FiniteCertificate,
) -> SameTargetComposition:
    """Baseline union-bound composition for two same-target certificates."""

    if first.target != second.target:
        raise ValueError("same-target composition requires matching targets")

    scope = first.scope.intersection(second.scope)
    if not scope:
        raise ValueError("certificate scopes do not overlap")

    return SameTargetComposition(
        target=first.target,
        scope=frozenset(scope),
        bound=min(first.bound, second.bound),
        alpha=min(1.0, first.alpha + second.alpha),
    )


def _require_claim_scope_coverage(
    certificates: tuple[FiniteCertificate, ...],
    claim: FiniteClaim,
) -> None:
    """Fail closed unless every certificate covers the full claim scope."""

    if not certificates:
        raise ValueError("at least one certificate is required")

    for certificate in certificates:
        missing = claim.scope.difference(certificate.scope)
        if missing:
            raise ValueError(
                f"certificate {certificate.name!r} does not cover claim worlds: "
                f"{sorted(missing)}"
            )


def heterogeneous_compatible_worlds(
    certificates: tuple[FiniteCertificate, ...],
    claim: FiniteClaim,
) -> frozenset[str]:
    """Claim worlds satisfying all realized certificate inequalities.

    This function deliberately requires full claim-scope coverage. Silently
    intersecting scopes would turn an uncovered deployment world into an
    apparently harmless absence of a witness.
    """

    _require_claim_scope_coverage(certificates, claim)
    return frozenset(
        world
        for world in claim.scope
        if all(
            float(certificate.risk_by_world[world]) <= certificate.bound
            for certificate in certificates
        )
    )


def sharp_finite_claim_bound_under_certificates(
    certificates: tuple[FiniteCertificate, ...],
    claim: FiniteClaim,
) -> float | None:
    """Sharp finite-world claim-risk envelope under realized certificate bounds.

    The returned value is the maximum downstream claim risk among all declared
    claim worlds that satisfy every realized certificate inequality. It is a
    finite-world quantitative warrant. None means the realized constraints
    leave no compatible world; callers should treat that case as unresolved
    rather than silently promoting.
    """

    worlds = heterogeneous_compatible_worlds(certificates, claim)
    if not worlds:
        return None
    return max(float(claim.risk_by_world[world]) for world in worlds)


def find_heterogeneous_composition_witness(
    certificates: tuple[FiniteCertificate, ...],
    claim: FiniteClaim,
) -> str | None:
    """Find a fully covered world satisfying every bound but violating claim."""

    for world in sorted(heterogeneous_compatible_worlds(certificates, claim)):
        if float(claim.risk_by_world[world]) > claim.delta:
            return world
    return None

def composed_confidence_budget(
    certificates: tuple[FiniteCertificate, ...],
) -> float:
    """Union-bound failure budget for warranted heterogeneous composition."""

    if not certificates:
        raise ValueError("at least one certificate is required")
    return min(1.0, sum(certificate.alpha for certificate in certificates))
