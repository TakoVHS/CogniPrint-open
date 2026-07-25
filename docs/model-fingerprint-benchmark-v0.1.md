# CogniPrint Model-Fingerprint Benchmark v0.1

Status: protocol draft for controlled research. This document does not expand current scientific claims.

## Purpose

The benchmark tests a narrow, falsifiable question:

> Under controlled conditions, do text-derived CogniPrint features contain enough stable information to distinguish outputs from known model families better than simple baselines, and how quickly does that signal degrade under domain shift, multilingual use, paraphrasing, translation, and human editing?

The benchmark is intentionally not designed to prove unique model identity in the open world.

## Primary hypotheses

H1. A model-family classifier trained on controlled outputs can exceed chance on held-out prompts from the same domains.

H2. Performance will decline under cross-domain, multilingual, paraphrase, translation, and substantial human-edit conditions.

H3. Calibration and abstention are necessary: some samples should be reported as insufficient evidence rather than assigned to a source family.

H4. A content fingerprint and authenticated provenance metadata provide complementary evidence and should not be collapsed into one score.

## Experimental units

Each generated sample should be linked to a generation record with, when lawfully and technically available:

- sample_id;
- prompt_id;
- prompt_family;
- language;
- domain;
- model_provider;
- model_family;
- model_version or declared model identifier;
- generation timestamp;
- temperature / sampling parameters when exposed;
- max-output setting when exposed;
- system-prompt class without storing secrets;
- raw-output hash;
- transformation lineage;
- release status and license/usage note.

Sensitive credentials, API keys, private prompts, personal data, and provider secrets must never be committed.

## Initial target matrix

A useful first public study should aim for at least:

- 4 independent model families;
- 3 languages;
- 4 content domains;
- 25 prompt seeds per language/domain cell;
- at least 2 generation settings per model where the provider exposes them;
- a human-written comparison set with compatible domains and licensing;
- transformed variants for a documented subset.

This is a target design, not a claim that the current repository already contains these samples.

## Split policy

The split must prevent prompt leakage.

- Train: prompt families A.
- Validation: disjoint prompt seeds from families A/B as documented.
- Test: prompt seeds never used for fitting or threshold selection.
- Cross-domain test: domains excluded from training.
- Cross-language test: at least one language excluded from fitting when feasible.
- Open-world test: samples from at least one unseen model family.

No near-duplicate prompt or transformed sibling may be split across train and test unless the experiment explicitly studies transformation robustness.

## Feature groups

Evaluate feature groups separately before combining them:

1. Current 12-dimensional CogniPrint profile φ(T).
2. Entropy features.
3. Character n-grams.
4. Word n-grams.
5. Length / punctuation / lexical diversity controls.
6. Optional learned representations in a clearly separated experiment.

The current interpretable feature map should remain available as the simplest reproducible baseline.

## Baselines

At minimum compare against:

- majority-class / chance baseline;
- length-only baseline;
- simple character n-gram classifier;
- simple word n-gram classifier;
- current CogniPrint profile alone;
- combined interpretable features.

A complex model is not evidence of a useful fingerprint unless it improves over simple baselines on genuinely held-out conditions.

## Metrics

For closed-set model-family classification report:

- macro F1;
- balanced accuracy;
- one-vs-rest ROC-AUC where appropriate;
- log loss or Brier score for probability quality;
- expected calibration error or reliability curves;
- confusion matrix;
- coverage versus accuracy when abstention is enabled.

For binary human-vs-generated comparison, align with established evaluation practice by reporting ROC-AUC and Brier score alongside calibration. NIST GenAI Text 2026 uses AUC-ROC and Brier-style probability evaluation for text discriminators; CogniPrint should not claim equivalence to the NIST challenge, but should borrow the discipline of calibrated evaluation.

## Robustness tracks

Evaluate the same frozen system under:

- paraphrasing;
- translation and back-translation;
- grammar correction;
- punctuation cleanup;
- compression / expansion;
- style transfer;
- sentence reordering;
- mixed human editing at low, medium, and high edit intensity;
- model-version drift when a provider changes the served model.

For every track, record both predictive performance and profile displacement Δφ.

## Human–AI intervention track

A separate track should use controlled revision chains:

1. machine draft;
2. light human copy-edit;
3. substantive human rewrite;
4. optional second-model rewrite;
5. final human approval.

The task is not to identify a person. It is to test whether change points or regions with different production characteristics can be detected with calibrated uncertainty.

## Open-world and abstention requirement

Closed-set accuracy is insufficient for deployment claims.

A required test set must include outputs from an unseen model family. The system should be allowed to produce `unknown / insufficient evidence` rather than force every sample into a known class.

Report:

- false attribution rate on unseen families;
- abstention coverage;
- accuracy conditional on non-abstention;
- calibration under distribution shift.

## Provenance-fusion track

Content-derived evidence and provenance metadata must be evaluated separately.

Potential provenance inputs include:

- content hashes;
- signed Content Credentials / C2PA assertions;
- revision history;
- model/tool execution logs;
- repository or publication history;
- authenticated approvals.

The benchmark should test three conditions:

1. content evidence only;
2. provenance evidence only;
3. combined evidence.

Actor or commissioning identity must never be inferred from prose alone. It may be represented only when independently authenticated records support that statement.

## Reproducibility requirements

Every released experiment should include:

- immutable input manifest or hashes;
- feature-map version;
- code commit SHA;
- split manifest;
- evaluation configuration;
- random seed(s);
- environment lock or dependency snapshot;
- raw metric outputs;
- summary report;
- limitations and non-claims.

## Failure criteria

The programme should publish a negative or mixed result if any of the following occur:

- performance does not beat simple baselines;
- performance collapses under modest domain/language shift;
- false attribution on unseen models is unacceptably high;
- probabilities are badly calibrated;
- model-family signal disappears after ordinary human editing;
- results cannot be reproduced from the released artifacts.

These outcomes are scientifically useful because they define the boundary of fingerprint-based attribution.

## Milestone sequence

### M0 — protocol freeze

Publish this benchmark design, manifest schema, evaluation metrics, and non-claims before collecting the main corpus.

### M1 — pilot corpus

Collect a small legally releasable pilot across multiple model families and human controls. Validate manifests and leakage checks.

### M2 — closed-set baseline

Run simple baselines and the current CogniPrint feature map. Publish calibration and confusion results.

### M3 — robustness

Freeze the fitted system, then run transformation and human-edit tracks.

### M4 — open-world

Evaluate unseen model families and abstention.

### M5 — provenance fusion

Prototype a separate provenance-evidence channel and compare it with content-only inference.

## Current claim boundary

As of v0.1.2, CogniPrint provides reproducible descriptive text profiles. The benchmark above is the protocol for testing stronger future claims; those claims remain unvalidated until results are collected, reviewed, and reproduced.
