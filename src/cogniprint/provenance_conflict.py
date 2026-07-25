"""Evidence-conflict classification without choosing a privileged 'truth'."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AttestationStatus(str, Enum):
    VALIDATED = "VALIDATED"
    PRESENT_UNVERIFIED = "PRESENT_UNVERIFIED"
    INVALID = "INVALID"
    ABSENT = "ABSENT"
    UNSUPPORTED = "UNSUPPORTED"


class ConflictStatus(str, Enum):
    CONSISTENT = "CONSISTENT"
    PROVENANCE_CONFLICT = "PROVENANCE_CONFLICT"
    STATISTICAL_EVIDENCE_ONLY = "STATISTICAL_EVIDENCE_ONLY"
    ATTESTED_EVIDENCE_ONLY = "ATTESTED_EVIDENCE_ONLY"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True)
class ConflictResult:
    status: ConflictStatus
    inferred_label: str | None
    attested_label: str | None
    attestation_status: AttestationStatus
    note: str

    def to_dict(self) -> dict[str, str | None]:
        return {
            "status": self.status.value,
            "inferred_label": self.inferred_label,
            "attested_label": self.attested_label,
            "attestation_status": self.attestation_status.value,
            "note": self.note,
        }


def _normalise_label(value: str | None) -> str | None:
    if value is None:
        return None
    compact = " ".join(str(value).strip().casefold().split())
    return compact or None


def classify_conflict(
    *,
    inferred_label: str | None,
    inference_allowed: bool,
    attested_label: str | None,
    attestation_status: AttestationStatus,
) -> ConflictResult:
    """Classify agreement/conflict while keeping evidence classes separate.

    This function does not decide which source is 'the truth'.  A validated
    attestation and a statistical inference can agree or conflict; the caller
    must preserve both records and their provenance.
    """

    inferred = _normalise_label(inferred_label) if inference_allowed else None
    attested = _normalise_label(attested_label)
    attestation_valid = attestation_status is AttestationStatus.VALIDATED and attested is not None

    if inferred is not None and attestation_valid:
        if inferred == attested:
            return ConflictResult(
                status=ConflictStatus.CONSISTENT,
                inferred_label=inferred_label,
                attested_label=attested_label,
                attestation_status=attestation_status,
                note=(
                    "Statistical inference and validated external attestation are consistent. "
                    "Consistency does not merge the two evidence classes."
                ),
            )
        return ConflictResult(
            status=ConflictStatus.PROVENANCE_CONFLICT,
            inferred_label=inferred_label,
            attested_label=attested_label,
            attestation_status=attestation_status,
            note=(
                "Statistical inference conflicts with a validated external attestation. "
                "CogniPrint must preserve the disagreement and must not silently choose a winner."
            ),
        )

    if inferred is not None:
        return ConflictResult(
            status=ConflictStatus.STATISTICAL_EVIDENCE_ONLY,
            inferred_label=inferred_label,
            attested_label=attested_label,
            attestation_status=attestation_status,
            note=(
                "Only statistical evidence is usable for this comparison; no validated external "
                "attestation is available."
            ),
        )

    if attestation_valid:
        return ConflictResult(
            status=ConflictStatus.ATTESTED_EVIDENCE_ONLY,
            inferred_label=inferred_label,
            attested_label=attested_label,
            attestation_status=attestation_status,
            note=(
                "A validated external attestation is available, while no statistical attribution "
                "is authorised for this evidence state."
            ),
        )

    return ConflictResult(
        status=ConflictStatus.INSUFFICIENT_EVIDENCE,
        inferred_label=inferred_label,
        attested_label=attested_label,
        attestation_status=attestation_status,
        note="Neither an authorised inference nor a validated external attestation is available.",
    )
