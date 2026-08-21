from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_project_status_exact_gate.py"
spec = importlib.util.spec_from_file_location("exact_status_gate", SCRIPT)
assert spec and spec.loader
exact_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exact_gate)


class ExactStatusGateTests(unittest.TestCase):
    def test_missing_expected_head_fails_before_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(exact_gate.main(["--root", temporary]), 2)

    def test_compile_python_does_not_create_source_cache(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in ("src", "scripts", "tests"):
                path = root / directory / "sample.py"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("value = 1\n", encoding="utf-8")
            destination = root / "isolated-pyc"
            exact_gate.compile_python(root, destination)
            self.assertEqual(len(list(destination.glob("*.pyc"))), 3)
            self.assertEqual(list(root.glob("src/**/__pycache__")), [])
            self.assertEqual(list(root.glob("scripts/**/__pycache__")), [])
            self.assertEqual(list(root.glob("tests/**/__pycache__")), [])

    def test_strict_json_rejects_non_finite_values(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "report.json"
            path.write_text('{"decision": NaN}\n', encoding="utf-8")
            with self.assertRaisesRegex(exact_gate.GateError, "non-finite"):
                exact_gate.strict_json(path)

    def test_readiness_escalation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "report.json"

            def fake_run(_root: Path, *command: str, capture: bool = False) -> str:
                del command, capture
                destination.write_text('{"decision": "inferential_candidate"}\n', encoding="utf-8")
                return ""

            with mock.patch.object(exact_gate, "run", side_effect=fake_run):
                with self.assertRaisesRegex(exact_gate.GateError, "unexpected readiness"):
                    exact_gate.derive_readiness(root, destination)


if __name__ == "__main__":
    unittest.main()
