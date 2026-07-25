# Challenge 001 — Development Exposure Registry

Status: `ACTIVE PRE-FREEZE CONTROL`

Purpose: record data sources/corpora that have already been visible to development, analysis, debugging, benchmark design, threshold/calibration planning, or public release work and therefore **must not later be represented as sealed Stage B evidence** for Challenge 001.

This registry is intentionally conservative. When uncertain whether a corpus influenced development, classify it as development-visible.

## Quarantined from sealed Stage B

### 1. CogniPrint Public Benchmark v1.1

Repository roots:

- `datasets/public-benchmark-v1.1/`
- `evidence/public-benchmark-v1.1/`

Exposure reason:

- released publicly inside the CogniPrint repository;
- contains 20 baseline excerpts and 120 controlled variants;
- has already been used for descriptive validation/evidence work;
- source classes, languages, perturbation axes and provenance metadata are visible to the project.

Allowed Challenge 001 use:

- Stage A feature-stability checks;
- development-only perturbation diagnostics;
- minimum-evidence/length feasibility exploration where appropriate;
- evaluator/pipeline sanity.

Forbidden use:

- sealed Stage B performance evidence;
- a post-hoc holdout presented as previously unseen merely because a subset was not used in one script run.

### 2. RAID config `raid`, split `train`, as defined by M1 Pilot A

Pinned dataset revision:

`865cac74188466cb0c3b7574a10204007b57a459`

Exposure reason:

- the repository already specifies the development matrix using known labels/classes: `human`, `chatgpt`, `gpt4`, `llama-chat`, `mistral-chat`;
- domains and selection policy are already visible;
- the intended baseline-analysis procedure is already documented;
- any run of this pilot is explicitly suitable for development/stress testing, not a future claim that labels/configuration were unknown.

Allowed Challenge 001 use:

- Stage A source-family feasibility;
- development of lineage grouping;
- minimum-evidence exploration;
- OOD/calibration method prototyping when clearly marked development-only;
- feature/baseline comparison and robustness planning.

Forbidden use:

- sealed Stage B claim evidence under the same exposed selection/label policy.

## Exposure rule for future data

A source/corpus must be added here if any of the following occurs before Stage B prediction freeze:

- labels are inspected during development;
- examples are manually reviewed to tune features/thresholds/calibration/OOD;
- samples are used in debugging;
- samples are used to choose public demo cases;
- samples appear in reference/calibration/training data;
- data selection logic is altered after observing its performance;
- ground truth is available to the process that chooses inference rules.

Adding a source to this registry is not a failure. It simply reserves it for development rather than sealed evaluation.

## Stage B rule

Stage B must be constructed from a separately frozen manifest and must pass `scripts/check_challenge_leakage.py` against all materialised Stage A manifests.

At minimum:

```text
sample_id_overlap = 0
content_hash_overlap = 0
```

Any ambiguity about prior development visibility is resolved in favor of **development-visible**, not sealed.

## Current consequence

As of this pre-freeze state, neither `public-benchmark-v1.1` nor the documented RAID `raid/train` Pilot A matrix can serve as the sealed Stage B evidence that unlocks model-family attribution claims.
