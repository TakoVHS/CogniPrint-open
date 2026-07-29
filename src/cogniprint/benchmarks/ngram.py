"""Deterministic privacy-preserving hashed n-gram baselines for RAID Stage A.

The feature vocabulary and source text never leave memory. Only aggregate model
settings and classification metrics are intended for persistence.
"""
from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Iterator

from cogniprint.benchmarks.evaluation import classification_metrics

SparseVector = dict[int, float]
Record = dict[str, Any]


@dataclass(frozen=True)
class HashedNgramConfig:
    name: str
    mode: str
    min_n: int
    max_n: int
    dimensions: int
    hash_algorithm: str = "sha256"
    tf_transform: str = "1+log(count)"
    idf_transform: str = "log((1+n_train)/(1+df))+1"
    normalization: str = "l2"
    classifier: str = "cosine-nearest-centroid"

    def validate(self) -> None:
        if self.mode not in {"char", "word"}:
            raise ValueError("mode must be 'char' or 'word'")
        if self.min_n <= 0 or self.max_n < self.min_n:
            raise ValueError("invalid n-gram range")
        if self.dimensions <= 0:
            raise ValueError("dimensions must be positive")


def char_config(dimensions: int = 262_144) -> HashedNgramConfig:
    return HashedNgramConfig("character_3_5_hashed_tfidf", "char", 3, 5, dimensions)


def word_config(dimensions: int = 131_072) -> HashedNgramConfig:
    return HashedNgramConfig("word_1_2_hashed_tfidf", "word", 1, 2, dimensions)


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def word_tokens(text: str) -> list[str]:
    normalized = normalize_text(text)
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)?|\d+", normalized, flags=re.UNICODE)


def iter_ngrams(text: str, config: HashedNgramConfig) -> Iterator[str]:
    config.validate()
    if config.mode == "char":
        units: str | list[str] = normalize_text(text)
    else:
        units = word_tokens(text)
    for n in range(config.min_n, config.max_n + 1):
        if len(units) < n:
            continue
        for index in range(len(units) - n + 1):
            if config.mode == "char":
                yield str(units[index : index + n])
            else:
                yield "\x1f".join(units[index : index + n])


def hash_bucket(value: str, *, namespace: str, dimensions: int) -> int:
    digest = hashlib.sha256(f"{namespace}\0{value}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % dimensions


def hashed_counts(text: str, config: HashedNgramConfig) -> Counter[int]:
    config.validate()
    return Counter(
        hash_bucket(gram, namespace=config.name, dimensions=config.dimensions)
        for gram in iter_ngrams(text, config)
    )


def fit_idf(counts: Iterable[Counter[int]]) -> tuple[dict[int, float], float, int]:
    documents = list(counts)
    if not documents:
        raise ValueError("cannot fit IDF on an empty training set")
    document_frequency: Counter[int] = Counter()
    for vector in documents:
        document_frequency.update(vector.keys())
    n_train = len(documents)
    idf = {
        index: math.log((1.0 + n_train) / (1.0 + frequency)) + 1.0
        for index, frequency in document_frequency.items()
    }
    unseen_idf = math.log(1.0 + n_train) + 1.0
    return idf, unseen_idf, len(document_frequency)


def transform_tfidf(counts: Counter[int], idf: dict[int, float], unseen_idf: float) -> SparseVector:
    weighted = {
        index: (1.0 + math.log(count)) * idf.get(index, unseen_idf)
        for index, count in counts.items()
        if count > 0
    }
    norm = math.sqrt(sum(value * value for value in weighted.values()))
    if norm <= 0.0:
        return {}
    return {index: value / norm for index, value in weighted.items()}


def sparse_dot(left: SparseVector, right: SparseVector) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(index, 0.0) for index, value in left.items())


def fit_centroids(records: list[Record], vectors: list[SparseVector]) -> dict[str, SparseVector]:
    if len(records) != len(vectors) or not records:
        raise ValueError("records and vectors must be non-empty and equal length")
    sums: dict[str, defaultdict[int, float]] = defaultdict(lambda: defaultdict(float))
    counts: Counter[str] = Counter()
    for record, vector in zip(records, vectors):
        label = str(record.get("model_family") or "").strip()
        if not label:
            raise ValueError("record is missing model_family")
        counts[label] += 1
        for index, value in vector.items():
            sums[label][index] += value
    centroids: dict[str, SparseVector] = {}
    for label in sorted(sums):
        averaged = {index: value / counts[label] for index, value in sums[label].items()}
        norm = math.sqrt(sum(value * value for value in averaged.values()))
        centroids[label] = (
            {index: value / norm for index, value in averaged.items()} if norm > 0.0 else {}
        )
    return centroids


def predict_cosine_nearest_centroid(
    centroids: dict[str, SparseVector], vectors: Iterable[SparseVector]
) -> list[str]:
    if not centroids:
        raise ValueError("centroids are empty")
    labels = sorted(centroids)
    predictions: list[str] = []
    for vector in vectors:
        predictions.append(
            min(labels, key=lambda label: (-sparse_dot(vector, centroids[label]), label))
        )
    return predictions


def evaluate_hashed_ngram(
    train: list[Record],
    test: list[Record],
    config: HashedNgramConfig,
) -> dict[str, Any]:
    config.validate()
    if not train or not test:
        raise ValueError("train and test must be non-empty")
    train_counts = [hashed_counts(str(record.get("_text") or ""), config) for record in train]
    test_counts = [hashed_counts(str(record.get("_text") or ""), config) for record in test]
    if any(not counts for counts in train_counts + test_counts):
        raise ValueError(f"{config.name} produced an empty vector")
    idf, unseen_idf, occupied_train_bins = fit_idf(train_counts)
    train_vectors = [transform_tfidf(counts, idf, unseen_idf) for counts in train_counts]
    test_vectors = [transform_tfidf(counts, idf, unseen_idf) for counts in test_counts]
    centroids = fit_centroids(train, train_vectors)
    predictions = predict_cosine_nearest_centroid(centroids, test_vectors)
    truth = [str(record["model_family"]) for record in test]
    return {
        "config": asdict(config),
        "training_documents": len(train),
        "test_documents": len(test),
        "occupied_training_hash_bins": occupied_train_bins,
        "persisted_vocabulary": False,
        "raw_text_persisted": False,
        "metrics": classification_metrics(truth, predictions),
    }
