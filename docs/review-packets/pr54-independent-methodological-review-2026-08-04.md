# CogniPrint PR #54 — Independent Methodological Review Packet

Prepared: 4 August 2026

## Review target

- Repository: `TakoVHS/CogniPrint-open`
- Pull request: `#54`
- Branch: `development/challenge-001-stage-a-methods-001`
- Exact head: `98cf9637a4889c15b7d8ecb2082d9d9e56d672ec`
- Exact tree: `4b9ca053e85c261ec1d4a2a73cf0fd8649872794`
- Base: `d154b8610b182fe9110bf52fcadf02914498d356`
- State: OPEN / DRAFT / mergeable / not merged

## Purpose of this review

Please assess whether the development-only methods and claim boundaries are methodologically adequate for changing PR #54 from Draft to Ready for broader code review.

A positive assessment would **not** authorize merge, Stage B execution, a canonical freeze, Research Lock, external registration or any scientific attribution claim.

## Hard boundaries

- `DEVELOPMENT_ONLY`
- `SCIENTIFIC_CLAIM_EVIDENCE=false`
- `CANONICAL_FREEZE=PRE-FREEZE`
- `EXTERNAL_REGISTRATION=NOT_SUBMITTED`
- `STAGE_B=NOT_AUTHORISED_TO_START`
- `GITHUB_ACTIONS=NOT_EXECUTED`; equivalent-runner evidence is recorded separately
- no authorship, identity, legal, forensic, psychological, hidden-intent or deterministic-source claim

## Methods under review

### 1. Transparent surface-statistics baseline

Dependency-free 12-feature descriptive representation using reference-only standardization, L2 normalization, deterministic cosine nearest-centroid classification and lineage-overlap rejection.

### 2. Class-conditional split-conformal `UNKNOWN`

Separate reference and conformal-calibration roles; outcomes include `UNKNOWN_OOD`, `UNKNOWN_AMBIGUOUS` and `UNKNOWN_INSUFFICIENT_EVIDENCE`; missing-class and calibration/reference overlap checks; finite-sample resolution gate.

### 3. Single-temperature probability calibration

Bounded deterministic temperature fitting with multiclass NLL, Brier score and tie-preserving equal-frequency ECE; malformed and non-finite input rejection.

### 4. Uncertainty and claim-narrowing utilities

Two-sided Wilson intervals; deterministic paired lineage-group bootstrap; prospective ten-rule evaluator recording observed values, thresholds, conditions and consequences.

## Exact-tree technical validation

Free complete-checkout Linux runner deployment: `dpl_AH8NWkgNUZVMBQoymZxFuA228JLh`

- `RUNNER_EXECUTED`: PASS
- `PYTHON_EXECUTED`: PASS
- Python 3.12.13
- Ruff 0.16.1: PASS
- `py_compile`: PASS
- Stage A targeted suite run 1: PASS
- Stage A targeted suite run 2: PASS
- deterministic output probe: PASS
- RAID n-gram regression: 15/15 PASS
- RAID pilot regression: 3/3 PASS
- sanitized public-release `--check-only`: PASS, 568 selected and 16 excluded
- full tracked-tree secret scan: PASS
- `git diff --check`: PASS
- worktree clean: PASS

Technical PASS establishes deterministic execution under the tested conditions. It does not establish real-world attribution validity, generalization, legal fitness or scientific claim evidence.

## Questions for the reviewer

1. Are the claim boundaries sufficiently narrow and resistant to being interpreted as authorship attribution, a universal AI detector or proof of model provenance?
2. Should conformal evaluation lineage overlap with both reference and calibration partitions be rejected explicitly at the decision boundary?
3. Is the class-conditional conformal method and finite-sample resolution handling adequate for development-only use?
4. Is bounded single-temperature scaling an acceptable transparent baseline, and is the ECE tie policy reasonable?
5. Should paired bootstrap reject malformed group IDs and inputs with fewer than two distinct lineage groups?
6. Should Wilson boundary cases `0/n` and `n/n` be clamped exactly to 0 and 1?
7. Should claim evaluation explicitly require complement, confidence-interval and threshold coherence checks?
8. Which additional baselines, ablations, perturbations or adversarial cases are essential before future scientific evaluation?

## Requested outcome

Please choose one and explain the most important reasons:

1. **READY RECOMMENDED** — suitable to leave Draft for broader code review, with no permission to merge or start Stage B.
2. **READY WITH REQUIRED CHANGES** — list exact changes required before leaving Draft.
3. **REMAIN DRAFT** — substantial methodological or claim-boundary revision is required.

## Reviewer record

- Reviewer name:
- Affiliation or relevant expertise:
- Date:
- Exact head reviewed:
- Outcome:
- Required changes:
- Non-blocking recommendations:
- Conflicts or limitations:

## Contact

Roman Adriashkin  
CogniPrint maintainer  
https://github.com/TakoVHS/CogniPrint-open
