"""Deterministic case manifest hashing for future .cogcase bundles.

This module provides integrity/chain-of-custody primitives only.  It does not
implement a digital signature and must not be described as a signed case format
until a reviewed signing implementation is added.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CASE_MANIFEST_SCHEMA = "cogniprint-case-manifest-v0.1"
EXCLUDED_TOP_LEVEL = {"MANIFEST.json", "SIGNATURES"}


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _iter_case_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] in EXCLUDED_TOP_LEVEL:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def build_case_manifest(root: str | Path, *, case_id: str) -> dict[str, object]:
    base = Path(root).resolve()
    if not base.is_dir():
        raise ValueError("case root must be an existing directory")
    case_id = str(case_id).strip()
    if not case_id or len(case_id) > 128:
        raise ValueError("case_id must be a non-empty string up to 128 characters")

    entries: list[dict[str, object]] = []
    for path in _iter_case_files(base):
        rel = path.relative_to(base).as_posix()
        data = path.read_bytes()
        entries.append(
            {
                "path": rel,
                "sha256": _sha256_bytes(data),
                "size_bytes": len(data),
            }
        )

    body = {
        "schema": CASE_MANIFEST_SCHEMA,
        "case_id": case_id,
        "files": entries,
        "signature_status": "UNSIGNED",
    }
    return {
        **body,
        "manifest_sha256": _sha256_bytes(_canonical_json(body)),
    }


def verify_case_manifest(root: str | Path, manifest: dict[str, object]) -> dict[str, object]:
    base = Path(root).resolve()
    if manifest.get("schema") != CASE_MANIFEST_SCHEMA:
        return {"ok": False, "reason": "unexpected schema"}

    claimed_hash = str(manifest.get("manifest_sha256", ""))
    body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    computed_hash = _sha256_bytes(_canonical_json(body))
    if computed_hash != claimed_hash:
        return {
            "ok": False,
            "reason": "manifest_sha256 mismatch",
            "claimed": claimed_hash,
            "computed": computed_hash,
        }

    expected_files = manifest.get("files")
    if not isinstance(expected_files, list):
        return {"ok": False, "reason": "files must be a list"}

    expected_by_path: dict[str, dict[str, object]] = {}
    for entry in expected_files:
        if not isinstance(entry, dict):
            return {"ok": False, "reason": "invalid file entry"}
        path_value = entry.get("path")
        if not isinstance(path_value, str) or not path_value:
            return {"ok": False, "reason": "invalid file path"}
        if path_value.startswith("/") or ".." in Path(path_value).parts:
            return {"ok": False, "reason": "unsafe file path"}
        expected_by_path[path_value] = entry

    actual_paths = {
        path.relative_to(base).as_posix(): path
        for path in _iter_case_files(base)
    }

    if set(actual_paths) != set(expected_by_path):
        return {
            "ok": False,
            "reason": "case file set mismatch",
            "missing": sorted(set(expected_by_path) - set(actual_paths)),
            "unexpected": sorted(set(actual_paths) - set(expected_by_path)),
        }

    for rel, path in actual_paths.items():
        data = path.read_bytes()
        entry = expected_by_path[rel]
        if _sha256_bytes(data) != entry.get("sha256"):
            return {"ok": False, "reason": "file hash mismatch", "path": rel}
        if len(data) != entry.get("size_bytes"):
            return {"ok": False, "reason": "file size mismatch", "path": rel}

    return {
        "ok": True,
        "manifest_sha256": computed_hash,
        "signature_status": manifest.get("signature_status", "UNSIGNED"),
    }
