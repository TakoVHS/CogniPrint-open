from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cogniprint import dossier as base
from cogniprint import dossier_security as security
from cogniprint.entrypoint import main as entrypoint_main


class DossierM3Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "source.txt"
        self.source.write_text("private source bytes\n", encoding="utf-8")
        self.artifact = self.root / "result.json"
        self.artifact.write_text('{"signal":"descriptive"}\n', encoding="utf-8")
        self.commit = "b" * 40

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _export(self, name: str = "bundle") -> Path:
        output = self.root / name
        security.export_dossier_hardened(
            source=self.source,
            artifacts={"results/result.json": self.artifact},
            output=output,
            software_commit=self.commit,
        )
        return output

    def test_hardened_export_self_verifies(self) -> None:
        bundle = self._export()
        report = security.verify_dossier_hardened(bundle)
        self.assertEqual(report["status"], "VERIFIED")
        self.assertEqual(report["hardening_profile"], security.HARDENING_PROFILE)
        self.assertGreaterEqual(report["tree_entries"], 2)

    def test_primary_cli_routes_export_verify_and_limits(self) -> None:
        bundle = self.root / "cli-bundle"
        self.assertEqual(
            entrypoint_main(
                [
                    "dossier",
                    "export",
                    "--source",
                    str(self.source),
                    "--artifact",
                    f"result.json={self.artifact}",
                    "--software-commit",
                    self.commit,
                    "--output",
                    str(bundle),
                ]
            ),
            0,
        )
        self.assertEqual(entrypoint_main(["dossier", "verify", "--bundle", str(bundle)]), 0)
        self.assertEqual(entrypoint_main(["dossier", "limits"]), 0)

    def test_deep_json_is_rejected_before_standard_parser(self) -> None:
        bundle = self.root / "deep"
        (bundle / "artifacts").mkdir(parents=True)
        raw = b'{"x":' + (b"[" * (security.MAX_JSON_NESTING + 1)) + b"0" + (
            b"]" * (security.MAX_JSON_NESTING + 1)
        ) + b"}\n"
        (bundle / base.DOSSIER_FILENAME).write_bytes(raw)
        with self.assertRaisesRegex(base.DossierError, "maximum nesting"):
            security.preflight_dossier(bundle)

    def test_brackets_inside_strings_do_not_increase_depth(self) -> None:
        raw = b'{"value":"[[[{{{\\\"still-a-string"}\n'
        self.assertEqual(security._json_max_nesting(raw), 1)

    def test_invalid_utf8_manifest_fails_closed(self) -> None:
        bundle = self.root / "invalid-utf8"
        (bundle / "artifacts").mkdir(parents=True)
        (bundle / base.DOSSIER_FILENAME).write_bytes(b"\xff\xfe")
        with self.assertRaises(base.DossierError):
            security.verify_dossier_hardened(bundle)

    def test_manifest_size_limit_is_preflighted(self) -> None:
        bundle = self.root / "large-manifest"
        (bundle / "artifacts").mkdir(parents=True)
        manifest = bundle / base.DOSSIER_FILENAME
        with manifest.open("wb") as handle:
            handle.truncate(base.MAX_MANIFEST_BYTES + 1)
        with self.assertRaisesRegex(base.DossierError, "maximum size"):
            security.preflight_dossier(bundle)

    def test_artifact_tree_entry_limit_is_fail_closed(self) -> None:
        bundle = self.root / "many"
        root = bundle / "artifacts"
        root.mkdir(parents=True)
        (bundle / base.DOSSIER_FILENAME).write_text("{}\n", encoding="utf-8")
        for index in range(4):
            (root / f"{index}.txt").write_text("x", encoding="utf-8")
        with patch.object(security, "MAX_TREE_ENTRIES", 3):
            with self.assertRaisesRegex(base.DossierError, "entry count"):
                security.preflight_dossier(bundle)

    def test_artifact_tree_depth_limit_is_fail_closed(self) -> None:
        bundle = self.root / "deep-tree"
        root = bundle / "artifacts/a/b"
        root.mkdir(parents=True)
        (bundle / base.DOSSIER_FILENAME).write_text("{}\n", encoding="utf-8")
        (root / "x.txt").write_text("x", encoding="utf-8")
        with patch.object(security, "MAX_TREE_DEPTH", 2):
            with self.assertRaisesRegex(base.DossierError, "maximum depth"):
                security.preflight_dossier(bundle)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO unavailable")
    def test_special_files_are_rejected(self) -> None:
        bundle = self.root / "fifo"
        root = bundle / "artifacts"
        root.mkdir(parents=True)
        (bundle / base.DOSSIER_FILENAME).write_text("{}\n", encoding="utf-8")
        os.mkfifo(root / "pipe")
        with self.assertRaisesRegex(base.DossierError, "unsupported filesystem entry"):
            security.preflight_dossier(bundle)

    def test_change_during_verification_is_detected(self) -> None:
        bundle = self._export()
        original = base.verify_dossier

        def verify_then_mutate(path: Path) -> dict[str, object]:
            report = original(path)
            artifact = bundle / "artifacts/results/result.json"
            artifact.write_text("changed after base verification\n", encoding="utf-8")
            return report

        with patch.object(security._base, "verify_dossier", side_effect=verify_then_mutate):
            with self.assertRaisesRegex(base.DossierError, "changed during verification"):
                security.verify_dossier_hardened(bundle)

    def test_failed_export_leaves_no_staging_directory(self) -> None:
        with self.assertRaisesRegex(base.DossierError, "matches excluded source"):
            security.export_dossier_hardened(
                source=self.source,
                artifacts={"source-copy.txt": self.source},
                output=self.root / "rejected",
                software_commit=self.commit,
            )
        self.assertEqual(list(self.root.glob(f"{security.TEMP_PREFIX}*")), [])

    def test_source_limit_is_enforced(self) -> None:
        with patch.object(base, "MAX_SOURCE_BYTES", 4):
            with self.assertRaisesRegex(base.DossierError, "maximum size"):
                security.export_dossier_hardened(
                    source=self.source,
                    artifacts={"result.json": self.artifact},
                    output=self.root / "too-large",
                    software_commit=self.commit,
                )

    def test_artifact_count_limit_is_enforced(self) -> None:
        artifacts = {f"{index:03d}.json": self.artifact for index in range(base.MAX_ARTIFACTS + 1)}
        with self.assertRaisesRegex(base.DossierError, "provide 1 to"):
            security.export_dossier_hardened(
                source=self.source,
                artifacts=artifacts,
                output=self.root / "too-many",
                software_commit=self.commit,
            )

    def test_purge_dry_run_preserves_data(self) -> None:
        candidate = self.root / f"{security.TEMP_PREFIX}dry"
        candidate.mkdir()
        (candidate / "secret.tmp").write_text("temporary", encoding="utf-8")
        report = security.purge_temporary_data(self.root, dry_run=True)
        self.assertEqual(report["status"], "DRY_RUN")
        self.assertTrue(candidate.exists())

    def test_purge_removes_only_prefixed_children(self) -> None:
        candidate = self.root / f"{security.TEMP_PREFIX}old"
        candidate.mkdir()
        (candidate / "secret.tmp").write_text("temporary", encoding="utf-8")
        retained = self.root / "operator-data"
        retained.mkdir()
        (retained / "keep.txt").write_text("keep", encoding="utf-8")
        report = security.purge_temporary_data(self.root, dry_run=False)
        self.assertEqual(report["status"], "PURGED")
        self.assertFalse(candidate.exists())
        self.assertTrue((retained / "keep.txt").exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_purge_unlinks_symlink_without_following_target(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        protected = outside / "protected.txt"
        protected.write_text("keep", encoding="utf-8")
        link = self.root / f"{security.TEMP_PREFIX}link"
        link.symlink_to(outside, target_is_directory=True)
        security.purge_temporary_data(self.root, dry_run=False)
        self.assertFalse(link.exists())
        self.assertTrue(protected.exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlink_workspace_is_rejected(self) -> None:
        workspace = self.root / "workspace"
        workspace.mkdir()
        link = self.root / "workspace-link"
        link.symlink_to(workspace, target_is_directory=True)
        with self.assertRaisesRegex(base.DossierError, "workspace must be"):
            security.purge_temporary_data(link, dry_run=True)

    def test_purge_entry_budget_fails_before_deletion(self) -> None:
        candidate = self.root / f"{security.TEMP_PREFIX}budget"
        candidate.mkdir()
        for index in range(3):
            (candidate / f"{index}.tmp").write_text("x", encoding="utf-8")
        with patch.object(security, "MAX_PURGE_ENTRIES", 2):
            with self.assertRaisesRegex(base.DossierError, "purge entry count"):
                security.purge_temporary_data(self.root, dry_run=False)
        self.assertTrue(candidate.exists())
        self.assertEqual(len(list(candidate.iterdir())), 3)

    def test_limits_are_machine_readable(self) -> None:
        limits = security.resource_limits()
        self.assertEqual(limits["hardening_profile"], security.HARDENING_PROFILE)
        self.assertEqual(limits["max_artifacts"], base.MAX_ARTIFACTS)
        json.dumps(limits, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
