"""Machine-readable evidence classes and claim firewall for CogniPrint.

The policy deliberately separates what CogniPrint directly measures from what a
statistical model infers, what an external provenance source attests, and what
remains unknown.  The default policy is conservative: model-family inference is
disabled until a dedicated benchmark/calibration gate is explicitly enabled.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Iterable


POLICY_VERSION = "cogniprint-claim-firewall-v1"


class EvidenceClass(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    ATTESTED = "ATTESTED"
    UNKNOWN = "UNKNOWN"


class ClaimLevel(IntEnum):
    NONE = 0
    SIMILARITY_ONLY = 1
    MODEL_FAMILY_CANDIDATE = 2
    CALIBRATED_ATTRIBUTION_CANDIDATE = 3
    ATTESTED_PROVENANCE = 4


class ClaimKind(str, Enum):
    MEASUREMENT = "measurement"
    SIMILARITY = "similarity"
    MODEL_FAMILY = "model_family"
    EXACT_MODEL = "exact_model"
    AUTHORSHIP = "authorship"
    ACTOR_OR_COMMISSIONER = "actor_or_commissioner"
    INTENT_OR_RESPONSIBILITY = "intent_or_responsibility"
    LEGAL_OR_FORENSIC_PROVENANCE = "legal_or_forensic_provenance"


HIGH_STAKES_DENY = {
    ClaimKind.AUTHORSHIP,
    ClaimKind.ACTOR_OR_COMMISSIONER,
    ClaimKind.INTENT_OR_RESPONSIBILITY,
    ClaimKind.LEGAL_OR_FORENSIC_PROVENANCE,
}


class LimitationCode(str, Enum):
    DESCRIPTIVE_ONLY = "DESCRIPTIVE_ONLY"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    SHORT_TEXT = "SHORT_TEXT"
    OUT_OF_DISTRIBUTION = "OUT_OF_DISTRIBUTION"
    UNSEEN_DOMAIN = "UNSEEN_DOMAIN"
    LOW_REFERENCE_COVERAGE = "LOW_REFERENCE_COVERAGE"
    UNCALIBRATED_SCORE = "UNCALIBRATED_SCORE"
    NO_EXTERNAL_PROVENANCE = "NO_EXTERNAL_PROVENANCE"
    CONFLICTING_PROVENANCE = "CONFLICTING_PROVENANCE"


@dataclass(frozen=True)
class EvidenceContext:
    """Evidence state consumed by the firewall.

    `attribution_enabled` must remain False until a dedicated benchmark,
    calibration and open-world review gate has been passed for the relevant
    scope.  It is intentionally not inferred from a model score.
    """

    strength: ClaimLevel = ClaimLevel.NONE
    minimum_evidence_met: bool = False
    in_distribution: bool = False
    calibrated: bool = False
    attribution_enabled: bool = False
    external_attestation: bool = False
    limitations: tuple[LimitationCode, ...] = ()


@dataclass(frozen=True)
class ClaimDecision:
    allowed: bool
    evidence_class: EvidenceClass
    requested_claim: ClaimKind
    maximum_level: ClaimLevel
    safe_statement: str
    limitations: tuple[LimitationCode, ...]
    policy_version: str = POLICY_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "allowed": self.allowed,
            "evidence_class": self.evidence_class.value,
            "requested_claim": self.requested_claim.value,
            "maximum_level": int(self.maximum_level),
            "safe_statement": self.safe_statement,
            "limitations": [item.value for item in self.limitations],
            "policy_version": self.policy_version,
        }


def _merge_limitations(*groups: Iterable[LimitationCode]) -> tuple[LimitationCode, ...]:
    seen: set[LimitationCode] = set()
    ordered: list[LimitationCode] = []
    for group in groups:
        for item in group:
            if item not in seen:
                seen.add(item)
                ordered.append(item)
    return tuple(ordered)


def evaluate_claim(kind: ClaimKind, context: EvidenceContext) -> ClaimDecision:
    """Return the strongest statement allowed by the current evidence state."""

    limitations = context.limitations

    if kind in HIGH_STAKES_DENY:
        return ClaimDecision(
            allowed=False,
            evidence_class=EvidenceClass.UNKNOWN,
            requested_claim=kind,
            maximum_level=min(context.strength, ClaimLevel.SIMILARITY_ONLY),
            safe_statement=(
                "CogniPrint does not establish this claim from content analysis. "
                "Independent, appropriately governed evidence is required."
            ),
            limitations=_merge_limitations(
                limitations,
                (LimitationCode.NO_EXTERNAL_PROVENANCE,),
            ),
        )

    if kind is ClaimKind.MEASUREMENT:
        if context.strength >= ClaimLevel.SIMILARITY_ONLY:
            return ClaimDecision(
                allowed=True,
                evidence_class=EvidenceClass.OBSERVED,
                requested_claim=kind,
                maximum_level=ClaimLevel.SIMILARITY_ONLY,
                safe_statement="Measured descriptive features are available for this artifact.",
                limitations=limitations,
            )
        return ClaimDecision(
            allowed=False,
            evidence_class=EvidenceClass.UNKNOWN,
            requested_claim=kind,
            maximum_level=ClaimLevel.NONE,
            safe_statement="Insufficient evidence to report a stable descriptive measurement.",
            limitations=_merge_limitations(limitations, (LimitationCode.INSUFFICIENT_EVIDENCE,)),
        )

    if kind is ClaimKind.SIMILARITY:
        if context.strength >= ClaimLevel.SIMILARITY_ONLY and context.minimum_evidence_met:
            return ClaimDecision(
                allowed=True,
                evidence_class=EvidenceClass.OBSERVED,
                requested_claim=kind,
                maximum_level=ClaimLevel.SIMILARITY_ONLY,
                safe_statement=(
                    "The artifact can be compared with the stated reference space; "
                    "similarity is not source identity."
                ),
                limitations=limitations,
            )
        return ClaimDecision(
            allowed=False,
            evidence_class=EvidenceClass.UNKNOWN,
            requested_claim=kind,
            maximum_level=ClaimLevel.NONE,
            safe_statement="Insufficient evidence for a stable reference-space comparison.",
            limitations=_merge_limitations(limitations, (LimitationCode.INSUFFICIENT_EVIDENCE,)),
        )

    if kind is ClaimKind.MODEL_FAMILY:
        missing: list[LimitationCode] = []
        if not context.minimum_evidence_met:
            missing.append(LimitationCode.INSUFFICIENT_EVIDENCE)
        if not context.in_distribution:
            missing.append(LimitationCode.OUT_OF_DISTRIBUTION)
        if not context.calibrated:
            missing.append(LimitationCode.UNCALIBRATED_SCORE)
        if not context.attribution_enabled:
            missing.append(LimitationCode.DESCRIPTIVE_ONLY)

        allowed = (
            context.strength >= ClaimLevel.MODEL_FAMILY_CANDIDATE
            and not missing
        )
        if allowed:
            return ClaimDecision(
                allowed=True,
                evidence_class=EvidenceClass.INFERRED,
                requested_claim=kind,
                maximum_level=ClaimLevel.MODEL_FAMILY_CANDIDATE,
                safe_statement=(
                    "A calibrated, benchmark-bounded model-family candidate may be reported; "
                    "UNKNOWN remains an allowed outcome."
                ),
                limitations=limitations,
            )
        return ClaimDecision(
            allowed=False,
            evidence_class=EvidenceClass.UNKNOWN,
            requested_claim=kind,
            maximum_level=min(context.strength, ClaimLevel.SIMILARITY_ONLY),
            safe_statement=(
                "Model-family attribution is not permitted for this evidence state; "
                "report measurements/similarity or UNKNOWN instead."
            ),
            limitations=_merge_limitations(limitations, missing),
        )

    if kind is ClaimKind.EXACT_MODEL:
        if context.external_attestation and context.strength >= ClaimLevel.ATTESTED_PROVENANCE:
            return ClaimDecision(
                allowed=True,
                evidence_class=EvidenceClass.ATTESTED,
                requested_claim=kind,
                maximum_level=ClaimLevel.ATTESTED_PROVENANCE,
                safe_statement=(
                    "An external provenance source attests a model identity; "
                    "CogniPrint does not infer that identity from text alone."
                ),
                limitations=limitations,
            )
        return ClaimDecision(
            allowed=False,
            evidence_class=EvidenceClass.UNKNOWN,
            requested_claim=kind,
            maximum_level=min(context.strength, ClaimLevel.MODEL_FAMILY_CANDIDATE),
            safe_statement=(
                "Exact model identity is not established. A content-derived family candidate, "
                "if separately validated, is not an exact-model attestation."
            ),
            limitations=_merge_limitations(limitations, (LimitationCode.NO_EXTERNAL_PROVENANCE,)),
        )

    raise ValueError(f"unsupported claim kind: {kind}")
