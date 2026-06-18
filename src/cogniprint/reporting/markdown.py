"""Markdown report generation from CogniPrint study artifacts."""

from __future__ import annotations

import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def generate_markdown_report(study_dir: Path, output_file: Path) -> Path:
    manifest, aggregated = _load_study(study_dir)
    lines = [
        "# CogniPrint Research Report",
        "",
        f"- Generated UTC: `{datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')}`",
        f"- Study: `{manifest.get('name', study_dir.name)}`",
        f"- Study ID: `{manifest.get('study_id', study_dir.name)}`",
        "",
        "## Conservative Interpretation",
        "",
        aggregated.get("disclaimer") or manifest.get("interpretive_note") or "Use these outputs as analytical research signals.",
        "",
        "## Baseline Profile",
        "",
    ]
    baseline = aggregated.get("baseline_profile", {})
    metrics = baseline.get("metrics", {})
    if metrics:
        lines.extend(_metric_table(metrics))
    else:
        lines.append("Baseline metrics were not available in the study artifact.")
    lines.extend(["", "## Comparison Summary", ""])
    rows = aggregated.get("comparison_rows", [])
    if rows:
        lines.extend(
            [
                "| Variant | Cosine similarity signal | Euclidean distance metric | Interpretation |",
                "|---|---:|---:|---|",
            ]
        )
        for row in rows:
            lines.append(
                f"| {row.get('variant_label', 'variant')} | `{row.get('cosine_similarity', 'n/a')}` | `{row.get('euclidean_distance', 'n/a')}` | {row.get('interpretation', 'review in context')} |"
            )
    else:
        lines.append("No comparison rows were available in the study artifact.")
    lines.extend(
        [
            "",
            "## Manuscript Use",
            "",
            "Use this report for theory validation notes, descriptive tables, and follow-up experiment planning. Do not treat a single run as a final judgement.",
            "",
        ]
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return output_file


def generate_aggregate_report(study_root: Path, output_file: Path, csv_output: Path | None = None) -> Path:
    rows = []
    for study_dir in sorted(path for path in study_root.iterdir() if path.is_dir()):
        _, aggregated = _load_study(study_dir)
        for row in aggregated.get("comparison_rows", []):
            rows.append(
                {
                    "study_id": aggregated.get("study_id", study_dir.name),
                    "study_name": aggregated.get("name", study_dir.name),
                    "variant_label": row.get("variant_label", "variant"),
                    "cosine_similarity": row.get("cosine_similarity"),
                    "euclidean_distance": row.get("euclidean_distance"),
                    "interpretation": row.get("interpretation", "review in context"),
                }
            )
    lines = [
        "# CogniPrint Aggregate Study Summary",
        "",
        f"- Study root: `{study_root}`",
        f"- Comparison rows: `{len(rows)}`",
        "",
        "## Aggregate Table",
        "",
        "| Study | Variant | Cosine similarity signal | Euclidean distance metric | Observation |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['study_name']} | {row['variant_label']} | `{row['cosine_similarity']}` | `{row['euclidean_distance']}` | {row['interpretation']} |"
        )
    lines.extend(["", "Use this aggregate as a navigation aid for repeated local studies, not as a standalone conclusion.", ""])
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")
    if csv_output:
        csv_output.parent.mkdir(parents=True, exist_ok=True)
        with csv_output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["study_id", "study_name", "variant_label", "cosine_similarity", "euclidean_distance", "interpretation"])
            writer.writeheader()
            writer.writerows(rows)
    return output_file


def _load_study(study_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_path = study_dir / "study-manifest.json"
    aggregated_path = study_dir / "aggregated-results.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    aggregated = json.loads(aggregated_path.read_text(encoding="utf-8")) if aggregated_path.exists() else {}
    return manifest, aggregated


def _metric_table(metrics: dict[str, Any]) -> list[str]:
    lines = ["| Metric | Value |", "|---|---:|"]
    for key, value in sorted(metrics.items()):
        lines.append(f"| `{key}` | `{value}` |")
    return lines
