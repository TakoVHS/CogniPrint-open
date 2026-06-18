from __future__ import annotations

import unittest
from pathlib import Path


class SiteLinkTests(unittest.TestCase):
    def test_site_pages_reference_evidence_and_review(self) -> None:
        site_root = Path(__file__).resolve().parents[2] / "TakoVHS.github.io"
        if not site_root.exists():
            self.skipTest("Sibling website repo is not available.")

        software = (site_root / "software" / "index.html").read_text(encoding="utf-8")
        evidence = (site_root / "evidence" / "index.html").read_text(encoding="utf-8")
        review = (site_root / "review" / "index.html").read_text(encoding="utf-8")

        for text in (software, evidence, review):
            self.assertIn("/evidence/", text)
            self.assertIn("/review/", text)

        self.assertIn("evidence/public-benchmark-v1.1", evidence)
        self.assertIn("validation/statistical-validation-v1.2", evidence)
        self.assertIn("validation/conventional-stylometry-baseline-v1", evidence)
        self.assertIn("docs/current-state-summary.md", review)
        self.assertIn("docs/evidence-dossier.md", review)
        self.assertIn("docs/validation-upgrade-plan.md", review)
        self.assertIn("docs/external-review/dispatch-2026-05-11.md", review)


if __name__ == "__main__":
    unittest.main()
