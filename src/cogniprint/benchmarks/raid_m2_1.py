"""Post-result exploratory diagnostics for the executed RAID M2 study.

M2.1 is deliberately separate from the frozen M2 result. It may diagnose
selective-risk persistence, conformal ambiguity, score scale and conformal
effective sample structure. It must not overwrite or relabel M2 #1.
"""
from __future__ import annotations

import math
from collections import defaultdict
from statistics import fmean, median
from typing import Any, Iterable, Sequence

from cogniprint.benchmarks.development_methods import (
    fit_temperature,
    multiclass_brier_per_example,
    multiclass_nll_per_example,
    softmax,
)
from cogniprint.benchmarks.development_statistics import selective_risk_curve
from cogniprint.benchmarks.evaluation import lineage_group
from cogniprint.benchmarks.raid_m2 import (
    DEFAULT_MACHINE_FAMILIES,
    M2RoleFractions,
    _dense_score_rows,
    _ngram_score_rows,
    _predictions_from_probabilities,
    _probability_rows,
    build_open_set_fold,
    fit_probability_conformal,
    probability_conformal_set,
    select_threshold_for_min_coverage,
)

Record = dict[str, Any]

M2_PARENT_RESULTS_SHA256 = (
    "1fb39616725c90470e5dbc35ff7f4211190448e9bb1505c256d5febeba275dc3"
)
M2_1_COVERAGE_TARGETS = (0.25, 0.50, 0.60, 0.75, 0.90, 1.00)
M2_1_TEMPERATURE_GRID = (
    0.005,
    0.010,
    0.020,
    0.050,
    0.100,
    0.200,
    0.500,
    1.000,
    2.000,
    5.000,
    10.000,
    20.000,
    50.000,
    100.000,
    200.000,
)


def _quantile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise ValueError("quantile values are empty")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("quantile probability must be in [0,1]")
    ordered = sorted(float(value) for value in values)
    if any(not math.isfinite(value) for value in ordered):
        raise ValueError("quantile values must be finite")
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def summarize_score_scale(
    score_rows: Sequence[Sequence[float]],
) -> dict[str, float | int]:
    if not score_rows:
        raise ValueError("score rows are empty")
    flattened: list[float] = []
    top_scores: list[float] = []
    margins: list[float] = []
    width: int | None = None
    for row in score_rows:
        values = [float(value) for value in row]
        if not values or any(not math.isfinite(value) for value in values):
            raise ValueError("score rows must be non-empty and finite")
        if width is None:
            width = len(values)
        elif len(values) != width:
            raise ValueError("score rows must have equal width")
        flattened.extend(values)
        ordered = sorted(values, reverse=True)
        top_scores.append(ordered[0])
        margins.append(
            ordered[0] - ordered[1] if len(ordered) > 1 else 0.0
        )
    mean = fmean(flattened)
    variance = fmean((value - mean) ** 2 for value in flattened)
    return {
        "records": len(score_rows),
        "classes": int(width or 0),
        "score_min": min(flattened),
        "score_max": max(flattened),
        "score_mean": mean,
        "score_std": math.sqrt(variance),
        "top1_mean": fmean(top_scores),
        "margin_mean": fmean(margins),
        "margin_median": median(margins),
        "margin_q25": _quantile(margins, 0.25),
        "margin_q75": _quantile(margins, 0.75),
    }


def temperature_sensitivity_profile(
    score_rows: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
    *,
    temperatures: Sequence[float] = M2_1_TEMPERATURE_GRID,
) -> dict[str, Any]:
    if not temperatures:
        raise ValueError("temperature grid is empty")
    grid = [float(value) for value in temperatures]
    if any(not math.isfinite(value) or value <= 0.0 for value in grid):
        raise ValueError("temperatures must be finite and positive")
    if len(set(grid)) != len(grid):
        raise ValueError("temperature grid must not contain duplicates")

    points: list[dict[str, float]] = []
    for temperature in grid:
        losses = multiclass_nll_per_example(
            score_rows,
            truth,
            labels,
            temperature=temperature,
        )
        points.append(
            {
                "temperature": temperature,
                "nll": fmean(losses),
            }
        )
    best = min(points, key=lambda item: (item["nll"], item["temperature"]))
    return {
        "grid": points,
        "best_grid_temperature": best["temperature"],
        "best_grid_nll": best["nll"],
        "selection_partition": "probability_calibration_only",
        "status": "POST_RESULT_EXPLORATORY",
    }


