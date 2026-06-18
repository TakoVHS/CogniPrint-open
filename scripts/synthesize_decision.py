#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

VOTE_PATTERNS = {
    "increment": re.compile(r"^\s*decision:\s*increment\b", re.IGNORECASE),
    "memo": re.compile(r"^\s*decision:\s*memo\b", re.IGNORECASE),
    "abstain": re.compile(r"^\s*decision:\s*abstain\b", re.IGNORECASE),
}


def parse_votes(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for line in text.splitlines():
        normalized = line.strip()
        if not normalized or normalized.startswith("#"):
            continue
        for vote, pattern in VOTE_PATTERNS.items():
            if pattern.search(normalized):
                counts[vote] += 1
                break
    return counts


def resolve_decision(counts: Counter[str]) -> str:
    total = sum(counts.values())
    if total == 0:
        return "pending"
    threshold = (2 * total + 2) // 3
    if counts["increment"] >= threshold:
        return "increment"
    if counts["memo"] >= threshold:
        return "memo"
    return "ambiguous"


def render_summary(counts: Counter[str], decision: str) -> str:
    total = sum(counts.values())
    payload = {
        "total_votes": total,
        "increment": counts["increment"],
        "memo": counts["memo"],
        "abstain": counts["abstain"],
        "decision": decision,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize decision-gate votes for the current benchmark review pass.")
    parser.add_argument("--input", type=Path, required=True, help="Text file containing one vote-bearing line per reviewer response.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    args = parser.parse_args(argv)

    text = args.input.read_text(encoding="utf-8") if args.input.exists() else ""
    counts = parse_votes(text)
    decision = resolve_decision(counts)
    rendered = render_summary(counts, decision)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
