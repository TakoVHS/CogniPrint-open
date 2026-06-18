from __future__ import annotations

import unittest

from scripts.sync_decision_gate_issue import extract_decision_line, render_votes, strip_decision_metadata


class SyncDecisionGateIssueTests(unittest.TestCase):
    def test_extract_decision_line_exact(self) -> None:
        self.assertEqual(extract_decision_line("Decision: Increment"), "Decision: Increment")
        self.assertEqual(extract_decision_line("Decision: Memo"), "Decision: Memo")
        self.assertEqual(extract_decision_line("Decision: Abstain"), "Decision: Abstain")

    def test_extract_decision_line_ignores_non_exact(self) -> None:
        self.assertIsNone(extract_decision_line("Decision: increment maybe"))
        self.assertIsNone(extract_decision_line("I think increment"))

    def test_extract_decision_line_rejects_template_comment_with_multiple_votes(self) -> None:
        payload = "Decision: Increment\nor\nDecision: Memo\nor\nDecision: Abstain"
        self.assertIsNone(extract_decision_line(payload))

    def test_render_votes_skips_comments_without_decision(self) -> None:
        payload = [
            {"body": "No vote here", "author": {"login": "alice"}, "createdAt": "2026-04-30T00:00:00Z"},
            {"body": "Decision: Memo\nReasoning: Still sensitive.", "author": {"login": "bob"}, "createdAt": "2026-04-30T01:00:00Z"},
        ]
        rendered = render_votes(payload)
        self.assertIn("Reviewer: bob", rendered)
        self.assertIn("Decision: Memo", rendered)
        self.assertNotIn("Reviewer: alice", rendered)

    def test_render_votes_does_not_duplicate_decision_line_in_reasoning(self) -> None:
        payload = [
            {
                "body": "Decision: Increment\n\nReasoning: Enough for a bounded increment.",
                "author": {"login": "alice"},
                "createdAt": "2026-04-30T00:00:00Z",
            }
        ]
        rendered = render_votes(payload)
        self.assertEqual(rendered.splitlines().count("Decision: Increment"), 1)
        self.assertIn("Enough for a bounded increment.", rendered)

    def test_strip_decision_metadata_keeps_reasoning_text(self) -> None:
        body = "Decision: Abstain\nReasoning:\nNeed another reviewer."
        self.assertEqual(strip_decision_metadata(body), "Need another reviewer.")


if __name__ == "__main__":
    unittest.main()
