#!/usr/bin/env python3
"""Fail-closed validation for the Challenge 001 preregistration/custody HOLD package."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PREREG_PATH = Path(
    "challenge-001/preregistration/"
    "PREREGISTRATION_SUBMISSION_MANIFEST_001.template.json"
)
CUSTODY_PATH = Path(
    "challenge-001/custody/STAGE_B_CUSTODY_RECORD_001.template.json"
)
PREREG_SCHEMA_PATH = Path(
    "schemas/challenge-001-preregistration-submission-manifest-v1.schema.json"
)
CUSTODY_SCHEMA_PATH = Path(
    "schemas/challenge-001-stage-b-custody-record-v1.schema.json"
)
PUBLIC_RELEASE_PATH = Path("config/public-release.json")
FREEZE_PATH = Path("RESEARCH_FREEZE_001.md")
PLAN_PATH = Path("docs/stage-b-preregistration-custody-plan-002.md")
VALIDATOR_PATH = Path("scripts/check_stage_b_preregistration_package.py")

DECISION_KEYS = {
    "hypotheses_frozen",
    "non_hypotheses_frozen",
    "source_families_frozen",
    "held_out_unknown_policy_frozen",
    "human_control_frozen",
    "collection_window_frozen",
    "sample_counts_and_strata_frozen",
    "lineage_and_split_rules_frozen",
    "minimum_evidence_policy_frozen",
    "ood_unknown_method_frozen",
    "calibration_method_frozen",
    "baseline_implementations_frozen",
    "metric_semantics_frozen",
    "exclusion_rules_frozen",
    "stop_and_claim_narrowing_rules_frozen",
    "custody_and_reveal_procedure_frozen",
}
FORBIDDEN_EXACT_KEYS = {
    "true_class",
    "known_to_reference",
    "model_family",
    "source_family",
    "generator",
    "sample_id",
    "sample_ids",
    "raw_text",
    "prompt",
    "api_key",
    "access_token",
    "password",
    "private_key",
    "secret",
}


class ValidationError(ValueError):
    """Raised when the preregistration/custody package violates a HOLD guard."""


def load_json(root: Path, relative: Path) -> dict[str, Any]:
    path = root / relative
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing required file: {relative}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {relative}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValidationError(f"{relative} must contain a JSON object")
    return payload


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def walk_keys(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            require(
                key not in FORBIDDEN_EXACT_KEYS,
                f"forbidden predictor/secret field at {path}.{key}",
            )
            walk_keys(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            walk_keys(nested, f"{path}[{index}]")


def validate_schema_shape(schema: dict[str, Any], expected_id_suffix: str) -> None:
    require(
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
        "schema must declare JSON Schema draft 2020-12",
    )
    require(
        str(schema.get("$id", "")).endswith(expected_id_suffix),
        f"unexpected schema $id for {expected_id_suffix}",
    )
    require(schema.get("type") == "object", "schema root must be object")
    require(
        schema.get("additionalProperties") is False,
        "schema root must fail closed on additional properties",
    )
    require(isinstance(schema.get("allOf"), list), "schema transition rules missing")


def validate_prereg_template(payload: dict[str, Any]) -> None:
    require(
        payload.get("schema")
        == "cogniprint-preregistration-submission-manifest-001",
        "unexpected preregistration schema identifier",
    )
    require(payload.get("record_mode") == "TEMPLATE", "prereg record_mode must be TEMPLATE")
    require(payload.get("status") == "HOLD", "prereg template must remain HOLD")
    state = payload.get("scientific_state", {})
    require(state.get("readiness") == "descriptive_only", "readiness expanded")
    require(state.get("research_mode") == "PROOF_MODE", "research mode changed")
    require(state.get("research_freeze") == "PRE-FREEZE", "template falsely frozen")
    require(
        state.get("stage_b_status") == "NOT_AUTHORISED_TO_START",
        "template falsely authorises Stage B",
    )
    require(state.get("scientific_claim_evidence") is False, "claim evidence falsely enabled")

    registration = payload.get("registration", {})
    for field in (
        "registration_id",
        "canonical_url",
        "submitted_at_utc",
        "accepted_at_utc",
        "public_doi",
    ):
        require(registration.get(field) is None, f"template has fake registration field: {field}")
    require(registration.get("visibility") == "UNDECIDED", "visibility prematurely selected")
    require(registration.get("contributors_verified") is False, "contributors falsely verified")
    require(registration.get("license_verified") is False, "license falsely verified")

    repository = payload.get("repository", {})
    for field in (
        "commit_sha",
        "tree_sha",
        "dirty_status",
        "evaluator_commit_sha",
        "environment_lock_sha256",
    ):
        require(repository.get(field) is None, f"template has fake repository value: {field}")

    controls = payload.get("frozen_controls", {})
    require(controls.get("research_freeze_status") == "PRE-FREEZE", "freeze status mismatch")
    require(controls.get("research_lock_status") == "NOT_CREATED", "fake Research Lock")
    for key, value in controls.items():
        if key.endswith("_sha256"):
            require(value is None, f"template has fake frozen hash: {key}")

    decisions = payload.get("scientific_decisions", {})
    require(set(decisions) == DECISION_KEYS, "scientific decision key set drifted")
    require(all(value is False for value in decisions.values()), "decision falsely frozen")

    gates = payload.get("execution_gates", {})
    require(gates.get("runner_gate_issue") == 30, "runner issue changed")
    require(gates.get("runner_gate_status") == "NOT_EXECUTED", "runner falsely executed")
    require(gates.get("real_stage_a_b_leakage_audit_status") == "NOT_EXECUTED", "fake leakage PASS")
    require(gates.get("sample_id_overlap") is None, "fake sample overlap result")
    require(gates.get("content_hash_overlap") is None, "fake content overlap result")
    require(gates.get("sealed_predictions_exist") is False, "sealed predictions already exist")
    require(gates.get("sealed_labels_revealed") is False, "sealed labels already revealed")
    require(gates.get("stage_b_execution_authorised") is False, "Stage B falsely authorised")

    privacy = payload.get("privacy_and_custody", {})
    require(privacy.get("prediction_process_has_label_access") is False, "label access enabled")
    require(privacy.get("whole_label_artifact_hash_policy") == "TO_BE_FROZEN", "hash policy prematurely frozen")
    require(privacy.get("custodian_role_assigned") is False, "fake custodian assignment")
    require(privacy.get("prediction_role_assigned") is False, "fake prediction role assignment")
    require(privacy.get("independent_review_role_assigned") is False, "fake review role assignment")

    require(payload.get("created_as_template") is True, "template marker missing")
    require(payload.get("stage_b_data_created") is False, "template claims Stage B data")
    require(bool(payload.get("hold_reasons")), "HOLD template needs explicit blockers")
    walk_keys(payload)


def validate_custody_template(payload: dict[str, Any]) -> None:
    require(
        payload.get("schema") == "cogniprint-stage-b-custody-record-001",
        "unexpected custody schema identifier",
    )
    require(payload.get("record_mode") == "TEMPLATE", "custody record_mode must be TEMPLATE")
    require(payload.get("status") == "HOLD", "custody template must remain HOLD")
    state = payload.get("scientific_state", {})
    require(state.get("research_freeze") == "PRE-FREEZE", "custody template falsely frozen")
    require(
        state.get("stage_b_status") == "NOT_AUTHORISED_TO_START",
        "custody template falsely authorises Stage B",
    )

    roles = payload.get("roles", {})
    for field in (
        "protocol_owner_role_id",
        "corpus_label_custodian_role_id",
        "prediction_operator_role_id",
        "independent_evaluator_role_id",
    ):
        require(roles.get(field) is None, f"template has fake role ID: {field}")
    require(roles.get("technical_separation_documented") is False, "fake separation record")

    boundary = payload.get("storage_boundary", {})
    require(boundary.get("blinded_package_location_id") is None, "fake blinded location")
    require(boundary.get("sealed_label_location_id") is None, "fake sealed location")
    require(boundary.get("locations_logically_separate") is False, "fake storage separation")
    require(boundary.get("sealed_location_not_mounted_to_prediction_process") is True, "mount guard weakened")
    require(boundary.get("sealed_location_not_committed_to_public_repository") is True, "repository guard weakened")
    require(boundary.get("sealed_location_not_in_predictor_visible_ci_artifacts") is True, "CI guard weakened")
    require(boundary.get("secret_paths_credentials_or_keys_recorded_here") is False, "secret field enabled")

    for key, value in payload.get("artifacts", {}).items():
        require(value is None, f"template has fake artifact hash: {key}")
    for key, value in payload.get("events", {}).items():
        require(value is None, f"template has fake event timestamp: {key}")

    eligibility = payload.get("eligibility", {})
    require(eligibility.get("stage_a_b_leakage_audit_status") == "NOT_EXECUTED", "fake leakage status")
    require(eligibility.get("sample_id_overlap") is None, "fake sample overlap")
    require(eligibility.get("content_hash_overlap") is None, "fake content overlap")

    reveal = payload.get("reveal_gate", {})
    require(reveal.get("predictions_exist") is False, "template claims predictions")
    require(reveal.get("prediction_freeze_receipt_verified") is False, "fake receipt verification")
    require(reveal.get("reveal_authorised") is False, "template authorises reveal")
    require(reveal.get("sealed_label_bytes_unchanged") is None, "fake label-byte check")

    safety = payload.get("safety_guards", {})
    require(safety.get("contains_real_stage_b_sample_ids") is False, "real sample IDs in template")
    require(safety.get("contains_real_labels") is False, "real labels in template")
    require(safety.get("contains_secret_locations") is False, "secret locations in template")
    require(safety.get("contains_access_credentials") is False, "credentials in template")
    require(safety.get("stage_b_artifacts_created") is False, "template claims Stage B artifacts")
    walk_keys(payload)


def validate_public_release(root: Path) -> None:
    config = load_json(root, PUBLIC_RELEASE_PATH)
    include = config.get("include")
    require(isinstance(include, list), "public release include must be a list")
    for required in (str(PLAN_PATH), str(VALIDATOR_PATH)):
        require(required in include, f"sanitized release omits {required}")
    require("challenge-001/**" in include, "sanitized release omits challenge-001 templates")
    require("schemas/**" in include, "sanitized release omits schemas")
    require("tests/**" in include, "sanitized release omits tests")


def validate_package(root: Path) -> dict[str, Any]:
    prereg = load_json(root, PREREG_PATH)
    custody = load_json(root, CUSTODY_PATH)
    prereg_schema = load_json(root, PREREG_SCHEMA_PATH)
    custody_schema = load_json(root, CUSTODY_SCHEMA_PATH)

    validate_schema_shape(
        prereg_schema,
        "schemas/challenge-001-preregistration-submission-manifest-v1.schema.json",
    )
    validate_schema_shape(
        custody_schema,
        "schemas/challenge-001-stage-b-custody-record-v1.schema.json",
    )
    validate_prereg_template(prereg)
    validate_custody_template(custody)
    validate_public_release(root)

    freeze_text = (root / FREEZE_PATH).read_text(encoding="utf-8")
    require("PRE-FREEZE" in freeze_text, "RESEARCH_FREEZE_001.md no longer records PRE-FREEZE")
    plan_text = (root / PLAN_PATH).read_text(encoding="utf-8")
    require("STAGE B NOT AUTHORISED" in plan_text, "custody plan boundary missing")

    return {
        "status": "PASS",
        "package_status": "HOLD",
        "research_freeze": "PRE-FREEZE",
        "stage_b_status": "NOT_AUTHORISED_TO_START",
        "external_registration": "NOT_SUBMITTED",
        "runner_gate": "NOT_EXECUTED",
        "templates_validated": 2,
        "schemas_parsed": 2,
        "sanitized_release_guard": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = validate_package(args.root.resolve())
    except (OSError, ValidationError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
