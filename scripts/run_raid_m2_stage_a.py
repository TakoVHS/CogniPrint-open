#!/usr/bin/env python3
"""Execute the exact pinned RAID M2 Stage A development evidence run.

This wrapper is intentionally strict. It accepts only the historical M1 RAID
source/features/selection pins, requires a clean repository worktree, executes
the M2 and n-gram contract tests, runs the privacy-preserving M2 CLI, audits the
outputs, writes hashes, and packages a raw-text-free evidence archive.

It does not authorize Challenge 001 Stage B.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_SOURCE_SHA256 = "c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4"
EXPECTED_SOURCE_SIZE = 801_662_741
EXPECTED_FEATURES_SHA256 = "13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca"
EXPECTED_SELECTION_MANIFEST_SHA256 = "30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb"
EXPECTED_SOURCE_CONTRACT_SHA256 = "e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948"
EXPECTED_SELECTED_RECORDS = 500
SEED = 20261124
CONFORMAL_ALPHA = 0.05
MINIMUM_KNOWN_COVERAGE = 0.60
CHAR_DIMENSIONS = 262_144
WORD_DIMENSIONS = 131_072
BOOTSTRAP_RESAMPLES = 10_000

FORBIDDEN_KEYS = {
    "generation",
    "prompt",
    "raw_text",
    "raw_prompt",
    "_text",
    "tokens",
    "vocabulary",
    "ngrams",
}
FORBIDDEN_NAMES = {"train_none.csv", ".env", ".venv", "venv"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def git_output(repo_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=repo_root,
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def run_logged(command: list[str], *, cwd: Path, env: dict[str, str], log_path: Path) -> None:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    log_path.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed with exit code {completed.returncode}: "
            f"{' '.join(command)}; see {log_path}"
        )


def assert_no_forbidden_keys(payload: Any, path: str = "root") -> None:
    if isinstance(payload, dict):
        forbidden = FORBIDDEN_KEYS & payload.keys()
        if forbidden:
            raise AssertionError(
                f"forbidden persisted keys at {path}: {sorted(forbidden)}"
            )
        for key, value in payload.items():
            assert_no_forbidden_keys(value, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            assert_no_forbidden_keys(value, f"{path}[{index}]")


def validate_inputs(source: Path, features: Path, contract: Path) -> dict[str, str | int]:
    source_sha = sha256_file(source)
    features_sha = sha256_file(features)
    contract_sha = sha256_file(contract)
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise ValueError("authoritative RAID source SHA-256 mismatch")
    if source.stat().st_size != EXPECTED_SOURCE_SIZE:
        raise ValueError("authoritative RAID source byte-size mismatch")
    if features_sha != EXPECTED_FEATURES_SHA256:
        raise ValueError("historical M1 features SHA-256 mismatch")
    if contract_sha != EXPECTED_SOURCE_CONTRACT_SHA256:
        raise ValueError("historical RAID source-contract SHA-256 mismatch")
    return {
        "source_sha256": source_sha,
        "source_byte_size": source.stat().st_size,
        "features_sha256": features_sha,
        "source_contract_sha256": contract_sha,
    }


def validate_outputs(output_dir: Path) -> dict[str, Any]:
    required = [
        output_dir / "m2-results.json",
        output_dir / "m2-role-manifest.json",
        output_dir / "m2-reproducibility.json",
        output_dir / "m2-report.md",
    ]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    result = json.loads(required[0].read_text(encoding="utf-8"))
    roles = json.loads(required[1].read_text(encoding="utf-8"))
    reproducibility = json.loads(required[2].read_text(encoding="utf-8"))

    for payload in (result, roles, reproducibility):
        assert_no_forbidden_keys(payload)

    if result.get("status") != "DEVELOPMENT_ONLY":
        raise AssertionError("M2 result status is not DEVELOPMENT_ONLY")
    if result.get("stage_b_status") != "NOT_AUTHORISED_TO_START":
        raise AssertionError("M2 result unexpectedly changes Stage B status")
    if result.get("scientific_claim_evidence") is not False:
        raise AssertionError("M2 result unexpectedly claims scientific evidence")
    if result.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        raise AssertionError("M2 output source SHA-256 mismatch")
    if result.get("selected_features_sha256") != EXPECTED_FEATURES_SHA256:
        raise AssertionError("M2 output features SHA-256 mismatch")
    if result.get("selection_manifest_sha256") != EXPECTED_SELECTION_MANIFEST_SHA256:
        raise AssertionError("M2 output selection-manifest SHA-256 mismatch")
    if reproducibility.get("status") != "PASS" or reproducibility.get("match") is not True:
        raise AssertionError("M2 deterministic rerun did not pass")
    if len(result.get("folds") or []) != 4:
        raise AssertionError("M2 did not report exactly four unknown-family folds")
    if len(roles.get("folds") or []) != 4:
        raise AssertionError("M2 role manifest did not report exactly four folds")

    return {
        "result": result,
        "roles": roles,
        "reproducibility": reproducibility,
    }


def privacy_audit(run_dir: Path) -> dict[str, Any]:
    scanned = 0
    json_files = 0
    for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
        scanned += 1
        if any(part in FORBIDDEN_NAMES for part in path.parts):
            raise AssertionError(f"forbidden path persisted in evidence bundle: {path}")
        if path.suffix in {".json", ".jsonl"}:
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert_no_forbidden_keys(payload)
            json_files += 1
        elif path.suffix in {".md", ".txt", ".log"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in (
                '"generation"',
                '"prompt"',
                '"raw_text"',
                '"raw_prompt"',
                '"_text"',
            ):
                if token in text:
                    raise AssertionError(
                        f"forbidden raw-data marker {token} found in {path}"
                    )
    return {
        "schema": "cogniprint-raid-m2-privacy-audit-001",
        "status": "PASS",
        "files_scanned": scanned,
        "json_files_scanned": json_files,
        "raw_source_persisted": False,
        "raw_prompt_persisted": False,
        "raw_generation_persisted": False,
        "recoverable_vocabulary_persisted": False,
    }


def write_evidence_manifest(run_dir: Path) -> int:
    manifest = run_dir / "EVIDENCE_SHA256SUMS.txt"
    rows: list[str] = []
    for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
        if path == manifest:
            continue
        rows.append(f"{sha256_file(path)}  {path.relative_to(run_dir).as_posix()}")
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def build_archive(run_dir: Path, archive_path: Path) -> None:
    with tarfile.open(archive_path, "w:gz") as handle:
        handle.add(run_dir, arcname=run_dir.name)
    with tarfile.open(archive_path, "r:gz") as handle:
        for member in handle.getmembers():
            parts = set(Path(member.name).parts)
            if parts & FORBIDDEN_NAMES:
                raise AssertionError(
                    f"forbidden path found in M2 evidence archive: {member.name}"
                )
            if member.issym() or member.islnk():
                raise AssertionError(
                    f"links are forbidden in M2 evidence archive: {member.name}"
                )


def status_markdown(repository_commit: str) -> str:
    return "\n".join(
        [
            "# CogniPrint RAID M2 exact Stage A run",
            "",
            "Status: EXECUTED / DEVELOPMENT_ONLY / PRE-FREEZE",
            "",
            f"Repository commit: {repository_commit}",
            f"Source SHA-256: {EXPECTED_SOURCE_SHA256}",
            f"Features SHA-256: {EXPECTED_FEATURES_SHA256}",
            f"Selection manifest SHA-256: {EXPECTED_SELECTION_MANIFEST_SHA256}",
            f"Source contract SHA-256: {EXPECTED_SOURCE_CONTRACT_SHA256}",
            f"Seed: {SEED}",
            f"Conformal alpha: {CONFORMAL_ALPHA}",
            f"Minimum known coverage: {MINIMUM_KNOWN_COVERAGE}",
            "",
            "Archive SHA-256 is deliberately stored outside this bundle in a "
            "sidecar file to avoid self-referential hashing.",
            "",
            "Boundary: Stage A development evidence only. This run does not "
            "authorize Stage B or establish exact model identity, AI origin, "
            "authorship, actor identity, commissioning, intent, legal or "
            "forensic provenance.",
            "",
        ]
    )

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path, required=True)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--source-contract", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    source = args.input_file.resolve()
    features = args.features.resolve()
    contract = args.source_contract.resolve()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    if git_output(repo_root, "status", "--short"):
        raise RuntimeError("repository worktree must be clean before exact M2 evidence execution")

    repository_commit = git_output(repo_root, "rev-parse", "HEAD")
    repository_tree = git_output(repo_root, "rev-parse", "HEAD^{tree}")
    branch = git_output(repo_root, "branch", "--show-current")
    remote = git_output(repo_root, "remote", "get-url", "origin")
    input_audit = validate_inputs(source, features, contract)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"raid-m2-{timestamp}"
    analysis_dir = run_dir / "analysis"
    logs_dir = run_dir / "logs"
    analysis_dir.mkdir(parents=True)
    logs_dir.mkdir(parents=True)

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    source_root = str(repo_root / "src")
    env["PYTHONPATH"] = (
        f"{source_root}{os.pathsep}{env.get('PYTHONPATH', '')}"
    ).rstrip(os.pathsep)

    run_logged(
        [
            args.python,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_raid_calibration_m2.py",
            "-v",
        ],
        cwd=repo_root,
        env=env,
        log_path=logs_dir / "test-raid-calibration-m2.log",
    )
    run_logged(
        [
            args.python,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_raid_ngram_baselines.py",
            "-v",
        ],
        cwd=repo_root,
        env=env,
        log_path=logs_dir / "test-raid-ngram-regression.log",
    )

    run_logged(
        [
            args.python,
            str(repo_root / "scripts" / "analyze_raid_calibration_m2.py"),
            "--features",
            str(features),
            "--input-file",
            str(source),
            "--expected-source-sha256",
            EXPECTED_SOURCE_SHA256,
            "--expected-features-sha256",
            EXPECTED_FEATURES_SHA256,
            "--expected-selection-manifest-sha256",
            EXPECTED_SELECTION_MANIFEST_SHA256,
            "--source-contract",
            str(contract),
            "--output-dir",
            str(analysis_dir),
            "--seed",
            str(SEED),
            "--conformal-alpha",
            str(CONFORMAL_ALPHA),
            "--minimum-known-coverage",
            str(MINIMUM_KNOWN_COVERAGE),
            "--char-dimensions",
            str(CHAR_DIMENSIONS),
            "--word-dimensions",
            str(WORD_DIMENSIONS),
            "--bootstrap-resamples",
            str(BOOTSTRAP_RESAMPLES),
        ],
        cwd=repo_root,
        env=env,
        log_path=logs_dir / "m2-analysis.log",
    )

    validated = validate_outputs(analysis_dir)
    repository_state = {
        "schema": "cogniprint-raid-m2-repository-state-001",
        "repository_commit": repository_commit,
        "repository_tree": repository_tree,
        "branch": branch,
        "remote": remote,
        "worktree_clean": True,
        "execution_channel": "LOCAL_PINNED_SOURCE",
        **input_audit,
    }
    write_json(run_dir / "repository-state.json", repository_state)

    protocol_source = repo_root / "docs" / "raid-calibration-m2-development.md"
    shutil.copy2(protocol_source, run_dir / "raid-calibration-m2-development.md")

    audit = privacy_audit(run_dir)
    write_json(run_dir / "privacy-audit.json", audit)

    (run_dir / "FINAL_STATUS.md").write_text(
        status_markdown(repository_commit),
        encoding="utf-8",
    )
    internal_summary = {
        "schema": "cogniprint-raid-m2-exact-run-internal-001",
        "status": "PASS",
        "repository_commit": repository_commit,
        "m2_result_sha256": sha256_file(analysis_dir / "m2-results.json"),
        "m2_role_manifest_sha256": sha256_file(
            analysis_dir / "m2-role-manifest.json"
        ),
        "m2_reproducibility_sha256": sha256_file(
            analysis_dir / "m2-reproducibility.json"
        ),
        "privacy_audit_status": audit["status"],
        "stage_b_status": validated["result"]["stage_b_status"],
    }
    write_json(run_dir / "RUN_SUMMARY.json", internal_summary)
    manifest_entries = write_evidence_manifest(run_dir)

    archive_path = output_root / f"{run_dir.name}.tar.gz"
    build_archive(run_dir, archive_path)
    archive_sha = sha256_file(archive_path)

    external_summary = {
        "schema": "cogniprint-raid-m2-exact-run-archive-001",
        "status": "PASS",
        "repository_commit": repository_commit,
        "evidence_manifest_entries": manifest_entries,
        "archive": archive_path.name,
        "archive_sha256": archive_sha,
        "run_directory": run_dir.name,
    }
    summary_path = output_root / f"{run_dir.name}.summary.json"
    write_json(summary_path, external_summary)
    sha_path = output_root / f"{run_dir.name}.sha256"
    sha_path.write_text(
        f"{archive_sha}  {archive_path.name}\n",
        encoding="utf-8",
    )

    print(run_dir)
    print(archive_path)
    print(summary_path)
    print(sha_path)
    print(archive_sha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
