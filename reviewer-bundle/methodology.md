# CogniPrint Reviewer Bundle — Methodology

## Formal object — implemented

CogniPrint represents a text sample as a finite-dimensional statistical profile. A feature map maps token sequences into a vector space, and the resulting vector is treated as the text profile or cognitive fingerprint.

The public implementation currently uses a documented versioned 12-coordinate profile. The broader mathematical formalism does not imply that these coordinates uniquely identify a person, model, or production process.

## Comparison layer — implemented

The framework compares profiles using geometric quantities such as Euclidean distance and cosine similarity. These measurements are descriptive and are not classification decisions.

## Stability layer — implemented/conditional

Perturbation analysis is conditional. Stability statements depend on explicit coordinate-wise assumptions and non-degeneracy conditions for the selected feature family and regime.

The assumptions are part of the statement; they are not evidence that arbitrary transformations preserve a fingerprint.

## Empirical layer — executed development evidence

The public empirical layer is a diagnostic/research layer.

Historical RAID M1 and the first real pinned RAID M2 have both executed on Stage A-visible data. Neither is blind Stage B evidence.

### M1

M1 used a grouped 351/149 split over a fixed 500-record RAID Pilot A selection.

Historical macro-F1:

- CogniPrint 12D: `0.535883`;
- character 3–5 hashed TF-IDF: `0.578782`;
- word 1–2 hashed TF-IDF: `0.595220`.

The lexical baselines outperformed 12D on that fixed closed-set comparison.

### M2

M2 asks a different question: probability quality, abstention and open-set failure under matched scoring procedures.

The executed design includes:

- exact source/features/selection/source-contract hash gates;
- four predeclared leave-one-machine-family-out folds;
- human retained as a known control;
- lineage-safe five-role separation:
  - classifier/reference training;
  - probability calibration;
  - conformal calibration;
  - threshold development;
  - held-out development evaluation;
- matched cosine-nearest-centroid scoring across 12D, character n-gram and word n-gram representations;
- temperature fitted only on probability calibration;
- proper-score evaluation with NLL and multiclass Brier;
- selective-risk/AURC reporting;
- max-confidence false-known/AUROC open-set baseline;
- class-conditional probability-conformal prediction;
- lineage-group paired bootstrap intervals.

Primary aggregate point estimates do not favor 12D. Full values and evidence hashes are in `reviewer-bundle/m2-results.md`.

The correct interpretation is negative/mixed and development-bounded.

## Key methodological tensions exposed by M2

### Score-to-probability mapping

The M2 score vectors are cosine-centroid similarities treated as logit-like inputs to scalar temperature scaling.

This is transparent and argmax-preserving, but M2 exposed a scale problem:

- all n-gram temperatures hit the lower bound `T=0.05`;
- 12D held-out NLL worsened in all four folds after temperature scaling.

A reviewer should assess whether this mapping is defensible or should be prospectively reformulated.

### Open-set confidence

Maximum calibrated class confidence performed weakly as an OOD ranking score. Mean AUROC remained near 0.51–0.54.

The implementation therefore must not present confidence thresholding as validated OOD detection.

### Conformal interpretation

The probability-conformal layer yielded near-zero false-known singleton behavior on held-out families, but also extremely low singleton rates for known examples.

This is a highly conservative prediction-set regime, not proof of practical OOD recognition.

A post-result diagnostic should separate unknown empty-set outcomes from unknown ambiguous-set abstention before stronger OOD language is considered.

### Cross-fold inference

The same Stage A-visible corpus participates in multiple leave-one-family-out folds.

Per-fold paired bootstrap intervals are available, but no pooled cross-fold inferential claim is currently authorised.

A reviewer should recommend an estimand/inference structure if pooled comparison is scientifically useful.

## Human–AI intervention — proposed research target

A separate proposed direction asks whether controlled revision chains can support sentence/span-level or change-point analysis of substantial human editing in machine-assisted documents.

No current-release output is described as a validated human–AI intervention map.

## Provenance layer — evidence-class separation

CogniPrint keeps separate:

1. **content-derived measurements** — statistical properties observed in the artifact;
2. **authenticated/declared provenance** — hashes, signed credentials, revision history, publication records or tool/workflow records where legitimately available.

A content-derived similarity score must not be upgraded into authenticated provenance.

Actor, commissioner, approval or workflow identity can enter a future provenance graph only when independent records support it.

## Local explanation prototype — non-scientific evidence transformation

The experimental QVAC integration consumes a whitelisted CogniPrint evidence envelope and may generate a local human-readable explanation.

The explanation layer is not permitted to alter deterministic measurements or create stronger scientific evidence.

## Reviewer focus

Please review:

1. whether the feature-map abstraction is clearly defined;
2. whether the perturbation assumptions are narrow enough;
3. whether M1/M2 lineage controls are adequate;
4. whether the five-role M2 split is appropriate for calibration/conformal/threshold development;
5. whether cosine-centroid scores should be mapped to probabilities using scalar temperature scaling;
6. how repeated temperature-bound hits should be handled without post-result tuning;
7. whether risk-coverage/AURC reporting is appropriately scoped;
8. whether false-known/AUROC adequately capture the open-set failure visible here;
9. how conformal empty-set and ambiguous-set behavior should be separated;
10. whether any cross-fold inferential comparison is justified;
11. what should be frozen before any sealed Stage B evaluation;
12. whether any public claim remains stronger than the evidence supports.

## Claims boundary

The current methodology should be read as a descriptive framework plus executed development experiments and documented future extensions.

It should **not** be read as a validated authorship system, exact-model identifier, AI-origin oracle, actor/commissioner identifier, legal-status classifier or forensic provenance system.
