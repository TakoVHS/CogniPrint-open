# CogniPrint RESEARCH FREEZE 001

Status: **PRE-FREEZE — NOT YET IMMUTABLY FROZEN**

Purpose: establish the exact research state that must be frozen before sealed Stage B evaluation for Attribution Challenge 001.

This file is a scientific control surface, not a claim that Challenge 001 has already been preregistered or executed.

## Freeze rule

No sealed Challenge 001 evaluation may begin until every required field below is resolved, this document is committed, its SHA-256 is preserved, and an external timestamped preregistration records the same protocol state.

After the freeze, any change capable of affecting the scientific result — including source families, sample inclusion, split logic, feature extraction, attribution decision rules, calibration, OOD thresholds, metrics, or stop criteria — invalidates the frozen Challenge 001 configuration. Such a change requires an explicitly versioned new challenge or preregistered amendment; it must never be silently applied after sealed predictions exist.

## Canonical software state

- CogniPrint repository: `TakoVHS/CogniPrint-open`
- CogniPrint commit: **TO BE FILLED AT FREEZE**
- Independent evaluator commit: **TO BE FILLED AT FREEZE**
- Evidence Schema: `cogniprint-evidence-v1`
- Claim Firewall: `cogniprint-claim-firewall-v1`
- Independent evaluator output schema: `cogniprint-challenge-evaluation-v0.1`
- Fingerprint/reference-space version: **TO BE FILLED AT FREEZE**
- Reference registry version: **TO BE FILLED AT FREEZE**
- Dataset/corpus version: **TO BE FILLED AT FREEZE**
- Dependency/environment lock hash: **TO BE FILLED AT FREEZE**

## Scientific claim under test

Primary question:

> Under what preregistered conditions, if any, is model-family attribution scientifically defensible beyond simple confounders while preserving an explicit UNKNOWN / insufficient-evidence outcome for unsupported cases?

Challenge 001 tests family-level inference only. It does not establish exact-model identity, authorship, operator/commissioner identity, intent, legal responsibility, universal AI origin, or forensic provenance.

## Hypotheses

The exact hypotheses must be copied from the final preregistration-ready Challenge 001 protocol and frozen here before execution.

Required minimum:

1. whether CogniPrint features add family-level information beyond transparent baselines;
2. whether the signal survives required domain/prompt holdouts;
3. whether calibrated abstention reduces false attribution on held-out generators;
4. whether transformations such as editing, translation and model-to-model rewriting materially degrade the signal;
5. whether observed performance is sufficiently stable to justify any scoped public claim.

Final frozen hypotheses: **TO BE FILLED AT FREEZE**

## Source families and controls

Exact source families, checkpoints/endpoints, provider/API evidence where available, observation window and human-control sources must be frozen before sealed evaluation.

- known reference families: **TO BE FILLED AT FREEZE**
- held-out unknown family/families: **TO BE FILLED AT FREEZE**
- human control definition: **TO BE FILLED AT FREEZE**
- collection/generation dates: **TO BE FILLED AT FREEZE**

No family may be added or removed after sealed predictions are produced.

## Languages and domains

The first challenge must remain narrower than the long-term research programme.

- languages: **TO BE FILLED AT FREEZE**
- domains: **TO BE FILLED AT FREEZE**
- language holdout policy: **TO BE FILLED AT FREEZE**
- domain holdout policy: **TO BE FILLED AT FREEZE**

Claims after the experiment may not extend beyond the tested language/domain scope without new evidence.

## Sample and lineage design

- sample count and per-stratum counts: **TO BE FILLED AT FREEZE**
- prompt/task strata: **TO BE FILLED AT FREEZE**
- length strata: **TO BE FILLED AT FREEZE**
- transformation tracks included in primary analysis: **TO BE FILLED AT FREEZE**
- exploratory transformation tracks: **TO BE FILLED AT FREEZE**
- lineage grouping key: **TO BE FILLED AT FREEZE**
- train/reference/test partition rule: **TO BE FILLED AT FREEZE**
- sealed-ground-truth storage rule: **TO BE FILLED AT FREEZE**

Parent/child transformations, near-duplicates and prompt-linked response families must never leak across partitions.

## Minimum Evidence Policy

A minimum-evidence rule is mandatory, but no arbitrary token threshold is accepted merely because it sounds plausible.

- minimum-evidence criterion: **TO BE DETERMINED AND FROZEN FROM PRE-SEALED DEVELOPMENT/VALIDATION EVIDENCE**
- short-text handling: `UNKNOWN / INSUFFICIENT EVIDENCE`

The minimum-evidence rule must be selected before sealed predictions and may be scoped by language/domain if evidence requires it.

