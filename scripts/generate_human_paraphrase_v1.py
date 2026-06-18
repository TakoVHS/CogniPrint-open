"""Generate human-paraphrase-v1 artifacts from public paraphrase datasets.

The default mode uses Hugging Face ``datasets.load_dataset`` to stream small,
bounded samples from public paraphrase corpora. The ``--use-seed-fixtures`` flag
keeps a fast no-network path for CI and smoke tests. All outputs remain
descriptive diagnostics; they do not raise readiness or establish a detector.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import fmean, median
from typing import Any, Iterable

from cogniprint.fingerprint import FINGERPRINT_VERSION, CognitiveFingerprint
from cogniprint.validation import (
    DeterministicRandomVectorBaseline,
    SimpleTfidfBaseline,
    generate_random_pair_distances,
    permutation_test_against_random,
)


SEED_PAIRS = [
    {
        "pair_id": "seed-hp-001",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "CogniPrint measures compact statistical profiles of text under a documented feature map.",
        "text_b": "CogniPrint records a compact set of text statistics using a fixed and documented feature map.",
    },
    {
        "pair_id": "seed-hp-002",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "The current evidence package remains descriptive until an external methodological review is archived.",
        "text_b": "The project should stay in a descriptive state until a non-owner methodological review is recorded.",
    },
    {
        "pair_id": "seed-hp-003",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "A dynamic threshold should be recomputed for each corpus rather than reused as a universal constant.",
        "text_b": "Thresholds need to be calibrated from the active corpus instead of treated as fixed universal values.",
    },
    {
        "pair_id": "seed-hp-004",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "PCA can summarize the covariance geometry of the twelve fingerprint coordinates on a bounded corpus.",
        "text_b": "Principal component analysis describes how the twelve coordinates vary together within the selected corpus.",
    },
    {
        "pair_id": "seed-hp-005",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "Length-stability diagnostics estimate how profile dispersion changes as text fragments become longer.",
        "text_b": "The length experiment checks whether longer fragments produce less dispersed profile vectors.",
    },
    {
        "pair_id": "seed-hp-006",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "Empirical Lipschitz diagnostics describe observed sensitivity per word edit in the available variants.",
        "text_b": "The observed Lipschitz check estimates profile movement for each token-level edit in the variants.",
    },
    {
        "pair_id": "seed-hp-007",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "TF-IDF and deterministic random vectors are useful baselines for descriptive distance comparisons.",
        "text_b": "Distance reports should include simple TF-IDF and deterministic random-vector baselines for context.",
    },
    {
        "pair_id": "seed-hp-008",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "The profile is not a final decision system and should not be interpreted as a source conclusion.",
        "text_b": "A CogniPrint vector is a research signal, not a final judgement about where a text came from.",
    },
    {
        "pair_id": "seed-hp-009",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "A reviewer bundle should contain enough data and commands to reproduce the reported diagnostics.",
        "text_b": "Review materials need to include the data and commands required to rerun the diagnostic outputs.",
    },
    {
        "pair_id": "seed-hp-010",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "External review is a governance gate, while mathematical diagnostics characterize feature behavior.",
        "text_b": "The review gate controls readiness language; the diagnostics only describe how the features behave.",
    },
    {
        "pair_id": "seed-hp-011",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "Corpus-specific calibration reduces the risk of overclaiming a threshold that only worked locally.",
        "text_b": "Calibrating on the active corpus helps avoid presenting a local threshold as generally valid.",
    },
    {
        "pair_id": "seed-hp-012",
        "pair_source": "seed_fixture_synthetic_human_like",
        "pair_type": "paraphrase",
        "source_dataset": "seed_fixture",
        "source_split": "local",
        "source_license": "repository_test_fixture",
        "text_a": "The next mathematical step is to replace seed fixtures with licensed public paraphrase data.",
        "text_b": "A stronger follow-up should swap these fixtures for a public paraphrase dataset with clear licensing.",
    },
]


SOURCE_METADATA = {
    "cointegrated": {
        "dataset": "cointegrated/ru-paraphrase-NMT-Leipzig",
        "config": None,
        "split": "test",
        "license": "CC-BY-4.0",
        "url": "https://huggingface.co/datasets/cointegrated/ru-paraphrase-NMT-Leipzig",
        "pair_source": "generated_paraphrase_round_trip_translation",
    },
    "inkoziev": {
        "dataset": "inkoziev/paraphrases",
        "config": None,
        "split": "train",
        "license": "CC-BY-NC-4.0",
        "url": "https://huggingface.co/datasets/inkoziev/paraphrases",
        "pair_source": "generated_or_curated_paraphrase_group",
    },
    "paws": {
        "dataset": "google-research-datasets/paws",
        "config": "labeled_final",
        "split": "train",
        "license": "Google Research PAWS public benchmark; freely usable per dataset documentation",
        "url": "https://huggingface.co/datasets/google-research-datasets/paws",
        "pair_source": "adversarial_paraphrase_benchmark",
    },
    "parisci": {
        "dataset": "HHousen/ParaSCI",
        "config": None,
        "split": "train",
        "license": "public Hugging Face dataset card; verify upstream license before redistribution",
        "url": "https://huggingface.co/datasets/HHousen/ParaSCI",
        "pair_source": "scientific_sentence_paraphrase",
    },
}


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pairs_path = Path(args.pairs_csv)

    if args.use_seed_fixtures:
        pairs = list(SEED_PAIRS)
        write_csv(pairs_path, pair_fieldnames(pairs), pairs)
        data_mode = "seed_fixture_test"
    elif args.use_existing_pairs:
        pairs = read_pairs(pairs_path)
        data_mode = "existing_pairs_csv"
    else:
        source_names = [item.strip() for item in args.datasets.split(",") if item.strip()]
        pairs = load_real_paraphrase_pairs(
            source_names,
            limit_per_source=args.limit_per_source,
            min_tokens=args.min_tokens,
            seed=args.seed,
        )
        if not pairs:
            raise SystemExit("No public paraphrase pairs were loaded.")
        write_csv(pairs_path, pair_fieldnames(pairs), pairs)
        data_mode = "real_public_or_generated_dataset"

    corpus_texts = load_corpus_texts(Path(args.corpus_dir))
    corpus_texts.extend(row["text_a"] for row in pairs)
    corpus_texts.extend(row["text_b"] for row in pairs)
    corpus_texts = [text for text in corpus_texts if text.strip()]
    if len(corpus_texts) < 2:
        raise SystemExit("Need at least two texts for random-pair calibration.")

    random_euclidean = generate_random_pair_distances(
        corpus_texts,
        metric="euclidean",
        n_pairs=args.random_pairs,
        seed=args.seed,
    )
    random_cosine = generate_random_pair_distances(
        corpus_texts,
        metric="cosine",
        n_pairs=args.random_pairs,
        seed=args.seed,
    )
    tfidf = SimpleTfidfBaseline(corpus_texts)
    random_vector = DeterministicRandomVectorBaseline(seed=args.seed)

    results = []
    for row in pairs:
        left = CognitiveFingerprint(row["text_a"]).vector(normalized=True)
        right = CognitiveFingerprint(row["text_b"]).vector(normalized=True)
        euclidean_distance = CognitiveFingerprint.distance(left, right, metric="euclidean")
        cosine_distance = CognitiveFingerprint.distance(left, right, metric="cosine")
        results.append(
            {
                "pair_id": row["pair_id"],
                "pair_source": row["pair_source"],
                "pair_type": row["pair_type"],
                "source_dataset": row["source_dataset"],
                "source_split": row["source_split"],
                "source_license": row["source_license"],
                "text_a_tokens": token_count(row["text_a"]),
                "text_b_tokens": token_count(row["text_b"]),
                "euclidean_distance": round(euclidean_distance, 6),
                "cosine_similarity": round(1.0 - cosine_distance, 6),
                "cosine_distance": round(cosine_distance, 6),
                "p_value_euclidean_less_plus_one": round(
                    permutation_test_against_random(euclidean_distance, random_euclidean, alternative="less"),
                    6,
                ),
                "p_value_cosine_less_plus_one": round(
                    permutation_test_against_random(cosine_distance, random_cosine, alternative="less"),
                    6,
                ),
                "tfidf_cosine_distance": round(1.0 - tfidf.similarity(row["text_a"], row["text_b"]), 6),
                "random_vector_distance": round(1.0 - random_vector.similarity(row["text_a"], row["text_b"]), 6),
            }
        )

    write_csv(output_dir / "results.csv", list(results[0].keys()), results)
    random_rows = [
        {"pair_type": "random_corpus_pair", "metric": "euclidean_distance", "distance": round(value, 6)}
        for value in random_euclidean
    ] + [
        {"pair_type": "random_corpus_pair", "metric": "cosine_distance", "distance": round(value, 6)}
        for value in random_cosine
    ]
    write_csv(output_dir / "random-pair-distances.csv", ["pair_type", "metric", "distance"], random_rows)

    summary = {
        "snapshot_id": "human-paraphrase-v1",
        "status": (
            "real public/generated paraphrase diagnostic"
            if not args.use_seed_fixtures
            else "seed fixture diagnostic for CI only"
        ),
        "data_mode": data_mode,
        "readiness_boundary": "descriptive_only",
        "external_review_gate_satisfied": False,
        "fingerprint_version": FINGERPRINT_VERSION,
        "pair_count": len(results),
        "pair_source_counts": dict(Counter(row["pair_source"] for row in results)),
        "source_dataset_counts": dict(Counter(row["source_dataset"] for row in results)),
        "source_license_notes": sorted({row["source_license"] for row in pairs}),
        "random_pair_count": len(random_euclidean),
        "euclidean_distance_summary": numeric_summary([row["euclidean_distance"] for row in results]),
        "cosine_distance_summary": numeric_summary([row["cosine_distance"] for row in results]),
        "tfidf_cosine_distance_summary": numeric_summary([row["tfidf_cosine_distance"] for row in results]),
        "random_euclidean_summary": numeric_summary(random_euclidean),
        "random_cosine_summary": numeric_summary(random_cosine),
        "significant_euclidean_p_lt_0_05_count": sum(1 for row in results if row["p_value_euclidean_less_plus_one"] < 0.05),
        "guardrail": (
            "Generated paraphrase datasets are marked as generated_paraphrase where applicable. "
            "These outputs describe profile behavior on the selected corpora and do not establish validation, "
            "source identity, or universal thresholds."
        ),
    }
    write_json(output_dir / "summary.json", summary)
    write_svg_distribution(
        output_dir / "distribution.svg",
        paraphrase_values=[row["euclidean_distance"] for row in results],
        random_values=random_euclidean,
        title="human-paraphrase-v1 Euclidean distance diagnostic",
        paraphrase_label="public/generated paraphrase",
    )
    write_readme(output_dir, pairs_path, summary, args)
    print(f"Human paraphrase v1 diagnostics written: {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs-csv", default="validation/human-paraphrase-v1/pairs.csv")
    parser.add_argument("--corpus-dir", default="datasets/public-benchmark-v1.1/raw")
    parser.add_argument("--output-dir", default="validation/human-paraphrase-v1")
    parser.add_argument("--datasets", default="cointegrated,inkoziev,paws")
    parser.add_argument("--limit-per-source", type=int, default=40)
    parser.add_argument("--min-tokens", type=int, default=5)
    parser.add_argument("--random-pairs", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--use-existing-pairs", action="store_true")
    parser.add_argument("--use-seed-fixtures", action="store_true")
    return parser.parse_args()


def load_real_paraphrase_pairs(
    source_names: list[str],
    *,
    limit_per_source: int,
    min_tokens: int,
    seed: int,
) -> list[dict[str, str]]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit(
            "Real paraphrase mode requires the Hugging Face datasets package. "
            "Run: .venv/bin/pip install -e '.[real-data]'"
        ) from exc

    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    _ = seed
    for source_name in source_names:
        if source_name not in SOURCE_METADATA:
            raise SystemExit(f"Unknown paraphrase source {source_name!r}; choose from {sorted(SOURCE_METADATA)}")
        source = SOURCE_METADATA[source_name]
        dataset_kwargs: dict[str, Any] = {"split": source["split"], "streaming": True}
        if source["config"]:
            dataset = load_dataset(source["dataset"], source["config"], **dataset_kwargs)
        else:
            dataset = load_dataset(source["dataset"], **dataset_kwargs)
        source_count = 0
        for pair in iter_source_pairs(source_name, dataset, min_tokens=min_tokens):
            key = (pair["source_dataset"], pair["text_a"], pair["text_b"])
            if key in seen:
                continue
            seen.add(key)
            pair["pair_id"] = f"{source_name}-{len(rows) + 1:05d}"
            rows.append(pair)
            source_count += 1
            if source_count >= limit_per_source:
                break
    return rows


def iter_source_pairs(source_name: str, dataset: Iterable[dict[str, Any]], *, min_tokens: int) -> Iterable[dict[str, str]]:
    source = SOURCE_METADATA[source_name]
    if source_name == "cointegrated":
        for example in dataset:
            text_a = clean_text(str(example.get("original", "")))
            text_b = clean_text(str(example.get("ru", "")))
            if not valid_pair(text_a, text_b, min_tokens=min_tokens):
                continue
            yield base_pair(source, text_a, text_b, pair_type="generated_paraphrase")
    elif source_name == "inkoziev":
        for example in dataset:
            paraphrases = [clean_text(str(item)) for item in example.get("paraphrases", [])]
            paraphrases = [item for item in paraphrases if token_count(item) >= min_tokens]
            if len(paraphrases) < 2:
                continue
            anchor = paraphrases[0]
            for candidate in paraphrases[1:]:
                if valid_pair(anchor, candidate, min_tokens=min_tokens):
                    yield base_pair(source, anchor, candidate, pair_type="generated_or_curated_paraphrase")
    elif source_name == "paws":
        for example in dataset:
            if int(example.get("label", 0)) != 1:
                continue
            text_a = clean_text(str(example.get("sentence1", "")))
            text_b = clean_text(str(example.get("sentence2", "")))
            if valid_pair(text_a, text_b, min_tokens=min_tokens):
                yield base_pair(source, text_a, text_b, pair_type="adversarial_paraphrase")
    elif source_name == "parisci":
        for example in dataset:
            text_a = clean_text(str(example.get("sentence1", "")))
            text_b = clean_text(str(example.get("sentence2", "")))
            if valid_pair(text_a, text_b, min_tokens=min_tokens):
                yield base_pair(source, text_a, text_b, pair_type="scientific_paraphrase")


def base_pair(source: dict[str, str], text_a: str, text_b: str, *, pair_type: str) -> dict[str, str]:
    return {
        "pair_id": "",
        "pair_source": source["pair_source"],
        "pair_type": pair_type,
        "source_dataset": source["dataset"],
        "source_split": source["split"],
        "source_license": source["license"],
        "text_a": text_a,
        "text_b": text_b,
    }


def clean_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if ("Ð" in value or "Ñ" in value or "Â" in value) and not any("а" <= char.lower() <= "я" for char in value):
        try:
            repaired = value.encode("latin-1").decode("utf-8")
            if repaired.count("�") <= value.count("�"):
                value = repaired
        except UnicodeError:
            pass
    return " ".join(value.split())


def valid_pair(text_a: str, text_b: str, *, min_tokens: int) -> bool:
    return text_a != text_b and token_count(text_a) >= min_tokens and token_count(text_b) >= min_tokens


def token_count(text: str) -> int:
    return len([part for part in text.split() if part.strip()])


def read_pairs(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"pair_id", "pair_source", "pair_type", "text_a", "text_b"}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise SystemExit(f"Missing required pair columns in {path}: {sorted(missing)}")
    for row in rows:
        row.setdefault("source_dataset", "unknown")
        row.setdefault("source_split", "unknown")
        row.setdefault("source_license", "unknown")
    return rows


def load_corpus_texts(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [item.read_text(encoding="utf-8") for item in sorted(path.glob("*.txt")) if item.is_file()]


def numeric_summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": round(fmean(values), 6),
        "median": round(median(values), 6),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
    }


def pair_fieldnames(rows: list[dict[str, str]]) -> list[str]:
    preferred = [
        "pair_id",
        "pair_source",
        "pair_type",
        "source_dataset",
        "source_split",
        "source_license",
        "text_a",
        "text_b",
    ]
    extra = sorted({key for row in rows for key in row} - set(preferred))
    return preferred + extra


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_svg_distribution(
    path: Path,
    *,
    paraphrase_values: list[float],
    random_values: list[float],
    title: str,
    paraphrase_label: str,
) -> None:
    width = 760
    height = 360
    left = 120
    right = 40
    top = 48
    bottom = 54
    max_value = max(paraphrase_values + random_values + [1e-9])

    def x(value: float) -> float:
        return left + (value / max_value) * (width - left - right)

    def row(values: list[float], y: int, color: str) -> str:
        if not values:
            return ""
        ordered = sorted(values)
        q1 = percentile(ordered, 0.25)
        q2 = percentile(ordered, 0.50)
        q3 = percentile(ordered, 0.75)
        low = min(ordered)
        high = max(ordered)
        dots = []
        for index, value in enumerate(ordered):
            jitter = ((index % 7) - 3) * 2
            dots.append(f'<circle cx="{x(value):.2f}" cy="{y + jitter}" r="2.4" fill="{color}" opacity="0.45"/>')
        return "\n".join(
            [
                f'<line x1="{x(low):.2f}" y1="{y}" x2="{x(high):.2f}" y2="{y}" stroke="{color}" stroke-width="1"/>',
                f'<rect x="{x(q1):.2f}" y="{y - 16}" width="{max(1.0, x(q3) - x(q1)):.2f}" height="32" fill="{color}" opacity="0.14" stroke="{color}"/>',
                f'<line x1="{x(q2):.2f}" y1="{y - 20}" x2="{x(q2):.2f}" y2="{y + 20}" stroke="{color}" stroke-width="2"/>',
                *dots,
            ]
        )

    axis = []
    for tick in range(6):
        value = max_value * tick / 5
        xpos = x(value)
        axis.append(f'<line x1="{xpos:.2f}" y1="{height - bottom}" x2="{xpos:.2f}" y2="{height - bottom + 6}" stroke="#999"/>')
        axis.append(f'<text x="{xpos:.2f}" y="{height - bottom + 24}" text-anchor="middle" font-size="11" fill="#555">{value:.2f}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  <text x="{left}" y="28" font-size="16" font-family="Arial, sans-serif">{title}</text>
  <text x="{left - 12}" y="{top + 85}" text-anchor="end" font-size="12" font-family="Arial, sans-serif">{paraphrase_label}</text>
  <text x="{left - 12}" y="{top + 185}" text-anchor="end" font-size="12" font-family="Arial, sans-serif">random corpus</text>
  {row(paraphrase_values, top + 80, "#111")}
  {row(random_values, top + 180, "#777")}
  <line x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" stroke="#bbb"/>
  {''.join(axis)}
  <text x="{(width + left - right) / 2:.2f}" y="{height - 12}" text-anchor="middle" font-size="12" fill="#555" font-family="Arial, sans-serif">Euclidean profile distance</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def percentile(ordered: list[float], q: float) -> float:
    if not ordered:
        return 0.0
    index = (len(ordered) - 1) * q
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[int(index)]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def write_readme(output_dir: Path, pairs_path: Path, summary: dict[str, Any], args: argparse.Namespace) -> None:
    source_lines = "\n".join(
        f"- `{key}`: {meta['dataset']} ({meta['license']}) - {meta['url']}"
        for key, meta in SOURCE_METADATA.items()
    )
    text = f"""# Human Paraphrase V1

