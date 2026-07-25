# CogniPrint Attribution Challenge 001 — Preregistration Submission Packet

Status: **HOLD — DO NOT SUBMIT WHILE `RESEARCH_FREEZE_001.md` IS `PRE-FREEZE`**

Purpose: provide a copy-ready preregistration package for an external timestamped registration service once Challenge 001 is genuinely frozen.

Recommended registration path: use a general-purpose preregistration template suitable for a prospective empirical benchmark (for example, OSF Preregistration) unless a more appropriate community template is identified before submission.

## Submission gate

This packet may be submitted only when all of the following are true:

- `RESEARCH_FREEZE_001.md` status is `FROZEN`;
- every `TO BE FILLED AT FREEZE` field is resolved;
- the frozen file SHA-256 is preserved;
- exact CogniPrint/evaluator commits are recorded;
- source families, sample counts, languages/domains and holdouts are frozen;
- minimum-evidence, OOD/UNKNOWN and calibration methods are frozen;
- exclusions, primary metrics and stop/claim-narrowing criteria are frozen;
- issue #30 has actual executed runtime-test evidence or an equivalent reproducible-runner record exists;
- no sealed Stage B analysis has occurred.

If any item is false, the preregistration remains `HOLD`.

## Proposed title

**CogniPrint Attribution Challenge 001: A preregistered blind evaluation of model-family signal, calibration and open-world abstention in synthetic-language fingerprints**

## Study type / design summary

Prospective, preregistered, blind benchmark evaluation.

The study tests whether a fixed set of interpretable content-derived features contains model-family information beyond transparent confounders under controlled conditions, while requiring calibrated abstention for unsupported or out-of-distribution cases.

The design separates:

- directly measured evidence (`OBSERVED`);
- statistical inference (`INFERRED`);
- external provenance (`ATTESTED`);
- insufficient/unsupported conclusions (`UNKNOWN`).

Challenge 001 concerns family-level statistical inference only. It does not test author identity, commissioner/operator identity, intent, legal responsibility, universal AI origin, or forensic provenance.

## Research question

> Under what preregistered conditions, if any, is model-family attribution scientifically defensible beyond simple confounders while preserving an explicit UNKNOWN / insufficient-evidence outcome for unsupported cases?

## Primary hypothesis

Under leakage-safe and preregistered evaluation, at least some generation processes may exhibit stable multivariate differences that permit model-family discrimination above transparent length/surface/n-gram baselines within a bounded reference space, while open-world and transformed inputs require calibrated abstention.

This hypothesis is allowed to fail.

## Non-hypotheses / prohibited interpretations

Challenge 001 does not establish:

- exact-model identity in the open world;
- authorship identity;
- actor/operator/commissioner identity;
- intent or responsibility;
- legal or regulatory status;
- definitive AI origin;
- validated forensic provenance;
- universal generalisation across languages/domains/models;
- production readiness.

## Source population / model families

**FROZEN VALUE REQUIRED BEFORE SUBMISSION**

- known reference families: `TO BE COPIED FROM RESEARCH_FREEZE_001.md`
- held-out unknown family/families: `TO BE COPIED FROM RESEARCH_FREEZE_001.md`
- exact endpoints/checkpoints/versions: `TO BE COPIED FROM RESEARCH_FREEZE_001.md`
- collection/generation window: `TO BE COPIED FROM RESEARCH_FREEZE_001.md`
- human-control definition: `TO BE COPIED FROM RESEARCH_FREEZE_001.md`

No source family may be added or removed after sealed predictions are produced.

## Sample size and strata

**FROZEN VALUE REQUIRED BEFORE SUBMISSION**

- total sample count: `TBD AT FREEZE`
- samples per source family/control: `TBD AT FREEZE`
- prompt/task strata: `TBD AT FREEZE`
- length strata: `TBD AT FREEZE`
- domain strata: `TBD AT FREEZE`
- language strata: `TBD AT FREEZE`
- transformation strata included in primary analysis: `TBD AT FREEZE`
- exploratory transformation strata: `TBD AT FREEZE`

The sample design must be fixed before sealed predictions.

## Inclusion criteria

Final criteria must be copied verbatim from `RESEARCH_FREEZE_001.md`.

At minimum, an included sample must:

