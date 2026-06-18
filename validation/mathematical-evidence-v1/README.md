# Mathematical Evidence V1

Status: pre-review mathematical diagnostics.
Readiness boundary: `descriptive_only`.

This folder summarizes corpus-specific geometry and sensitivity behavior for
the CogniPrint v2 feature map. It does not satisfy the external review gate and
does not establish validation, authorship, provenance, AI detection, legal
status, forensic status, deterministic classification, or a universal
threshold.

## Inputs

- baseline texts: 20
- independent holdout texts: 10
- baseline/variant pairs: 120
- fingerprint version: `cognitive-fingerprint-v2.0`

## Diagnostics

- PCA effective dimension: 4.284743
- PCA components for 90% variance: 5
- PCA components for 95% variance: 6
- First evaluated length within 10% of the lowest mean deviation: 320
- Empirical K max over observed variants: 0.46955
- Baseline/variant rows: 120
- Random baseline-pair rows: 190

## Interpretation

These outputs are intended to make the mathematical evidence base more
auditable:

1. PCA describes covariance geometry of the 12 coordinates on the current
   corpus.
2. Length stability estimates how fragment size changes profile dispersion on
   the current token pool.
3. Empirical Lipschitz diagnostics estimate observed sensitivity per word edit.
4. Baseline contrasts compare CogniPrint distances with TF-IDF and deterministic
   random-vector baselines.

All interpretation remains descriptive until a valid non-owner methodological
review is archived and the manuscript validation plan is updated.
