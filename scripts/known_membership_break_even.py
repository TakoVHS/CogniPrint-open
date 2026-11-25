"""Break-even analysis for the known-membership certificate (study plan v0.2).

Pure arithmetic on the certificate formula; no data are read. It shows:

1. the accept-everything gate (L_K = U_U = 1) has risk exactly pi_U and
   break-even prevalence exactly delta, so any pi_U <= delta is certified
   without a detector;
2. the minimum per-family sample size that can make U_U small enough in the
   informative region pi_U > delta, under the full Bonferroni allocation;
3. the detector "lift" pi*(tau) / delta, the quantity a design must report.

Usage:
    python scripts/known_membership_break_even.py [--delta 0.10]
        [--alpha 0.05] [--thresholds 10] [--known-strata 5]
        [--unknown-strata 3]
"""

from __future__ import annotations

import argparse
import math


def certificate_risk(pi_u: float, l_k: float, u_u: float) -> float | None:
    """B = pi_U U_U / ((1 - pi_U) L_K + pi_U U_U); None if undefined."""

    den = (1.0 - pi_u) * l_k + pi_u * u_u
    if den <= 0.0:
        return None
    return pi_u * u_u / den


def break_even(delta: float, l_k: float, u_u: float) -> float | None:
    """Largest pi with B <= delta; None when L_K = U_U = 0 (no acceptance)."""

    den = u_u * (1.0 - delta) + delta * l_k
    if den <= 0.0:
        return None
    return min(1.0, delta * l_k / den)


def lift(delta: float, l_k: float, u_u: float) -> float | None:
    """pi*(tau) / pi*(accept-all). Above 1 means the detector adds value."""

    pe = break_even(delta, l_k, u_u)
    base = break_even(delta, 1.0, 1.0)
    if pe is None or base is None or base == 0.0:
        return None
    return pe / base


def required_u_u(delta: float, pi_u: float, l_k: float) -> float:
    """Largest U_U with B <= delta (from pi U (1-delta) <= delta (1-pi) L)."""

    if pi_u == 0.0:
        return 1.0
    return min(1.0, delta * (1.0 - pi_u) * l_k / (pi_u * (1.0 - delta)))


def zero_accept_n(u_target: float, tail: float) -> int | None:
    """Smallest n whose zero-success one-sided CP upper bound <= u_target.

    The exact bound with 0 successes is 1 - tail**(1/n).
    """

    if u_target >= 1.0:
        return 1
    if u_target <= 0.0:
        return None
    return math.ceil(math.log(tail) / math.log(1.0 - u_target))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--delta", type=float, default=0.10)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--thresholds", type=int, default=10)
    ap.add_argument("--known-strata", type=int, default=5)
    ap.add_argument("--unknown-strata", type=int, default=3)
    a = ap.parse_args()

    n_bounds = a.thresholds * (a.known_strata + a.unknown_strata)
    tail = a.alpha / n_bounds
    grid = [0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50]

    print(f"delta={a.delta}  alpha={a.alpha}  bounds={n_bounds}  "
          f"per-bound tail={tail:.6f}\n")

    print("1) Accept-all gate (L_K = U_U = 1): risk = pi_U, "
          f"break-even = {break_even(a.delta, 1.0, 1.0):.4f}")
    print("   pi_U   risk   certified?")
    for p in grid:
        r = certificate_risk(p, 1.0, 1.0)
        print(f"   {p:<5}  {r:.3f}  {'PROMOTE' if r <= a.delta else 'ABSTAIN'}")

    print("\n2) Even a gate that accepts every unknown (U_U = 1) passes "
          "when pi_U is small:")
    print("   L_K   pi_U   B      certified?")
    for l_k in (0.3, 0.6, 0.9):
        for p in (0.02, 0.05):
            b = certificate_risk(p, l_k, 1.0)
            print(f"   {l_k:<4}  {p:<5}  {b:.3f}  "
                  f"{'PROMOTE' if b <= a.delta else 'ABSTAIN'}")

    print("\n3) Informative region only (pi_U > delta): U_U needed and the")
    print("   minimum n per unknown family even if it accepts zero unknowns")
    print("   pi_U   L_K   U_U needed   min n")
    for p in grid:
        if p <= a.delta:
            continue
        for l_k in (0.3, 0.6, 0.9):
            u = required_u_u(a.delta, p, l_k)
            print(f"   {p:<5}  {l_k:<4}  {u:<11.4f}  {zero_accept_n(u, tail)}")

    print("\n4) Lift over accept-all, pi*(tau)/delta, at illustrative points")
    print("   (M2-like point: known acceptance ~0.6, unknown acceptance ~0.5)")
    print("   L_K   U_U    pi*     lift")
    for l_k, u_u in ((0.6, 0.5), (0.6, 0.2), (0.6, 0.05), (0.9, 0.01)):
        pe = break_even(a.delta, l_k, u_u)
        print(f"   {l_k:<4}  {u_u:<5}  {pe:.4f}  {lift(a.delta, l_k, u_u):.2f}")


if __name__ == "__main__":
    main()
