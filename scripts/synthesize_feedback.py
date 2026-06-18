#!/usr/bin/env python3
"""Summarize GitHub reviewer feedback issues into a compact markdown digest."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT = Path("docs/feedback-synthesis-latest.md")
DEFAULT_TEMPLATE = Path("docs/feedback-synthesis-template.md")
KNOWN_CATEGORIES = (
    "framing / claims",
    "methods (statistics, metrics)",
    "results / evidence interpretation",
    "limitations",
    "benchmark / validation layer",
    "reproducibility / code",
    "documentation",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="TakoVHS/CogniPrint", help="GitHub repository in owner/name form.")
    parser.add_argument("--label", default="feedback", help="Issue label used for reviewer feedback.")
    parser.add_argument("--state", default="all", choices=("open", "closed", "all"), help="Issue state filter.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Markdown synthesis output.")
    parser.add_argument("--template-output", type=Path, default=DEFAULT_TEMPLATE, help="Fallback template output.")
    args = parser.parse_args()

    issues = _fetch_feedback_issues(repo=args.repo, label=args.label, state=args.state)
    if issues is None:
        args.template_output.parent.mkdir(parents=True, exist_ok=True)
        args.template_output.write_text(_fallback_template(), encoding="utf-8")
        print(f"No feedback issues available. Wrote template: {args.template_output}")
        return 0

    markdown = synthesize_feedback(issues)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"Feedback synthesis written: {args.output}")
    return 0


def _fetch_feedback_issues(*, repo: str, label: str, state: str) -> list[dict[str, Any]] | None:
    gh_path = _find_gh()
    if gh_path is None:
        return None

    env = os.environ.copy()
    command = [
        gh_path,
        "issue",
        "list",
        "--repo",
        repo,
        "--label",
        label,
        "--state",
        state,
        "--limit",
        "200",
        "--json",
        "number,title,body,url,labels,state,author,createdAt,updatedAt",
    ]
    result = subprocess.run(command, text=True, capture_output=True, env=env)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def synthesize_feedback(issues: list[dict[str, Any]]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    severity_counts: dict[str, int] = defaultdict(int)
    for issue in issues:
        body = issue.get("body", "") or ""
        category = infer_category(body)
        severity = infer_severity(body)
        severity_counts[severity] += 1
        grouped[category].append(
            {
                "number": issue.get("number"),
                "title": issue.get("title", "Untitled"),
                "url": issue.get("url", ""),
                "state": issue.get("state", "unknown"),
                "severity": severity,
                "preview": preview_text(body),
            }
        )

    now = datetime.now(timezone.utc).date().isoformat()
    lines = [
        f"# Feedback Synthesis - {now}",
        "",
        f"- Source issues: `{len(issues)}`",
        f"- Critical: `{severity_counts.get('critical', 0)}`",
        f"- Major: `{severity_counts.get('major', 0)}`",
        f"- Minor: `{severity_counts.get('minor', 0)}`",
        "",
    ]
    if not issues:
        lines.extend(
            [
                "## Current intake status",
                "",
                "No external feedback issues have been collected yet through the GitHub reviewer feedback template.",
                "",
                "## Provisional next step",
                "",
                "Until real reviewer input arrives, the most defensible next technical priority is benchmark expansion first rather than stronger inferential wording.",
                "",
                "Reason:",
                "",
                "- the current descriptive validation layer is already implemented;",
                "- the current benchmark subset is still small;",
                "- stronger inferential work without broader benchmark coverage would outrun the current evidence base.",
                "",
            ]
        )
    for category in sorted(grouped):
        lines.append(f"## {category} ({len(grouped[category])})")
        lines.append("")
        for item in grouped[category]:
            lines.append(f"- [#{item['number']} {item['title']}]({item['url']})")
            lines.append(f"  - state: `{item['state']}`")
            lines.append(f"  - severity: `{item['severity']}`")
            lines.append(f"  - preview: {item['preview']}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def infer_category(body: str) -> str:
    lowered = body.lower()
    for category in KNOWN_CATEGORIES:
        if category.lower() in lowered:
            return category
    if "framing" in lowered or "claim" in lowered:
        return "framing / claims"
    if "method" in lowered or "stat" in lowered or "metric" in lowered:
        return "methods (statistics, metrics)"
    if "limit" in lowered:
        return "limitations"
    if "benchmark" in lowered or "validation" in lowered:
        return "benchmark / validation layer"
    if "reproduc" in lowered or "code" in lowered:
        return "reproducibility / code"
    if "doc" in lowered:
        return "documentation"
    return "uncategorized"


def infer_severity(body: str) -> str:
    lowered = body.lower()
    if "critical (blocks publication or validation)" in lowered or "severity\ncritical" in lowered:
        return "critical"
    if "major (should be fixed before the next release)" in lowered or "severity\nmajor" in lowered:
        return "major"
    if "minor (clarification, wording, typo)" in lowered or "severity\nminor" in lowered:
        return "minor"
    if "critical" in lowered:
        return "critical"
    if "major" in lowered:
        return "major"
    return "minor"


def preview_text(body: str, *, limit: int = 180) -> str:
    compact = " ".join(body.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _fallback_template() -> str:
    return "\n".join(
        [
            "# Feedback Intake Log",
            "",
            "No GitHub feedback issues were available from the current environment.",
            "",
            "Use the reviewer issue template to collect structured feedback, then rerun:",
            "",
            "```bash",
            "make sync-feedback",
            "```",
            "",
        ]
    )


def _find_gh() -> str | None:
    return os.environ.get("GH_PATH") or _which("gh")


def _which(name: str) -> str | None:
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / name
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
