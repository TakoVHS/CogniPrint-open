# CogniPrint Inferential V1

Snapshot: 2026-05-12

Status: pre-review inferential candidate outputs. These files do not upgrade readiness.

## Purpose

This directory records the next validation pass after the current descriptive package and external-review gate are preserved. The current repository already contains descriptive bootstrap, permutation, effect-size, sensitivity, correction, holdout, and stylometry-baseline layers. The files here freeze the inferential-v1 inputs and execute candidate outputs for reviewer-facing discussion.

## Current Boundary

- Current readiness: `descriptive_only`
- External review: `0/1` valid reviews
- Stronger readiness: blocked until a valid non-owner review artifact exists and repository gates pass

## Frozen Input Artifacts

- `input-manifest.json`
- `permutation-spec.json`

These files freeze tracked public inputs, hashes, the primary metric family, random seed, resample count, correction methods, and the predeclared six-axis local-campaign versus public-growth contrast family.

## Generated Candidate Outputs

- `bootstrap-summary.csv`
- `bootstrap-summary.json`
- `permutation-results.csv`
- `permutation-results.json`
- `effect-sizes.csv`
- `effect-sizes.json`
- `sensitivity-results.csv`
- `sensitivity-results.json`
- `ablation-results.csv`
- `ablation-results.json`
- `reviewer-validation-report.json` when `make validation-full` is run locally
- `reviewer-validation-report-pvalues.csv` when `make validation-full` is run locally
- `reviewer-validation-report-summary.csv` when `make validation-full` is run locally
- `results-report.md`
- `limitations-report.md`
- `output-manifest.json`
- `checksum-manifest.txt`
- `command-log.txt`

## Reviewer Validation Dry-Run

The reviewer-facing validation dry-run can be regenerated with:

```bash
make validation-full
```

This command runs:

```bash
cogniprint validate \
  --corpus-dir datasets/public-benchmark-v1.1/raw \
  --campaign-dir validation/inferential-v1/reviewer-campaign-004 \
  --output validation/inferential-v1/reviewer-validation-report.json
```

The report includes cognitive fingerprint v2 distances, sparse TF-IDF cosine baseline values, deterministic random-vector baseline values, random-pair permutation contrasts, an empirical threshold recommendation, and an approximate power-analysis summary.

It also evaluates the historical exploratory threshold `0.15` separately. If the fixed threshold has a high random-pair false-positive rate for the selected corpus, the report should be read as a reason to narrow threshold language rather than strengthen it.

The report remains a pre-review candidate artifact. It does not satisfy the external-review gate and must not be described as completed validation.

## Template Artifacts

- `input-manifest.template.json`
- `permutation-spec.template.json`
- `output-manifest.template.json`

Retain these templates for future runs and format checks.

## Required Rule

Do not describe this directory as completed validation. It is a pre-review inferential candidate layer for methodological review. Stronger readiness remains blocked until a valid non-owner review artifact exists and repository gates pass.
