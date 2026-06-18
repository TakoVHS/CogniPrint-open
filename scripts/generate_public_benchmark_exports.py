#!/usr/bin/env python3
"""Generate descriptive coverage exports for the public benchmark subset."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    samples_path = Path("datasets/public-benchmark-v1/metadata/samples.csv").resolve()
    output_dir = Path("evidence/public-benchmark-v1").resolve()
    with samples_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    baselines = [row for row in rows if row["relation_type"] == "baseline"]
    variants = [row for row in rows if row["relation_type"] != "baseline"]

    by_language = _counter_rows(Counter(row["language"] for row in baselines), "language")
    by_source = _counter_rows(Counter(row["source_class"] for row in baselines), "source_class")
    by_axis = _counter_rows(Counter(row["relation_type"] for row in variants), "perturbation_axis")

    _write_json(output_dir / "coverage-by-language.json", {"row_count": len(by_language), "rows": by_language})
    _write_json(output_dir / "coverage-by-source-class.json", {"row_count": len(by_source), "rows": by_source})
    _write_json(output_dir / "coverage-by-perturbation-axis.json", {"row_count": len(by_axis), "rows": by_axis})
    _write_csv(output_dir / "coverage-by-language.csv", by_language, ["language", "count"])
    _write_csv(output_dir / "coverage-by-source-class.csv", by_source, ["source_class", "count"])
    _write_csv(output_dir / "coverage-by-perturbation-axis.csv", by_axis, ["perturbation_axis", "count"])
    _write_markdown(
        output_dir / "coverage-summary.md",
        baseline_count=len(baselines),
        variant_count=len(variants),
        by_language=by_language,
        by_source=by_source,
        by_axis=by_axis,
    )
    print(f"Public benchmark coverage exports written: {output_dir}")
    return 0


def _counter_rows(counter: Counter[str], field_name: str) -> list[dict[str, int | str]]:
    return [{field_name: key, "count": count} for key, count in sorted(counter.items())]


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, int | str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(
    path: Path,
    *,
    baseline_count: int,
    variant_count: int,
    by_language: list[dict[str, int | str]],
    by_source: list[dict[str, int | str]],
    by_axis: list[dict[str, int | str]],
) -> None:
    lines = [
        "# Public Benchmark v1 Coverage Summary",
        "",
        f"- released baseline excerpts: `{baseline_count}`",
        f"- released controlled variants: `{variant_count}`",
        "",
        "## Coverage by Language",
        "",
        "| Language | Count |",
        "|---|---:|",
    ]
    for row in by_language:
        lines.append(f"| {row['language']} | `{row['count']}` |")
    lines.extend(["", "## Coverage by Source Class", "", "| Source class | Count |", "|---|---:|"])
    for row in by_source:
        lines.append(f"| {row['source_class']} | `{row['count']}` |")
    lines.extend(["", "## Coverage by Perturbation Axis", "", "| Axis | Count |", "|---|---:|"])
    for row in by_axis:
        lines.append(f"| {row['perturbation_axis']} | `{row['count']}` |")
    lines.extend(["", "This summary is descriptive coverage metadata only. It does not claim benchmark analysis results.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
