"""Perturbation lab workflows for CogniPrint."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .study import collect_study_samples, create_study
from .workstation import DISCLAIMER, ensure_workspace


def create_perturbation_lab(
    *,
    workspace: Path,
    name: str,
    baseline_file: Path,
    light_file: Path | None,
    strong_file: Path | None,
    variant_files: list[Path],
    variant_folder: Path | None,
    lab_id: str | None = None,
    cli_args: dict[str, Any] | None = None,
) -> Path:
    ensure_workspace(workspace)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    actual_lab_id = lab_id or _slug(f"{timestamp}-perturbation-{name}")
    lab_dir = workspace / "perturbations" / actual_lab_id
    if lab_dir.exists():
        raise FileExistsError(f"Perturbation directory already exists: {lab_dir}")
    lab_dir.mkdir(parents=True)

    ordered_variants = []
    if light_file:
        ordered_variants.append(light_file)
    if strong_file and strong_file not in ordered_variants:
        ordered_variants.append(strong_file)
    for path in variant_files:
        if path not in ordered_variants:
            ordered_variants.append(path)

    baseline, variants = collect_study_samples(
        baseline_text=None,
        baseline_file=baseline_file,
        variant_texts=[],
        variant_files=ordered_variants,
        variant_folders=[variant_folder] if variant_folder else [],
    )
    study_dir = create_study(
        workspace=workspace,
        name=name,
        baseline=baseline,
        variants=variants,
        cli_args=cli_args,
    )
    aggregated = json.loads((study_dir / "aggregated-results.json").read_text(encoding="utf-8"))
    manifest = {
        "perturbation_id": actual_lab_id,
        "name": name,
        "timestamp_utc": timestamp,
        "baseline_file": str(baseline_file),
        "light_file": str(light_file) if light_file else None,
        "strong_file": str(strong_file) if strong_file else None,
        "variant_files": [str(path) for path in variant_files],
        "variant_folder": str(variant_folder) if variant_folder else None,
        "study_dir": str(study_dir),
        "cli_args": _json_safe(cli_args or {}),
        "interpretive_note": DISCLAIMER,
    }
    _write_json(lab_dir / "perturbation-manifest.json", manifest)
    _write_json(lab_dir / "perturbation-results.json", aggregated)
    _write_csv(lab_dir / "perturbation-summary.csv", aggregated)
    _write_summary(lab_dir / "stability-summary.md", manifest, aggregated)
    shutil.copytree(study_dir, lab_dir / "study", dirs_exist_ok=True)
    return lab_dir


def _write_summary(path: Path, manifest: dict[str, Any], aggregated: dict[str, Any]) -> None:
    lines = [
        "# CogniPrint Perturbation Stability Summary",
        "",
        f"- Perturbation ID: `{manifest['perturbation_id']}`",
        f"- Name: `{manifest['name']}`",
        f"- Baseline: `{manifest['baseline_file']}`",
        f"- Variant count: `{aggregated.get('variant_count', 0)}`",
        "",
        "## Interpretation Boundary",
        "",
        DISCLAIMER,
        "",
        "Use this summary to inspect profile shifts, metric deltas, observed changes, perturbation effects, and stability patterns.",
        "",
        "## Variant Signals",
        "",
        "| Variant | Cosine similarity signal | Euclidean distance metric | Stability pattern |",
        "|---|---:|---:|---|",
    ]
    for row in aggregated.get("comparison_rows", []):
        pattern = _stability_pattern(float(row.get("euclidean_distance", 0)))
        lines.append(
            f"| {row.get('variant_label', 'variant')} | `{row.get('cosine_similarity', 'n/a')}` | `{row.get('euclidean_distance', 'n/a')}` | {pattern} |"
        )
    lines.extend(["", "## Follow-Up", "", "Review the largest observed changes against edit strength, text length, and repeated experiments before using the values in manuscript arguments.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_csv(path: Path, aggregated: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["variant_label", "cosine_similarity", "euclidean_distance", "manhattan_distance", "stability_pattern"])
        for row in aggregated.get("comparison_rows", []):
            distance = float(row.get("euclidean_distance", 0))
            writer.writerow(
                [
                    row.get("variant_label", "variant"),
                    row.get("cosine_similarity"),
                    row.get("euclidean_distance"),
                    row.get("manhattan_distance"),
                    _stability_pattern(distance),
                ]
            )


def _stability_pattern(distance: float) -> str:
    if distance < 1.0:
        return "low observed profile shift"
    if distance < 4.0:
        return "moderate observed profile shift"
    return "larger observed profile shift"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if callable(value):
        return getattr(value, "__name__", str(value))
    return value


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")[:96] or "perturbation"
