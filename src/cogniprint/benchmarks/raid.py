"""Deterministic metadata-only adapter for a small RAID pilot.

The adapter intentionally does not persist source text. It computes CogniPrint
features in memory and emits hashes plus benchmark metadata so the public repo
can contain reproducible evidence without redistributing the external corpus.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import Any, Iterable

from cogniprint.fingerprint import CognitiveFingerprint, FINGERPRINT_VERSION


DEFAULT_MODELS = ("human", "chatgpt", "gpt4", "llama-chat", "mistral-chat")
DEFAULT_DOMAINS = ("abstracts", "news", "reviews", "wiki")
REQUIRED_SOURCE_COLUMNS = (
    "id",
    "adv_source_id",
    "source_id",
    "model",
    "decoding",
    "repetition_penalty",
    "attack",
    "domain",
    "prompt",
    "generation",
)
MODEL_ALIASES = {
    "human": "human",
    "chatgpt": "chatgpt",
    "gpt4": "gpt4",
    "gpt-4": "gpt4",
    "llama-chat": "llama-chat",
    "mistral-chat": "mistral-chat",
}
DOMAIN_ALIASES = {
    "abstracts": "abstracts",
    "news": "news",
    "reviews": "reviews",
    "wiki": "wiki",
    "wikipedia": "wiki",
}
CLEAN_ATTACK_VALUES = {"", "clean", "none", "null"}


@dataclass(frozen=True)
class RaidPilotConfig:
    """Frozen selection policy for the first clean English RAID pilot."""

    models: tuple[str, ...] = DEFAULT_MODELS
    domains: tuple[str, ...] = DEFAULT_DOMAINS
    per_cell: int = 25
    model_decoding: str = "sampling"
    repetition_penalty: str = "no"
    language: str = "en"

    def target_cells(self) -> tuple[tuple[str, str], ...]:
        return tuple(product(self.models, self.domains))


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip().lower()


def canonical_model(value: Any) -> str:
    return MODEL_ALIASES.get(_clean(value), "")


def canonical_domain(value: Any) -> str:
    return DOMAIN_ALIASES.get(_clean(value), "")


def canonical_attack(value: Any) -> str:
    cleaned = _clean(value)
    return "none" if cleaned in CLEAN_ATTACK_VALUES else cleaned


def validate_source_columns(fieldnames: Iterable[str] | None) -> tuple[str, ...]:
    columns = tuple(fieldnames or ())
    return tuple(column for column in REQUIRED_SOURCE_COLUMNS if column not in columns)


def source_lineage_id(source_id: str, prompt_sha256: str | None, text_sha256: str) -> str:
    if source_id.strip():
        return f"source_id:{source_id.strip()}"
    if prompt_sha256:
        return f"prompt_sha256:{prompt_sha256}"
    return f"text_sha256:{text_sha256}"


def stable_selection_key(row: dict[str, Any], seed: int) -> str:
    parts = (
        str(seed),
        canonical_model(row.get("model")),
        canonical_domain(row.get("domain")),
        str(row.get("id") or ""),
        str(row.get("source_id") or ""),
        str(row.get("adv_source_id") or ""),
    )
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _is_clean_attack(value: Any) -> bool:
    return canonical_attack(value) == "none"


def is_eligible_row(row: dict[str, Any], config: RaidPilotConfig) -> bool:
    """Return True only for rows that match the frozen, low-confound pilot."""

    model = canonical_model(row.get("model"))
    domain = canonical_domain(row.get("domain"))
    if model not in config.models or domain not in config.domains:
        return False
    if not _is_clean_attack(row.get("attack")):
        return False

    # Human controls have no model decoding settings in RAID.
    if model == "human":
        return True

    return (
        _clean(row.get("decoding")) == config.model_decoding
        and _clean(row.get("repetition_penalty")) == config.repetition_penalty
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def feature_record(row: dict[str, Any], config: RaidPilotConfig) -> dict[str, Any]:
    """Convert one RAID row into metadata plus CogniPrint features.

    Raw generation and prompt text are deliberately omitted from the returned
    record. Their hashes are retained for lineage and reproducibility checks.
    """

    text = row.get("generation")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("RAID row is missing non-empty generation text")

    prompt = row.get("prompt")
    prompt_text = prompt if isinstance(prompt, str) else ""
    fingerprint = CognitiveFingerprint(text, language=config.language)
    text_sha256 = _sha256_text(text)
    prompt_sha256 = _sha256_text(prompt_text) if prompt_text else None
    source_id = str(row.get("source_id") or "")

    return {
        "source_dataset": "liamdugan/raid",
        "source_license": "MIT",
        "source_record_id": str(row.get("id") or ""),
        "source_id": source_id,
        "adv_source_id": str(row.get("adv_source_id") or ""),
        "lineage_id": source_lineage_id(source_id, prompt_sha256, text_sha256),
        "model_family": canonical_model(row.get("model")),
        "domain": canonical_domain(row.get("domain")),
        "decoding": _clean(row.get("decoding")),
        "repetition_penalty": _clean(row.get("repetition_penalty")),
        "attack": canonical_attack(row.get("attack")),
        "language": config.language,
        "text_sha256": text_sha256,
        "prompt_sha256": prompt_sha256,
        "character_count": len(text),
        "token_count": len(fingerprint.words),
        "fingerprint_version": FINGERPRINT_VERSION,
        "features_raw": fingerprint.feature_dict(),
        "features_normalized": fingerprint.normalized_feature_dict(),
        "readiness_boundary": "descriptive_only",
    }


def collect_records(
    rows: Iterable[dict[str, Any]],
    config: RaidPilotConfig,
    *,
    max_scanned: int | None = None,
) -> tuple[list[dict[str, Any]], int]:
    """Collect a balanced metadata-only pilot from an iterable of RAID rows."""

    targets = set(config.target_cells())
    counts: Counter[tuple[str, str]] = Counter()
    records: list[dict[str, Any]] = []
    scanned = 0

    for row in rows:
        scanned += 1
        if max_scanned is not None and scanned > max_scanned:
            break
        if not is_eligible_row(row, config):
            continue

        cell = (canonical_model(row.get("model")), canonical_domain(row.get("domain")))
        if cell not in targets or counts[cell] >= config.per_cell:
            continue

        records.append(feature_record(row, config))
        counts[cell] += 1
        if all(counts[cell] >= config.per_cell for cell in targets):
            break

    missing = {
        f"{model}/{domain}": config.per_cell - counts[(model, domain)]
        for model, domain in sorted(targets)
        if counts[(model, domain)] < config.per_cell
    }
    if missing:
        raise RuntimeError(
            "RAID pilot quotas were not satisfied; missing counts: "
            + ", ".join(f"{cell}={remaining}" for cell, remaining in missing.items())
        )

    return records, scanned


def count_cells(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for record in records:
        counts[f"{record['model_family']}/{record['domain']}"] += 1
    return dict(sorted(counts.items()))
