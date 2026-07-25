# CogniPrint Attribution Challenge 001

Status: **preregistration-ready experimental protocol; no challenge result is claimed here.**

Scientific readiness before execution: `descriptive_only`.

## Purpose

Attribution Challenge 001 is the first deliberately falsifiable test of the hypothesis that text-generation processes may leave measurable multidimensional signatures that contain source-family information beyond trivial confounders.

The challenge is not designed to prove that arbitrary text can be assigned to an exact model. It is designed to determine:

1. whether any useful model-family signal exists under controlled conditions;
2. whether CogniPrint features add information beyond simple baselines;
3. how quickly the signal collapses under editing, paraphrase, translation, domain shift, and unseen models;
4. whether an explicit `UNKNOWN / INSUFFICIENT EVIDENCE` class can prevent forced false attribution;
5. which research directions should be abandoned if the evidence is weak.

## Primary hypothesis

> Under a preregistered benchmark with leakage-safe splits, some generation processes will exhibit stable multivariate differences that permit model-family discrimination above simple length and n-gram baselines, while still requiring calibrated abstention under open-world and transformed conditions.

This hypothesis is allowed to fail.

## Non-hypotheses

Challenge 001 does not test or establish:

- author identity;
- commissioning actor identity;
- intent or responsibility;
- legal or forensic provenance;
- universal AI detection;
- exact-model identity in the open world;
- production readiness.

## Two-stage design

### Stage A — external benchmark smoke test

Use the pinned RAID pilot infrastructure already present in the repository.

Purpose:

- verify data adapter and evaluation code on an independently maintained corpus;
- compare current 12D CogniPrint features with transparent controls;
- identify obvious leakage/confounding failures before creating a larger bespoke corpus.

Stage A is not the headline attribution result.

### Stage B — controlled blind challenge

Construct a dedicated challenge corpus with labels hidden from the evaluation process until predictions are frozen.

The exact source set must be frozen in a preregistration before generation/evaluation begins.

## Capability target

Challenge 001 targets **family-level discrimination**, not adjacent-version discrimination.

Do not design the first challenge around distinctions such as one minor release versus its immediate successor. The progression is evidence-gated:

- Level 0: descriptive profile;
- Level 1: model family + `UNKNOWN`;
- Level 2: specific model candidate;
- Level 3: generation configuration;
- Level 4: human intervention map;
- Level 5: cross-model lineage.

Challenge 001 concerns Level 1 only.

## Source classes

The final class list should contain:

- at least one human control class;
- multiple distinct model families;
- at least one model family held out entirely for open-world testing;
- where licensing/API conditions permit, more than one version/checkpoint within a family so the classifier cannot rely on a single endpoint artifact.

Exact model names and versions must be frozen before evaluation.

## Prompt and task structure

The challenge should separate source signal from prompt/domain signal.

Required prompt strata:

- factual/expository;
- analytical/argumentative;
- summarisation;
- instructional;
- creative but non-poetic prose;
- dialogue/assistant response where appropriate.

Prompt IDs must be shared across source classes where feasible.

Related outputs from the same prompt/source lineage must never be split across training and test partitions.

## Generation variation

Where the source system exposes the setting, preregister multiple generation regimes such as:

- default/sampling;
- lower and higher temperature or equivalent sampling diversity;
- more deterministic decoding where available;
- different maximum lengths.

Do not infer unsupported generation parameters for systems that do not expose them.

## Length strata

At minimum:

- short;
- medium;
- long.

Exact token/word cutoffs must be preregistered.

Very short outputs should be evaluated as a separate failure regime rather than silently mixed into the main score.

## Transformation tracks

The original clean challenge and transformation challenge must be reported separately.

### T0 — clean

Original generated or human text.

### T1 — light human edit

Controlled punctuation, typo, small lexical, and local phrasing edits.

### T2 — substantial human rewrite

Meaning preserved but structure and wording materially changed by a human participant under a documented protocol.

### T3 — AI paraphrase

One model rewrites another model's output.

### T4 — translation round-trip

Translation to a second language and back, with model/tool versions recorded.

### T5 — cross-model rewrite

Source family A output rewritten by family B.

### T6 — mixed chain

A preregistered sequence such as:

`model A → human edit → model B rewrite`

T6 is exploratory for Challenge 001 and must not be presented as validated lineage reconstruction.

## Ground truth

Every sample must have a machine-readable lineage record that is separate from the text itself.

Minimum fields:

- sample ID;
- prompt ID;
- source class/family;
- source version/checkpoint where known;
- generation date/time window;
- generation configuration where known;
- transformation track;
- transformation tool/model/human protocol where relevant;
- parent sample ID for derived texts;
- human-control provenance category;
- cryptographic hashes of raw artifacts where permitted.

Ground-truth lineage must not be available to the classifier during blind evaluation.

## Data leakage rules

The following are prohibited:

- train/test copies or near-copies of the same response;
- parent/child transformed samples split across train and test;
- prompt-specific leakage across partitions where the same prompt response family is present on both sides;
- labels encoded in filenames, directories, metadata visible to the classifier, or generation wrappers;
- evaluation against reference data created after test labels have been inspected.

