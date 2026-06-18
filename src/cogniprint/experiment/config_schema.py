"""Minimal validation for CogniPrint experiment configs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    baseline_file: Path
    variant_files: list[Path]
    variant_folder: Path | None
    output_dir: Path
    description: str | None = None


def parse_experiment_config(payload: dict[str, Any], base_dir: Path) -> ExperimentConfig:
    if not isinstance(payload, dict):
        raise ValueError("Experiment config must be a mapping.")
    name = _required_string(payload, "name")
    baseline_file = _resolve(base_dir, _required_string(payload, "baseline_file"))
    variant_files = [_resolve(base_dir, str(item)) for item in payload.get("variant_files", [])]
    variant_folder = payload.get("variant_folder")
    output_dir = _resolve(base_dir, str(payload.get("output_dir", "workspace/experiments")))
    if not variant_files and not variant_folder:
        raise ValueError("Experiment config requires variant_files or variant_folder.")
    return ExperimentConfig(
        name=name,
        description=payload.get("description"),
        baseline_file=baseline_file,
        variant_files=variant_files,
        variant_folder=_resolve(base_dir, str(variant_folder)) if variant_folder else None,
        output_dir=output_dir,
    )


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Experiment config requires non-empty string field: {key}")
    return value


def _resolve(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base_dir / path).resolve()
