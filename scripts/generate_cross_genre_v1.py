"""Generate cross-genre-v1 diagnostic artifacts.

Default real-data mode consumes a PAN15-derived corpus CSV prepared by
``scripts/prepare_cross_genre_data.py``. The ``--use-seed-fixtures`` mode keeps
fast CI coverage without network access. Outputs remain descriptive diagnostics.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from statistics import fmean, median
from typing import Any

from cogniprint.fingerprint import FINGERPRINT_VERSION, CognitiveFingerprint


SEED_CORPUS = [
    {
        "text_id": "seed-cg-a01-research",
        "author_id": "seed-author-a",
        "genre": "research_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "The analysis describes a bounded feature map, a reproducible corpus, and diagnostic thresholds calibrated from random pairs.",
    },
    {
        "text_id": "seed-cg-a01-blog",
        "author_id": "seed-author-a",
        "genre": "blog_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "I keep returning to the same rule: measure carefully, name the limits, and avoid turning a metric into a verdict.",
    },
    {
        "text_id": "seed-cg-a01-letter",
        "author_id": "seed-author-a",
        "genre": "letter",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "Thank you for reviewing the evidence package. The project is intentionally narrow and every stronger claim is deferred.",
    },
    {
        "text_id": "seed-cg-b01-research",
        "author_id": "seed-author-b",
        "genre": "research_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "This report estimates covariance structure, observed profile displacement, and descriptive separation between corpus contrasts.",
    },
    {
        "text_id": "seed-cg-b01-blog",
        "author_id": "seed-author-b",
        "genre": "blog_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "A useful experiment is modest: define the comparison, run the same code twice, and keep the conclusion smaller than the data.",
    },
    {
        "text_id": "seed-cg-b01-letter",
        "author_id": "seed-author-b",
        "genre": "letter",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "I am sending the current diagnostic files for inspection. They should be treated as reproducibility material only.",
    },
    {
        "text_id": "seed-cg-c01-research",
        "author_id": "seed-author-c",
        "genre": "research_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "The method computes lexical diversity, entropy, sentence length, and simplified readability in a fixed coordinate system.",
    },
    {
        "text_id": "seed-cg-c01-blog",
        "author_id": "seed-author-c",
        "genre": "blog_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "When a profile changes after rewriting, the interesting question is how much changed and under which preprocessing assumptions.",
    },
    {
        "text_id": "seed-cg-c01-letter",
        "author_id": "seed-author-c",
        "genre": "letter",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "Please read the attached limitations first. They explain which uses are outside the current mathematical evidence base.",
    },
    {
        "text_id": "seed-cg-d01-research",
        "author_id": "seed-author-d",
        "genre": "research_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "Random baselines, TF-IDF distances, and profile geometry provide complementary diagnostics for corpus-specific behavior.",
    },
    {
        "text_id": "seed-cg-d01-blog",
        "author_id": "seed-author-d",
        "genre": "blog_note",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "A dashboard can be elegant, but the real work is the audit trail: inputs, outputs, checksums, and limits.",
    },
    {
        "text_id": "seed-cg-d01-letter",
        "author_id": "seed-author-d",
        "genre": "letter",
        "corpus_source": "seed_fixture_cross_genre",
        "text": "The next revision should keep the same boundary language while improving the stress tests across genres.",
    },
]


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    corpus_path = Path(args.corpus_csv)

    if args.use_seed_fixtures:
        write_csv(corpus_path, corpus_fieldnames(SEED_CORPUS), SEED_CORPUS)
        data_mode = "seed_fixture_test"
    elif not corpus_path.exists():
        raise SystemExit(
            f"Corpus CSV not found: {corpus_path}. "
            "Run `make cross-genre-real` or `python scripts/prepare_cross_genre_data.py` first."
        )
    else:
        data_mode = "real_public_pan15"

    corpus = read_corpus(corpus_path)
    rows = build_pair_rows(corpus, max_pairs=args.max_pairs)
    if not rows:
        raise SystemExit("No cross-genre pair rows could be built from corpus.csv")
    write_csv(output_dir / "results.csv", list(rows[0].keys()), rows)

    within = [row["euclidean_distance"] for row in rows if row["pair_type"] == "within_author_cross_genre"]
    controls = [row["euclidean_distance"] for row in rows if row["pair_type"].startswith("inter_author")]
    permutation = permutation_mean_gap(within, controls, permutations=args.permutations, seed=args.seed)
    summary = {
        "snapshot_id": "cross-genre-v1",
        "status": "PAN15-derived public corpus diagnostic" if data_mode == "real_public_pan15" else "seed fixture diagnostic for CI only",
        "data_mode": data_mode,
        "readiness_boundary": "descriptive_only",
        "external_review_gate_satisfied": False,
        "fingerprint_version": FINGERPRINT_VERSION,
        "text_count": len(corpus),
        "author_count": len({row["author_id"] for row in corpus}),
        "genre_count": len({row["genre"] for row in corpus}),
        "corpus_source_counts": dict(Counter(row["corpus_source"] for row in corpus)),
        "source_license_notes": sorted({row.get("source_license", "unknown") for row in corpus}),
        "within_author_cross_genre_count": len(within),
        "inter_author_control_count": len(controls),
        "inter_author_same_genre_count": sum(1 for row in rows if row["pair_type"] == "inter_author_same_genre"),
        "inter_author_cross_genre_control_count": sum(1 for row in rows if row["pair_type"] == "inter_author_cross_genre_control"),
        "within_author_cross_genre_euclidean_summary": numeric_summary(within),
        "inter_author_control_euclidean_summary": numeric_summary(controls),
        "inter_author_same_genre_euclidean_summary": numeric_summary(
            [row["euclidean_distance"] for row in rows if row["pair_type"] == "inter_author_same_genre"]
        ),
        "permutation_mean_gap": permutation,
        "guardrail": (
            "PAN15 rows are author-verification problem documents. Dutch and Spanish problem prefixes are used as "
            "cross-genre verification stress tests. The output is a descriptive contrast, not a source or author conclusion."
        ),
    }
    write_json(output_dir / "summary.json", summary)
    write_svg_distribution(output_dir / "genre-stability.svg", rows)
    write_readme(output_dir, corpus_path, summary)
    print(f"Cross-genre v1 diagnostics written: {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-csv", default="validation/cross-genre-v1/corpus.csv")
    parser.add_argument("--output-dir", default="validation/cross-genre-v1")
    parser.add_argument("--max-pairs", type=int, default=100)
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--use-seed-fixtures", action="store_true")
    return parser.parse_args()


def read_corpus(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"text_id", "author_id", "genre", "corpus_source", "text"}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise SystemExit(f"Missing required corpus columns in {path}: {sorted(missing)}")
    for row in rows:
        row.setdefault("problem_id", "")
        row.setdefault("truth_label", "")
        row.setdefault("document_role", "")
        row.setdefault("pan_problem_type", "")
        row.setdefault("source_record", "")
        row.setdefault("source_license", "unknown")
    return rows


def build_pair_rows(corpus: list[dict[str, str]], *, max_pairs: int | None) -> list[dict[str, Any]]:
    if any(row.get("corpus_source") == "pan15_author_verification" for row in corpus):
        rows = build_pan15_pair_rows(corpus)
    else:
        rows = build_generic_pair_rows(corpus)
    return bounded_pairs(rows, max_pairs=max_pairs)


def build_pan15_pair_rows(corpus: list[dict[str, str]]) -> list[dict[str, Any]]:
    vectors = {row["text_id"]: CognitiveFingerprint(row["text"]).vector(normalized=True) for row in corpus}
    by_problem: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in corpus:
        if row.get("problem_id"):
            by_problem[row["problem_id"]].append(row)

    rows: list[dict[str, Any]] = []
    for problem_id in sorted(by_problem):
        problem_rows = by_problem[problem_id]
        known = [row for row in problem_rows if row.get("document_role") == "known"]
        questioned = [row for row in problem_rows if row.get("document_role") == "questioned"]
        if not known or not questioned:
            continue
        for left in known:
            for right in questioned:
                same_author = left["author_id"] == right["author_id"]
                pair_type = "within_author_cross_genre" if same_author else "inter_author_cross_genre_control"
                rows.append(pair_row(left, right, vectors, pair_type=pair_type, problem_id=problem_id))
    return rows


def build_generic_pair_rows(corpus: list[dict[str, str]]) -> list[dict[str, Any]]:
    vectors = {row["text_id"]: CognitiveFingerprint(row["text"]).vector(normalized=True) for row in corpus}
    rows: list[dict[str, Any]] = []
    for left, right in combinations(corpus, 2):
        same_author = left["author_id"] == right["author_id"]
        same_genre = left["genre"] == right["genre"]
        if same_author and not same_genre:
            pair_type = "within_author_cross_genre"
        elif same_genre and not same_author:
            pair_type = "inter_author_same_genre"
        else:
            continue
        rows.append(pair_row(left, right, vectors, pair_type=pair_type, problem_id=""))
    return rows


def pair_row(
    left: dict[str, str],
    right: dict[str, str],
    vectors: dict[str, list[float]],
    *,
    pair_type: str,
    problem_id: str,
) -> dict[str, Any]:
    left_vector = vectors[left["text_id"]]
    right_vector = vectors[right["text_id"]]
    cosine_distance = CognitiveFingerprint.distance(left_vector, right_vector, metric="cosine")
    return {
        "pair_type": pair_type,
        "problem_id": problem_id,
        "truth_label": left.get("truth_label") or right.get("truth_label") or "",
        "pan_problem_type": left.get("pan_problem_type") or right.get("pan_problem_type") or "",
        "left_text_id": left["text_id"],
        "right_text_id": right["text_id"],
        "left_author_id": left["author_id"],
        "right_author_id": right["author_id"],
        "left_genre": left["genre"],
        "right_genre": right["genre"],
        "left_document_role": left.get("document_role", ""),
        "right_document_role": right.get("document_role", ""),
        "euclidean_distance": round(CognitiveFingerprint.distance(left_vector, right_vector, metric="euclidean"), 6),
        "cosine_similarity": round(1.0 - cosine_distance, 6),
        "cosine_distance": round(cosine_distance, 6),
    }


def bounded_pairs(rows: list[dict[str, Any]], *, max_pairs: int | None) -> list[dict[str, Any]]:
    if max_pairs is None or max_pairs <= 0 or len(rows) <= max_pairs:
        return rows
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["pair_type"]].append(row)
    per_group = max(1, max_pairs // max(1, len(grouped)))
    selected: list[dict[str, Any]] = []
    selected_ids: set[tuple[str, str, str]] = set()
    for pair_type in sorted(grouped):
        for row in grouped[pair_type][:per_group]:
            selected.append(row)
            selected_ids.add((row["pair_type"], row["left_text_id"], row["right_text_id"]))
    for row in rows:
        if len(selected) >= max_pairs:
            break
        row_id = (row["pair_type"], row["left_text_id"], row["right_text_id"])
        if row_id not in selected_ids:
            selected.append(row)
            selected_ids.add(row_id)
    return selected


def permutation_mean_gap(within: list[float], controls: list[float], *, permutations: int, seed: int) -> dict[str, float | int | None]:
    if not within or not controls:
        return {"observed_gap_control_minus_within": None, "p_value_greater_plus_one": None, "permutations": permutations}
    observed = fmean(controls) - fmean(within)
    combined = within + controls
    within_count = len(within)
    rng = random.Random(seed)
    exceed = 0
    for _ in range(permutations):
        shuffled = combined[:]
        rng.shuffle(shuffled)
        shuffled_within = shuffled[:within_count]
        shuffled_controls = shuffled[within_count:]
        gap = fmean(shuffled_controls) - fmean(shuffled_within)
        if gap >= observed:
            exceed += 1
    return {
        "observed_gap_control_minus_within": round(observed, 6),
        "p_value_greater_plus_one": round((exceed + 1) / (permutations + 1), 6),
        "permutations": permutations,
        "within_count": len(within),
        "control_count": len(controls),
    }


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


def corpus_fieldnames(rows: list[dict[str, str]]) -> list[str]:
    preferred = ["text_id", "author_id", "genre", "corpus_source", "text"]
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


def write_svg_distribution(path: Path, rows: list[dict[str, Any]]) -> None:
    groups = {
        "within_author_cross_genre": [row["euclidean_distance"] for row in rows if row["pair_type"] == "within_author_cross_genre"],
        "inter_author_control": [row["euclidean_distance"] for row in rows if row["pair_type"].startswith("inter_author")],
    }
    width = 760
    height = 360
    left = 170
    right = 44
    top = 48
    bottom = 54
    max_value = max([value for values in groups.values() for value in values] + [1e-9])

    def x(value: float) -> float:
        return left + (value / max_value) * (width - left - right)

    def strip(values: list[float], y: int, color: str) -> str:
        if not values:
            return ""
        ordered = sorted(values)
        mean = fmean(ordered)
        dots = []
        for index, value in enumerate(ordered):
            jitter = ((index % 9) - 4) * 2.1
            dots.append(f'<circle cx="{x(value):.2f}" cy="{y + jitter:.2f}" r="3" fill="{color}" opacity="0.5"/>')
        return "\n".join(
            [
                f'<line x1="{x(min(ordered)):.2f}" y1="{y}" x2="{x(max(ordered)):.2f}" y2="{y}" stroke="{color}" opacity="0.55"/>',
                f'<line x1="{x(mean):.2f}" y1="{y - 24}" x2="{x(mean):.2f}" y2="{y + 24}" stroke="{color}" stroke-width="3"/>',
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
  <text x="{left}" y="28" font-size="16" font-family="Arial, sans-serif">cross-genre-v1 Euclidean distance diagnostic</text>
  <text x="{left - 12}" y="{top + 85}" text-anchor="end" font-size="12" font-family="Arial, sans-serif">same author / cross genre</text>
  <text x="{left - 12}" y="{top + 185}" text-anchor="end" font-size="12" font-family="Arial, sans-serif">cross-author control</text>
  {strip(groups["within_author_cross_genre"], top + 80, "#111")}
  {strip(groups["inter_author_control"], top + 180, "#777")}
  <line x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" stroke="#bbb"/>
  {''.join(axis)}
  <text x="{(width + left - right) / 2:.2f}" y="{height - 12}" text-anchor="middle" font-size="12" fill="#555" font-family="Arial, sans-serif">Euclidean profile distance</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def write_readme(output_dir: Path, corpus_path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Cross Genre V1

Status: descriptive mathematical diagnostic.
Readiness boundary: `descriptive_only`.

This folder implements a cross-genre stress test. In real-data mode it uses the
PAN15 Author Identification / Verification dataset from Zenodo:

- record: https://zenodo.org/records/3737563
- file: `pan15-authorship-verification-test-and-training.zip`
- checksum used by the preparer: `md5:0ee8837ff58fe43e1c5f2e004484e8d7`
- source license note: `{summary["source_license_notes"]}`

PAN15 exposes verification problems, not a clean author-by-genre table. The
Dutch and Spanish prefixes are documented by PAN15 as cross-genre problems, so
the experiment compares known-vs-questioned documents for same-author (`Y`) and
cross-author (`N`) verification cases.

## Reproduction

```bash
make cross-genre-real
make cross-genre-test
```

Equivalent direct commands:

```bash
PYTHONPATH=src .venv/bin/python scripts/prepare_cross_genre_data.py --max-problems 60
PYTHONPATH=src .venv/bin/python scripts/generate_cross_genre_v1.py --max-pairs 100
```

## Inputs

- corpus file: `{corpus_path}`
- text count: {summary["text_count"]}
- author count: {summary["author_count"]}
- role/genre count: {summary["genre_count"]}
- corpus sources: `{summary["corpus_source_counts"]}`

## Outputs

- `corpus.csv`
- `results.csv`
- `summary.json`
- `genre-stability.svg`

## Current Diagnostic Summary

- within-author cross-genre rows: {summary["within_author_cross_genre_count"]}
- cross-author control rows: {summary["inter_author_control_count"]}
- mean within-author cross-genre distance: {summary["within_author_cross_genre_euclidean_summary"]["mean"]}
- mean cross-author control distance: {summary["inter_author_control_euclidean_summary"]["mean"]}
- permutation p-value: {summary["permutation_mean_gap"]["p_value_greater_plus_one"]}

## Boundary

These outputs do not establish validation, author identity, text origin,
AI-origin, legal status, forensic status, or a universal threshold.
"""
    (output_dir / "README.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
