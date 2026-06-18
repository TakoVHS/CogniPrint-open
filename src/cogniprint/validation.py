"""Reviewer-facing validation utilities for cognitive fingerprint v2.

The functions in this module are intentionally dependency-light. They provide
baseline comparisons, random-pair contrasts, and threshold summaries without
turning CogniPrint into a classifier or raising scientific readiness.
"""

from __future__ import annotations

import hashlib
import math
import random
import re
from collections import Counter
from statistics import fmean, median
from typing import Any

from .fingerprint import FINGERPRINT_VERSION, CognitiveFingerprint

TOKEN_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+", re.UNICODE)


class SimpleTfidfBaseline:
    """Small TF-IDF cosine baseline implemented with sparse dictionaries."""

    def __init__(self, corpus_texts: list[str]) -> None:
        if not corpus_texts:
            raise ValueError("TF-IDF baseline requires at least one corpus text.")
        self.document_count = len(corpus_texts)
        document_frequencies: Counter[str] = Counter()
        for text in corpus_texts:
            document_frequencies.update(set(_tokens(text)))
        self.idf = {
            token: math.log((1 + self.document_count) / (1 + frequency)) + 1.0
            for token, frequency in document_frequencies.items()
        }

    def vector(self, text: str) -> dict[str, float]:
        tokens = _tokens(text)
        if not tokens:
            return {}
        counts = Counter(tokens)
        total = len(tokens)
        return {
            token: (count / total) * self.idf.get(token, 0.0)
            for token, count in counts.items()
        }

    def similarity(self, text_a: str, text_b: str) -> float:
        return sparse_cosine(self.vector(text_a), self.vector(text_b))


