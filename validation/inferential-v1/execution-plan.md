# Inferential V1 Execution Plan

Date: 2026-05-12

Status: executable pre-review plan.

Readiness boundary: `descriptive_only`.

## Purpose

This plan executes the frozen inferential-v1 protocol without changing CogniPrint readiness. It produces candidate reviewer-facing outputs from the current local campaign rows, public empirical-growth rows, independent holdout context, and frozen permutation specification.

## Inputs

- `validation/inferential-v1/input-manifest.json`
- `validation/inferential-v1/permutation-spec.json`
- `workspace/campaigns/*/campaign-results.json`
- `evidence/empirical-growth-v1/comparison-rows.csv`
- `evidence/independent-holdout-v1/comparison-rows.csv`

## Command

```bash
make inferential-v1
```

Equivalent direct command:

```bash
PYTHONPATH=. .venv/bin/python scripts/generate_inferential_v1.py
```

## Expected Outputs

- `validation/inferential-v1/bootstrap-summary.csv`
- `validation/inferential-v1/bootstrap-summary.json`
- `validation/inferential-v1/permutation-results.csv`
- `validation/inferential-v1/permutation-results.json`
- `validation/inferential-v1/effect-sizes.csv`
- `validation/inferential-v1/effect-sizes.json`
- `validation/inferential-v1/sensitivity-results.csv`
- `validation/inferential-v1/sensitivity-results.json`
- `validation/inferential-v1/ablation-results.csv`
- `validation/inferential-v1/ablation-results.json`
- `validation/inferential-v1/results-report.md`
- `validation/inferential-v1/limitations-report.md`
- `validation/inferential-v1/output-manifest.json`
- `validation/inferential-v1/checksum-manifest.txt`
- `validation/inferential-v1/command-log.txt`

## Acceptance Checks

Run:

```bash
make claims-guard-check
make statistical-readiness-check
make reviewer-release-check
```

`make external-review-check` is expected to remain pending until a real non-owner review artifact exists.

## Boundary

The generated outputs can support reviewer discussion and manuscript planning. They must not be described as completed validation, external review, author identification, text provenance determination, legal conclusion, deterministic classification, or universal performance.