- have a unique sample ID;
- have documented source-family/control provenance in the hidden ground truth;
- have a cryptographic artifact/content hash where permitted;
- belong to a frozen prompt/task/length/language/domain stratum;
- satisfy the frozen collection protocol;
- have a documented lineage key that prevents parent/child leakage.

## Exclusion criteria

**FROZEN VALUE REQUIRED BEFORE SUBMISSION**

Exclusion criteria must be objective and independent of sealed performance.

No post-reveal exclusion may replace the primary preregistered result. Any post-reveal exclusion must be disclosed as a protocol deviation/sensitivity analysis alongside the unchanged primary result.

## Data leakage and contamination controls

The following are prohibited:

- train/reference/test duplicates or near-duplicates;
- parent/child transformed samples split across partitions;
- prompt-linked response families split in a way that leaks source information;
- source labels embedded in filenames/directories/metadata exposed to the predictor;
- reference examples selected after sealed-test labels or outcomes are inspected;
- development/debug access to sealed labels;
- manual cherry-picking of public demo cases before blind evaluation is complete.

A Dataset Lineage Ledger / manifest must record development visibility, reference-set membership and evaluation visibility for each sample.

## Partitioning / blinding

**FROZEN VALUE REQUIRED BEFORE SUBMISSION**

- lineage grouping key: `TBD AT FREEZE`
- reference/training split: `TBD AT FREEZE`
- calibration split: `TBD AT FREEZE`
- sealed challenge split: `TBD AT FREEZE`
- held-out unknown-generator split: `TBD AT FREEZE`

Ground-truth labels for the sealed challenge set must be unavailable to the prediction process until predictions are frozen and hashed.

## Prediction freeze

The pipeline must produce `predictions.jsonl` without access to sealed labels.

Before label reveal preserve:

- prediction file SHA-256;
- CogniPrint commit SHA;
- evaluator commit SHA;
- feature/reference/calibration versions;
- environment/dependency lock hash;
- configuration hash;
- prediction-generation timestamp.

No model, threshold, feature, calibration or exclusion change is allowed after prediction freeze for the primary analysis.

## Minimum Evidence Policy

A minimum-evidence rule is mandatory.

The exact threshold/criterion must be selected before sealed evaluation from non-sealed development/validation evidence and copied from `RESEARCH_FREEZE_001.md`.

If minimum evidence is not met, the permitted outcome is `UNKNOWN / INSUFFICIENT EVIDENCE`, not forced classification.

## OOD / UNKNOWN method

**FROZEN VALUE REQUIRED BEFORE SUBMISSION**

Record:

- reference-space membership method;
- OOD statistic/score;
- threshold-selection procedure;
- held-out-generator protocol;
- insufficient-evidence rule.

The primary open-world question is whether the system can avoid a false known-family claim when the correct source family is absent from the reference space.

## Calibration method

**FROZEN VALUE REQUIRED BEFORE SUBMISSION**

Record:

- calibration method;
- calibration partition;
- ECE binning;
- interpretation of reported confidence/probability;
- preregistered acceptance criterion for any calibrated-confidence claim.

If the acceptance criterion is not met, the Claim Firewall must keep calibrated-attribution language locked.

## Baselines

Required baseline set:

1. chance expectation;
2. majority class;
3. length-only;
4. simple punctuation/surface statistics;
5. current CogniPrint 12D feature map;
6. character n-gram classifier;
7. word n-gram classifier.

Any additional learned model/baseline included in the primary comparison must be frozen before sealed predictions.

## Primary outcomes / metrics

Report at minimum:

- Top-1 accuracy with abstentions handled explicitly;
- macro-F1 with explicit zero-division semantics;
- balanced accuracy;
- per-class precision/recall/F1;
- confusion matrix;
- coverage;
- selective accuracy;
- selective risk;
- held-out-generator unknown rejection rate;
- held-out-generator false-known rate;
- Brier score only when frozen calibrated class probabilities exist;
- Expected Calibration Error only when frozen calibrated confidence exists.

Raw accuracy alone is not a sufficient primary result.

## Secondary / robustness outcomes

Only tracks frozen before submission may be interpreted as preregistered robustness results.

Candidate tracks include:

- light human edit;
- substantial human rewrite;
- translation round-trip;
- AI paraphrase;
- cross-model rewrite;
- mixed multi-stage chain.

For each included track report degradation relative to the clean condition and the effect on UNKNOWN/false-known behavior.

## Stop / falsification / claim-narrowing rules

