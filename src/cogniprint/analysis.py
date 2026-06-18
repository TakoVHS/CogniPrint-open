"""Deterministic text profile analysis for local CogniPrint runs."""

from __future__ import annotations

import hashlib
import math
import re
import statistics
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .fingerprint import (
    FEATURE_NAMES,
    FINGERPRINT_VERSION,
    CognitiveFingerprint,
    feature_schema_payload,
    normalize_features,
)

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-'][A-Za-zА-Яа-яЁё0-9]+)?", re.UNICODE)
SENTENCE_RE = re.compile(r"[.!?]+")

FINGERPRINT_KEYS = FEATURE_NAMES


@dataclass(frozen=True)
class TextProfile:
    """A compact statistical profile for one text sample."""

    metrics: dict[str, float | int]
    raw_fingerprint: dict[str, float]
    fingerprint: dict[str, float]
    fingerprint_vector: list[float]
    content_hash: str
    fingerprint_version: str
    feature_schema: list[dict[str, Any]]
    normalization: dict[str, Any]


def analyze_text(text: str) -> TextProfile:
    """Compute deterministic local metrics and a fixed-order profile vector."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    words = WORD_RE.findall(normalized)
    lower_words = [word.lower() for word in words]
    word_lengths = [len(word) for word in words]
    unique_words = set(lower_words)
    frequencies = Counter(lower_words)

    char_count = len(normalized)
    non_space_count = sum(1 for char in normalized if not char.isspace())
    letter_count = sum(1 for char in normalized if char.isalpha())
    digit_count = sum(1 for char in normalized if char.isdigit())
    uppercase_count = sum(1 for char in normalized if char.isupper())
    punctuation_count = sum(1 for char in normalized if char in ".,;:!?()[]{}\"'-")
    word_count = len(words)
    sentence_count = max(1, len([part for part in SENTENCE_RE.split(normalized) if part.strip()]))
    unique_word_count = len(unique_words)
    hapax_count = sum(1 for count in frequencies.values() if count == 1)

    word_length_stddev = statistics.pstdev(word_lengths) if len(word_lengths) > 1 else 0.0
    hapax_ratio = hapax_count / word_count if word_count else 0.0
    v2 = CognitiveFingerprint(normalized)
    raw_fingerprint = v2.feature_dict()
    fingerprint = normalize_features(raw_fingerprint)

    metrics: dict[str, float | int] = {
        "char_count": char_count,
        "non_space_count": non_space_count,
        "letter_count": letter_count,
        "digit_count": digit_count,
        "punctuation_count": punctuation_count,
        "word_count": word_count,
        "unique_word_count": unique_word_count,
        "sentence_count": sentence_count if normalized.strip() else 0,
        "avg_word_length": raw_fingerprint["mean_word_length"],
        "word_length_stddev": round(word_length_stddev, 6),
        "avg_sentence_length_words": raw_fingerprint["mean_sentence_length_words"],
        "type_token_ratio": raw_fingerprint["type_token_ratio"],
        "hapax_ratio": round(hapax_ratio, 6),
        "punctuation_ratio": raw_fingerprint["punctuation_ratio"],
        "digit_ratio": raw_fingerprint["digit_token_ratio"],
        "uppercase_ratio": raw_fingerprint["uppercase_ratio"],
        "legacy_punctuation_ratio_non_space": round(punctuation_count / non_space_count, 6) if non_space_count else 0.0,
        "legacy_digit_char_ratio_non_space": round(digit_count / non_space_count, 6) if non_space_count else 0.0,
        "legacy_uppercase_ratio": round(uppercase_count / max(letter_count, 1), 6) if letter_count else 0.0,
        "mean_word_length": raw_fingerprint["mean_word_length"],
        "char_entropy": raw_fingerprint["char_entropy"],
        "word_entropy": raw_fingerprint["word_entropy"],
        "mean_syllables_per_word": raw_fingerprint["mean_syllables_per_word"],
        "char_bigram_uniqueness": raw_fingerprint["char_bigram_uniqueness"],
        "simpson_diversity": raw_fingerprint["simpson_diversity"],
        "digit_token_ratio": raw_fingerprint["digit_token_ratio"],
        "mean_sentence_length_words": raw_fingerprint["mean_sentence_length_words"],
        "flesch_reading_ease": raw_fingerprint["flesch_reading_ease"],
    }

    vector = [fingerprint[key] for key in FINGERPRINT_KEYS]
    content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return TextProfile(
        metrics=metrics,
        raw_fingerprint=raw_fingerprint,
        fingerprint=fingerprint,
        fingerprint_vector=vector,
        content_hash=content_hash,
        fingerprint_version=FINGERPRINT_VERSION,
        feature_schema=feature_schema_payload(),
        normalization={
            "method": "bounded_minmax_v1",
            "bounds_source": "cogniprint.fingerprint.FEATURE_SPECS",
            "clip": False,
        },
    )


def compare_profiles(left: TextProfile, right: TextProfile) -> dict[str, Any]:
    """Compare two profiles and return conservative distance/similarity signals."""

    left_vector = left.fingerprint_vector
    right_vector = right.fingerprint_vector
    deltas = {
        key: round(right.fingerprint[key] - left.fingerprint[key], 6)
        for key in FINGERPRINT_KEYS
    }
    return {
        "cosine_similarity": round(_cosine(left_vector, right_vector), 6),
        "cosine_distance": round(1.0 - _cosine(left_vector, right_vector), 6),
        "euclidean_distance": round(_euclidean(left_vector, right_vector), 6),
        "manhattan_distance": round(sum(abs(a - b) for a, b in zip(left_vector, right_vector)), 6),
        "delta_fingerprint": deltas,
        "observed_change": _summarize_delta(deltas),
    }


def _cosine(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def _euclidean(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def _summarize_delta(deltas: dict[str, float]) -> list[dict[str, float | str]]:
    ranked = sorted(deltas.items(), key=lambda item: abs(item[1]), reverse=True)
    return [
        {"metric": metric, "delta": delta}
        for metric, delta in ranked[:5]
        if delta != 0
    ]
