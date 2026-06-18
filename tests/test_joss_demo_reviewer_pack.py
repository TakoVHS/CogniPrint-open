from __future__ import annotations

import py_compile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class JossDemoReviewerPackTests(unittest.TestCase):
    def test_streamlit_demo_compiles_without_importing_streamlit(self) -> None:
        py_compile.compile(str(ROOT / "demo" / "app.py"), doraise=True)

    def test_external_review_template_matches_gate_parser_fields(self) -> None:
        text = (ROOT / "docs" / "external-review" / "response-template.md").read_text(encoding="utf-8")
        for field in [
            "Reviewer:",
            "Affiliation or role:",
            "Review date:",
            "Version reviewed:",
            "Reviewer independence:",
            "External review status:",
        ]:
            self.assertIn(field, text)

    def test_reviewer_reproducibility_script_exists_and_is_bounded(self) -> None:
        path = ROOT / "scripts" / "reproducibility_check.sh"
        text = path.read_text(encoding="utf-8")
        self.assertIn("make mathematical-evidence-v1", text)
        self.assertIn("make human-paraphrase-test", text)
        self.assertIn("make cross-genre-test", text)
        self.assertIn("readiness_boundary", text)

    def test_joss_stub_keeps_descriptive_boundary(self) -> None:
        text = (ROOT / "paper" / "joss.md").read_text(encoding="utf-8").casefold()
        self.assertIn("descriptive research workstation", text)
        self.assertIn("does not provide author identity decisions", text)


if __name__ == "__main__":
    unittest.main()
