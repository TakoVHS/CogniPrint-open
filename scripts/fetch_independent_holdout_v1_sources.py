#!/usr/bin/env python3
"""Fetch public-domain excerpts for the independent holdout v1 dataset."""

from __future__ import annotations

import csv
import re
import textwrap
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "datasets" / "independent-holdout-v1"
RAW_DIR = DATASET_DIR / "raw"
METADATA_DIR = DATASET_DIR / "metadata"
SOURCES_CSV = METADATA_DIR / "sources.csv"
EXCERPT_CHARS = 2200
LICENSE_URL = "https://www.gutenberg.org/policy/license"


SOURCES = [
    ("ihv1-sample-001", "Frankenstein", "Mary Wollstonecraft Shelley", "84"),
    ("ihv1-sample-002", "Moby-Dick", "Herman Melville", "2701"),
    ("ihv1-sample-003", "Dracula", "Bram Stoker", "345"),
    ("ihv1-sample-004", "The Adventures of Sherlock Holmes", "Arthur Conan Doyle", "1661"),
    ("ihv1-sample-005", "A Modest Proposal", "Jonathan Swift", "1080"),
    ("ihv1-sample-006", "Jane Eyre", "Charlotte Bronte", "1260"),
    ("ihv1-sample-007", "Adventures of Huckleberry Finn", "Mark Twain", "76"),
    ("ihv1-sample-008", "Great Expectations", "Charles Dickens", "1400"),
    ("ihv1-sample-009", "The Yellow Wallpaper", "Charlotte Perkins Gilman", "1952"),
    ("ihv1-sample-010", "Heart of Darkness", "Joseph Conrad", "219"),
]


def gutenberg_url(gutenberg_id: str) -> str:
    return f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt"


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "CogniPrint research holdout builder"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def strip_boilerplate(text: str) -> str:
    start_match = re.search(r"\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", text, flags=re.I | re.S)
    if start_match:
        text = text[start_match.end() :]
    end_match = re.search(r"\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*", text, flags=re.I | re.S)
    if end_match:
        text = text[: end_match.start()]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    cleaned = "\n\n".join(paragraphs)
    return cleaned[:EXCERPT_CHARS].strip() + "\n"


def write_sources_csv(rows: list[dict[str, str]]) -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "sample_id",
        "title",
        "author",
        "language",
        "source_class",
        "source_domain",
        "source_url",
        "license",
        "license_url",
        "file_path",
        "acquisition_date",
        "usage_note",
    ]
    with SOURCES_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_static_notes() -> None:
    (DATASET_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Independent Holdout v1",
                "",
                "This dataset contains short public-domain excerpts from Project Gutenberg sources that do not overlap with the current public benchmark v1.1 registry.",
                "",
                "The excerpts are used as an independent holdout source family for descriptive validation. Generated variant texts are not published; evidence artifacts store metrics, hashes, and provenance.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (DATASET_DIR / "LICENSE-NOTES.md").write_text(
        "\n".join(
            [
                "# License Notes",
                "",
                "The holdout excerpts are sourced from Project Gutenberg texts. Project Gutenberg states that many ebooks are not restricted by copyright in the United States, while the Project Gutenberg trademark and license terms remain separate from the book text.",
                "",
                f"Project Gutenberg license reference: {LICENSE_URL}",
                "",
                "Use outside the United States may require separate copyright review. CogniPrint treats this holdout layer as a research artifact and preserves source URLs, license references, and hashes for auditability.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for sample_id, title, author, gutenberg_id in SOURCES:
        url = gutenberg_url(gutenberg_id)
        excerpt = strip_boilerplate(fetch_text(url))
        relative_path = Path("datasets") / "independent-holdout-v1" / "raw" / f"{sample_id}.txt"
        (ROOT / relative_path).write_text(textwrap.dedent(excerpt).strip() + "\n", encoding="utf-8")
        rows.append(
            {
                "sample_id": sample_id,
                "title": title,
                "author": author,
                "language": "en",
                "source_class": "Project Gutenberg public-domain source text",
                "source_domain": "literary prose",
                "source_url": url,
                "license": "Project Gutenberg source text; book text not restricted by U.S. copyright according to Project Gutenberg policy",
                "license_url": LICENSE_URL,
                "file_path": str(relative_path),
                "acquisition_date": "2026-05-05",
                "usage_note": "Short excerpt for independent holdout validation; generated variants are not published.",
            }
        )
    write_sources_csv(rows)
    write_static_notes()
    print(f"Fetched {len(rows)} independent holdout excerpts into {RAW_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
