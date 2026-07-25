# CogniPrint Evidence Ontology v1

Status: **normative research/output contract; not a legal-forensics standard.**

## Purpose

CogniPrint must never collapse measurement, statistical inference, external provenance, and uncertainty into one generic "result".

Every conclusion belongs to exactly one primary truth class:

1. **OBSERVED** — directly measured or deterministically derived from the artifact or analysis environment.
2. **INFERRED** — a probabilistic conclusion produced from observed evidence relative to a declared reference space.
3. **ATTESTED** — a statement carried by an external provenance/credential/log source whose validation status is separately recorded.
4. **UNKNOWN** — the available evidence is insufficient, outside the validated reference space, uncalibrated, conflicting, or unsupported for the requested claim.

Machine-readable schema: `schemas/cogniprint-evidence-v1.schema.json`.
Claim policy: `src/cogniprint/evidence_policy.py`.

## OBSERVED

Examples:

- SHA-256 of the analysed artifact;
- word/character counts;
- the current 12D CogniPrint feature vector;
- distance to a named reference vector;
- a detected C2PA manifest being physically present in an artifact, once a reader exists;
- software/configuration versions actually used.

OBSERVED does **not** mean the interpretation is true. A distance is observed; "therefore model X created it" is not.

Example wording:

> **OBSERVED:** the artifact has feature profile `F`, content hash `H`, and distance `d` to reference distribution `R`.

## INFERRED

INFERRED is allowed only for claims that have a dedicated validation scope.

A machine-readable inference must record:

- candidate(s);
- score/confidence;
- whether the score is calibrated;
- reference-space status (`IN_DISTRIBUTION`, `OUT_OF_DISTRIBUTION`, `UNKNOWN`);
- reference-registry version;
- alternatives where meaningful;
- applicable limitations.

Current project policy keeps attribution disabled while scientific readiness is `descriptive_only`.

Future wording, only after the relevant benchmark gate:

> **INFERRED:** under benchmark `B` and registry `R`, family `A` is the best-supported candidate among tested classes, calibrated confidence `C`; alternatives `B/C`; UNKNOWN remains permitted.

Never shorten this to "Model A created the document."

## ATTESTED

ATTESTED is a different evidence class from content inference.

Potential sources include:

- C2PA/Content Credentials;
- signed provider attestations;
- authenticated execution logs;
- signed revision history;
- other independently verifiable workflow records.

Each attestation must carry a validation status such as:

- `VALIDATED`;
- `PRESENT_UNVERIFIED`;
- `INVALID`;
- `CONFLICT`;
- `UNSUPPORTED`.

ATTESTED does not automatically mean absolute truth. It means an external provenance source made a statement and CogniPrint records how that source was validated.

Example:

> **ATTESTED:** a validated external credential states that tool `T` performed action `A` at time `Z`.

CogniPrint should never silently convert this into a stronger content-derived claim.

## UNKNOWN

UNKNOWN is a first-class scientific output, not an error condition.

Typical reasons:

- `INSUFFICIENT_EVIDENCE`;
- `OUT_OF_DISTRIBUTION`;
- `UNCALIBRATED`;
- `NO_ATTESTATION`;
- `CONFLICTING_EVIDENCE`;
- `UNSUPPORTED_CLAIM`.

Examples:

> **UNKNOWN:** exact model identity cannot be established from the available content evidence.

> **UNKNOWN:** the artifact is outside the current reference space; no family attribution is issued.

## Claim Firewall

The code-level firewall uses evidence strength levels:

- **0 — NONE:** no attribution;
- **1 — SIMILARITY_ONLY:** descriptive measurement/comparison only;
- **2 — MODEL_FAMILY_CANDIDATE:** future benchmark-bounded family candidate;
- **3 — CALIBRATED_ATTRIBUTION_CANDIDATE:** future stronger inferential gate;
- **4 — ATTESTED_PROVENANCE:** independent provenance evidence is present and validated for the specific statement.

The current default policy does **not** enable model-family inference. A model score cannot enable itself.

The following remain prohibited as content-only conclusions:

- authorship identity;
- actor/commissioner identity;
- intent/responsibility;
- legal or forensic provenance.

Exact model identity may be represented only as an **ATTESTED** external statement under the current policy, not inferred from prose alone.

## Conflict principle

Evidence classes may disagree.

Example:

```text
ATTESTED: external credential declares workflow/tool A
INFERRED: statistical evidence is more consistent with family B
OBSERVED: artifact hash/feature profile recorded
UNKNOWN: reason for the disagreement cannot currently be established
```

CogniPrint must report the disagreement as a **provenance conflict**. It must not choose whichever signal is more convenient.

## Downstream contract

Any future safe/decision API should expose:

- the truth class for every claim;
- the claim-firewall policy version;
- limitations codes;
- calibration status;
- OOD/reference-space status;
- provenance validation status;
- explicit UNKNOWN outcomes.

A downstream UI may simplify presentation, but it must not delete or upgrade these semantics.

## High-stakes boundary

CogniPrint output must not, by itself, be used to:

- accuse a person of misconduct;
- automatically punish a student;
- terminate employment;
- determine legal liability;
- establish criminal or civil responsibility.

Any future high-stakes deployment requires domain-specific validation, governance, independent review, and evidence beyond CogniPrint content inference.
