# Evidence Dossier M3 Operator Guide

Status: `DEVELOPMENT_ONLY`

## Main CLI

The installed console command now exposes the hardened workflow:

```bash
cogniprint dossier limits

cogniprint dossier export \
  --source private-source.txt \
  --artifact analysis.json=workspace/analysis.json \
  --software-commit "$(git rev-parse HEAD)" \
  --output dossier-out

cogniprint dossier verify --bundle dossier-out
```

The same route is available through `python -m cogniprint dossier ...`.

A successful report contains:

```text
status=VERIFIED
offline=true
hardening_profile=m3-bounded-offline-v1
```

## Resource limits

The machine-readable command `cogniprint dossier limits` is the source of truth. The M3 profile adds bounded JSON nesting, artifact-tree depth and entry counts on top of the M2 source, artifact, aggregate and manifest byte limits.

Inputs that exceed a limit fail closed; limits are not silently raised.

## Temporary-data cleanup

First perform a dry run:

```bash
cogniprint dossier purge-temp --workspace /path/to/workspace
```

Then execute logical deletion explicitly:

```bash
cogniprint dossier purge-temp \
  --workspace /path/to/workspace \
  --confirm
```

Only direct children named `.cogniprint-dossier-*` are eligible. Other operator files are untouched. Symlinks are unlinked without following their targets. A complete bounded deletion plan is built before any entry is removed.

The command does not promise cryptographic erasure. Use encrypted storage when recoverability after unlink is unacceptable.

## Quick reproducible demonstration

```bash
python demo/evidence_dossier_quickstart.py \
  --software-commit "$(git rev-parse HEAD)" \
  --output /tmp/cogniprint-demo-dossier
```

Expected markers:

```text
M3_QUICKSTART_EXPORT_VERIFY=PASS
M3_QUICKSTART_MUTATION_REJECTION=PASS
```

## Cross-installation verification

The following gate builds one wheel, installs it into two independent virtual environments, exports with the producer installation and verifies with the second installation under a socket-blocking `sitecustomize` guard:

```bash
python demo/cross_installation_dossier_gate.py --repo .
```

Expected markers:

```text
CROSS_INSTALLATION_PRODUCER=PASS
CROSS_INSTALLATION_OFFLINE_VERIFIER=PASS
CROSS_INSTALLATION_MUTATION_REJECTION=PASS
```

## OCI

```bash
podman build -t cogniprint-workstation -f Containerfile .
podman run --rm --network none cogniprint-workstation dossier limits
```

The image runs as UID/GID `10001:10001`. The Compose skeleton additionally uses a read-only root, drops every capability and sets `no-new-privileges`.

## Nix

```bash
nix flake check
nix develop -c cogniprint dossier limits
```

## Failure handling

- `DOSSIER_ERROR` means the operation failed closed.
- Do not edit `dossier.json` manually; any non-canonical rewrite is rejected.
- Do not retry by weakening limits or following symlinks.
- Preserve the rejected bundle separately only when an independent reviewer needs it and local policy allows retention.

## Scientific and product boundaries

The workflow remains a descriptive evidence and reproducibility layer. It does not establish authorship, identity, legal responsibility, forensic conclusions, intent or deterministic model origin. PR #57 remains Draft until independent security and usability review.
