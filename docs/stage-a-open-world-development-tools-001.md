# Challenge 001 Stage A open-world development tools

Status: `DEVELOPMENT_ONLY`

Scientific boundary:

- canonical research freeze: `PRE-FREEZE`;
- freeze candidate: separate Draft PR #50, unchanged by this work;
- external registration: `NOT_SUBMITTED`;
- Stage B: `NOT_AUTHORISED_TO_START`;
- scientific claim evidence: `false`.

## Purpose

This package implements four mechanisms required for development review before
the numerical freeze candidate can be considered operational:

1. a transparent punctuation/surface-statistics baseline;
2. class-conditional split-conformal `UNKNOWN` decisions;
3. deterministic single-temperature probability calibration;
4. Wilson intervals, paired lineage-group bootstrap and an executable
   failure-first claim matrix.

All validation uses synthetic or Stage A/development-visible fixtures. No
Stage B corpus, hidden label, sealed manifest or prediction is created.

## Surface-statistics baseline

The fixed vector contains:

1. word count;
2. Unicode-letter count;
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

Text is read only from a transient `_text` field. The returned evaluation
payload contains aggregate metrics and protocol metadata only. Classification
uses training-only standardisation followed by cosine nearest centroids and a
lexicographic tie-break.

## Conformal UNKNOWN

The conformal implementation is class-conditional:

- fit one cosine centroid per known class on the reference partition;
- compute true-class nonconformity scores on the conformal-calibration
  partition only;
- use finite-sample p-values
  `(1 + count(calibration_score >= candidate_score)) / (n_class + 1)`;
- emit `KNOWN` only when exactly one class has `p > alpha`;
- emit `UNKNOWN_OOD` when none pass;
- emit `UNKNOWN_AMBIGUOUS` when more than one passes;
- emit `UNKNOWN_INSUFFICIENT_EVIDENCE` before scoring when the evidence gate
  fails.

The p-values are conformal decision quantities, not calibrated class
probabilities.

## Temperature calibration

The calibration module:

- consumes a separate probability-calibration partition;
- fits one positive temperature by deterministic bounded NLL minimisation;
- reports multiclass NLL, Brier score and equal-frequency ECE before and after;
- rejects malformed probability rows;
- exposes an `accepted` flag only when ECE meets the development threshold and
  NLL/Brier do not worsen.

The module never converts a failed calibration into confidence wording.

## Uncertainty and claim narrowing

The uncertainty module provides:

- two-sided Wilson score intervals for proportions;
- deterministic class-stratified lineage-group paired bootstrap;
- fixed metric semantics for accuracy, balanced accuracy and macro-F1;
- percentile intervals over paired metric deltas.

The claim evaluator implements ten development gates:

- open-world false-known;
- unknown rejection;
- known coverage;
- known signal;
- CogniPrint 12D versus best n-gram;
- per-class collapse;
- calibration failure;
- domain collapse;
- missing primary strata;
- T1 light-edit robustness.

Its defaults mirror the non-canonical numerical candidate for executable
development testing. They are not a frozen protocol and do not authorize Stage
B.

## Validation

Repository-native checks:

```bash
python scripts/check_stage_a_open_world_tools.py
python -m unittest discover \
  -s tests \
  -p "test_stage_a_open_world_tools.py" \
  -v
python -m py_compile \
  src/cogniprint/benchmarks/surface.py \
  src/cogniprint/benchmarks/conformal.py \
  src/cogniprint/benchmarks/calibration.py \
  src/cogniprint/benchmarks/uncertainty.py \
  src/cogniprint/benchmarks/claims.py \
  scripts/check_stage_a_open_world_tools.py \
  tests/test_stage_a_open_world_tools.py
```

Expected smoke-check markers:

```text
STAGE_A_SURFACE_BASELINE_DEVELOPMENT_PASS
STAGE_A_CONFORMAL_UNKNOWN_DEVELOPMENT_PASS
STAGE_A_TEMPERATURE_CALIBRATION_DEVELOPMENT_PASS
STAGE_A_WILSON_BOOTSTRAP_CLAIM_MATRIX_DEVELOPMENT_PASS
STATUS=DEVELOPMENT_ONLY
CANONICAL_RESEARCH_FREEZE=PRE-FREEZE
EXTERNAL_REGISTRATION=NOT_SUBMITTED
STAGE_B=NOT_AUTHORISED_TO_START
```

## Completion boundary

A passing development PR shows that the mechanisms execute on allowed fixtures.
It does not show that the candidate source registry is feasible, that licences
are resolved, that calibration/UNKNOWN performance is acceptable on a future
candidate corpus, or that the Challenge is frozen. Those remain separate gates
under issues #49, #28 and #30.
