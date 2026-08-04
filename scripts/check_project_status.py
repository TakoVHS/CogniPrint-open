#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

STATUS = Path("docs/evidence-project-status.json")
REVIEW = Path("docs/external-review/status.json")
FIXED = {
    "scientific_readiness": "descriptive_only",
    "research_mode": "PROOF_MODE",
    "canonical_freeze": "PRE-FREEZE",
    "stage_b": "NOT_AUTHORISED_TO_START",
    "github_actions": "NOT_EXECUTED",
    "main_exact_snapshot": "NOT_EXECUTED",
}


class StatusError(RuntimeError):
    pass


def _reject_constant(token: str) -> None:
    raise StatusError(f"non-finite JSON number: {token}")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise StatusError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StatusError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise StatusError(f"{path} root must be an object")
    return value


def exact(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        actual = set(value) if isinstance(value, dict) else set()
        raise StatusError(
            f"{label} keys mismatch; missing={sorted(keys - actual)}, extra={sorted(actual - keys)}"
        )
    return value


def validate(status: dict[str, Any]) -> None:
    exact(
        status,
        {"schema", "status_date", "canonical", "development_evidence", "policy"},
        "status",
    )
    if status["schema"] != "cogniprint-project-status-v1":
        raise StatusError("unknown project status schema")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(status["status_date"])):
        raise StatusError("status_date must use YYYY-MM-DD")
    canonical = exact(
        status["canonical"],
        {
            "repository",
            "main_commit",
            "release",
            *FIXED,
            "external_methodological_reviews",
            "doi",
        },
        "canonical",
    )
    if canonical["repository"] != "TakoVHS/CogniPrint-open":
        raise StatusError("canonical repository is invalid")
    if not re.fullmatch(r"[0-9a-f]{40}", str(canonical["main_commit"])):
        raise StatusError("canonical main commit is invalid")
    for key, expected in FIXED.items():
        if canonical[key] != expected:
            raise StatusError(f"unauthorized status escalation: {key}={canonical[key]!r}")
    if canonical["external_methodological_reviews"] != {"valid": 0, "required": 1}:
        raise StatusError("external methodological review gate mismatch")
    if canonical["doi"] != {
        "reference": "10.5281/zenodo.20756421",
        "verification": "PENDING_DIRECT_PUBLIC_VERIFICATION",
    }:
        raise StatusError("DOI status mismatch")
    if not isinstance(status["development_evidence"], list):
        raise StatusError("development_evidence must be a list")
    for item in status["development_evidence"]:
        exact(
            item,
            {
                "pull_request",
                "head",
                "tree",
                "state",
                "canonical_capability_change",
                "evidence",
            },
            "development evidence",
        )
        if item["state"] != "DRAFT" or item["canonical_capability_change"] is not False:
            raise StatusError("development evidence must remain Draft and non-canonical")
        if not all(re.fullmatch(r"[0-9a-f]{40}", str(item[key])) for key in ("head", "tree")):
            raise StatusError("development evidence SHA is invalid")
    if status["policy"] != {
        "branch_evidence_changes_main_status": False,
        "not_executed_is_failure": False,
        "product_progress_unlocks_scientific_claims": False,
    }:
        raise StatusError("status policy must remain fail-closed")


def document_errors(root: Path, status: dict[str, Any]) -> list[str]:
    canonical = status["canonical"]
    release = canonical["release"]
    reviews = canonical["external_methodological_reviews"]
    surfaces = {
        "README.md": [
            "descriptive_only",
            f"v{release}",
            "pending direct public Zenodo verification",
        ],
        "docs/current-state-summary.md": [
            "Scientific readiness: `descriptive_only`",
            "Research mode: `PROOF_MODE`",
            "Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`",
            "CI evidence status: `NOT_EXECUTED`",
            f"Release line: `v{release}`",
            "DOI: pending direct public Zenodo verification",
        ],
        "docs/trust.md": [
            "Current scientific readiness: `descriptive_only`",
            "Research mode: `PROOF_MODE`",
            "Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`",
            "`NOT_EXECUTED`",
        ],
        "docs/external-review.md": [
            "Scientific readiness: `descriptive_only`",
            f"External methodological reviews: `{reviews['valid']}/{reviews['required']}`",
            f"Release line: `v{release}`",
        ],
        "CITATION.cff": [f'version: "{release}"', "descriptive_only"],
        "pyproject.toml": [f'version = "{release}"'],
        "RESEARCH_FREEZE_001.md": ["PRE-FREEZE", "NOT AUTHORISED TO START"],
    }
    errors: list[str] = []
    for relative, tokens in surfaces.items():
        path = root / relative
        if not path.exists():
            errors.append(f"missing status surface: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(f"{relative}: missing {token!r}" for token in tokens if token not in text)
    expected_review = {
        "schema": "cogniprint-external-review-status-v1",
        "status_date": status["status_date"],
        "valid_review_count": reviews["valid"],
        "minimum_required_valid_reviews": reviews["required"],
        "independent_external_review_present": False,
        "qualifying_evidence": [],
    }
    if load(root / REVIEW) != expected_review:
        errors.append("external review status does not match project status")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args(argv).root.resolve()
    try:
        status = load(root / STATUS)
        validate(status)
        errors = document_errors(root, status)
    except StatusError as exc:
        print(f"PROJECT_STATUS_ERROR: {exc}")
        return 1
    if errors:
        print("Project status consistency check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PROJECT_STATUS_CONSISTENCY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
