# CogniPrint current state

Status date: 24 November 2026.

CogniPrint is an MIT-licensed research framework for constructing compact statistical fingerprints of text and building reproducible evidence about synthetic-language production processes without collapsing measurement, inference, external provenance and uncertainty into one verdict.

## Current scientific status

- Scientific readiness: `descriptive_only`
- Research mode: `PROOF_MODE`
- Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`
- Hosted-runner execution: `PASS / ACTIVE`
- External methodological reviews: `0/1`
- Release line: `v0.1.2`
- DOI: pending direct public Zenodo verification
- Repository: https://github.com/TakoVHS/CogniPrint-open

The current public release supports reproducible **measurement and evidence structuring**, not validated source attribution.

## Hosted-runner status

The historical GitHub Actions `steps: []` blocker is resolved.

Fresh minimal canary on 24 November 2026:

- workflow: `Runner Canary Current`;
- run id: `45371785458`;
- conclusion: `success`;
- log contains `RUNNER_EXECUTED`;
- log contains `PYTHON_EXECUTED`;
- Python reported `3.14.4`.

Issue #30 is closed as completed.

Current hosted workflows also execute successfully for:

- Stage A Methods CI on Python 3.10 / 3.11 / 3.12;
- RAID M2 Development CI on Python 3.10 / 3.11 / 3.12;
- RAID Pilot Adapter CI;
- Public Release CI;
- real pinned RAID M2 external evidence execution.

This resolves an infrastructure blocker only. It does not unlock a scientific claim.

## Implemented measurement core

CogniPrint currently provides:

- a documented 12-dimensional text profile `φ(T)`;
- profile comparison with Euclidean distance and cosine similarity;
- corpus-relative exploratory diagnostics;
- perturbation analysis;
- corpus aggregation and dispersion summaries;
- entropy and word/character n-gram diagnostics;
- reproducibility, validation, benchmark and evidence artifacts.

## Implemented trust/evidence foundation

The repository contains:

- **Evidence Schema v1** with `OBSERVED`, `INFERRED`, `ATTESTED`, `UNKNOWN`;
- **Claim Firewall v1** that keeps attribution disabled until explicit evidence/calibration/OOD gates are satisfied;
- exact-model identity blocked as content-only inference;
- authorship, actor/commissioner, intent/responsibility and legal/forensic conclusions blocked as content-only claims;
- machine-readable limitation states;
- provenance-conflict handling;
- deterministic `.cogcase` manifest/integrity primitives;
- Data Constitution and benchmark governance;
- calibration/OOD/holdout evaluation contracts;
- an independent sealed-challenge evaluator architecture;
- Research Lock tooling for deterministic integrity binding.

These are research controls, not validation that source attribution works.

## Stage A evidence already executed

Stage A is development-only and is not blind Challenge 001 evidence.

### Historical RAID M1

The fixed M1 comparison remains:

- CogniPrint 12D macro-F1: `0.535883`;
- character 3–5 hashed TF-IDF: `0.578782`;
- word 1–2 hashed TF-IDF: `0.595220`.

Both tested lexical baselines outperformed 12D on that fixed closed-set task.

### RAID M2 — calibration, abstention and open-set development

The first real pinned M2 run completed on 24 November 2026.

All historical input gates passed before metrics were produced:

- authoritative `train_none.csv` byte size: `801662741`;
- source SHA-256:
  `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- regenerated features SHA-256:
  `13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca`;
- selected-record manifest SHA-256:
  `30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb`;
- source-contract SHA-256:
  `e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948`;
- selected records: exactly `500`.

Primary external run:

- workflow run: `45370233451`;
- evidence archive SHA-256:
  `93c2cdb6c05919fb3ba348c948c73a836358da633352e566c243dd6c8a1e2352`.

An independent repeat external run `45371006757` reproduced the persisted `m2-results.json` byte-for-byte.

Persisted result SHA-256:

`1fb39616725c90470e5dbc35ff7f4211190448e9bb1505c256d5febeba275dc3`

### M2 aggregate result

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D cosine centroid | 0.382981 | 1.348983 | 0.710081 | 0.511947 | 0.657500 |
| Character 3–5 hashed TF-IDF | 0.447966 | 1.241039 | 0.673324 | 0.338034 | **0.485000** |
| Word 1–2 hashed TF-IDF | **0.515231** | **1.234877** | **0.670327** | **0.303210** | 0.512500 |

The first real M2 result is **negative/mixed**, not a 12D win.

Important findings:

- lexical baselines have stronger aggregate point estimates on the principal tested metrics;
- all predeclared per-fold 95% paired proper-score bootstrap intervals include zero;
- scalar temperature scaling worsened held-out 12D NLL in all four folds;
- both n-gram temperature fits repeatedly hit the lower bound `T=0.05`;
- max-confidence open-set ranking remained weak;
- conformal prediction was extremely conservative, with near-zero false-known singleton behavior but very low known singleton rates.

Correct scientific interpretation:

> Current evidence favors abstention and claim narrowing rather than stronger source attribution.

Full records:

- `docs/raid-calibration-m2-development.md`;
- `docs/raid-m2-results-2026-11-24.md`;
- `evidence/raid-m2/2026-11-24/summary.json`;
- `reviewer-bundle/m2-results.md`.

