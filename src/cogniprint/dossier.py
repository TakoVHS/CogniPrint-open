"""Portable, deterministic and offline-verifiable CogniPrint evidence dossiers."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_ID = "urn:cogniprint:evidence-dossier:1"
SCHEMA_VERSION = 1
DOSSIER_FILENAME = "dossier.json"
ARTIFACTS_DIRECTORY = "artifacts"
DEFAULT_SOFTWARE_VERSION = "0.1.2"
MAX_MANIFEST_BYTES = 1_048_576
MAX_SOURCE_BYTES = 104_857_600
MAX_ARTIFACT_BYTES = 104_857_600
MAX_TOTAL_ARTIFACT_BYTES = 536_870_912
MAX_ARTIFACTS = 128
EMPTY_CONFIGURATION_BYTES = b"{}\n"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
VERSION_RE = re.compile(r"^[0-9]+(?:\.[0-9]+){1,3}[A-Za-z0-9.+-]*$")
CLAIM_BOUNDARY = (
    "descriptive-signals-only",
    "no-authorship-or-identity-claim",
    "no-legal-or-forensic-determination",
    "no-deterministic-model-source-claim",
)


class DossierError(RuntimeError):
    """Raised when a dossier cannot be created or verified safely."""


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise DossierError(f"dossier is not canonical JSON: {exc}") from exc
    return (text + "\n").encode("utf-8")


def _reject_constant(token: str) -> None:
    raise DossierError(f"non-finite JSON number is forbidden: {token}")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DossierError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_manifest(path: Path) -> tuple[dict[str, Any], bytes]:
    if path.is_symlink() or not path.is_file():
        raise DossierError("dossier.json must be a regular non-symlink file")
    size = path.stat().st_size
    if size > MAX_MANIFEST_BYTES:
        raise DossierError("dossier.json exceeds the maximum size")
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DossierError("dossier.json must be UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise DossierError(f"invalid dossier JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise DossierError("dossier root must be an object")
    if _canonical_bytes(value) != raw:
        raise DossierError("dossier.json is not in canonical JSON form")
    return value, raw


def _open_regular(path: Path, label: str) -> tuple[int, os.stat_result]:
    if path.is_symlink():
        raise DossierError(f"{label} must not be a symlink")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise DossierError(f"cannot open {label}: {path}") from exc
    metadata = os.fstat(descriptor)
    if not stat.S_ISREG(metadata.st_mode):
        os.close(descriptor)
        raise DossierError(f"{label} must be a regular file")
    return descriptor, metadata


def _hash_regular_file(path: Path, label: str, maximum: int) -> tuple[str, int]:
    descriptor, metadata = _open_regular(path, label)
    try:
        if metadata.st_size > maximum:
            raise DossierError(f"{label} exceeds the maximum size")
        digest = hashlib.sha256()
        count = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            if count > maximum:
                raise DossierError(f"{label} exceeds the maximum size")
            digest.update(chunk)
        if count != metadata.st_size:
            raise DossierError(f"{label} changed while it was read")
        return digest.hexdigest(), count
    finally:
        os.close(descriptor)


def _copy_regular_file(path: Path, destination: Path, label: str) -> tuple[str, int]:
    descriptor, metadata = _open_regular(path, label)
    try:
        if metadata.st_size > MAX_ARTIFACT_BYTES:
            raise DossierError(f"{label} exceeds the maximum size")
        destination.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256()
        count = 0
        with destination.open("xb") as output:
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                count += len(chunk)
                if count > MAX_ARTIFACT_BYTES:
                    raise DossierError(f"{label} exceeds the maximum size")
                digest.update(chunk)
                output.write(chunk)
        if count != metadata.st_size:
            raise DossierError(f"{label} changed while it was copied")
        return digest.hexdigest(), count
    finally:
        os.close(descriptor)


def _safe_artifact_path(value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 240:
        raise DossierError("artifact path must contain 1 to 240 characters")
    if "\\" in value or any(ord(character) < 32 for character in value):
        raise DossierError(f"unsafe artifact path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or str(path) != value:
        raise DossierError(f"artifact path must be normalized and relative: {value!r}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise DossierError(f"unsafe artifact path: {value!r}")
    for part in path.parts:
        if not re.fullmatch(r"[A-Za-z0-9._-]+", part):
            raise DossierError(f"artifact path contains unsupported characters: {value!r}")
    return value


def _require_exact_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DossierError(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        raise DossierError(f"{label} keys mismatch; missing={missing}, extra={extra}")
    return value


def _require_int(value: Any, label: str, maximum: int) -> int:
    if type(value) is not int or value < 0 or value > maximum:
        raise DossierError(f"{label} must be an integer in [0, {maximum}]")
    return value


def _require_hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise DossierError(f"{label} must be a lowercase SHA-256 hex digest")
    return value


def _validate_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    root_keys = {
        "$schema",
        "schema_version",
        "status",
        "scientific_claim_evidence",
        "source",
        "software",
        "configuration",
        "artifacts",
        "claim_boundary",
    }
    _require_exact_keys(manifest, root_keys, "dossier")
    if manifest["$schema"] != SCHEMA_ID or manifest["schema_version"] != SCHEMA_VERSION:
        raise DossierError("unknown or unsupported dossier schema")
    if manifest["status"] != "DEVELOPMENT_ONLY":
        raise DossierError("dossier status must remain DEVELOPMENT_ONLY")
    if manifest["scientific_claim_evidence"] is not False:
        raise DossierError("scientific_claim_evidence must be false")

    source = _require_exact_keys(manifest["source"], {"sha256", "byte_length", "included"}, "source")
    source_hash = _require_hash(source["sha256"], "source.sha256")
    source_size = _require_int(source["byte_length"], "source.byte_length", MAX_SOURCE_BYTES)
    if source["included"] is not False:
        raise DossierError("raw source inclusion is forbidden in dossier v1")

    software = _require_exact_keys(manifest["software"], {"name", "version", "commit"}, "software")
    if software["name"] != "cogniprint":
        raise DossierError("software.name must be cogniprint")
    if not isinstance(software["version"], str) or VERSION_RE.fullmatch(software["version"]) is None:
        raise DossierError("software.version is invalid")
    if not isinstance(software["commit"], str) or COMMIT_RE.fullmatch(software["commit"]) is None:
        raise DossierError("software.commit must be a lowercase 40-character Git SHA")

    configuration = _require_exact_keys(
        manifest["configuration"],
        {"sha256", "byte_length", "included", "basis"},
        "configuration",
    )
    configuration_hash = _require_hash(configuration["sha256"], "configuration.sha256")
    configuration_size = _require_int(
        configuration["byte_length"],
        "configuration.byte_length",
        MAX_SOURCE_BYTES,
    )
    if configuration["included"] is not False:
        raise DossierError("configuration content must not be embedded in dossier v1")
    if configuration["basis"] not in {"default-empty", "local-file-hash-only"}:
        raise DossierError("configuration.basis is invalid")

    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list) or not 1 <= len(artifacts) <= MAX_ARTIFACTS:
        raise DossierError(f"artifacts must contain 1 to {MAX_ARTIFACTS} entries")
    validated: list[dict[str, Any]] = []
    names: list[str] = []
    total = 0
    for index, raw_entry in enumerate(artifacts):
        entry = _require_exact_keys(
            raw_entry,
            {"path", "sha256", "byte_length", "media_type"},
            f"artifacts[{index}]",
        )
        name = _safe_artifact_path(entry["path"])
        digest = _require_hash(entry["sha256"], f"artifacts[{index}].sha256")
        size = _require_int(entry["byte_length"], f"artifacts[{index}].byte_length", MAX_ARTIFACT_BYTES)
        if entry["media_type"] != "application/octet-stream":
            raise DossierError("artifact media_type must be application/octet-stream")
        if (digest, size) in {(source_hash, source_size), (configuration_hash, configuration_size)}:
            raise DossierError("an artifact matches excluded source or configuration content")
        total += size
        if total > MAX_TOTAL_ARTIFACT_BYTES:
            raise DossierError("artifact total exceeds the maximum size")
        names.append(name)
        validated.append(entry)
    if names != sorted(names) or len(names) != len(set(names)):
        raise DossierError("artifact paths must be unique and lexicographically sorted")

    claim_boundary = manifest["claim_boundary"]
    if claim_boundary != list(CLAIM_BOUNDARY):
        raise DossierError("claim_boundary does not match the fixed dossier v1 boundary")
    return validated


def export_dossier(
    *,
    source: Path,
    artifacts: Mapping[str, Path],
    output: Path,
    software_commit: str,
    software_version: str = DEFAULT_SOFTWARE_VERSION,
    configuration: Path | None = None,
) -> dict[str, Any]:
    """Create a deterministic directory bundle without copying source/configuration content."""
    source = Path(source)
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise DossierError(f"output already exists: {output}")
    if not isinstance(software_commit, str) or COMMIT_RE.fullmatch(software_commit) is None:
        raise DossierError("software_commit must be a lowercase 40-character Git SHA")
    if not isinstance(software_version, str) or VERSION_RE.fullmatch(software_version) is None:
        raise DossierError("software_version is invalid")
    if not artifacts or len(artifacts) > MAX_ARTIFACTS:
        raise DossierError(f"provide 1 to {MAX_ARTIFACTS} artifacts")

    source_hash, source_size = _hash_regular_file(source, "source", MAX_SOURCE_BYTES)
    if configuration is None:
        configuration_hash = hashlib.sha256(EMPTY_CONFIGURATION_BYTES).hexdigest()
        configuration_size = len(EMPTY_CONFIGURATION_BYTES)
        configuration_basis = "default-empty"
    else:
        configuration_hash, configuration_size = _hash_regular_file(
            Path(configuration),
            "configuration",
            MAX_SOURCE_BYTES,
        )
        configuration_basis = "local-file-hash-only"

    normalized: list[tuple[str, Path]] = []
    seen: set[str] = set()
    for raw_name, raw_path in artifacts.items():
        name = _safe_artifact_path(raw_name)
        if name in seen:
            raise DossierError(f"duplicate artifact path: {name}")
        seen.add(name)
        normalized.append((name, Path(raw_path)))
    normalized.sort(key=lambda item: item[0])

    parent = output.parent
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".cogniprint-dossier-", dir=parent))
    try:
        entries: list[dict[str, Any]] = []
        total = 0
        for name, path in normalized:
            destination = staging / ARTIFACTS_DIRECTORY / PurePosixPath(name)
            digest, size = _copy_regular_file(path, destination, f"artifact {name}")
            if (digest, size) in {
                (source_hash, source_size),
                (configuration_hash, configuration_size),
            }:
                raise DossierError(f"artifact {name} matches excluded source or configuration content")
            total += size
            if total > MAX_TOTAL_ARTIFACT_BYTES:
                raise DossierError("artifact total exceeds the maximum size")
            entries.append(
                {
                    "path": name,
                    "sha256": digest,
                    "byte_length": size,
                    "media_type": "application/octet-stream",
                }
            )

        manifest: dict[str, Any] = {
            "$schema": SCHEMA_ID,
            "schema_version": SCHEMA_VERSION,
            "status": "DEVELOPMENT_ONLY",
            "scientific_claim_evidence": False,
            "source": {
                "sha256": source_hash,
                "byte_length": source_size,
                "included": False,
            },
            "software": {
                "name": "cogniprint",
                "version": software_version,
                "commit": software_commit,
            },
            "configuration": {
                "sha256": configuration_hash,
                "byte_length": configuration_size,
                "included": False,
                "basis": configuration_basis,
            },
            "artifacts": entries,
            "claim_boundary": list(CLAIM_BOUNDARY),
        }
        _validate_manifest(manifest)
        (staging / DOSSIER_FILENAME).write_bytes(_canonical_bytes(manifest))
        staging.replace(output)
        return manifest
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def verify_dossier(bundle: Path) -> dict[str, Any]:
    """Verify one dossier directory using only local files and deterministic checks."""
    bundle = Path(bundle)
    if bundle.is_symlink() or not bundle.is_dir():
        raise DossierError("bundle must be a regular directory, not a symlink")
    top_level = {entry.name for entry in bundle.iterdir()}
    if top_level != {DOSSIER_FILENAME, ARTIFACTS_DIRECTORY}:
        raise DossierError("bundle must contain exactly dossier.json and artifacts/")
    artifact_root = bundle / ARTIFACTS_DIRECTORY
    if artifact_root.is_symlink() or not artifact_root.is_dir():
        raise DossierError("artifacts must be a regular directory, not a symlink")

    manifest, raw_manifest = _load_manifest(bundle / DOSSIER_FILENAME)
    entries = _validate_manifest(manifest)
    expected_names = {entry["path"] for entry in entries}
    actual_names: set[str] = set()
    for path in artifact_root.rglob("*"):
        if path.is_symlink():
            raise DossierError(f"symlink inside artifacts is forbidden: {path}")
        if path.is_file():
            actual_names.add(path.relative_to(artifact_root).as_posix())
        elif not path.is_dir():
            raise DossierError(f"unsupported filesystem entry: {path}")
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        raise DossierError(f"artifact inventory mismatch; missing={missing}, extra={extra}")

    for entry in entries:
        path = artifact_root.joinpath(*PurePosixPath(entry["path"]).parts)
        digest, size = _hash_regular_file(path, f"artifact {entry['path']}", MAX_ARTIFACT_BYTES)
        if digest != entry["sha256"] or size != entry["byte_length"]:
            raise DossierError(f"artifact verification failed: {entry['path']}")

    return {
        "protocol": "cogniprint-evidence-dossier-verification-v1",
        "status": "VERIFIED",
        "offline": True,
        "schema": SCHEMA_ID,
        "artifact_count": len(entries),
        "dossier_sha256": hashlib.sha256(raw_manifest).hexdigest(),
    }


def _parse_artifact_specs(values: Sequence[str]) -> dict[str, Path]:
    artifacts: dict[str, Path] = {}
    for value in values:
        name, separator, raw_path = value.partition("=")
        if not separator or not name or not raw_path:
            raise DossierError("each --artifact must use NAME=PATH")
        if name in artifacts:
            raise DossierError(f"duplicate artifact path: {name}")
        artifacts[name] = Path(raw_path)
    return artifacts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m cogniprint.dossier")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser("export", help="Create a deterministic local evidence dossier.")
    export_parser.add_argument("--source", type=Path, required=True)
    export_parser.add_argument("--artifact", action="append", required=True, help="Safe relative NAME=PATH; repeatable.")
    export_parser.add_argument("--configuration", type=Path)
    export_parser.add_argument("--software-commit", required=True)
    export_parser.add_argument("--software-version", default=DEFAULT_SOFTWARE_VERSION)
    export_parser.add_argument("--output", type=Path, required=True)

    verify_parser = subparsers.add_parser("verify", help="Verify a dossier using local files only.")
    verify_parser.add_argument("--bundle", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            manifest = export_dossier(
                source=args.source,
                artifacts=_parse_artifact_specs(args.artifact),
                configuration=args.configuration,
                software_commit=args.software_commit,
                software_version=args.software_version,
                output=args.output,
            )
            print(
                _canonical_bytes(
                    {"status": "EXPORTED", "artifact_count": len(manifest["artifacts"])}
                ).decode("utf-8"),
                end="",
            )
            return 0
        report = verify_dossier(args.bundle)
        print(_canonical_bytes(report).decode("utf-8"), end="")
        return 0
    except DossierError as exc:
        print(f"DOSSIER_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
