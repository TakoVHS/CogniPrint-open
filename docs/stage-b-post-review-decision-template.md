# Challenge 001 — Post-Review Stage B Decision Record

Status: `TEMPLATE / BLOCKED_PENDING_EXTERNAL_REVIEW`

Current external methodological review count: `0/1`

Research state: `PRE-FREEZE`

Stage B: `NOT_AUTHORISED_TO_START`

## Purpose

This record is completed only after a substantive independent methodological
review of the executed M1/M2/M2.1 evidence has been received and preserved.

It exists to prevent an external review from becoming a vague endorsement
signal. Every material criticism must change, narrow, reject, or explicitly
leave unchanged a scientific design decision.

The review may be critical or negative. Agreement is not required.

## Review identity

- reviewer: `PENDING`
- affiliation / expertise: `PENDING`
- response date: `PENDING`
- response channel: `PENDING`
- permission / preservation boundary: `PENDING`
- classification:
  - `SUBSTANTIVE_METHODOLOGICAL_REVIEW`
  - `INFORMAL_COMMENT`
  - `DECLINE_REFERRAL`
  - `ACKNOWLEDGEMENT_ONLY`
  - `AUTOMATED_RESPONSE`

Only `SUBSTANTIVE_METHODOLOGICAL_REVIEW` may satisfy the `1/1` gate.

## Reviewer criticisms

For each material criticism create one row.

| ID | Reviewer criticism | Evidence affected | Severity | Disposition | Reason |
| --- | --- | --- | --- | --- | --- |
| R1 | PENDING | PENDING | PENDING | PENDING | PENDING |

Allowed dispositions:

- `ACCEPT`
- `PARTIALLY_ACCEPT`
- `REJECT_WITH_REASON`
- `REQUIRES_NEW_EVIDENCE`

A criticism that affects probability mapping, calibration, OOD/UNKNOWN,
thresholding, sample design, inference, falsification or claim scope must not be
left without a disposition.

## Required scientific decisions after review

### 1. Does the current Stage B question survive?

Choose exactly one:

- `PROCEED_WITH_REDESIGN`
- `NARROW`
- `ABANDON`

Decision: `PENDING`

Rationale: `PENDING`

### 2. Status of the current 12D representation

Choose one:

- `KEEP_AS_INTERPRETABLE_BASELINE_ONLY`
- `KEEP_AS_PRIMARY_CANDIDATE_WITH_JUSTIFICATION`
- `RETIRE_FROM_ATTRIBUTION_STUDY`

Decision: `PENDING`

### 3. Probability model

The current M2 mapping from cosine-centroid score vectors to scalar-temperature
probabilities is not automatically carried into Stage B.

Post-review decision:

- probability semantics: `PENDING`
- score-to-probability map: `PENDING`
- calibration method: `PENDING`
- calibration partition design: `PENDING`
- acceptance criterion: `PENDING`

Any replacement must be justified prospectively.

### 4. OOD / UNKNOWN method

Post-review decision:

- OOD statistic / decision object: `PENDING`
- threshold-selection method: `PENDING`
- UNKNOWN semantics: `PENDING`
- held-out unknown design: `PENDING`
- false-known stop criterion: `PENDING`

The M2/M2.1 conformal result must not be described as validated OOD detection.

### 5. Selective prediction

Post-review decision:

- coverage target(s): `PENDING`
- risk criterion: `PENDING`
- whether global thresholds are allowed: `PENDING`
- whether context-conditional thresholds are allowed: `PENDING`

No operating point may be selected because it looks favorable on already
exposed Stage A evaluation outcomes.

### 6. Cross-fold / inferential structure

Post-review decision:

- estimand: `PENDING`
- unit of independence: `PENDING`
- interval / uncertainty method: `PENDING`
- pooled inference allowed: `PENDING`

### 7. Sealed Stage B scope

Post-review decision:

- source families: `PENDING`
- unseen-family policy: `PENDING`
- domains: `PENDING`
- languages: `PENDING`
- transformations: `PENDING`
- human-control definition: `PENDING`
- sample-size rationale: `PENDING`

## Anti-tuning declaration

Before this record can be marked complete, affirm all of the following:

- [ ] no new Stage B method was selected by optimizing exposed Stage A
      evaluation outcomes;
- [ ] no seed search was used to choose a favorable method;
- [ ] no representation was promoted because a post-result exploratory
      diagnostic looked better;
- [ ] M2 #1 remains unchanged;
- [ ] M2.1 remains labelled post-result exploratory;
- [ ] reviewer criticism was not softened or omitted because it was
      unfavorable.

## Claim-scope decision

After review, classify the strongest permissible Stage B research claim as one
of:

- `DESCRIPTIVE_MEASUREMENT_ONLY`
- `BENCHMARK_BOUNDED_SIGNAL_HYPOTHESIS`
- `SEALED_FAMILY_LEVEL_ATTRIBUTION_HYPOTHESIS`
- `NO_STAGE_B_ATTRIBUTION_HYPOTHESIS`

Decision: `PENDING`

This decision is not itself a claim unlock. It defines what the sealed study is
allowed to test.

## Gate outcome

The review gate may close at `1/1` while the Stage B decision is still
`NARROW` or `ABANDON`.

Final decision record status must be one of:

- `REVIEW_RECEIVED_DESIGN_PENDING`
- `READY_FOR_FREEZE_CANDIDATE`
- `STAGE_B_NARROWED`
- `STAGE_B_ABANDONED`

Current status:

`BLOCKED_PENDING_EXTERNAL_REVIEW`

## Next transition

Only `READY_FOR_FREEZE_CANDIDATE` or a documented narrower equivalent may
proceed to:

1. exact protocol choices;
2. candidate manifests;
3. leakage audit;
4. Research Lock;
5. external preregistration.

No state in this file directly authorizes Stage B execution.
