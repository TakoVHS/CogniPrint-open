from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_stage_b_preregistration_package.py"
SPEC = importlib.util.spec_from_file_location("stage_b_package_validator", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class StageBPreregistrationPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.prereg = json.loads((REPO_ROOT / validator.PREREG_PATH).read_text())
        cls.custody = json.loads((REPO_ROOT / validator.CUSTODY_PATH).read_text())

    def test_current_hold_package_passes(self) -> None:
        result = validator.validate_package(REPO_ROOT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["package_status"], "HOLD")
        self.assertEqual(result["stage_b_status"], "NOT_AUTHORISED_TO_START")

    def test_ready_status_cannot_be_faked_by_editing_status_only(self) -> None:
        payload = copy.deepcopy(self.prereg)
        payload["status"] = "READY_TO_SUBMIT"
        with self.assertRaises(validator.ValidationError):
            validator.validate_prereg_template(payload)

    def test_registration_fields_cannot_be_prepopulated_in_template(self) -> None:
        payload = copy.deepcopy(self.prereg)
        payload["registration"]["registration_id"] = "fake-registration"
        with self.assertRaises(validator.ValidationError):
            validator.validate_prereg_template(payload)

    def test_stage_b_authorisation_is_rejected_in_template(self) -> None:
        payload = copy.deepcopy(self.prereg)
        payload["execution_gates"]["stage_b_execution_authorised"] = True
        with self.assertRaises(validator.ValidationError):
            validator.validate_prereg_template(payload)

    def test_custody_template_cannot_claim_sealed_state(self) -> None:
        payload = copy.deepcopy(self.custody)
        payload["status"] = "SEALED"
        with self.assertRaises(validator.ValidationError):
            validator.validate_custody_template(payload)

    def test_custody_template_cannot_claim_reveal(self) -> None:
        payload = copy.deepcopy(self.custody)
        payload["reveal_gate"]["reveal_authorised"] = True
        with self.assertRaises(validator.ValidationError):
            validator.validate_custody_template(payload)

    def test_templates_reject_forbidden_ground_truth_fields(self) -> None:
        payload = copy.deepcopy(self.custody)
        payload["true_class"] = "hidden-family"
        with self.assertRaises(validator.ValidationError):
            validator.validate_custody_template(payload)

    def test_sanitized_release_requires_plan_and_validator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            (root / "config/public-release.json").write_text(
                json.dumps({"include": ["challenge-001/**", "schemas/**", "tests/**"]})
            )
            with self.assertRaises(validator.ValidationError):
                validator.validate_public_release(root)


if __name__ == "__main__":
    unittest.main()
