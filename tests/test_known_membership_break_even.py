"""Tests for the known-membership break-even arithmetic."""

from __future__ import annotations

import importlib.util
import math
import pathlib
import random
import unittest

_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts"
    / "known_membership_break_even.py"
)
_spec = importlib.util.spec_from_file_location("kmbe", _PATH)
kmbe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kmbe)


class BreakEvenTests(unittest.TestCase):
    def test_accept_all_gate_risk_equals_prevalence(self) -> None:
        for p in (0.0, 0.01, 0.2, 0.7, 1.0):
            self.assertAlmostEqual(kmbe.certificate_risk(p, 1.0, 1.0), p)

    def test_accept_all_break_even_equals_delta(self) -> None:
        for d in (0.01, 0.1, 0.25):
            self.assertAlmostEqual(kmbe.break_even(d, 1.0, 1.0), d)
            self.assertAlmostEqual(kmbe.lift(d, 1.0, 1.0), 1.0)

    def test_break_even_is_exact_boundary(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            d = rng.uniform(0.01, 0.5)
            l_k = rng.uniform(0.01, 1.0)
            u_u = rng.uniform(0.0, 1.0)
            pe = kmbe.break_even(d, l_k, u_u)
            if pe < 1.0:
                self.assertTrue(
                    math.isclose(kmbe.certificate_risk(pe, l_k, u_u), d,
                                 rel_tol=1e-9)
                )
            for p in (pe * 0.5, pe):
                self.assertLessEqual(
                    kmbe.certificate_risk(p, l_k, u_u), d + 1e-12
                )
            if pe < 1.0:
                above = min(1.0, pe + 1e-3)
                self.assertGreater(kmbe.certificate_risk(above, l_k, u_u), d)

    def test_required_u_u_is_consistent(self) -> None:
        for p in (0.2, 0.3, 0.5):
            for l_k in (0.3, 0.6, 0.9):
                u = kmbe.required_u_u(0.1, p, l_k)
                self.assertLessEqual(
                    kmbe.certificate_risk(p, l_k, u), 0.1 + 1e-12
                )

    def test_zero_accept_n_meets_target(self) -> None:
        tail = 0.05 / 80
        for target in (0.4, 0.1, 0.0333):
            n = kmbe.zero_accept_n(target, tail)
            self.assertLessEqual(1 - tail ** (1 / n), target + 1e-12)
            self.assertGreater(1 - tail ** (1 / (n - 1)), target)

    def test_undefined_cases_are_non_numeric(self) -> None:
        self.assertIsNone(kmbe.certificate_risk(0.0, 0.0, 0.5))
        self.assertIsNone(kmbe.break_even(0.1, 0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
