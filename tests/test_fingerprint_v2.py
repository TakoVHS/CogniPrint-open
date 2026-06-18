from __future__ import annotations

import unittest

from cogniprint.fingerprint import (
    FEATURE_NAMES,
    CognitiveFingerprint,
    apply_synonym_replacements,
    perturb_stability_test,
    remove_stop_words,
    rotate_sentences,
)


class CognitiveFingerprintV2Tests(unittest.TestCase):
    def test_vector_has_stable_twelve_feature_order(self) -> None:
        text = "CogniPrint studies compact statistical profiles. It keeps claims bounded."
        profile = CognitiveFingerprint(text, language="en")

        self.assertEqual(len(FEATURE_NAMES), 12)
        self.assertEqual(len(profile.vector(normalized=False)), 12)
        self.assertEqual(len(profile.vector(normalized=True)), 12)
        self.assertEqual(FEATURE_NAMES[0], "mean_word_length")
        self.assertEqual(FEATURE_NAMES[-1], "flesch_reading_ease")

    def test_identical_profiles_have_zero_distance(self) -> None:
        text = "Stable text profiles should compare deterministically."
        left = CognitiveFingerprint(text, language="en").vector()
        right = CognitiveFingerprint(text, language="en").vector()

        self.assertAlmostEqual(CognitiveFingerprint.distance(left, right, "cosine"), 0.0, places=9)
        self.assertAlmostEqual(CognitiveFingerprint.distance(left, right, "euclidean"), 0.0, places=9)

    def test_controlled_perturbation_helpers_are_deterministic(self) -> None:
        text = "The method studies evidence. The evidence remains bounded."

        replaced = apply_synonym_replacements(text, {"method": "framework"})
        rotated = rotate_sentences(text)
        without_stop_words = remove_stop_words(text, language="en")

        self.assertIn("framework", replaced)
        self.assertTrue(rotated.startswith("The evidence"))
        self.assertNotIn(" The ", f" {without_stop_words} ")

    def test_stability_summary_preserves_descriptive_boundary(self) -> None:
        baseline = "CogniPrint studies reproducible statistical profiles of text."
        variants = [
            "CogniPrint studies reproducible statistical text profiles.",
            "Reproducible statistical profiles of text are studied by CogniPrint.",
        ]

        summary = perturb_stability_test(baseline, variants, metric="cosine")

        self.assertEqual(summary["variant_count"], 2)
        self.assertEqual(summary["sample_count"], 2)
        self.assertEqual(summary["readiness_boundary"], "descriptive_only")
        self.assertIn("distances", summary)


if __name__ == "__main__":
    unittest.main()
