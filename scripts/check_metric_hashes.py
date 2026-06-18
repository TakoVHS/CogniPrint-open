#!/usr/bin/env python3
"""Check stable hashes for key public evidence metric artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_HASHES = {
    "evidence/empirical-v1/counts.json": "1aa2dfbd443e3c599fcb3502ede4c2092e3ba87cbb9eb75b133cba8a80e5330c",
    "evidence/public-benchmark-v1/counts.json": "d7c6358807eb0b553ec72137188adf966b33d9b4bc4f63bdcc835c4ce081384f",
    "evidence/public-benchmark-v1.1/counts.json": "3770429b49a3e1880e12e0a66a4f5321f65ea7114e4499a5a98833ed2c37059b",
    "evidence/statistical-validation-v1/counts.json": "01675eb3ef13aebc5c1cd4c33d6ef94515fae42d1fad384160c3c168a4d1d2f7",
    "evidence/statistical-validation-v1/overall-metrics.json": "302e974bc9be9df81c0a007ed20ffa904803f4278520da49ba17dc781adaaa89",
    "evidence/statistical-validation-v1/random-baseline-summary.json": "75053ab9901bf48b301ff23b079181b60731c1be3cd61cd5dd12f23e38a4ae3c",
    "evidence/statistical-validation-v1/benchmark-campaign-bridge.json": "0b57fa5a748175c2538ffd6c693646515f1b6e8f711adcfc846effa7f6b39f65",
    "evidence/statistical-validation-v1/threshold-sensitivity.json": "9a4323644ec5a8eae354ddd1daa91929fb3dbcf373e72b80a3e574b0bb7b6b95",
}


def canonical_json_hash(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)

    root = args.root.resolve()
    errors: list[str] = []
    for rel_path, expected_hash in EXPECTED_HASHES.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing metric artifact: {rel_path}")
            continue
        actual_hash = canonical_json_hash(path)
        if actual_hash != expected_hash:
            errors.append(f"{rel_path}: {actual_hash} != {expected_hash}")

    if errors:
        print("Metric hash check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Metric hash check passed for {len(EXPECTED_HASHES)} artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
