from __future__ import annotations

import unittest

from scripts.decision_gate_status import summarize_comments


class DecisionGateStatusTests(unittest.TestCase):
    def test_summarize_comments_counts_only_single_vote_comments(self) -> None:
        comments = [
            {
                "body": "Decision: Increment\nReasoning: Enough.",
                "author": {"login": "alice"},
                "createdAt": "2026-04-30T00:00:00Z",
            },
            {
                "body": "Decision: Increment\nor\nDecision: Memo",
                "author": {"login": "owner"},
                "createdAt": "2026-04-30T01:00:00Z",
            },
        ]
        summary = summarize_comments(comments)
        self.assertEqual(summary["comment_count"], 2)
        self.assertEqual(summary["decision_comment_count"], 1)
        self.assertEqual(summary["decision_comments"][0]["author"], "alice")
        self.assertEqual(summary["decision_comments"][0]["decision"], "increment")


if __name__ == "__main__":
    unittest.main()
