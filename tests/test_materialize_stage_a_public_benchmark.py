from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "materialize_stage_a_public_benchmark.py"
SPEC = importlib.util.spec_from_file_location("stage_a_materializer", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("cannot load Stage A materializer")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


FIELDS = [
    "sample_id",
    "baseline_sample_id",
    "file_path",
    "source_url",
    "acquisition_date",
    "release_status",
]


class StageAPublicBenchmarkMaterializerTests(unittest.TestCase):
    def test_materializes_development_only_records_with_real_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            (data / "base.txt").write_text("alpha", encoding="utf-8")
            (data / "variant.txt").write_text("beta", encoding="utf-8")
            metadata = root / "metadata.csv"
            with metadata.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerow(
                    {
                        "sample_id": "base",
                        "baseline_sample_id": "",
                        "file_path": "data/base.txt",
                        "source_url": "https://example.invalid/base",
                        "acquisition_date": "2026-01-01",
                        "release_status": "released",
                    }
                )
                writer.writerow(
                    {
                        "sample_id": "variant",
                        "baseline_sample_id": "base",
                        "file_path": "data/variant.txt",
                        "source_url": "https://example.invalid/base",
                        "acquisition_date": "2026-01-01",
                        "release_status": "released",
                    }
                )

            rows = MODULE.materialize(root, metadata)
            self.assertEqual(len(rows), 2)
            for row in rows:
                self.assertEqual(row["stage"], "STAGE_A_DEVELOPMENT")
                self.assertTrue(row["development_visibility"])
                self.assertFalse(row["evaluation_visibility"])
                self.assertEqual(row["reference_set_membership"], "DEVELOPMENT_ONLY")
                self.assertRegex(row["content_sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(row["lineage_group_hash"], r"^[0-9a-f]{64}$")
                self.assertRegex(row["origin_record_hash"], r"^[0-9a-f]{64}$")
            self.assertEqual(rows[0]["lineage_group_hash"], rows[1]["lineage_group_hash"])

    def test_unreleased_rows_are_not_materialized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x.txt").write_text("x", encoding="utf-8")
            metadata = root / "metadata.csv"
            with metadata.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerow(
                    {
                        "sample_id": "x",
                        "baseline_sample_id": "",
                        "file_path": "x.txt",
                        "source_url": "https://example.invalid/x",
                        "acquisition_date": "2026-01-01",
                        "release_status": "draft",
                    }
                )
            with self.assertRaisesRegex(ValueError, "no released benchmark rows"):
                MODULE.materialize(root, metadata)

    def test_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata = root / "metadata.csv"
            with metadata.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerow(
                    {
                        "sample_id": "x",
                        "baseline_sample_id": "",
                        "file_path": "../outside.txt",
                        "source_url": "https://example.invalid/x",
                        "acquisition_date": "2026-01-01",
                        "release_status": "released",
                    }
                )
            with self.assertRaisesRegex(ValueError, "unsafe file_path"):
                MODULE.materialize(root, metadata)


if __name__ == "__main__":
    unittest.main()
