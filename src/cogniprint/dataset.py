"""Dataset scaffold helpers for future CogniPrint releases."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def create_dataset_scaffold(
    *,
    workspace: Path,
    name: str,
    description: str | None = None,
    baseline_files: list[Path] | None = None,
    variant_files: list[Path] | None = None,
    sources_file: Path | None = None,
) -> Path:
    dataset_dir = workspace / "datasets" / _slug(name)
    for relative in ["raw", "variants", "metadata", "exports"]:
        (dataset_dir / relative).mkdir(parents=True, exist_ok=True)
    resolved_sources = sources_file.expanduser().resolve() if sources_file else None
    if resolved_sources and not resolved_sources.exists():
        raise FileNotFoundError(f"Sources metadata file not found: {resolved_sources}")
    manifest = {
        "name": name,
        "dataset_id": dataset_dir.name,
        "description": description,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "raw_dir": str(dataset_dir / "raw"),
        "variants_dir": str(dataset_dir / "variants"),
        "metadata_dir": str(dataset_dir / "metadata"),
        "exports_dir": str(dataset_dir / "exports"),
        "sample_count": len(baseline_files or []),
        "variant_count": len(variant_files or []),
        "relation_model": "variants reference baseline_sample_id when a baseline sample is available",
        "source_policy": "Record source, license, acquisition date, and usage notes for external texts. This is a research provenance record, not legal advice.",
        "sources_file": str(resolved_sources) if resolved_sources else None,
    }
    _write_json(dataset_dir / "dataset-manifest.json", manifest)
    if resolved_sources:
        (dataset_dir / "metadata" / "SOURCES.md").write_text(resolved_sources.read_text(encoding="utf-8"), encoding="utf-8")
    _write_samples_csv(dataset_dir / "metadata" / "samples.csv", baseline_files or [])
    _write_variants_csv(dataset_dir / "metadata" / "variants.csv", variant_files or [])
    _write_readme(dataset_dir / "README.md", manifest)
    return dataset_dir


def _write_samples_csv(path: Path, files: list[Path]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sample_id", "source_ref", "role", "sha256"])
        for index, file_path in enumerate(files, start=1):
            writer.writerow([f"sample-{index:04d}", str(file_path), "baseline", _sha256(file_path)])


def _write_variants_csv(path: Path, files: list[Path]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["variant_id", "source_ref", "baseline_sample_id", "relation_type", "sha256", "notes"])
        for index, file_path in enumerate(files, start=1):
            writer.writerow([f"variant-{index:04d}", str(file_path), "sample-0001", "controlled_variant", _sha256(file_path), ""])


def _write_readme(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        f"# {manifest['name']}",
        "",
        manifest.get("description") or "CogniPrint dataset scaffold for local research preparation.",
        "",
        "## Structure",
        "",
        "- `raw/` stores baseline or source text samples.",
        "- `variants/` stores controlled variants.",
        "- `metadata/` stores sample and variant metadata.",
        "- `exports/` stores derived release or analysis exports.",
        "",
        "Variant rows include `baseline_sample_id` and `relation_type` so baseline/variant relations remain explicit during later review.",
        "",
        "## Interpretation",
        "",
        "Dataset outputs should be used as research material for profile and perturbation analysis. They should not be framed as final judgements about any source text.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")[:80] or "dataset"
