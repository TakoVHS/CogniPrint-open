from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_challenge_leakage.py"
SPEC = importlib.util.spec_from_file_location("challenge_leakage", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("cannot load challenge leakage checker")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def row(sample_id: str, content_hash: str, prompt_hash: str) -> dict[str, str]:
    return {
        "sample_id": sample_id,
        "content_sha256": content_hash,
        "prompt_hash": prompt_hash,
    }


class ChallengeLeakageTests(unittest.TestCase):
    def test_disjoint_stage_a_and_b_pass(self) -> None:
        stage_a = [row("a-1", "hash-a-1", "prompt-family-1")]
        stage_b = [row("b-1", "hash-b-1", "prompt-family-1")]
        report = MODULE.audit(stage_a, stage_b)
        self.assertEqual(report["freeze_gate"], "PASS")
        self.assertEqual(report["sample_id_overlap"], 0)
        self.assertEqual(report["content_hash_overlap"], 0)
        self.assertEqual(report["prompt_hash_overlap"], 1)
        self.assertEqual(report["prompt_overlap_policy"], "REPORT_ONLY_UNTIL_PROTOCOL_FREEZE")

    def test_sample_id_overlap_blocks_freeze(self) -> None:
        stage_a = [row("same", "hash-a", "p-a")]
        stage_b = [row("same", "hash-b", "p-b")]
        report = MODULE.audit(stage_a, stage_b)
        self.assertEqual(report["freeze_gate"], "BLOCKED")
        self.assertIn("SAMPLE_ID_OVERLAP", report["blocking_reasons"])

    def test_content_hash_overlap_blocks_freeze(self) -> None:
        stage_a = [row("a", "same-hash", "p-a")]
        stage_b = [row("b", "same-hash", "p-b")]
        report = MODULE.audit(stage_a, stage_b)
        self.assertEqual(report["freeze_gate"], "BLOCKED")
        self.assertIn("CONTENT_HASH_OVERLAP", report["blocking_reasons"])

    def test_duplicate_content_within_stage_blocks_freeze(self) -> None:
        stage_a = [row("a-1", "dup", "p-1"), row("a-2", "dup", "p-2")]
        stage_b = [row("b-1", "clean", "p-3")]
        report = MODULE.audit(stage_a, stage_b)
        self.assertEqual(report["freeze_gate"], "BLOCKED")
        self.assertIn("DUPLICATE_CONTENT_HASH_WITHIN_STAGE", report["blocking_reasons"])


if __name__ == "__main__":
    unittest.main()
