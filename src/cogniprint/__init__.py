"""CogniPrint local research workstation."""

from .analysis import analyze_text, compare_profiles
from .fingerprint import CognitiveFingerprint, perturb_stability_test

__all__ = ["CognitiveFingerprint", "analyze_text", "compare_profiles", "perturb_stability_test"]
__version__ = "0.1.0"
