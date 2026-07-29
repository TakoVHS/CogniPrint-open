from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "finalize_evidence_archive.py"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_input_archive(path: Path, *, traversal: bool = False) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "20260729-110902"
        root.mkdir()
        (root / "metrics.json").write_text(
            json.dumps({"accuracy": 0.5}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (root / "FINAL_LOCAL_STATUS_003.json").write_text(
            json.dumps(
                {
                    "status": "EXECUTED",
                    "archive_name": "old.tar.gz",
                    "archive_sha256": "1" * 64,
                    "scientific_claim_evidence": False,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        (root / "FINAL_STATUS.md").write_text(
            "Final evidence archive: `old.tar.gz`\n"
            "Final evidence archive SHA-256: `" + "1" * 64 + "`\n",
            encoding="utf-8",
        )
        manifest = root / "EVIDENCE_SHA256SUMS.txt"
        files = sorted(
            item for item in root.rglob("*") if item.is_file() and item != manifest
        )
        manifest.write_text(
            "".join(
                f"{sha256_file(item)}  {item.relative_to(root).as_posix()}\n"
                for item in files
            ),
            encoding="utf-8",
        )
        with tarfile.open(path, "w:gz") as handle:
            handle.add(root, arcname=root.name)
            if traversal:
                info = tarfile.TarInfo("../escape.txt")
                info.size = 0
                handle.addfile(info)


def verify_manifest(root: Path) -> int:
    count = 0
    for line in (root / "EVIDENCE_SHA256SUMS.txt").read_text(
        encoding="utf-8"
    ).splitlines():
        expected, relative = line.split("  ", 1)
        actual = sha256_file(root / relative)
        if actual != expected:
            raise AssertionError(relative)
        count += 1
    return count


class EvidenceArchiveFinalizerTests(unittest.TestCase):
    def run_finalizer(
        self,
        input_archive: Path,
        output_archive: Path,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input-archive",
                str(input_archive),
                "--output-archive",
                str(output_archive),
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )

    def test_final_hash_is_detached_and_manifest_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_archive = root / "input.tar.gz"
            output_archive = root / "output.tar.gz"
            create_input_archive(input_archive)
            result = self.run_finalizer(input_archive, output_archive)
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            sidecar = Path(payload["sidecar"])
            self.assertTrue(output_archive.is_file())
            self.assertTrue(sidecar.is_file())
            self.assertEqual(
                sidecar.read_text(encoding="utf-8"),
                f"{sha256_file(output_archive)}  {output_archive.name}\n",
            )
            with tempfile.TemporaryDirectory() as extracted:
                with tarfile.open(output_archive, "r:gz") as handle:
                    members = handle.getmembers()
                    self.assertFalse(
                        any(member.issym() or member.islnk() for member in members)
                    )
                    handle.extractall(extracted)
                evidence_root = next(Path(extracted).iterdir())
                status = json.loads(
                    (evidence_root / "FINAL_LOCAL_STATUS_003.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertNotIn("archive_sha256", status)
                self.assertFalse(status["archive_sha256_embedded"])
                self.assertEqual(
                    status["archive_sha256_policy"],
                    "DETACHED_EXTERNAL_SIDECAR",
                )
                policy = json.loads(
                    (evidence_root / "ARCHIVE_HASH_POLICY_001.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertFalse(policy["self_hash_embedded"])
                self.assertFalse(policy["scientific_metrics_changed"])
                self.assertGreaterEqual(verify_manifest(evidence_root), 4)

    def test_output_is_deterministic_for_stable_archive_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_archive = root / "input.tar.gz"
            first = root / "first" / "output.tar.gz"
            second = root / "second" / "output.tar.gz"
            create_input_archive(input_archive)
            first_result = self.run_finalizer(input_archive, first)
            second_result = self.run_finalizer(input_archive, second)
            self.assertEqual(first_result.returncode, 0, msg=first_result.stderr)
            self.assertEqual(second_result.returncode, 0, msg=second_result.stderr)
            self.assertEqual(sha256_file(first), sha256_file(second))

    def test_unsafe_traversal_archive_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_archive = root / "unsafe.tar.gz"
            output_archive = root / "output.tar.gz"
            create_input_archive(input_archive, traversal=True)
            result = self.run_finalizer(input_archive, output_archive)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe archive path", result.stderr + result.stdout)

    def test_output_archive_paths_are_safe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_archive = root / "input.tar.gz"
            output_archive = root / "output.tar.gz"
            create_input_archive(input_archive)
            result = self.run_finalizer(input_archive, output_archive)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            with tarfile.open(output_archive, "r:gz") as handle:
                for member in handle.getmembers():
                    path = PurePosixPath(member.name)
                    self.assertFalse(path.is_absolute())
                    self.assertNotIn("..", path.parts)
                    self.assertFalse(member.issym())
                    self.assertFalse(member.islnk())


if __name__ == "__main__":
    unittest.main()
