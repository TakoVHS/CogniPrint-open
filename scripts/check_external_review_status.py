#!/usr/bin/env python3
"""Materialize and check the external-review readiness gate."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESPONSES_DIR = ROOT / "docs" / "external-review" / "responses"
DEFAULT_OUTPUT = ROOT / "docs" / "external-review" / "status.json"
MINIMUM_VALID_REVIEWS = 1
MIN_REVIEW_BODY_CHARS = 600


REQUIRED_FIELDS = [
    "Reviewer",
    "Affiliation or role",
    "Review date",
    "Version reviewed",
    "Reviewer independence",
    "External review status",
]


def parse_field(text: str, field: str) -> str:
    pattern = re.compile(rf"^\s*[-*]?\s*{re.escape(field)}\s*:\s*(.+?)\s*$", re.I | re.M)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def validate_response(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    fields = {field: parse_field(text, field) for field in REQUIRED_FIELDS}
    missing = [field for field, value in fields.items() if not value or value.lower() in {"tbd", "todo", "<required>"}]
    review_body = re.sub(r"^\s*[-*]?\s*[^:\n]{1,80}\s*:\s*.+$", "", text, flags=re.M).strip()
    errors: list[str] = []
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if "external" not in fields.get("Reviewer independence", "").casefold():
        errors.append("Reviewer independence must state external independence")
    if fields.get("External review status", "").casefold() != "complete":
        errors.append("External review status must be complete")
    if len(review_body) < MIN_REVIEW_BODY_CHARS:
        errors.append(f"review body length {len(review_body)} < {MIN_REVIEW_BODY_CHARS}")
    return {
        "path": display_path(path),
        "reviewer": fields.get("Reviewer", ""),
        "affiliation_or_role": fields.get("Affiliation or role", ""),
        "review_date": fields.get("Review date", ""),
        "version_reviewed": fields.get("Version reviewed", ""),
        "valid": not errors,
        "errors": errors,
    }


def display_path(path: Path) -> str:
    resolved = path.resolve()
    return str(resolved.relative_to(ROOT)) if resolved.is_relative_to(ROOT) else str(resolved)


def build_status(responses_dir: Path) -> dict[str, Any]:
    response_files = sorted(
        path for path in responses_dir.glob("*.md")
        if path.is_file() and "template" not in path.name.casefold()
    )
    reviews = [validate_response(path) for path in response_files]
    valid_reviews = [review for review in reviews if review["valid"]]
    return {
        "snapshot_id": "external-review-gate-v1",
        "responses_dir": str(responses_dir.relative_to(ROOT)) if responses_dir.is_relative_to(ROOT) else str(responses_dir),
        "minimum_required_valid_reviews": MINIMUM_VALID_REVIEWS,
        "response_file_count": len(response_files),
        "valid_review_count": len(valid_reviews),
        "independent_external_review_present": len(valid_reviews) >= MINIMUM_VALID_REVIEWS,
        "valid_reviews": valid_reviews,
        "invalid_reviews": [review for review in reviews if not review["valid"]],
        "guardrail": "Do not mark this gate true without a real external reviewer response file.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--responses-dir", type=Path, default=RESPONSES_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Fail if the output status is stale.")
    parser.add_argument("--require-present", action="store_true", help="Fail unless at least one valid external review is present.")
    args = parser.parse_args(argv)

    responses_dir = args.responses_dir.resolve()
    responses_dir.mkdir(parents=True, exist_ok=True)
    status = build_status(responses_dir)
    output_path = args.output.resolve()
    rendered = json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    if args.check:
        if not output_path.exists():
            print(f"Missing external review status file: {output_path}")
            return 1
        if output_path.read_text(encoding="utf-8") != rendered:
            print(f"Stale external review status file: {output_path}")
            print("Run: python scripts/check_external_review_status.py --output docs/external-review/status.json")
            return 1
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"External review status written: {output_path}")

    print(
        "External review gate: "
        f"{status['valid_review_count']}/{status['minimum_required_valid_reviews']} valid reviews."
    )
    if args.require_present and not status["independent_external_review_present"]:
        print("External review gate is not satisfied.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
