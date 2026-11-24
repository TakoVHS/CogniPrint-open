from __future__ import annotations

import re
import unittest
from pathlib import Path


class TheoryManuscriptStructureTests(unittest.TestCase):
    def test_theorem_like_environments_are_balanced(self) -> None:
        path = Path("paper/claim-promotion-identifiability-draft.tex")
        content = path.read_text(encoding="utf-8")

        tracked = {
            "theorem",
            "proposition",
            "definition",
            "proof",
            "corollary",
            "remark",
        }
        pattern = re.compile(r"\\(begin|end)\{([^}]+)\}")
        stack: list[tuple[str, int]] = []

        for match in pattern.finditer(content):
            action, environment = match.groups()
            if environment not in tracked:
                continue
            line = content.count("\n", 0, match.start()) + 1
            if action == "begin":
                stack.append((environment, line))
                continue

            self.assertTrue(
                stack,
                msg=f"unexpected end{{{environment}}} at line {line}",
            )
            opened, opened_line = stack.pop()
            self.assertEqual(
                opened,
                environment,
                msg=(
                    f"environment mismatch: begin{{{opened}}} at line "
                    f"{opened_line} closed by end{{{environment}}} at line {line}"
                ),
            )

        self.assertEqual(
            stack,
            [],
            msg=f"unclosed theorem-like environments: {stack}",
        )

    def test_candidate_manuscript_contains_scope_judgment_section(self) -> None:
        content = Path(
            "paper/claim-promotion-identifiability-draft.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(
            r"\section{Certificate Scope Judgment (Candidate Interface)}",
            content,
        )
        self.assertIn(
            r"\begin{proposition}[Direct typed-promotion soundness]",
            content,
        )
        self.assertIn(
            r"\begin{proposition}[Non-promotion witness characterization]",
            content,
        )
        self.assertIn(
            r"\begin{proposition}[Same-target confidence-budget composition]",
            content,
        )


if __name__ == "__main__":
    unittest.main()