Split groups should be based on the strongest available shared lineage key, not individual rows.

## Baselines

No complex classifier should be considered informative until it beats transparent baselines under the same split.

Required baselines:

1. chance expectation;
2. majority class;
3. length-only;
4. punctuation/simple surface statistics;
5. current CogniPrint 12D feature map;
6. character n-gram classifier;
7. word n-gram classifier.

Optional learned representations may be added only after these are frozen.

## Primary metrics

Report at least:

- balanced accuracy;
- macro F1;
- per-class precision/recall/F1;
- confusion matrix;
- Top-1 accuracy;
- Top-k accuracy where candidate ranking is meaningful.

Raw accuracy alone is insufficient.

## Calibration metrics

If probabilities/confidences are exposed, report at least:

- Brier score or multiclass equivalent;
- expected calibration error with preregistered binning;
- reliability plot/table.

A confidence number that is not calibrated must be labelled as an uncalibrated score.

## UNKNOWN / out-of-distribution evaluation

`UNKNOWN` is a required first-class outcome.

Open-world testing must include at least one source family not present in the closed-set reference/training data.

Evaluate:

- known-class accuracy at multiple abstention thresholds;
- unknown rejection rate;
- false-known rate on held-out families;
- selective risk versus coverage;
- performance under transformed/OOD samples.

The system must be allowed to return `INSUFFICIENT EVIDENCE` for short/unstable inputs even if the source family exists in the reference set.

## Blind evaluation procedure

1. Freeze protocol, source set, transformations, metrics, split rules, and exclusions.
2. Generate/collect corpus and assign hidden ground-truth labels.
3. Create training/reference partition and sealed challenge partition.
4. Fit/calibrate only on allowed partitions.
5. Produce predictions for the sealed challenge set.
6. Freeze prediction file and its SHA-256.
7. Reveal labels.
8. Compute metrics without changing predictions.
9. Publish errors and failure analysis.

Any post-reveal model change belongs to a new experiment/version.

## Prediction record

Each sealed prediction should contain:

- sample ID;
- Top-1 candidate;
- Top-k candidates where applicable;
- confidence/score with calibration status;
- `known / unknown / insufficient-evidence` decision;
- reference-registry version;
- feature-map/classifier version;
- evidence hash;
- no ground-truth label.

## Blind Case 001

In addition to aggregate metrics, publish one reviewer-friendly case set of approximately 20 sealed documents.

For each case after label reveal, show:

- prediction;
- ground truth;
- confidence/calibration status;
- whether UNKNOWN was available;
- error/success;
- most relevant measured evidence;
- alternative explanation;
- why the system may have failed.

The case set must include failures. It is not a marketing highlight reel.

## Falsification / stop criteria

The project should narrow or abandon a model-family claim if any of the following persists after reasonable protocol checks:

- performance is not meaningfully above simple length/surface baselines;
- n-grams explain essentially all apparent gains;
- open-world false-known rates remain unsafe at useful coverage;
- transformation robustness collapses to chance while the public use case requires transformed text;
- results do not replicate across prompt/domain holdouts;
- reference fingerprints drift too quickly to remain useful;
- confidence cannot be calibrated well enough to support abstention.

A failed Challenge 001 is still a valuable result if the protocol and artifacts are reproducible.

## Failure report

Publish a dedicated `Where CogniPrint fails` report containing at least:

- shortest reliable length regime observed;
- worst domains;
- hardest source pairs;
- unseen-model behaviour;
- paraphrase/translation degradation;
- human-edit degradation;
- cross-model rewrite degradation;
- calibration failures;
- examples where UNKNOWN prevented a false attribution;
- examples where it did not.

## Fingerprint Registry seed

Challenge 001 should produce the first experimental registry entries keyed conceptually by:

`family → source/version → observation period → benchmark configuration → reference fingerprint`

Registry entries are benchmark references, not immutable identities.

They must record expiry/drift assumptions and the source data used to construct them.

## Evidence bundle

Every published challenge result should map to a machine-readable evidence package containing:

- dataset/manifest hashes;
- exact source/version registry;
- split manifest hash;
- feature/extractor version;
- classifier/baseline version;
- calibration configuration;
- prediction-file hash;
- revealed-label-file hash;
- metrics;
- known limitations;
- software commit;
- reproducibility commands.

The existing CogniPrint Evidence Capsule may be used as one storage/reproducibility representation after its relevant integration gates are satisfied.

## Preregistration gate

Before Stage B begins, freeze at minimum:

- hypotheses;
- model/source list;
- collection dates;
- prompt/task strata;
- generation settings;
- transformation protocols;
- length bins;
- inclusion/exclusion rules;
- lineage grouping and split logic;
- baseline list;
- primary and calibration metrics;
- UNKNOWN decision method;
- stop/falsification criteria.

The preregistration hash and timestamp should be preserved before sealed-test predictions are produced.

## Publication boundary

Until Challenge 001 is executed, the project may say:

> “CogniPrint has a preregisterable protocol for testing model-family fingerprints and open-world abstention.”

It may not say:

> “CogniPrint identifies which model generated arbitrary text.”
