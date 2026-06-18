#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from synthesize_decision import parse_votes, resolve_decision


def fallback_message(decision: str, counts: Counter[str]) -> str:
    if decision == "increment":
        return "Decision resolved: increment. Proceed only with a provenance-clean benchmark increment."
    if decision == "memo":
        return "Decision resolved: memo. Prepare a manuscript-facing interpretation memo without a new benchmark wave."
    if decision == "pending":
        return "Decision pending. No reviewer votes recorded yet; keep wording unchanged and wait for reviewer input before choosing wave-005."
    total = sum(counts.values())
    return (
        "Decision ambiguous. Keep inferential wording unchanged, avoid a large automatic benchmark wave, "
        f"and use a narrower follow-up pass or clarifying review question before choosing wave-005. Total votes: {total}."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve fallback behavior for ambiguous decision-gate outcomes.")
    parser.add_argument("--input", type=Path, required=True, help="Text file containing vote-bearing reviewer responses.")
    args = parser.parse_args(argv)

    text = args.input.read_text(encoding="utf-8") if args.input.exists() else ""
    counts = parse_votes(text)
    decision = resolve_decision(counts)
    print(fallback_message(decision, counts))
    return 2 if decision == "ambiguous" else 0


if __name__ == "__main__":
    raise SystemExit(main())
