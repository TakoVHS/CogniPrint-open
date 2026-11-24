# RAID M2 — calibration, abstention and open-set development protocol

Status: `DEVELOPMENT_ONLY / NOT EXECUTED ON REAL RAID M2`

Scientific-claim evidence: `NO`

Canonical Challenge 001 freeze: `PRE-FREEZE`

Stage B: `NOT_AUTHORISED_TO_START`

## Purpose

M2 is a follow-on Stage A development study motivated by the fixed M1 result
where both tested lexical n-gram baselines outperformed the compact CogniPrint
12D representation on closed-set macro-F1.

M2 does not attempt to repair that historical result. It asks a different,
prospectively specified question:

> Under lineage-disjoint development evaluation, how do compact 12D and lexical
> representations differ in probability quality, selective-risk behavior and
> false-known behavior when the scoring family and calibration procedure are
> controlled?

Positive, mixed and negative outcomes are all admissible.

## Inherited source boundary

M2 reuses the same already-selected Stage A RAID material and source custody
contract used by M1. The current historical pins are:

- authoritative source: RAID `train_none.csv`;
- source SHA-256:
  `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- source byte size: `801662741`;
- selected metadata-only features SHA-256:
  `13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca`;
- selected-record manifest SHA-256:
  `30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb`;
- source-contract SHA-256:
  `e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948`;
- selected records: `500`;
- exposed classes: `human`, `chatgpt`, `gpt4`, `llama-chat`,
  `mistral-chat`.

The raw source and metadata evidence are local execution inputs. The public
repository does not contain the real `features.jsonl` or raw source CSV.

## Privacy boundary

The M2 CLI must:

1. verify the raw source SHA-256;
2. verify the metadata features SHA-256;
3. verify the selected-record manifest SHA-256;
4. verify the machine-readable source contract;
5. rehydrate only the selected source rows;
6. verify generation and prompt hashes against the metadata selection;
7. keep generation text, prompt text, token strings, n-gram strings, sparse
   vectors, IDF maps and centroids in memory only;
8. persist only metadata manifests, hashes and aggregate/statistical outputs.

A public evidence artifact must not contain `generation`, `prompt`,
`raw_text`, `raw_prompt`, `_text`, recoverable vocabulary, token lists or
n-gram strings.

## Open-set design

The human control is always a known class.

The four machine families are evaluated with a predeclared
leave-one-machine-family-out design, in this order:

1. `chatgpt` unknown;
2. `gpt4` unknown;
3. `llama-chat` unknown;
4. `mistral-chat` unknown.

Each fold therefore has four known classes including the human control and one
fully excluded machine family.

This is development-visible leave-one-family-out analysis. Because all five
labels are already known to the research process, it is **not** a blind
external unknown-source test.

## Lineage-safe role assignment

Lineage key semantics remain the M1 rule:

1. `source_id`;
2. otherwise `prompt_sha256`;
3. otherwise `text_sha256`.

M2 role-assignment seed is fixed to:

`20261124`

Known-only lineage groups are assigned deterministically by SHA-256 hash into:

- classifier/reference training: `0.35`;
- probability calibration: `0.15`;
- conformal calibration: `0.30`;
- threshold development: `0.10`;
- held-out development evaluation: `0.10`.

The fractions sum to one.

If any lineage group contains a record from the designated unknown family, the
**entire lineage group** is forced into the evaluation role. This prevents a
known-class sibling from the same lineage leaking into fitting while the
unknown sibling is evaluated.

Any overlap between role lineage sets is a hard error.

The role seed and fractions must not be changed after real M2 metrics are
inspected.

## Conformal resolution gate

Primary conformal alpha:

`0.05`

The class-conditional finite-sample p-value resolution requirement is:

`ceil((1 - alpha) / alpha) = 19`

Therefore every known class must contribute at least 19 records to the
conformal-calibration role in every fold.

If any real fold fails this requirement, M2 reports:

`INSUFFICIENT DEVELOPMENT EVIDENCE`

The response is **not** to change the seed, alpha or role fractions after
seeing performance.

A future protocol amendment may be proposed separately, timestamped and
justified without reusing the failed run as if it had been prospectively
specified.

## Representations

### CogniPrint 12D — M2 scoring variant

M2 uses the existing normalized 12D feature record with:

- training-role standardization only;
- L2 normalization;
- deterministic cosine nearest centroid;
- lexical label tie-break.

This is a new M2 scoring variant. It must not be silently substituted for the
historical M1 12D nearest-centroid number.

### Character n-gram

Historical representation settings are retained:

- Unicode NFKC;
- casefold;
- character n-grams 3–5;
- SHA-256 hashing into `262144` bins;
- `1 + log(count)` TF;
- train-only IDF `log((1+n_train)/(1+df))+1`;
- L2 normalization;
- cosine nearest centroid.

### Word n-gram

Historical settings are retained:

- word n-grams 1–2;
- SHA-256 hashing into `131072` bins;
- otherwise the same TF/IDF/normalization/scoring procedure.

No vocabulary is persisted.

## Probability semantics and temperature scaling

For each representation, the frozen centroid-similarity score vector is treated
as a logit-like score vector for the purpose of a single scalar
temperature transform.

Temperature bounds remain:

`[0.05, 20.0]`

Temperature is fitted **only** on the probability-calibration role by minimizing
multiclass NLL.

Positive scalar temperature preserves score ordering and therefore preserves
the top-1 class for each example.

Temperature is then frozen before threshold development, conformal calibration
and held-out evaluation.

## Probability-conformal prediction

M2 uses a representation-agnostic class-conditional split-conformal layer on
the separately temperature-scaled probability vectors.

For calibration example `(x_i, y_i)`:

`score_i = 1 - p(y_i | x_i)`

For candidate class `k` on a new example:

`candidate_score = 1 - p(k | x)`

The class-conditional conformal p-value is:

`(1 + count(calibration_score >= candidate_score)) / (n_class + 1)`

Decision mapping:

- exactly one accepted class -> candidate known class;
- zero accepted classes -> `UNKNOWN_OOD`;
- more than one accepted class -> `UNKNOWN_AMBIGUOUS`.

The coverage interpretation applies to prediction sets under the relevant
class-conditional exchangeability assumptions. It is not a guarantee of
singleton correctness and not an OOD-rejection theorem.

## Threshold-development policy

The transparent max-confidence open-set baseline uses a threshold selected
**only** on the threshold-development role.

Minimum requested known coverage is fixed to:

`0.60`

The rule selects the highest observed confidence threshold whose
threshold-development coverage is at least 0.60, with exact confidence ties
accepted together.

No unknown-family evaluation label participates in threshold selection.

## Primary outcomes

### Probability quality

Primary:

- held-out multiclass NLL;
- held-out multiclass Brier score;
- lineage-group paired confidence intervals for CogniPrint-minus-baseline NLL;
- lineage-group paired confidence intervals for CogniPrint-minus-baseline
  Brier.

For loss deltas, negative values favor CogniPrint.

Bootstrap:

- complete lineage groups resampled together;
- `10000` resamples;
- fixed base seed `20261124`;
- Brier comparison seed `20261125`;
- 95% percentile interval.

### Selective/open-set

Primary:

- known-class selective risk at matched coverage operating points;
- achieved known coverage;
- false-known rate on the held-out unknown family;
- Wilson interval for false-known rate;
- conformal unknown false-known rate;
- conformal unknown rejection rate.

Secondary:

- AURC;
- known-vs-unknown AUROC;
- top-label ECE;
- macro classwise ECE;
- reliability plots.

Closed-set macro-F1 and balanced accuracy remain mandatory context.

## Four-fold reporting rule

Every machine-family fold must be reported individually.

The aggregate table may report means across the four folds, but the aggregate
must not replace family-specific results.

A result favorable only for one held-out family must be described as
family-specific.

## Determinism

The CLI executes the complete M2 calculation twice with the same inputs and
parameters.

The two canonical JSON payload hashes must be identical.

Mismatch is a hard failure.

## Falsification / claim-narrowing

The evidence does not support a stronger M2 claim when an apparent advantage:

- disappears under lineage-disjoint roles;
- depends on test-tuned temperature or threshold;
- appears only in a chosen ECE binning while NLL/Brier do not support it;
- requires near-universal abstention;
- appears only for one convenient unknown family;
- disappears under the fixed n-gram representations;
- requires changing the role seed after observing results;
- relies on hiding worse closed-set performance.

Negative and mixed results must remain in the evidence record.

## Current implementation status

Implemented in Draft PR #81:

- in-memory 12D/n-gram score matrices;
- deterministic five-role fold builder;
- four leave-one-machine-family-out folds;
- held-out temperature evaluation;
- probability-conformal calibration;
- tie-preserving risk-coverage / AURC;
- pre-frozen max-confidence open-set baseline;
- false-known / Wilson / AUROC metrics;
- lineage-group paired proper-score bootstrap;
- pinned-source M2 CLI;
- deterministic rerun and privacy output checks;
- dedicated Python 3.10 / 3.11 / 3.12 M2 development CI.

## Real-evidence status

Real pinned RAID M2 run: `NOT EXECUTED`.

No values from synthetic CI fixtures are scientific M2 outcomes.

No DOI, preregistration, Stage B authorization, attribution claim expansion or
external methodological review follows from this protocol alone.
