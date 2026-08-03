#!/usr/bin/env python3
"""Fail-closed validation for the initial self-hosted packaging contract."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BASE = "python:3.12.13-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de"
EXPECTED_USER = "10001:10001"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    flake = (ROOT / "flake.nix").read_text(encoding="utf-8")
    lock = (ROOT / "flake.lock").read_text(encoding="utf-8")
    containerfile = (ROOT / "Containerfile").read_text(encoding="utf-8")
    requirements = (ROOT / "packaging/oci-requirements.txt").read_text(encoding="utf-8").splitlines()
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))

    require('github:NixOS/nixpkgs/nixos-26.05' in flake, "flake input is not pinned to the 26.05 release branch")
    require('"version": 7' in lock, "unexpected flake.lock format")
    require(containerfile.count(f"FROM {EXPECTED_BASE}") == 2, "OCI stages must use the same pinned multi-platform base digest")
    require("USER 10001:10001" in containerfile, "OCI runtime must use the unprivileged fixed user")
    require("ENTRYPOINT [\"cogniprint\"]" in containerfile, "OCI entrypoint must be the installed CLI")

    expected_requirements = {"pip==26.1.2", "setuptools==83.0.0", "PyYAML==6.0.3"}
    require(set(requirements) == expected_requirements, "OCI build requirements are not exactly pinned")
    for line in requirements:
        require(bool(re.fullmatch(r"[A-Za-z0-9_.-]+==[0-9][A-Za-z0-9_.-]*", line)), f"invalid exact requirement: {line}")

    require(isinstance(compose, dict), "compose root must be a mapping")
    service = compose.get("services", {}).get("cogniprint")
    require(isinstance(service, dict), "compose service cogniprint is missing")
    require(service.get("user") == EXPECTED_USER, "compose must preserve the fixed unprivileged user")
    require(service.get("read_only") is True, "compose root filesystem must be read-only")
    require(service.get("network_mode") == "none", "compose default must have no network")
    require(service.get("privileged") in (None, False), "compose privileged mode is forbidden")
    require("ALL" in service.get("cap_drop", []), "compose must drop all Linux capabilities")
    require("no-new-privileges:true" in service.get("security_opt", []), "compose must set no-new-privileges")
    require(any(str(item).startswith("/tmp:rw,noexec,nosuid,nodev") for item in service.get("tmpfs", [])), "compose /tmp hardening is missing")
    volumes = service.get("volumes", [])
    require(any(isinstance(item, dict) and item.get("source") == "./workspace" and item.get("target") == "/workspace" for item in volumes), "compose workspace bind mount is missing")

    print("SELF_HOSTED_PACKAGING_STATIC_CHECK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
