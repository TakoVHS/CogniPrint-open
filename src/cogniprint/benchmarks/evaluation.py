"""Small dependency-free baselines for the M1 model-fingerprint pilot.

These routines intentionally stop at transparent nearest-centroid baselines.
They are diagnostic tools, not a validated attribution system.
"""

from __future__ import annotations

import hashlib
import math
from collections import Counter, defaultdict
from statistics import fmean, pstdev
from typing import Any, Callable, Iterable

from cogniprint.fingerprint import FEATURE_NAMES


Record = dict[str, Any]
VectorFn = Callable[[Record], list[float]]


def lineage_group(record: Record) -> str:
    """Return a stable group key used to keep related samples in one split."""

    for key in ("source_id", "prompt_sha256", "text_sha256"):
        value = str(record.get(key) or "").strip()
        if value:
            return f"{key}:{value}"
    raise ValueError("record has no source_id, prompt_sha256, or text_sha256 for leakage-safe grouping")


def _hash_fraction(value: str, seed: int) -> float:
    digest = hashlib.sha256(f"{seed}:{value}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16) / float(0xFFFFFFFFFFFFFFFF)


def grouped_split(
    records: Iterable[Record],
    *,
    test_fraction: float = 0.30,
    seed: int = 20260725,
) -> tuple[list[Record], list[Record]]:
    """Deterministically split records while keeping lineage groups intact."""

    if not 0.0 < test_fraction < 1.0:
        raise ValueError("test_fraction must be between 0 and 1")

    train: list[Record] = []
    test: list[Record] = []
    for record in records:
        target = test if _hash_fraction(lineage_group(record), seed) < test_fraction else train
        target.append(record)

    if not train or not test:
        raise ValueError("grouped split produced an empty train or test partition")

    train_groups = {lineage_group(record) for record in train}
    test_groups = {lineage_group(record) for record in test}
    overlap = train_groups & test_groups
    if overlap:
        raise AssertionError(f"lineage leakage detected across split: {sorted(overlap)[:3]}")

    return train, test


def fingerprint_vector(record: Record) -> list[float]:
    values = record.get("features_normalized")
    if not isinstance(values, dict):
        raise ValueError("record is missing features_normalized")
    return [float(values[name]) for name in FEATURE_NAMES]


def length_vector(record: Record) -> list[float]:
    return [
        math.log1p(float(record.get("character_count") or 0.0)),
        math.log1p(float(record.get("token_count") or 0.0)),
    ]


def _fit_standardizer(vectors: list[list[float]]) -> tuple[list[float], list[float]]:
    if not vectors:
        raise ValueError("cannot fit standardizer on an empty vector set")
    width = len(vectors[0])
    if width == 0 or any(len(vector) != width for vector in vectors):
        raise ValueError("inconsistent feature-vector width")
    means = [fmean(vector[index] for vector in vectors) for index in range(width)]
    scales = [pstdev(vector[index] for vector in vectors) for index in range(width)]
    return means, [scale if scale > 1e-12 else 1.0 for scale in scales]


def _standardize(vector: list[float], means: list[float], scales: list[float]) -> list[float]:
    return [(value - means[index]) / scales[index] for index, value in enumerate(vector)]


def _centroids(
    records: list[Record],
    vector_fn: VectorFn,
) -> tuple[dict[str, list[float]], list[float], list[float]]:
    raw_vectors = [vector_fn(record) for record in records]
    means, scales = _fit_standardizer(raw_vectors)
    by_class: dict[str, list[list[float]]] = defaultdict(list)
    for record, vector in zip(records, raw_vectors):
        label = str(record.get("model_family") or "").strip()
        if not label:
            raise ValueError("record is missing model_family")
        by_class[label].append(_standardize(vector, means, scales))

    result: dict[str, list[float]] = {}
    for label, vectors in by_class.items():
        width = len(vectors[0])
        result[label] = [fmean(vector[index] for vector in vectors) for index in range(width)]
    return result, means, scales


def _euclidean(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def predict_nearest_centroid(
    train: list[Record],
    test: list[Record],
    vector_fn: VectorFn,
) -> list[str]:
    centroids, means, scales = _centroids(train, vector_fn)
    predictions: list[str] = []
    for record in test:
        vector = _standardize(vector_fn(record), means, scales)
        predictions.append(min(centroids, key=lambda label: (_euclidean(vector, centroids[label]), label)))
    return predictions


def classification_metrics(truth: list[str], predictions: list[str]) -> dict[str, Any]:
    if len(truth) != len(predictions) or not truth:
        raise ValueError("truth and predictions must be non-empty and have equal length")

    labels = sorted(set(truth) | set(predictions))
    confusion: dict[str, dict[str, int]] = {
        actual: {predicted: 0 for predicted in labels} for actual in labels
    }
    for actual, predicted in zip(truth, predictions):
        confusion[actual][predicted] += 1

    recalls: list[float] = []
    f1_values: list[float] = []
    per_class: dict[str, dict[str, float | int]] = {}
    for label in labels:
        tp = confusion[label][label]
        fn = sum(confusion[label][other] for other in labels if other != label)
        fp = sum(confusion[other][label] for other in labels if other != label)
        support = tp + fn
        recall = tp / support if support else 0.0
        precision = tp / (tp + fp) if tp + fp else 0.0
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
        recalls.append(recall)
        f1_values.append(f1)
        per_class[label] = {
            "support": support,
            "precision": round(precision, 6),
            "recall": round(recall, 6),
            "f1": round(f1, 6),
        }

    accuracy = sum(1 for actual, predicted in zip(truth, predictions) if actual == predicted) / len(truth)
    return {
        "accuracy": round(accuracy, 6),
        "balanced_accuracy": round(fmean(recalls), 6),
        "macro_f1": round(fmean(f1_values), 6),
        "per_class": per_class,
        "confusion_matrix": confusion,
    }


def _class_counts(records: Iterable[Record]) -> dict[str, int]:
    counts = Counter(str(record.get("model_family") or "") for record in records)
    counts.pop("", None)
    return dict(sorted(counts.items()))


def evaluate_pilot(
    records: list[Record],
    *,
    test_fraction: float = 0.30,
    seed: int = 20260725,
) -> dict[str, Any]:
    """Evaluate transparent first-pass baselines on a grouped deterministic split."""

    train, test = grouped_split(records, test_fraction=test_fraction, seed=seed)
    train_labels = {str(record.get("model_family") or "") for record in train}
    test_labels = {str(record.get("model_family") or "") for record in test}
    if train_labels != test_labels:
        raise ValueError(
            "train/test class sets differ after grouped split; increase pilot size or adjust the predeclared split seed"
        )

    truth = [str(record["model_family"]) for record in test]
    train_counts = Counter(str(record["model_family"]) for record in train)
    majority_label = sorted(train_counts, key=lambda label: (-train_counts[label], label))[0]
    majority_predictions = [majority_label] * len(test)

    chance = 1.0 / len(train_labels)
    return {
        "protocol": "m1-raid-pilot-baselines-v1",
        "readiness_boundary": "descriptive_only",
        "seed": seed,
        "test_fraction": test_fraction,
        "train_records": len(train),
        "test_records": len(test),
        "train_groups": len({lineage_group(record) for record in train}),
        "test_groups": len({lineage_group(record) for record in test}),
        "train_class_counts": _class_counts(train),
        "test_class_counts": _class_counts(test),
        "chance_accuracy_reference": round(chance, 6),
        "majority": classification_metrics(truth, majority_predictions),
        "length_only_nearest_centroid": classification_metrics(
            truth,
            predict_nearest_centroid(train, test, length_vector),
        ),
        "cogniprint_12d_nearest_centroid": classification_metrics(
            truth,
            predict_nearest_centroid(train, test, fingerprint_vector),
        ),
        "calibration_note": (
            "Nearest-centroid outputs are uncalibrated labels. Probability-quality metrics and abstention "
            "thresholds must be evaluated in a separate calibrated stage and are not inferred here."
        ),
    }
