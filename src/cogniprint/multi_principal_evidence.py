"""Pre-award Schmidt Q1 multi-principal evidence primitives.

This module is DEVELOPMENT_ONLY scaffolding for the submitted Schmidt Sciences
Q1 milestone. It does not establish that the Q1 scientific milestone has been
met, and it must not be cited as validation of cross-principal attribution.

The verifier is deliberately dependency-free and fail-closed. It validates a
small, explicit evidence-bundle contract, checks deterministic integrity hashes,
and reconstructs declared delegation edges from synthetic fixtures.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any


SCHEMA_VERSION = "cogniprint-multi-principal-evidence-v0.1"
ALLOWED_EVIDENCE_CLASSES = {"OBSERVED", "ATTESTED", "INFERRED", "UNKNOWN"}
ALLOWED_EVENT_TYPES = {
    "DELEGATION",
    "ACTION",
    "TOOL_CALL",
    "MESSAGE",
    "AUTHORIZATION_CHANGE",
    "REVOCATION",
    "CLONE",
    "FORK",
    "UPDATE",
}
REQUIRED_EVENT_FIELDS = {
    "event_id",
    "sequence",
    "timestamp",
    "principal_id",
    "agent_id",
    "event_type",
    "evidence_class",
    "parent_event_ids",
    "authorization_scope",
    "payload_commitment_sha256",
    "integrity_sha256",
}


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def event_integrity_sha256(event: dict[str, Any]) -> str:
    """Return the deterministic hash of an event excluding its integrity field."""

    body = {key: value for key, value in event.items() if key != "integrity_sha256"}
    return _sha256(body)


def with_event_integrity(event: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of *event* carrying its deterministic integrity hash."""

    result = deepcopy(event)
    result["integrity_sha256"] = event_integrity_sha256(result)
    return result


def bundle_integrity_sha256(bundle: dict[str, Any]) -> str:
    body = {key: value for key, value in bundle.items() if key != "bundle_integrity_sha256"}
    return _sha256(body)


def with_bundle_integrity(bundle: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(bundle)
    result["bundle_integrity_sha256"] = bundle_integrity_sha256(result)
    return result


def _is_sha256(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def verify_multi_principal_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Fail-closed validation for a synthetic/pre-award multi-principal bundle."""

    if not isinstance(bundle, dict):
        return {"ok": False, "reason": "bundle must be an object"}
    if bundle.get("schema") != SCHEMA_VERSION:
        return {"ok": False, "reason": "unexpected schema"}
    if bundle.get("research_status") != "DEVELOPMENT_ONLY_PREAWARD":
        return {"ok": False, "reason": "research_status must remain DEVELOPMENT_ONLY_PREAWARD"}

    principals = bundle.get("principals")
    if not isinstance(principals, list) or not 3 <= len(principals) <= 6:
        return {"ok": False, "reason": "fixtures must contain 3 to 6 principals"}

    principal_ids: set[str] = set()
    for principal in principals:
        if not isinstance(principal, dict):
            return {"ok": False, "reason": "principal entry must be an object"}
        principal_id = principal.get("principal_id")
        if not isinstance(principal_id, str) or not principal_id:
            return {"ok": False, "reason": "invalid principal_id"}
        if principal_id in principal_ids:
            return {"ok": False, "reason": "duplicate principal_id", "principal_id": principal_id}
        principal_ids.add(principal_id)

    events = bundle.get("events")
    if not isinstance(events, list) or not events:
        return {"ok": False, "reason": "events must be a non-empty list"}

    event_ids: set[str] = set()
    sequences: set[int] = set()
    for event in events:
        if not isinstance(event, dict):
            return {"ok": False, "reason": "event must be an object"}
        missing = sorted(REQUIRED_EVENT_FIELDS - set(event))
        if missing:
            return {"ok": False, "reason": "missing required event fields", "missing": missing}

        event_id = event["event_id"]
        if not isinstance(event_id, str) or not event_id:
            return {"ok": False, "reason": "invalid event_id"}
        if event_id in event_ids:
            return {"ok": False, "reason": "duplicate event_id", "event_id": event_id}
        event_ids.add(event_id)

        sequence = event["sequence"]
        if not isinstance(sequence, int) or sequence < 0 or sequence in sequences:
            return {"ok": False, "reason": "invalid or duplicate sequence", "event_id": event_id}
        sequences.add(sequence)

        if event["principal_id"] not in principal_ids:
            return {"ok": False, "reason": "unknown principal", "event_id": event_id}
        if event["event_type"] not in ALLOWED_EVENT_TYPES:
            return {"ok": False, "reason": "unsupported event_type", "event_id": event_id}
        if event["evidence_class"] not in ALLOWED_EVIDENCE_CLASSES:
            return {"ok": False, "reason": "unsupported evidence_class", "event_id": event_id}
        if not isinstance(event["parent_event_ids"], list):
            return {"ok": False, "reason": "parent_event_ids must be a list", "event_id": event_id}
        if not isinstance(event["authorization_scope"], list):
            return {"ok": False, "reason": "authorization_scope must be a list", "event_id": event_id}
        if not _is_sha256(event["payload_commitment_sha256"]):
            return {"ok": False, "reason": "invalid payload commitment", "event_id": event_id}
        if event_integrity_sha256(event) != event["integrity_sha256"]:
            return {"ok": False, "reason": "event integrity mismatch", "event_id": event_id}

        if event["event_type"] == "DELEGATION":
            target = event.get("target_principal_id")
            if target not in principal_ids or target == event["principal_id"]:
                return {"ok": False, "reason": "invalid delegation target", "event_id": event_id}

    for event in events:
        for parent in event["parent_event_ids"]:
            if parent not in event_ids:
                return {"ok": False, "reason": "unknown parent event", "event_id": event["event_id"], "parent": parent}

    claimed_bundle_hash = bundle.get("bundle_integrity_sha256")
    if not _is_sha256(claimed_bundle_hash):
        return {"ok": False, "reason": "invalid bundle integrity hash"}
    if bundle_integrity_sha256(bundle) != claimed_bundle_hash:
        return {"ok": False, "reason": "bundle integrity mismatch"}

    return {
        "ok": True,
        "schema": SCHEMA_VERSION,
        "principal_count": len(principal_ids),
        "event_count": len(events),
        "delegation_edges": reconstruct_delegation_edges(bundle),
        "research_status": "DEVELOPMENT_ONLY_PREAWARD",
    }


def reconstruct_delegation_edges(bundle: dict[str, Any]) -> list[list[str]]:
    """Return declared principal-to-principal delegation edges in sequence order."""

    events = sorted(bundle.get("events", []), key=lambda event: event.get("sequence", -1))
    edges: list[list[str]] = []
    for event in events:
        if event.get("event_type") == "DELEGATION":
            edges.append([event["principal_id"], event["target_principal_id"]])
    return edges


def structural_field_ablation(bundle: dict[str, Any]) -> dict[str, bool]:
    """Development-only structural ablation, not a scientific Q1 result.

    Each required event field is deleted once from the first event. ``True``
    means the verifier correctly rejects the malformed bundle.
    """

    outcomes: dict[str, bool] = {}
    for field in sorted(REQUIRED_EVENT_FIELDS):
        candidate = deepcopy(bundle)
        candidate["events"][0].pop(field, None)
        candidate = with_bundle_integrity(candidate)
        outcomes[field] = not verify_multi_principal_bundle(candidate)["ok"]
    return outcomes
