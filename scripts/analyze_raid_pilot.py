#!/usr/bin/env python3
"""Analyze metadata-only RAID pilot features with transparent first-pass baselines."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.benchmarks.evaluation import evaluate_pilot


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            records.append(payload)
    if not records:
        raise ValueError(f"{path}: no records found")
    return records


def markdown_report(result: dict) -> str:
    lines = [
        "# CogniPrint M1 RAID pilot — baseline report",
        "",
        f"Protocol: `{result['protocol']}`",
        f"Readiness boundary: `{result['readiness_boundary']}`",
        f"Train/test records: {result['train_records']} / {result['test_records']}",
        f"Train/test lineage groups: {result['train_groups']} / {result['test_groups']}",
        f"Chance accuracy reference: {result['chance_accuracy_reference']:.3f}",
        "",
        "| Baseline | Accuracy | Balanced accuracy | Macro F1 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key, label in (
        ("majority", "Majority"),
        ("length_only_nearest_centroid", "Length-only nearest centroid"),
        ("cogniprint_12d_nearest_centroid", "CogniPrint 12D nearest centroid"),
    ):
        metrics = result[key]
        lines.append(
            f"| {label} | {metrics['accuracy']:.3f} | {metrics['balanced_accuracy']:.3f} | {metrics['macro_f1']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            result["calibration_note"],
            "",
            "This report is a benchmark diagnostic. It is not proof of exact model identity, AI origin, authorship, actor identity, or forensic provenance.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--features",
        type=Path,
        default=Path("evidence/model-fingerprint-m1/raid-pilot/features.jsonl"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evidence/model-fingerprint-m1/raid-pilot"),
    )
    parser.add_argument("--test-fraction", type=float, default=0.30)
    parser.add_argument("--seed", type=int, default=20260725)
    args = parser.parse_args()

    records = load_jsonl(args.features)
    result = evaluate_pilot(records, test_fraction=args.test_fraction, seed=args.seed)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = args.output_dir / "baseline-metrics.json"
    report_path = args.output_dir / "baseline-report.md"
    metrics_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(markdown_report(result), encoding="utf-8")

    print(metrics_path)
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