def evaluate_probability_quality_at_temperatures(
    score_rows: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
    temperatures: Iterable[float],
) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for raw_temperature in temperatures:
        temperature = float(raw_temperature)
        key = format(temperature, ".12g")
        nll = multiclass_nll_per_example(
            score_rows,
            truth,
            labels,
            temperature=temperature,
        )
        brier = multiclass_brier_per_example(
            score_rows,
            truth,
            labels,
            temperature=temperature,
        )
        result[key] = {
            "temperature": temperature,
            "nll": fmean(nll),
            "brier": fmean(brier),
        }
    return result


def selective_risk_at_targets(
    truth: Sequence[str],
    predictions: Sequence[str],
    confidences: Sequence[float],
    *,
    targets: Sequence[float] = M2_1_COVERAGE_TARGETS,
) -> list[dict[str, float | int]]:
    curve = selective_risk_curve(truth, predictions, confidences)
    result: list[dict[str, float | int]] = []
    for raw_target in targets:
        target = float(raw_target)
        if not 0.0 < target <= 1.0:
            raise ValueError("coverage targets must be in (0,1]")
        point = next(
            (candidate for candidate in curve if float(candidate["coverage"]) >= target),
            curve[-1],
        )
        result.append(
            {
                "target_coverage": target,
                "achieved_coverage": float(point["coverage"]),
                "accepted": int(point["accepted"]),
                "errors": int(point["errors"]),
                "selective_risk": float(point["selective_risk"]),
                "threshold": float(point["threshold"]),
            }
        )
    return result


def selective_risk_at_frozen_threshold(
    truth: Sequence[str],
    predictions: Sequence[str],
    confidences: Sequence[float],
    *,
    threshold: float,
) -> dict[str, float | int]:
    if not (len(truth) == len(predictions) == len(confidences)):
        raise ValueError("threshold selective-risk inputs must have equal length")
    if not truth:
        raise ValueError("threshold selective-risk inputs are empty")
    threshold = float(threshold)
    if not math.isfinite(threshold):
        raise ValueError("threshold must be finite")
    indices = [
        index for index, confidence in enumerate(confidences)
        if float(confidence) >= threshold
    ]
    accepted = len(indices)
    errors = sum(
        int(str(predictions[index]) != str(truth[index]))
        for index in indices
    )
    total = len(truth)
    return {
        "threshold": threshold,
        "accepted": accepted,
        "errors": errors,
        "coverage": accepted / total,
        "selective_risk": errors / accepted if accepted else None,
        "total": total,
    }


def conformal_outcome_decomposition(
    model: Any,
    probabilities: Sequence[Sequence[float]],
    truth: Sequence[str],
) -> dict[str, Any]:
    if len(probabilities) != len(truth) or not probabilities:
        raise ValueError("conformal diagnostic inputs must be non-empty and equal length")
    known_labels = set(model.labels)
    buckets = {
        "known": {
            "total": 0,
            "singleton": 0,
            "singleton_correct": 0,
            "singleton_incorrect": 0,
            "empty": 0,
            "ambiguous": 0,
            "covered": 0,
            "set_sizes": [],
        },
        "unknown": {
            "total": 0,
            "singleton_false_known": 0,
            "empty": 0,
            "ambiguous": 0,
            "set_sizes": [],
        },
    }
    for row, actual_raw in zip(probabilities, truth):
        actual = str(actual_raw)
        outcome = probability_conformal_set(model, row)
        accepted = list(outcome["accepted_classes"])
        size = len(accepted)
        if actual in known_labels:
            bucket = buckets["known"]
            bucket["total"] += 1
            bucket["set_sizes"].append(size)
            if actual in accepted:
                bucket["covered"] += 1
            if size == 0:
                bucket["empty"] += 1
            elif size == 1:
                bucket["singleton"] += 1
                if accepted[0] == actual:
                    bucket["singleton_correct"] += 1
                else:
                    bucket["singleton_incorrect"] += 1
            else:
                bucket["ambiguous"] += 1
        else:
            bucket = buckets["unknown"]
            bucket["total"] += 1
            bucket["set_sizes"].append(size)
            if size == 0:
                bucket["empty"] += 1
            elif size == 1:
                bucket["singleton_false_known"] += 1
            else:
                bucket["ambiguous"] += 1

    def summarize_known(bucket: dict[str, Any]) -> dict[str, Any]:
        total = int(bucket["total"])
        sizes = [int(value) for value in bucket["set_sizes"]]
        singleton = int(bucket["singleton"])
        return {
            "total": total,
            "prediction_set_coverage": bucket["covered"] / total if total else None,
            "singleton_rate": singleton / total if total else None,
            "singleton_accuracy": (
                bucket["singleton_correct"] / singleton if singleton else None
            ),
            "singleton_correct_rate": (
                bucket["singleton_correct"] / total if total else None
            ),
            "singleton_incorrect_rate": (
                bucket["singleton_incorrect"] / total if total else None
            ),
            "empty_set_rate": bucket["empty"] / total if total else None,
            "ambiguous_set_rate": bucket["ambiguous"] / total if total else None,
            "set_size_mean": fmean(sizes) if sizes else None,
            "set_size_median": median(sizes) if sizes else None,
            "set_size_max": max(sizes) if sizes else None,
        }

    def summarize_unknown(bucket: dict[str, Any]) -> dict[str, Any]:
        total = int(bucket["total"])
        sizes = [int(value) for value in bucket["set_sizes"]]
        return {
            "total": total,
            "empty_set_rate": bucket["empty"] / total if total else None,
            "ambiguous_set_rate": bucket["ambiguous"] / total if total else None,
            "singleton_false_known_rate": (
                bucket["singleton_false_known"] / total if total else None
            ),
            "set_size_mean": fmean(sizes) if sizes else None,
            "set_size_median": median(sizes) if sizes else None,
            "set_size_max": max(sizes) if sizes else None,
        }

    return {
        "known": summarize_known(buckets["known"]),
        "unknown": summarize_unknown(buckets["unknown"]),
        "interpretation_boundary": (
            "empty and ambiguous conformal sets are reported separately; neither "
            "is proof that the generating source is genuinely unknown"
        ),
    }


