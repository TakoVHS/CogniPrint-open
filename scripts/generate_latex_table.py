#!/usr/bin/env python3
"""Generate a conservative LaTeX table from CogniPrint study results."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(study_dir: str) -> int:
    path = Path(study_dir)
    aggregated_path = path / "aggregated-results.json"
    if not aggregated_path.exists():
        print(f"Missing aggregated-results.json in {path}", file=sys.stderr)
        return 2
    payload = json.loads(aggregated_path.read_text(encoding="utf-8"))
    print(r"\begin{tabular}{lrr}")
    print(r"\hline")
    print(r"Variant & Cosine signal & Euclidean metric \\")
    print(r"\hline")
    for row in payload.get("comparison_rows", []):
        label = str(row.get("variant_label", "variant")).replace("&", r"\&")
        cosine = row.get("cosine_similarity", "N/A")
        euclidean = row.get("euclidean_distance", "N/A")
        print(f"{label} & {cosine} & {euclidean} \\\\")
    print(r"\hline")
    print(r"\end{tabular}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