## OOD / UNKNOWN definition

`UNKNOWN` is a first-class decision, not an error state.

Freeze:

- reference-space membership method: **TO BE FILLED AT FREEZE**
- OOD score/statistic: **TO BE FILLED AT FREEZE**
- threshold-selection method: **TO BE FILLED AT FREEZE**
- held-out-generator protocol: **TO BE FILLED AT FREEZE**
- insufficient-evidence rule: **TO BE FILLED AT FREEZE**

The system must not force an artifact into a known family when the required evidence gates are not met.

## Calibration

Freeze before sealed evaluation:

- calibration method: **TO BE FILLED AT FREEZE**
- calibration partition: **TO BE FILLED AT FREEZE**
- ECE binning: **TO BE FILLED AT FREEZE**
- probability output semantics: **TO BE FILLED AT FREEZE**
- acceptance criterion for any calibrated-confidence claim: **TO BE FILLED AT FREEZE**

If calibration does not meet the preregistered acceptance criterion, Claim Firewall must keep calibrated-attribution language locked.

## Baselines

Required minimum baselines:

1. chance expectation;
2. majority class;
3. length-only;
4. simple punctuation/surface statistics;
5. current CogniPrint 12D feature map;
6. character n-gram baseline;
7. word n-gram baseline.

Any additional learned baseline/model must be frozen before sealed predictions.

## Primary metrics

Freeze exact definitions and implementations for:

- Top-1 accuracy with abstentions handled explicitly;
- macro-F1;
- balanced accuracy;
- per-class precision/recall/F1;
- confusion matrix;
- coverage;
- selective accuracy / selective risk;
- held-out-generator unknown rejection rate;
- held-out-generator false-known rate;
- Brier score when calibrated class probabilities exist;
- Expected Calibration Error when calibrated confidence exists.

Raw accuracy alone is never sufficient.

## Exclusion rules

Allowed exclusion rules must be explicit and independent of the observed sealed result.

Frozen exclusion rules: **TO BE FILLED AT FREEZE**

Post-reveal exclusions are prohibited unless reported as protocol deviations and accompanied by the original unmodified result.

## Stop / claim-narrowing rules

Before sealed evaluation, numeric acceptance thresholds must be frozen where defensible.

At minimum, the model-family claim remains locked or is narrowed if any preregistered failure condition is met, including unacceptable false-known behavior, calibration failure, dominant trivial confounding, domain/generalisation collapse, or insufficient replication across the intended scope.

Exact thresholds and decision table: **TO BE FILLED AT FREEZE**

A failed Challenge 001 remains a valid scientific result.

## Blind execution order

1. Freeze this protocol and all referenced versions.
2. Preserve commit/file hashes.
3. Complete external timestamped preregistration.
4. Build/freeze the corpus and reference partitions.
5. Keep sealed ground truth unavailable to the prediction process.
6. Produce predictions.
7. Freeze `predictions.jsonl` and its SHA-256.
8. Reveal labels only after predictions are frozen.
9. Run the independent evaluator without fitting/tuning.
10. Publish results and failures together.

## Required hashes at reveal

- protocol SHA-256: **PENDING**
- dataset/corpus manifest SHA-256: **PENDING**
- split manifest SHA-256: **PENDING**
- reference registry SHA-256: **PENDING**
- predictions SHA-256: **PENDING**
- labels SHA-256: **PENDING**
- evaluator SHA-256: **PENDING**
- environment/dependency lock SHA-256: **PENDING**

## Change-control rule

After `FROZEN` status is declared, a scientific-impacting change requires one of:

- an externally timestamped preregistered amendment made before sealed predictions; or
- a new explicitly versioned challenge.

Never overwrite the frozen protocol to make the completed result look cleaner.

## Freeze completion checklist

The status may change from `PRE-FREEZE` to `FROZEN` only when:

- [ ] exact software/evaluator commits are recorded;
- [ ] dataset/reference versions are recorded;
- [ ] source families and held-out generators are recorded;
- [ ] language/domain/sample strata are recorded;
- [ ] split/lineage rules are frozen;
- [ ] minimum-evidence policy is frozen;
- [ ] OOD/UNKNOWN method is frozen;
- [ ] calibration method/acceptance criteria are frozen;
- [ ] metrics/baselines are frozen;
- [ ] exclusion rules are frozen;
- [ ] stop/claim-narrowing criteria are frozen;
- [ ] protocol file SHA-256 is preserved;
- [ ] external timestamped preregistration is complete;
- [ ] CI/runtime validation required by issue #30 has actually executed or an equivalent reproducible runner record is archived.

Until every box is satisfied, Challenge 001 Stage B remains **NOT AUTHORISED TO START**.
