#!/usr/bin/env python3
"""Build a deterministic Research Lock Hash for a frozen CogniPrint experiment.

The lock binds exact file bytes and an optional repository commit into one
canonical SHA-256. It is an integrity binding, not a digital signature and not
proof that the locked scientific choices are correct.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "cogniprint-research-lock-001"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def resolve_relative_file(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"unsafe research-lock path: {relative}")
    target = root / rel
    if target.is_symlink():
        raise ValueError(f"symlink is not allowed in research lock: {relative}")
    resolved_root = root.resolve()
    resolved_target = target.resolve(strict=True)
    try:
        resolved_target.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"research-lock path escapes root: {relative}") from exc
    if not resolved_target.is_file():
        raise ValueError(f"research-lock entry is not a regular file: {relative}")
    return resolved_target


def build_lock(root: Path, includes: list[str], *, commit: str | None = None) -> dict[str, Any]:
    if not includes:
        raise ValueError("at least one --include file is required")
    normalized = [Path(item).as_posix() for item in includes]
    if len(normalized) != len(set(normalized)):
        raise ValueError("duplicate research-lock paths are not allowed")

    entries = []
    for relative in sorted(normalized):
        target = resolve_relative_file(root, relative)
        entries.append({"path": relative, "sha256": sha256_file(target)})

    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "repository_commit": commit,
        "entries": entries,
    }
    lock_hash = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return {
        **payload,
        "research_lock_sha256": lock_hash,
        "signature_status": "UNSIGNED",
        "meaning": "Integrity binding over exact locked files; not a digital signature or scientific-validity certificate.",
    }


def verify_lock(root: Path, lock: dict[str, Any]) -> dict[str, Any]:
    if lock.get("schema") != SCHEMA:
        return {"ok": False, "reason": "unsupported schema"}
    if lock.get("signature_status") != "UNSIGNED":
        return {"ok": False, "reason": "unsupported signature status"}
    entries = lock.get("entries")
    if not isinstance(entries, list) or not entries:
        return {"ok": False, "reason": "missing entries"}

    includes: list[str] = []
    expected_hashes: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            return {"ok": False, "reason": "invalid entry"}
        path = entry.get("path")
        digest = entry.get("sha256")
        if not isinstance(path, str) or not isinstance(digest, str):
            return {"ok": False, "reason": "invalid entry fields"}
        if path in expected_hashes:
            return {"ok": False, "reason": "duplicate path"}
        includes.append(path)
        expected_hashes[path] = digest

    try:
        rebuilt = build_lock(root, includes, commit=lock.get("repository_commit"))
    except (OSError, ValueError) as exc:
        return {"ok": False, "reason": str(exc)}

    for entry in rebuilt["entries"]:
        if expected_hashes.get(entry["path"]) != entry["sha256"]:
            return {"ok": False, "reason": f"file hash mismatch: {entry['path']}"}

    if rebuilt["research_lock_sha256"] != lock.get("research_lock_sha256"):
        return {"ok": False, "reason": "research lock hash mismatch"}
    return {"ok": True, "research_lock_sha256": rebuilt["research_lock_sha256"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build")
    build.add_argument("--root", type=Path, default=Path("."))
    build.add_argument("--include", action="append", required=True)
    build.add_argument("--commit")
    build.add_argument("--output", required=True, type=Path)

    verify = sub.add_parser("verify")
    verify.add_argument("--root", type=Path, default=Path("."))
    verify.add_argument("--lock", required=True, type=Path)

    args = parser.parse_args()
    if args.command == "build":
        lock = build_lock(args.root, args.include, commit=args.commit)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(args.output), "research_lock_sha256": lock["research_lock_sha256"]}, indent=2))
        return 0

    lock = json.loads(args.lock.read_text(encoding="utf-8"))
    result = verify_lock(args.root, lock)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
