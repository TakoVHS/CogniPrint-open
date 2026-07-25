from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_research_lock_001.py"
SPEC = importlib.util.spec_from_file_location("research_lock_001", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("cannot load research lock builder")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ResearchLock001Tests(unittest.TestCase):
    def test_lock_is_deterministic_and_order_independent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            (root / "b.txt").write_text("beta", encoding="utf-8")
            left = MODULE.build_lock(root, ["a.txt", "b.txt"], commit="abc123")
            right = MODULE.build_lock(root, ["b.txt", "a.txt"], commit="abc123")
            self.assertEqual(left, right)
            self.assertTrue(MODULE.verify_lock(root, left)["ok"])

    def test_tampering_changes_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "protocol.md"
            target.write_text("frozen", encoding="utf-8")
            lock = MODULE.build_lock(root, ["protocol.md"])
            target.write_text("changed", encoding="utf-8")
            result = MODULE.verify_lock(root, lock)
            self.assertFalse(result["ok"])
            self.assertIn("file hash mismatch", result["reason"])

    def test_duplicate_paths_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x").write_text("x", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                MODULE.build_lock(root, ["x", "x"])

    def test_parent_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "unsafe"):
                MODULE.build_lock(root, ["../escape"])

    def test_fake_signed_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x").write_text("x", encoding="utf-8")
            lock = MODULE.build_lock(root, ["x"])
            lock["signature_status"] = "SIGNED"
            result = MODULE.verify_lock(root, lock)
            self.assertFalse(result["ok"])
            self.assertEqual(result["reason"], "unsupported signature status")


if __name__ == "__main__":
    unittest.main()
