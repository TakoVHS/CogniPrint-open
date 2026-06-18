#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def load_decision(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return str(payload.get("decision", "pending")).strip().lower()


def run(root: Path, *args: str) -> int:
    return subprocess.call(list(args), cwd=root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dispatch the next safe step after reviewer decision synthesis.")
    parser.add_argument("--decision-file", type=Path, default=Path("docs/decisions/final-decision.json"))
    parser.add_argument("--execute", action="store_true", help="Execute the memo-generation path when decision = memo.")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    decision_file = root / args.decision_file
    if not decision_file.exists():
        raise SystemExit(f"Missing decision file: {decision_file}")
    decision = load_decision(decision_file)

    if decision == "increment":
        print("Decision = increment.")
        print("Next safe step: complete docs/pre-registration-wave005.md, then run scripts/preregister_wave005.py before any data loading.")
        return 0
    if decision == "memo":
        print("Decision = memo.")
        if args.execute:
            return run(root, str(root / ".venv/bin/python"), "scripts/generate_interpretation_memo.py")
        print("Run `python scripts/generate_interpretation_memo.py` to materialize the manuscript-facing memo.")
        return 0
    if decision == "ambiguous":
        print("Decision = ambiguous.")
        return run(root, str(root / ".venv/bin/python"), "scripts/decision_gate_fallback.py", "--input", "docs/decisions/votes-raw.txt")

    print("Decision = pending. Wait for reviewer input before selecting wave-005 or the interpretation memo path.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
