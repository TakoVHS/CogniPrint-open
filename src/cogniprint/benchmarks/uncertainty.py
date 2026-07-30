"""Development-only uncertainty and paired lineage bootstrap utilities."""
from __future__ import annotations

import math
import random
from collections import defaultdict
from statistics import fmean
from typing import Any, Sequence


def _finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def wilson_interval(
    successes: int,
    total: int,
    *,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    """Return the two-sided Wilson score interval."""

    if isinstance(successes, bool) or isinstance(total, bool):
        raise TypeError("successes and total must be integers")
    if not isinstance(successes, int) or not isinstance(total, int):
        raise TypeError("successes and total must be integers")
    if total <= 0 or not 0 <= successes <= total:
        raise ValueError("require 0 <= successes <= total and total > 0")
    z = _finite(z, "z")
    proportion = successes / total
    denominator = 1.0 + z * z / total
    centre = (proportion + z * z / (2.0 * total)) / denominator
    margin = (
        z
        * math.sqrt(
            proportion * (1.0 - proportion) / total
            + z * z / (4.0 * total * total)
        )
        / denominator
    )
    return max(0.0, centre - margin), min(1.0, centre + margin)


def _fixed_metric(
    truth: Sequence[str],
    predictions: Sequence[str],
    labels: Sequence[str],
    metric: str,
) -> float:
    if len(truth) != len(predictions) or not truth:
        raise ValueError("truth and predictions must be non-empty and equal length")
    if metric == "accuracy":
        return (
            sum(
                actual == predicted
                for actual, predicted in zip(truth, predictions)
            )
            / len(truth)
        )

    recalls: list[float] = []
    f1_values: list[float] = []
    for label in labels:
        tp = sum(
            actual == label and predicted == label
            for actual, predicted in zip(truth, predictions)
        )
        fn = sum(
            actual == label and predicted != label
            for actual, predicted in zip(truth, predictions)
        )
        fp = sum(
            actual != label and predicted == label
            for actual, predicted in zip(truth, predictions)
        )
        recall = tp / (tp + fn) if tp + fn else 0.0
        precision = tp / (tp + fp) if tp + fp else 0.0
        f1 = (
            2.0 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )
        recalls.append(recall)
        f1_values.append(f1)

    if metric == "balanced_accuracy":
        return fmean(recalls)
    if metric == "macro_f1":
        return fmean(f1_values)
    raise ValueError(
        "metric must be accuracy, balanced_accuracy, or macro_f1"
    )


def _percentile(
    values: Sequence[float],
    probability: float,
) -> float:
    if not values or not 0.0 <= probability <= 1.0:
        raise ValueError("invalid percentile request")
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def paired_group_bootstrap_delta(
    truth: Sequence[str],
    predictions_a: Sequence[str],
    predictions_b: Sequence[str],
    groups: Sequence[str],
    *,
    metric: str = "macro_f1",
    resamples: int = 10_000,
    seed: int = 20260730,
) -> dict[str, Any]:
    """Deterministic class-stratified lineage-group paired bootstrap."""

    size = len(truth)
    if size == 0 or not (
        len(predictions_a) == len(predictions_b) == len(groups) == size
    ):
        raise ValueError(
            "truth, predictions, and groups must be non-empty and equal length"
        )
    if resamples <= 0:
        raise ValueError("resamples must be positive")
    labels = tuple(sorted(set(truth)))
    if not labels or any(not label for label in labels):
        raise ValueError("truth labels must be non-empty")

    group_indices: dict[str, list[int]] = defaultdict(list)
    for index, group in enumerate(groups):
        group_id = str(group).strip()
        if not group_id:
            raise ValueError("group IDs must be non-empty")
        group_indices[group_id].append(index)

    groups_by_class: dict[str, list[str]] = {
        label: [] for label in labels
    }
    for group_id, indices in sorted(group_indices.items()):
        group_truth = {truth[index] for index in indices}
        if len(group_truth) != 1:
            raise ValueError(
                f"group {group_id!r} spans multiple truth classes"
            )
        groups_by_class[next(iter(group_truth))].append(group_id)
    if any(not values for values in groups_by_class.values()):
        raise ValueError(
            "every truth class must contain at least one lineage group"
        )

    point_a = _fixed_metric(truth, predictions_a, labels, metric)
    point_b = _fixed_metric(truth, predictions_b, labels, metric)
    rng = random.Random(seed)
    deltas: list[float] = []
    for _ in range(resamples):
        sampled_indices: list[int] = []
        for label in labels:
            class_groups = groups_by_class[label]
            for _ in range(len(class_groups)):
                sampled_group = class_groups[
                    rng.randrange(len(class_groups))
                ]
                sampled_indices.extend(group_indices[sampled_group])
        sample_truth = [truth[index] for index in sampled_indices]
        sample_a = [predictions_a[index] for index in sampled_indices]
        sample_b = [predictions_b[index] for index in sampled_indices]
        deltas.append(
            _fixed_metric(
                sample_truth,
                sample_a,
                labels,
                metric,
            )
            - _fixed_metric(
                sample_truth,
                sample_b,
                labels,
                metric,
            )
        )

    return {
        "metric": metric,
        "point_delta": round(point_a - point_b, 12),
        "ci_lower": round(_percentile(deltas, 0.025), 12),
        "ci_upper": round(_percentile(deltas, 0.975), 12),
        "resamples": resamples,
        "seed": seed,
        "group_count": len(group_indices),
        "stratified_by_truth_class": True,
    }
