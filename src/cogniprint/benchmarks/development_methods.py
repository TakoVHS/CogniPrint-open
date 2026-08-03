"""Dependency-free Challenge 001 methods for Stage A development fixtures only.

Nothing in this module is frozen scientific-claim evidence or authorization to
construct, inspect, or evaluate sealed Stage B data.
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from statistics import fmean, pstdev
from typing import Any, Callable, Iterable, Sequence

from cogniprint.benchmarks.evaluation import classification_metrics, lineage_group

Record = dict[str, Any]
VectorFn = Callable[[Record], list[float]]
UNKNOWN_OOD = "UNKNOWN_OOD"
UNKNOWN_AMBIGUOUS = "UNKNOWN_AMBIGUOUS"
UNKNOWN_INSUFFICIENT_EVIDENCE = "UNKNOWN_INSUFFICIENT_EVIDENCE"

SURFACE_FEATURE_NAMES = (
    "word_count",
    "unicode_letter_count",
    "sentence_count",
    "mean_word_length",
    "type_token_ratio",
    "digit_ratio",
    "uppercase_ratio",
    "newline_ratio",
    "period_ratio",
    "comma_ratio",
    "question_exclamation_ratio",
    "colon_semicolon_ratio",
)


def _require_finite_vector(vector: Sequence[float]) -> list[float]:
    values = [float(value) for value in vector]
    if any(not math.isfinite(value) for value in values):
        raise ValueError("feature vectors must be finite")
    return values


def _require_positive_int(value: Any, name: str, *, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def surface_statistics(text: str) -> dict[str, float]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    normalized = unicodedata.normalize("NFKC", text)
    words = re.findall(r"[^\W_]+", normalized, flags=re.UNICODE)
    letters = [char for char in normalized if char.isalpha()]
    non_space_count = max(sum(not char.isspace() for char in normalized), 1)
    sentence_count = (
        len(re.findall(r"[^.!?]+(?:[.!?]+|$)", normalized.strip()))
        if normalized.strip()
        else 0
    )
    word_count = len(words)
    letter_count = len(letters)
    return {
        "word_count": float(word_count),
        "unicode_letter_count": float(letter_count),
        "sentence_count": float(sentence_count),
        "mean_word_length": (
            sum(len(word) for word in words) / word_count if word_count else 0.0
        ),
        "type_token_ratio": (
            len({word.casefold() for word in words}) / word_count
            if word_count
            else 0.0
        ),
        "digit_ratio": sum(char.isdigit() for char in normalized) / non_space_count,
        "uppercase_ratio": (
            sum(char.isupper() for char in letters) / max(letter_count, 1)
        ),
        "newline_ratio": normalized.count("\n") / max(len(normalized), 1),
        "period_ratio": normalized.count(".") / non_space_count,
        "comma_ratio": normalized.count(",") / non_space_count,
        "question_exclamation_ratio": (
            normalized.count("?") + normalized.count("!")
        )
        / non_space_count,
        "colon_semicolon_ratio": (
            normalized.count(":") + normalized.count(";")
        )
        / non_space_count,
    }


def surface_statistics_vector(record: Record) -> list[float]:
    text = record.get("_text")
    if not isinstance(text, str):
        raise ValueError("record is missing transient _text for surface statistics")
    values = surface_statistics(text)
    return [values[name] for name in SURFACE_FEATURE_NAMES]


def _fit_standardizer(
    vectors: list[list[float]],
) -> tuple[list[float], list[float]]:
    if not vectors:
        raise ValueError("cannot fit standardizer on an empty vector set")
    sanitized = [_require_finite_vector(vector) for vector in vectors]
    width = len(sanitized[0])
    if width == 0 or any(len(vector) != width for vector in sanitized):
        raise ValueError("inconsistent feature-vector width")
    means = [fmean(vector[index] for vector in sanitized) for index in range(width)]
    scales = [pstdev(vector[index] for vector in sanitized) for index in range(width)]
    return means, [scale if scale > 1e-12 else 1.0 for scale in scales]


def _standardize(
    vector: Sequence[float],
    means: Sequence[float],
    scales: Sequence[float],
) -> list[float]:
    if len(vector) != len(means) or len(vector) != len(scales):
        raise ValueError("vector width does not match standardizer")
    checked = _require_finite_vector(vector)
    return [
        (value - means[index]) / scales[index]
        for index, value in enumerate(checked)
    ]


def _l2(vector: Sequence[float]) -> list[float]:
    checked = _require_finite_vector(vector)
    norm = math.sqrt(sum(value**2 for value in checked))
    if norm <= 1e-15:
        return [0.0 for _ in checked]
    return [value / norm for value in checked]


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("cosine vectors have different widths")
    checked_left = _require_finite_vector(left)
    checked_right = _require_finite_vector(right)
    left_norm = math.sqrt(sum(value**2 for value in checked_left))
    right_norm = math.sqrt(sum(value**2 for value in checked_right))
    if left_norm <= 1e-15 or right_norm <= 1e-15:
        return 0.0
    return sum(a * b for a, b in zip(checked_left, checked_right)) / (
        left_norm * right_norm
    )


def _require_disjoint(partitions: dict[str, Iterable[Record]]) -> None:
    seen: dict[str, str] = {}
    for role, records in partitions.items():
        for record in records:
            group = lineage_group(record)
            prior = seen.get(group)
            if prior is not None and prior != role:
                raise ValueError(
                    f"lineage group {group!r} appears in both {prior!r} and {role!r}"
                )
            seen[group] = role


@dataclass(frozen=True)
class CentroidModel:
    labels: tuple[str, ...]
    means: tuple[float, ...]
    scales: tuple[float, ...]
    centroids: dict[str, tuple[float, ...]]
    score_semantics: str = "cosine_similarity_to_standardized_l2_centroid"


def fit_centroid_model(records: list[Record], vector_fn: VectorFn) -> CentroidModel:
    if not records:
        raise ValueError("reference records are empty")
    raw_vectors = [vector_fn(record) for record in records]
    means, scales = _fit_standardizer(raw_vectors)
    by_class: dict[str, list[list[float]]] = defaultdict(list)
    for record, vector in zip(records, raw_vectors):
        label = str(record.get("model_family") or "").strip()
        if not label:
            raise ValueError("record is missing model_family")
        by_class[label].append(_l2(_standardize(vector, means, scales)))
    centroids: dict[str, tuple[float, ...]] = {}
    for label in sorted(by_class):
        vectors = by_class[label]
        centroid = [
            fmean(vector[index] for vector in vectors)
            for index in range(len(vectors[0]))
        ]
        centroids[label] = tuple(_l2(centroid))
    return CentroidModel(
        tuple(sorted(centroids)),
        tuple(means),
        tuple(scales),
        centroids,
    )


def centroid_scores(
    model: CentroidModel,
    record: Record,
    vector_fn: VectorFn,
) -> dict[str, float]:
    vector = _l2(_standardize(vector_fn(record), model.means, model.scales))
    return {
        label: _cosine(vector, model.centroids[label]) for label in model.labels
    }


def predict_centroid(
    model: CentroidModel,
    records: Iterable[Record],
    vector_fn: VectorFn,
) -> list[str]:
    predictions: list[str] = []
    for record in records:
        scores = centroid_scores(model, record, vector_fn)
        predictions.append(
            min(model.labels, key=lambda label: (-scores[label], label))
        )
    return predictions


def evaluate_surface_baseline(
    reference: list[Record],
    test: list[Record],
) -> dict[str, Any]:
    if not reference or not test:
        raise ValueError("reference and test must be non-empty")
    _require_disjoint({"reference": reference, "test": test})
    model = fit_centroid_model(reference, surface_statistics_vector)
    truth = [str(record.get("model_family") or "").strip() for record in test]
    if any(not label for label in truth):
        raise ValueError("test record is missing model_family")
    return {
        "protocol": "challenge-001-stage-a-surface-baseline-development-v1",
        "status": "DEVELOPMENT_ONLY",
        "scientific_claim_evidence": False,
        "features": list(SURFACE_FEATURE_NAMES),
        "classifier": model.score_semantics,
        "metrics": classification_metrics(
            truth,
            predict_centroid(model, test, surface_statistics_vector),
        ),
        "raw_text_persisted": False,
    }


@dataclass(frozen=True)
class ConformalModel:
    centroid_model: CentroidModel
    alpha: float
    calibration_scores: dict[str, tuple[float, ...]]
    method: str = "class_conditional_split_conformal_on_cosine_nonconformity"


def fit_class_conditional_conformal(
    reference: list[Record],
    calibration: list[Record],
    vector_fn: VectorFn,
    *,
    alpha: float = 0.05,
) -> ConformalModel:
    alpha = float(alpha)
    if not math.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be finite and in (0,1)")
    if not reference or not calibration:
        raise ValueError("reference and conformal calibration must be non-empty")
    _require_disjoint(
        {
            "reference": reference,
            "conformal_calibration": calibration,
        }
    )
    centroid_model = fit_centroid_model(reference, vector_fn)
    by_class: dict[str, list[float]] = defaultdict(list)
    for record in calibration:
        label = str(record.get("model_family") or "").strip()
        if label not in centroid_model.labels:
            raise ValueError(
                f"calibration label {label!r} is absent from reference classes"
            )
        by_class[label].append(
            1.0 - centroid_scores(centroid_model, record, vector_fn)[label]
        )
    missing = set(centroid_model.labels) - set(by_class)
    if missing:
        raise ValueError(
            f"missing conformal calibration classes: {sorted(missing)}"
        )
    return ConformalModel(
        centroid_model,
        alpha,
        {
            label: tuple(sorted(values))
            for label, values in sorted(by_class.items())
        },
    )


def _minimum_conformal_calibration_size(alpha: float) -> int:
    return math.ceil((1.0 - alpha) / alpha)


def conformal_p_values(
    model: ConformalModel,
    record: Record,
    vector_fn: VectorFn,
) -> dict[str, float]:
    similarities = centroid_scores(model.centroid_model, record, vector_fn)
    values: dict[str, float] = {}
    for label in model.centroid_model.labels:
        calibration = model.calibration_scores.get(label, ())
        if not calibration:
            raise ValueError(f"conformal calibration scores missing for {label!r}")
        if any(not math.isfinite(value) for value in calibration):
            raise ValueError("conformal calibration scores must be finite")
        candidate = 1.0 - similarities[label]
        values[label] = (
            1.0 + sum(value >= candidate for value in calibration)
        ) / (len(calibration) + 1.0)
    return values


def conformal_decision(
    model: ConformalModel,
    record: Record,
    vector_fn: VectorFn,
    *,
    evidence_sufficient: bool = True,
) -> dict[str, Any]:
    if not isinstance(evidence_sufficient, bool):
        raise TypeError("evidence_sufficient must be a boolean")
    alpha = float(model.alpha)
    if not math.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("model alpha must be finite and in (0,1)")
    minimum_size = _minimum_conformal_calibration_size(alpha)
    undersized = sorted(
        label
        for label in model.centroid_model.labels
        if len(model.calibration_scores.get(label, ())) < minimum_size
    )
    if not evidence_sufficient or undersized:
        return {
            "decision": UNKNOWN_INSUFFICIENT_EVIDENCE,
            "p_values": {},
            "accepted_classes": [],
            "alpha": alpha,
            "calibrated_probability": False,
            "minimum_calibration_size_per_class": minimum_size,
            "undersized_calibration_classes": undersized,
        }
    p_values = conformal_p_values(model, record, vector_fn)
    accepted = sorted(
        label for label, value in p_values.items() if value > model.alpha
    )
    if len(accepted) == 1:
        decision = accepted[0]
    elif not accepted:
        decision = UNKNOWN_OOD
    else:
        decision = UNKNOWN_AMBIGUOUS
    return {
        "decision": decision,
        "p_values": p_values,
        "accepted_classes": accepted,
        "alpha": alpha,
        "calibrated_probability": False,
        "minimum_calibration_size_per_class": minimum_size,
        "undersized_calibration_classes": [],
    }


def _validate_logits(
    logits: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
) -> tuple[list[list[float]], list[str], tuple[str, ...]]:
    if any(not isinstance(label, str) for label in labels):
        raise ValueError("labels must be non-empty, unique strings")
    labels_tuple = tuple(label.strip() for label in labels)
    if (
        not labels_tuple
        or any(not label for label in labels_tuple)
        or len(set(labels_tuple)) != len(labels_tuple)
    ):
        raise ValueError("labels must be non-empty, unique strings")
    matrix = [[float(value) for value in row] for row in logits]
    truth_list = [str(value).strip() for value in truth]
    if not matrix or len(matrix) != len(truth_list):
        raise ValueError("logits and truth must be non-empty and have equal length")
    if any(len(row) != len(labels_tuple) for row in matrix):
        raise ValueError("logit width must match labels")
    if any(not label or label not in labels_tuple for label in truth_list):
        raise ValueError("truth contains a label absent from labels")
    if any(not math.isfinite(value) for row in matrix for value in row):
        raise ValueError("logits must be finite")
    return matrix, truth_list, labels_tuple


def softmax(
    logits: Sequence[float],
    *,
    temperature: float = 1.0,
) -> list[float]:
    temperature = float(temperature)
    if not math.isfinite(temperature) or not temperature > 0.0:
        raise ValueError("temperature must be finite and positive")
    values = _require_finite_vector(logits)
    if not values:
        raise ValueError("logits must be non-empty")
    scaled = [value / temperature for value in values]
    if any(not math.isfinite(value) for value in scaled):
        raise ValueError("temperature-scaled logits must be finite")
    maximum = max(scaled)
    exps = [math.exp(value - maximum) for value in scaled]
    total = sum(exps)
    return [value / total for value in exps]


def multiclass_nll(
    logits: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
    *,
    temperature: float = 1.0,
) -> float:
    matrix, truth_list, labels_tuple = _validate_logits(logits, truth, labels)
    index = {label: position for position, label in enumerate(labels_tuple)}
    return fmean(
        -math.log(
            max(
                softmax(row, temperature=temperature)[index[actual]],
                1e-15,
            )
        )
        for row, actual in zip(matrix, truth_list)
    )


def multiclass_brier(
    logits: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
    *,
    temperature: float = 1.0,
) -> float:
    matrix, truth_list, labels_tuple = _validate_logits(logits, truth, labels)
    index = {label: position for position, label in enumerate(labels_tuple)}
    values: list[float] = []
    for row, actual in zip(matrix, truth_list):
        probabilities = softmax(row, temperature=temperature)
        target = index[actual]
        values.append(
            sum(
                (probability - (1.0 if position == target else 0.0)) ** 2
                for position, probability in enumerate(probabilities)
            )
        )
    return fmean(values)


def expected_calibration_error(
    logits: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
    *,
    temperature: float = 1.0,
    bins: int = 15,
) -> float:
    matrix, truth_list, labels_tuple = _validate_logits(logits, truth, labels)
    bins = _require_positive_int(bins, "bins")
    confidence_groups: dict[float, list[int]] = defaultdict(list)
    for row, actual in zip(matrix, truth_list):
        probabilities = softmax(row, temperature=temperature)
        predicted = min(
            range(len(labels_tuple)),
            key=lambda index: (-probabilities[index], labels_tuple[index]),
        )
        confidence_groups[probabilities[predicted]].append(
            int(labels_tuple[predicted] == actual)
        )

    grouped_observations = [
        (confidence, len(outcomes), sum(outcomes))
        for confidence, outcomes in sorted(confidence_groups.items())
    ]
    total = len(matrix)
    target_size = max(1, math.ceil(total / bins))
    buckets: list[list[tuple[float, int, int]]] = []
    current: list[tuple[float, int, int]] = []
    current_size = 0
    for group in grouped_observations:
        _, group_size, _ = group
        if (
            current
            and current_size + group_size > target_size
            and len(buckets) < bins - 1
        ):
            buckets.append(current)
            current = []
            current_size = 0
        current.append(group)
        current_size += group_size
    if current:
        buckets.append(current)

    ece = 0.0
    for bucket in buckets:
        bucket_size = sum(group_size for _, group_size, _ in bucket)
        mean_confidence = sum(
            confidence * group_size
            for confidence, group_size, _ in bucket
        ) / bucket_size
        mean_accuracy = sum(correct for _, _, correct in bucket) / bucket_size
        ece += bucket_size / total * abs(mean_accuracy - mean_confidence)
    return ece


@dataclass(frozen=True)
class TemperatureCalibrationResult:
    temperature: float
    uncalibrated_nll: float
    calibrated_nll: float
    uncalibrated_brier: float
    calibrated_brier: float
    uncalibrated_ece: float
    calibrated_ece: float
    ece_bins: int
    fit_partition: str = "probability_calibration_only"
    probability_semantics: str = "temperature_scaled_softmax_development_only"


def fit_temperature(
    logits: Sequence[Sequence[float]],
    truth: Sequence[str],
    labels: Sequence[str],
    *,
    bounds: tuple[float, float] = (0.05, 20.0),
    ece_bins: int = 15,
    iterations: int = 96,
) -> TemperatureCalibrationResult:
    matrix, truth_list, labels_tuple = _validate_logits(logits, truth, labels)
    ece_bins = _require_positive_int(ece_bins, "ece_bins")
    iterations = _require_positive_int(iterations, "iterations", minimum=16)
    lower, upper = map(float, bounds)
    if (
        not math.isfinite(lower)
        or not math.isfinite(upper)
        or not 0.0 < lower < upper
    ):
        raise ValueError(
            "temperature bounds must be finite and satisfy 0 < lower < upper"
        )
    left, right = math.log(lower), math.log(upper)
    phi = (1.0 + math.sqrt(5.0)) / 2.0

    def objective(log_temperature: float) -> float:
        return multiclass_nll(
            matrix,
            truth_list,
            labels_tuple,
            temperature=math.exp(log_temperature),
        )

    c = right - (right - left) / phi
    d = left + (right - left) / phi
    fc, fd = objective(c), objective(d)
    for _ in range(iterations):
        if fc <= fd:
            right, d, fd = d, c, fc
            c = right - (right - left) / phi
            fc = objective(c)
        else:
            left, c, fc = c, d, fd
            d = left + (right - left) / phi
            fd = objective(d)
    candidates = [lower, upper, math.exp((left + right) / 2.0)]
    if lower <= 1.0 <= upper:
        candidates.append(1.0)
    temperature = min(
        candidates,
        key=lambda value: (
            multiclass_nll(
                matrix,
                truth_list,
                labels_tuple,
                temperature=value,
            ),
            value,
        ),
    )
    return TemperatureCalibrationResult(
        temperature,
        multiclass_nll(matrix, truth_list, labels_tuple),
        multiclass_nll(
            matrix,
            truth_list,
            labels_tuple,
            temperature=temperature,
        ),
        multiclass_brier(matrix, truth_list, labels_tuple),
        multiclass_brier(
            matrix,
            truth_list,
            labels_tuple,
            temperature=temperature,
        ),
        expected_calibration_error(
            matrix,
            truth_list,
            labels_tuple,
            bins=ece_bins,
        ),
        expected_calibration_error(
            matrix,
            truth_list,
            labels_tuple,
            temperature=temperature,
            bins=ece_bins,
        ),
        ece_bins,
    )
