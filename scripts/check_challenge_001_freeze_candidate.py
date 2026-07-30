#!/usr/bin/env python3
"""Fail-closed checks for the non-canonical Challenge 001 freeze candidate."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "challenge-001/protocol/frozen/NUMERICAL_FREEZE_DECISIONS_001.candidate.json"
CANDIDATE = ROOT / "challenge-001/protocol/frozen/RESEARCH_FREEZE_001.candidate.md"
CANONICAL = ROOT / "RESEARCH_FREEZE_001.md"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def load_decisions(path: Path = DECISIONS) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_decisions(
    data: dict[str, Any],
    *,
    canonical_text: str,
    candidate_text: str,
) -> list[str]:
    errors: list[str] = []

    state = data.get("scientific_state", {})
    _require(errors, data.get("status") == "CANDIDATE_HOLD", "status must remain CANDIDATE_HOLD")
    _require(errors, data.get("canonical_research_freeze_unchanged") is True, "canonical freeze must remain unchanged")
    _require(errors, state.get("readiness") == "descriptive_only", "readiness must remain descriptive_only")
    _require(errors, state.get("research_mode") == "PROOF_MODE", "research mode must remain PROOF_MODE")
    _require(errors, state.get("research_freeze") == "PRE-FREEZE", "candidate must remain PRE-FREEZE")
    _require(errors, state.get("external_registration") == "NOT_SUBMITTED", "external registration must remain NOT_SUBMITTED")
    _require(errors, state.get("stage_b_status") == "NOT_AUTHORISED_TO_START", "Stage B must remain unauthorised")
    _require(errors, state.get("scientific_claim_evidence") is False, "candidate is not scientific claim evidence")
    _require(errors, "PRE-FREEZE" in canonical_text, "canonical RESEARCH_FREEZE_001.md must state PRE-FREEZE")
    _require(errors, "CANDIDATE_HOLD" in candidate_text, "candidate Markdown must state CANDIDATE_HOLD")
    _require(errors, "NOT FROZEN" in candidate_text, "candidate Markdown must state NOT FROZEN")

    evidence = data.get("evidence_basis", {})
    for key in (
        "stage_a_source_sha256",
        "stage_a_selection_manifest_sha256",
        "stage_a_selected_features_sha256",
    ):
        _require(errors, bool(HEX64.fullmatch(str(evidence.get(key, "")))), f"{key} must be SHA-256")
    _require(errors, evidence.get("stage_a_records") == 500, "Stage A record count must remain 500")
    _require(errors, evidence.get("stage_a_lineage_overlap") == 0, "Stage A lineage overlap must remain zero")

    scope = data.get("scope", {})
    domains = scope.get("domains", [])
    tasks = scope.get("task_strata", [])
    lengths = scope.get("length_strata_words", {})
    _require(errors, scope.get("language") == ["en"], "candidate scope must remain English-only")
    _require(errors, len(domains) == 4 and len(set(domains)) == 4, "exactly four unique domains required")
    _require(errors, len(tasks) == 6 and len(set(tasks)) == 6, "exactly six unique task strata required")
    _require(errors, set(lengths) == {"short", "medium", "long"}, "three named length strata required")
    _require(errors, lengths.get("short") == [128, 255], "short length stratum drift")
    _require(errors, lengths.get("medium") == [256, 511], "medium length stratum drift")
    _require(errors, lengths.get("long") == [512, 900], "long length stratum drift")
    _require(errors, scope.get("primary_transformation_track") == "T0_CLEAN", "T0 must remain the sole primary track")

    registry = data.get("source_registry_candidate", {})
    known = registry.get("known_classes", [])
    unknown = registry.get("held_out_unknown_classes", [])
    _require(errors, len(known) == 4, "candidate must contain four known classes")
    _require(errors, len(unknown) == 1, "candidate must contain one held-out unknown class")
    _require(errors, known and known[0].get("type") == "human_control", "first known class must be human control")
    for entry in known[1:] + unknown:
        _require(errors, entry.get("type") == "model_family", "non-human source must be model_family")
        _require(errors, bool(entry.get("repository")), "model repository is required")
        _require(errors, bool(HEX40.fullmatch(str(entry.get("revision", "")))), "model revision must be a 40-character commit")
    _require(errors, known[0].get("exact_source_manifest") is None, "real human source manifest must not be fabricated in candidate")

    design = data.get("sample_design", {})
    domain_count = design.get("domain_count")
    task_count = design.get("task_count")
    length_count = design.get("length_count")
    cells = design.get("cell_count")
    _require(errors, all(_is_int(v) for v in (domain_count, task_count, length_count, cells)), "sample dimensions must be integers")
    if all(_is_int(v) for v in (domain_count, task_count, length_count, cells)):
        _require(errors, cells == domain_count * task_count * length_count, "cell count arithmetic mismatch")
        _require(errors, domain_count == len(domains), "domain count must match scope")
        _require(errors, task_count == len(tasks), "task count must match scope")
        _require(errors, length_count == len(lengths), "length count must match scope")

    per_cell = design.get("known_partition_per_cell_per_class", {})
    per_known_cell = design.get("known_lineages_per_cell_per_class")
    unknown_per_cell = design.get("unknown_lineages_per_cell")
    partition_sum = sum(value for value in per_cell.values() if _is_int(value))
    _require(errors, set(per_cell) == {"reference", "probability_calibration", "conformal_calibration", "sealed_test"}, "known partition roles drift")
    _require(errors, partition_sum == per_known_cell == 6, "known per-cell partition must sum to six")
    _require(errors, unknown_per_cell == 3, "unknown per-cell count must remain three")

    counts = design.get("counts", {})
    if _is_int(cells):
        _require(errors, counts.get("per_known_class_total") == cells * 6, "per-known total mismatch")
        _require(errors, counts.get("per_known_class_reference") == cells * 3, "reference count mismatch")
        _require(errors, counts.get("per_known_class_probability_calibration") == cells, "probability calibration count mismatch")
        _require(errors, counts.get("per_known_class_conformal_calibration") == cells, "conformal calibration count mismatch")
        _require(errors, counts.get("per_known_class_sealed_test") == cells, "known sealed count mismatch")
        _require(errors, counts.get("all_known_total") == cells * 6 * 4, "all-known total mismatch")
        _require(errors, counts.get("held_out_unknown_sealed_test") == cells * 3, "unknown total mismatch")
        _require(errors, counts.get("clean_total") == cells * 6 * 4 + cells * 3, "clean total mismatch")
        _require(errors, counts.get("sealed_clean_total") == cells * 4 + cells * 3, "sealed clean total mismatch")
        _require(errors, design.get("secondary_t1_count") == len(domains) * len(tasks) * 5, "T1 count mismatch")
    _require(errors, design.get("partition_seed") == 20260730, "partition seed drift")

    minimum = data.get("minimum_evidence", {})
    _require(errors, minimum.get("minimum_words") == 128, "minimum word threshold drift")
    _require(errors, minimum.get("minimum_unicode_letters") == 600, "minimum letter threshold drift")
    _require(errors, minimum.get("maximum_words_for_primary_scope") == 900, "maximum primary word scope drift")
    _require(errors, minimum.get("failure_outcome") == "UNKNOWN_INSUFFICIENT_EVIDENCE", "insufficient-evidence outcome drift")

    ood = data.get("ood_unknown", {})
    alpha = ood.get("alpha")
    _require(errors, isinstance(alpha, (int, float)) and 0 < alpha < 1, "conformal alpha must be in (0,1)")
    _require(errors, alpha == 0.05, "conformal alpha drift")
    _require(errors, ood.get("calibration_partition") == "conformal_calibration_only", "conformal partition drift")
    _require(errors, ood.get("threshold_tuning_on_stage_b") is False, "Stage B threshold tuning must remain forbidden")

    calibration = data.get("probability_calibration", {})
    acceptance = calibration.get("acceptance", {})
    _require(errors, calibration.get("fit_partition") == "probability_calibration_only", "probability partition drift")
    _require(errors, calibration.get("ece_bins") == 15, "ECE bin count drift")
    _require(errors, acceptance.get("ece_max") == 0.1, "ECE acceptance drift")
    _require(errors, acceptance.get("minimum_calibration_samples_per_known_class") == 50, "minimum calibration count drift")

    baselines = data.get("baseline_protocol", {})
    for key in ("chance", "majority", "length_only", "surface_statistics", "cogniprint_12d", "character_ngram", "word_ngram"):
        _require(errors, key in baselines, f"required baseline missing: {key}")

    stop = data.get("stop_and_claim_narrowing", {})
    rules = stop.get("rules", [])
    ids = [rule.get("id") for rule in rules if isinstance(rule, dict)]
    required_ids = {
        "OPEN_WORLD_FALSE_KNOWN",
        "UNKNOWN_REJECTION",
        "KNOWN_COVERAGE",
        "KNOWN_SIGNAL",
        "COGNIPRINT_VS_NGRAM",
        "PER_CLASS_COLLAPSE",
        "CALIBRATION_FAILURE",
        "DOMAIN_COLLAPSE",
        "STRATUM_REPLICATION",
        "T1_ROBUSTNESS",
    }
    _require(errors, len(ids) == len(set(ids)), "claim-narrowing rule IDs must be unique")
    _require(errors, set(ids) == required_ids, "claim-narrowing rule set drift")
    for rule in rules:
        _require(errors, bool(rule.get("condition")), "every claim rule needs an exact condition")
        _require(errors, bool(rule.get("consequence")), "every claim rule needs a consequence")

    custody = data.get("custody_boundary", {})
    _require(errors, custody.get("candidate_only") is True, "custody record must remain candidate-only")
    _require(errors, custody.get("stage_b_artifacts_created") is False, "candidate must not create Stage B artifacts")
    _require(errors, custody.get("sealed_labels_created") is False, "candidate must not create sealed labels")
    _require(errors, custody.get("predictor_label_access") is False, "predictor must not have label access")
    _require(errors, custody.get("external_registration_submitted") is False, "candidate must not claim external registration")
    _require(errors, len(data.get("unresolved_blockers", [])) >= 8, "HOLD candidate must retain unresolved blockers")

    return errors


def main() -> int:
    try:
        data = load_decisions()
        canonical_text = CANONICAL.read_text(encoding="utf-8")
        candidate_text = CANDIDATE.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Challenge 001 freeze candidate check failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_decisions(data, canonical_text=canonical_text, candidate_text=candidate_text)
    if errors:
        print("Challenge 001 freeze candidate check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("CHALLENGE_001_FREEZE_CANDIDATE_VALIDATED")
    print("STATUS=CANDIDATE_HOLD")
    print("CANONICAL_RESEARCH_FREEZE=PRE-FREEZE")
    print("EXTERNAL_REGISTRATION=NOT_SUBMITTED")
    print("STAGE_B=NOT_AUTHORISED_TO_START")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
