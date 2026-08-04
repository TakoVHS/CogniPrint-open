"""M3 privacy, resource and deletion hardening for evidence dossiers."""
from __future__ import annotations

import argparse
import os
import stat
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

from . import dossier as _base

HARDENING_PROFILE = "m3-bounded-offline-v1"
TEMP_PREFIX = ".cogniprint-dossier-"
MAX_JSON_NESTING = 32
MAX_TREE_DEPTH = 16
MAX_TREE_ENTRIES = 512
MAX_PURGE_DEPTH = 32
MAX_PURGE_ENTRIES = 4096


class _DeletePlan:
    def __init__(self, root: Path, leaves: list[Path], directories: list[Path], byte_count: int) -> None:
        self.root = root
        self.leaves = leaves
        self.directories = directories
        self.byte_count = byte_count

    @property
    def entry_count(self) -> int:
        return len(self.leaves) + len(self.directories)


def resource_limits() -> dict[str, int | str]:
    """Return the fail-closed limits enforced by the M3 adapter."""
    return {
        "hardening_profile": HARDENING_PROFILE,
        "max_manifest_bytes": _base.MAX_MANIFEST_BYTES,
        "max_source_bytes": _base.MAX_SOURCE_BYTES,
        "max_artifact_bytes": _base.MAX_ARTIFACT_BYTES,
        "max_total_artifact_bytes": _base.MAX_TOTAL_ARTIFACT_BYTES,
        "max_artifacts": _base.MAX_ARTIFACTS,
        "max_json_nesting": MAX_JSON_NESTING,
        "max_tree_depth": MAX_TREE_DEPTH,
        "max_tree_entries": MAX_TREE_ENTRIES,
        "max_purge_depth": MAX_PURGE_DEPTH,
        "max_purge_entries": MAX_PURGE_ENTRIES,
    }


def _json_max_nesting(raw: bytes) -> int:
    depth = 0
    maximum = 0
    in_string = False
    escaped = False
    for byte in raw:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 0x5C:
                escaped = True
            elif byte == 0x22:
                in_string = False
            continue
        if byte == 0x22:
            in_string = True
        elif byte in (0x5B, 0x7B):
            depth += 1
            maximum = max(maximum, depth)
            if maximum > MAX_JSON_NESTING:
                raise _base.DossierError(
                    f"dossier JSON exceeds maximum nesting depth {MAX_JSON_NESTING}"
                )
        elif byte in (0x5D, 0x7D):
            depth -= 1
            if depth < 0:
                break
    return maximum


def _read_regular_limited(path: Path, label: str, maximum: int) -> bytes:
    if path.is_symlink():
        raise _base.DossierError(f"{label} must not be a symlink")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise _base.DossierError(f"cannot open {label}: {path}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise _base.DossierError(f"{label} must be a regular file")
        if before.st_size > maximum:
            raise _base.DossierError(f"{label} exceeds the maximum size")
        chunks: list[bytes] = []
        count = 0
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, maximum + 1 - count))
            if not chunk:
                break
            chunks.append(chunk)
            count += len(chunk)
            if count > maximum:
                raise _base.DossierError(f"{label} exceeds the maximum size")
        after = os.fstat(descriptor)
        identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        if identity_before != identity_after or count != before.st_size:
            raise _base.DossierError(f"{label} changed while it was read")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _bounded_inventory(root: Path) -> dict[str, tuple[int, int, int, int, int]]:
    if root.is_symlink() or not root.is_dir():
        raise _base.DossierError("artifacts must be a regular directory, not a symlink")
    inventory: dict[str, tuple[int, int, int, int, int]] = {}
    stack: list[tuple[Path, int]] = [(root, 0)]
    count = 0
    while stack:
        directory, depth = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as exc:
            raise _base.DossierError(f"cannot scan artifact directory: {directory}") from exc
        for entry in entries:
            count += 1
            if count > MAX_TREE_ENTRIES:
                raise _base.DossierError(
                    f"artifact tree exceeds maximum entry count {MAX_TREE_ENTRIES}"
                )
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise _base.DossierError(f"cannot stat artifact entry: {entry.path}") from exc
            relative = Path(entry.path).relative_to(root).as_posix()
            item_depth = depth + 1
            if item_depth > MAX_TREE_DEPTH:
                raise _base.DossierError(
                    f"artifact tree exceeds maximum depth {MAX_TREE_DEPTH}"
                )
            signature = (
                metadata.st_mode,
                metadata.st_size,
                metadata.st_mtime_ns,
                metadata.st_ino,
                metadata.st_dev,
            )
            inventory[relative] = signature
            if stat.S_ISLNK(metadata.st_mode):
                raise _base.DossierError(f"symlink inside artifacts is forbidden: {relative}")
            if stat.S_ISDIR(metadata.st_mode):
                stack.append((Path(entry.path), item_depth))
            elif not stat.S_ISREG(metadata.st_mode):
                raise _base.DossierError(f"unsupported filesystem entry: {relative}")
    return inventory