Status: descriptive mathematical diagnostic.
Readiness boundary: `descriptive_only`.

This folder implements the human-paraphrase experiment pipeline. The default
real-data command streams bounded samples from public Hugging Face datasets via
`datasets.load_dataset`. The explicit `--use-seed-fixtures` mode is only for
fast CI/smoke tests.

## Dataset Sources

{source_lines}

Generated or machine-assisted sources are marked in `pair_source`; they are not
described as independently written human paraphrases.

## Reproduction

```bash
make human-paraphrase-real
make human-paraphrase-test
```

Equivalent direct command:

```bash
PYTHONPATH=src .venv/bin/python scripts/generate_human_paraphrase_v1.py \\
  --datasets {args.datasets} \\
  --limit-per-source {args.limit_per_source} \\
  --random-pairs {args.random_pairs}
```

## Inputs

- pair file: `{pairs_path}`
- pair count: {summary["pair_count"]}
- pair sources: `{summary["pair_source_counts"]}`
- source datasets: `{summary["source_dataset_counts"]}`
- source license notes: `{summary["source_license_notes"]}`
- random-pair count: {summary["random_pair_count"]}

## Outputs

- `pairs.csv`
- `results.csv`
- `random-pair-distances.csv`
- `summary.json`
- `distribution.svg`

## Current Diagnostic Summary

- mean pair Euclidean distance: {summary["euclidean_distance_summary"]["mean"]}
- median pair Euclidean distance: {summary["euclidean_distance_summary"]["median"]}
- mean random-pair Euclidean distance: {summary["random_euclidean_summary"]["mean"]}
- Euclidean p<0.05 count: {summary["significant_euclidean_p_lt_0_05_count"]}

## Boundary

These outputs do not establish validation, author identity, text origin,
AI-origin, legal status, forensic status, or a universal threshold.
"""
    (output_dir / "README.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