class DeterministicRandomVectorBaseline:
    """Deterministic random-vector baseline keyed by text hash."""

    def __init__(self, dim: int = 100, seed: int = 42) -> None:
        self.dim = dim
        self.seed = seed
        self._cache: dict[str, list[float]] = {}

    def vector(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if digest not in self._cache:
            local_seed = int(digest[:16], 16) ^ self.seed
            rng = random.Random(local_seed)
            values = [rng.gauss(0.0, 1.0) for _ in range(self.dim)]
            norm = math.sqrt(sum(value * value for value in values)) or 1.0
            self._cache[digest] = [value / norm for value in values]
        return self._cache[digest]

    def similarity(self, text_a: str, text_b: str) -> float:
        left = self.vector(text_a)
        right = self.vector(text_b)
        return sum(a * b for a, b in zip(left, right))


def load_texts_from_dir(path: str | Any, pattern: str = "*.txt") -> list[tuple[str, str]]:
    """Load text files recursively from a directory as ``(path, text)`` rows."""

    from pathlib import Path

    root = Path(path).expanduser().resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Corpus directory not found: {root}")
    rows = [
        (str(item), item.read_text(encoding="utf-8"))
        for item in sorted(root.rglob(pattern))
        if item.is_file()
    ]
    if not rows:
        raise ValueError(f"No corpus texts matched {pattern!r} under {root}")
    return rows


def generate_random_pair_distances(
    texts: list[str],
    *,
    metric: str = "cosine",
    n_pairs: int = 1000,
    seed: int = 42,
) -> list[float]:
    """Generate fingerprint distances between random text pairs."""

    if len(texts) < 2:
        raise ValueError("At least two corpus texts are required for random-pair distances.")
    rng = random.Random(seed)
    vectors = [CognitiveFingerprint(text).vector(normalized=True) for text in texts]
    distances: list[float] = []
    for _ in range(max(0, n_pairs)):
        left_index, right_index = rng.sample(range(len(vectors)), 2)
        distances.append(
            CognitiveFingerprint.distance(vectors[left_index], vectors[right_index], metric=metric)
        )
    return distances


def permutation_test_against_random(
    observed_distance: float,
    random_distances: list[float],
    *,
    alternative: str = "less",
    plus_one_correction: bool = True,
) -> float:
    """Empirical one-sided contrast against random-pair distances."""

    if not random_distances:
        raise ValueError("Permutation test requires at least one random distance.")
    if alternative == "less":
        count = sum(1 for distance in random_distances if distance <= observed_distance)
    elif alternative == "greater":
        count = sum(1 for distance in random_distances if distance >= observed_distance)
    else:
        center = median(random_distances)
        observed_delta = abs(observed_distance - center)
        count = sum(1 for distance in random_distances if abs(distance - center) >= observed_delta)
    if plus_one_correction:
        return (count + 1) / (len(random_distances) + 1)
    return count / len(random_distances)


def bootstrap_ci(data: list[float], *, resamples: int = 1000, ci: float = 95.0, seed: int = 42) -> dict[str, float | int]:
    """Bootstrap confidence interval for the mean of a numeric sample."""

    if not data:
        return {"count": 0, "mean": 0.0, "lower": 0.0, "upper": 0.0, "resamples": resamples}
    rng = random.Random(seed)
    means = [
        fmean(rng.choice(data) for _ in range(len(data)))
        for _ in range(max(1, resamples))
    ]
    means.sort()
    lower_index = int(((100.0 - ci) / 200.0) * (len(means) - 1))
    upper_index = int((1.0 - ((100.0 - ci) / 200.0)) * (len(means) - 1))
    return {
        "count": len(data),
        "mean": round(fmean(data), 6),
        "lower": round(means[lower_index], 6),
        "upper": round(means[upper_index], 6),
        "resamples": resamples,
    }


def cohens_d(left: list[float], right: list[float]) -> float:
    """Cohen's d for two numeric samples."""

    if len(left) < 2 or len(right) < 2:
        return 0.0
    pooled = math.sqrt((_sample_variance(left) + _sample_variance(right)) / 2.0)
    if not pooled:
        return 0.0
    return (fmean(left) - fmean(right)) / pooled


def required_sample_size_for_power(
    effect_size: float,
    *,
    power: float = 0.8,
    alpha: float = 0.05,
    one_tailed: bool = True,
) -> int | None:
    """Approximate per-group sample size for a two-sample contrast."""

    magnitude = abs(effect_size)
    if magnitude == 0:
        return None
    z_alpha = 1.6448536269514722 if one_tailed and abs(alpha - 0.05) < 1e-9 else 1.959963984540054
    z_beta = 0.8416212335729143 if abs(power - 0.8) < 1e-9 else 0.8416212335729143
    return max(2, math.ceil((2.0 * (z_alpha + z_beta) ** 2) / (magnitude**2)))


def recommend_threshold(
    perturbation_distances: list[float],
    random_distances: list[float],
    *,
    alpha: float = 0.05,
    min_power: float = 0.8,
) -> dict[str, float | None]:
    """Find an empirical threshold with bounded random-pair false-positive rate."""

    if not perturbation_distances or not random_distances:
        return {
            "recommended_threshold": None,
            "fpr_at_threshold": None,
            "power_at_threshold": None,
            "alpha": alpha,
            "min_required_power": min_power,
        }
    candidates = sorted(set(perturbation_distances + random_distances))
    best_threshold: float | None = None
    best_power = -1.0
    for threshold in candidates:
        fpr = sum(1 for distance in random_distances if distance <= threshold) / len(random_distances)
        power_value = sum(1 for distance in perturbation_distances if distance <= threshold) / len(perturbation_distances)
        if fpr <= alpha and power_value >= min_power and power_value > best_power:
            best_threshold = threshold
            best_power = power_value
    if best_threshold is None:
        best_threshold = median(perturbation_distances)
    return {
        "recommended_threshold": round(float(best_threshold), 6),
        "fpr_at_threshold": round(sum(1 for distance in random_distances if distance <= best_threshold) / len(random_distances), 6),
        "power_at_threshold": round(sum(1 for distance in perturbation_distances if distance <= best_threshold) / len(perturbation_distances), 6),
        "alpha": alpha,
        "min_required_power": min_power,
    }


def evaluate_threshold(
    perturbation_distances: list[float],
    random_distances: list[float],
    *,
    threshold: float,
) -> dict[str, float | int | None]:
    """Evaluate false-positive rate and empirical power for a fixed threshold."""

    if not perturbation_distances or not random_distances:
        return {"threshold": threshold, "fpr_at_threshold": None, "power_at_threshold": None}
    return {
        "threshold": threshold,
        "fpr_at_threshold": round(sum(1 for distance in random_distances if distance <= threshold) / len(random_distances), 6),
        "power_at_threshold": round(sum(1 for distance in perturbation_distances if distance <= threshold) / len(perturbation_distances), 6),
        "random_pair_count": len(random_distances),
        "perturbation_pair_count": len(perturbation_distances),
    }


def run_validation_suite(
    *,
    corpus_texts: list[str],
    original_text: str,
    variant_texts: list[str],
    variant_labels: list[str],
    metric: str = "cosine",
    n_permutations: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    """Build a reviewer-facing validation report for one campaign input folder."""

    original_vector = CognitiveFingerprint(original_text).vector(normalized=True)
    perturbation_distances = [
        CognitiveFingerprint.distance(
            original_vector,
            CognitiveFingerprint(text).vector(normalized=True),
            metric=metric,
        )
        for text in variant_texts
    ]
    random_distances = generate_random_pair_distances(
        corpus_texts,
        metric=metric,
        n_pairs=n_permutations,
        seed=seed,
    )
    tfidf = SimpleTfidfBaseline(corpus_texts + [original_text] + variant_texts)
    random_vector = DeterministicRandomVectorBaseline(seed=seed)
    p_values = [
        permutation_test_against_random(distance, random_distances, alternative="less")
        for distance in perturbation_distances
    ]
    effect_size = cohens_d(random_distances, perturbation_distances)
    threshold = recommend_threshold(perturbation_distances, random_distances)
    variant_results = []
    for label, text, distance, p_value in zip(variant_labels, variant_texts, perturbation_distances, p_values):
        variant_results.append(
            {
                "variant_label": label,
                "fingerprint_distance": round(distance, 6),
                "permutation_p_less_plus_one": round(p_value, 6),
                "significant_at_alpha_0_05": p_value < 0.05,
                "tfidf_cosine_similarity": round(tfidf.similarity(original_text, text), 6),
                "random_vector_similarity": round(random_vector.similarity(original_text, text), 6),
            }
        )
    return {
        "report_type": "reviewer_validation_dry_run",
        "readiness_boundary": "descriptive_only",
        "external_review_gate_satisfied": False,
        "fingerprint_version": FINGERPRINT_VERSION,
        "metric": metric,
        "seed": seed,
        "n_perturbation_pairs": len(perturbation_distances),
        "n_random_pairs": len(random_distances),
        "variant_results": variant_results,
        "perturbation_distance_summary": _summary(perturbation_distances),
        "random_distance_summary": _summary(random_distances),
        "perturbation_bootstrap_ci_95": bootstrap_ci(perturbation_distances, seed=seed),
        "effect_size_cohens_d_random_vs_perturbation": round(effect_size, 6),
        "required_sample_size_for_power_0_8": required_sample_size_for_power(effect_size),
        "threshold_recommendation": threshold,
        "fixed_threshold_0_15_evaluation": evaluate_threshold(
            perturbation_distances,
            random_distances,
            threshold=0.15,
        ),
        "random_distances_sample": [round(value, 6) for value in random_distances[:10]],
        "interpretive_note": (
            "These outputs are pre-review candidate validation aids. They do not establish "
            "authorship, provenance, AI detection, legal status, or final scientific readiness."
        ),
    }


def sparse_cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(value * right.get(token, 0.0) for token, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def _sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = fmean(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "std": None, "min": None, "max": None}
    mean = fmean(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return {
        "count": len(values),
        "mean": round(mean, 6),
        "std": round(math.sqrt(variance), 6),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
    }
