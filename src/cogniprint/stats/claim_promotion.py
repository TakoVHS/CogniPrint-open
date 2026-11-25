"""Claim-promotion identifiability utilities.

The functions here support finite counterexamples and exact algebraic
demonstrations. They do not establish novelty and do not authorize Stage B.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum
from typing import Mapping, Sequence


def _probability(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def total_variation(
    law_a: Mapping[str, float],
    law_b: Mapping[str, float],
) -> float:
    """Total variation distance between two finite probability laws."""

    keys = set(law_a) | set(law_b)
    mass_a = fsum(float(law_a.get(key, 0.0)) for key in keys)
    mass_b = fsum(float(law_b.get(key, 0.0)) for key in keys)
    if abs(mass_a - 1.0) > 1e-12 or abs(mass_b - 1.0) > 1e-12:
        raise ValueError("laws must each sum to one")
    if any(float(law_a.get(key, 0.0)) < 0.0 for key in keys):
        raise ValueError("law_a contains negative mass")
    if any(float(law_b.get(key, 0.0)) < 0.0 for key in keys):
        raise ValueError("law_b contains negative mass")
    return 0.5 * fsum(
        abs(float(law_a.get(key, 0.0)) - float(law_b.get(key, 0.0)))
        for key in keys
    )


def equal_prior_binary_bayes_error(tv_distance: float) -> float:
    """Optimal equal-prior binary testing error from total variation."""

    tv_distance = _probability(tv_distance, "tv_distance")
    return 0.5 * (1.0 - tv_distance)


def camouflaged_mixture_selective_risk(
    unknown_fraction: float,
    known_selective_risk: float,
) -> float:
    """Risk under exact evidence-law camouflage.

    Assumptions:
    - unknown and known observations have the same acceptance probability
      because the acceptance rule is measurable through an evidence channel
      whose law is identical in both groups;
    - every accepted unknown is an error for known-family classification;
    - known accepted examples have selective risk known_selective_risk.

    Then the unknown fraction among accepted examples equals its prior fraction
    and total selective risk is
        pi + (1-pi) * r_known.
    """

    pi = _probability(unknown_fraction, "unknown_fraction")
    risk = _probability(known_selective_risk, "known_selective_risk")
    return pi + (1.0 - pi) * risk


@dataclass(frozen=True)
class BlackwellToyExample:
    known_full_law: dict[str, float]
    unknown_full_law: dict[str, float]
    known_channel_law: dict[str, float]
    unknown_channel_law: dict[str, float]
    full_tv: float
    channel_tv: float
    full_bayes_error: float
    channel_bayes_error: float


def blackwell_garbling_counterexample() -> BlackwellToyExample:
    """Return a finite experiment where compression destroys K-vs-U information.

    K: mass on a,b. U: mass on c,d.
    Channel: a,c -> z1 and b,d -> z2.

    Full X separates K/U perfectly, while the compressed channel laws coincide.
    """

    known_full = {"a": 0.5, "b": 0.5, "c": 0.0, "d": 0.0}
    unknown_full = {"a": 0.0, "b": 0.0, "c": 0.5, "d": 0.5}
    known_channel = {"z1": 0.5, "z2": 0.5}
    unknown_channel = {"z1": 0.5, "z2": 0.5}
    full_tv = total_variation(known_full, unknown_full)
    channel_tv = total_variation(known_channel, unknown_channel)
    return BlackwellToyExample(
        known_full_law=known_full,
        unknown_full_law=unknown_full,
        known_channel_law=known_channel,
        unknown_channel_law=unknown_channel,
        full_tv=full_tv,
        channel_tv=channel_tv,
        full_bayes_error=equal_prior_binary_bayes_error(full_tv),
        channel_bayes_error=equal_prior_binary_bayes_error(channel_tv),
    )


def claim_family_is_down_closed(
    admissible_claims: Sequence[str],
    implication_edges: Sequence[tuple[str, str]],
) -> bool:
    """Check down-closure for a finite claim poset.

    Each edge is (weaker, stronger), meaning stronger logically implies weaker.
    """

    admissible = set(admissible_claims)
    changed = True
    required_weaker: dict[str, set[str]] = {}
    for weaker, stronger in implication_edges:
        required_weaker.setdefault(stronger, set()).add(weaker)

    # Compute transitive weaker requirements.
    while changed:
        changed = False
        for stronger, weaker_set in list(required_weaker.items()):
            expanded = set(weaker_set)
            for weaker in list(weaker_set):
                expanded.update(required_weaker.get(weaker, set()))
            if expanded != weaker_set:
                required_weaker[stronger] = expanded
                changed = True

    for stronger in admissible:
        if not required_weaker.get(stronger, set()).issubset(admissible):
            return False
    return True
