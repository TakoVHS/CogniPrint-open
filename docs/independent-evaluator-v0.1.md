# CogniPrint Independent Challenge Evaluator v0.1

Status: **evaluation tooling for future Challenge 001; no attribution result is claimed.**

## Purpose

The evaluator is deliberately separate from model fitting and threshold selection.

It consumes:

```text
frozen predictions.jsonl + revealed labels.jsonl
                    ↓
        deterministic evaluator
                    ↓
              metrics.json
```

The evaluator does not receive source text and does not refit, calibrate, tune, or reinterpret predictions after label reveal.

Implementation: `scripts/evaluate_challenge_predictions.py`.

## Prediction record

Minimum fields:

```json
{"sample_id":"S001","decision":"known","top1_candidate":"family-a"}
```

Allowed decisions:

- `known`;
- `unknown`;
- `insufficient-evidence`.

For an abstention, `top1_candidate` must be null/absent. This prevents a downstream report from quietly displaying a hidden candidate as if abstention had not occurred.

Optional calibrated fields:

```json
{
  "confidence": 0.72,
  "calibrated": true,
  "probabilities": {"family-a": 0.72, "family-b": 0.28}
}
```

Rules:

- confidence must be in `[0,1]`;
- a confidence requires an explicit boolean calibration flag;
- a probability vector must sum to 1;
- probability vectors are accepted only with `calibrated: true`;
- ground-truth fields are forbidden in prediction rows.

## Label record

The sealed label file is separate:

```json
{"sample_id":"S001","true_class":"family-a","known_to_reference":true}
```

A held-out generator uses `known_to_reference: false` even though its true class remains recorded for post-reveal analysis.

Prediction and label sample-ID sets must match exactly.

## Metrics

### Known-reference partition

Reported:

- Top-1 accuracy with abstentions counted as errors;
- balanced accuracy with abstentions counted as errors;
- macro-F1 with explicit `zero_division=0` semantics;
- coverage;
- abstention rate;
- selective accuracy/risk on issued known decisions;
- per-class precision/recall/F1;
- confusion matrix with an explicit `__ABSTAIN__` column.

### Held-out / unknown-reference partition

Reported:

- unknown rejection rate;
- false-known rate.

This is intentionally separate from closed-set accuracy.

### Calibration

When the frozen predictions include the necessary calibrated data:

- multiclass Brier score on known-reference rows;
- Expected Calibration Error on issued known decisions;
- reliability-bin table.

Missing calibration data is returned as null. The evaluator does not invent, retrofit, or calibrate probabilities after label reveal.

## Artifact binding

CLI execution records SHA-256 for:

- frozen predictions file;
- revealed labels file.

The metrics artifact can therefore be bound into a `.cogcase` / Evidence Capsule later without ambiguity about which prediction and label files were evaluated.

## Blind-evaluation order

1. freeze challenge protocol;
2. freeze reference/training/calibration data;
3. produce sealed predictions;
4. hash predictions;
5. reveal labels;
6. run this evaluator;
7. publish metrics and failures;
8. any model/threshold change becomes a new experiment version.

## Current runtime status

The source and unit tests are present in the repository branch/PR. A local clone-based execution attempt from the current development environment could not begin because that environment could not resolve `github.com`. This network failure is **not** a test PASS or FAIL.

Do not mark the evaluator runtime gate green until the test module executes successfully in an environment with the branch contents available.
