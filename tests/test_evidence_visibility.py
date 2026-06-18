from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_evidence_visibility import load_json


class EvidenceVisibilityTests(unittest.TestCase):
    def test_load_json_reads_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.json"
            path.write_text(json.dumps({"status": "ok"}), encoding="utf-8")
            payload = load_json(path)
            self.assertEqual(payload["status"], "ok")


if __name__ == "__main__":
    unittest.main()
