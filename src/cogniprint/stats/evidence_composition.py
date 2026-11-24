"""Finite exact utilities for sharp evidence-channel composition.

The population theorem is measure-theoretic. These utilities provide finite
counterexamples and regression tests for its set-theoretic consequences.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable


@dataclass(frozen=True)
class FiniteCompositionWorld:
    name: str
    risk: float
    coarse_signature: Hashable
    conditional_signature: Hashable

    def __post_init__(self) -> None:
        if not 0.0 <= float(self.risk) <= 1.0:
            raise ValueError("risk must be in [0, 1]")


@dataclass(frozen=True)
class CompositionReport:
    coarse_risks: tuple[float, ...]
    product_risks: tuple[float, ...]
    coarse_upper: float | None
    product_upper: float | None
    strict_shrink: bool
    strict_worst_case_gain: bool


def _sorted_unique(values: Iterable[float]) -> tuple[float, ...]:
    return tuple(sorted(set(float(value) for value in values)))


def composition_report(
    worlds: Iterable[FiniteCompositionWorld],
    observed_coarse_signature: Hashable,
    observed_conditional_signature: Hashable,
) -> CompositionReport:
    """Return exact finite identified-risk sets before and after composition."""

    worlds = list(worlds)
    coarse = [
        world
        for world in worlds
        if world.coarse_signature == observed_coarse_signature
    ]
    product = [
        world
        for world in coarse
        if world.conditional_signature == observed_conditional_signature
    ]

    coarse_risks = _sorted_unique(world.risk for world in coarse)
    product_risks = _sorted_unique(world.risk for world in product)
    coarse_upper = max(coarse_risks) if coarse_risks else None
    product_upper = max(product_risks) if product_risks else None

    return CompositionReport(
        coarse_risks=coarse_risks,
        product_risks=product_risks,
        coarse_upper=coarse_upper,
        product_upper=product_upper,
        strict_shrink=set(product_risks) < set(coarse_risks),
        strict_worst_case_gain=(
            coarse_upper is not None
            and product_upper is not None
            and product_upper < coarse_upper
        ),
    )


def robustly_admissible(upper_risk: float | None, delta: float) -> bool:
    if not 0.0 <= float(delta) <= 1.0:
        raise ValueError("delta must be in [0, 1]")
    return upper_risk is not None and upper_risk <= delta


def delta_separating(
    worlds: Iterable[FiniteCompositionWorld],
    observed_coarse_signature: Hashable,
    observed_conditional_signature: Hashable,
    delta: float,
) -> bool:
    """Exact finite version of the unsafe-world elimination criterion."""

    worlds = list(worlds)
    unsafe_coarse = [
        world
        for world in worlds
        if world.coarse_signature == observed_coarse_signature
        and world.risk > delta
    ]
    unsafe_product = [
        world
        for world in unsafe_coarse
        if world.conditional_signature == observed_conditional_signature
    ]
    return bool(unsafe_coarse) and not unsafe_product


def conditionally_redundant(
    worlds: Iterable[FiniteCompositionWorld],
    observed_coarse_signature: Hashable,
) -> bool:
    """Check world-invariant conditional signature inside the coarse fiber."""

    signatures = {
        world.conditional_signature
        for world in worlds
        if world.coarse_signature == observed_coarse_signature
    }
    return len(signatures) <= 1
