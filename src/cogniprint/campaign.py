"""Campaign-level empirical workflows for CogniPrint."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .perturbation import create_perturbation_lab
from .reporting.notes import generate_empirical_notes
from .workstation import DISCLAIMER, ensure_workspace


def run_campaign(config: dict[str, Any], *, config_path: Path, workspace: Path) -> Path:
    ensure_workspace(workspace)
    name = _required_string(config, "name")
    campaign_id = _slug(config.get("campaign_id") or name)
    campaign_dir = workspace / "campaigns" / campaign_id
    if campaign_dir.exists():
        raise FileExistsError(f"Campaign directory already exists: {campaign_dir}")
    for relative in ["studies", "reports", "exports", "latex"]:
        (campaign_dir / relative).mkdir(parents=True, exist_ok=True)

    base_dir = config_path.parent
    series_entries = config.get("series")
    if not isinstance(series_entries, list) or not series_entries:
        raise ValueError("Campaign config requires a non-empty `series` list.")

    series_records = []
    for index, entry in enumerate(series_entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError("Each campaign series entry must be a mapping.")
        series_name = _required_string(entry, "name")
        lab_id = f"{campaign_id}-{_slug(series_name)}"
        lab_dir = create_perturbation_lab(
            workspace=workspace,
            name=series_name,
            lab_id=lab_id,
            baseline_file=_resolve(base_dir, _required_string(entry, "baseline_file")),
            light_file=_optional_path(base_dir, entry.get("light_file")),
            strong_file=_optional_path(base_dir, entry.get("strong_file")),
            variant_files=[_resolve(base_dir, str(path)) for path in entry.get("variant_files", [])],
            variant_folder=_optional_path(base_dir, entry.get("variant_folder")),
            cli_args={"campaign_config": str(config_path), "series_index": index},
        )
        study_copy = campaign_dir / "studies" / lab_id
        shutil.copytree(lab_dir / "study", study_copy)
        notes_dir = campaign_dir / "reports" / lab_id
        generate_empirical_notes(study_copy, notes_dir)
        series_records.append(
            {
                "series_name": series_name,
                "source_record_id": entry.get("source_record_id"),
                "perturbation_dir": str(lab_dir),
                "study_dir": str(study_copy),
                "notes_dir": str(notes_dir),
            }
        )

    manifest = {
        "campaign_id": campaign_id,
        "name": name,
        "description": config.get("description"),
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "config_path": str(config_path),
        "sources_file": str(_optional_path(base_dir, config.get("sources_file"))) if config.get("sources_file") else None,
        "series_count": len(series_records),
        "series": series_records,
        "interpretive_note": DISCLAIMER,
        "source_policy_note": "Campaign source metadata supports research reproducibility and should not be treated as legal advice.",
    }
    _write_json(campaign_dir / "manifest.json", manifest)
    summarize_campaign(campaign_dir)
    return campaign_dir


def summarize_campaign(campaign_dir: Path) -> Path:
    manifest_path = campaign_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"campaign_id": campaign_dir.name, "name": campaign_dir.name}
    rows = _collect_rows(campaign_dir)
    result = {
        "campaign_id": manifest.get("campaign_id", campaign_dir.name),
        "name": manifest.get("name", campaign_dir.name),
        "series_count": manifest.get("series_count", len({row["series_name"] for row in rows})),
        "comparison_count": len(rows),
        "rows": rows,
        "interpretive_note": DISCLAIMER,
    }
    _write_json(campaign_dir / "campaign-results.json", result)
    _write_csv(campaign_dir / "campaign-results.csv", rows)
    _write_summary(campaign_dir / "campaign-summary.md", result)
    _write_appendix(campaign_dir / "manuscript-appendix.md", result)
    _write_latex(campaign_dir / "latex" / "campaign-summary-table.tex", rows)
    reports_dir = campaign_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    _write_paper_materials(reports_dir, result)
    return campaign_dir


def summarize_all_campaigns(*, workspace: Path, campaign_root: Path | None = None) -> Path:
    ensure_workspace(workspace)
    root = campaign_root or (workspace / "campaigns")
    campaign_results = [_load_campaign_result(path) for path in sorted(root.iterdir()) if path.is_dir()]
    campaign_results = [result for result in campaign_results if result is not None]
    rows = [
        {
            "campaign_id": result["campaign_id"],
            "campaign_name": result["name"],
            "series_count": result["series_count"],
            "comparison_count": result["comparison_count"],
            "mean_cosine_similarity": _mean(_numeric(row.get("cosine_similarity")) for row in result["rows"]),
            "mean_euclidean_distance": _mean(_numeric(row.get("euclidean_distance")) for row in result["rows"]),
        }
        for result in campaign_results
    ]
    payload = {
        "campaign_count": len(campaign_results),
        "comparison_count": sum(int(result["comparison_count"]) for result in campaign_results),
        "rows": rows,
        "interpretive_note": DISCLAIMER,
    }
    _write_json(workspace / "exports" / "multi-campaign-summary.json", payload)
    _write_multi_csv(workspace / "exports" / "multi-campaign-summary.csv", rows)
    _write_multi_summary(workspace / "reports" / "multi-campaign-summary.md", payload)
    _write_multi_appendix(workspace / "reports" / "multi-campaign-appendix.md", payload)
    _write_multi_limitations(workspace / "reports" / "multi-campaign-limitations.md", payload)
    return workspace / "reports" / "multi-campaign-summary.md"


def create_colleague_pack(*, campaign_dir: Path, output_dir: Path, dataset_dir: Path | None = None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = _load_campaign_result(campaign_dir)
    if result is None:
        raise FileNotFoundError(f"Campaign results not found: {campaign_dir / 'campaign-results.json'}")
    copies = {
        "campaign-summary.md": campaign_dir / "campaign-summary.md",
        "manuscript-appendix.md": campaign_dir / "manuscript-appendix.md",
        "latex-summary-table.tex": campaign_dir / "latex" / "campaign-summary-table.tex",
    }
    for target_name, source in copies.items():
        if not source.exists():
            raise FileNotFoundError(f"Required campaign artifact not found: {source}")
        shutil.copyfile(source, output_dir / target_name)
    empirical_note = _first_file(campaign_dir / "reports", "empirical-note.md")
    if empirical_note is None:
        raise FileNotFoundError(f"No empirical-note.md found under: {campaign_dir / 'reports'}")
    shutil.copyfile(empirical_note, output_dir / "empirical-note.md")
    dataset_manifest = _resolve_dataset_manifest(dataset_dir)
    if dataset_manifest:
        shutil.copyfile(dataset_manifest, output_dir / "dataset-manifest.json")
    else:
        _write_json(output_dir / "dataset-manifest-summary.json", {"note": "No dataset manifest was provided for this share pack."})
    _write_share_readme(output_dir / "README.md", result, bool(dataset_manifest))
    _write_project_summary(output_dir / "project-summary.md", result)
    _write_interpretation_note(output_dir / "interpretation-note.md")
    return output_dir


def generate_paper2_outputs(*, workspace: Path, campaign_root: Path | None = None, output_dir: Path | None = None) -> Path:
    ensure_workspace(workspace)
    root = campaign_root or (workspace / "campaigns")
    destination = output_dir or (workspace / "reports" / "paper-2")
    destination.mkdir(parents=True, exist_ok=True)
    campaign_results = [_load_campaign_result(path) for path in sorted(root.iterdir()) if path.is_dir()]
    campaign_results = [result for result in campaign_results if result is not None]
    payload = {
        "campaign_count": len(campaign_results),
        "comparison_count": sum(int(result["comparison_count"]) for result in campaign_results),
        "rows": [
            {
                "campaign_id": result["campaign_id"],
                "name": result["name"],
                "series_count": result["series_count"],
                "comparison_count": result["comparison_count"],
            }
            for result in campaign_results
        ],
    }
    materials = _paper2_materials(payload)
    for filename, lines in materials.items():
        (destination / filename).write_text("\n".join(lines), encoding="utf-8")
    return destination


def _collect_rows(campaign_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for study_dir in sorted((campaign_dir / "studies").iterdir() if (campaign_dir / "studies").exists() else []):
        if not study_dir.is_dir():
            continue
        aggregated_path = study_dir / "aggregated-results.json"
        if not aggregated_path.exists():
            continue
        aggregated = json.loads(aggregated_path.read_text(encoding="utf-8"))
        for row in aggregated.get("comparison_rows", []):
            rows.append(
                {
                    "series_name": aggregated.get("name", study_dir.name),
                    "study_id": aggregated.get("study_id", study_dir.name),
                    "variant_label": row.get("variant_label", "variant"),
                    "cosine_similarity": row.get("cosine_similarity"),
                    "euclidean_distance": row.get("euclidean_distance"),
                    "manhattan_distance": row.get("manhattan_distance"),
                    "interpretation": row.get("interpretation", "review in context"),
                }
            )
    return rows


def _load_campaign_result(campaign_dir: Path) -> dict[str, Any] | None:
    path = campaign_dir / "campaign-results.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.setdefault("campaign_id", campaign_dir.name)
    payload.setdefault("name", campaign_dir.name)
    payload.setdefault("series_count", 0)
    payload.setdefault("comparison_count", 0)
    payload.setdefault("rows", [])
    return payload


def _write_summary(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# CogniPrint Empirical Campaign Summary",
        "",
        f"- Campaign: `{result['name']}`",
        f"- Series count: `{result['series_count']}`",
        f"- Comparison rows: `{result['comparison_count']}`",
        "",
        "## Interpretation Boundary",
        "",
        DISCLAIMER,
        "",
        "## Observed Patterns",
        "",
        "| Series | Variant | Cosine similarity signal | Euclidean distance metric | Comparative regularity |",
        "|---|---|---:|---:|---|",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['series_name']} | {row['variant_label']} | `{row['cosine_similarity']}` | `{row['euclidean_distance']}` | {row['interpretation']} |"
        )
    lines.extend(["", "Use this campaign summary to select follow-up studies and draft empirical appendices.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_appendix(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# Empirical Appendix Draft",
        "",
        "This appendix summarizes repeated CogniPrint perturbation series as profile-level observations.",
        "",
        "## Campaign Design",
        "",
        f"The campaign `{result['name']}` contains `{result['series_count']}` perturbation series and `{result['comparison_count']}` comparison rows.",
        "",
        "## Summary Table",
        "",
        "| Series | Variant | Profile shift metric | Stability signal |",
        "|---|---|---:|---|",
    ]
    for row in result["rows"]:
        lines.append(f"| {row['series_name']} | {row['variant_label']} | `{row['euclidean_distance']}` | {row['interpretation']} |")
    lines.extend(["", "All statements should remain tied to observed metric patterns and repeated local validation.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_paper_materials(reports_dir: Path, result: dict[str, Any]) -> None:
    materials = {
        "paper-outline.md": [
            "# Follow-Up Preprint Outline",
            "",
            "## Working Focus",
            "Empirical stability of CogniPrint profile representations under controlled text perturbations.",
            "",
            "## Sections",
            "- Introduction and motivation",
            "- Deterministic profile construction",
            "- Perturbation campaign design",
            "- Observed stability patterns",
            "- Limitations and future validation",
            "",
        ],
        "methods-section-draft.md": [
            "# Methods Section Draft",
            "",
            f"The campaign contains `{result['series_count']}` locally reproducible perturbation series. Each series compares one baseline profile against controlled variants and records metric deltas, profile shifts, and comparison signals.",
            "",
        ],
        "results-section-draft.md": [
            "# Results Section Draft",
            "",
            f"The campaign produced `{result['comparison_count']}` comparison rows. The results should be described as observed profile shifts and comparative regularities across controlled variants.",
            "",
        ],
        "limitations-section-draft.md": [
            "# Limitations Section Draft",
            "",
            "The current campaign is local and exploratory. Results depend on sample selection, edit design, and text length. Additional corpora and repeated studies are required before broader claims are appropriate.",
            "",
        ],
    }
    for filename, lines in materials.items():
        (reports_dir / filename).write_text("\n".join(lines), encoding="utf-8")


def _write_multi_summary(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# CogniPrint Multi-Campaign Summary",
        "",
        f"- Campaigns reviewed: `{payload['campaign_count']}`",
        f"- Comparison rows reviewed: `{payload['comparison_count']}`",
        "",
        "## Interpretation Boundary",
        "",
        DISCLAIMER,
        "",
        "## Repeated Observed Patterns",
        "",
        "| Campaign | Series | Comparisons | Mean cosine signal | Mean Euclidean metric |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['campaign_name']} | `{row['series_count']}` | `{row['comparison_count']}` | `{row['mean_cosine_similarity']}` | `{row['mean_euclidean_distance']}` |"
        )
    lines.extend(["", "Use this summary to track metric shifts, profile differences, perturbation effects, and stability tendencies across repeated campaigns.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_multi_appendix(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Multi-Campaign Appendix Draft",
        "",
        "This appendix collects repeated campaign-level observations from completed CogniPrint perturbation campaigns.",
        "",
        f"The current body contains `{payload['campaign_count']}` campaigns and `{payload['comparison_count']}` comparison rows.",
        "",
        "## Campaign Table",
        "",
        "| Campaign | Comparisons | Observational Use |",
        "|---|---:|---|",
    ]
    for row in payload["rows"]:
        lines.append(f"| {row['campaign_name']} | `{row['comparison_count']}` | empirical note for repeated profile-shift review |")
    lines.extend(["", "Claims should remain descriptive and tied to observed metric behavior.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_multi_limitations(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Multi-Campaign Limitations",
        "",
        "The current campaign body is local, exploratory, and sample-dependent.",
        "",
        "- Repeated observed patterns should be treated as empirical notes, not final conclusions.",
        "- Metric shifts can depend on text length, edit design, and variant selection.",
        "- Additional campaigns and external review are needed before broader claims are appropriate.",
        f"- Current campaign count: `{payload['campaign_count']}`.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_multi_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "campaign_id",
                "campaign_name",
                "series_count",
                "comparison_count",
                "mean_cosine_similarity",
                "mean_euclidean_distance",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_share_readme(path: Path, result: dict[str, Any], has_dataset_manifest: bool) -> None:
    lines = [
        "# CogniPrint Colleague Share Pack",
        "",
        "This compact pack shows a current CogniPrint empirical campaign as a reproducible research workstation output.",
        "",
        "## Primary Files",
        "",
        "- `project-summary.md`",
        "- `campaign-summary.md`",
        "- `manuscript-appendix.md`",
        "- `empirical-note.md`",
        "- `latex-summary-table.tex`",
        "- `interpretation-note.md`",
    ]
    lines.append("- `dataset-manifest.json`" if has_dataset_manifest else "- `dataset-manifest-summary.json`")
    lines.extend(
        [
            "",
            "## Campaign Snapshot",
            "",
            f"- Campaign: `{result['name']}`",
            f"- Series count: `{result['series_count']}`",
            f"- Comparison rows: `{result['comparison_count']}`",
            "",
            "Use this pack to discuss compact statistical text profiles, empirical perturbation studies, profile shifts, and stability tendencies.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_project_summary(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# CogniPrint MVP Project Summary",
        "",
        "CogniPrint is a reproducible research workstation for compact statistical text profiles and controlled perturbation studies.",
        "",
        "## Current Demonstration",
        "",
        f"The included campaign `{result['name']}` contains `{result['series_count']}` perturbation series and `{result['comparison_count']}` comparison rows.",
        "",
        "The materials should be read as empirical signals about profile differences and measured perturbation effects.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_interpretation_note(path: Path) -> None:
    lines = [
        "# Interpretation Note",
        "",
        DISCLAIMER,
        "",
        "Recommended language: reproducible research workstation, compact statistical text profiles, empirical perturbation studies, profile shifts, metric shifts, and stability tendencies.",
        "",
        "Avoid presenting these outputs as source guarantees, legal conclusions, or final classification claims.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _paper2_materials(payload: dict[str, Any]) -> dict[str, list[str]]:
    campaign_count = payload["campaign_count"]
    comparison_count = payload["comparison_count"]
    return {
        "title-options.md": [
            "# Title Options",
            "",
            "- Empirical Stability of CogniPrint Profiles under Controlled Text Perturbations",
            "- Controlled Perturbation Studies for Compact Statistical Text Profiles",
            "- Profile Shift and Stability Tendencies in Local CogniPrint Campaigns",
            "",
        ],
        "abstract-notes.md": [
            "# Abstract Notes",
            "",
            f"This draft line summarizes `{campaign_count}` local campaigns with `{comparison_count}` comparison rows.",
            "The paper should describe measured profile differences and perturbation effects under controlled edits.",
            "",
        ],
        "introduction-notes.md": [
            "# Introduction Notes",
            "",
            "Frame the work as empirical stability analysis for compact statistical text profiles.",
            "Motivate the need for reproducible local campaigns before broader dataset or preprint claims.",
            "",
        ],
        "methods-section-draft.md": [
            "# Methods Section Draft",
            "",
            "Each campaign compares a baseline text against controlled variants. CogniPrint records profile metrics, comparison rows, and campaign-level summaries that can be audited locally.",
            "",
        ],
        "results-section-draft.md": [
            "# Results Section Draft",
            "",
            f"The current campaign body contains `{comparison_count}` comparison rows. Results should be reported as observed metric shifts, profile differences, perturbation effects, and stability tendencies.",
            "",
        ],
        "limitations-section-draft.md": [
            "# Limitations Section Draft",
            "",
            "The current evidence body is local and exploratory. It depends on sample selection, edit design, and the number of completed campaigns.",
            "",
        ],
        "conclusion-notes.md": [
            "# Conclusion Notes",
            "",
            "The second paper can present CogniPrint as a reproducible empirical workflow for studying profile stability under controlled perturbations.",
            "",
        ],
        "appendix-draft.md": [
            "# Appendix Draft",
            "",
            "Include campaign-level tables, per-series empirical notes, and limitations notes. Keep all statements tied to generated artifacts.",
            "",
        ],
        "candidate-tables.md": [
            "# Candidate Tables",
            "",
            "- Multi-campaign summary table",
            "- Campaign-level perturbation rows",
            "- Dataset manifest and baseline/variant relation table",
            "",
        ],
        "candidate-figures.md": [
            "# Candidate Figures",
            "",
            "- Campaign flow diagram",
            "- Profile-shift comparison schematic",
            "- Stability tendency overview by campaign",
            "",
        ],
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["series_name", "study_id", "variant_label", "cosine_similarity", "euclidean_distance", "manhattan_distance", "interpretation"])
        writer.writeheader()
        writer.writerows(rows)


def _write_latex(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [r"\begin{tabular}{llrr}", r"\hline", r"Series & Variant & Cosine signal & Euclidean metric \\", r"\hline"]
    for row in rows:
        series = _latex_escape(str(row["series_name"]))
        variant = _latex_escape(str(row["variant_label"]))
        lines.append(f"{series} & {variant} & {row['cosine_similarity']} & {row['euclidean_distance']} \\\\")
    lines.extend([r"\hline", r"\end{tabular}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _first_file(root: Path, name: str) -> Path | None:
    if not root.exists():
        return None
    matches = sorted(path for path in root.rglob(name) if path.is_file())
    return matches[0] if matches else None


def _resolve_dataset_manifest(dataset_dir: Path | None) -> Path | None:
    if dataset_dir is None:
        return None
    path = dataset_dir / "dataset-manifest.json" if dataset_dir.is_dir() else dataset_dir
    return path if path.exists() else None


def _mean(values: Any) -> float | None:
    numeric_values = [value for value in values if value is not None]
    if not numeric_values:
        return None
    return round(sum(numeric_values) / len(numeric_values), 6)


def _numeric(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Campaign config requires non-empty string field: {key}")
    return value


def _optional_path(base_dir: Path, value: Any) -> Path | None:
    if value is None:
        return None
    return _resolve(base_dir, str(value))


def _resolve(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base_dir / path).resolve()


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")[:80] or "campaign"


def _latex_escape(value: str) -> str:
    return value.replace("&", r"\&").replace("_", r"\_").replace("%", r"\%")
