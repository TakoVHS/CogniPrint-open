from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_claims_drift import find_matches
from scripts.synthesize_decision import parse_votes, resolve_decision


class DecisionScriptTests(unittest.TestCase):
    def test_parse_votes_counts_increment_and_memo(self) -> None:
        counts = parse_votes("Decision: Increment\nDecision: Memo\nDecision: Abstain\n")
        self.assertEqual(counts["increment"], 1)
        self.assertEqual(counts["memo"], 1)
        self.assertEqual(counts["abstain"], 1)

    def test_resolve_decision_increment(self) -> None:
        counts = parse_votes("Decision: Increment\nDecision: Increment\nDecision: Memo\n")
        self.assertEqual(resolve_decision(counts), "increment")

    def test_resolve_decision_ambiguous(self) -> None:
        counts = parse_votes("Decision: Increment\nDecision: Memo\nDecision: Abstain\n")
        self.assertEqual(resolve_decision(counts), "ambiguous")


class ClaimsDriftTests(unittest.TestCase):
    def test_guardrail_wording_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Do not describe this as a forensic system.", encoding="utf-8")
            errors = find_matches(root, ["README.md"])
            self.assertEqual(errors, [])

    def test_dangerous_wording_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("This system identifies authors with high accuracy.", encoding="utf-8")
            errors = find_matches(root, ["README.md"])
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
