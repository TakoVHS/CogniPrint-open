"""Development-only executable claim-narrowing matrix."""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Mapping


def _finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True)
class DevelopmentClaimThresholds:
    false_known_point_max: float = 0.10
    false_known_wilson_upper_max: float = 0.15
    unknown_rejection_min: float = 0.90
    known_coverage_min: float = 0.60
    known_balanced_accuracy_min: float = 0.50
    known_macro_f1_min: float = 0.50
    cogniprint_ngram_delta_min: float = 0.02
    per_class_recall_min: float = 0.40
    ece_max: float = 0.10
    domain_balanced_accuracy_min: float = 0.40
    domain_drop_max: float = 0.15
    t1_balanced_accuracy_drop_max: float = 0.15
    t1_false_known_increase_max: float = 0.05


def evaluate_claim_narrowing(
    values: Mapping[str, float | int],
    *,
    thresholds: DevelopmentClaimThresholds = DevelopmentClaimThresholds(),
) -> dict[str, Any]:
    """Evaluate failure-first development gates.

    These defaults mirror the non-canonical candidate values but do not freeze
    or authorize them.
    """

    required = {
        "held_out_false_known_point",
        "held_out_false_known_wilson_upper",
        "held_out_unknown_rejection",
        "known_coverage",
        "best_system_balanced_accuracy",
        "best_system_macro_f1",
        "cogniprint_vs_ngram_delta_macro_f1",
        "cogniprint_vs_ngram_ci_lower",
        "minimum_known_class_recall",
        "ece",
        "calibrated_nll",
        "uncalibrated_nll",
        "calibrated_brier",
        "uncalibrated_brier",
        "minimum_domain_balanced_accuracy",
        "maximum_domain_drop",
        "empty_primary_cells",
        "t1_balanced_accuracy_drop",
        "t1_false_known_increase",
    }
    missing = sorted(required - set(values))
    if missing:
        raise ValueError(f"claim inputs are missing: {missing}")
    numeric = {
        key: _finite(float(values[key]), key) for key in required
    }

    rules = [
        (
            "OPEN_WORLD_FALSE_KNOWN",
            numeric["held_out_false_known_point"]
            > thresholds.false_known_point_max
            or numeric["held_out_false_known_wilson_upper"]
            > thresholds.false_known_wilson_upper_max,
            "Open-world family attribution claim remains locked.",
        ),
        (
            "UNKNOWN_REJECTION",
            numeric["held_out_unknown_rejection"]
            < thresholds.unknown_rejection_min,
            "UNKNOWN/OOD effectiveness claim remains locked.",
        ),
        (
            "KNOWN_COVERAGE",
            numeric["known_coverage"] < thresholds.known_coverage_min,
            "No operational attribution claim; report descriptive signal "
            "and abstention burden.",
        ),
        (
            "KNOWN_SIGNAL",
            numeric["best_system_balanced_accuracy"]
            < thresholds.known_balanced_accuracy_min
            or numeric["best_system_macro_f1"]
            < thresholds.known_macro_f1_min,
            "No family-level discrimination claim.",
        ),
        (
            "COGNIPRINT_VS_NGRAM",
            numeric["cogniprint_vs_ngram_ci_lower"] <= 0.0
            or numeric["cogniprint_vs_ngram_delta_macro_f1"]
            < thresholds.cogniprint_ngram_delta_min,
            "No claim that CogniPrint 12D adds value beyond lexical baselines.",
        ),
        (
            "PER_CLASS_COLLAPSE",
            numeric["minimum_known_class_recall"]
            < thresholds.per_class_recall_min,
            "Result is mixed; collapsed classes must be named.",
        ),
        (
            "CALIBRATION_FAILURE",
            numeric["ece"] > thresholds.ece_max
            or numeric["calibrated_nll"] > numeric["uncalibrated_nll"]
            or numeric["calibrated_brier"] > numeric["uncalibrated_brier"],
            "Calibrated-confidence language remains locked.",
        ),
        (
            "DOMAIN_COLLAPSE",
            numeric["minimum_domain_balanced_accuracy"]
            < thresholds.domain_balanced_accuracy_min
            or numeric["maximum_domain_drop"] > thresholds.domain_drop_max,
            "Cross-domain generalisation claim remains locked.",
        ),
        (
            "STRATUM_REPLICATION",
            numeric["empty_primary_cells"] > 0,
            "Primary run is incomplete and must be reported as a protocol "
            "deviation.",
        ),
        (
            "T1_ROBUSTNESS",
            numeric["t1_balanced_accuracy_drop"]
            > thresholds.t1_balanced_accuracy_drop_max
            or numeric["t1_false_known_increase"]
            > thresholds.t1_false_known_increase_max,
            "No light-edit robustness claim.",
        ),
    ]
    decisions = [
        {
            "id": rule_id,
            "triggered": bool(triggered),
            "consequence": consequence,
        }
        for rule_id, triggered, consequence in rules
    ]
    return {
        "schema": "cogniprint-development-claim-narrowing-001",
        "status": "DEVELOPMENT_ONLY",
        "all_gates_clear": not any(
            item["triggered"] for item in decisions
        ),
        "triggered_rule_ids": [
            item["id"] for item in decisions if item["triggered"]
        ],
        "rules": decisions,
        "thresholds": asdict(thresholds),
        "stage_b_authorised": False,
        "scientific_claim_evidence": False,
    }


FORBIDDEN_PERSISTED_KEYS = frozenset(
    {
        "_text",
        "text",
        "generation",
        "prompt",
        "raw_text",
        "raw_prompt",
        "tokens",
        "vocabulary",
        "ngrams",
        "vectors",
        "per_document_vectors",
        "logits",
    }
)


def assert_aggregate_output_safe(
    payload: Any,
    path: str = "root",
) -> None:
    """Reject raw/recoverable development inputs in persisted outputs."""

    if isinstance(payload, dict):
        forbidden = FORBIDDEN_PERSISTED_KEYS & set(payload)
        if forbidden:
            raise ValueError(
                f"forbidden persisted keys at {path}: {sorted(forbidden)}"
            )
        for key, value in payload.items():
            assert_aggregate_output_safe(value, f"{path}.{key}")
    elif isinstance(payload, (list, tuple)):
        for index, value in enumerate(payload):
            assert_aggregate_output_safe(value, f"{path}[{index}]")
