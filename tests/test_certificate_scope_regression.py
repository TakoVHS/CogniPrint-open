"""Regression and property tests for fail-closed scope semantics.

These tests compare implementation outputs with the finite-world mathematical
definition rather than merely duplicating implementation branches.
"""

from __future__ import annotations

import itertools
import random
import unittest

from cogniprint.stats.certificate_scope import (
    FiniteCertificate,
    FiniteClaim,
    certificate_compatible_worlds,
    find_nonpromotion_witness,
    sharp_finite_claim_bound_under_certificates,
    worst_claim_risk_under_certificate,
)


class ScopeGapRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.certificate = FiniteCertificate(
            name="closed-set",
            target="known-family-error",
            scope=frozenset({"D0"}),
            risk_by_world={"D0": 0.05},
            bound=0.08,
            alpha=0.05,
        )
        self.claim = FiniteClaim(
            name="known-membership",
            target="unknown-contamination",
            scope=frozenset({"D0", "D1"}),
            risk_by_world={"D0": 0.0, "D1": 0.35},
            delta=0.10,
        )

    def test_worst_risk_fails_closed_on_scope_gap(self) -> None:
        with self.assertRaises(ValueError):
            worst_claim_risk_under_certificate(self.certificate, self.claim)

    def test_witness_fails_closed_on_scope_gap(self) -> None:
        with self.assertRaises(ValueError):
            find_nonpromotion_witness(self.certificate, self.claim)

    def test_compatible_worlds_fails_closed_on_scope_gap(self) -> None:
        with self.assertRaises(ValueError):
            certificate_compatible_worlds(self.certificate, self.claim)


def _brute_envelope(
    certificates: tuple[FiniteCertificate, ...],
    claim: FiniteClaim,
) -> float | None:
    worlds = [
        world
        for world in claim.scope
        if all(
            certificate.risk_by_world[world] <= certificate.bound
            for certificate in certificates
        )
    ]
    if not worlds:
        return None
    return max(claim.risk_by_world[world] for world in worlds)


class EnvelopePropertyTests(unittest.TestCase):
    def test_envelope_matches_definition_and_is_monotone(self) -> None:
        rng = random.Random(20261125)
        grid = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 1.0]

        for _ in range(300):
            names = [f"w{i}" for i in range(rng.randint(1, 5))]
            scope = frozenset(names)
            claim = FiniteClaim(
                "c",
                "claim",
                scope,
                {world: rng.choice(grid) for world in names},
                rng.choice(grid),
            )
            certificates = tuple(
                FiniteCertificate(
                    f"k{j}",
                    f"t{j}",
                    scope,
                    {world: rng.choice(grid) for world in names},
                    rng.choice(grid),
                    0.01,
                )
                for j in range(rng.randint(1, 3))
            )

            got = sharp_finite_claim_bound_under_certificates(
                certificates, claim
            )
            self.assertEqual(got, _brute_envelope(certificates, claim))

            for j, bound in itertools.product(
                range(len(certificates)), grid
            ):
                if bound < certificates[j].bound:
                    continue
                looser = list(certificates)
                certificate = certificates[j]
                looser[j] = FiniteCertificate(
                    certificate.name,
                    certificate.target,
                    certificate.scope,
                    certificate.risk_by_world,
                    bound,
                    certificate.alpha,
                )
                got_looser = sharp_finite_claim_bound_under_certificates(
                    tuple(looser), claim
                )
                if got is not None:
                    self.assertIsNotNone(got_looser)
                    assert got_looser is not None
                    self.assertGreaterEqual(got_looser, got)

    def test_envelope_is_itself_a_warrant_at_realized_risk_vector(self) -> None:
        rng = random.Random(7)
        grid = [0.0, 0.1, 0.3, 0.6, 1.0]

        for _ in range(200):
            names = [f"w{i}" for i in range(rng.randint(1, 5))]
            scope = frozenset(names)
            claim_risk = {world: rng.choice(grid) for world in names}
            certificate_risks = [
                {world: rng.choice(grid) for world in names}
                for _ in range(rng.randint(1, 3))
            ]
            claim = FiniteClaim("c", "claim", scope, claim_risk, 0.1)

            for world in names:
                certificates = tuple(
                    FiniteCertificate(
                        f"k{j}",
                        f"t{j}",
                        scope,
                        risks,
                        risks[world],
                        0.01,
                    )
                    for j, risks in enumerate(certificate_risks)
                )
                sharp = sharp_finite_claim_bound_under_certificates(
                    certificates, claim
                )
                self.assertIsNotNone(sharp)
                assert sharp is not None
                self.assertLessEqual(claim_risk[world], sharp)


if __name__ == "__main__":
    unittest.main()
