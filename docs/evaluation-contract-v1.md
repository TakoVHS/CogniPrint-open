# CogniPrint Evaluation Contract v1

Status: **normative research protocol for future attribution experiments; no attribution result is claimed.**

This contract complements `docs/attribution-challenge-001.md`. It defines the minimum evaluation hygiene required before any confidence-bearing source-family output may be exposed outside research diagnostics.

## 1. Calibration before confidence

Raw accuracy is insufficient.

A confidence-bearing experiment must report at least:

- balanced accuracy;
- macro F1;
- per-class precision/recall/F1;
- Top-1 accuracy;
- Top-k accuracy where ranking is meaningful;
- Brier score or a documented multiclass equivalent;
- Expected Calibration Error with preregistered binning;
- reliability table/plot data;
- selective risk versus coverage;
- OOD/unknown rejection performance;
- false-known rate on held-out generators.

A score that has not been calibrated must be labelled **uncalibrated** and must not be rendered as a probability.

## 2. OOD gate before attribution

The decision order is:

```text
minimum evidence?
    ↓
inside validated reference space?
    ↓
calibrated for this scope?
    ↓
family candidate or UNKNOWN
```

The system must not perform "which known family?" before answering whether the artifact is sufficiently supported by the reference space.

Required OOD outcomes:

- `IN_DISTRIBUTION`;
- `OUT_OF_DISTRIBUTION`;
- `UNKNOWN`.

`OUT_OF_DISTRIBUTION` must lead to `UNKNOWN` for source-family attribution under Claim Firewall v1.

## 3. Generator holdout

At least one generator family must be completely absent from training/reference fitting.

Primary question:

> Does the system reject an unseen generator as UNKNOWN rather than confidently forcing it into a known class?

Report false-known rate separately from closed-set accuracy.

## 4. Temporal holdout

Random splits are not sufficient for model-drift claims.

Where collection dates permit, reserve a later observation period that is not used to construct the earlier reference registry.

Conceptual design:

```text
reference period: T0 ... T1
sealed future period: T2 ... T3
```

The goal is to measure whether a reference fingerprint survives provider/model drift, not to assume temporal stationarity.

## 5. Domain holdout

At least one domain family should be absent from fitting/calibration when evaluating cross-domain generalisation.

Examples may include expository, news, technical, legal-like synthetic tasks, fiction, social-style prose, or other preregistered categories, subject to licensing/safety constraints.

A domain-holdout failure must not be hidden inside aggregate performance.

## 6. Language holdout / multilingual phase

Do not claim multilingual robustness from English evidence.

Initial proposed languages for a later dedicated phase:

- English;
- Russian;
- Vietnamese.

The research question is whether any family-level signal remains useful across language changes after language-specific confounders are controlled.

Cross-language transfer must be reported separately from within-language performance.

## 7. Translation attack

A translation robustness track should record every tool/model/version involved.

Example controlled chain:

```text
English source
→ Russian translation
→ Vietnamese translation
→ English back-translation
```

Measure both attribution performance and feature-space drift. A complete loss of signal is a valid scientific result.

## 8. Human editing survival curve

"Human edited" is too coarse.

A future controlled experiment should preregister edit-budget bins, for example:

```text
0%, 5%, 10%, 20%, 40%, 60%, 80%
```

The exact operational definition of edit percentage must be frozen before evaluation (token replacement, revision distance, controlled rewriting protocol, or another defensible measure).

Primary artifact: **fingerprint survival curve** versus human-edit budget.

No threshold is a current product guarantee.

## 9. Model-to-model laundering

Test controlled rewrite chains such as:

```text
family A → family B rewrite
family B → family C rewrite
```

Measure whether evidence resembles the initial source, final rewriter, a mixture, or falls outside the validated reference space.

This is an exploratory precursor to generation-lineage research, not proof that lineage can currently be reconstructed.

## 10. Minimum Evidence Policy

A future decision API must refuse attribution below an empirically validated evidence floor.

Do **not** hard-code a public threshold such as "200 tokens" before Challenge 001 determines an appropriate regime.

The threshold must be:

- derived from preregistered evaluation;
- versioned;
- tied to language/domain/reference-space conditions;
- machine-readable;
- conservative under uncertainty.

Below the threshold, return `UNKNOWN / INSUFFICIENT_EVIDENCE`.

## 11. Independent evaluator

Predictions and ground truth must remain separate until reveal.

Preferred files:

```text
predictions.jsonl
labels.sealed.jsonl
```

Evaluation code should consume both only after predictions are frozen and hashed.

The evaluator should be simple, deterministic, separately reviewable, and should not refit the model or alter thresholds after label reveal.

## 12. Preregistration

Before Stage B of Challenge 001, freeze hypotheses, sources, exclusions, metrics, thresholds, holdouts, calibration, UNKNOWN rule and failure criteria.

Preferred external record: a timestamped read-only preregistration (for example OSF) created before sealed-test analysis, in addition to a repository hash of the exact protocol.

If an external registration is unavailable, preserve an immutable timestamped protocol artifact by another independently reviewable mechanism and disclose that limitation.

## 13. Required failure publication

Every headline result must ship with:

- shortest reliable evidence regime;
- worst domain;
- worst language tested;
- held-out generator false-known rate;
- temporal degradation where available;
- translation/human-edit/model-rewrite degradation;
- calibration failures;
- UNKNOWN success/failure cases;
- negative results.

See `docs/where-cogniprint-fails.md`.
