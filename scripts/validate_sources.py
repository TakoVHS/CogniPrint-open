"""Validate lightweight CogniPrint source provenance records."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "source_name:",
    "source_ref:",
    "source_class:",
    "license:",
    "acquisition_date:",
    "usage_note:",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate CogniPrint input source metadata.")
    parser.add_argument("--sources", type=Path, default=Path("workspace/input/SOURCES.md"))
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    sources = (repo_root / args.sources).resolve() if not args.sources.is_absolute() else args.sources
    errors: list[str] = []

    if not sources.exists():
        errors.append(f"Missing sources file: {sources}")
    else:
        text = sources.read_text(encoding="utf-8")
        if "source-id:" not in text:
            errors.append("SOURCES.md must contain at least one `source-id:` record.")
        for field in REQUIRED_FIELDS:
            if field not in text:
                errors.append(f"SOURCES.md missing required field marker: {field}")

    tracked = _tracked_files(repo_root)
    private_tracked = [path for path in tracked if path.startswith("workspace/input/private/")]
    if private_tracked:
        errors.append("Private input paths are tracked: " + ", ".join(private_tracked))

    public_inputs = [
        path
        for path in tracked
        if path.startswith("workspace/input/public/") and not path.endswith("/.gitkeep")
    ]
    if public_inputs and sources.exists():
        text = sources.read_text(encoding="utf-8")
        for path in public_inputs:
            if Path(path).name not in text and path not in text:
                errors.append(f"Tracked public input has no obvious source reference in SOURCES.md: {path}")

    if errors:
        for error in errors:
            print(f"source-validation-error: {error}", file=sys.stderr)
        return 1
    print(f"Source provenance validation passed: {sources}")
    return 0


def _tracked_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "workspace/input"],
        cwd=repo_root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
