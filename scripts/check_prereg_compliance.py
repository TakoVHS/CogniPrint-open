#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def summarize_results(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    summary: dict[str, object] = {}
    for key in ("hedges_g", "cliffs_delta", "permutation_p_value", "decision"):
        if key in payload:
            summary[key] = payload[key]
    if "mean_difference" in payload and isinstance(payload["mean_difference"], dict):
        summary["mean_difference"] = payload["mean_difference"]
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check that a locked wave-005 pre-registration still matches the current file.")
    parser.add_argument("--prereg-file", type=Path, default=Path("docs/pre-registration-wave005.md"))
    parser.add_argument("--hash-file", type=Path, default=Path("validation/wave005_prereg_hash.txt"))
    parser.add_argument("--results-file", type=Path, default=Path("validation/wave005_results.json"))
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    prereg_path = root / args.prereg_file
    hash_path = root / args.hash_file
    if not prereg_path.exists():
        raise SystemExit(f"Missing pre-registration file: {prereg_path}")
    if not hash_path.exists():
        raise SystemExit(f"Missing pre-registration hash file: {hash_path}")

    current_hash = digest_text(prereg_path.read_text(encoding="utf-8"))
    locked_hash = hash_path.read_text(encoding="utf-8").strip()
    if current_hash != locked_hash:
        raise SystemExit("Pre-registration hash mismatch. The wave-005 pre-registration changed after lock.")

    print("Pre-registration hash matches.")
    results_path = root / args.results_file
    if results_path.exists():
        print(json.dumps(summarize_results(results_path), ensure_ascii=False, indent=2))
    else:
        print(f"Results file not found: {results_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
