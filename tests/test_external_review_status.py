import tempfile
import unittest
from pathlib import Path

from scripts.check_external_review_status import build_status, validate_response


VALID_BODY = """
# External Review Response

- Reviewer: Example Reviewer
- Affiliation or role: External methods reviewer
- Review date: 2026-05-05
- Version reviewed: commit abc123
- Reviewer independence: external reviewer; no project-owner self-review
- External review status: complete

## Summary Assessment

The current package is methodologically clear enough for a cautious descriptive manuscript pass, provided the text does not claim inference beyond the documented evidence layers. The public growth layer and independent holdout layer materially improve auditability, but their limitations should remain visible.

## Methods And Reproducibility

The methods and provenance boundaries are understandable. The package distinguishes local campaigns, public controlled growth, and independent holdout validation. The reproducibility path is credible for a reviewer who can run the documented scripts and inspect the generated JSON summaries.

## Evidence And Validation

The empirical row count, holdout layer, correction layer, and conventional baseline are useful. They support descriptive manuscript wording, but they do not support forensic, authorship, or production decision claims. The corrected p-values should remain diagnostic.

## Limitations And Claims

The main remaining limitation is external replication and broader multilingual holdout work. The English-only holdout should be described as a first independent source-family check, not as final validation.

## Required Changes Before Manuscript Wording

No blocking evidence change is required for a cautious descriptive manuscript pass.

## Recommendation

Proceed with cautious descriptive manuscript pass.
"""


class ExternalReviewStatusTests(unittest.TestCase):
    def test_valid_response_counts_toward_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer-a.md"
            path.write_text(VALID_BODY, encoding="utf-8")

            status = build_status(Path(tmp))

        self.assertEqual(status["valid_review_count"], 1)
        self.assertTrue(status["independent_external_review_present"])

    def test_template_like_response_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer-a.md"
            path.write_text(
                "\n".join([
                    "- Reviewer: <required>",
                    "- Affiliation or role: <required>",
                    "- Review date: YYYY-MM-DD",
                    "- Version reviewed: <commit>",
                    "- Reviewer independence: internal",
                    "- External review status: pending",
                ]),
                encoding="utf-8",
            )

            review = validate_response(path)

        self.assertFalse(review["valid"])
        self.assertTrue(review["errors"])


if __name__ == "__main__":
    unittest.main()
