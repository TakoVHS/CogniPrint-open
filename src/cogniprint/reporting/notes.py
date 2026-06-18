"""Empirical note generation for CogniPrint study artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def generate_empirical_notes(study_dir: Path, output_dir: Path) -> Path:
    manifest, aggregated = _load_study(study_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_empirical_note(output_dir / "empirical-note.md", manifest, aggregated)
    _write_methods_note(output_dir / "methods-note.md", manifest, aggregated)
    _write_result_summary(output_dir / "result-summary.md", manifest, aggregated)
    return output_dir


def _write_empirical_note(path: Path, manifest: dict[str, Any], aggregated: dict[str, Any]) -> None:
    rows = aggregated.get("comparison_rows", [])
    lines = [
        "# Empirical Note",
        "",
        "## Study Identity",
        "",
        f"- Study: `{manifest.get('name', aggregated.get('name', path.parent.name))}`",
        f"- Study ID: `{manifest.get('study_id', aggregated.get('study_id', path.parent.name))}`",
        "",
        "## Inputs",
        "",
        f"- Input count: `{manifest.get('input_count', 'n/a')}`",
        f"- Variant count: `{aggregated.get('variant_count', len(rows))}`",
        "",
        "## Key Observed Patterns",
        "",
    ]
    if rows:
        for row in rows:
            lines.append(f"- `{row.get('variant_label', 'variant')}` shows `{row.get('interpretation', 'a profile comparison signal')}`.")
    else:
        lines.append("- No comparison rows were available.")
    lines.extend(
        [
            "",
            "## Interpretation Limits",
            "",
            "These observations are profile and metric signals for research review. They should be interpreted with input context and repeated experiments.",
            "",
            "## Next Follow-Up Ideas",
            "",
            "- Add more controlled variants.",
            "- Repeat the study with longer samples.",
            "- Compare aggregate deltas across related studies.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_methods_note(path: Path, manifest: dict[str, Any], aggregated: dict[str, Any]) -> None:
    lines = [
        "# Methods Note",
        "",
        "## Comparison Design",
        "",
        "The study compares one baseline profile against one or more controlled variant profiles using deterministic CogniPrint metrics.",
        "",
        "## Artifacts",
        "",
        f"- Source run: `{manifest.get('run_id', aggregated.get('run_id', 'n/a'))}`",
        "- Study manifest: `study-manifest.json`",
        "- Aggregated results: `aggregated-results.json`",
        "- CSV table: `aggregated-results.csv`",
        "",
        "## Reproducibility",
        "",
        "Keep the input files, run bundle, and study bundle together when using these outputs for manuscript preparation.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_result_summary(path: Path, manifest: dict[str, Any], aggregated: dict[str, Any]) -> None:
    lines = [
        "# Result Summary",
        "",
        "| Variant | Cosine similarity signal | Euclidean distance metric | Observation |",
        "|---|---:|---:|---|",
    ]
    for row in aggregated.get("comparison_rows", []):
        lines.append(
            f"| {row.get('variant_label', 'variant')} | `{row.get('cosine_similarity', 'n/a')}` | `{row.get('euclidean_distance', 'n/a')}` | {row.get('interpretation', 'review in context')} |"
        )
    lines.extend(["", "Use this table as a draft aid, not as a standalone conclusion.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _load_study(study_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_path = study_dir / "study-manifest.json"
    aggregated_path = study_dir / "aggregated-results.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    aggregated = json.loads(aggregated_path.read_text(encoding="utf-8")) if aggregated_path.exists() else {}
    return manifest, aggregated
