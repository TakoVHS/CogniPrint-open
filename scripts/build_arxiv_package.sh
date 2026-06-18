#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PAPER_DIR="$REPO_ROOT/paper"
STAGE_DIR="$REPO_ROOT/release_artifacts/arxiv-v1/cogniprint-arxiv-v1"
ARCHIVE="$REPO_ROOT/release_artifacts/cogniprint-arxiv-v1.tar.gz"

cd "$REPO_ROOT"

"$PAPER_DIR/../.venv/bin/python" scripts/generate_paper_figures.py

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR/figures"

cp "$PAPER_DIR/main.tex" "$STAGE_DIR/"
cp "$PAPER_DIR/references.bib" "$STAGE_DIR/"
cp "$PAPER_DIR/README-for-arxiv.md" "$STAGE_DIR/"
cp "$PAPER_DIR/arxiv-abstract.txt" "$STAGE_DIR/"
cp "$PAPER_DIR/figures/"*.pdf "$STAGE_DIR/figures/"

tar -C "$REPO_ROOT/release_artifacts/arxiv-v1" -czf "$ARCHIVE" cogniprint-arxiv-v1
echo "arXiv package written: $ARCHIVE"
