# CogniPrint RESEARCH FREEZE 001 — Candidate

Status: **CANDIDATE_HOLD — NOT FROZEN — NOT REGISTERED — STAGE B NOT AUTHORISED**

Canonical `/RESEARCH_FREEZE_001.md` remains `PRE-FREEZE`.

Normative candidate values are stored in:

- `challenge-001/protocol/frozen/NUMERICAL_FREEZE_DECISIONS_001.candidate.json`;
- `docs/challenge-001-numerical-freeze-decision-memo-001.md`.

This file is a review index for issue #49. It creates no Stage B corpus, labels, source manifest, Research Lock or external registration.

## Scientific boundary

Challenge 001 tests bounded English family-level discrimination plus an explicit UNKNOWN outcome. It does not establish exact model identity, authorship, operator identity, legal responsibility, universal AI origin or forensic provenance.

Stage A showed that fixed character and word n-gram baselines outperformed CogniPrint 12D on RAID Pilot A. Therefore the candidate must permit a negative 12D result and cannot privilege 12D over transparent baselines.

## Candidate scope

- language: English only;
- domains: abstracts, news, reviews, encyclopedic/expository prose;
- tasks: six frozen task strata;
- lengths: `128–255`, `256–511`, `512–900` words;
- primary track: `T0_CLEAN`;
- secondary track: `T1_LIGHT_HUMAN_EDIT`;
- T2–T6: outside Challenge 001.

## Candidate source classes

Known:

- verified pre-2020 human prose;
- Llama 3.1 8B Instruct candidate revision;
- Mistral 7B Instruct v0.3 candidate revision;
- Qwen2.5 7B Instruct candidate revision.

Held out from the reference space:

- Falcon3 7B Instruct candidate revision.

Exact repository IDs, revision hashes, access conditions and licence states are recorded in the machine-readable candidate. Every revision must still resolve locally and the human source registry must be materialised before freeze.

## Candidate sample counts

Cell definition:

`4 domains × 6 tasks × 3 lengths = 72 cells`

Per known class and cell:

- reference: 3;
- probability calibration: 1;
- conformal calibration: 1;
- sealed test: 1.

Held-out unknown per cell:

- sealed test: 3.

Totals:

- per known class: `432`;
- four known classes: `1728`;
- held-out unknown: `216`;
- clean total: `1944`;
- sealed clean total: `504`.

Partition seed is `20260730`; partitioning is by strongest lineage key with deterministic SHA-256 ordering.

## Minimum evidence

Primary evidence requires at least:

- `128` normalized words;
- `600` Unicode letters.

Below the threshold the outcome is `UNKNOWN_INSUFFICIENT_EVIDENCE`. Such cases remain in coverage denominators.

## UNKNOWN method

The candidate uses class-conditional split conformal prediction over cosine nonconformity with alpha `0.05` and a dedicated conformal-calibration partition.

A known class may be returned only when evidence passes and exactly one known class has conformal p-value above `0.05`.

- no passing class: `UNKNOWN_OOD`;
- multiple passing classes: `UNKNOWN_AMBIGUOUS`;
- insufficient evidence: `UNKNOWN_INSUFFICIENT_EVIDENCE`.

Any known assignment for the held-out family is false-known.

## Probability calibration

Candidate method:

- one temperature parameter over frozen class scores;
- probability-calibration partition only;
- temperature bounds `[0.05, 20.0]`;
- 15 equal-frequency ECE bins.

Probability-like wording remains locked unless ECE is at most `0.10` and calibrated NLL/Brier do not worsen.

## Baselines

1. uniform chance;
2. majority;
3. length-only;
4. fixed surface-statistics baseline;
5. CogniPrint 12D;
6. character 3–5 hashed TF-IDF;
7. word 1–2 hashed TF-IDF.

No primary baseline may be added after the blind run begins.

## Claim-narrowing gates

The machine-readable table fixes, among others:

- false-known point estimate at most `0.10` and Wilson upper bound at most `0.15`;
- unknown rejection at least `0.90`;
- known coverage at least `0.60`;
- best-system balanced accuracy and macro-F1 at least `0.50`;
- 12D improvement over the best n-gram at least `0.02` with paired 95% interval above zero for any incremental-value claim;
- per-known-class recall at least `0.40` for a uniform claim;
- domain balanced accuracy at least `0.40` and no domain more than `0.15` below overall;
- T1 degradation no more than `0.15` balanced accuracy or `0.05` false-known increase.

A failed gate remains publishable but narrows or locks the relevant claim.

## Exclusion boundary

Only objective pre-run failures may exclude a candidate: unreadable/hash-mismatched artifact, licence/consent failure, exact or frozen near-duplicate, visible source-label leak, or lineage/partition violation.

Refusal, difficult style, low quality or unfavourable behaviour are not exclusions. After the blind run starts, no replacement is allowed.

## HOLD blockers

- exact human source manifest;
- local model revision and artifact verification;
- licence/access review;
- development-only implementation and tests;
- independent methodological review;
- issue #30 runner evidence or accepted equivalent;
- candidate blinded/sealed manifests;
- real Stage A/B zero-overlap audit;
- final Research Lock;
- external timestamped registration.

Until all blockers pass:

```text
CANONICAL_RESEARCH_FREEZE = PRE-FREEZE
CANDIDATE = HOLD
EXTERNAL_REGISTRATION = NOT_SUBMITTED
STAGE_B = NOT_AUTHORISED_TO_START
```