def preflight_dossier(bundle: Path) -> dict[str, int | str]:
    """Bound manifest complexity and filesystem traversal before verification."""
    bundle = Path(bundle)
    if bundle.is_symlink() or not bundle.is_dir():
        raise _base.DossierError("bundle must be a regular directory, not a symlink")
    raw = _read_regular_limited(
        bundle / _base.DOSSIER_FILENAME,
        _base.DOSSIER_FILENAME,
        _base.MAX_MANIFEST_BYTES,
    )
    nesting = _json_max_nesting(raw)
    inventory = _bounded_inventory(bundle / _base.ARTIFACTS_DIRECTORY)
    return {
        "hardening_profile": HARDENING_PROFILE,
        "json_nesting": nesting,
        "tree_entries": len(inventory),
    }


def verify_dossier_hardened(bundle: Path) -> dict[str, Any]:
    """Verify offline with bounded traversal and change-during-read detection."""
    bundle = Path(bundle)
    before = preflight_dossier(bundle)
    inventory_before = _bounded_inventory(bundle / _base.ARTIFACTS_DIRECTORY)
    report = _base.verify_dossier(bundle)
    inventory_after = _bounded_inventory(bundle / _base.ARTIFACTS_DIRECTORY)
    if inventory_before != inventory_after:
        raise _base.DossierError("artifact tree changed during verification")
    result = dict(report)
    result.update(before)
    return result


def export_dossier_hardened(
    *,
    source: Path,
    artifacts: Mapping[str, Path],
    output: Path,
    software_commit: str,
    software_version: str = _base.DEFAULT_SOFTWARE_VERSION,
    configuration: Path | None = None,
) -> dict[str, Any]:
    """Export the v1 format and fail closed unless immediate offline verification passes."""
    output = Path(output)
    manifest = _base.export_dossier(
        source=source,
        artifacts=artifacts,
        output=output,
        software_commit=software_commit,
        software_version=software_version,
        configuration=configuration,
    )
    try:
        verify_dossier_hardened(output)
    except Exception:
        _remove_created_output(output)
        raise
    return manifest


def _safe_child_name(path: Path) -> bool:
    return path.name.startswith(TEMP_PREFIX) and path.name != TEMP_PREFIX


def _build_delete_plan(root: Path, *, allow_symlink_root: bool = False) -> _DeletePlan:
    root = Path(root)
    try:
        root_metadata = root.lstat()
    except OSError as exc:
        raise _base.DossierError(f"cannot inspect deletion target: {root}") from exc
    if stat.S_ISLNK(root_metadata.st_mode):
        if not allow_symlink_root:
            raise _base.DossierError(f"deletion target must not be a symlink: {root}")
        return _DeletePlan(root, [root], [], 0)
    if not stat.S_ISDIR(root_metadata.st_mode):
        raise _base.DossierError(f"deletion target must be a directory: {root}")

    leaves: list[Path] = []
    directories: list[Path] = []
    byte_count = 0
    stack: list[tuple[Path, int]] = [(root, 0)]
    entry_count = 0
    while stack:
        directory, depth = stack.pop()
        if depth > MAX_PURGE_DEPTH:
            raise _base.DossierError(
                f"temporary tree exceeds maximum purge depth {MAX_PURGE_DEPTH}"
            )
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as exc:
            raise _base.DossierError(f"cannot scan deletion target: {directory}") from exc
        for entry in entries:
            entry_count += 1
            if entry_count > MAX_PURGE_ENTRIES:
                raise _base.DossierError(
                    f"temporary tree exceeds maximum purge entry count {MAX_PURGE_ENTRIES}"
                )
            path = Path(entry.path)
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise _base.DossierError(f"cannot stat deletion entry: {path}") from exc
            if metadata.st_dev != root_metadata.st_dev:
                raise _base.DossierError(f"refusing to cross filesystem boundary: {path}")
            if stat.S_ISLNK(metadata.st_mode) or stat.S_ISREG(metadata.st_mode):
                leaves.append(path)
                byte_count += metadata.st_size
            elif stat.S_ISDIR(metadata.st_mode):
                directories.append(path)
                stack.append((path, depth + 1))
            else:
                raise _base.DossierError(f"unsupported temporary filesystem entry: {path}")
    directories.sort(key=lambda path: len(path.parts), reverse=True)
    return _DeletePlan(root, leaves, directories, byte_count)


