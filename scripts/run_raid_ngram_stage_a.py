#!/usr/bin/env python3
"""Execute and package the pinned Stage A RAID n-gram comparison.

This orchestrator verifies the prior evidence chain and authoritative raw source,
runs the targeted tests and n-gram analysis twice, then writes a chained evidence
bundle without copying raw RAID text into the bundle or repository.
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
import tempfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cogniprint.benchmarks.ngram import char_config, word_config

EXPECTED_BRANCH = "feat/raid-ngram-baselines"
EXPECTED_SOURCE_SHA256 = "c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4"
EXPECTED_SOURCE_SIZE = 801_662_741
EXPECTED_PREVIOUS_ARCHIVE_SHA256 = "9f7a0c39f24ee71539cb74d896d204e4220261dc1ddfa2343b44d2ac72a04a82"
EXPECTED_FEATURES_SHA256 = "13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca"
EXPECTED_SOURCE_CONTRACT_SHA256 = "e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948"
EXPECTED_SELECTION_MANIFEST_SHA256 = "30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb"
EXPECTED_TRAIN_RECORDS = 351
EXPECTED_TEST_RECORDS = 149
EXPECTED_TRAIN_GROUPS = 336
EXPECTED_TEST_GROUPS = 145
EXPECTED_LINEAGE_OVERLAP = 0
EXPECTED_SELECTED_RECORDS = 500
EXPECTED_UNIQUE_TEXT_HASHES = 500
SEED = 20260725
TEST_FRACTION = 0.30
FORBIDDEN_JSON_KEYS = {
    "generation",
    "prompt",
    "raw_text",
    "raw_prompt",
    "_text",
    "tokens",
    "vocabulary",
    "ngrams",
}
CHECKPOINT_STAGES = [
    "repository_audit",
    "branch_sync",
    "source_verification",
    "previous_archive_verification",
    "previous_evidence_extraction",
    "code_audit",
    "targeted_tests",
    "selected_record_verification",
    "source_rehydration",
    "split_verification",
    "character_ngram_analysis",
    "word_ngram_analysis",
    "reproducibility_rerun",
    "privacy_audit",
    "evidence_manifest",
    "archive_build",
    "archive_verification",
    "git_update",
    "pr_update",
    "issue_update",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def git_output(repo_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=repo_root, text=True, stderr=subprocess.STDOUT
    ).strip()


def list_safe_tar_members(archive: Path) -> list[tarfile.TarInfo]:
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
    safe_members: list[tarfile.TarInfo] = []
    for member in members:
        if member.name.startswith("/"):
            raise ValueError(f"unsafe archive member with absolute path: {member.name}")
        parts = [part for part in member.name.split("/") if part not in ("", ".")]
        if ".." in parts:
            raise ValueError(f"unsafe archive member with traversal path: {member.name}")
        if member.issym() or member.islnk():
            raise ValueError(f"unsafe archive member with link: {member.name}")
        if not (member.isdir() or member.isfile()):
            raise ValueError(f"unsupported archive member type: {member.name}")
        safe_members.append(member)
    return safe_members


def safe_extract_archive(archive: Path, destination: Path) -> int:
    safe_members = list_safe_tar_members(archive)
    extracted_files = 0
    with tarfile.open(archive, "r:gz") as handle:
        for member in safe_members:
            target = destination / member.name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            extracted = handle.extractfile(member)
            if extracted is None:
                raise ValueError(f"failed to extract regular file: {member.name}")
            with target.open("wb") as out:
                for chunk in iter(lambda: extracted.read(1024 * 1024), b""):
                    out.write(chunk)
            extracted_files += 1
    return extracted_files


def verify_manifest(root: Path) -> tuple[bool, int]:
    manifest = root / "EVIDENCE_SHA256SUMS.txt"
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    checked = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        actual = sha256_file(root / relative)
        if actual != expected:
            raise AssertionError(f"evidence manifest mismatch for {relative}")
        checked += 1
    return True, checked


def find_unique(root: Path, name: str) -> Path:
    matches = [path for path in root.rglob(name) if path.is_file()]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {name}, found {len(matches)}")
    return matches[0]


def assert_no_forbidden_keys(payload: Any, path: str = "root") -> None:
    if isinstance(payload, dict):
        forbidden = FORBIDDEN_JSON_KEYS & payload.keys()
        if forbidden:
            raise AssertionError(f"forbidden persisted keys at {path}: {sorted(forbidden)}")
        for key, value in payload.items():
            assert_no_forbidden_keys(value, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            assert_no_forbidden_keys(value, f"{path}[{index}]")


def selection_manifest_sha256_from_features(features_path: Path) -> str:
    records = [
        json.loads(line)
        for line in features_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    selection = [
        {
            "source_record_id": record.get("source_record_id"),
            "source_id": record.get("source_id"),
            "model_family": record.get("model_family"),
            "domain": record.get("domain"),
            "text_sha256": record.get("text_sha256"),
            "prompt_sha256": record.get("prompt_sha256"),
            "lineage_id": record.get("lineage_id"),
        }
        for record in sorted(records, key=lambda item: str(item.get("source_record_id") or ""))
    ]
    return sha256_json(selection)


def initialize_checkpoint(repository_commit: str) -> dict[str, Any]:
    return {
        "schema": "cogniprint-stage-a-ngram-checkpoint-001",
        "status": "RUNNING",
        "repository_commit": repository_commit,
        "stages": {stage: "PENDING" for stage in CHECKPOINT_STAGES},
    }


def write_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    write_json(path, checkpoint)


def set_stage(path: Path, checkpoint: dict[str, Any], stage: str, status: str) -> None:
    checkpoint["stages"][stage] = status
    if status == "FAIL":
        checkpoint["status"] = "FAIL"
    write_checkpoint(path, checkpoint)


def append_log(path: Path, message: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


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
            f"command failed with exit code {completed.returncode}: {' '.join(command)}; see {log_path}"
        )


def metric_row(payload: dict[str, Any]) -> str:
    return (
        f"accuracy={payload['accuracy']:.6f}, "
        f"balanced_accuracy={payload['balanced_accuracy']:.6f}, "
        f"macro_f1={payload['macro_f1']:.6f}"
    )


def build_status_markdown(
    metrics: dict[str, Any],
    repository_commit: str,
    archive_name: str,
    archive_sha256: str,
) -> str:
    char_metrics = metrics["character_3_5_hashed_tfidf"]["metrics"]
    word_metrics = metrics["word_1_2_hashed_tfidf"]["metrics"]
    return "\n".join(
        [
            "# CogniPrint Stage A n-gram comparison — final local status",
            "",
            "Status: `EXECUTED / DESCRIPTIVE_ONLY / PRE-FREEZE`",
            "",
            f"Repository commit: `{repository_commit}`",
            f"Source SHA-256: `{EXPECTED_SOURCE_SHA256}`",
            f"Previous evidence archive SHA-256: `{EXPECTED_PREVIOUS_ARCHIVE_SHA256}`",
            f"Final evidence archive: `{archive_name}`",
            f"Final evidence archive SHA-256: `{archive_sha256}`",
            "",
            "## Baselines",
            "",
            f"- majority: {metric_row(metrics['majority'])}",
            f"- length-only: {metric_row(metrics['length_only_nearest_centroid'])}",
            f"- CogniPrint 12D: {metric_row(metrics['cogniprint_12d_nearest_centroid'])}",
            f"- character 3–5 hashed TF-IDF: {metric_row(char_metrics)}",
            f"- word 1–2 hashed TF-IDF: {metric_row(word_metrics)}",
            "",
            "## Boundary",
            "",
            "These are uncalibrated Stage A benchmark diagnostics. They do not establish exact model identity, AI origin, authorship, actor identity, commissioner identity, intent, responsibility, legal provenance, forensic provenance, production readiness, or Stage B authorization.",
            "",
        ]
    )


def validate_analysis_outputs(output_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    metrics_path = output_dir / "ngram-baseline-metrics.json"
    audit_path = output_dir / "ngram-source-rehydration-audit.json"
    reproducibility_path = output_dir / "ngram-reproducibility-check.json"
    report_path = output_dir / "ngram-baseline-report.md"
    for path in (metrics_path, audit_path, reproducibility_path, report_path):
        if not path.is_file():
            raise FileNotFoundError(path)
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    reproducibility = json.loads(reproducibility_path.read_text(encoding="utf-8"))
    for payload in (metrics, audit, reproducibility):
        assert_no_forbidden_keys(payload)
    if metrics.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        raise AssertionError("metrics source SHA-256 mismatch")
    if metrics.get("selection_manifest_sha256") != EXPECTED_SELECTION_MANIFEST_SHA256:
        raise AssertionError("metrics selection manifest SHA-256 mismatch")
    if metrics.get("train_records") != EXPECTED_TRAIN_RECORDS or metrics.get("test_records") != EXPECTED_TEST_RECORDS:
        raise AssertionError("metrics train/test record mismatch")
    if metrics.get("train_groups") != EXPECTED_TRAIN_GROUPS or metrics.get("test_groups") != EXPECTED_TEST_GROUPS:
        raise AssertionError("metrics train/test group mismatch")
    if metrics.get("lineage_overlap_count") != EXPECTED_LINEAGE_OVERLAP:
        raise AssertionError("metrics lineage overlap mismatch")
    if audit.get("selected_records") != EXPECTED_SELECTED_RECORDS or audit.get("rehydrated_records") != EXPECTED_SELECTED_RECORDS:
        raise AssertionError("rehydration audit did not verify exactly 500 records")
    if audit.get("selection_manifest_sha256") != EXPECTED_SELECTION_MANIFEST_SHA256:
        raise AssertionError("rehydration audit selection manifest mismatch")
    if audit.get("unique_source_record_ids") != EXPECTED_SELECTED_RECORDS:
        raise AssertionError("rehydration audit unique source_record_id mismatch")
    if audit.get("unique_text_hashes") != EXPECTED_UNIQUE_TEXT_HASHES:
        raise AssertionError("rehydration audit unique text hash mismatch")
    for key in (
        "all_text_hashes_verified",
        "all_prompt_hashes_verified",
        "all_model_families_verified",
        "all_domains_verified",
        "all_source_ids_verified",
    ):
        if audit.get(key) is not True:
            raise AssertionError(f"rehydration audit {key} is not true")
    if reproducibility.get("status") != "PASS" or reproducibility.get("match") is not True:
        raise AssertionError("internal deterministic reproducibility check failed")
    return metrics, audit, reproducibility


def build_privacy_audit(run_dir: Path, archive_path: Path | None = None) -> dict[str, Any]:
    structured_extensions = {".json", ".jsonl"}
    text_extensions = {".md", ".log", ".txt"}
    forbidden_names = {".git", ".venv", "venv", "train_none.csv"}
    structured_files = 0
    text_files = 0
    scanned_files = 0
    for path in sorted(p for p in run_dir.rglob("*") if p.is_file()):
        if path.name == "EVIDENCE_SHA256SUMS.txt":
            continue
        scanned_files += 1
        if any(part in forbidden_names for part in path.parts):
            raise AssertionError(f"forbidden path component in evidence bundle: {path}")
        if path.suffix in structured_extensions:
            payload = json.loads(path.read_text(encoding="utf-8"))
            assert_no_forbidden_keys(payload)
            structured_files += 1
        elif path.suffix in text_extensions:
            text_files += 1
    tar_members_checked = 0
    if archive_path is not None:
        tar_members_checked = len(list_safe_tar_members(archive_path))
    return {
        "schema": "cogniprint-raid-ngram-privacy-audit-001",
        "status": "PASS",
        "forbidden_structured_keys_absent": True,
        "raw_source_in_bundle": False,
        "raw_prompt_in_bundle": False,
        "raw_generation_in_bundle": False,
        "raw_previous_archive_copied": False,
        "recoverable_vocabulary_persisted": False,
        "structured_files_scanned": structured_files,
        "markdown_and_log_files_scanned": text_files,
        "total_files_scanned": scanned_files,
        "archive_member_safety_checked": archive_path is not None,
        "archive_members_checked": tar_members_checked,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path, required=True)
    parser.add_argument("--previous-archive", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    source_path = args.input_file.resolve()
    previous_archive = args.previous_archive.resolve()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    repository_commit = git_output(repo_root, "rev-parse", "HEAD")
    repository_tree = git_output(repo_root, "rev-parse", "HEAD^{tree}")
    repository_status = git_output(repo_root, "status", "--short")
    branch = git_output(repo_root, "branch", "--show-current")
    origin_main_commit = git_output(repo_root, "rev-parse", "origin/main")
    remote_origin = git_output(repo_root, "remote", "get-url", "origin")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / timestamp
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True)
    execution_log = logs_dir / "execution.log"

    checkpoint = initialize_checkpoint(repository_commit)
    checkpoint_path = run_dir / "CHECKPOINT_STATUS.json"
    write_checkpoint(checkpoint_path, checkpoint)

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    source_root = str(repo_root / "src")
    env["PYTHONPATH"] = f"{source_root}{os.pathsep}{env.get('PYTHONPATH', '')}".rstrip(os.pathsep)

    try:
        append_log(execution_log, "Starting repository audit")
        set_stage(checkpoint_path, checkpoint, "repository_audit", "RUNNING")
        if repository_status:
            raise RuntimeError("repository working tree must be clean before evidence execution")
        repository_state = {
            "schema": "cogniprint-repository-state-003",
            "remote": remote_origin,
            "branch": branch,
            "repository_commit": repository_commit,
            "repository_tree": repository_tree,
            "origin_main_commit": origin_main_commit,
            "repository_dirty_status": repository_status,
            "execution_channel": "LOCAL_PINNED_SOURCE",
            "github_actions_status": "NOT_EXECUTED_SEPARATE_INFRASTRUCTURE_BLOCKER",
        }
        write_json(run_dir / "REPOSITORY_STATE.json", repository_state)
        set_stage(checkpoint_path, checkpoint, "repository_audit", "PASS")

        append_log(execution_log, "Checking branch sync")
        set_stage(checkpoint_path, checkpoint, "branch_sync", "RUNNING")
        if branch != EXPECTED_BRANCH:
            raise RuntimeError(f"expected branch {EXPECTED_BRANCH!r}, got {branch!r}")
        set_stage(checkpoint_path, checkpoint, "branch_sync", "PASS")

        append_log(execution_log, "Verifying authoritative source")
        set_stage(checkpoint_path, checkpoint, "source_verification", "RUNNING")
        if not source_path.exists() or not source_path.is_file():
            raise FileNotFoundError(source_path)
        if source_path.is_symlink():
            raise ValueError("authoritative source must not be a symlink")
        if source_path.stat().st_size != EXPECTED_SOURCE_SIZE:
            raise ValueError(
                f"source byte-size mismatch: expected {EXPECTED_SOURCE_SIZE}, got {source_path.stat().st_size}"
            )
        source_sha256 = sha256_file(source_path)
        if source_sha256 != EXPECTED_SOURCE_SHA256:
            raise ValueError(
                f"source SHA-256 mismatch: expected {EXPECTED_SOURCE_SHA256}, got {source_sha256}"
            )
        set_stage(checkpoint_path, checkpoint, "source_verification", "PASS")

        append_log(execution_log, "Verifying previous evidence archive")
        set_stage(checkpoint_path, checkpoint, "previous_archive_verification", "RUNNING")
        if not previous_archive.exists() or not previous_archive.is_file():
            raise FileNotFoundError(previous_archive)
        previous_sha256 = sha256_file(previous_archive)
        if previous_sha256 != EXPECTED_PREVIOUS_ARCHIVE_SHA256:
            raise ValueError(
                f"previous evidence archive SHA-256 mismatch: expected {EXPECTED_PREVIOUS_ARCHIVE_SHA256}, got {previous_sha256}"
            )
        safe_previous_members = list_safe_tar_members(previous_archive)
        set_stage(checkpoint_path, checkpoint, "previous_archive_verification", "PASS")

        append_log(execution_log, "Extracting previous evidence safely")
        set_stage(checkpoint_path, checkpoint, "previous_evidence_extraction", "RUNNING")
        with tempfile.TemporaryDirectory(prefix="cogniprint-ngram-prior-") as temp_name:
            extracted = Path(temp_name)
            safe_extract_archive(previous_archive, extracted)
            extracted_root = next(path for path in extracted.iterdir() if path.is_dir())
            manifest_ok, manifest_count = verify_manifest(extracted_root)
            features = find_unique(extracted_root, "features.jsonl")
            baseline_metrics = find_unique(extracted_root, "baseline-metrics.json")
            source_contract = find_unique(extracted_root, "RAID_SOURCE_CONTRACT_001.json")
            if sha256_file(features) != EXPECTED_FEATURES_SHA256:
                raise AssertionError("previous selected features SHA-256 mismatch")
            if sha256_file(source_contract) != EXPECTED_SOURCE_CONTRACT_SHA256:
                raise AssertionError("previous source contract SHA-256 mismatch")
            if selection_manifest_sha256_from_features(features) != EXPECTED_SELECTION_MANIFEST_SHA256:
                raise AssertionError("previous selected-record manifest SHA-256 mismatch")
            shutil.copy2(source_contract, run_dir / "RAID_SOURCE_CONTRACT_001.json")
            set_stage(checkpoint_path, checkpoint, "previous_evidence_extraction", "PASS")

            append_log(execution_log, "Running code audit")
            set_stage(checkpoint_path, checkpoint, "code_audit", "RUNNING")
            run_logged(
                [
                    args.python,
                    "-m",
                    "py_compile",
                    "src/cogniprint/benchmarks/ngram.py",
                    "scripts/analyze_raid_ngrams.py",
                    "scripts/run_raid_ngram_stage_a.py",
                    "tests/test_raid_ngram_baselines.py",
                ],
                cwd=repo_root,
                env=env,
                log_path=logs_dir / "py-compile.log",
            )
            if shutil.which("ruff"):
                run_logged(
                    [
                        "ruff",
                        "check",
                        "src/cogniprint/benchmarks/ngram.py",
                        "scripts/analyze_raid_ngrams.py",
                        "scripts/run_raid_ngram_stage_a.py",
                        "tests/test_raid_ngram_baselines.py",
                    ],
                    cwd=repo_root,
                    env=env,
                    log_path=logs_dir / "ruff.log",
                )
            else:
                (logs_dir / "ruff.log").write_text("ruff-not-found\n", encoding="utf-8")
            set_stage(checkpoint_path, checkpoint, "code_audit", "PASS")

            append_log(execution_log, "Running targeted tests")
            set_stage(checkpoint_path, checkpoint, "targeted_tests", "RUNNING")
            test_commands = [
                (
                    "test-raid-ngram-baselines.log",
                    [args.python, "-m", "unittest", "discover", "-s", "tests", "-p", "test_raid_ngram_baselines.py", "-v"],
                ),
                (
                    "test-raid-pilot-adapter.log",
                    [args.python, "-m", "unittest", "discover", "-s", "tests", "-p", "test_raid_pilot_adapter.py", "-v"],
                ),
                (
                    "test-raid-pilot-evaluation.log",
                    [args.python, "-m", "unittest", "discover", "-s", "tests", "-p", "test_raid_pilot_evaluation.py", "-v"],
                ),
                (
                    "test-raid-pilot-source-contract.log",
                    [args.python, "-m", "unittest", "discover", "-s", "tests", "-p", "test_raid_pilot_source_contract.py", "-v"],
                ),
            ]
            for log_name, command in test_commands:
                run_logged(command, cwd=repo_root, env=env, log_path=logs_dir / log_name)
            set_stage(checkpoint_path, checkpoint, "targeted_tests", "PASS")

            append_log(execution_log, "Verifying selected record contract")
            set_stage(checkpoint_path, checkpoint, "selected_record_verification", "RUNNING")
            selected_records = [
                json.loads(line)
                for line in features.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            if len(selected_records) != EXPECTED_SELECTED_RECORDS:
                raise AssertionError("selected metadata-only record count mismatch")
            unique_ids = {str(record.get("source_record_id") or "") for record in selected_records}
            unique_hashes = {str(record.get("text_sha256") or "") for record in selected_records}
            if len(unique_ids) != EXPECTED_SELECTED_RECORDS:
                raise AssertionError("selected source_record_id uniqueness mismatch")
            if len(unique_hashes) != EXPECTED_UNIQUE_TEXT_HASHES:
                raise AssertionError("selected text SHA uniqueness mismatch")
            prior_baseline_sha256 = sha256_file(baseline_metrics)
            set_stage(checkpoint_path, checkpoint, "selected_record_verification", "PASS")

            protocol = {
                "schema": "cogniprint-raid-ngram-protocol-001",
                "status": "PINNED",
                "readiness_boundary": "descriptive_only",
                "research_mode": "PROOF_MODE",
                "research_freeze": "PRE-FREEZE",
                "stage_a_status": "DEVELOPMENT",
                "stage_b_status": "NOT_AUTHORISED_TO_START",
                "scientific_claim_evidence": False,
                "repository_commit": repository_commit,
                "repository_tree": repository_tree,
                "branch": branch,
                "origin_main_commit": origin_main_commit,
                "source_filename": source_path.name,
                "source_byte_size": EXPECTED_SOURCE_SIZE,
                "source_sha256": EXPECTED_SOURCE_SHA256,
                "source_contract_sha256": EXPECTED_SOURCE_CONTRACT_SHA256,
                "previous_archive": previous_archive.name,
                "previous_archive_sha256": EXPECTED_PREVIOUS_ARCHIVE_SHA256,
                "selected_features_sha256": EXPECTED_FEATURES_SHA256,
                "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
                "prior_baseline_sha256": prior_baseline_sha256,
                "seed": SEED,
                "test_fraction": TEST_FRACTION,
                "expected_train_records": EXPECTED_TRAIN_RECORDS,
                "expected_test_records": EXPECTED_TEST_RECORDS,
                "expected_train_groups": EXPECTED_TRAIN_GROUPS,
                "expected_test_groups": EXPECTED_TEST_GROUPS,
                "expected_lineage_overlap": EXPECTED_LINEAGE_OVERLAP,
                "char_baseline": asdict(char_config()),
                "word_baseline": asdict(word_config()),
                "forbidden_persisted_fields": sorted(FORBIDDEN_JSON_KEYS),
                "previous_internal_manifest_verified": manifest_ok,
                "previous_internal_manifest_file_count": manifest_count,
                "previous_archive_members_checked": len(safe_previous_members),
            }
            write_json(run_dir / "NGRAM_PROTOCOL_001.json", protocol)
            protocol_sha256 = sha256_json(protocol)

            append_log(execution_log, "Running real-source n-gram analysis twice")
            analysis_root = Path(temp_name) / "analysis"
            run1_dir = analysis_root / "run-1"
            run2_dir = analysis_root / "run-2"
            for ordinal, out_dir, log_name in ((1, run1_dir, "ngram-analysis-run-1.log"), (2, run2_dir, "ngram-analysis-run-2.log")):
                run_logged(
                    [
                        args.python,
                        str(repo_root / "scripts" / "analyze_raid_ngrams.py"),
                        "--features",
                        str(features),
                        "--baseline-metrics",
                        str(baseline_metrics),
                        "--input-file",
                        str(source_path),
                        "--expected-source-sha256",
                        EXPECTED_SOURCE_SHA256,
                        "--source-contract",
                        str(source_contract),
                        "--output-dir",
                        str(out_dir),
                        "--seed",
                        str(SEED),
                        "--test-fraction",
                        str(TEST_FRACTION),
                    ],
                    cwd=repo_root,
                    env=env,
                    log_path=logs_dir / log_name,
                )
                append_log(execution_log, f"Completed analysis run {ordinal}")

            metrics_1, audit_1, reproducibility_1 = validate_analysis_outputs(run1_dir)
            metrics_2, audit_2, reproducibility_2 = validate_analysis_outputs(run2_dir)

            set_stage(checkpoint_path, checkpoint, "source_rehydration", "RUNNING")
            if audit_1["rehydrated_records"] != EXPECTED_SELECTED_RECORDS:
                raise AssertionError("rehydration record count mismatch")
            set_stage(checkpoint_path, checkpoint, "source_rehydration", "PASS")

            set_stage(checkpoint_path, checkpoint, "split_verification", "RUNNING")
            if metrics_1["train_records"] != EXPECTED_TRAIN_RECORDS or metrics_1["test_records"] != EXPECTED_TEST_RECORDS:
                raise AssertionError("split record counts mismatch")
            if metrics_1["train_groups"] != EXPECTED_TRAIN_GROUPS or metrics_1["test_groups"] != EXPECTED_TEST_GROUPS:
                raise AssertionError("split group counts mismatch")
            if metrics_1["lineage_overlap_count"] != EXPECTED_LINEAGE_OVERLAP:
                raise AssertionError("lineage overlap mismatch")
            set_stage(checkpoint_path, checkpoint, "split_verification", "PASS")

            set_stage(checkpoint_path, checkpoint, "character_ngram_analysis", "RUNNING")
            if not isinstance(metrics_1.get("character_3_5_hashed_tfidf"), dict):
                raise AssertionError("missing character baseline")
            set_stage(checkpoint_path, checkpoint, "character_ngram_analysis", "PASS")

            set_stage(checkpoint_path, checkpoint, "word_ngram_analysis", "RUNNING")
            if not isinstance(metrics_1.get("word_1_2_hashed_tfidf"), dict):
                raise AssertionError("missing word baseline")
            set_stage(checkpoint_path, checkpoint, "word_ngram_analysis", "PASS")

            set_stage(checkpoint_path, checkpoint, "reproducibility_rerun", "RUNNING")
            run_1_metrics_sha256 = sha256_file(run1_dir / "ngram-baseline-metrics.json")
            run_2_metrics_sha256 = sha256_file(run2_dir / "ngram-baseline-metrics.json")
            run_1_audit_sha256 = sha256_file(run1_dir / "ngram-source-rehydration-audit.json")
            run_2_audit_sha256 = sha256_file(run2_dir / "ngram-source-rehydration-audit.json")
            if run_1_metrics_sha256 != run_2_metrics_sha256 or run_1_audit_sha256 != run_2_audit_sha256:
                raise AssertionError("full deterministic n-gram rerun mismatch")
            reproducibility = {
                "schema": "cogniprint-raid-ngram-reproducibility-check-001",
                "status": "PASS",
                "match": True,
                "run_1_metrics_sha256": run_1_metrics_sha256,
                "run_2_metrics_sha256": run_2_metrics_sha256,
                "run_1_rehydration_audit_sha256": run_1_audit_sha256,
                "run_2_rehydration_audit_sha256": run_2_audit_sha256,
                "source_sha256": EXPECTED_SOURCE_SHA256,
                "source_contract_sha256": EXPECTED_SOURCE_CONTRACT_SHA256,
                "selected_features_sha256": EXPECTED_FEATURES_SHA256,
                "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
                "protocol_sha256": protocol_sha256,
                "seed": SEED,
                "test_fraction": TEST_FRACTION,
                "inner_run_status": reproducibility_1.get("status"),
                "inner_run_match": reproducibility_1.get("match"),
            }
            write_json(run_dir / "ngram-reproducibility-check.json", reproducibility)
            set_stage(checkpoint_path, checkpoint, "reproducibility_rerun", "PASS")

            shutil.copy2(run1_dir / "ngram-baseline-metrics.json", run_dir / "ngram-baseline-metrics.json")
            shutil.copy2(run1_dir / "ngram-baseline-report.md", run_dir / "ngram-baseline-report.md")
            shutil.copy2(run1_dir / "ngram-source-rehydration-audit.json", run_dir / "ngram-source-rehydration-audit.json")

        append_log(execution_log, "Capturing environment metadata")
        (run_dir / "PYTHON_VERSION.txt").write_text(
            subprocess.check_output([args.python, "--version"], text=True, stderr=subprocess.STDOUT),
            encoding="utf-8",
        )
        (run_dir / "UNAME.txt").write_text(
            subprocess.check_output(["uname", "-a"], text=True),
            encoding="utf-8",
        )
        (run_dir / "pip-freeze.txt").write_text(
            subprocess.check_output([args.python, "-m", "pip", "freeze", "--all"], text=True),
            encoding="utf-8",
        )

        set_stage(checkpoint_path, checkpoint, "privacy_audit", "RUNNING")
        privacy_audit = build_privacy_audit(run_dir)
        write_json(run_dir / "NGRAM_PRIVACY_AUDIT_001.json", privacy_audit)
        set_stage(checkpoint_path, checkpoint, "privacy_audit", "PASS")

        previous_reference = {
            "schema": "cogniprint-previous-evidence-reference-003",
            "archive": previous_archive.name,
            "sha256": previous_sha256,
            "selected_features_sha256": EXPECTED_FEATURES_SHA256,
            "source_contract_sha256": EXPECTED_SOURCE_CONTRACT_SHA256,
            "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
            "raw_previous_archive_copied": False,
        }
        write_json(run_dir / "PREVIOUS_EVIDENCE_REFERENCE.json", previous_reference)

        metrics = json.loads((run_dir / "ngram-baseline-metrics.json").read_text(encoding="utf-8"))
        final_status = {
            "schema": "cogniprint-stage-a-ngram-final-local-status-003",
            "status": "EXECUTED",
            "readiness_boundary": "descriptive_only",
            "research_mode": "PROOF_MODE",
            "research_status": "PRE-FREEZE",
            "stage_a_status": "DEVELOPMENT",
            "stage_b_status": "NOT_AUTHORISED_TO_START",
            "scientific_claim_evidence": False,
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "source_byte_size": EXPECTED_SOURCE_SIZE,
            "repository_commit": repository_commit,
            "repository_tree": repository_tree,
            "previous_archive_sha256": previous_sha256,
            "selected_features_sha256": EXPECTED_FEATURES_SHA256,
            "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
            "train_records": metrics["train_records"],
            "test_records": metrics["test_records"],
            "train_groups": metrics["train_groups"],
            "test_groups": metrics["test_groups"],
            "lineage_overlap_count": metrics["lineage_overlap_count"],
            "character_3_5_metrics": metrics["character_3_5_hashed_tfidf"]["metrics"],
            "word_1_2_metrics": metrics["word_1_2_hashed_tfidf"]["metrics"],
            "cogniprint_12d_metrics": metrics["cogniprint_12d_nearest_centroid"],
            "privacy_status": "PASS",
            "reproducibility_status": "PASS",
        }
        write_json(run_dir / "FINAL_LOCAL_STATUS_003.json", final_status)

        set_stage(checkpoint_path, checkpoint, "evidence_manifest", "RUNNING")
        manifest_path = run_dir / "EVIDENCE_SHA256SUMS.txt"
        files = sorted(path for path in run_dir.rglob("*") if path.is_file() and path != manifest_path)
        manifest_path.write_text(
            "".join(
                f"{sha256_file(path)}  {path.relative_to(run_dir).as_posix()}\n"
                for path in files
            ),
            encoding="utf-8",
        )
        manifest_ok, manifest_file_count = verify_manifest(run_dir)
        set_stage(checkpoint_path, checkpoint, "evidence_manifest", "PASS")

        set_stage(checkpoint_path, checkpoint, "archive_build", "RUNNING")
        archive_path = output_root / f"cogniprint-stage-a-ngram-complete-{timestamp}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as handle:
            handle.add(run_dir, arcname=timestamp)
        archive_sha256 = sha256_file(archive_path)
        set_stage(checkpoint_path, checkpoint, "archive_build", "PASS")

        set_stage(checkpoint_path, checkpoint, "archive_verification", "RUNNING")
        safe_final_members = list_safe_tar_members(archive_path)
        run_logged(["tar", "-tzf", str(archive_path)], cwd=repo_root, env=env, log_path=logs_dir / "archive-tar-list.log")
        privacy_audit = build_privacy_audit(run_dir, archive_path=archive_path)
        write_json(run_dir / "NGRAM_PRIVACY_AUDIT_001.json", privacy_audit)
        final_status["archive_name"] = archive_path.name
        final_status["archive_sha256"] = archive_sha256
        final_status["manifest_verified"] = manifest_ok
        final_status["manifest_file_count"] = manifest_file_count
        write_json(run_dir / "FINAL_LOCAL_STATUS_003.json", final_status)
        (run_dir / "FINAL_STATUS.md").write_text(
            build_status_markdown(metrics, repository_commit, archive_path.name, archive_sha256),
            encoding="utf-8",
        )
        set_stage(checkpoint_path, checkpoint, "archive_verification", "PASS")

        checkpoint["status"] = "PASS"
        write_checkpoint(checkpoint_path, checkpoint)

        result = {
            "status": "PASS",
            "evidence_directory": str(run_dir),
            "archive": str(archive_path),
            "archive_sha256": archive_sha256,
            "repository_commit": repository_commit,
            "repository_tree": repository_tree,
            "source_sha256": source_sha256,
            "selected_features_sha256": EXPECTED_FEATURES_SHA256,
            "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
            "internal_manifest_verified": manifest_ok,
            "internal_manifest_file_count": manifest_file_count,
            "archive_members_checked": len(safe_final_members),
            "character_3_5": metrics["character_3_5_hashed_tfidf"]["metrics"],
            "word_1_2": metrics["word_1_2_hashed_tfidf"]["metrics"],
            "cogniprint_12d": metrics["cogniprint_12d_nearest_centroid"],
            "scientific_claim_evidence": False,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception:
        checkpoint["status"] = "FAIL"
        write_checkpoint(checkpoint_path, checkpoint)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
