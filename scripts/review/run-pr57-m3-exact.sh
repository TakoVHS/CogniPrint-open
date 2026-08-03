#!/usr/bin/env bash
set -euo pipefail
HEAD=6832729562d4587609bb93e5af3d4f7f96911d06
TREE=6d3754f3bc695c7e482c4f307316e6da99d29589
BASE=d154b8610b182fe9110bf52fcadf02914498d356
rm -rf repo .venv public demo-output cross-repo network-guard
mkdir -p public

echo RUNNER_EXECUTED
python --version
git clone -q https://github.com/TakoVHS/CogniPrint-open.git repo
cd repo
git checkout -q "$HEAD"
[ "$(git rev-parse HEAD)" = "$HEAD" ]
[ "$(git rev-parse HEAD^{tree})" = "$TREE" ]
echo "HEAD=$HEAD"
echo "TREE=$TREE"

cat > ../expected-files.txt <<'LIST'
.dockerignore
Containerfile
compose.yaml
demo/cross_installation_dossier_gate.py
demo/evidence_dossier_quickstart.py
docs/evidence-dossier-m3-operator-guide.md
docs/evidence-dossier-v1.md
docs/evidence-threat-model-v1.md
docs/self-hosted-evidence-workstation-001.md
docs/self-hosted-packaging.md
flake.lock
flake.nix
packaging/oci-requirements.txt
pyproject.toml
schemas/cogniprint-evidence-dossier-v1.schema.json
scripts/check_self_hosted_packaging.py
src/cogniprint/__main__.py
src/cogniprint/dossier.py
src/cogniprint/dossier_security.py
src/cogniprint/entrypoint.py
tests/test_dossier_m3.py
tests/test_evidence_dossier.py
LIST
git diff --name-only "$BASE...$HEAD" | sort > ../actual-files.txt
diff -u ../expected-files.txt ../actual-files.txt
[ "$(wc -l < ../actual-files.txt)" -eq 22 ]
git diff --check "$BASE...$HEAD"
[ -z "$(git status --porcelain)" ]
echo EXACT_IDENTITY_SCOPE_CLEAN=PASS

python -m venv ../.venv
../.venv/bin/python -m pip install -q --upgrade pip setuptools wheel
../.venv/bin/python -m pip install -q PyYAML==6.0.3 ruff==0.16.1
export PYTHONPATH="$PWD/src"
../.venv/bin/ruff check --select E4,E7,E9,F \
  src/cogniprint/__main__.py \
  src/cogniprint/dossier.py \
  src/cogniprint/dossier_security.py \
  src/cogniprint/entrypoint.py \
  tests/test_evidence_dossier.py \
  tests/test_dossier_m3.py \
  demo/cross_installation_dossier_gate.py \
  demo/evidence_dossier_quickstart.py \
  scripts/check_self_hosted_packaging.py
../.venv/bin/python -m py_compile \
  src/cogniprint/__main__.py \
  src/cogniprint/dossier.py \
  src/cogniprint/dossier_security.py \
  src/cogniprint/entrypoint.py \
  tests/test_evidence_dossier.py \
  tests/test_dossier_m3.py \
  demo/cross_installation_dossier_gate.py \
  demo/evidence_dossier_quickstart.py \
  scripts/check_self_hosted_packaging.py

../.venv/bin/python -m unittest discover -s tests -p 'test_*dossier*.py' -v > ../tests-1.log 2>&1
../.venv/bin/python -m unittest discover -s tests -p 'test_*dossier*.py' -v > ../tests-2.log 2>&1
python - <<'PY'
from pathlib import Path
import re

def normalized(path: str) -> str:
    text = Path(path).read_text()
    return re.sub(r'Ran (\d+) tests in [0-9.]+s', r'Ran \1 tests in <elapsed>s', text)

first = normalized('../tests-1.log')
second = normalized('../tests-2.log')
assert first == second
assert 'Ran 32 tests' in first
assert '\nOK\n' in first
PY
echo RUFF_COMPILE_TESTS=PASS

../.venv/bin/python demo/evidence_dossier_quickstart.py \
  --software-commit "$HEAD" \
  --output ../demo-output

cd ..
cp -a repo cross-repo
cd cross-repo
PYTHONPATH= ../.venv/bin/python demo/cross_installation_dossier_gate.py \
  --repo . \
  --software-commit "$HEAD"
cd ../repo

mkdir -p ../network-guard
cat > ../network-guard/sitecustomize.py <<'PY'
import socket

def blocked(*args, **kwargs):
    raise RuntimeError('network disabled by exact-head gate')

socket.socket = blocked
socket.create_connection = blocked
PY
TMP=$(mktemp -d)
printf 'source\n' > "$TMP/source.txt"
printf '{"signal":"descriptive"}\n' > "$TMP/artifact.json"
../.venv/bin/python -m cogniprint dossier export \
  --source "$TMP/source.txt" \
  --artifact "artifact.json=$TMP/artifact.json" \
  --software-commit "$HEAD" \
  --output "$TMP/bundle"
PYTHONPATH="../network-guard:$PWD/src" ../.venv/bin/python -m cogniprint dossier verify --bundle "$TMP/bundle"
../.venv/bin/python -m cogniprint dossier limits
mkdir -p "$TMP/.cogniprint-dossier-stale/sub"
printf x > "$TMP/.cogniprint-dossier-stale/sub/file"
../.venv/bin/python -m cogniprint dossier purge-temp --workspace "$TMP" >/dev/null
[ -d "$TMP/.cogniprint-dossier-stale" ]
../.venv/bin/python -m cogniprint dossier purge-temp --workspace "$TMP" --confirm >/dev/null
[ ! -e "$TMP/.cogniprint-dossier-stale" ]
rm -rf "$TMP"
echo QUICKSTART_CROSS_CLI_PURGE=PASS

