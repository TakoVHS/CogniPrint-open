#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PAPER_DIR="$REPO_ROOT/paper"
MAIN_TEX="$PAPER_DIR/main.tex"

if [[ ! -f "$MAIN_TEX" ]]; then
  echo "Missing paper/main.tex"
  exit 1
fi

if command -v latexmk >/dev/null 2>&1; then
  cd "$PAPER_DIR"
  latexmk -pdf -interaction=nonstopmode main.tex
  exit 0
fi

if command -v docker >/dev/null 2>&1; then
  docker run --rm \
    -v "$PAPER_DIR:/work" \
    -w /work \
    texlive/texlive:latest \
    latexmk -pdf -interaction=nonstopmode main.tex
  exit 0
fi

echo "Neither latexmk nor docker is available; cannot build paper/main.tex."
exit 1
