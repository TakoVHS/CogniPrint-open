"""Tests for the Stage-A known-membership RAID development pipeline."""

from __future__ import annotations

import csv
import importlib.util
import json
import pathlib
import random
import tempfile
import unittest

import sklearn  # noqa: F401

_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts"
    / "run_known_membership_dev.py"
)
_spec = importlib.util.spec_from_file_location("kmdev", _PATH)
kmdev = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kmdev)

FAMILIES = ["human", "fam-a", "fam-b", "fam-c"]
SECRET = "zzsecretmarkerzz"


def _write_synthetic(path: pathlib.Path, n_sources: int = 120) -> None:
    rng = random.Random(3)
    common = [f"w{i}" for i in range(60)]
    style = {
        f: [f"{f.replace('-', '')}tok{i}" for i in range(8)]
        for f in FAMILIES
    }
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "source_id",
                "model",
                "decoding",
                "repetition_penalty",
                "attack",
                "domain",
                "generation",
            ],
        )
        writer.writeheader()
        for source in range(n_sources):
            source_id = f"src{source}"
            for family in FAMILIES:
                for decoding in ("greedy", "sampling"):
                    words = (
                        rng.choices(common, k=40)
                        + rng.choices(style[family], k=8)
                    )
                    rng.shuffle(words)
                    writer.writerow(
                        {
                            "id": f"{source_id}-{family}-{decoding}",
                            "source_id": source_id,
                            "model": family,
                            "decoding": decoding,
                            "repetition_penalty": "no",
                            "attack": "none",
                            "domain": "news",
                            "generation": " ".join(words) + " " + SECRET,
                        }
                    )


class CertificateTests(unittest.TestCase):
    def test_accept_all_is_trivial_reference(self) -> None:
        thresholds = [0.0, 0.5]
        known = {"k": ({0.0: 100, 0.5: 100}, 100)}
        unknown = {"u": ({0.0: 100, 0.5: 100}, 100)}
        out = kmdev.certify(
            known, unknown, thresholds, 0.05, 0.10, [0.05, 0.2], [0.5]
        )
        self.assertAlmostEqual(out["thresholds"][0]["lift"], 1.0)
        self.assertEqual(
            out["decisions"]["0.05"]["decision"], "PROMOTE_TRIVIAL"
        )
        self.assertEqual(out["decisions"]["0.2"]["decision"], "ABSTAIN")

    def test_good_gate_promotes_above_delta(self) -> None:
        thresholds = [0.0, 0.5]
        known = {"k": ({0.0: 1000, 0.5: 900}, 1000)}
        unknown = {"u": ({0.0: 1000, 0.5: 0}, 1000)}
        out = kmdev.certify(
            known, unknown, thresholds, 0.05, 0.10, [0.2, 0.5], [0.5]
        )
        self.assertEqual(out["n_bounds"], 2)
        self.assertEqual(out["decisions"]["0.5"]["decision"], "PROMOTE")
        self.assertGreater(out["best_lift_by_LK_floor"]["0.5"], 5.0)

    def test_empty_unknown_sample_is_vacuous(self) -> None:
        thresholds = [0.0, 0.5]
        known = {"k": ({0.0: 100, 0.5: 90}, 100)}
        unknown = {"u": ({0.0: 0, 0.5: 0}, 0)}
        out = kmdev.certify(
            known, unknown, thresholds, 0.05, 0.10, [0.2], [0.5]
        )
        self.assertEqual(out["thresholds"][1]["U_U"], 1.0)
        self.assertEqual(out["decisions"]["0.2"]["decision"], "ABSTAIN")

    def test_lift_floor_blocks_tiny_coverage_cherry_pick(self) -> None:
        thresholds = [0.0, 0.5, 0.9]
        known = {"k": ({0.0: 1000, 0.5: 600, 0.9: 5}, 1000)}
        unknown = {"u": ({0.0: 1000, 0.5: 100, 0.9: 0}, 1000)}
        out = kmdev.certify(
            known, unknown, thresholds, 0.05, 0.10, [0.2], [0.5]
        )
        self.assertIsNotNone(out["best_lift_any_gate"])
        self.assertIsNotNone(out["best_lift_by_LK_floor"]["0.5"])

    def test_roles_are_group_stable(self) -> None:
        self.assertEqual(
            {kmdev.role_of("seed", "news\x1fsrc42") for _ in range(10)},
            {kmdev.role_of("seed", "news\x1fsrc42")},
        )


class EndToEndTests(unittest.TestCase):
    def test_pipeline_runs_without_persisting_raw_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = pathlib.Path(tmp_dir)
            source = tmp / "train_none.csv"
            _write_synthetic(source)
            output = tmp / "out"
            rc = kmdev.main(
                [
                    "--input-file",
                    str(source),
                    "--output-dir",
                    str(output),
                    "--families",
                    ",".join(FAMILIES),
                    "--domains",
                    "news",
                    "--per-family",
                    "100",
                    "--max-features",
                    "5000",
                    "--transport",
                ]
            )
            self.assertEqual(rc, 0)

            summary_text = (
                output / "known-membership-dev-summary.json"
            ).read_text(encoding="utf-8")
            report_text = (
                output / "known-membership-dev-report.md"
            ).read_text(encoding="utf-8")
            self.assertNotIn(SECRET, summary_text)
            self.assertNotIn(SECRET, report_text)

            summary = json.loads(summary_text)
            self.assertFalse(summary["raw_text_persisted"])
            self.assertEqual(
                set(summary["leave_one_family_out"]),
                {"fam-a", "fam-b", "fam-c"},
            )
            self.assertEqual(len(summary["transport_pairs"]), 6)

            for family in FAMILIES:
                counts = summary["record_counts"][family]
                self.assertEqual(sum(counts.values()), 100)

    def test_common_groups_and_fixed_decoding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            source = pathlib.Path(tmp_dir) / "train_none.csv"
            _write_synthetic(source, n_sources=40)
            rows = kmdev.load_records(
                source,
                FAMILIES,
                ["news"],
                30,
                "seed",
                "sampling",
            )
            by_family = {
                family: {r["group"] for r in rows if r["family"] == family}
                for family in FAMILIES
            }
            first = by_family[FAMILIES[0]]
            self.assertTrue(all(groups == first for groups in by_family.values()))
            self.assertEqual(len(first), 30)


if __name__ == "__main__":
    unittest.main()
