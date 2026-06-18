"""Prepare a bounded PAN15 cross-genre corpus CSV for cross-genre-v1.

PAN15 is an authorship verification corpus. For the Dutch and Spanish
sub-corpora, PAN describes the problems as cross-genre. This script converts the
training verification problems into a deterministic document table consumed by
``scripts/generate_cross_genre_v1.py``.

The source archive is cached locally and is not committed by this script.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
import zipfile
from pathlib import Path
from typing import Any


PAN15_URL = "https://zenodo.org/api/records/3737563/files/pan15-authorship-verification-test-and-training.zip/content"
PAN15_RECORD = "https://zenodo.org/records/3737563"
PAN15_OUTER_MD5 = "0ee8837ff58fe43e1c5f2e004484e8d7"
TRAINING_ZIP = "pan15-authorship-verification-training-dataset-2015-04-19.zip"
PREFIX_TO_LANGUAGE_ZIP = {
    "DU": "pan15-authorship-verification-training-dataset-dutch-2015-04-19.zip",
    "SP": "pan15-authorship-verification-training-dataset-spanish-2015-04-19.zip",
    "EN": "pan15-authorship-verification-training-dataset-english-2015-04-19.zip",
    "GR": "pan15-authorship-verification-training-dataset-greek-2015-04-19.zip",
}
PREFIX_TO_LANGUAGE = {
    "DU": "Dutch",
    "SP": "Spanish",
    "EN": "English",
    "GR": "Greek",
}
PREFIX_TO_PAN_TYPE = {
    "DU": "cross_genre",
    "SP": "cross_genre",
    "EN": "cross_topic",
    "GR": "cross_topic",
}


def main() -> None:
    args = parse_args()
    prefixes = [item.strip().upper() for item in args.problem_prefixes.split(",") if item.strip()]
    unknown = [prefix for prefix in prefixes if prefix not in PREFIX_TO_LANGUAGE_ZIP]
    if unknown:
        raise SystemExit(f"Unknown PAN15 problem prefixes: {unknown}")

    cache_dir = Path(args.cache_dir)
    output_csv = Path(args.output_csv)
    cache_dir.mkdir(parents=True, exist_ok=True)
    archive = cache_dir / "pan15-authorship-verification-test-and-training.zip"
    if args.force_download or not archive.exists():
        download_file(PAN15_URL, archive)
    checksum = md5sum(archive)
    if checksum != PAN15_OUTER_MD5:
        raise SystemExit(f"Unexpected PAN15 archive MD5: {checksum}; expected {PAN15_OUTER_MD5}")

    extract_root = cache_dir / "extracted"
    if args.reextract and extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True, exist_ok=True)
    outer_root = extract_root / "outer"
    safe_extract_zip(archive, outer_root)
    training_zip = outer_root / TRAINING_ZIP
    if not training_zip.exists():
        raise SystemExit(f"PAN15 training zip not found after extraction: {training_zip}")

    training_root = extract_root / "training"
    safe_extract_zip(training_zip, training_root)

    rows: list[dict[str, str]] = []
    problem_count = 0
    for prefix in prefixes:
        language_zip = next(training_root.rglob(PREFIX_TO_LANGUAGE_ZIP[prefix]), None)
        if language_zip is None:
            raise SystemExit(f"Language zip not found for prefix {prefix}: {PREFIX_TO_LANGUAGE_ZIP[prefix]}")
        language_root = extract_root / f"language-{prefix.lower()}"
        safe_extract_zip(language_zip, language_root)
        truth = read_truth(language_root)
        problem_dirs = sorted(
            item
            for item in language_root.rglob(f"{prefix}*")
            if item.is_dir() and item.name in truth
        )
        for problem_dir in problem_dirs:
            if args.max_problems is not None and problem_count >= args.max_problems:
                break
            problem_id = problem_dir.name
            truth_label = truth[problem_id]
            known_files = sorted(problem_dir.glob("known*.txt"))
            unknown_file = problem_dir / "unknown.txt"
            if not known_files or not unknown_file.exists():
                continue
            known_author_id = f"pan15:{problem_id}:known-author"
            unknown_author_id = known_author_id if truth_label == "Y" else f"pan15:{problem_id}:questioned-author"
            for known_file in known_files:
                rows.append(
                    build_row(
                        text_id=f"{problem_id}-{known_file.stem}",
                        author_id=known_author_id,
                        problem_id=problem_id,
                        prefix=prefix,
                        truth_label=truth_label,
                        document_role="known",
                        source_file=known_file,
                        text=read_text(known_file, max_chars=args.max_chars),
                    )
                )
            rows.append(
                build_row(
                    text_id=f"{problem_id}-unknown",
                    author_id=unknown_author_id,
                    problem_id=problem_id,
                    prefix=prefix,
                    truth_label=truth_label,
                    document_role="questioned",
                    source_file=unknown_file,
                    text=read_text(unknown_file, max_chars=args.max_chars),
                )
            )
            problem_count += 1

    if not rows:
        raise SystemExit("No PAN15 rows were prepared.")
    fieldnames = [
        "text_id",
        "author_id",
        "genre",
        "corpus_source",
        "problem_id",
        "language",
        "pan_problem_type",
        "truth_label",
        "document_role",
        "source_file",
        "source_record",
        "source_license",
        "text",
    ]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Prepared PAN15 cross-genre corpus rows: {len(rows)} -> {output_csv}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-csv", default="validation/cross-genre-v1/corpus.csv")
    parser.add_argument("--cache-dir", default=".cache/cogniprint/pan15")
    parser.add_argument("--problem-prefixes", default="DU,SP")
    parser.add_argument("--max-problems", type=int, default=60)
    parser.add_argument("--max-chars", type=int, default=6000)
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--reextract", action="store_true")
    return parser.parse_args()


def download_file(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        import requests

        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            with target.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
    except ImportError:
        from urllib.request import urlopen

        with urlopen(url, timeout=60) as response, target.open("wb") as handle:
            shutil.copyfileobj(response, handle)


def md5sum(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract_zip(archive: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    root = target_dir.resolve()
    with zipfile.ZipFile(archive) as zip_file:
        for member in zip_file.infolist():
            resolved = (target_dir / member.filename).resolve()
            if root not in resolved.parents and resolved != root:
                raise SystemExit(f"Unsafe path in archive {archive}: {member.filename}")
        zip_file.extractall(target_dir)


def read_truth(language_root: Path) -> dict[str, str]:
    truth_files = sorted(language_root.rglob("truth.txt"))
    if not truth_files:
        raise SystemExit(f"No truth.txt found under {language_root}")
    truth: dict[str, str] = {}
    for line in truth_files[0].read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split()
        if len(parts) >= 2 and parts[1] in {"Y", "N"}:
            truth[parts[0]] = parts[1]
    return truth


def build_row(
    *,
    text_id: str,
    author_id: str,
    problem_id: str,
    prefix: str,
    truth_label: str,
    document_role: str,
    source_file: Path,
    text: str,
) -> dict[str, str]:
    return {
        "text_id": text_id,
        "author_id": author_id,
        "genre": document_role,
        "corpus_source": "pan15_author_verification",
        "problem_id": problem_id,
        "language": PREFIX_TO_LANGUAGE[prefix],
        "pan_problem_type": PREFIX_TO_PAN_TYPE[prefix],
        "truth_label": truth_label,
        "document_role": document_role,
        "source_file": str(source_file),
        "source_record": PAN15_RECORD,
        "source_license": "Zenodo open dataset record; verify reuse terms before redistribution",
        "text": text,
    }


def read_text(path: Path, *, max_chars: int) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    text = " ".join(text.replace("\r\n", "\n").replace("\r", "\n").split())
    return text[:max_chars]


if __name__ == "__main__":
    main()
