"""Privacy-preserving XRPL evidence commitment prototype.

This module is deliberately network-free. It creates and verifies the compact
commitment payload that a later transport layer can place in an XRPL
transaction memo. It does not sign, submit, or claim validation of any ledger
transaction.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping

ANCHOR_SCHEMA = "cogniprint-xrpl-anchor-v0.1"
COMMITMENT_ALGORITHM = "sha256"
ARTIFACT_TYPE = "cogniprint-evidence-manifest"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class AnchorError(ValueError):
    """Raised when an anchor payload cannot be constructed safely."""


def canonical_json_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for JSON-compatible input.

    NaN and Infinity are rejected because they are not valid interoperable JSON
    values and would undermine cross-implementation determinism.
    """

    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise AnchorError("manifest is not canonical JSON data") from exc
    return encoded.encode("utf-8")


def manifest_commitment(manifest: Mapping[str, Any]) -> str:
    """Compute a SHA-256 commitment for a public-safe evidence manifest."""

    if not isinstance(manifest, Mapping):
        raise AnchorError("manifest must be a mapping")
    return hashlib.sha256(canonical_json_bytes(dict(manifest))).hexdigest()


def build_anchor_payload(
    manifest: Mapping[str, Any],
    *,
    artifact_schema: str,
) -> dict[str, str]:
    """Build the compact public payload intended for an XRPL memo."""

    if not isinstance(artifact_schema, str) or not artifact_schema.strip():
        raise AnchorError("artifact_schema must be a non-empty string")

    return {
        "schema": ANCHOR_SCHEMA,
        "commitment_alg": COMMITMENT_ALGORITHM,
        "manifest_commitment": manifest_commitment(manifest),
        "artifact_type": ARTIFACT_TYPE,
        "artifact_schema": artifact_schema.strip(),
    }


def verify_anchor_payload(
    manifest: Mapping[str, Any],
    payload: Mapping[str, Any],
) -> bool:
    """Fail closed unless the payload is supported and the commitment matches."""

    if not isinstance(payload, Mapping):
        return False
    if payload.get("schema") != ANCHOR_SCHEMA:
        return False
    if payload.get("commitment_alg") != COMMITMENT_ALGORITHM:
        return False
    if payload.get("artifact_type") != ARTIFACT_TYPE:
        return False

    artifact_schema = payload.get("artifact_schema")
    if not isinstance(artifact_schema, str) or not artifact_schema.strip():
        return False

    claimed = payload.get("manifest_commitment")
    if not isinstance(claimed, str) or _SHA256_RE.fullmatch(claimed) is None:
        return False

    try:
        expected = manifest_commitment(manifest)
    except AnchorError:
        return False
    return claimed == expected


def encode_memo_data(payload: Mapping[str, Any]) -> str:
    """Encode a validated anchor payload as uppercase hex UTF-8 JSON.

    This is transport preparation only. It does not submit a transaction.
    """

    required = {
        "schema",
        "commitment_alg",
        "manifest_commitment",
        "artifact_type",
        "artifact_schema",
    }
    if set(payload) != required:
        raise AnchorError("anchor payload fields do not match v0.1 schema")
    if payload.get("schema") != ANCHOR_SCHEMA:
        raise AnchorError("unsupported anchor schema")
    if payload.get("commitment_alg") != COMMITMENT_ALGORITHM:
        raise AnchorError("unsupported commitment algorithm")
    if payload.get("artifact_type") != ARTIFACT_TYPE:
        raise AnchorError("unsupported artifact type")

    commitment = payload.get("manifest_commitment")
    if not isinstance(commitment, str) or _SHA256_RE.fullmatch(commitment) is None:
        raise AnchorError("invalid manifest commitment")

    artifact_schema = payload.get("artifact_schema")
    if not isinstance(artifact_schema, str) or not artifact_schema.strip():
        raise AnchorError("invalid artifact schema")

    return canonical_json_bytes(dict(payload)).hex().upper()
