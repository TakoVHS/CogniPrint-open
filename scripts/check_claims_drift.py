#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

DANGEROUS_PATTERNS = [
    r"(?i)(determin(e|es|ing)|identif(y|ies|ying))\s+(author|authorship)",
    r"(?i)(forensic|legal|court)\s+(decision|determination|instrument|system)",
    r"(?i)high(\s*[-–])?accuracy(\s+rate)?",
    r"(?i)production(\s*)ready(\s+detector|system)",
    r"(?i)guarantee(\s+correct|\s+accuracy)?",
    r"(?i)(90%|99%|100%)\s+(accuracy|confidence|correct)",
]

DEFAULT_GLOBS = [
    "README.md",
    "docs/**/*.md",
    "evidence/**/*.md",
    "site/**/*.html",
]

ALLOW_IF_NEAR = (
    "do not",
    "should not",
    "not claim",
    "guardrail",
    "forbidden",
    "non-claim",
    "non-claims",
    "does not",
    "not be presented",
    "not currently",
    "avoid",
    "insufficiently reinforced",
    "explicit non-claim",
    "explicit non-claims",
    "legal conclusions",
    "source guarantees",
    "guaranteed source classification",
    "theorem-level guarantees",
    "must not be marketed",
    "should not currently be described as",
)


def find_matches(root: Path, globs: list[str]) -> list[str]:
    errors: list[str] = []
    for pattern in globs:
        candidate = Path(pattern)
        if candidate.is_absolute():
            paths = [candidate]
        else:
            paths = list(root.glob(pattern))
        for path in paths:
            if path.name == "check_claims_drift.py":
                continue
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            lowered = text.casefold()
            for expr in DANGEROUS_PATTERNS:
                regex = re.compile(expr)
                for match in regex.finditer(text):
                    start = max(0, match.start() - 160)
                    end = min(len(text), match.end() + 160)
                    window = lowered[start:end]
                    if any(token in window for token in ALLOW_IF_NEAR):
                        continue
                    errors.append(f"{path}: dangerous claim drift match `{match.group(0)}`")
                    break
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check tracked docs and site text for dangerous claims drift.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--additional", nargs="*", default=[], help="Additional files or glob patterns relative to root.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    errors = find_matches(root, DEFAULT_GLOBS + list(args.additional))
    if errors:
        print("Claims drift check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Claims drift check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
