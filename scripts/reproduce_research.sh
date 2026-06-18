#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

PYTHON_BIN="${PYTHON:-python3}"

if [[ ! -x ".venv/bin/python" ]]; then
  "${PYTHON_BIN}" -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
python -m pip install -r apps/api/requirements.txt

make validate-sources
python -m compileall -q src tests scripts apps/api/app apps/api/tests
make test
make api-contract-test
make smoke
python scripts/check_metadata_consistency.py
python scripts/check_evidence_snapshot.py
python scripts/check_metric_hashes.py
python scripts/check_claims_drift.py

if command -v pdflatex >/dev/null 2>&1 && [[ -f paper/main.tex ]]; then
  (
    cd paper
    pdflatex -interaction=nonstopmode -halt-on-error main.tex >/tmp/cogniprint-paper-build.log
  )
  echo "LaTeX compile passed: paper/main.pdf"
else
  echo "LaTeX compile skipped: pdflatex not available or paper/main.tex missing"
fi

notebook_count="$(find . \
  -path ./.git -prune -o \
  -path ./.venv -prune -o \
  -path ./workspace -prune -o \
  -path ./apps/web/node_modules -prune -o \
  -name '*.ipynb' -print | wc -l)"

if [[ "${notebook_count}" != "0" ]]; then
  if ! command -v jupyter >/dev/null 2>&1; then
    echo "Notebook execution failed: ${notebook_count} notebooks found but jupyter is not installed"
    exit 1
  fi
  find . \
    -path ./.git -prune -o \
    -path ./.venv -prune -o \
    -path ./workspace -prune -o \
    -path ./apps/web/node_modules -prune -o \
    -name '*.ipynb' -print0 |
    xargs -0 -r -n 1 jupyter nbconvert --to notebook --execute --inplace
else
  echo "Notebook execution skipped: no notebooks found"
fi

echo "CogniPrint research audit passed."
