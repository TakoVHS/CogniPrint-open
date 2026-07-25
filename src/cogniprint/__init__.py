"""CogniPrint local research workstation."""

from .analysis import analyze_text, compare_profiles
from .evidence_policy import (
    ClaimDecision,
    ClaimKind,
    ClaimLevel,
    EvidenceClass,
    EvidenceContext,
    LimitationCode,
    evaluate_claim,
)
from .fingerprint import CognitiveFingerprint, perturb_stability_test
from .provenance_conflict import (
    AttestationStatus,
    ConflictResult,
    ConflictStatus,
    classify_conflict,
)

__all__ = [
    "AttestationStatus",
    "ClaimDecision",
    "ClaimKind",
    "ClaimLevel",
    "CognitiveFingerprint",
    "ConflictResult",
    "ConflictStatus",
    "EvidenceClass",
    "EvidenceContext",
    "LimitationCode",
    "analyze_text",
    "classify_conflict",
    "compare_profiles",
    "evaluate_claim",
    "perturb_stability_test",
]
__version__ = "0.1.0"
