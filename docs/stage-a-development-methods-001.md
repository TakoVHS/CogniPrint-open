# Challenge 001 — Stage A development methods 001

Status: `DEVELOPMENT_ONLY`

Scientific-claim evidence: `NO`

Canonical freeze: `PRE-FREEZE`

Stage B: `NOT_AUTHORISED_TO_START`

## Purpose

This package implements four statistical mechanisms needed to evaluate the
Challenge 001 numerical freeze candidate on synthetic and development-visible
Stage A fixtures:

1. a transparent surface-statistics baseline;
2. class-conditional split-conformal `UNKNOWN` decisions;
3. single-temperature probability calibration;
4. Wilson intervals, lineage-group paired bootstrap and an executable
   claim-narrowing matrix.

The implementation does not read the non-canonical numerical freeze candidate,
does not change PR #50 and does not authorize any proposed candidate value.
Defaults in the development claim evaluator are testable prospective defaults,
not a declaration that the canonical protocol is frozen.

## Hard separation from Stage B

The code and tests in this package must not:

- create a Stage B corpus;
- create, inspect or infer sealed labels;
- generate model or human-control samples;
- create reference, calibration or sealed manifests;
- create a Research Lock;
- submit an external registration;
- tune any threshold against Stage B outcomes;
- expand attribution, authorship, legal or forensic claims.

Synthetic fixtures use transient `_text` and `_vector` fields. Reports produced
by the surface baseline contain aggregate features and metrics only; raw text is
not persisted.

## 1. Surface-statistics baseline

The fixed feature map is:

1. word count;
2. Unicode letter count;
3. sentence count;
4. mean word length;
5. type-token ratio;
6. digit ratio;
7. uppercase ratio;
8. newline ratio;
9. period ratio;
10. comma ratio;
11. question/exclamation ratio;
12. colon/semicolon ratio.

Text normalization is Unicode NFKC. The classifier is a standardized,
L2-normalized cosine nearest-centroid model with deterministic lexical class
tie-breaking.

The standardizer and centroids are fitted on the reference partition only.
Reference and test lineage groups must be disjoint; overlap fails closed before
model fitting or evaluation.

## 2. Conformal UNKNOWN

The implementation uses class-conditional split conformal prediction with
cosine nonconformity:

```text
nonconformity = 1 - cosine_similarity(sample, class_centroid)
```

For each known class, its calibration scores come only from the dedicated
conformal-calibration partition. The finite-sample p-value is:

```text
(1 + count(calibration_score >= candidate_score)) / (n_class + 1)
```

Decision semantics:

- exactly one accepted class: return that known class;
- no accepted classes: `UNKNOWN_OOD`;
- multiple accepted classes: `UNKNOWN_AMBIGUOUS`;
- failed evidence gate: `UNKNOWN_INSUFFICIENT_EVIDENCE`.

Conformal p-values are not class probabilities. The output explicitly records
`calibrated_probability = false`.

The fitter rejects lineage overlap between the reference and conformal
calibration roles, missing calibration classes and non-finite vectors. The
decision layer also fails closed when a class has too few calibration examples
to attain a p-value at or below alpha. The minimum per-class size is:

```text
ceil((1 - alpha) / alpha)
```

For example, alpha `0.05` requires at least `19` calibration observations per
known class before the open-set decision is considered sufficiently resolved.
This is a development evidence gate, not a claim that the eventual sample size
is scientifically adequate.

## 3. Temperature calibration

The calibration method is a single positive temperature applied to a fixed
logit/score matrix:

```text
softmax(logits / temperature)
```

Temperature is selected on the probability-calibration partition only by
minimizing multiclass negative log-likelihood. The dependency-free optimizer
performs deterministic golden-section search in log-temperature space.

The implementation fails closed on empty or non-finite logits, overflow after
temperature scaling, malformed labels, invalid bin/iteration controls and
non-finite temperature bounds. Every candidate, including `T = 1`, must lie
inside the configured bounds; the fitted result therefore cannot escape those
bounds.

