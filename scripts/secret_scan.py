#!/usr/bin/env python3
"""Scan tracked files and, optionally, Git history for high-risk secret patterns."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


ROOT = Path(__file__).resolve().parents[1]
SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".mp4",
    ".ico",
    ".woff",
    ".woff2",
    ".zip",
    ".gz",
    ".tar",
}
ALLOW_MARKERS = (
    "example",
    "placeholder",
    "redacted",
    "dummy",
    "changeme",
    "not-a-real",
    "test value",
    "test_only",
    "${",
    "<secret",
    "<token",
    "<password",
    "<api-key",
    "<api_key",
)


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]


RULES = (
    Rule("stripe_secret_key", re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    Rule("stripe_webhook_secret", re.compile(r"\bwhsec_[A-Za-z0-9]{16,}\b")),
    Rule("openai_api_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    Rule("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    Rule("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    Rule("huggingface_token", re.compile(r"\bhf_[A-Za-z0-9]{20,}\b")),
    Rule("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    Rule("sendgrid_key", re.compile(r"\bSG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\b")),
    Rule("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    Rule("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    Rule("telegram_bot_token", re.compile(r"\b[0-9]{8,12}:[A-Za-z0-9_-]{35,}\b")),
    Rule("private_key_header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    Rule(
        "postgres_dsn_with_password",
        re.compile(r"\bpostgres(?:ql)?://[^:\s/@]+:[^@\s]+@[^/\s]+/[^\s]+"),
    ),
    Rule(
        "mongodb_dsn_with_password",
        re.compile(r"\bmongodb(?:\+srv)?://[^:\s/@]+:[^@\s]+@[^\s]+"),
    ),
    Rule("redis_dsn_with_password", re.compile(r"\bredis://[^:\s/@]*:[^@\s]+@[^\s]+")),
)


@dataclass(frozen=True)
class Finding:
    rule_name: str
    location: str
    line_number: int


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root to scan. Defaults to the CogniPrint repository root.",
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Also scan textual Git patches across all refs. This is slower but required before a public release.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()

    findings = list(scan_tracked_tree(root))
    if args.history:
        findings.extend(scan_history(root))

    findings = deduplicate(findings)
    if findings:
        print("Potential secrets found:")
        for finding in findings:
            print(f"- {finding.rule_name}: {finding.location}:{finding.line_number}")
        print("Move live values to managed secret storage and rotate exposed credentials before release.")
        return 1

    scope = "tracked files and Git history" if args.history else "tracked files"
    print(f"Secret scan passed: no high-risk patterns found in {scope}.")
    return 0


def scan_tracked_tree(root: Path) -> Iterator[Finding]:
    for rel_path in tracked_files(root):
        path = root / rel_path
        if should_skip(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        yield from scan_lines(text.splitlines(), rel_path)


def scan_history(root: Path) -> list[Finding]:
    command = [
        "git",
        "log",
        "--all",
        "--full-history",
        "-p",
        "--no-ext-diff",
        "--text",
        "--format=commit %H",
        "--",
        ".",
    ]
    process = subprocess.Popen(
        command,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.stdout is None:
        stderr = process.stderr.read() if process.stderr is not None else ""
        process.wait()
        detail = stderr.strip() or "stdout pipe was not created"
        raise RuntimeError(f"Git history scan failed: {detail}")

    findings = scan_history_stream(process.stdout)

    stderr = process.stderr.read() if process.stderr is not None else ""
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"Git history scan failed: {stderr.strip()}")
    return findings


def scan_history_stream(lines: Iterable[str]) -> list[Finding]:
    """Scan a git-log patch stream while attributing deleted files to their old path."""
    findings: list[Finding] = []
    commit = "unknown"
    old_path = "history"
    current_path = "history"
    line_number = 0

    for raw_line in lines:
        line_number += 1
        line = raw_line.rstrip("\n")
        if line.startswith("commit "):
            commit = line.removeprefix("commit ").strip()
            old_path = "history"
            current_path = "history"
        elif line.startswith("--- a/"):
            old_path = line.removeprefix("--- a/").strip()
        elif line == "--- /dev/null":
            old_path = "history"
        elif line.startswith("+++ b/"):
            current_path = line.removeprefix("+++ b/").strip()
        elif line == "+++ /dev/null":
            current_path = old_path

        location = f"history:{commit[:12]}:{current_path}"
        findings.extend(scan_lines((line,), location, start_line=line_number))

    return findings


def scan_lines(
    lines: Iterable[str],
    location: str,
    *,
    start_line: int = 1,
) -> Iterator[Finding]:
    for offset, line in enumerate(lines):
        line_number = start_line + offset
        lowered = line.casefold()
        if any(marker in lowered for marker in ALLOW_MARKERS):
            continue
        for rule in RULES:
            if rule.pattern.search(line):
                yield Finding(rule.name, location, line_number)


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def should_skip(path: Path) -> bool:
    if path.suffix.casefold() in SKIP_SUFFIXES:
        return True
    try:
        sample = path.read_bytes()[:2048]
    except OSError:
        return True
    return b"\0" in sample


def deduplicate(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(set(findings), key=lambda item: (item.location, item.line_number, item.rule_name))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"Secret scan failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
