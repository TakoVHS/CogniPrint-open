from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_claims_drift import find_matches
from scripts.check_prereg_compliance import digest_text
from scripts.generate_interpretation_memo import effect_label
from scripts.preregister_wave005 import is_placeholder


class PreregistrationHelpersTests(unittest.TestCase):
    def test_placeholder_detection(self) -> None:
        self.assertTrue(is_placeholder("Status:\n- placeholder only\n"))
        self.assertFalse(is_placeholder("# Pre-registration\nFilled content.\n"))

    def test_digest_is_stable(self) -> None:
        self.assertEqual(digest_text("abc"), digest_text("abc"))


class InterpretationMemoHelpersTests(unittest.TestCase):
    def test_effect_label_thresholds(self) -> None:
        self.assertEqual(effect_label(0.1), "negligible")
        self.assertEqual(effect_label(0.3), "small")
        self.assertEqual(effect_label(0.7), "medium")
        self.assertEqual(effect_label(1.2), "large")


class ClaimsDriftAdditionalTests(unittest.TestCase):
    def test_additional_file_scan_flags_dangerous_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "memo.md"
            path.write_text("This is a production ready detector.", encoding="utf-8")
            errors = find_matches(root, ["memo.md"])
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
