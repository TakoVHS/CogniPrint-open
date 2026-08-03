"""Development-only uncertainty and prospective claim-narrowing utilities."""
from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import asdict, dataclass
from statistics import NormalDist
from typing import Any, Callable, Sequence

from cogniprint.benchmarks.evaluation import classification_metrics


def _require_finite_scalar(value: Any, name: str) -> float:
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    return numeric


def wilson_interval(
    successes: int,
    total: int,
    *,
    confidence: float = 0.95,
) -> tuple[float, float]:
    if (
        isinstance(successes, bool)
        or isinstance(total, bool)
        or not isinstance(successes, int)
        or not isinstance(total, int)
    ):
        raise TypeError("successes and total must be integers")
    if total <= 0 or successes < 0 or successes > total:
        raise ValueError("require 0 <= successes <= total and total > 0")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0,1)")
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    proportion = successes / total
    denominator = 1.0 + z * z / total
    center = (
        proportion + z * z / (2.0 * total)
    ) / denominator
    radius = (
        z
        * math.sqrt(
            proportion * (1.0 - proportion) / total
            + z * z / (4.0 * total * total)
        )
        / denominator
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def _macro_f1(truth: list[str], predictions: list[str]) -> float:
    return float(classification_metrics(truth, predictions)["macro_f1"])


def paired_group_bootstrap_delta(
    truth: Sequence[str],
    predictions_a: Sequence[str],
    predictions_b: Sequence[str],
    group_ids: Sequence[str],
    *,
    metric_fn: Callable[[list[str], list[str]], float] = _macro_f1,
    resamples: int = 10_000,
    seed: int = 20260730,
    confidence: float = 0.95,
) -> dict[str, float | int]:
    if not (
        len(truth)
        == len(predictions_a)
        == len(predictions_b)
        == len(group_ids)
    ):
        raise ValueError("paired bootstrap inputs must have equal length")
    if not truth:
        raise ValueError("paired bootstrap inputs are empty")
    if resamples <= 0:
        raise ValueError("resamples must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0,1)")

    grouped: dict[str, list[int]] = defaultdict(list)
    for index, group_id in enumerate(group_ids):
        group = str(group_id).strip()
        if not group:
            raise ValueError("group IDs must be non-empty")
        grouped[group].append(index)
    groups = sorted(grouped)
    truth_list = [str(value) for value in truth]
    predictions_a_list = [str(value) for value in predictions_a]
    predictions_b_list = [str(value) for value in predictions_b]
    point = _require_finite_scalar(
        metric_fn(truth_list, predictions_a_list)
        - metric_fn(
            truth_list,
            predictions_b_list,
        ),
        "point bootstrap delta",
    )

    rng = random.Random(seed)
    deltas: list[float] = []
    for _ in range(resamples):
        sampled_groups = [groups[rng.randrange(len(groups))] for _ in groups]
        indices = [
            index
            for group in sampled_groups
            for index in grouped[group]
        ]
        sampled_truth = [truth_list[index] for index in indices]
        sampled_a = [predictions_a_list[index] for index in indices]
        sampled_b = [predictions_b_list[index] for index in indices]
        deltas.append(
            _require_finite_scalar(
                metric_fn(sampled_truth, sampled_a)
                - metric_fn(sampled_truth, sampled_b),
                "bootstrap delta",
            )
        )
    deltas.sort()

    def quantile(probability: float) -> float:
        position = probability * (len(deltas) - 1)
        lower_index = math.floor(position)
        upper_index = math.ceil(position)
        if lower_index == upper_index:
            return deltas[lower_index]
        weight = position - lower_index
        return deltas[lower_index] * (1.0 - weight) + deltas[upper_index] * weight

    tail = (1.0 - confidence) / 2.0
    return {
        "point_delta": point,
        "ci_lower": quantile(tail),
        "ci_upper": quantile(1.0 - tail),
        "confidence": confidence,
        "resamples": resamples,
        "seed": seed,
        "group_count": len(groups),
    }


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
    domain_gap_max: float = 0.15
    t1_balanced_accuracy_drop_max: float = 0.15
    t1_false_known_increase_max: float = 0.05


def evaluate_claim_narrowing(
    metrics: dict[str, Any],
    *,
    thresholds: DevelopmentClaimThresholds | None = None,
) -> dict[str, Any]:
    """Evaluate the prospective development-only claim matrix fail closed."""
    config = thresholds or DevelopmentClaimThresholds()
    required = {
        "held_out_false_known_point",
        "held_out_false_known_wilson_upper",
        "held_out_unknown_rejection",
        "known_coverage",
        "best_frozen_system_balanced_accuracy",
        "best_frozen_system_macro_f1",
        "cogniprint_vs_ngram_delta_macro_f1",
        "cogniprint_vs_ngram_ci_lower",
        "minimum_known_class_recall",
        "ece",
        "calibrated_nll",
        "uncalibrated_nll",
        "calibrated_brier",
        "uncalibrated_brier",
        "minimum_domain_balanced_accuracy",
        "maximum_domain_gap",
        "any_empty_primary_cell",
        "t1_balanced_accuracy_drop",
        "t1_false_known_increase",
    }
    missing = sorted(required - set(metrics))
    if missing:
        raise ValueError(f"claim metrics are incomplete: {missing}")

    numeric_metrics = {
        key: _require_finite_scalar(metrics[key], key)
        for key in required
        if key != "any_empty_primary_cell"
    }
    if not isinstance(metrics["any_empty_primary_cell"], bool):
        raise ValueError("any_empty_primary_cell must be a boolean")

    rules = [
        {
            "id": "OPEN_WORLD_FALSE_KNOWN",
            "triggered": (
                numeric_metrics["held_out_false_known_point"]
                > config.false_known_point_max
                or numeric_metrics["held_out_false_known_wilson_upper"]
                > config.false_known_wilson_upper_max
            ),
            "observed_values": {
                "held_out_false_known_point": numeric_metrics["held_out_false_known_point"],
                "held_out_false_known_wilson_upper": numeric_metrics["held_out_false_known_wilson_upper"],
            },
            "threshold": {
                "false_known_point_max": config.false_known_point_max,
                "false_known_wilson_upper_max": config.false_known_wilson_upper_max,
            },
            "condition": "held_out_false_known_point <= max AND held_out_false_known_wilson_upper <= max",
            "consequence": "Open-world family attribution claim remains locked.",
        },
        {
            "id": "UNKNOWN_REJECTION",
            "triggered": numeric_metrics["held_out_unknown_rejection"] < config.unknown_rejection_min,
            "observed_values": {
                "held_out_unknown_rejection": numeric_metrics["held_out_unknown_rejection"],
            },
            "threshold": {"unknown_rejection_min": config.unknown_rejection_min},
            "condition": "held_out_unknown_rejection >= minimum",
            "consequence": "UNKNOWN/OOD effectiveness claim remains locked.",
        },
        {
            "id": "KNOWN_COVERAGE",
            "triggered": numeric_metrics["known_coverage"] < config.known_coverage_min,
            "observed_values": {"known_coverage": numeric_metrics["known_coverage"]},
            "threshold": {"known_coverage_min": config.known_coverage_min},
            "condition": "known_coverage >= minimum",
            "consequence": "No operational attribution claim; report descriptive signal and abstention burden.",
        },
        {
            "id": "KNOWN_SIGNAL",
            "triggered": (
                numeric_metrics["best_frozen_system_balanced_accuracy"] < config.known_balanced_accuracy_min
                or numeric_metrics["best_frozen_system_macro_f1"] < config.known_macro_f1_min
            ),
            "observed_values": {
                "best_frozen_system_balanced_accuracy": numeric_metrics["best_frozen_system_balanced_accuracy"],
                "best_frozen_system_macro_f1": numeric_metrics["best_frozen_system_macro_f1"],
            },
            "threshold": {
                "known_balanced_accuracy_min": config.known_balanced_accuracy_min,
                "known_macro_f1_min": config.known_macro_f1_min,
            },
            "condition": "balanced accuracy and macro-F1 must each meet minimum",
            "consequence": "No family-level discrimination claim.",
        },
        {
            "id": "COGNIPRINT_VS_NGRAM",
            "triggered": (
                numeric_metrics["cogniprint_vs_ngram_ci_lower"] <= 0.0
                or numeric_metrics["cogniprint_vs_ngram_delta_macro_f1"] < config.cogniprint_ngram_delta_min
            ),
            "observed_values": {
                "cogniprint_vs_ngram_delta_macro_f1": numeric_metrics["cogniprint_vs_ngram_delta_macro_f1"],
                "cogniprint_vs_ngram_ci_lower": numeric_metrics["cogniprint_vs_ngram_ci_lower"],
            },
            "threshold": {
                "cogniprint_ngram_delta_min": config.cogniprint_ngram_delta_min,
                "cogniprint_vs_ngram_ci_lower_min": 0.0,
            },
            "condition": "point delta >= minimum AND paired 95% interval lower bound > 0",
            "consequence": "No claim that CogniPrint 12D adds value beyond lexical baselines.",
        },
        {
            "id": "PER_CLASS_COLLAPSE",
            "triggered": numeric_metrics["minimum_known_class_recall"] < config.per_class_recall_min,
            "observed_values": {
                "minimum_known_class_recall": numeric_metrics["minimum_known_class_recall"],
            },
            "threshold": {"per_class_recall_min": config.per_class_recall_min},
            "condition": "minimum per-known-class recall >= minimum",
            "consequence": "Result is mixed; collapsed classes must be named.",
        },
        {
            "id": "CALIBRATION_FAILURE",
            "triggered": (
                numeric_metrics["ece"] > config.ece_max
                or numeric_metrics["calibrated_nll"] > numeric_metrics["uncalibrated_nll"]
                or numeric_metrics["calibrated_brier"] > numeric_metrics["uncalibrated_brier"]
            ),
            "observed_values": {
                "ece": numeric_metrics["ece"],
                "calibrated_nll": numeric_metrics["calibrated_nll"],
                "uncalibrated_nll": numeric_metrics["uncalibrated_nll"],
                "calibrated_brier": numeric_metrics["calibrated_brier"],
                "uncalibrated_brier": numeric_metrics["uncalibrated_brier"],
            },
            "threshold": {"ece_max": config.ece_max},
            "condition": "ECE <= max AND calibrated NLL/Brier do not exceed uncalibrated values",
            "consequence": "Calibrated-confidence language remains locked.",
        },
        {
            "id": "DOMAIN_COLLAPSE",
            "triggered": (
                numeric_metrics["minimum_domain_balanced_accuracy"] < config.domain_balanced_accuracy_min
                or numeric_metrics["maximum_domain_gap"] > config.domain_gap_max
            ),
            "observed_values": {
                "minimum_domain_balanced_accuracy": numeric_metrics["minimum_domain_balanced_accuracy"],
                "maximum_domain_gap": numeric_metrics["maximum_domain_gap"],
            },
            "threshold": {
                "domain_balanced_accuracy_min": config.domain_balanced_accuracy_min,
                "domain_gap_max": config.domain_gap_max,
            },
            "condition": "minimum domain balanced accuracy >= minimum AND maximum domain gap <= max",
            "consequence": "Cross-domain generalisation claim remains locked.",
        },
        {
            "id": "STRATUM_REPLICATION",
            "triggered": metrics["any_empty_primary_cell"],
            "observed_values": {"any_empty_primary_cell": metrics["any_empty_primary_cell"]},
            "threshold": {"any_empty_primary_cell": False},
            "condition": "no empty primary cells are permitted",
            "consequence": "Primary run is a protocol deviation.",
        },
        {
            "id": "T1_ROBUSTNESS",
            "triggered": (
                numeric_metrics["t1_balanced_accuracy_drop"] > config.t1_balanced_accuracy_drop_max
                or numeric_metrics["t1_false_known_increase"] > config.t1_false_known_increase_max
            ),
            "observed_values": {
                "t1_balanced_accuracy_drop": numeric_metrics["t1_balanced_accuracy_drop"],
                "t1_false_known_increase": numeric_metrics["t1_false_known_increase"],
            },
            "threshold": {
                "t1_balanced_accuracy_drop_max": config.t1_balanced_accuracy_drop_max,
                "t1_false_known_increase_max": config.t1_false_known_increase_max,
            },
            "condition": "T1 balanced-accuracy drop and false-known increase must each stay within max",
            "consequence": "No light-edit robustness claim.",
        },
    ]
    triggered = [rule for rule in rules if rule["triggered"]]
    return {
        "protocol": "challenge-001-claim-narrowing-development-v1",
        "status": "DEVELOPMENT_ONLY",
        "scientific_claim_evidence": False,
        "thresholds": asdict(config),
        "rules": rules,
        "triggered_rule_ids": [rule["id"] for rule in triggered],
        "all_claims_unlocked": not triggered,
    }
