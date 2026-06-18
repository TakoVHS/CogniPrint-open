#!/usr/bin/env python3
"""Build or validate an allowlist-driven sanitized CogniPrint release tree."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "public-release.json"
DEFAULT_DESTINATION = ROOT / "release_artifacts" / "public-release"
PUBLIC_RELEASE_MANIFEST = "PUBLIC_RELEASE_MANIFEST.json"
PUBLIC_GITIGNORE = """# CogniPrint sanitized public release
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.env
.env.*
!.env.example
workspace/
release_artifacts/
dist/
build/
*.egg-info/
.DS_Store
"""

ALLOW_MARKERS = (
    "example",
    "placeholder",
    "redacted",
    "dummy",
    "changeme",
    "not-a-real",
    "test value",
    "test_only",
    "${",
    "<secret",
    "<token",
    "<password",
    "<api-key",
    "<api_key",
)

SECRET_RULES = (
    ("stripe_secret_key", re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    ("stripe_webhook_secret", re.compile(r"\bwhsec_[A-Za-z0-9]{16,}\b")),
    ("openai_api_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("huggingface_token", re.compile(r"\bhf_[A-Za-z0-9]{20,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("sendgrid_key", re.compile(r"\bSG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("telegram_bot_token", re.compile(r"\b[0-9]{8,12}:[A-Za-z0-9_-]{35,}\b")),
    ("private_key_header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    (
        "postgres_dsn_with_password",
        re.compile(r"\bpostgres(?:ql)?://[^:\s/@]+:[^@\s]+@[^/\s]+/[^\s]+"),
    ),
    (
        "mongodb_dsn_with_password",
        re.compile(r"\bmongodb(?:\+srv)?://[^:\s/@]+:[^@\s]+@[^\s]+"),
    ),
    ("redis_dsn_with_password", re.compile(r"\bredis://[^:\s/@]*:[^@\s]+@[^\s]+")),
)

PORTAL_NAME = "sm" + "apply"
SCHMIDT_CODE_PREFIX = "TAI" + "-RFP-"
PRIVATE_RULES = (
    (
        "grant_application_id",
        re.compile(r"\b(?:grant|funding|submission|portal)\s+application\s+id\s*:", re.IGNORECASE),
    ),
    ("gmail_message_id", re.compile(r"\bgmail(?:\s+confirmation)?\s+message\s+id\b", re.IGNORECASE)),
    ("smapply_portal_reference", re.compile(rf"\b{PORTAL_NAME}\b", re.IGNORECASE)),
    ("portal_paste_pack", re.compile(r"\bportal\s+paste\s+pack\b", re.IGNORECASE)),
    ("uploaded_headshot", re.compile(r"\buploaded\s+headshot\b", re.IGNORECASE)),
    ("schmidt_application_code", re.compile(rf"\b{SCHMIDT_CODE_PREFIX}[A-Z0-9-]+\b")),
)


class ReleaseError(RuntimeError):
    """Raised when a release candidate violates a release gate."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Release configuration JSON.")
    parser.add_argument(
        "--destination",
        type=Path,
        default=DEFAULT_DESTINATION,
        help="Destination directory for the release candidate.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate the selected source files without writing a release tree.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove an existing destination before exporting.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    config_path = resolve_from_root(root, args.config)
    destination = resolve_from_root(root, args.destination)
    config = load_config(config_path)

    tracked = tracked_files(root)
    selected = select_paths(tracked, config)
    validate_required_files(selected, config)
    validate_public_safe_workflows(selected, config)
    findings = scan_selected_files(root, selected)
    if findings:
        print("Public release validation failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1

    if args.check_only:
        print(f"Public release check passed: {len(selected)} tracked files selected.")
        print(f"Excluded from candidate: {len(tracked) - len(selected)} tracked files.")
        return 0

    prepare_destination(root, destination, clean=args.clean)
    manifest = export_files(root, destination, selected)
    manifest_path = destination / PUBLIC_RELEASE_MANIFEST
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    verify_manifest_parity(destination, manifest, ignored_paths={PUBLIC_RELEASE_MANIFEST})

    print(f"Public release candidate created at: {destination}")
    print(f"Files exported: {len(manifest['files'])}")
    print(f"Manifest: {manifest_path}")
    print("Manual review is still required before publication.")
    return 0


def resolve_from_root(root: Path, value: Path) -> Path:
    return value.resolve() if value.is_absolute() else (root / value).resolve()


def load_config(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReleaseError(f"Release configuration not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReleaseError(f"Invalid release configuration JSON: {exc}") from exc

    for key in ("include", "exclude", "blocked_suffixes", "required_files"):
        value = data.get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ReleaseError(f"Configuration key {key!r} must be a list of strings.")
    public_safe_workflows = data.get("public_safe_workflows", [])
    if not isinstance(public_safe_workflows, list) or not all(
        isinstance(item, str) for item in public_safe_workflows
    ):
        raise ReleaseError("Configuration key 'public_safe_workflows' must be a list of strings.")
    data["public_safe_workflows"] = public_safe_workflows
    return data


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return sorted(line for line in result.stdout.splitlines() if line)


def select_paths(paths: Iterable[str], config: dict[str, Any]) -> list[str]:
    include_patterns = config["include"]
    exclude_patterns = config["exclude"]
    blocked_suffixes = {suffix.casefold() for suffix in config["blocked_suffixes"]}
    public_safe_workflows = set(config.get("public_safe_workflows", []))

    selected: list[str] = []
    for raw_path in paths:
        path = raw_path.replace("\\", "/")
        if path in public_safe_workflows:
            selected.append(path)
            continue
        if Path(path).suffix.casefold() in blocked_suffixes:
            continue
        if not any(fnmatch.fnmatchcase(path, pattern) for pattern in include_patterns):
            continue
        if any(fnmatch.fnmatchcase(path, pattern) for pattern in exclude_patterns):
            continue
        selected.append(path)
    return sorted(set(selected))


def validate_required_files(selected: list[str], config: dict[str, Any]) -> None:
    missing = sorted(set(config["required_files"]) - set(selected))
    if missing:
        raise ReleaseError(f"Required public release files are missing: {', '.join(missing)}")
    if len(selected) < 10:
        raise ReleaseError("Release selection is unexpectedly small; inspect the allowlist configuration.")


def validate_public_safe_workflows(selected: list[str], config: dict[str, Any]) -> None:
    expected = sorted(config.get("public_safe_workflows", []))
    if not expected:
        return
    if len(expected) != 1:
        raise ReleaseError("Exactly one public-safe workflow must be configured for the sanitized candidate.")

    selected_workflows = sorted(path for path in selected if path.startswith(".github/workflows/"))
    if selected_workflows != expected:
        raise ReleaseError(
            "Sanitized candidate must include exactly the configured public-safe workflow: "
            f"expected {expected}, selected {selected_workflows}"
        )


def scan_selected_files(root: Path, selected: Iterable[str]) -> list[str]:
    findings: list[str] = []
    for rel_path in selected:
        source = root / rel_path
        if source.is_symlink():
            findings.append(f"symlink_not_allowed: {rel_path}")
            continue
        try:
            raw = source.read_bytes()
        except OSError as exc:
            findings.append(f"unreadable_file: {rel_path}: {exc}")
            continue
        if b"\0" in raw[:4096]:
            findings.append(f"binary_file_not_allowed: {rel_path}")
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(f"non_utf8_file_not_allowed: {rel_path}")
            continue

        for line_number, line in enumerate(text.splitlines(), 1):
            lowered = line.casefold()
            allow_secret_example = any(marker in lowered for marker in ALLOW_MARKERS)
            if not allow_secret_example:
                for rule_name, pattern in SECRET_RULES:
                    if pattern.search(line):
                        findings.append(f"{rule_name}: {rel_path}:{line_number}")
            for rule_name, pattern in PRIVATE_RULES:
                if pattern.search(line):
                    findings.append(f"{rule_name}: {rel_path}:{line_number}")
    return sorted(set(findings))


def prepare_destination(root: Path, destination: Path, *, clean: bool) -> None:
    if destination == root or destination in root.parents:
        raise ReleaseError("Destination cannot be the repository root or one of its parent directories.")
    if destination.exists():
        if not clean:
            raise ReleaseError(f"Destination already exists: {destination}. Use --clean to replace it.")
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=False)


def file_record(path: Path, relative_path: str) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": relative_path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
    }


def export_files(root: Path, destination: Path, selected: Iterable[str]) -> dict[str, Any]:
    selected_paths = list(selected)
    records: list[dict[str, Any]] = []
    for rel_path in selected_paths:
        source = root / rel_path
        target = destination / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        records.append(file_record(target, rel_path))

    if ".gitignore" not in selected_paths:
        public_gitignore = destination / ".gitignore"
        public_gitignore.write_text(PUBLIC_GITIGNORE, encoding="utf-8")
        records.append(file_record(public_gitignore, ".gitignore"))

    records.sort(key=lambda record: record["path"])
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_commit": git_head(root),
        "scientific_readiness": "descriptive_only",
        "external_methodological_reviews": "0/1",
        "publication_status": "release_candidate_requires_manual_review",
        "files": records,
    }


def verify_manifest_parity(
    destination: Path,
    manifest: dict[str, Any],
    *,
    ignored_paths: set[str] | None = None,
) -> None:
    ignored_paths = ignored_paths or set()
    manifest_files = manifest.get("files")
    if not isinstance(manifest_files, list):
        raise ReleaseError("Manifest parity check failed: manifest['files'] is not a list.")

    expected: dict[str, dict[str, Any]] = {}
    for record in manifest_files:
        if not isinstance(record, dict):
            raise ReleaseError("Manifest parity check failed: file record is not an object.")
        path = record.get("path")
        sha256 = record.get("sha256")
        size_bytes = record.get("size_bytes")
        if not isinstance(path, str) or not isinstance(sha256, str) or not isinstance(size_bytes, int):
            raise ReleaseError(f"Manifest parity check failed: malformed record {record!r}.")
        expected[path] = record

    actual_paths = sorted(
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*")
        if path.is_file() and path.relative_to(destination).as_posix() not in ignored_paths
    )
    expected_paths = sorted(expected)
    missing = sorted(set(expected_paths) - set(actual_paths))
    extra = sorted(set(actual_paths) - set(expected_paths))
    if missing or extra:
        raise ReleaseError(
            "Manifest parity check failed: "
            f"missing={missing or 'none'}, extra={extra or 'none'}"
        )

    mismatches: list[str] = []
    for rel_path in actual_paths:
        actual = file_record(destination / rel_path, rel_path)
        expected_record = expected[rel_path]
        if actual["sha256"] != expected_record["sha256"] or actual["size_bytes"] != expected_record["size_bytes"]:
            mismatches.append(rel_path)
    if mismatches:
        raise ReleaseError(f"Manifest parity check failed: hash/size mismatch for {', '.join(mismatches)}")


def git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ReleaseError, subprocess.SubprocessError) as exc:
        print(f"Public release export failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
