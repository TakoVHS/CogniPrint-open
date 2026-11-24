"""Development-only RAID M2 calibration, abstention and open-set evaluator.

This module is deliberately bounded to Stage A-visible data. It does not
authorize Challenge 001 Stage B and does not turn benchmark association into
authorship, provenance, actor, intent, legal or forensic evidence.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from statistics import fmean
from typing import Any, Iterable, Sequence

from cogniprint.benchmarks.development_methods import (
    centroid_scores,
    evaluate_temperature,
    fit_centroid_model,
    fit_temperature,
    multiclass_brier_per_example,
    multiclass_nll_per_example,
    softmax,
)
from cogniprint.benchmarks.development_statistics import (
    area_under_risk_coverage,
    open_set_confidence_metrics,
    paired_group_bootstrap_mean_delta,
)
from cogniprint.benchmarks.evaluation import (
    classification_metrics,
    fingerprint_vector,
    lineage_group,
)
from cogniprint.benchmarks.ngram import (
    char_config,
    fit_hashed_ngram_scoring_model,
    hashed_ngram_score_matrix,
    word_config,
)

Record = dict[str, Any]

HUMAN_CONTROL = "human"
DEFAULT_MACHINE_FAMILIES = ("chatgpt", "gpt4", "llama-chat", "mistral-chat")
ROLE_ORDER = (
    "train",
    "probability_calibration",
    "conformal_calibration",
    "threshold_development",
    "evaluation",
)


@dataclass(frozen=True)
class M2RoleFractions:
    train: float = 0.35
    probability_calibration: float = 0.15
    conformal_calibration: float = 0.30
    threshold_development: float = 0.10
    evaluation: float = 0.10

    def validate(self) -> None:
        values = [float(getattr(self, role)) for role in ROLE_ORDER]
        if any(not math.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError("all M2 role fractions must be finite and positive")
        if abs(sum(values) - 1.0) > 1e-12:
            raise ValueError("M2 role fractions must sum to 1.0")


def _hash_fraction(value: str, seed: int) -> float:
    digest = hashlib.sha256(f"{seed}:{value}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16) / float(0xFFFFFFFFFFFFFFFF)


def _role_for_group(group: str, seed: int, fractions: M2RoleFractions) -> str:
    fractions.validate()
    value = _hash_fraction(group, seed)
    cumulative = 0.0
    for role in ROLE_ORDER:
        cumulative += float(getattr(fractions, role))
        if value < cumulative or role == ROLE_ORDER[-1]:
            return role
    raise AssertionError("unreachable M2 role assignment")


def _class_counts(records: Iterable[Record]) -> dict[str, int]:
    counts = Counter(str(record.get("model_family") or "").strip() for record in records)
    counts.pop("", None)
    return dict(sorted(counts.items()))


def _role_summary(records: list[Record]) -> dict[str, Any]:
    return {
        "records": len(records),
        "groups": len({lineage_group(record) for record in records}),
        "class_counts": _class_counts(records),
    }


def _stable_manifest_hash(rows: list[dict[str, str]]) -> str:
    encoded = json.dumps(
        rows,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_open_set_fold(
    records: list[Record],
    *,
    unknown_family: str,
    machine_families: Sequence[str] = DEFAULT_MACHINE_FAMILIES,
    human_control: str = HUMAN_CONTROL,
    seed: int = 20261124,
    fractions: M2RoleFractions | None = None,
    conformal_alpha: float = 0.05,
) -> dict[str, Any]:
    """Create leakage-safe M2 roles with one machine family fully held out.

    Every lineage group containing the unknown family is assigned wholly to the
    evaluation role. All other groups are deterministically hashed into the
    remaining/evaluation roles. This prevents a known-class sibling from the
    same lineage leaking into training when the unknown sibling is evaluated.
    """
    if not records:
        raise ValueError("M2 records are empty")
    fractions = fractions or M2RoleFractions()
    fractions.validate()
    if not math.isfinite(conformal_alpha) or not 0.0 < conformal_alpha < 1.0:
        raise ValueError("conformal_alpha must be finite and in (0,1)")

    machines = tuple(str(value).strip() for value in machine_families)
    if not machines or any(not value for value in machines) or len(set(machines)) != len(machines):
        raise ValueError("machine_families must be non-empty unique strings")
    unknown = str(unknown_family).strip()
    if unknown not in machines:
        raise ValueError("unknown_family must be one of machine_families")
    human = str(human_control).strip()
    if not human or human in machines:
        raise ValueError("human_control must be non-empty and distinct from machine families")

    expected_labels = {human, *machines}
    observed_labels = {str(record.get("model_family") or "").strip() for record in records}
    if "" in observed_labels:
        raise ValueError("M2 record is missing model_family")
    if observed_labels != expected_labels:
        raise ValueError(
            f"M2 label set mismatch: expected {sorted(expected_labels)}, got {sorted(observed_labels)}"
        )

    known_labels = tuple(sorted(expected_labels - {unknown}))
    groups: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        groups[lineage_group(record)].append(record)

    roles: dict[str, list[Record]] = {role: [] for role in ROLE_ORDER}
    manifest_rows: list[dict[str, str]] = []
    for group in sorted(groups):
        group_records = groups[group]
        group_labels = {str(record["model_family"]) for record in group_records}
        role = (
            "evaluation"
            if unknown in group_labels
            else _role_for_group(group, seed, fractions)
        )
        roles[role].extend(group_records)
        for record in sorted(
            group_records,
            key=lambda item: str(item.get("source_record_id") or item.get("text_sha256") or ""),
        ):
            manifest_rows.append(
                {
                    "source_record_id": str(record.get("source_record_id") or ""),
                    "lineage_group": group,
                    "model_family": str(record["model_family"]),
                    "role": role,
                }
            )

    role_groups = {
        role: {lineage_group(record) for record in role_records}
        for role, role_records in roles.items()
    }
    for left_index, left in enumerate(ROLE_ORDER):
        for right in ROLE_ORDER[left_index + 1 :]:
            overlap = role_groups[left] & role_groups[right]
            if overlap:
                raise AssertionError(
                    f"M2 lineage leakage between {left} and {right}: {sorted(overlap)[:3]}"
                )

    for role in ROLE_ORDER[:-1]:
        if any(str(record["model_family"]) == unknown for record in roles[role]):
            raise AssertionError(f"unknown family leaked into M2 {role}")

    for role in ROLE_ORDER:
        if not roles[role]:
            raise ValueError(f"M2 role {role} is empty")

    min_conformal = math.ceil((1.0 - conformal_alpha) / conformal_alpha)
    for role in (
        "train",
        "probability_calibration",
        "conformal_calibration",
        "threshold_development",
    ):
        labels = {str(record["model_family"]) for record in roles[role]}
        missing = set(known_labels) - labels
        if missing:
            raise ValueError(f"M2 role {role} is missing known classes: {sorted(missing)}")

    evaluation_known = [
        record for record in roles["evaluation"]
        if str(record["model_family"]) in known_labels
    ]
    evaluation_unknown = [
        record for record in roles["evaluation"]
        if str(record["model_family"]) == unknown
    ]
    if not evaluation_known:
        raise ValueError("M2 evaluation contains no known-class records")
    if not evaluation_unknown:
        raise ValueError("M2 evaluation contains no held-out unknown records")
    missing_eval = set(known_labels) - {str(record["model_family"]) for record in evaluation_known}
    if missing_eval:
        raise ValueError(
            f"M2 known evaluation is missing classes: {sorted(missing_eval)}"
        )

    conformal_counts = _class_counts(roles["conformal_calibration"])
    undersized = {
        label: conformal_counts.get(label, 0)
        for label in known_labels
        if conformal_counts.get(label, 0) < min_conformal
    }
    if undersized:
        raise ValueError(
            "INSUFFICIENT DEVELOPMENT EVIDENCE: conformal calibration "
            f"requires at least {min_conformal} records per known class; got {undersized}"
        )

    return {
        "unknown_family": unknown,
        "known_labels": list(known_labels),
        "seed": seed,
        "fractions": asdict(fractions),
        "conformal_alpha": conformal_alpha,
        "minimum_conformal_records_per_class": min_conformal,
        "roles": roles,
        "evaluation_known": evaluation_known,
        "evaluation_unknown": evaluation_unknown,
        "role_summary": {
            role: _role_summary(role_records)
            for role, role_records in roles.items()
        },
        "role_assignment_sha256": _stable_manifest_hash(manifest_rows),
        "role_manifest": manifest_rows,
        "lineage_overlap_count": 0,
    }


@dataclass(frozen=True)
class ProbabilityConformalModel:
    labels: tuple[str, ...]
    alpha: float
    calibration_scores: dict[str, tuple[float, ...]]
    method: str = "class_conditional_split_conformal_on_one_minus_probability"


def fit_probability_conformal(
    probabilities: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
    *,
    alpha: float = 0.05,
) -> ProbabilityConformalModel:
    labels_tuple = tuple(str(label).strip() for label in labels)
    if (
        not labels_tuple
        or any(not label for label in labels_tuple)
        or len(set(labels_tuple)) != len(labels_tuple)
    ):
        raise ValueError("conformal labels must be non-empty unique strings")
    if len(probabilities) != len(truth) or not probabilities:
        raise ValueError("conformal probabilities and truth must be non-empty and equal length")
    if not math.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("conformal alpha must be finite and in (0,1)")

    index = {label: position for position, label in enumerate(labels_tuple)}
    by_class: dict[str, list[float]] = defaultdict(list)
    for row, actual_raw in zip(probabilities, truth):
        actual = str(actual_raw).strip()
        if actual not in index:
            raise ValueError("conformal truth contains a label absent from labels")
        values = [float(value) for value in row]
        if len(values) != len(labels_tuple):
            raise ValueError("conformal probability width does not match labels")
        if any(not math.isfinite(value) or value < 0.0 or value > 1.0 for value in values):
            raise ValueError("conformal probabilities must be finite and in [0,1]")
        if abs(sum(values) - 1.0) > 1e-6:
            raise ValueError("conformal probabilities must sum to one")
        by_class[actual].append(1.0 - values[index[actual]])

    missing = set(labels_tuple) - set(by_class)
    if missing:
        raise ValueError(f"conformal calibration is missing classes: {sorted(missing)}")
    minimum = math.ceil((1.0 - alpha) / alpha)
    undersized = {
        label: len(by_class[label])
        for label in labels_tuple
        if len(by_class[label]) < minimum
    }
    if undersized:
        raise ValueError(
            "INSUFFICIENT DEVELOPMENT EVIDENCE: probability conformal "
            f"requires at least {minimum} records per class; got {undersized}"
        )

    return ProbabilityConformalModel(
        labels=labels_tuple,
        alpha=alpha,
        calibration_scores={
            label: tuple(sorted(by_class[label]))
            for label in labels_tuple
        },
    )


def probability_conformal_set(
    model: ProbabilityConformalModel,
    probabilities: Sequence[float],
) -> dict[str, Any]:
    values = [float(value) for value in probabilities]
    if len(values) != len(model.labels):
        raise ValueError("probability row width does not match conformal labels")
    if any(not math.isfinite(value) or value < 0.0 or value > 1.0 for value in values):
        raise ValueError("probability row must be finite and in [0,1]")
    if abs(sum(values) - 1.0) > 1e-6:
        raise ValueError("probability row must sum to one")

    p_values: dict[str, float] = {}
    for index, label in enumerate(model.labels):
        candidate = 1.0 - values[index]
        calibration = model.calibration_scores[label]
        p_values[label] = (
            1.0 + sum(score >= candidate for score in calibration)
        ) / (len(calibration) + 1.0)
    accepted = sorted(
        label for label, p_value in p_values.items()
        if p_value > model.alpha
    )
    if len(accepted) == 1:
        decision = accepted[0]
    elif not accepted:
        decision = "UNKNOWN_OOD"
    else:
        decision = "UNKNOWN_AMBIGUOUS"
    return {
        "decision": decision,
        "accepted_classes": accepted,
        "p_values": p_values,
        "alpha": model.alpha,
    }


def evaluate_probability_conformal(
    model: ProbabilityConformalModel,
    probabilities: Sequence[Sequence[float]],
    truth: Sequence[str],
) -> dict[str, Any]:
    if len(probabilities) != len(truth) or not probabilities:
        raise ValueError("evaluation probabilities and truth must be non-empty and equal length")

    known_labels = set(model.labels)
    known_total = known_covered = known_singleton = known_singleton_correct = 0
    known_empty = known_ambiguous = 0
    unknown_total = unknown_false_known = unknown_rejected = 0
    for row, actual_raw in zip(probabilities, truth):
        actual = str(actual_raw).strip()
        result = probability_conformal_set(model, row)
        accepted = set(result["accepted_classes"])
        decision = str(result["decision"])
        if actual in known_labels:
            known_total += 1
            if actual in accepted:
                known_covered += 1
            if decision in known_labels:
                known_singleton += 1
                if decision == actual:
                    known_singleton_correct += 1
            elif decision == "UNKNOWN_OOD":
                known_empty += 1
            else:
                known_ambiguous += 1
        else:
            unknown_total += 1
            if decision in known_labels:
                unknown_false_known += 1
            else:
                unknown_rejected += 1

    return {
        "known_total": known_total,
        "known_prediction_set_coverage": (
            known_covered / known_total if known_total else None
        ),
        "known_singleton_rate": (
            known_singleton / known_total if known_total else None
        ),
        "known_singleton_accuracy": (
            known_singleton_correct / known_singleton
            if known_singleton else None
        ),
        "known_empty_set_rate": (
            known_empty / known_total if known_total else None
        ),
        "known_ambiguous_set_rate": (
            known_ambiguous / known_total if known_total else None
        ),
        "unknown_total": unknown_total,
        "unknown_false_known_rate": (
            unknown_false_known / unknown_total if unknown_total else None
        ),
        "unknown_rejection_rate": (
            unknown_rejected / unknown_total if unknown_total else None
        ),
        "coverage_guarantee_scope": (
            "known-class prediction-set coverage under class-conditional "
            "exchangeability; no singleton-correctness or OOD-rejection guarantee"
        ),
    }


def select_threshold_for_min_coverage(
    probabilities: Sequence[Sequence[float]],
    *,
    min_coverage: float = 0.60,
) -> dict[str, float]:
    if not probabilities:
        raise ValueError("threshold-development probabilities are empty")
    if not math.isfinite(min_coverage) or not 0.0 < min_coverage <= 1.0:
        raise ValueError("min_coverage must be finite and in (0,1]")
    confidences: list[float] = []
    for row in probabilities:
        values = [float(value) for value in row]
        if not values or any(not math.isfinite(value) or value < 0.0 or value > 1.0 for value in values):
            raise ValueError("threshold-development probabilities must be finite and in [0,1]")
        confidences.append(max(values))
    candidates = sorted(set(confidences), reverse=True)
    admissible = [
        threshold for threshold in candidates
        if sum(value >= threshold for value in confidences) / len(confidences)
        >= min_coverage
    ]
    if not admissible:
        raise AssertionError("no threshold can satisfy requested coverage")
    threshold = max(admissible)
    coverage = sum(value >= threshold for value in confidences) / len(confidences)
    return {
        "threshold": threshold,
        "development_coverage": coverage,
        "minimum_required_coverage": min_coverage,
    }


def _predictions_from_probabilities(
    probabilities: Sequence[Sequence[float]],
    labels: Sequence[str],
) -> tuple[list[str], list[float]]:
    labels_tuple = tuple(labels)
    predictions: list[str] = []
    confidences: list[float] = []
    for row in probabilities:
        values = [float(value) for value in row]
        index = min(
            range(len(labels_tuple)),
            key=lambda position: (-values[position], labels_tuple[position]),
        )
        predictions.append(labels_tuple[index])
        confidences.append(values[index])
    return predictions, confidences


def _dense_score_rows(
    train: list[Record],
    role_records: dict[str, list[Record]],
) -> tuple[tuple[str, ...], dict[str, list[list[float]]]]:
    model = fit_centroid_model(train, fingerprint_vector)
    labels = model.labels
    rows: dict[str, list[list[float]]] = {}
    for role, records in role_records.items():
        rows[role] = [
            [
                centroid_scores(model, record, fingerprint_vector)[label]
                for label in labels
            ]
            for record in records
        ]
    return labels, rows


def _ngram_score_rows(
    train: list[Record],
    role_records: dict[str, list[Record]],
    *,
    kind: str,
    char_dimensions: int,
    word_dimensions: int,
) -> tuple[tuple[str, ...], dict[str, list[list[float]]], int]:
    if kind == "char":
        config = char_config(char_dimensions)
    elif kind == "word":
        config = word_config(word_dimensions)
    else:
        raise ValueError("ngram kind must be 'char' or 'word'")
    model = fit_hashed_ngram_scoring_model(train, config)
    rows = {
        role: hashed_ngram_score_matrix(model, records)
        for role, records in role_records.items()
    }
    return model.labels, rows, model.occupied_training_hash_bins


def _probability_rows(
    score_rows: Sequence[Sequence[float]],
    *,
    temperature: float,
) -> list[list[float]]:
    return [
        softmax(row, temperature=temperature)
        for row in score_rows
    ]


def evaluate_representation(
    *,
    representation: str,
    labels: Sequence[str],
    role_records: dict[str, list[Record]],
    score_rows: dict[str, list[list[float]]],
    conformal_alpha: float,
    minimum_known_coverage: float,
) -> dict[str, Any]:
    labels_tuple = tuple(labels)
    expected_known = {
        str(record["model_family"])
        for record in role_records["train"]
    }
    if set(labels_tuple) != expected_known:
        raise ValueError(
            f"{representation}: scoring labels do not match training classes"
        )

    probability_truth = [
        str(record["model_family"])
        for record in role_records["probability_calibration"]
    ]
    temperature_fit = fit_temperature(
        score_rows["probability_calibration"],
        probability_truth,
        labels_tuple,
    )
    temperature = temperature_fit.temperature

    evaluation_known = [
        record for record in role_records["evaluation"]
        if str(record["model_family"]) in set(labels_tuple)
    ]
    evaluation_unknown = [
        record for record in role_records["evaluation"]
        if str(record["model_family"]) not in set(labels_tuple)
    ]
    known_indices = [
        index for index, record in enumerate(role_records["evaluation"])
        if str(record["model_family"]) in set(labels_tuple)
    ]
    unknown_indices = [
        index for index, record in enumerate(role_records["evaluation"])
        if str(record["model_family"]) not in set(labels_tuple)
    ]
    known_scores = [score_rows["evaluation"][index] for index in known_indices]
    unknown_scores = [score_rows["evaluation"][index] for index in unknown_indices]
    known_truth = [str(record["model_family"]) for record in evaluation_known]

    temperature_evaluation = evaluate_temperature(
        known_scores,
        known_truth,
        labels_tuple,
        temperature=temperature,
        calibration_group_ids=[
            lineage_group(record)
            for record in role_records["probability_calibration"]
        ],
        evaluation_group_ids=[
            lineage_group(record)
            for record in evaluation_known
        ],
    )

    threshold_probabilities = _probability_rows(
        score_rows["threshold_development"],
        temperature=temperature,
    )
    threshold_policy = select_threshold_for_min_coverage(
        threshold_probabilities,
        min_coverage=minimum_known_coverage,
    )

    known_probabilities = _probability_rows(
        known_scores,
        temperature=temperature,
    )
    unknown_probabilities = _probability_rows(
        unknown_scores,
        temperature=temperature,
    )
    known_predictions, known_confidences = _predictions_from_probabilities(
        known_probabilities,
        labels_tuple,
    )
    _, unknown_confidences = _predictions_from_probabilities(
        unknown_probabilities,
        labels_tuple,
    )

    selective = area_under_risk_coverage(
        known_truth,
        known_predictions,
        known_confidences,
    )
    open_set = open_set_confidence_metrics(
        known_confidences,
        unknown_confidences,
        frozen_threshold=threshold_policy["threshold"],
    )

    conformal_probabilities = _probability_rows(
        score_rows["conformal_calibration"],
        temperature=temperature,
    )
    conformal_truth = [
        str(record["model_family"])
        for record in role_records["conformal_calibration"]
    ]
    conformal_model = fit_probability_conformal(
        conformal_probabilities,
        conformal_truth,
        labels_tuple,
        alpha=conformal_alpha,
    )
    combined_probabilities = known_probabilities + unknown_probabilities
    combined_truth = known_truth + [
        str(record["model_family"]) for record in evaluation_unknown
    ]
    conformal = evaluate_probability_conformal(
        conformal_model,
        combined_probabilities,
        combined_truth,
    )

    nll_values = multiclass_nll_per_example(
        known_scores,
        known_truth,
        labels_tuple,
        temperature=temperature,
    )
    brier_values = multiclass_brier_per_example(
        known_scores,
        known_truth,
        labels_tuple,
        temperature=temperature,
    )

    return {
        "representation": representation,
        "labels": list(labels_tuple),
        "temperature": temperature,
        "temperature_fit_partition": "probability_calibration_only",
        "classification": classification_metrics(known_truth, known_predictions),
        "probability_quality": {
            "uncalibrated_nll": temperature_evaluation.uncalibrated_nll,
            "calibrated_nll": temperature_evaluation.calibrated_nll,
            "uncalibrated_brier": temperature_evaluation.uncalibrated_brier,
            "calibrated_brier": temperature_evaluation.calibrated_brier,
            "uncalibrated_ece": temperature_evaluation.uncalibrated_ece,
            "calibrated_ece": temperature_evaluation.calibrated_ece,
            "uncalibrated_classwise_ece": (
                temperature_evaluation.uncalibrated_classwise_ece
            ),
            "calibrated_classwise_ece": (
                temperature_evaluation.calibrated_classwise_ece
            ),
        },
        "threshold_policy": threshold_policy,
        "selective": {
            "aurc": selective["aurc"],
            "full_coverage_risk": selective["full_coverage_risk"],
            "point_count": selective["point_count"],
        },
        "open_set": open_set,
        "conformal": conformal,
        "_nll_values": nll_values,
        "_brier_values": brier_values,
    }


def evaluate_m2_fold(
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
    bootstrap_resamples: int = 10_000,
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
        role: list(role_values)
        for role, role_values in roles.items()
        if role != "train"
    }

    dense_labels, dense_scores = _dense_score_rows(train, role_records)
    char_labels, char_scores, char_occupied = _ngram_score_rows(
        train,
        role_records,
        kind="char",
        char_dimensions=char_dimensions,
        word_dimensions=word_dimensions,
    )
    word_labels, word_scores, word_occupied = _ngram_score_rows(
        train,
        role_records,
        kind="word",
        char_dimensions=char_dimensions,
        word_dimensions=word_dimensions,
    )
    if not (dense_labels == char_labels == word_labels):
        raise ValueError("M2 representation label sets differ")

    representations = {
        "cogniprint_12d_cosine_centroid": evaluate_representation(
            representation="cogniprint_12d_cosine_centroid",
            labels=dense_labels,
            role_records=roles,
            score_rows=dense_scores,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
        ),
        "character_3_5_hashed_tfidf": evaluate_representation(
            representation="character_3_5_hashed_tfidf",
            labels=char_labels,
            role_records=roles,
            score_rows=char_scores,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
        ),
        "word_1_2_hashed_tfidf": evaluate_representation(
            representation="word_1_2_hashed_tfidf",
            labels=word_labels,
            role_records=roles,
            score_rows=word_scores,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
        ),
    }
    representations["character_3_5_hashed_tfidf"][
        "occupied_training_hash_bins"
    ] = char_occupied
    representations["word_1_2_hashed_tfidf"][
        "occupied_training_hash_bins"
    ] = word_occupied

    evaluation_known = fold["evaluation_known"]
    group_ids = [lineage_group(record) for record in evaluation_known]
    comparisons: dict[str, Any] = {}
    base = representations["cogniprint_12d_cosine_centroid"]
    for other_name in (
        "character_3_5_hashed_tfidf",
        "word_1_2_hashed_tfidf",
    ):
        other = representations[other_name]
        comparisons[f"cogniprint_12d_vs_{other_name}"] = {
            "nll_mean_delta": paired_group_bootstrap_mean_delta(
                base["_nll_values"],
                other["_nll_values"],
                group_ids,
                resamples=bootstrap_resamples,
                seed=seed,
            ),
            "brier_mean_delta": paired_group_bootstrap_mean_delta(
                base["_brier_values"],
                other["_brier_values"],
                group_ids,
                resamples=bootstrap_resamples,
                seed=seed + 1,
            ),
            "delta_semantics": (
                "cogniprint_12d_minus_baseline; negative favors CogniPrint "
                "for loss metrics"
            ),
        }

    for result in representations.values():
        result.pop("_nll_values", None)
        result.pop("_brier_values", None)

    return {
        "unknown_family": fold["unknown_family"],
        "known_labels": fold["known_labels"],
        "seed": seed,
        "conformal_alpha": conformal_alpha,
        "minimum_known_coverage": minimum_known_coverage,
        "role_summary": fold["role_summary"],
        "role_assignment_sha256": fold["role_assignment_sha256"],
        "lineage_overlap_count": fold["lineage_overlap_count"],
        "representations": representations,
        "paired_comparisons": comparisons,
    }


def evaluate_raid_m2(
    records: list[Record],
    *,
    machine_families: Sequence[str] = DEFAULT_MACHINE_FAMILIES,
    seed: int = 20261124,
    fractions: M2RoleFractions | None = None,
    conformal_alpha: float = 0.05,
    minimum_known_coverage: float = 0.60,
    char_dimensions: int = 262_144,
    word_dimensions: int = 131_072,
    bootstrap_resamples: int = 10_000,
) -> dict[str, Any]:
    """Evaluate all predeclared leave-one-machine-family-out Stage A folds."""
    machines = tuple(machine_families)
    folds = [
        evaluate_m2_fold(
            records,
            unknown_family=unknown,
            machine_families=machines,
            seed=seed,
            fractions=fractions,
            conformal_alpha=conformal_alpha,
            minimum_known_coverage=minimum_known_coverage,
            char_dimensions=char_dimensions,
            word_dimensions=word_dimensions,
            bootstrap_resamples=bootstrap_resamples,
        )
        for unknown in machines
    ]

    representation_names = tuple(folds[0]["representations"])
    aggregate: dict[str, Any] = {}
    for name in representation_names:
        aggregate[name] = {
            "mean_macro_f1": fmean(
                fold["representations"][name]["classification"]["macro_f1"]
                for fold in folds
            ),
            "mean_calibrated_nll": fmean(
                fold["representations"][name]["probability_quality"]["calibrated_nll"]
                for fold in folds
            ),
            "mean_calibrated_brier": fmean(
                fold["representations"][name]["probability_quality"]["calibrated_brier"]
                for fold in folds
            ),
            "mean_aurc": fmean(
                fold["representations"][name]["selective"]["aurc"]
                for fold in folds
            ),
            "mean_false_known_rate": fmean(
                fold["representations"][name]["open_set"]["false_known_rate"]
                for fold in folds
            ),
            "mean_conformal_unknown_false_known_rate": fmean(
                fold["representations"][name]["conformal"]["unknown_false_known_rate"]
                for fold in folds
            ),
        }

    return {
        "schema": "cogniprint-raid-calibration-m2-development-001",
        "protocol": "raid-m2-calibration-abstention-lofo-v1",
        "status": "DEVELOPMENT_ONLY",
        "scientific_claim_evidence": False,
        "readiness_boundary": "descriptive_only",
        "research_status": "PRE-FREEZE",
        "stage_b_status": "NOT_AUTHORISED_TO_START",
        "unknown_family_design": "leave-one-machine-family-out",
        "machine_families": list(machines),
        "human_control": HUMAN_CONTROL,
        "seed": seed,
        "fractions": asdict(fractions or M2RoleFractions()),
        "conformal_alpha": conformal_alpha,
        "minimum_known_coverage": minimum_known_coverage,
        "folds": folds,
        "aggregate": aggregate,
        "interpretation_boundary": (
            "Stage A development evidence only. No exact-model, AI-origin, "
            "authorship, actor, commissioning, intent, legal or forensic claim."
        ),
    }
