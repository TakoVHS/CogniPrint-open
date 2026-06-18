#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path


def load_decision(path: Path) -> str:
    if not path.exists():
        return "pending"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return str(payload.get("decision", "pending")).strip().lower()


def is_placeholder(text: str) -> bool:
    lowered = text.casefold()
    return "placeholder only" in lowered or "must be completed before any future `wave-005`" in lowered


def current_git_commit(root: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def lock_payload(prereg_path: Path, root: Path) -> dict[str, str]:
    content = prereg_path.read_text(encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "date": str(date.today()),
        "git_commit": current_git_commit(root),
        "prereg_path": str(prereg_path.relative_to(root)),
        "sha256": digest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lock the current wave-005 pre-registration after an increment decision.")
    parser.add_argument("--decision-file", type=Path, default=Path("docs/decisions/final-decision.json"))
    parser.add_argument("--prereg-file", type=Path, default=Path("docs/pre-registration-wave005.md"))
    parser.add_argument("--hash-file", type=Path, default=Path("validation/wave005_prereg_hash.txt"))
    parser.add_argument("--lock-file", type=Path, default=Path("validation/wave005_prereg_lock.json"))
    parser.add_argument("--skip-decision-check", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    prereg_path = (root / args.prereg_file).resolve()
    if not prereg_path.exists():
        raise SystemExit(f"Missing pre-registration file: {prereg_path}")

    if not args.skip_decision_check:
        decision = load_decision(root / args.decision_file)
        if decision != "increment":
            raise SystemExit(f"Refusing to lock pre-registration before an increment decision. Current decision: {decision}")

    content = prereg_path.read_text(encoding="utf-8")
    if is_placeholder(content):
        raise SystemExit("Pre-registration file still contains placeholder text. Complete it before locking wave-005.")

    payload = lock_payload(prereg_path, root)
    hash_path = (root / args.hash_file).resolve()
    lock_path = (root / args.lock_file).resolve()
    hash_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    if not args.force and hash_path.exists():
        existing = hash_path.read_text(encoding="utf-8").strip()
        if existing and existing != payload["sha256"]:
            raise SystemExit("Existing pre-registration hash differs from the current document. Review changes before relocking.")

    hash_path.write_text(payload["sha256"] + "\n", encoding="utf-8")
    lock_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
