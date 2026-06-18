"""Run YAML-configured CogniPrint experiments."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .config_schema import parse_experiment_config
from cogniprint.study import collect_study_samples, create_study


def run_experiment(config_payload: dict[str, Any], *, config_path: Path, workspace: Path) -> Path:
    config = parse_experiment_config(config_payload, config_path.parent)
    baseline, variants = collect_study_samples(
        baseline_text=None,
        baseline_file=config.baseline_file,
        variant_texts=[],
        variant_files=config.variant_files,
        variant_folders=[config.variant_folder] if config.variant_folder else [],
    )
    experiment_dir = config.output_dir / _slug(config.name)
    experiment_dir.mkdir(parents=True, exist_ok=True)
    study_dir = create_study(
        workspace=workspace,
        name=config.name,
        baseline=baseline,
        variants=variants,
        cli_args={"config": str(config_path), "description": config.description},
    )
    linked_study_dir = experiment_dir / "study"
    if linked_study_dir.exists():
        shutil.rmtree(linked_study_dir)
    shutil.copytree(study_dir, linked_study_dir)
    manifest = {
        "name": config.name,
        "description": config.description,
        "config_path": str(config_path),
        "workspace_study_dir": str(study_dir),
        "study_copy": str(linked_study_dir),
    }
    (experiment_dir / "experiment-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return experiment_dir


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")[:64] or "experiment"
