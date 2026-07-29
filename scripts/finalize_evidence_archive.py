#!/usr/bin/env python3
"""Finalize an evidence TAR.GZ with a detached authoritative SHA-256 sidecar.

An archive cannot stably contain its own final SHA-256 because changing the
embedded value changes the archive bytes. This tool removes stale self-hash
claims from the bundle, records an explicit detached-hash policy, rebuilds the
internal evidence manifest, creates a deterministic TAR.GZ, and writes the
archive hash beside it as ``<archive>.sha256``.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


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


def safe_members(archive: Path) -> list[tarfile.TarInfo]:
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
    for member in members:
        path = PurePosixPath(member.name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"unsafe archive path: {member.name}")
        if member.issym() or member.islnk():
            raise ValueError(f"archive links are not permitted: {member.name}")
        if not (member.isdir() or member.isfile()):
            raise ValueError(f"unsupported archive member: {member.name}")
    return members


def safe_extract(archive: Path, destination: Path) -> Path:
    members = safe_members(archive)
    with tarfile.open(archive, "r:gz") as handle:
        for member in members:
            target = destination / member.name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            extracted = handle.extractfile(member)
            if extracted is None:
                raise ValueError(f"failed to extract {member.name}")
            with target.open("wb") as output:
                for chunk in iter(lambda: extracted.read(1024 * 1024), b""):
                    output.write(chunk)
    roots = sorted(path for path in destination.iterdir() if path.is_dir())
    if len(roots) != 1:
        raise ValueError(f"expected one evidence root, found {len(roots)}")
    return roots[0]


def rebuild_manifest(root: Path) -> int:
    manifest = root / "EVIDENCE_SHA256SUMS.txt"
    files = sorted(
        path for path in root.rglob("*") if path.is_file() and path != manifest
    )
    manifest.write_text(
        "".join(
            f"{sha256_file(path)}  {path.relative_to(root).as_posix()}\n"
            for path in files
        ),
        encoding="utf-8",
    )
    return len(files)


def verify_manifest(root: Path) -> int:
    manifest = root / "EVIDENCE_SHA256SUMS.txt"
    checked = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        actual = sha256_file(root / relative)
        if actual != expected:
            raise AssertionError(f"manifest mismatch for {relative}")
        checked += 1
    return checked


def build_deterministic_archive(root: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w") as handle:
                paths = [root, *sorted(root.rglob("*"), key=lambda item: item.as_posix())]
                for path in paths:
                    arcname = (
                        root.name
                        if path == root
                        else f"{root.name}/{path.relative_to(root).as_posix()}"
                    )
                    info = handle.gettarinfo(str(path), arcname=arcname)
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    info.mtime = 0
                    if path.is_file():
                        with path.open("rb") as source:
                            handle.addfile(info, source)
                    else:
                        handle.addfile(info)


def update_bundle_metadata(
    root: Path,
    *,
    input_archive: Path,
    output_archive: Path,
    input_sha256: str,
) -> str | None:
    status_json = root / "FINAL_LOCAL_STATUS_003.json"
    stale_hash: str | None = None
    if status_json.is_file():
        payload = json.loads(status_json.read_text(encoding="utf-8"))
        stale = payload.pop("archive_sha256", None)
        stale_hash = str(stale) if stale is not None else None
        payload.update(
            {
                "archive_name": output_archive.name,
                "archive_sha256_embedded": False,
                "archive_sha256_policy": "DETACHED_EXTERNAL_SIDECAR",
                "archive_sha256_sidecar_name": f"{output_archive.name}.sha256",
                "packaging_correction": {
                    "schema": "cogniprint-evidence-packaging-correction-001",
                    "corrected_from_archive": input_archive.name,
                    "corrected_from_archive_sha256": input_sha256,
                    "stale_internal_archive_sha256_removed": stale_hash,
                    "scientific_metrics_changed": False,
                    "reason": (
                        "An archive cannot stably embed its own final SHA-256 "
                        "because changing the embedded value changes the archive bytes."
                    ),
                },
            }
        )
        write_json(status_json, payload)

    policy = {
        "schema": "cogniprint-archive-hash-policy-001",
        "status": "PASS",
        "policy": "DETACHED_EXTERNAL_SHA256_SIDECAR",
        "self_hash_embedded": False,
        "corrected_from_archive": input_archive.name,
        "corrected_from_archive_sha256": input_sha256,
        "stale_internal_archive_sha256_removed": stale_hash,
        "output_archive": output_archive.name,
        "sidecar": f"{output_archive.name}.sha256",
        "scientific_metrics_changed": False,
        "scientific_boundary": (
            "descriptive_only / PROOF_MODE / PRE-FREEZE / "
            "Stage B NOT_AUTHORISED_TO_START"
        ),
        "reason": (
            "The final archive SHA-256 is recorded outside the archive to avoid "
            "a self-referential hash."
        ),
    }
    write_json(root / "ARCHIVE_HASH_POLICY_001.json", policy)

    status_markdown = root / "FINAL_STATUS.md"
    if status_markdown.is_file():
        text = status_markdown.read_text(encoding="utf-8")
        text = re.sub(
            r"Final evidence archive: `[^`]+`",
            f"Final evidence archive: `{output_archive.name}`",
            text,
        )
        replacement = (
            "Final evidence archive SHA-256: stored in detached sidecar "
            f"`{output_archive.name}.sha256`; not embedded to avoid self-reference."
        )
        text = re.sub(
            r"Final evidence archive SHA-256: `[^`]+`",
            replacement,
            text,
        )
        if "## Packaging correction" not in text:
            text += (
                "\n## Packaging correction\n\n"
                "The archive hash is authoritative only in the detached `.sha256` "
                "sidecar. Scientific metrics and source/split evidence were not "
                "changed by this packaging correction.\n"
            )
        status_markdown.write_text(text, encoding="utf-8")
    return stale_hash


def finalize(input_archive: Path, output_archive: Path) -> dict[str, Any]:
    input_archive = input_archive.resolve()
    output_archive = output_archive.resolve()
    input_sha256 = sha256_file(input_archive)
    with tempfile.TemporaryDirectory(prefix="cogniprint-evidence-finalize-") as tmp:
        root = safe_extract(input_archive, Path(tmp))
        stale_hash = update_bundle_metadata(
            root,
            input_archive=input_archive,
            output_archive=output_archive,
            input_sha256=input_sha256,
        )
        manifest_files = rebuild_manifest(root)
        if verify_manifest(root) != manifest_files:
            raise AssertionError("manifest verification count mismatch")
        build_deterministic_archive(root, output_archive)

    safe_members(output_archive)
    output_sha256 = sha256_file(output_archive)
    sidecar = Path(f"{output_archive}.sha256")
    sidecar.write_text(
        f"{output_sha256}  {output_archive.name}\n",
        encoding="utf-8",
    )
    with tempfile.TemporaryDirectory(prefix="cogniprint-evidence-verify-") as tmp:
        verified_root = safe_extract(output_archive, Path(tmp))
        verified_files = verify_manifest(verified_root)
        if verified_files != manifest_files:
            raise AssertionError("final manifest file count mismatch")
    return {
        "status": "PASS",
        "input_archive": str(input_archive),
        "input_archive_sha256": input_sha256,
        "stale_internal_archive_sha256_removed": stale_hash,
        "output_archive": str(output_archive),
        "output_archive_sha256": output_sha256,
        "sidecar": str(sidecar),
        "manifest_file_count": manifest_files,
        "scientific_metrics_changed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-archive", type=Path, required=True)
    parser.add_argument("--output-archive", type=Path, required=True)
    args = parser.parse_args()
    result = finalize(args.input_archive, args.output_archive)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
