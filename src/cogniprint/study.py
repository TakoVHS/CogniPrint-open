"""Study-level aggregation for CogniPrint local research workflows."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .workstation import DISCLAIMER, TextSample, collect_samples, create_run, ensure_workspace


def create_study(
    *,
    workspace: Path,
    name: str,
    baseline: list[TextSample],
    variants: list[TextSample],
    study_id: str | None = None,
    cli_args: dict[str, Any] | None = None,
) -> Path:
    if len(baseline) != 1:
        raise ValueError("Study mode requires exactly one baseline text.")
    if not variants:
        raise ValueError("Study mode requires at least one variant text.")

    ensure_workspace(workspace)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    actual_study_id = study_id or _build_study_id(timestamp, name, baseline + variants)
    study_dir = workspace / "studies" / actual_study_id
    if study_dir.exists():
        raise FileExistsError(f"Study directory already exists: {study_dir}")
    study_dir.mkdir(parents=True)

    run_id = f"{actual_study_id}-comparison"
    run_dir = create_run(
        samples=baseline + variants,
        workspace=workspace,
        command_name="study",
        run_label=name,
        run_id=run_id,
        baseline_index=0,
        cli_args=cli_args,
    )

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    results = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))
    comparisons = results.get("comparisons", [])
    aggregated = _aggregate_results(actual_study_id, name, run_id, results, comparisons)
    study_manifest = {
        "study_id": actual_study_id,
        "name": name,
        "timestamp_utc": timestamp,
        "run_id": run_id,
        "run_bundle": str(run_dir),
        "input_count": len(baseline) + len(variants),
        "baseline_sample_id": baseline[0].sample_id,
        "variant_sample_ids": [sample.sample_id for sample in variants],
        "cli_args": _json_safe(cli_args or {}),
        "run_manifest": manifest,
        "interpretive_note": DISCLAIMER,
    }

    _write_json(study_dir / "study-manifest.json", study_manifest)
    _write_json(study_dir / "aggregated-results.json", aggregated)
    _write_csv(study_dir / "aggregated-results.csv", aggregated)
    _write_summary(study_dir / "study-summary.md", study_manifest, aggregated)
    _write_note_stub(study_dir / "manuscript-note.md", study_manifest, aggregated)
    return study_dir


def collect_study_samples(
    *,
    baseline_text: str | None,
    baseline_file: Path | None,
    variant_texts: list[str],
    variant_files: list[Path],
    variant_folders: list[Path],
) -> tuple[list[TextSample], list[TextSample]]:
    baseline_sources = [source for source in [baseline_text, baseline_file] if source]
    if len(baseline_sources) != 1:
        raise ValueError("Provide exactly one baseline input with --baseline-text or --baseline-file.")
    baseline = collect_samples(
        texts=[baseline_text] if baseline_text else [],
        files=[baseline_file] if baseline_file else [],
    )
    variants = collect_samples(texts=variant_texts, files=variant_files, folders=variant_folders)
    return baseline, variants


def _aggregate_results(
    study_id: str,
    name: str,
    run_id: str,
    results: dict[str, Any],
    comparisons: list[dict[str, Any]],
) -> dict[str, Any]:
    profiles_by_id = {profile["sample_id"]: profile for profile in results["profiles"]}
    rows = []
    for comparison in comparisons:
        variant_id = comparison["variant_sample_id"]
        variant_profile = profiles_by_id[variant_id]
        rows.append(
            {
                "baseline_sample_id": comparison["baseline_sample_id"],
                "baseline_label": comparison["baseline_label"],
                "variant_sample_id": variant_id,
                "variant_label": comparison["variant_label"],
                "variant_word_count": variant_profile["metrics"]["word_count"],
                "variant_type_token_ratio": variant_profile["metrics"]["type_token_ratio"],
                "cosine_similarity": comparison["cosine_similarity"],
                "euclidean_distance": comparison["euclidean_distance"],
                "manhattan_distance": comparison["manhattan_distance"],
                "largest_observed_changes": comparison["observed_change"],
                "interpretation": _interpret_comparison(comparison),
            }
        )
    return {
        "study_id": study_id,
        "name": name,
        "run_id": run_id,
        "disclaimer": DISCLAIMER,
        "baseline_profile": results["profiles"][0],
        "variant_count": len(rows),
        "comparison_rows": rows,
    }


def _interpret_comparison(comparison: dict[str, Any]) -> str:
    distance = comparison["euclidean_distance"]
    if distance < 1.0:
        return "low perturbation effect signal in this profile configuration"
    if distance < 4.0:
        return "moderate perturbation effect signal in this profile configuration"
    return "larger perturbation effect signal in this profile configuration"


def _write_summary(path: Path, manifest: dict[str, Any], aggregated: dict[str, Any]) -> None:
    lines = [
        "# CogniPrint Study Summary",
        "",
        f"- Study ID: `{manifest['study_id']}`",
        f"- Name: `{manifest['name']}`",
        f"- Timestamp UTC: `{manifest['timestamp_utc']}`",
        f"- Source run: `{manifest['run_id']}`",
        f"- Variant count: `{aggregated['variant_count']}`",
        "",
        "## Conservative Notes",
        "",
        DISCLAIMER,
        "",
        "Interpret comparison values as profile signals, metric deltas, observed changes, and perturbation effects. Repeated runs and contextual review are required before using these values in manuscript arguments.",
        "",
        "## Baseline Metrics",
        "",
    ]
    metrics = aggregated["baseline_profile"]["metrics"]
    lines.extend(
        [
            f"- Label: `{aggregated['baseline_profile']['label']}`",
            f"- Words: `{metrics['word_count']}`",
            f"- Unique words: `{metrics['unique_word_count']}`",
            f"- Type-token ratio: `{metrics['type_token_ratio']}`",
            f"- Average sentence length: `{metrics['avg_sentence_length_words']}`",
            "",
            "## Perturbation Comparison Table",
            "",
            "| Variant | Cosine similarity signal | Euclidean distance metric | Perturbation effect note |",
            "|---|---:|---:|---|",
        ]
    )
    for row in aggregated["comparison_rows"]:
        lines.append(
            f"| {row['variant_label']} | `{row['cosine_similarity']}` | `{row['euclidean_distance']}` | {row['interpretation']} |"
        )
    lines.extend(
        [
            "",
            "## Manuscript Use",
            "",
            "Use this study summary as a draftable record for theory validation notes, descriptive result tables, and follow-up experiment planning.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_note_stub(path: Path, manifest: dict[str, Any], aggregated: dict[str, Any]) -> None:
    lines = [
        "# Manuscript Note Stub",
        "",
        f"Study `{manifest['study_id']}` compares one baseline profile against `{aggregated['variant_count']}` controlled variant profile(s).",
        "",
        "## Claim Boundary",
        "",
        "This note should describe observed profile changes and perturbation effects only. It should not present the comparison as a source guarantee or final judgement.",
        "",
        "## Draft Observation",
        "",
        "The study records metric-level changes between the baseline text and controlled variants. The largest observed changes should be reviewed against text length, edit strength, and repeated experiment context before inclusion in a manuscript.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_csv(path: Path, aggregated: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "study_id",
                "variant_label",
                "cosine_similarity",
                "euclidean_distance",
                "manhattan_distance",
                "interpretation",
            ]
        )
        for row in aggregated["comparison_rows"]:
            writer.writerow(
                [
                    aggregated["study_id"],
                    row["variant_label"],
                    row["cosine_similarity"],
                    row["euclidean_distance"],
                    row["manhattan_distance"],
                    row["interpretation"],
                ]
            )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _build_study_id(timestamp: str, name: str, samples: list[TextSample]) -> str:
    payload = json.dumps(
        {
            "timestamp": timestamp,
            "name": name,
            "samples": [(sample.source_type, sample.source_ref, hashlib.sha256(sample.text.encode("utf-8")).hexdigest()) for sample in samples],
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    safe_timestamp = timestamp.replace(":", "").replace("-", "").replace("Z", "z")
    return f"{safe_timestamp}-study-{_slug(name)}-{digest}"


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")[:48] or "study"


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if callable(value):
        return getattr(value, "__name__", str(value))
    return value