**NUMERIC CRITERIA REQUIRED BEFORE SUBMISSION WHERE SCIENTIFICALLY DEFENSIBLE**

At minimum the model-family claim remains locked or is narrowed if preregistered failure conditions show any of the following at unacceptable levels:

- false-known behavior on held-out generators;
- calibration failure;
- performance explained primarily by trivial confounders;
- domain/generalisation collapse inconsistent with the intended claim scope;
- insufficient replication across frozen strata;
- instability under transformations that are part of the intended use case.

A negative or mixed result is publishable and does not invalidate the study.

## Analysis plan

1. Validate that prediction/label sample sets match after reveal.
2. Run the independent evaluator without fitting/tuning.
3. Compute preregistered closed-set and open-world metrics.
4. Compute calibration metrics only if frozen calibrated outputs exist.
5. Report all frozen strata/holdouts and transformation tracks.
6. Preserve all artifact hashes.
7. Publish failures and scope restrictions before or alongside positive claims.

Any exploratory post-reveal analysis must be labelled exploratory and must not replace the preregistered primary result.

## Failure-first reporting plan

The public result must include a `Where CogniPrint Fails` section covering, where included in the frozen protocol:

- unseen-generator false-known rate;
- minimum reliable evidence/length regime;
- hardest source-family pairs;
- domain shift;
- translation degradation;
- human-edit degradation;
- model-to-model rewrite degradation;
- calibration failures;
- cases where UNKNOWN prevented a false claim;
- cases where UNKNOWN failed to prevent one.

Only after these boundaries are shown may the report state what worked within the validated scope.

## Artifact and reproducibility plan

Preserve at minimum:

- frozen protocol hash;
- repository commit SHA;
- evaluator commit/hash;
- dataset/corpus manifest hash;
- split manifest hash;
- reference registry hash;
- predictions hash;
- revealed labels hash;
- results/evaluator output hash;
- environment/dependency lock hash;
- integrity-verifiable evidence bundle.

The evidence bundle must not be called cryptographically signed until issue #27 is closed with a real verified signature implementation.

## Ethics / high-stakes boundary

Challenge 001 is research evaluation, not a disciplinary or legal decision system.

CogniPrint output must not by itself be used to:

- accuse a person of misconduct;
- punish a student;
- discipline or terminate an employee;
- determine legal responsibility;
- identify an operator/commissioner from text alone.

The study is designed to quantify technical evidence boundaries, including false-positive/false-known risks.

## Deviations after registration

Any unavoidable change after submission must be documented transparently as a registration update/deviation with:

- what changed;
- why it changed;
- when it changed;
- whether sealed predictions had already been produced;
- expected scientific impact;
- whether the primary preregistered analysis remains valid.

Silent rewriting of the registered plan is prohibited.

## Registration visibility decision

Decision required at submission:

- **public immediately** — maximises transparent timestamping/discoverability and normally receives a public DOI; or
- **embargoed** — only if a concrete blinded-review/data-release reason requires temporary privacy.

Do not choose embargo merely to hide an unfavourable result or an incomplete protocol.

## Submission metadata

- title: as above unless frozen version changes it;
- contributors: `TO BE VERIFIED AT SUBMISSION`;
- license: `TO BE VERIFIED AT SUBMISSION`;
- subjects/tags: synthetic content, model attribution, calibration, out-of-distribution detection, provenance, reproducibility;
- linked repository commit: `TO BE FILLED AT FREEZE`;
- linked protocol SHA-256: `TO BE FILLED AT FREEZE`.

## Final pre-submit checklist

- [ ] `RESEARCH_FREEZE_001.md` says `FROZEN`;
- [ ] no unresolved placeholders remain in the frozen protocol;
- [ ] issue #30 has actual executed test evidence or equivalent runner evidence;
- [ ] source/model list is exact and versioned;
- [ ] sample counts/strata are exact;
- [ ] minimum-evidence/OOD/calibration methods are exact;
- [ ] metrics/exclusions/stop criteria are exact;
- [ ] protocol/commit hashes are preserved;
- [ ] sealed labels have not been analysed;
- [ ] registration text matches the frozen repository protocol;
- [ ] visibility/public-vs-embargo decision is deliberate;
- [ ] submission reviewed for unsupported attribution/legal/forensic claims.

Until all boxes are checked: **DO NOT SUBMIT**.
