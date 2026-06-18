#!/usr/bin/env python3
"""Guard CogniPrint wording against unsupported public claims."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
    "release_artifacts",
    "venv",
    "workspace",
}
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".tex",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
PUBLIC_HINTS = (
    "README",
    "project_brief",
    "docs/",
    "paper/",
    "site/",
    "slides/",
    "apps/web/src/",
)
INTERNAL_HINTS = (
    ".github/workflows/",
    "apps/api/",
    "scripts/",
    "src/",
    "tests/",
)
REPORT_PATH_HINTS = (
    "docs/claims-guard-report.md",
)
GUARD_SELF_PATHS = (
    "scripts/cogniprint_claims_guard.py",
    "tests/test_cogniprint_claims_guard.py",
)
ALLOW_CONTEXT_MARKERS = (
    "avoid",
    "avoid:",
    "bounded",
    "do not describe",
    "do not",
    "does not",
    "forbidden",
    "guardrail",
    "must not",
    "no ",
    "not ",
    "not as",
    "not being presented as",
    "not claim",
    "outputs are not",
    "without claiming",
    "examples of language to avoid",
    "do not send as claims",
    "old arxiv-pending wording",
    "should not currently be described",
    "не делай",
    "не называй",
    "не описывай",
    "запрещ",
)


@dataclass(frozen=True)
class Term:
    phrase: str
    category: str
    public_only: bool = True


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    path: str
    line_number: int
    term: str
    line: str


LEGACY_TERMS = (
    Term("Aletheia", "legacy", public_only=False),
    Term("Linguistic DNA", "legacy", public_only=False),
    Term("FractalTruth", "legacy", public_only=False),
    Term("Fractal Truth", "legacy", public_only=False),
    Term("LabelShield", "legacy", public_only=False),
    Term("TesserakT", "legacy", public_only=False),
)

RISK_TERMS = (
    Term("AI detector", "unsupported-claim"),
    Term("arXiv ID:", "unsupported-claim"),
    Term("arXiv submission pending", "unsupported-claim"),
    Term("authorship attribution", "unsupported-claim"),
    Term("authorship detector", "unsupported-claim"),
    Term("bot detection", "unsupported-claim"),
    Term("definitive attribution", "unsupported-claim"),
    Term("definitive detector", "unsupported-claim"),
    Term("final judgment", "unsupported-claim"),
    Term("forensic authorship", "unsupported-claim"),
    Term("forensic proof", "unsupported-claim"),
    Term("grant awarded", "unsupported-claim"),
    Term("guaranteed authorship", "unsupported-claim"),
    Term("guaranteed classification", "unsupported-claim"),
    Term("guaranteed identification", "unsupported-claim"),
    Term("human vs AI", "unsupported-claim"),
    Term("legal proof", "unsupported-claim"),
    Term("origin verdict", "unsupported-claim"),
    Term("production detector", "unsupported-claim"),
    Term("provenance detector", "unsupported-claim"),
    Term("recipient route approved", "unsupported-claim"),
    Term("Schmidt-funded", "unsupported-claim"),
    Term("source guarantee", "unsupported-claim"),
    Term("source proof", "unsupported-claim"),
    Term("validated detector", "unsupported-claim"),
)


def classify_path(path: str) -> str:
    if any(path == hint or path.startswith(hint) for hint in REPORT_PATH_HINTS):
        return "generated-report"
    if any(hint in path for hint in PUBLIC_HINTS):
        return "public"
    if any(hint in path for hint in INTERNAL_HINTS):
        return "internal"
    return "unknown"


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(root).parts):
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {"Makefile", "Dockerfile"}:
            continue
        try:
            sample = path.read_bytes()[:2048]
        except OSError:
            continue
        if b"\0" in sample:
            continue
        yield path


def allowed_context(line: str) -> bool:
    lowered = line.casefold()
    return any(marker in lowered for marker in ALLOW_CONTEXT_MARKERS)


def allowed_context_window(lines: list[str], index: int) -> bool:
    start = max(index - 12, 0)
    window = "\n".join(lines[start : index + 1])
    return allowed_context(window)


def scan(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    terms = list(LEGACY_TERMS) + list(RISK_TERMS)
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        if rel in GUARD_SELF_PATHS:
            continue
        path_class = classify_path(rel)
        if path_class == "generated-report":
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, 1):
            lowered = line.casefold()
            for term in terms:
                if term.phrase.casefold() not in lowered:
                    continue
                if term.public_only and path_class == "internal":
                    severity = "internal-ok"
                elif term.category == "legacy":
                    severity = "blocker"
                elif allowed_context_window(lines, line_number - 1):
                    severity = "allow-review"
                else:
                    severity = "review"
                findings.append(
                    Finding(
                        severity=severity,
                        category=term.category,
                        path=rel,
                        line_number=line_number,
                        term=term.phrase,
                        line=line.strip()[:240],
                    )
                )
    return findings


def render(findings: list[Finding]) -> str:
    order = ("blocker", "review", "allow-review", "internal-ok")
    grouped = {key: [finding for finding in findings if finding.severity == key] for key in order}
    output = ["# CogniPrint Claims Guard Report", "", "## Summary", ""]
    for key in order:
        output.append(f"- {key}: {len(grouped[key])}")
    output.append("")

    for key in order:
        output.extend([f"## {key}", ""])
        if not grouped[key]:
            output.extend(["No findings.", ""])
            continue
        for finding in grouped[key]:
            output.extend(
                [
                    f"### `{finding.path}:{finding.line_number}`",
                    "",
                    f"- Term: `{finding.term}`",
                    f"- Category: `{finding.category}`",
                    "",
                    f"> {finding.line}",
                    "",
                ]
            )
    return "\n".join(output).rstrip() + "\n"


def should_fail(findings: list[Finding], fail_on: str) -> bool:
    if fail_on == "none":
        return False
    if fail_on == "blocker":
        return any(finding.severity == "blocker" for finding in findings)
    return any(finding.severity in {"blocker", "review"} for finding in findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--write-report", default="")
    parser.add_argument(
        "--fail-on",
        choices=("none", "blocker", "review"),
        default="review",
        help="Minimum finding severity that should fail the command.",
    )
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    findings = scan(root)
    report = render(findings)
    if args.write_report:
        output = root / args.write_report
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    else:
        print(report)

    if should_fail(findings, args.fail_on):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