def conformal_effective_sample_structure(
    records: Sequence[Record],
    labels: Sequence[str],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for label in labels:
        label_records = [
            record for record in records
            if str(record["model_family"]) == str(label)
        ]
        grouped: dict[str, int] = defaultdict(int)
        for record in label_records:
            grouped[lineage_group(record)] += 1
        counts = sorted(grouped.values())
        result[str(label)] = {
            "records": len(label_records),
            "unique_lineage_groups": len(grouped),
            "largest_records_per_lineage_group": max(counts) if counts else 0,
            "median_records_per_lineage_group": median(counts) if counts else None,
        }
    return result


def _diagnose_representation(
    *,
    name: str,
    labels: Sequence[str],
    roles: dict[str, list[Record]],
    score_rows: dict[str, list[list[float]]],
    conformal_alpha: float,
    minimum_known_coverage: float,
) -> dict[str, Any]:
    labels_tuple = tuple(labels)
    known_set = set(labels_tuple)
    probability_truth = [
        str(record["model_family"])
        for record in roles["probability_calibration"]
    ]
    m2_temperature = fit_temperature(
        score_rows["probability_calibration"],
        probability_truth,
        labels_tuple,
    ).temperature
    temperature_profile = temperature_sensitivity_profile(
        score_rows["probability_calibration"],
        probability_truth,
        labels_tuple,
    )
    diagnostic_temperature = float(
        temperature_profile["best_grid_temperature"]
    )

    known_indices = [
        index for index, record in enumerate(roles["evaluation"])
        if str(record["model_family"]) in known_set
    ]
    unknown_indices = [
        index for index, record in enumerate(roles["evaluation"])
        if str(record["model_family"]) not in known_set
    ]
    known_records = [roles["evaluation"][index] for index in known_indices]
    unknown_records = [roles["evaluation"][index] for index in unknown_indices]
    known_scores = [score_rows["evaluation"][index] for index in known_indices]
    unknown_scores = [score_rows["evaluation"][index] for index in unknown_indices]
    known_truth = [str(record["model_family"]) for record in known_records]

    known_probabilities = _probability_rows(
        known_scores,
        temperature=m2_temperature,
    )
    unknown_probabilities = _probability_rows(
        unknown_scores,
        temperature=m2_temperature,
    )
    predictions, confidences = _predictions_from_probabilities(
        known_probabilities,
        labels_tuple,
    )

    threshold_probabilities = _probability_rows(
        score_rows["threshold_development"],
        temperature=m2_temperature,
    )
    threshold_policy = select_threshold_for_min_coverage(
        threshold_probabilities,
        min_coverage=minimum_known_coverage,
    )

    conformal_probabilities = _probability_rows(
        score_rows["conformal_calibration"],
        temperature=m2_temperature,
    )
    conformal_truth = [
        str(record["model_family"])
        for record in roles["conformal_calibration"]
    ]
    conformal_model = fit_probability_conformal(
        conformal_probabilities,
        conformal_truth,
        labels_tuple,
        alpha=conformal_alpha,
    )

    return {
        "representation": name,
        "m2_temperature": m2_temperature,
        "score_scale": {
            "probability_calibration": summarize_score_scale(
                score_rows["probability_calibration"]
            ),
            "known_evaluation": summarize_score_scale(known_scores),
        },
        "temperature_sensitivity": temperature_profile,
        "known_evaluation_probability_quality": evaluate_probability_quality_at_temperatures(
            known_scores,
            known_truth,
            labels_tuple,
            (1.0, m2_temperature, diagnostic_temperature),
        ),
        "selective_risk_grid": selective_risk_at_targets(
            known_truth,
            predictions,
            confidences,
        ),
        "frozen_threshold_policy": {
            **threshold_policy,
            "known_evaluation": selective_risk_at_frozen_threshold(
                known_truth,
                predictions,
                confidences,
                threshold=threshold_policy["threshold"],
            ),
        },
        "conformal_decomposition": conformal_outcome_decomposition(
            conformal_model,
            known_probabilities + unknown_probabilities,
            known_truth + [
                str(record["model_family"]) for record in unknown_records
            ],
        ),
        "conformal_effective_sample_structure": conformal_effective_sample_structure(
            roles["conformal_calibration"],
            labels_tuple,
        ),
    }


def evaluate_m2_1_fold(
    records: list[Record],
    *,
    unknown_family: str,
    machine_families: Sequence[str] = DEFAULT_MACHINE_FAMILIES,
    seed: int = 20261124,
    fractions: M2RoleFractions | None = None,
    conformal_alpha: float = 0.05,
    minimum_known_coverage: float = 0.60,
    char_dimensions: int = 262_144,
    word_dimensions: int = 131_072,
) -> dict[str, Any]:
    fold = build_open_set_fold(
        records,
        unknown_family=unknown_family,
        machine_families=machine_families,
        seed=seed,
        fractions=fractions,
        conformal_alpha=conformal_alpha,
    )
    roles = fold["roles"]
    train = roles["train"]
    role_records = {
        role: list(values)
        for role, values in roles.items()
        if role != "train"
    }

    dense_labels, dense_scores = _dense_score_rows(train, role_records)
    char_labels, char_scores, _ = _ngram_score_rows(
        train,
        role_records,
        kind="char",
        char_dimensions=char_dimensions,
        word_dimensions=word_dimensions,
    )
    word_labels, word_scores, _ = _ngram_score_rows(
        train,
        role_records,
        kind="word",
        char_dimensions=char_dimensions,
        word_dimensions=word_dimensions,
    )
    if not (dense_labels == char_labels == word_labels):
        raise ValueError("M2.1 representation label sets differ")

    representations = {
        "cogniprint_12d_cosine_centroid": _diagnose_representation(
            name="cogniprint_12d_cosine_centroid",
            labels=dense_labels,
            roles=roles,
            score_rows=dense_scores,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
        ),
        "character_3_5_hashed_tfidf": _diagnose_representation(
            name="character_3_5_hashed_tfidf",
            labels=char_labels,
            roles=roles,
            score_rows=char_scores,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
        ),
        "word_1_2_hashed_tfidf": _diagnose_representation(
            name="word_1_2_hashed_tfidf",
            labels=word_labels,
            roles=roles,
            score_rows=word_scores,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
        ),
    }
    return {
        "unknown_family": fold["unknown_family"],
        "role_assignment_sha256": fold["role_assignment_sha256"],
        "lineage_overlap_count": fold["lineage_overlap_count"],
        "representations": representations,
    }


def evaluate_raid_m2_1(
    records: list[Record],
    *,
    machine_families: Sequence[str] = DEFAULT_MACHINE_FAMILIES,
    seed: int = 20261124,
    fractions: M2RoleFractions | None = None,
    conformal_alpha: float = 0.05,
    minimum_known_coverage: float = 0.60,
    char_dimensions: int = 262_144,
    word_dimensions: int = 131_072,
) -> dict[str, Any]:
    folds = [
        evaluate_m2_1_fold(
            records,
            unknown_family=unknown_family,
            machine_families=machine_families,
            seed=seed,
            fractions=fractions,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
            char_dimensions=char_dimensions,
            word_dimensions=word_dimensions,
        )
        for unknown_family in machine_families
    ]
    return {
        "schema": "cogniprint-raid-m2-1-post-result-diagnostics-001",
        "status": "POST_RESULT_EXPLORATORY",
        "scientific_claim_evidence": False,
        "parent_m2_results_sha256": M2_PARENT_RESULTS_SHA256,
        "readiness_boundary": "descriptive_only",
        "research_status": "PRE-FREEZE",
        "stage_b_status": "NOT_AUTHORISED_TO_START",
        "seed": seed,
        "conformal_alpha": conformal_alpha,
        "minimum_known_coverage": minimum_known_coverage,
        "coverage_targets": list(M2_1_COVERAGE_TARGETS),
        "temperature_grid": list(M2_1_TEMPERATURE_GRID),
        "folds": folds,
        "interpretation_boundary": (
            "Post-result exploratory diagnostics only; may explain M2 failure "
            "modes but may not replace or strengthen the frozen M2 result."
        ),
    }
