# Self-hosted packaging

Status: `DEVELOPMENT_ONLY`.

This initial packaging layer provides two paths:

- a Nix flake for a reproducible package and development shell;
- a rootless-compatible OCI fallback with a hardened Compose profile.

It does not authorize Stage B, change the canonical `PRE-FREEZE` state, or establish scientific attribution evidence.

## Nix

```bash
nix build
./result/bin/cogniprint --help
nix develop
```

The flake is locked to a concrete `nixpkgs` revision through `flake.lock`. The initial supported build platform is `x86_64-linux`.

## OCI with Podman or Docker

```bash
mkdir -p workspace
podman build -f Containerfile -t localhost/cogniprint-workstation:development .
podman run --rm --network none --read-only --cap-drop all --security-opt no-new-privileges \
  --user 10001:10001 --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -v "$PWD/workspace:/workspace:Z" localhost/cogniprint-workstation:development --help
```

Compose fallback:

```bash
mkdir -p workspace
docker compose run --rm cogniprint
```

The default Compose profile has no network, drops all capabilities, uses a read-only root filesystem, sets `no-new-privileges`, runs as UID/GID 10001 and exposes only the local `workspace` bind mount.

## Validation

```bash
python scripts/check_self_hosted_packaging.py
```

The clean-checkout gate additionally performs a real Nix build/development-shell import and a daemonless Buildah build/run using the pinned OCI base digest.
