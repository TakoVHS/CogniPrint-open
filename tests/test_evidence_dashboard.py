from __future__ import annotations

import unittest

from scripts.check_evidence_dashboard import require


class EvidenceDashboardTests(unittest.TestCase):
    def test_require_appends_error_on_false_condition(self) -> None:
        errors: list[str] = []
        require(errors, False, "missing")
        self.assertEqual(errors, ["missing"])

    def test_require_keeps_errors_empty_on_true_condition(self) -> None:
        errors: list[str] = []
        require(errors, True, "missing")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
