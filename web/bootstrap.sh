#!/usr/bin/env bash
set -euo pipefail

TARGET_SHA="35c553d1c52304bab291561e51311888b19ee544"
REPO_URL="https://github.com/TakoVHS/CogniPrint-open.git"
WORKDIR="/tmp/cogniprint-exact-${TARGET_SHA:0:8}"
OUTDIR="${PWD}/runner-out"

echo "RUNNER_EXECUTED"
python3 --version
git --version
make --version | head -n 1

rm -rf "$WORKDIR" "$OUTDIR"
git clone --filter=blob:none --no-checkout "$REPO_URL" "$WORKDIR"
cd "$WORKDIR"
git fetch --depth=1 origin "$TARGET_SHA"
git checkout --detach "$TARGET_SHA"

HEAD_SHA="$(git rev-parse HEAD)"
TREE_SHA="$(git rev-parse HEAD^{tree})"
echo "HEAD=${HEAD_SHA}"
echo "TREE=${TREE_SHA}"
test "$HEAD_SHA" = "$TARGET_SHA"
test -z "$(git status --porcelain --untracked-files=all)"
echo "EXACT_IDENTITY_SCOPE_CLEAN=PASS"

python3 -m venv .venv
make deps
.venv/bin/python -m pip check
make verify

FINAL_HEAD="$(git rev-parse HEAD)"
test "$FINAL_HEAD" = "$TARGET_SHA"
test -z "$(git status --porcelain --untracked-files=all)"

echo "MAKE_VERIFY_EXACT_SHA=PASS"
echo "EXACT_SHA=${FINAL_HEAD}"
echo "EXACT_TREE=${TREE_SHA}"

mkdir -p "$OUTDIR"
cat > "$OUTDIR/index.html" <<EOF
<!doctype html><html><head><meta charset="utf-8"><title>CogniPrint exact runner PASS</title></head><body><h1>PASS</h1><p>MAKE_VERIFY_EXACT_SHA=PASS</p><p>SHA: ${FINAL_HEAD}</p><p>Tree: ${TREE_SHA}</p></body></html>
EOF
