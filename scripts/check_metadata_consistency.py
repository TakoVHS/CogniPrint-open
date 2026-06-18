#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

EXPECTED_AUTHOR = "Adriashkin Roman"
EXPECTED_ORCID = "0009-0009-6337-1806"
EXPECTED_TITLE = "CogniPrint: A mathematical framework for cognitive fingerprint analysis of text"
EXPECTED_PROJECT_URL = "https://cogniprint.org"
EXPECTED_REPOSITORY_URL = "https://github.com/TakoVHS/CogniPrint"
EXPECTED_YEAR = "2026"


def normalize_author(value: str) -> str:
    text = " ".join((value or "").replace(",", " ").split()).strip()
    lower = text.casefold()
    if lower == "adriashkin roman":
        return EXPECTED_AUTHOR
    return text


def normalize_orcid(value: str) -> str:
    text = (value or "").strip()
    match = re.search(r"(\d{4}-\d{4}-\d{4}-\d{4})", text)
    return match.group(1) if match else text


def extract_readme_metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    author = EXPECTED_AUTHOR if EXPECTED_AUTHOR in text else ""
    orcid = normalize_orcid(EXPECTED_ORCID if EXPECTED_ORCID in text else "")
    title_match = re.search(r"\*\*CogniPrint\*\*.*", text)
    return {
        "author": author,
        "orcid": orcid,
        "title": EXPECTED_TITLE if "cognitive fingerprints" in text.casefold() else "",
        "project_url": EXPECTED_PROJECT_URL if EXPECTED_PROJECT_URL in text else "",
        "repository_url": EXPECTED_REPOSITORY_URL if EXPECTED_REPOSITORY_URL in text else "",
        "year": EXPECTED_YEAR if "2026" in text else "",
    }


def extract_citation_metadata(path: Path) -> dict[str, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    author_data = (data.get("authors") or [{}])[0]
    author = normalize_author(
        author_data.get("name")
        or f"{author_data.get('family-names', '')} {author_data.get('given-names', '')}".strip()
    )
    return {
        "author": author,
        "orcid": normalize_orcid(author_data.get("orcid", "")),
        "title": data.get("title", ""),
        "project_url": data.get("url", ""),
        "repository_url": data.get("repository-code", ""),
        "year": str(data.get("date-released", "")).split("-")[0] if data.get("date-released") else "",
    }


def extract_zenodo_metadata(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    creator = (data.get("creators") or [{}])[0]
    return {
        "author": normalize_author(creator.get("name", "")),
        "orcid": normalize_orcid(creator.get("orcid", "")),
        "title": data.get("title", ""),
        "project_url": EXPECTED_PROJECT_URL if EXPECTED_PROJECT_URL in data.get("description", "") else "",
        "repository_url": EXPECTED_REPOSITORY_URL if EXPECTED_REPOSITORY_URL in data.get("description", "") else "",
        "year": "",
    }


def extract_site_metadata(site_root: Path) -> dict[str, str]:
    candidates = [
        site_root / "index.html",
        site_root / "research.html",
        site_root / "evidence" / "index.html",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in candidates if path.exists())
    return {
        "author": EXPECTED_AUTHOR if EXPECTED_AUTHOR in text else "",
        "orcid": normalize_orcid(EXPECTED_ORCID if EXPECTED_ORCID in text else ""),
        "title": EXPECTED_TITLE if "CogniPrint" in text else "",
        "project_url": EXPECTED_PROJECT_URL if EXPECTED_PROJECT_URL in text else "",
        "repository_url": EXPECTED_REPOSITORY_URL if EXPECTED_REPOSITORY_URL in text else "",
        "year": EXPECTED_YEAR if "2026" in text else "",
    }


def collect_metadata(root: Path, site_root: Path | None = None) -> dict[str, dict[str, str]]:
    metadata = {
        "README.md": extract_readme_metadata(root / "README.md"),
        "CITATION.cff": extract_citation_metadata(root / "CITATION.cff"),
        ".zenodo.json": extract_zenodo_metadata(root / ".zenodo.json"),
    }
    if site_root and site_root.exists():
        metadata["website"] = extract_site_metadata(site_root)
    return metadata


def validate_metadata(metadata: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for source, values in metadata.items():
        author = normalize_author(values.get("author", ""))
        orcid = normalize_orcid(values.get("orcid", ""))
        title = values.get("title", "")
        project_url = values.get("project_url", "")
        repository_url = values.get("repository_url", "")
        year = values.get("year", "")

        if author and author != EXPECTED_AUTHOR:
            errors.append(f"{source}: author '{author}' != '{EXPECTED_AUTHOR}'")
        if orcid and orcid != EXPECTED_ORCID:
            errors.append(f"{source}: ORCID '{orcid}' != '{EXPECTED_ORCID}'")
        if title and title != EXPECTED_TITLE:
            errors.append(f"{source}: title '{title}' != '{EXPECTED_TITLE}'")
        if project_url and project_url != EXPECTED_PROJECT_URL:
            errors.append(f"{source}: project URL '{project_url}' != '{EXPECTED_PROJECT_URL}'")
        if repository_url and repository_url != EXPECTED_REPOSITORY_URL:
            errors.append(f"{source}: repository URL '{repository_url}' != '{EXPECTED_REPOSITORY_URL}'")
        if source == "CITATION.cff" and year and year != EXPECTED_YEAR:
            errors.append(f"{source}: release year '{year}' != '{EXPECTED_YEAR}'")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--site-root", default="")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    site_root = Path(args.site_root).resolve() if args.site_root else root.parent / "TakoVHS.github.io"
    metadata = collect_metadata(root, site_root if site_root.exists() else None)
    errors = validate_metadata(metadata)
    if errors:
        print("Metadata consistency check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Metadata consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
