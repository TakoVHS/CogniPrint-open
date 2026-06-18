from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.sync_external_review_issues import (
    is_external_review_issue,
    parse_issue_form_field,
    render_response,
    sync_issues,
)


LONG_TEXT = (
    "This section gives a substantive external review note with enough detail to "
    "be useful for the readiness gate. It comments on clarity, reproducibility, "
    "validation boundaries, and why the current package should stay descriptive. "
) * 3


def issue_body(status: str = "complete") -> str:
    return "\n".join(
        [
            "### Reviewer",
            "",
            "Example Reviewer",
            "",
            "### Affiliation or role",
            "",
            "External methods reviewer",
            "",
            "### Review date",
            "",
            "2026-05-06",
            "",
            "### Version reviewed",
            "",
            "v0.3.1-reviewer-20260506",
            "",
            "### Reviewer independence",
            "",
            "external reviewer; no project-owner self-review",
            "",
            "### External review status",
            "",
            status,
            "",
            "### Summary Assessment",
            "",
            LONG_TEXT,
            "",
            "### Methods And Reproducibility",
            "",
            LONG_TEXT,
            "",
            "### Evidence And Validation",
            "",
            LONG_TEXT,
            "",
            "### Limitations And Claims",
            "",
            LONG_TEXT,
            "",
            "### Required Changes Before Manuscript Wording",
            "",
            "No blocking change is required before a cautious descriptive manuscript pass.",
            "",
            "### Recommendation",
            "",
            "proceed with cautious descriptive manuscript pass",
            "",
        ]
    )


class SyncExternalReviewIssuesTests(unittest.TestCase):
    def test_parse_issue_form_field(self) -> None:
        self.assertEqual(parse_issue_form_field(issue_body(), "Reviewer"), "Example Reviewer")
        self.assertEqual(parse_issue_form_field(issue_body(), "Missing"), "")

    def test_external_review_title_filter(self) -> None:
        self.assertTrue(is_external_review_issue({"title": "[EXTERNAL REVIEW] methods"}))
        self.assertFalse(is_external_review_issue({"title": "[REVIEW] methods"}))

    def test_render_response_from_complete_issue(self) -> None:
        rendered = render_response(
            {
                "number": 42,
                "title": "[EXTERNAL REVIEW] methods",
                "body": issue_body(),
                "author": {"login": "external-reviewer"},
                "createdAt": "2026-05-06T00:00:00Z",
                "url": "https://github.com/TakoVHS/CogniPrint/issues/42",
            }
        )
        self.assertIsNotNone(rendered)
        assert rendered is not None
        self.assertIn("- Reviewer: Example Reviewer", rendered)
        self.assertIn("## Evidence And Validation", rendered)

    def test_render_response_rejects_incomplete_status(self) -> None:
        rendered = render_response(
            {
                "number": 42,
                "title": "[EXTERNAL REVIEW] methods",
                "body": issue_body(status="incomplete"),
                "author": {"login": "external-reviewer"},
            }
        )
        self.assertIsNone(rendered)

    def test_sync_skips_owner_issue_and_writes_external_issue(self) -> None:
        issues = [
            {
                "number": 1,
                "title": "[EXTERNAL REVIEW] owner",
                "body": issue_body(),
                "author": {"login": "TakoVHS"},
                "createdAt": "2026-05-06T00:00:00Z",
                "url": "https://github.com/TakoVHS/CogniPrint/issues/1",
            },
            {
                "number": 2,
                "title": "[EXTERNAL REVIEW] external",
                "body": issue_body(),
                "author": {"login": "external-reviewer"},
                "createdAt": "2026-05-06T00:00:00Z",
                "url": "https://github.com/TakoVHS/CogniPrint/issues/2",
            },
        ]
        with tempfile.TemporaryDirectory() as tmp:
            synced = sync_issues(issues, Path(tmp), {"TakoVHS"})
            files = list(Path(tmp).glob("*.md"))

        self.assertEqual(len(synced), 1)
        self.assertEqual(len(files), 1)
        self.assertTrue(synced[0]["valid_after_sync"])


if __name__ == "__main__":
    unittest.main()
