#!/usr/bin/env python3
"""Execute and package the pinned Stage A RAID n-gram comparison.

This orchestrator verifies the prior evidence chain and authoritative raw source,
runs the targeted tests and n-gram analysis, then writes a chained evidence
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_SOURCE_SHA256 = "c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4"
EXPECTED_SOURCE_SIZE = 801_662_741
EXPECTED_PREVIOUS_ARCHIVE_SHA256 = "9f7a0c39f24ee71539cb74d896d204e4220261dc1ddfa2343b44d2ac72a04a82"
EXPECTED_FEATURES_SHA256 = "13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca"
EXPECTED_SOURCE_CONTRACT_SHA256 = "e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948"
EXPECTED_SELECTION_MANIFEST_SHA256 = "30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb"
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
        ["git", *args], cwd=repo_root, text=True, stderr=subprocess.STDOUT
    ).strip()


def run_logged(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    log_path: Path,
) -> None:
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
            f"command failed with exit code {completed.returncode}: {' '.join(command)}; "
            f"see {log_path}"
        )


def safe_extract(archive: Path, destination: Path) -> None:
    destination_resolved = destination.resolve()
    with tarfile.open(archive, "r:gz") as handle:
        for member in handle.getmembers():
            candidate = (destination / member.name).resolve()
            if candidate != destination_resolved and destination_resolved not in candidate.parents:
                raise ValueError(f"unsafe archive member: {member.name}")
        handle.extractall(destination)


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


def validate_outputs(output_dir: Path) -> dict[str, Any]:
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

    expected_metrics = {
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
        "train_records": 351,
        "test_records": 149,
        "train_groups": 336,
        "test_groups": 145,
        "lineage_overlap_count": 0,
        "readiness_boundary": "descriptive_only",
        "research_status": "PRE-FREEZE",
        "stage_b_status": "NOT_AUTHORISED_TO_START",
        "scientific_claim_evidence": False,
    }
    for key, expected in expected_metrics.items():
        if metrics.get(key) != expected:
            raise AssertionError(
                f"metrics {key} mismatch: expected {expected!r}, got {metrics.get(key)!r}"
            )
    if audit.get("selected_records") != 500 or audit.get("rehydrated_records") != 500:
        raise AssertionError("rehydration audit did not verify exactly 500 records")
    if audit.get("selection_manifest_sha256") != EXPECTED_SELECTION_MANIFEST_SHA256:
        raise AssertionError("rehydration audit selection manifest mismatch")
    if audit.get("all_text_hashes_verified") is not True:
        raise AssertionError("text hashes were not fully verified")
    if audit.get("all_prompt_hashes_verified") is not True:
        raise AssertionError("prompt hashes were not fully verified")
    if reproducibility.get("status") != "PASS" or reproducibility.get("match") is not True:
        raise AssertionError("deterministic reproducibility check failed")

    for key in ("character_3_5_hashed_tfidf", "word_1_2_hashed_tfidf"):
        result = metrics.get(key)
        if not isinstance(result, dict) or not isinstance(result.get("metrics"), dict):
            raise AssertionError(f"missing {key} metrics")
        if result.get("persisted_vocabulary") is not False:
            raise AssertionError(f"{key} persisted a vocabulary")
        if result.get("raw_text_persisted") is not False:
            raise AssertionError(f"{key} persisted raw text")

    return {
        "metrics": metrics,
        "audit": audit,
        "reproducibility": reproducibility,
    }


def metric_row(payload: dict[str, Any]) -> str:
    return (
        f"accuracy={payload['accuracy']:.6f}, "
        f"balanced_accuracy={payload['balanced_accuracy']:.6f}, "
        f"macro_f1={payload['macro_f1']:.6f}"
    )


def build_status_markdown(validated: dict[str, Any], repository_commit: str) -> str:
    metrics = validated["metrics"]
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

    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    if source_path.stat().st_size != EXPECTED_SOURCE_SIZE:
        raise ValueError(
            f"source byte-size mismatch: expected {EXPECTED_SOURCE_SIZE}, "
            f"got {source_path.stat().st_size}"
        )
    source_sha256 = sha256_file(source_path)
    if source_sha256 != EXPECTED_SOURCE_SHA256:
        raise ValueError(
            f"source SHA-256 mismatch: expected {EXPECTED_SOURCE_SHA256}, got {source_sha256}"
        )
    previous_sha256 = sha256_file(previous_archive)
    if previous_sha256 != EXPECTED_PREVIOUS_ARCHIVE_SHA256:
        raise ValueError(
            "previous evidence archive SHA-256 mismatch: "
            f"expected {EXPECTED_PREVIOUS_ARCHIVE_SHA256}, got {previous_sha256}"
        )

    repository_commit = git_output(repo_root, "rev-parse", "HEAD")
    repository_tree = git_output(repo_root, "rev-parse", "HEAD^{tree}")
    repository_status = git_output(repo_root, "status", "--short")
    if repository_status:
        raise RuntimeError("repository working tree must be clean before evidence execution")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / timestamp
    logs_dir = run_dir / "logs"
    ngram_dir = run_dir / "ngram"
    logs_dir.mkdir(parents=True)
    ngram_dir.mkdir(parents=True)

    checkpoint = {
        "schema": "cogniprint-stage-a-ngram-checkpoint-001",
        "status": "RUNNING",
        "repository_commit": repository_commit,
        "source_sha256": source_sha256,
        "previous_archive_sha256": previous_sha256,
    }
    write_json(run_dir / "CHECKPOINT_STATUS.json", checkpoint)

    env = os.environ.copy()
    source_root = str(repo_root / "src")
    env["PYTHONPATH"] = f"{source_root}{os.pathsep}{env.get('PYTHONPATH', '')}".rstrip(os.pathsep)

    with tempfile.TemporaryDirectory(prefix="cogniprint-ngram-prior-") as temp_name:
        extracted = Path(temp_name)
        safe_extract(previous_archive, extracted)
        features = find_unique(extracted, "features.jsonl")
        baseline_metrics = find_unique(extracted, "baseline-metrics.json")
        source_contract = find_unique(extracted, "RAID_SOURCE_CONTRACT_001.json")

        if sha256_file(features) != EXPECTED_FEATURES_SHA256:
            raise AssertionError("previous selected features SHA-256 mismatch")
        if sha256_file(source_contract) != EXPECTED_SOURCE_CONTRACT_SHA256:
            raise AssertionError("previous source contract SHA-256 mismatch")

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
            log_path=logs_dir / "ngram-unit-tests.log",
        )
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
                str(ngram_dir),
                "--seed",
                "20260725",
                "--test-fraction",
                "0.30",
            ],
            cwd=repo_root,
            env=env,
            log_path=logs_dir / "ngram-analysis.log",
        )

        shutil.copy2(source_contract, run_dir / "RAID_SOURCE_CONTRACT_001.json")

    validated = validate_outputs(ngram_dir)
    previous_reference = {
        "schema": "cogniprint-previous-evidence-reference-002",
        "archive_name": previous_archive.name,
        "archive_sha256": previous_sha256,
        "selected_features_sha256": EXPECTED_FEATURES_SHA256,
        "source_contract_sha256": EXPECTED_SOURCE_CONTRACT_SHA256,
        "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
        "raw_previous_archive_copied": False,
    }
    repository_state = {
        "schema": "cogniprint-repository-state-002",
        "repository_commit": repository_commit,
        "repository_tree": repository_tree,
        "repository_dirty_status": repository_status,
        "execution_channel": "LOCAL_PINNED_SOURCE",
        "github_actions_status": "NOT_EXECUTED_SEPARATE_INFRASTRUCTURE_BLOCKER",
    }
    final_status = {
        "schema": "cogniprint-stage-a-ngram-final-local-status-001",
        "status": "EXECUTED",
        "readiness_boundary": "descriptive_only",
        "research_status": "PRE-FREEZE",
        "stage_b_status": "NOT_AUTHORISED_TO_START",
        "scientific_claim_evidence": False,
        "source_sha256": source_sha256,
        "source_byte_size": source_path.stat().st_size,
        "repository_commit": repository_commit,
        "previous_archive_sha256": previous_sha256,
        "selection_manifest_sha256": EXPECTED_SELECTION_MANIFEST_SHA256,
        "train_records": validated["metrics"]["train_records"],
        "test_records": validated["metrics"]["test_records"],
        "lineage_overlap_count": validated["metrics"]["lineage_overlap_count"],
        "character_3_5_metrics": validated["metrics"]["character_3_5_hashed_tfidf"]["metrics"],
        "word_1_2_metrics": validated["metrics"]["word_1_2_hashed_tfidf"]["metrics"],
        "cogniprint_12d_metrics": validated["metrics"]["cogniprint_12d_nearest_centroid"],
    }
    write_json(run_dir / "PREVIOUS_EVIDENCE_REFERENCE.json", previous_reference)
    write_json(run_dir / "REPOSITORY_STATE.json", repository_state)
    write_json(run_dir / "FINAL_LOCAL_STATUS_003.json", final_status)
    (run_dir / "FINAL_STATUS.md").write_text(
        build_status_markdown(validated, repository_commit), encoding="utf-8"
    )

    checkpoint["status"] = "PASS"
    write_json(run_dir / "CHECKPOINT_STATUS.json", checkpoint)

    manifest_path = run_dir / "EVIDENCE_SHA256SUMS.txt"
    files = sorted(
        path for path in run_dir.rglob("*") if path.is_file() and path != manifest_path
    )
    manifest_path.write_text(
        "".join(
            f"{sha256_file(path)}  {path.relative_to(run_dir).as_posix()}\n"
            for path in files
        ),
        encoding="utf-8",
    )
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        actual = sha256_file(run_dir / relative)
        if actual != expected:
            raise AssertionError(f"evidence manifest mismatch for {relative}")

    archive_path = output_root / f"cogniprint-stage-a-ngram-complete-{timestamp}.tar.gz"
    with tarfile.open(archive_path, "w:gz") as handle:
        handle.add(run_dir, arcname=timestamp)
    with tarfile.open(archive_path, "r:gz") as handle:
        members = handle.getmembers()
        if not members:
            raise AssertionError("final evidence archive is empty")

    result = {
        "status": "PASS",
        "evidence_directory": str(run_dir),
        "archive": str(archive_path),
        "archive_sha256": sha256_file(archive_path),
        "repository_commit": repository_commit,
        "source_sha256": source_sha256,
        "character_3_5": validated["metrics"]["character_3_5_hashed_tfidf"]["metrics"],
        "word_1_2": validated["metrics"]["word_1_2_hashed_tfidf"]["metrics"],
        "cogniprint_12d": validated["metrics"]["cogniprint_12d_nearest_centroid"],
        "scientific_claim_evidence": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