def _execute_delete_plan(plan: _DeletePlan) -> None:
    for path in plan.leaves:
        try:
            path.unlink()
        except PermissionError:
            path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            path.unlink()
    for path in plan.directories:
        path.rmdir()
    if plan.root.exists() or plan.root.is_symlink():
        if plan.root.is_symlink():
            plan.root.unlink()
        else:
            plan.root.rmdir()


def _remove_created_output(output: Path) -> None:
    output = Path(output)
    if not output.exists() and not output.is_symlink():
        return
    parent = output.parent.resolve()
    if output.parent.resolve() != parent or output.resolve(strict=False).parent != parent:
        raise _base.DossierError("refusing to remove output outside its declared parent")
    plan = _build_delete_plan(output)
    _execute_delete_plan(plan)


def purge_temporary_data(workspace: Path, *, dry_run: bool = True) -> dict[str, Any]:
    """Delete only direct CogniPrint staging children, never following symlinks."""
    workspace = Path(workspace)
    if workspace.is_symlink() or not workspace.is_dir():
        raise _base.DossierError("workspace must be a regular directory, not a symlink")
    plans: list[_DeletePlan] = []
    skipped: list[dict[str, str]] = []
    for child in sorted(workspace.iterdir(), key=lambda path: path.name):
        if not _safe_child_name(child):
            continue
        metadata = child.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            plans.append(_build_delete_plan(child, allow_symlink_root=True))
        elif stat.S_ISDIR(metadata.st_mode):
            plans.append(_build_delete_plan(child))
        else:
            skipped.append({"path": child.name, "reason": "not-a-directory-or-symlink"})

    report: dict[str, Any] = {
        "status": "DRY_RUN" if dry_run else "PURGED",
        "deletion_semantics": "logical-unlink-only-not-cryptographic-erasure",
        "workspace": str(workspace.resolve()),
        "candidate_count": len(plans),
        "entry_count": sum(plan.entry_count for plan in plans),
        "byte_count": sum(plan.byte_count for plan in plans),
        "paths": [plan.root.name for plan in plans],
        "skipped": skipped,
    }
    if not dry_run:
        for plan in plans:
            _execute_delete_plan(plan)
    return report


def _parse_artifact_specs(values: Sequence[str]) -> dict[str, Path]:
    artifacts: dict[str, Path] = {}
    for value in values:
        name, separator, raw_path = value.partition("=")
        if not separator or not name or not raw_path:
            raise _base.DossierError("each --artifact must use NAME=PATH")
        normalized = PurePosixPath(name).as_posix()
        if normalized in artifacts:
            raise _base.DossierError(f"duplicate artifact path: {normalized}")
        artifacts[normalized] = Path(raw_path)
    return artifacts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cogniprint dossier")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser("export", help="Create and self-verify a local dossier.")
    export_parser.add_argument("--source", type=Path, required=True)
    export_parser.add_argument("--artifact", action="append", required=True, help="NAME=PATH; repeatable.")
    export_parser.add_argument("--configuration", type=Path)
    export_parser.add_argument("--software-commit", required=True)
    export_parser.add_argument("--software-version", default=_base.DEFAULT_SOFTWARE_VERSION)
    export_parser.add_argument("--output", type=Path, required=True)

    verify_parser = subparsers.add_parser("verify", help="Verify a dossier offline with M3 bounds.")
    verify_parser.add_argument("--bundle", type=Path, required=True)

    purge_parser = subparsers.add_parser("purge-temp", help="Remove only CogniPrint staging directories.")
    purge_parser.add_argument("--workspace", type=Path, required=True)
    purge_parser.add_argument(
        "--confirm",
        action="store_true",
        help="Perform logical deletion. Without this flag the command is a dry run.",
    )

    subparsers.add_parser("limits", help="Print enforced resource limits.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            manifest = export_dossier_hardened(
                source=args.source,
                artifacts=_parse_artifact_specs(args.artifact),
                configuration=args.configuration,
                software_commit=args.software_commit,
                software_version=args.software_version,
                output=args.output,
            )
            report: Mapping[str, Any] = {
                "status": "EXPORTED",
                "self_verified": True,
                "hardening_profile": HARDENING_PROFILE,
                "artifact_count": len(manifest["artifacts"]),
            }
        elif args.command == "verify":
            report = verify_dossier_hardened(args.bundle)
        elif args.command == "purge-temp":
            report = purge_temporary_data(args.workspace, dry_run=not args.confirm)
        else:
            report = resource_limits()
        print(_base._canonical_bytes(report).decode("utf-8"), end="")
        return 0
    except _base.DossierError as exc:
        print(f"DOSSIER_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
