"""Development-only uncertainty and prospective claim-narrowing utilities."""
from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import asdict, dataclass
from statistics import NormalDist
from typing import Any, Callable, Sequence

from cogniprint.benchmarks.evaluation import classification_metrics


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
    point = metric_fn(truth_list, predictions_a_list) - metric_fn(
        truth_list,
        predictions_b_list,
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
            metric_fn(sampled_truth, sampled_a)
            - metric_fn(sampled_truth, sampled_b)
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

    rules = [
        (
            "OPEN_WORLD_FALSE_KNOWN",
            metrics["held_out_false_known_point"] > config.false_known_point_max
            or metrics["held_out_false_known_wilson_upper"]
            > config.false_known_wilson_upper_max,
            "Open-world family attribution claim remains locked.",
        ),
        (
            "UNKNOWN_REJECTION",
            metrics["held_out_unknown_rejection"]
            < config.unknown_rejection_min,
            "UNKNOWN/OOD effectiveness claim remains locked.",
        ),
        (
            "KNOWN_COVERAGE",
            metrics["known_coverage"] < config.known_coverage_min,
            "No operational attribution claim; report descriptive signal and abstention burden.",
        ),
        (
            "KNOWN_SIGNAL",
            metrics["best_frozen_system_balanced_accuracy"]
            < config.known_balanced_accuracy_min
            or metrics["best_frozen_system_macro_f1"]
            < config.known_macro_f1_min,
            "No family-level discrimination claim.",
        ),
        (
            "COGNIPRINT_VS_NGRAM",
            metrics["cogniprint_vs_ngram_ci_lower"] <= 0.0
            or metrics["cogniprint_vs_ngram_delta_macro_f1"]
            < config.cogniprint_ngram_delta_min,
            "No claim that CogniPrint 12D adds value beyond lexical baselines.",
        ),
        (
            "PER_CLASS_COLLAPSE",
            metrics["minimum_known_class_recall"] < config.per_class_recall_min,
            "Result is mixed; collapsed classes must be named.",
        ),
        (
            "CALIBRATION_FAILURE",
            metrics["ece"] > config.ece_max
            or metrics["calibrated_nll"] > metrics["uncalibrated_nll"]
            or metrics["calibrated_brier"] > metrics["uncalibrated_brier"],
            "Calibrated-confidence language remains locked.",
        ),
        (
            "DOMAIN_COLLAPSE",
            metrics["minimum_domain_balanced_accuracy"]
            < config.domain_balanced_accuracy_min
            or metrics["maximum_domain_gap"] > config.domain_gap_max,
            "Cross-domain generalisation claim remains locked.",
        ),
        (
            "STRATUM_REPLICATION",
            bool(metrics["any_empty_primary_cell"]),
            "Primary run is a protocol deviation.",
        ),
        (
            "T1_ROBUSTNESS",
            metrics["t1_balanced_accuracy_drop"]
            > config.t1_balanced_accuracy_drop_max
            or metrics["t1_false_known_increase"]
            > config.t1_false_known_increase_max,
            "No light-edit robustness claim.",
        ),
    ]
    evaluated = [
        {
            "id": rule_id,
            "triggered": bool(triggered),
            "consequence": consequence,
        }
        for rule_id, triggered, consequence in rules
    ]
    triggered = [rule for rule in evaluated if rule["triggered"]]
    return {
        "protocol": "challenge-001-claim-narrowing-development-v1",
        "status": "DEVELOPMENT_ONLY",
        "scientific_claim_evidence": False,
        "thresholds": asdict(config),
        "rules": evaluated,
        "triggered_rule_ids": [rule["id"] for rule in triggered],
        "all_claims_unlocked": not triggered,
    }
