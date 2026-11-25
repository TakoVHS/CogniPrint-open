"""Integrity checks for the known-membership study-plan Markdown.

This specifically guards against accidental escape-sequence corruption when
the plan is transferred between tools or language models.
"""

from __future__ import annotations

import unittest
from pathlib import Path


class KnownMembershipPlanIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.path = Path("paper/known-membership-certificates-study-plan-v0.2.md")
        self.content = self.path.read_text(encoding="utf-8")

    def test_no_control_character_corruption(self) -> None:
        bad = [
            (index, ord(char))
            for index, char in enumerate(self.content)
            if ord(char) < 32 and char not in "\n\r"
        ]
        self.assertEqual(bad, [], msg=f"control characters found: {bad[:10]}")

    def test_display_math_delimiters_are_balanced(self) -> None:
        self.assertGreater(self.content.count("$$"), 0)
        self.assertEqual(self.content.count("$$") % 2, 0)

    def test_key_latex_tokens_survive_transfer(self) -> None:
        required = (
            r"R(\tau)",
            r"\pi_U",
            r"\boxed{B_\tau",
            r"\frac{\pi_U",
            r"\pi_\tau^\star",
            r"\mathbf{1}",
            r"\boxed{\text{NO CONFIRMATORY RUN}}",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, self.content)

    def test_accept_all_reference_is_present(self) -> None:
        self.assertIn("Mandatory accept-all reference", self.content)
        self.assertIn("PROMOTE_TRIVIAL", self.content)
        self.assertIn(r"B_0(\pi_U) = \pi_U", self.content)
        self.assertIn(r"\pi_0^\star = \delta", self.content)


if __name__ == "__main__":
    unittest.main()
