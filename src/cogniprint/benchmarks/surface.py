"""Development-only transparent surface-statistics baseline."""
from __future__ import annotations

import math
import re
import unicodedata
from collections import defaultdict
from statistics import fmean, pstdev
from typing import Any

from cogniprint.benchmarks.evaluation import classification_metrics

Record = dict[str, Any]

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


def _word_tokens(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text)
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)?", normalized, flags=re.UNICODE)


def surface_statistics_vector(record: Record) -> list[float]:
    """Return the fixed 12-feature surface vector from transient ``_text``."""

    text = record.get("_text")
    if not isinstance(text, str):
        raise ValueError("surface baseline record is missing transient _text")
    normalized = unicodedata.normalize("NFKC", text)
    tokens = _word_tokens(normalized)
    folded_tokens = [token.casefold() for token in tokens]
    word_count = len(tokens)
    letters = sum(character.isalpha() for character in normalized)
    digits = sum(character.isdigit() for character in normalized)
    uppercase = sum(character.isupper() for character in normalized)
    character_count = max(len(normalized), 1)
    sentence_marks = re.findall(r"[.!?]+", normalized)
    sentence_count = len(sentence_marks) if sentence_marks else (1 if word_count else 0)
    token_character_count = sum(
        sum(character.isalnum() for character in token) for token in tokens
    )

    return [
        float(word_count),
        float(letters),
        float(sentence_count),
        token_character_count / word_count if word_count else 0.0,
        len(set(folded_tokens)) / word_count if word_count else 0.0,
        digits / character_count,
        uppercase / letters if letters else 0.0,
        normalized.count("\n") / character_count,
        normalized.count(".") / character_count,
        normalized.count(",") / character_count,
        (normalized.count("?") + normalized.count("!")) / character_count,
        (normalized.count(":") + normalized.count(";")) / character_count,
    ]


def evaluate_surface_baseline(
    train: list[Record],
    test: list[Record],
) -> dict[str, Any]:
    """Evaluate without persisting raw text or per-document vectors."""

    if not train or not test:
        raise ValueError("train and test must be non-empty")
    truth = [str(record.get("model_family") or "") for record in test]
    if any(not label for label in truth):
        raise ValueError("test record is missing model_family")
    train_vectors = [surface_statistics_vector(record) for record in train]
    width = len(train_vectors[0])
    if any(len(vector) != width for vector in train_vectors):
        raise ValueError("inconsistent surface-vector width")
    means = [
        fmean(vector[index] for vector in train_vectors)
        for index in range(width)
    ]
    scales = [
        pstdev(vector[index] for vector in train_vectors)
        for index in range(width)
    ]
    scales = [scale if scale > 1e-12 else 1.0 for scale in scales]

    def standardized(record: Record) -> list[float]:
        raw = surface_statistics_vector(record)
        return [
            (raw[index] - means[index]) / scales[index]
            for index in range(width)
        ]

    def normalize(vector: list[float]) -> list[float]:
        norm = math.sqrt(sum(value * value for value in vector))
        if norm <= 1e-15:
            return [0.0] * len(vector)
        return [value / norm for value in vector]

    by_class: dict[str, list[list[float]]] = defaultdict(list)
    for record in train:
        label = str(record.get("model_family") or "").strip()
        if not label:
            raise ValueError("train record is missing model_family")
        by_class[label].append(normalize(standardized(record)))
    centroids = {
        label: normalize(
            [
                fmean(vector[index] for vector in vectors)
                for index in range(width)
            ]
        )
        for label, vectors in sorted(by_class.items())
    }

    predictions: list[str] = []
    for record in test:
        vector = normalize(standardized(record))
        predictions.append(
            min(
                centroids,
                key=lambda label: (
                    -sum(
                        value * centroid_value
                        for value, centroid_value in zip(
                            vector,
                            centroids[label],
                        )
                    ),
                    label,
                ),
            )
        )
    return {
        "protocol": "challenge-001-surface-development-v1",
        "readiness_boundary": "development_only",
        "feature_names": list(SURFACE_FEATURE_NAMES),
        "classifier": "standardized_cosine_nearest_centroid",
        "raw_text_persisted": False,
        "per_document_vectors_persisted": False,
        "metrics": classification_metrics(truth, predictions),
    }
