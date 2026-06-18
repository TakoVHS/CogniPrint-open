from __future__ import annotations

import importlib.util
import io
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "secret_scan.py"
SPEC = importlib.util.spec_from_file_location("secret_scan", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
secret_scan = importlib.util.module_from_spec(SPEC)
sys.modules["secret_scan"] = secret_scan
SPEC.loader.exec_module(secret_scan)


class SecretScanTests(unittest.TestCase):
    def test_history_deleted_file_attribution_uses_old_path(self) -> None:
        synthetic_rules = (secret_scan.Rule("synthetic_secret", re.compile("MATCH_ME")),)
        with mock.patch.object(secret_scan, "RULES", synthetic_rules):
            findings = secret_scan.scan_history_stream(
                [
                    "commit 0123456789abcdef\n",
                    "diff --git a/docs/private.env b/docs/private.env\n",
                    "deleted file mode 100644\n",
                    "--- a/docs/private.env\n",
                    "+++ /dev/null\n",
                    "-MATCH_ME\n",
                ]
            )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule_name, "synthetic_secret")
        self.assertIn("history:0123456789ab:docs/private.env", findings[0].location)

    def test_history_scan_raises_runtime_error_when_stdout_pipe_is_missing(self) -> None:
        class FakeProcess:
            stdout = None
            stderr = io.StringIO("missing stdout")

            def wait(self) -> int:
                return 0

        with tempfile.TemporaryDirectory() as temporary_directory:
            with mock.patch.object(secret_scan.subprocess, "Popen", return_value=FakeProcess()):
                with self.assertRaisesRegex(RuntimeError, "missing stdout"):
                    secret_scan.scan_history(Path(temporary_directory))


if __name__ == "__main__":
    unittest.main()
