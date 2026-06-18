"""Run orchestration and artifact writing for the local CogniPrint workstation."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .analysis import FINGERPRINT_KEYS, TextProfile, analyze_text, compare_profiles
from .core.distances import selected_metric

CANONICAL_IDENTITY = {
    "project_name": "CogniPrint",
    "author": "Adriashkin Roman",
    "orcid": "0009-0009-6337-1806",
    "affiliation": "CogniPrint Research Initiative",
    "primary_arxiv_category": "math.ST",
    "secondary_arxiv_category": "cs.CL",
    "contact_email": "roman@cogniprint.org",
    "domain": "cogniprint.org",
}

TEXT_SUFFIXES = {".txt", ".md", ".text"}

DISCLAIMER = (
    "CogniPrint outputs are research signals for profile analysis and comparison. "
    "They are not legal conclusions, source guarantees, or final judgments about a text."
)


@dataclass(frozen=True)
class TextSample:
    sample_id: str
    label: str
    source_type: str
    source_ref: str
    text: str


def ensure_workspace(workspace: Path) -> None:
    for relative in [
        "input",
        "runs",
        "reports",
        "notes",
        "exports",
        "share",
        "studies",
        "profiles",
        "corpus",
        "experiments",
        "perturbations",
        "datasets",
        "campaigns",
    ]:
        (workspace / relative).mkdir(parents=True, exist_ok=True)


def collect_samples(
    texts: list[str] | None = None,
    files: list[Path] | None = None,
    folders: list[Path] | None = None,
) -> list[TextSample]:
    samples: list[TextSample] = []
    for index, text in enumerate(texts or [], start=1):
        samples.append(_sample_from_text(text, index))
    for path in files or []:
        samples.append(_sample_from_file(path))
    for folder in folders or []:
        samples.extend(_samples_from_folder(folder))
    return samples


def create_run(
    *,
    samples: list[TextSample],
    workspace: Path,
    command_name: str,
    run_label: str | None = None,
    run_id: str | None = None,
    baseline_index: int = 0,
    cli_args: dict[str, Any] | None = None,
    metric: str = "all",
) -> Path:
    if not samples:
        raise ValueError("At least one input text is required.")

    ensure_workspace(workspace)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    profiles = {sample.sample_id: analyze_text(sample.text) for sample in samples}
    actual_run_id = run_id or _build_run_id(timestamp, samples, command_name, run_label)
    run_dir = workspace / "runs" / actual_run_id
    if run_dir.exists():
        raise FileExistsError(f"Run directory already exists: {run_dir}")
    run_dir.mkdir(parents=True)

    comparisons = _build_comparisons(samples, profiles, baseline_index, metric) if len(samples) > 1 else []
    manifest = _build_manifest(
        samples=samples,
        profiles=profiles,
        timestamp=timestamp,
        command_name=command_name,
        run_label=run_label,
        run_id=actual_run_id,
        baseline_index=baseline_index,
        cli_args=cli_args,
        metric=metric,
    )
    results = _build_results(samples, profiles, comparisons)

    _write_json(run_dir / "manifest.json", manifest)
    _write_json(run_dir / "results.json", results)
    if comparisons:
        _write_json(run_dir / "comparisons.json", {"comparisons": comparisons})
    _write_summary(run_dir / "summary.md", manifest, results, comparisons)
    _write_csv(run_dir / "export.csv", samples, profiles, comparisons)

    reports_dir = workspace / "reports"
    exports_dir = workspace / "exports"
    report_path = reports_dir / f"{actual_run_id}.md"
    export_path = exports_dir / f"{actual_run_id}.csv"
    report_path.write_text((run_dir / "summary.md").read_text(encoding="utf-8"), encoding="utf-8")
    export_path.write_text((run_dir / "export.csv").read_text(encoding="utf-8"), encoding="utf-8")
    return run_dir


def _sample_from_text(text: str, index: int) -> TextSample:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return TextSample(
        sample_id=f"inline_{index}_{digest}",
        label=f"inline-{index}",
        source_type="inline",
        source_ref=f"inline:{digest}",
        text=text,
    )


def _sample_from_file(path: Path) -> TextSample:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Input file not found: {resolved}")
    text = resolved.read_text(encoding="utf-8")
    digest = hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()[:8]
    stem = _slug(resolved.stem) or "file"
    return TextSample(
        sample_id=f"{stem}_{digest}",
        label=resolved.name,
        source_type="file",
        source_ref=str(resolved),
        text=text,
    )


def _samples_from_folder(folder: Path) -> list[TextSample]:
    resolved = folder.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Input folder not found: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Input folder is not a directory: {resolved}")
    samples = [
        _sample_from_file(path)
        for path in sorted(resolved.rglob("*"))
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
    ]
    if not samples:
        raise ValueError(f"No supported text files found in folder: {resolved}")
    return samples


def _build_comparisons(
    samples: list[TextSample],
    profiles: dict[str, TextProfile],
    baseline_index: int,
    metric: str,
) -> list[dict[str, Any]]:
    baseline = samples[baseline_index]
    reference_vectors = [profiles[sample.sample_id].fingerprint_vector for sample in samples]
    comparisons = []
    for sample in samples:
        if sample.sample_id == baseline.sample_id:
            continue
        comparison = compare_profiles(profiles[baseline.sample_id], profiles[sample.sample_id])
        if metric != "all":
            metric_payload = selected_metric(
                metric,
                profiles[baseline.sample_id].fingerprint_vector,
                profiles[sample.sample_id].fingerprint_vector,
                reference_vectors,
            )
            if isinstance(metric_payload.get("value"), float):
                metric_payload["value"] = round(metric_payload["value"], 6)
            comparison["selected_metric"] = metric_payload
        comparison.update(
            {
                "baseline_sample_id": baseline.sample_id,
                "baseline_label": baseline.label,
                "variant_sample_id": sample.sample_id,
                "variant_label": sample.label,
            }
        )
        comparisons.append(comparison)
    return comparisons


def _build_manifest(
    *,
    samples: list[TextSample],
    profiles: dict[str, TextProfile],
    timestamp: str,
    command_name: str,
    run_label: str | None,
    run_id: str,
    baseline_index: int,
    cli_args: dict[str, Any] | None,
    metric: str,
) -> dict[str, Any]:
    input_modes = sorted({sample.source_type for sample in samples})
    first_profile = next(iter(profiles.values()))
    return {
        "run_id": run_id,
        "timestamp_utc": timestamp,
        "project": CANONICAL_IDENTITY,
        "tool": {
            "name": "cogniprint",
            "version": __version__,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "git_commit": _git_commit(),
        },
        "environment": {
            "executable": os.path.realpath(os.sys.executable),
            "cwd": os.getcwd(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "command": command_name,
        "run_label": run_label,
        "cli_args": _json_safe(cli_args or {}),
        "input_mode": "+".join(input_modes),
        "configuration": {
            "fingerprint_keys": FINGERPRINT_KEYS,
            "fingerprint_version": first_profile.fingerprint_version,
            "feature_schema": first_profile.feature_schema,
            "normalization": first_profile.normalization,
            "baseline_index": baseline_index,
            "input_count": len(samples),
            "text_suffixes": sorted(TEXT_SUFFIXES),
            "comparison_metric": metric,
        },
        "inputs": [
            {
                "sample_id": sample.sample_id,
                "label": sample.label,
                "source_type": sample.source_type,
                "source_ref": sample.source_ref,
                "sha256": hashlib.sha256(sample.text.encode("utf-8")).hexdigest(),
                "char_count": len(sample.text),
                "warning_notes": _input_warnings(sample.text),
            }
            for sample in samples
        ],
        "interpretive_note": DISCLAIMER,
    }


def _build_results(
    samples: list[TextSample],
    profiles: dict[str, TextProfile],
    comparisons: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "disclaimer": DISCLAIMER,
        "profiles": [
            {
                "sample_id": sample.sample_id,
                "label": sample.label,
                "source_type": sample.source_type,
                "source_ref": sample.source_ref,
                "content_hash": profiles[sample.sample_id].content_hash,
                "fingerprint_version": profiles[sample.sample_id].fingerprint_version,
                "metrics": profiles[sample.sample_id].metrics,
                "raw_fingerprint": profiles[sample.sample_id].raw_fingerprint,
                "fingerprint": profiles[sample.sample_id].fingerprint,
                "fingerprint_vector": profiles[sample.sample_id].fingerprint_vector,
                "feature_schema": profiles[sample.sample_id].feature_schema,
                "normalization": profiles[sample.sample_id].normalization,
            }
            for sample in samples
        ],
        "comparisons": comparisons,
    }


def _write_summary(
    path: Path,
    manifest: dict[str, Any],
    results: dict[str, Any],
    comparisons: list[dict[str, Any]],
) -> None:
    lines = [
        "# CogniPrint Local Run Summary",
        "",
        f"- Run ID: `{manifest['run_id']}`",
        f"- Timestamp UTC: `{manifest['timestamp_utc']}`",
        f"- Command: `{manifest['command']}`",
        f"- Input mode: `{manifest['input_mode']}`",
        f"- Input count: `{manifest['configuration']['input_count']}`",
        "",
        "## Interpretive Note",
        "",
        DISCLAIMER,
        "",
        "## Profiles",
        "",
    ]
    for profile in results["profiles"]:
        metrics = profile["metrics"]
        lines.extend(
            [
                f"### {profile['label']}",
                "",
                f"- Sample ID: `{profile['sample_id']}`",
                f"- Source: `{profile['source_type']}` / `{profile['source_ref']}`",
                f"- Fingerprint version: `{profile['fingerprint_version']}`",
                f"- Words: `{metrics['word_count']}`",
                f"- Unique words: `{metrics['unique_word_count']}`",
                f"- Type-token ratio: `{metrics['type_token_ratio']}`",
                f"- Average word length: `{metrics['avg_word_length']}`",
                f"- Average sentence length: `{metrics['avg_sentence_length_words']}`",
                "",
            ]
        )

    if comparisons:
        lines.extend(["## Comparisons", ""])
        for item in comparisons:
            lines.extend(
                [
                    f"### {item['baseline_label']} vs {item['variant_label']}",
                    "",
                    f"- Cosine similarity signal: `{item['cosine_similarity']}`",
                    f"- Euclidean distance metric: `{item['euclidean_distance']}`",
                    f"- Manhattan distance metric: `{item['manhattan_distance']}`",
                    "- Largest observed changes:",
                ]
            )
            for change in item["observed_change"]:
                lines.append(f"  - `{change['metric']}`: `{change['delta']}`")
            if not item["observed_change"]:
                lines.append("  - No non-zero fingerprint deltas observed.")
            lines.append("")

    lines.extend(
        [
            "## Research Use",
            "",
            "Use this bundle as a reproducible local record for experiment notes, theory validation, and manuscript preparation.",
            "Treat all values as analytical signals that require context and repeated validation.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_csv(
    path: Path,
    samples: list[TextSample],
    profiles: dict[str, TextProfile],
    comparisons: list[dict[str, Any]],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["record_type", "sample_id", "label", "metric", "value"])
        for sample in samples:
            profile = profiles[sample.sample_id]
            for key, value in profile.metrics.items():
                writer.writerow(["metric", sample.sample_id, sample.label, key, value])
            for key, value in profile.fingerprint.items():
                writer.writerow(["fingerprint", sample.sample_id, sample.label, key, value])
        for item in comparisons:
            label = f"{item['baseline_label']} vs {item['variant_label']}"
            writer.writerow(["comparison", item["variant_sample_id"], label, "cosine_similarity", item["cosine_similarity"]])
            writer.writerow(["comparison", item["variant_sample_id"], label, "euclidean_distance", item["euclidean_distance"]])
            writer.writerow(["comparison", item["variant_sample_id"], label, "manhattan_distance", item["manhattan_distance"]])


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def _input_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    stripped = text.strip()
    if not stripped:
        warnings.append("input text is empty after trimming whitespace")
    if 0 < len(stripped) < 80:
        warnings.append("input text is short; metrics may be unstable")
    if "\ufffd" in text:
        warnings.append("input contains replacement characters")
    return warnings


def _build_run_id(timestamp: str, samples: list[TextSample], command_name: str, run_label: str | None) -> str:
    payload = json.dumps(
        {
            "timestamp": timestamp,
            "command": command_name,
            "run_label": run_label,
            "samples": [(sample.source_type, sample.source_ref, hashlib.sha256(sample.text.encode("utf-8")).hexdigest()) for sample in samples],
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    safe_timestamp = timestamp.replace(":", "").replace("-", "").replace("Z", "z")
    prefix = _slug(run_label or command_name)
    return f"{safe_timestamp}-{prefix}-{digest}"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:48]


def _git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=Path(__file__).resolve().parents[2],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None
