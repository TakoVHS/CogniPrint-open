"""Repository-wide Markdown/LaTeX transfer-integrity checks.

The main failure mode guarded here is language/tool escaping that turns LaTeX
commands such as \\tau, \\boxed, \\frac, or \\rho into ASCII control bytes.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_ROOTS = (ROOT / "paper", ROOT / "docs")

# Historical files may be exempt only when the corruption is explicitly
# visible in the file itself. Do not add new entries: repair new corruption
# instead. This set is intended to shrink to empty.
LEGACY_FORMAT_EXCEPTIONS = frozenset(
    {
        "docs/claim-admissibility-novelty-audit-2026-11-24.md",
    }
)

WARNING_MARKER = "**LEGACY FORMAT WARNING"

LOST_COMMAND_PATTERNS = (
    re.compile(r"(?<!\\)mathcal\s+[A-Za-z]"),
    re.compile(r"(?<!\\)boxed\s*\{"),
    re.compile(r"(?<!\\)frac\s*\{"),
    re.compile(r"(?<!\\)rho_[A-Za-z{]"),
    re.compile(r"(?<!\\)kappa_[A-Za-z{]"),
    re.compile(r"(?<!\\)(?:varnothing|vdash|subseteq|notin|neq|leq|geq)\b"),
)


def markdown_paths() -> list[Path]:
    paths: list[Path] = []
    for root in MARKDOWN_ROOTS:
        paths.extend(root.rglob("*.md"))
    return sorted(paths)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def strip_code(text: str) -> str:
    text = re.sub(r"\`\`\`.*?\`\`\`", "", text, flags=re.DOTALL)
    text = re.sub(r"\`[^\`\n]*\`", "", text)
    return text


class MarkdownMathIntegrityTests(unittest.TestCase):
    def test_exception_list_is_known_and_visible(self) -> None:
        existing = {rel(path) for path in markdown_paths()}
        self.assertTrue(LEGACY_FORMAT_EXCEPTIONS <= existing)
        for item in LEGACY_FORMAT_EXCEPTIONS:
            content = (ROOT / item).read_text(encoding="utf-8", errors="strict")
            self.assertIn(
                WARNING_MARKER,
                content,
                msg=f"{item} is exempt but has no visible legacy warning",
            )

    def test_no_new_ascii_control_bytes(self) -> None:
        for path in markdown_paths():
            item = rel(path)
            if item in LEGACY_FORMAT_EXCEPTIONS:
                continue
            raw = path.read_bytes().replace(b"\r\n", b"\n")
            bad = [
                (index, byte)
                for index, byte in enumerate(raw)
                if byte < 32 and byte != 10
            ]
            with self.subTest(path=item):
                self.assertEqual(
                    bad,
                    [],
                    msg=f"{item}: ASCII control bytes found: {bad[:10]}",
                )

    def test_display_math_delimiters_are_balanced(self) -> None:
        for path in markdown_paths():
            item = rel(path)
            if item in LEGACY_FORMAT_EXCEPTIONS:
                continue
            content = path.read_text(encoding="utf-8", errors="strict")
            with self.subTest(path=item):
                self.assertEqual(
                    content.count("$$") % 2,
                    0,
                    msg=f"{item}: unbalanced $$ display-math delimiters",
                )

    def test_obvious_lost_latex_commands_are_absent(self) -> None:
        for path in markdown_paths():
            item = rel(path)
            if item in LEGACY_FORMAT_EXCEPTIONS:
                continue
            content = strip_code(
                path.read_text(encoding="utf-8", errors="strict")
            )
            hits: list[str] = []
            for pattern in LOST_COMMAND_PATTERNS:
                hits.extend(match.group(0) for match in pattern.finditer(content))
            with self.subTest(path=item):
                self.assertEqual(
                    hits,
                    [],
                    msg=f"{item}: possible lost LaTeX backslashes: {hits[:10]}",
                )


if __name__ == "__main__":
    unittest.main()
