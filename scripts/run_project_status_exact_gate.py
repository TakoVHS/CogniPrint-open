#!/usr/bin/env python3
"""Run the exact-head CogniPrint project-status gate on a clean checkout.

The runner is intentionally fail-closed. It validates the current repository head,
runs the status/release/security checks, derives statistical readiness twice in
separate temporary locations, and accepts only byte-identical
``descriptive_only`` reports. It does not modify the checkout or authorize a
scientific-status change.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path


class GateError(RuntimeError):
    pass


def run(root: Path, *command: str, capture: bool = False) -> str:
    print("+", " ".join(command), flush=True)
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.STDOUT if capture else None,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except OSError as exc:
        raise GateError(f"cannot execute {' '.join(command)}: {exc}") from exc
    if completed.returncode != 0:
        output = completed.stdout or ""
        if output:
            print(output, end="" if output.endswith("\n") else "\n")
        raise GateError(f"command failed ({completed.returncode}): {' '.join(command)}")
    return completed.stdout or ""


def git(root: Path, *args: str) -> str:
    return run(root, "git", *args, capture=True).strip()


def require_clean(root: Path) -> None:
    status = git(root, "status", "--short")
    if status:
        raise GateError(f"worktree is not clean:\n{status}")


def require_identity(root: Path, expected_head: str, expected_tree: str | None) -> tuple[str, str]:
    actual_head = git(root, "rev-parse", "HEAD")
    actual_tree = git(root, "rev-parse", "HEAD^{tree}")
    if actual_head != expected_head:
        raise GateError(f"head mismatch: expected {expected_head}, got {actual_head}")
    if expected_tree and actual_tree != expected_tree:
        raise GateError(f"tree mismatch: expected {expected_tree}, got {actual_tree}")
    return actual_head, actual_tree


def compile_python(root: Path, destination: Path) -> None:
    files = sorted(
        path
        for directory in ("src", "scripts", "tests")
        for path in (root / directory).rglob("*.py")
    )
    if not files:
        raise GateError("no Python files found for compilation")
    destination.mkdir(parents=True, exist_ok=True)
    for index, path in enumerate(files):
        try:
            py_compile.compile(
                str(path),
                cfile=str(destination / f"{index:05d}.pyc"),
                doraise=True,
            )
        except py_compile.PyCompileError as exc:
            raise GateError(f"Python compilation failed for {path.relative_to(root)}: {exc.msg}") from exc
    print(f"PY_COMPILE=PASS files={len(files)}")


def strict_json(path: Path) -> dict[str, object]:
    def reject_constant(token: str) -> None:
        raise GateError(f"non-finite number in {path}: {token}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GateError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise GateError(f"JSON root must be an object: {path}")
    return payload


def derive_readiness(root: Path, destination: Path) -> dict[str, object]:
    run(
        root,
        sys.executable,
        "scripts/check_statistical_readiness.py",
        "--output",
        str(destination),
    )
    payload = strict_json(destination)
    if payload.get("decision") != "descriptive_only":
        raise GateError(
            "unexpected readiness decision; independent methodological review is required before integration: "
            f"{payload.get('decision')!r}"
        )
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--expected-head", default=os.environ.get("EXPECTED_HEAD"))
    parser.add_argument("--expected-tree", default=os.environ.get("EXPECTED_TREE"))
    parser.add_argument("--ruff", default=os.environ.get("RUFF", "ruff"))
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not args.expected_head:
        print("PROJECT_STATUS_GATE=BLOCKED")
        print("BLOCKER=EXPECTED_HEAD is required")
        return 2

    try:
        require_clean(root)
        head, tree = require_identity(root, args.expected_head, args.expected_tree)

        run(root, args.ruff, "check", "src", "scripts", "tests", "--select", "E4,E7,E9,F")

        with tempfile.TemporaryDirectory(prefix="cogniprint-status-gate-") as temporary:
            temp = Path(temporary)
            compile_python(root, temp / "pyc")

            run(root, sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_project_status.py", "-v")
            run(root, sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_public_release_export.py", "-v")
            run(root, sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_secret_scan.py", "-v")
            run(root, sys.executable, "scripts/check_project_status.py")
            run(root, sys.executable, "scripts/secret_scan.py")
            run(root, sys.executable, "scripts/export_public_release.py", "--check-only")

            first = temp / "readiness-1.json"
            second = temp / "readiness-2.json"
            payload_first = derive_readiness(root, first)
            payload_second = derive_readiness(root, second)
            bytes_first = first.read_bytes()
            bytes_second = second.read_bytes()
            if bytes_first != bytes_second or payload_first != payload_second:
                raise GateError("statistical readiness derivation is not deterministic")

            candidate = temp / "public-release"
            run(
                root,
                sys.executable,
                "scripts/export_public_release.py",
                "--destination",
                str(candidate),
                "--clean",
            )
            run(
                root,
                sys.executable,
                str(candidate / "scripts/check_project_status.py"),
                "--root",
                str(candidate),
            )
            run(
                root,
                sys.executable,
                str(candidate / "scripts/secret_scan.py"),
                "--root",
                str(candidate),
            )

            readiness_sha256 = hashlib.sha256(bytes_first).hexdigest()

        require_clean(root)
        final_head, final_tree = require_identity(root, head, tree)
    except GateError as exc:
        print("PROJECT_STATUS_GATE=BLOCKED")
        print(f"BLOCKER={exc}")
        return 1

    print("PROJECT_STATUS_GATE=PASS")
    print("STATISTICAL_READINESS_MATERIALIZATION_CANDIDATE=PASS")
    print("SCIENTIFIC_READINESS=descriptive_only")
    print(f"EXACT_HEAD={final_head}")
    print(f"EXACT_TREE={final_tree}")
    print(f"READINESS_SHA256={readiness_sha256}")
    print("GITHUB_ACTIONS_STATUS=NOT_INFERRED_BY_THIS_RUNNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