## M2.1 — post-result failure analysis

A separate post-result diagnostic protocol was frozen after M2 #1 and executed once.

Status:

`POST_RESULT_EXPLORATORY / EXECUTED`

Workflow run: `45373412957`.

Evidence archive SHA-256:

`b9e8aaccb0816761d19de2aaa1d2329c5a29328fa4541037ab1b59936f79559b`

Main findings:

- conformal unknown empty-set rate was `0.0` in every fold/representation;
- the near-zero M2 conformal false-known result came almost entirely from multi-class ambiguity;
- exploratory matched-coverage risk did not reveal a 12D selective advantage;
- the 60% development-coverage threshold was not a held-out coverage guarantee;
- the n-gram `T=0.05` lower bound was materially restrictive for their cosine-score scale;
- a wider lower-temperature grid did not rescue 12D calibration;
- duplicate declared lineage groups did not explain conformal ambiguity.

M2.1 is failure analysis only and cannot replace M2 #1.

Full records:

- `docs/raid-m2-1-post-result-diagnostics.md`;
- `docs/raid-m2-1-results-2026-11-24.md`;
- `evidence/raid-m2-1/2026-11-24/summary.json`.

## Reproducibility and privacy state

The real M2 evidence path verifies:

- exact source/features/selection/source-contract identity;
- deterministic repeated calculation;
- raw source not persisted;
- raw prompts not persisted;
- raw generations not persisted;
- recoverable vocabulary not persisted;
- evidence archive and sidecar hashes.

This is engineering/research reproducibility evidence, not independent scientific replication by another group.

## Challenge 001 integrity controls

Challenge 001 has explicit pre-freeze controls:

- physically separated Stage A development and sealed Stage B namespaces;
- blinded Stage B sample schema;
- separate revealed-label schema;
- Development Exposure Registry;
- Stage A/Stage B visibility invariants;
- machine-readable leakage audit;
- Research Lock 001 tooling.

Already inspected RAID/public benchmark material remains development-visible and cannot later be represented as sealed Stage B evidence.

The final Research Lock hash does not yet exist because the protocol remains `PRE-FREEZE`.

## Proof mode / feature freeze

The no-new-headline-feature rule remains active.

Allowed work is limited to:

1. correctness/security fixes;
2. reproducibility;
3. test/runner infrastructure;
4. Stage A diagnostics needed to freeze the protocol;
5. preregistration/freeze work;
6. benchmark integrity/sealing;
7. corrections required to keep public claims aligned with evidence;
8. external methodological review preparation.

Post-result tuning must not overwrite M2. Any score-scale/temperature/conformal diagnostic is a separate exploratory protocol.

## Stage B remains blocked

Stage B is **not authorised to start**.

Before Stage B, the project still needs:

1. final candidate Stage A/Stage B manifests;
2. leakage-audit PASS for the frozen candidate;
3. frozen numerical/operational choices;
4. final Research Lock 001;
5. external timestamped preregistration;
6. sealed corpus/reference/split custody;
7. frozen predictions before label reveal;
8. independent post-reveal evaluation;
9. public failure analysis;
10. Scientific Claim Review.

The executed M2 cannot be reused as sealed Stage B evidence.

## External methodological review

External methodological review remains `0/1`.

The reviewer packet now includes the actual M1/M2 negative/mixed results rather than only proposed protocols.

A critical or negative independent review can satisfy the review definition. Endorsement is not required.

Closing the review counter alone does not change `descriptive_only`.

## External-provenance / regulatory interfaces

Documented interfaces still include:

- C2PA / Content Credentials bridge contract;
- Article-50-oriented transparency mapping with explicit non-certification boundary;
- NIST AI RMF mapping with explicit non-certification boundary.

The C2PA runtime reader/validator is not yet implemented or validated.

## Critical boundary

CogniPrint does **not** currently establish from text alone:

- a unique author;
- a unique/exact source model;
- definitive AI origin;
- generation-lineage reconstruction;
- who commissioned/requested generation;
- intent or responsibility;
- legal status;
- forensic provenance suitable for high-stakes decisions.

Content-derived signals can support bounded research hypotheses. Claims about actors, tools, workflow history or legal effect require independent evidence appropriate to the specific claim.

## Open gates

- external methodological review: `0/1`;
- DOI reference: not directly publicly verified;
- Challenge 001 research freeze: `PRE-FREEZE`;
- final candidate Stage A/Stage B leakage audit: open;
- final Research Lock 001: not generated;
- Challenge 001 external preregistration: open issue #28;
- Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`;
- C2PA runtime validation: open issue #26;
- detached `.cogcase` signatures: open issue #27;
- independent external replication: not completed.

Resolved:

- hosted-runner execution blocker: issue #30 **closed**;
- real RAID M1 development evidence: executed;
- real pinned RAID M2 development evidence: executed and independently repeated at the engineering level.

## Positioning

CogniPrint should be understood as an **evidence-first cognitive-provenance research programme**.

Its scientific value is not a headline AI score. It is the discipline of preserving what was measured, what was inferred, what failed, what remains unknown, and which claims the evidence still does not justify.
