#!/usr/bin/env bash
# Reviewer-facing smoke reproducibility check.
#
# Run from the repository root after creating a virtual environment and running:
#   pip install -e .

set -euo pipefail

echo "=== CogniPrint reproducibility check ==="
PYTHON_BIN="${PYTHON:-.venv/bin/python}"

echo "1. Running unit tests..."
make test

echo "2. Regenerating mathematical evidence diagnostics..."
make mathematical-evidence-v1

echo "3. Running fast human-paraphrase smoke diagnostics..."
make human-paraphrase-test

echo "4. Running fast cross-genre smoke diagnostics..."
make cross-genre-test

echo "5. Checking generated artifacts..."
"$PYTHON_BIN" - <<'PY'
from __future__ import annotations

import csv
import json
from pathlib import Path

required_files = [
    Path("validation/mathematical-evidence-v1/manifest.json"),
    Path("validation/mathematical-evidence-v1/pca-summary.json"),
    Path("validation/mathematical-evidence-v1/lipschitz-summary.json"),
    Path("workspace/experiments/math-phase2-test/human-paraphrase-v1/results.csv"),
    Path("workspace/experiments/math-phase2-test/cross-genre-v1/results.csv"),
]

for path in required_files:
    if not path.exists():
        raise SystemExit(f"Missing expected artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"Empty expected artifact: {path}")

manifest = json.loads(Path("validation/mathematical-evidence-v1/manifest.json").read_text(encoding="utf-8"))
if manifest.get("readiness_boundary") != "descriptive_only":
    raise SystemExit("Unexpected readiness boundary in mathematical evidence manifest.")

for csv_path in required_files[-2:]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"No data rows in {csv_path}")

print("All reproducibility smoke artifacts are present and non-empty.")
PY

echo "=== Done ==="
echo "If all steps passed, fill the external-review response template."
