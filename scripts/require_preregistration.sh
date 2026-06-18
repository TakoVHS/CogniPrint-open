#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${ROOT}/docs/pre-registration-wave005.md"

if [[ ! -f "${TARGET}" ]]; then
  echo "Missing required pre-registration file: docs/pre-registration-wave005.md"
  exit 1
fi

echo "Pre-registration scaffold found: ${TARGET}"