../.venv/bin/python scripts/check_self_hosted_packaging.py
../.venv/bin/python scripts/secret_scan.py
../.venv/bin/python scripts/export_public_release.py --check-only
echo SECURITY_RELEASE=PASS

if ! command -v newuidmap >/dev/null 2>&1; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq uidmap slirp4netns fuse-overlayfs >/dev/null
fi
useradd --create-home --uid 10002 gatebuilder 2>/dev/null || true
grep -q '^gatebuilder:' /etc/subuid || echo 'gatebuilder:100000:65536' >> /etc/subuid
grep -q '^gatebuilder:' /etc/subgid || echo 'gatebuilder:100000:65536' >> /etc/subgid
rm -rf /tmp/cogniprint-rootless /tmp/gatebuilder-runtime
cp -a "$PWD" /tmp/cogniprint-rootless
mkdir -p /tmp/gatebuilder-runtime
chown -R gatebuilder:gatebuilder /tmp/cogniprint-rootless /tmp/gatebuilder-runtime
chmod 0700 /tmp/gatebuilder-runtime
ROOTLESS_ENV=(env HOME=/home/gatebuilder XDG_RUNTIME_DIR=/tmp/gatebuilder-runtime STORAGE_DRIVER=vfs BUILDAH_ISOLATION=chroot)
runuser -u gatebuilder -- "${ROOTLESS_ENV[@]}" buildah --storage-driver=vfs bud --isolation=chroot \
  -t localhost/cogniprint-m3:exact \
  -f Containerfile \
  /tmp/cogniprint-rootless
runuser -u gatebuilder -- "${ROOTLESS_ENV[@]}" buildah --storage-driver=vfs inspect \
  localhost/cogniprint-m3:exact > ../oci-inspect.json
../.venv/bin/python - <<'PY'
import json
from pathlib import Path
payload = json.loads(Path('../oci-inspect.json').read_text())
assert payload['OCIv1']['config']['User'] == '10001:10001'
PY
container=$(runuser -u gatebuilder -- "${ROOTLESS_ENV[@]}" buildah --storage-driver=vfs from localhost/cogniprint-m3:exact)
runuser -u gatebuilder -- "${ROOTLESS_ENV[@]}" buildah --storage-driver=vfs run --isolation=chroot \
  "$container" -- /opt/venv/bin/cogniprint dossier limits > ../oci-limits.json
runuser -u gatebuilder -- "${ROOTLESS_ENV[@]}" buildah --storage-driver=vfs rm "$container"
echo ROOTLESS_OCI_M3=PASS

if [ ! -x /root/.nix-profile/bin/nix ]; then
  mkdir -p /nix
  chmod 0755 /nix
  curl -L https://nixos.org/nix/install | sh -s -- --no-daemon
fi
. /root/.nix-profile/etc/profile.d/nix.sh
if [ ! -e /dev/fd/0 ]; then
  rm -rf /dev/fd
  ln -s /proc/self/fd /dev/fd
fi
export NIX_CONFIG='experimental-features = nix-command flakes'
nix --version
nix flake check --no-write-lock-file
first=$(nix build --no-link --print-out-paths)
second=$(nix build --no-link --print-out-paths)
[ "$first" = "$second" ]
"$first/bin/cogniprint" dossier limits > ../nix-limits.json
nix develop --no-write-lock-file -c cogniprint dossier limits > ../nix-dev-limits.json
echo NIX_M3=PASS

! grep -RInE 'SCIENTIFIC_CLAIM_EVIDENCE[=:][[:space:]]*true|STAGE_B=AUTHORISED|CANONICAL_FREEZE=FROZEN' \
  src/cogniprint/dossier_security.py \
  src/cogniprint/entrypoint.py \
  docs/evidence-threat-model-v1.md \
  docs/evidence-dossier-m3-operator-guide.md

git diff --check "$BASE...$HEAD"
[ "$(git rev-parse HEAD)" = "$HEAD" ]
[ "$(git rev-parse HEAD^{tree})" = "$TREE" ]
[ -z "$(git status --porcelain)" ]

{
  echo "HEAD=$HEAD"
  echo "TREE=$TREE"
  echo "BASE=$BASE"
  for marker in \
    RUFF_0_16_1 PYCOMPILE M2_M3_TESTS TEST_DETERMINISM THREAT_MODEL \
    MALICIOUS_DOSSIER_TESTS RESOURCE_LIMITS SAFE_TEMP_PURGE MAIN_CLI_INTEGRATION \
    CROSS_INSTALLATION OFFLINE_NETWORK_GUARD QUICKSTART_DEMO ROOTLESS_OCI_M3 \
    NIX_M3 SECRET_SCAN PUBLIC_RELEASE_CHECK SCIENTIFIC_BOUNDARY SCOPE_22_FILES \
    WORKTREE_CLEAN EXACT_HEAD_M3_GATE; do
    echo "$marker=PASS"
  done
} > ../public/result.txt
printf '<!doctype html><html><body><pre>' > ../public/index.html
cat ../public/result.txt >> ../public/index.html
printf '</pre></body></html>\n' >> ../public/index.html
cat ../public/result.txt
