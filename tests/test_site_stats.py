from __future__ import annotations

import unittest
from pathlib import Path

from scripts.generate_site_stats import build_stats


class SiteStatsTests(unittest.TestCase):
    def test_build_stats_preserves_readiness_boundary(self) -> None:
        root = Path(__file__).resolve().parents[1]
        payload = build_stats(root)

        self.assertEqual(payload["schema_version"], "site-stats-v1")
        self.assertEqual(payload["readiness"], "descriptive_only")
        self.assertEqual(payload["external_review"]["valid_review_count"], 0)
        self.assertEqual(payload["external_review"]["minimum_required_valid_reviews"], 1)
        self.assertIn("threshold_policy", payload["reviewer_validation_dry_run"])
        self.assertIn("No fixed universal threshold", payload["reviewer_validation_dry_run"]["threshold_policy"])


if __name__ == "__main__":
    unittest.main()
