from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from cogniprint.dossier import (
    DOSSIER_FILENAME,
    DossierError,
    _canonical_bytes,
    export_dossier,
    main,
    verify_dossier,
)


class EvidenceDossierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "source.txt"
        self.source.write_text("Sensitive source text that must stay outside the bundle.\n", encoding="utf-8")
        self.artifact = self.root / "analysis.json"
        self.artifact.write_text('{"signal":"descriptive","value":0.25}\n', encoding="utf-8")
        self.configuration = self.root / "config.json"
        self.configuration.write_text('{"mode":"development"}\n', encoding="utf-8")
        self.commit = "a" * 40

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _export(self, name: str = "bundle", *, configuration: bool = False) -> Path:
        output = self.root / name
        export_dossier(
            source=self.source,
            artifacts={"results/analysis.json": self.artifact},
            configuration=self.configuration if configuration else None,
            software_commit=self.commit,
            output=output,
        )
        return output

    def _manifest(self, bundle: Path) -> dict[str, object]:
        return json.loads((bundle / DOSSIER_FILENAME).read_text(encoding="utf-8"))

    def _rewrite_manifest(self, bundle: Path, manifest: dict[str, object]) -> None:
        (bundle / DOSSIER_FILENAME).write_bytes(_canonical_bytes(manifest))

    def test_export_and_offline_verify(self) -> None:
        bundle = self._export()
        report = verify_dossier(bundle)
        self.assertEqual(report["status"], "VERIFIED")
        self.assertTrue(report["offline"])
        self.assertEqual(report["artifact_count"], 1)
        self.assertFalse((bundle / "source.txt").exists())
        self.assertFalse((bundle / "config.json").exists())
        self.assertFalse(self._manifest(bundle)["source"]["included"])

    def test_exports_are_byte_identical(self) -> None:
        first = self._export("first", configuration=True)
        second = self._export("second", configuration=True)
        self.assertEqual((first / DOSSIER_FILENAME).read_bytes(), (second / DOSSIER_FILENAME).read_bytes())
        self.assertEqual(
            (first / "artifacts/results/analysis.json").read_bytes(),
            (second / "artifacts/results/analysis.json").read_bytes(),
        )

    def test_one_byte_artifact_mutation_fails(self) -> None:
        bundle = self._export()
        artifact = bundle / "artifacts/results/analysis.json"
        data = bytearray(artifact.read_bytes())
        data[-2] ^= 1
        artifact.write_bytes(data)
        with self.assertRaisesRegex(DossierError, "artifact verification failed"):
            verify_dossier(bundle)

    def test_unknown_schema_fails(self) -> None:
        bundle = self._export()
        manifest = self._manifest(bundle)
        manifest["$schema"] = "urn:cogniprint:evidence-dossier:999"
        self._rewrite_manifest(bundle, manifest)
        with self.assertRaisesRegex(DossierError, "unknown or unsupported"):
            verify_dossier(bundle)

    def test_missing_required_field_fails(self) -> None:
        bundle = self._export()
        manifest = self._manifest(bundle)
        del manifest["software"]
        self._rewrite_manifest(bundle, manifest)
        with self.assertRaisesRegex(DossierError, "keys mismatch"):
            verify_dossier(bundle)

    def test_duplicate_json_key_fails(self) -> None:
        bundle = self._export()
        path = bundle / DOSSIER_FILENAME
        text = path.read_text(encoding="utf-8")
        text = text.replace('"schema_version":1', '"schema_version":1,"schema_version":1', 1)
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(DossierError, "duplicate JSON key"):
            verify_dossier(bundle)

    def test_noncanonical_json_fails(self) -> None:
        bundle = self._export()
        manifest = self._manifest(bundle)
        (bundle / DOSSIER_FILENAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(DossierError, "not in canonical JSON form"):
            verify_dossier(bundle)

    def test_path_traversal_fails(self) -> None:
        bundle = self._export()
        manifest = self._manifest(bundle)
        manifest["artifacts"][0]["path"] = "../escape.json"
        self._rewrite_manifest(bundle, manifest)
        with self.assertRaisesRegex(DossierError, "unsafe artifact path"):
            verify_dossier(bundle)

    def test_extra_artifact_fails(self) -> None:
        bundle = self._export()
        (bundle / "artifacts/extra.txt").write_text("extra", encoding="utf-8")
        with self.assertRaisesRegex(DossierError, "artifact inventory mismatch"):
            verify_dossier(bundle)

    def test_export_rejects_source_content_as_artifact(self) -> None:
        with self.assertRaisesRegex(DossierError, "matches excluded source"):
            export_dossier(
                source=self.source,
                artifacts={"copied-source.txt": self.source},
                software_commit=self.commit,
                output=self.root / "rejected",
            )

    def test_existing_output_fails(self) -> None:
        output = self.root / "existing"
        output.mkdir()
        with self.assertRaisesRegex(DossierError, "output already exists"):
            export_dossier(
                source=self.source,
                artifacts={"analysis.json": self.artifact},
                software_commit=self.commit,
                output=output,
            )

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlink_artifact_fails(self) -> None:
        link = self.root / "artifact-link"
        link.symlink_to(self.artifact)
        with self.assertRaisesRegex(DossierError, "must not be a symlink"):
            export_dossier(
                source=self.source,
                artifacts={"analysis.json": link},
                software_commit=self.commit,
                output=self.root / "symlink-rejected",
            )

    def test_cli_export_and_verify(self) -> None:
        bundle = self.root / "cli-bundle"
        self.assertEqual(
            main(
                [
                    "export",
                    "--source",
                    str(self.source),
                    "--artifact",
                    f"analysis.json={self.artifact}",
                    "--software-commit",
                    self.commit,
                    "--output",
                    str(bundle),
                ]
            ),
            0,
        )
        self.assertEqual(main(["verify", "--bundle", str(bundle)]), 0)


if __name__ == "__main__":
    unittest.main()
