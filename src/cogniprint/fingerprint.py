"""Cognitive fingerprint v2 feature map.

This module defines a compact, deterministic statistical profile for text.
It is intentionally dependency-light and uses only the Python standard library
so the research workstation remains easy to reproduce in reviewer settings.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from statistics import fmean
from typing import Any

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-'][A-Za-zА-Яа-яЁё0-9]+)?", re.UNICODE)
SENTENCE_RE = re.compile(r"[.!?;:]+")
PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)

RUSSIAN_VOWELS = set("аеёиоуыэюя")
ENGLISH_VOWELS = set("aeiouy")

DEFAULT_STOP_WORDS = {
    "ru": {
        "и",
        "в",
        "во",
        "не",
        "на",
        "с",
        "со",
        "а",
        "но",
        "или",
        "что",
        "это",
        "как",
        "к",
        "по",
        "для",
        "из",
        "у",
        "за",
    },
    "en": {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    },
}


@dataclass(frozen=True)
class FeatureSpec:
    """Document one coordinate in the v2 cognitive fingerprint."""

    name: str
    description: str
    minimum: float
    maximum: float


FEATURE_SPECS: tuple[FeatureSpec, ...] = (
    FeatureSpec("mean_word_length", "Mean word length in characters.", 2.0, 10.0),
    FeatureSpec("type_token_ratio", "Unique word ratio over token count.", 0.1, 1.0),
    FeatureSpec("char_entropy", "Shannon entropy of character distribution in bits.", 1.0, 5.0),
    FeatureSpec("word_entropy", "Shannon entropy of word distribution in bits.", 2.0, 10.0),
    FeatureSpec("punctuation_ratio", "Punctuation mark count over character count.", 0.0, 0.3),
    FeatureSpec("uppercase_ratio", "Uppercase alphabetic count over alphabetic count.", 0.0, 0.8),
    FeatureSpec("mean_syllables_per_word", "Mean simplified syllable count per word.", 1.0, 3.0),
    FeatureSpec("char_bigram_uniqueness", "Unique character bigram ratio.", 0.1, 0.9),
    FeatureSpec("simpson_diversity", "One minus Simpson dominance over word tokens.", 0.1, 0.95),
    FeatureSpec("digit_token_ratio", "Numeric token count over token count.", 0.0, 0.5),
    FeatureSpec("mean_sentence_length_words", "Mean sentence length in word tokens.", 3.0, 30.0),
    FeatureSpec("flesch_reading_ease", "Russian-adapted Flesch reading ease, clipped to 0..100.", 20.0, 90.0),
)

FEATURE_NAMES = [spec.name for spec in FEATURE_SPECS]
FINGERPRINT_VERSION = "cognitive-fingerprint-v2.0"


class CognitiveFingerprint:
    """Compact statistical profile of text under a documented feature map."""

    def __init__(self, text: str, language: str = "ru") -> None:
        self.raw_text = text.strip()
        self.language = language
        self.text = self.raw_text.replace("\r\n", "\n").replace("\r", "\n")
        self.sentences = [part.strip() for part in SENTENCE_RE.split(self.text) if part.strip()]
        self.words = WORD_RE.findall(self.text.lower())
        self.chars = list(self.text)

    def mean_word_length(self) -> float:
        return fmean([len(word) for word in self.words]) if self.words else 0.0

    def type_token_ratio(self) -> float:
        return len(set(self.words)) / len(self.words) if self.words else 0.0

    def char_entropy(self) -> float:
        return _entropy(self.chars)

    def word_entropy(self) -> float:
        return _entropy(self.words)

    def punctuation_ratio(self) -> float:
        if not self.chars:
            return 0.0
        return len(PUNCT_RE.findall(self.text)) / len(self.chars)

    def uppercase_ratio(self) -> float:
        letters = [char for char in self.raw_text if char.isalpha()]
        if not letters:
            return 0.0
        return sum(1 for char in letters if char.isupper()) / len(letters)

    def mean_syllables_per_word(self) -> float:
        if not self.words:
            return 0.0
        vowels = RUSSIAN_VOWELS | ENGLISH_VOWELS
        counts = [max(1, sum(1 for char in word.lower() if char in vowels)) for word in self.words]
        return fmean(counts)

    def char_bigram_uniqueness(self) -> float:
        if len(self.chars) < 2:
            return 1.0
        bigrams = [self.chars[index] + self.chars[index + 1] for index in range(len(self.chars) - 1)]
        return len(set(bigrams)) / len(bigrams)

    def simpson_diversity(self) -> float:
        if not self.words:
            return 1.0
        count_by_word = Counter(self.words)
        n = len(self.words)
        if n <= 1:
            return 1.0
        dominance = sum(count * (count - 1) for count in count_by_word.values()) / (n * (n - 1))
        return 1.0 - dominance

    def digit_token_ratio(self) -> float:
        return sum(1 for word in self.words if word.isdigit()) / len(self.words) if self.words else 0.0

    def mean_sentence_length_words(self) -> float:
        if not self.sentences:
            return 0.0
        lengths = [len(WORD_RE.findall(sentence)) for sentence in self.sentences]
        return fmean(lengths) if lengths else 0.0

    def flesch_reading_ease(self) -> float:
        if not self.sentences or not self.words:
            return 0.0
        words_per_sentence = len(self.words) / len(self.sentences)
        syllables_per_word = self.mean_syllables_per_word()
        score = 206.835 - 1.3 * words_per_sentence - 60.1 * syllables_per_word
        return min(100.0, max(0.0, score))

    def feature_dict(self) -> dict[str, float]:
        """Return raw v2 feature coordinates in stable order."""

        values = {
            "mean_word_length": self.mean_word_length(),
            "type_token_ratio": self.type_token_ratio(),
            "char_entropy": self.char_entropy(),
            "word_entropy": self.word_entropy(),
            "punctuation_ratio": self.punctuation_ratio(),
            "uppercase_ratio": self.uppercase_ratio(),
            "mean_syllables_per_word": self.mean_syllables_per_word(),
            "char_bigram_uniqueness": self.char_bigram_uniqueness(),
            "simpson_diversity": self.simpson_diversity(),
            "digit_token_ratio": self.digit_token_ratio(),
            "mean_sentence_length_words": self.mean_sentence_length_words(),
            "flesch_reading_ease": self.flesch_reading_ease(),
        }
        return {name: round(float(values[name]), 6) for name in FEATURE_NAMES}

    def vector(self, *, normalized: bool = True) -> list[float]:
        features = self.feature_dict()
        if normalized:
            features = normalize_features(features)
        return [features[name] for name in FEATURE_NAMES]

    def normalized_feature_dict(self) -> dict[str, float]:
        """Return normalized v2 feature coordinates in stable order."""

        return normalize_features(self.feature_dict())

    @staticmethod
    def distance(left: list[float], right: list[float], metric: str = "cosine") -> float:
        if metric == "cosine":
            return 1.0 - cosine_similarity(left, right)
        if metric == "euclidean":
            return euclidean_distance(left, right)
        raise ValueError(f"Unknown metric: {metric}")


def normalize_features(
    features: dict[str, float],
    ref_stats: dict[str, tuple[float, float]] | None = None,
) -> dict[str, float]:
    """Normalize feature coordinates using corpus z-stats or fixed v2 bounds."""

    normalized: dict[str, float] = {}
    for spec in FEATURE_SPECS:
        value = float(features.get(spec.name, 0.0))
        if ref_stats and spec.name in ref_stats:
            mean, stddev = ref_stats[spec.name]
            normalized[spec.name] = (value - mean) / (stddev + 1e-12)
        else:
            normalized[spec.name] = (value - spec.minimum) / (spec.maximum - spec.minimum + 1e-12)
    return {name: round(value, 6) for name, value in normalized.items()}


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norm = math.sqrt(sum(a * a for a in left)) * math.sqrt(sum(b * b for b in right))
    if not norm:
        return 0.0
    return dot / norm


def euclidean_distance(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def perturb_stability_test(
    original_text: str,
    perturbed_texts: list[str],
    *,
    metric: str = "cosine",
    threshold: float | None = None,
    language: str = "ru",
) -> dict[str, Any]:
    """Compare one baseline profile against controlled perturbation variants."""

    original = CognitiveFingerprint(original_text, language=language).vector(normalized=True)
    distances = [
        CognitiveFingerprint.distance(
            original,
            CognitiveFingerprint(text, language=language).vector(normalized=True),
            metric=metric,
        )
        for text in perturbed_texts
    ]
    mean_distance = fmean(distances) if distances else 0.0
    return {
        "fingerprint_version": FINGERPRINT_VERSION,
        "metric": metric,
        "variant_count": len(distances),
        "sample_count": len(distances),
        "mean_distance": round(mean_distance, 6),
        "std_distance": round(_population_stddev(distances), 6),
        "max_distance": round(max(distances), 6) if distances else 0.0,
        "threshold": threshold,
        "threshold_passed": (mean_distance < threshold if threshold is not None and distances else None),
        "threshold_note": (
            "No fixed stability threshold is validated. Supply an explicit threshold only for "
            "local diagnostics, and prefer corpus-specific random-pair calibration for interpretation."
        ),
        "readiness_boundary": "descriptive_only",
        "interpretive_note": (
            "This stability summary is a reproducible research signal, not a validation claim "
            "or final decision about text origin, authorship, or legal status."
        ),
        "distances": [round(distance, 6) for distance in distances],
    }


def apply_synonym_replacements(text: str, replacements: dict[str, str]) -> str:
    """Apply deterministic token replacements supplied by the caller."""

    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return replacements.get(token.lower(), token)

    return WORD_RE.sub(replace, text)


def rotate_sentences(text: str, offset: int = 1) -> str:
    sentences = [sentence.strip() for sentence in SENTENCE_RE.split(text) if sentence.strip()]
    if len(sentences) <= 1:
        return text
    offset = offset % len(sentences)
    return ". ".join(sentences[offset:] + sentences[:offset]) + "."


def remove_stop_words(text: str, *, language: str = "ru", stop_words: set[str] | None = None) -> str:
    blocked = stop_words if stop_words is not None else DEFAULT_STOP_WORDS.get(language, set())
    return " ".join(token for token in WORD_RE.findall(text) if token.lower() not in blocked)


def feature_schema_payload() -> list[dict[str, Any]]:
    return [
        {
            "name": spec.name,
            "description": spec.description,
            "normalization_min": spec.minimum,
            "normalization_max": spec.maximum,
        }
        for spec in FEATURE_SPECS
    ]


def _entropy(items: list[str]) -> float:
    if not items:
        return 0.0
    counts = Counter(items)
    total = len(items)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def _population_stddev(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = fmean(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))