The returned development report contains:

- fitted temperature;
- uncalibrated and calibrated NLL;
- uncalibrated and calibrated multiclass Brier score;
- uncalibrated and calibrated equal-frequency ECE;
- ECE bin count;
- explicit probability semantics.

Equal-frequency ECE uses tie-preserving confidence groups. Equal confidence
values are never split according to observed correctness, so the metric is
invariant to row permutations within a confidence tie.

Calibration improvement on a synthetic fixture does not establish real-world
calibration and does not unlock confidence wording.

## 4. Uncertainty and claim-narrowing

### Wilson interval

`wilson_interval` computes a two-sided Wilson score interval for a binomial
proportion. It is intended for rates such as held-out false-known behavior and
UNKNOWN rejection.

### Paired lineage-group bootstrap

`paired_group_bootstrap_delta` resamples complete lineage groups with
replacement. Both compared prediction systems receive the same resampled group
sequence. The implementation is deterministic under the supplied integer seed
and returns the point delta, percentile interval, group count and resampling
metadata.

Rows are never resampled independently when they share a lineage group.
Malformed controls and non-finite metric outputs fail closed.

### Claim-narrowing evaluator

The evaluator consumes a complete aggregate metric record and applies ten
prospective rule families:

- open-world false-known behavior;
- held-out UNKNOWN rejection;
- known coverage;
- known-family signal;
- CogniPrint-versus-n-gram incremental value;
- per-class collapse;
- calibration failure;
- domain collapse;
- empty primary strata;
- T1 light-edit robustness.

Missing required metrics, non-finite values, out-of-domain rates/deltas,
incoherent Wilson upper bounds and malformed custom thresholds fail closed.
Every rule returns its stable rule id, trigger flag, observed values, threshold
metadata, exact condition text and exact public consequence.
`all_claims_unlocked` can be true only when no rule is triggered and all inputs
pass validation; it remains a development diagnostic, not publication or freeze
authorization.

## Validation scope

Targeted validation command:

```bash
python -m unittest discover \
  -s tests \
  -p "test_stage_a_development_methods.py" \
  -v
```

Compilation:

```bash
python -m py_compile \
  src/cogniprint/benchmarks/development_methods.py \
  src/cogniprint/benchmarks/development_statistics.py \
  tests/test_stage_a_development_methods.py
```

The synthetic suite covers:

- the fixed surface feature map;
- metadata-only aggregate output;
- reference/test lineage leakage rejection;
- known, OOD, ambiguous and insufficient-evidence conformal outcomes;
- cross-partition lineage rejection;
- missing conformal class and insufficient p-value resolution;
- deterministic temperature fitting, NLL improvement and strict custom bounds;
- malformed, non-finite and overflowed logits;
- tie-preserving ECE behavior;
- Wilson interval behavior;
- deterministic grouped bootstrap and malformed controls;
- exact claim-rule triggers;
- fail-closed incomplete, non-finite, out-of-range or incoherent claim inputs;
- fail-closed malformed custom thresholds.

Before this branch can be marked Ready, exact-head validation must include the
targeted suite twice, deterministic output comparison, lightweight regressions,
`py_compile`, Ruff, `git diff --check`, sanitized public-release `--check-only`,
the repository secret scanner and privacy-boundary review.

## Scientific boundary

A passing synthetic suite establishes only that the mechanisms execute according
to their documented development contracts. It does not show that:

- the surface baseline is strong on the future challenge corpus;
- conformal UNKNOWN controls false-known risk under the proposed source set;
- temperature scaling is accepted on real calibration data;
- the numerical candidate thresholds are scientifically adequate;
- CogniPrint adds value beyond n-grams;
- Challenge 001 is frozen or preregistered.

PR #50 remains a separate `CANDIDATE_HOLD` record and must not be merged or
modified by this development package.
