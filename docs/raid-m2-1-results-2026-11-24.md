# RAID M2.1 post-result diagnostics — 24 November 2026

Status: **EXECUTED / POST_RESULT_EXPLORATORY / PRE-FREEZE**

Scientific-claim evidence: **NO**

Parent confirmatory/development record: **RAID M2 #1 remains unchanged**

Challenge 001 Stage B: **NOT_AUTHORISED_TO_START**

## Why this record exists

M2.1 was prospectively frozen **after** the first real M2 result was inspected.
It diagnoses failure modes and one disclosed M2 selective-output gap. It does
not replace, repair, relabel or strengthen M2 #1.

Canonical protocol:

`docs/raid-m2-1-post-result-diagnostics.md`

Tracked as issue #82.

## Execution identity

GitHub workflow:

- workflow: `RAID M2.1 Post-Result Diagnostics`;
- run: `#1`;
- run id: `45373412957`;
- job id: `138373183883`;
- head SHA:
  `576c939d8e491097fdf071476b796437a14a8a68`;
- GitHub artifact id: `14908979740`;
- artifact service digest:
  `sha256:5dfba463455ddf2ab127190727fcc22d2840eb000b88f24d81f1429626127bd8`.

Raw-text-free diagnostic archive:

- SHA-256:
  `b9e8aaccb0816761d19de2aaa1d2329c5a29328fa4541037ab1b59936f79559b`.

Persisted files:

- `m2-1-diagnostics.json` SHA-256:
  `5ab5a4bf99ad9ab2dcfba76fde6a9b38286f64910a5f5c6f39c1a7d2d6792e90`;
- `m2-1-reproducibility.json` SHA-256:
  `607744f280f8a582cfa082655c5de2cd785e6e24b229da4e65723a08ef35b73e`;
- `m2-1-report.md` SHA-256:
  `ffa4c18f321e0d857ba450ea1712e7a4d2a5026a0dacb6463f080f3f3815245c`.

## Parent M2 identity

M2.1 is explicitly bound to the persisted parent M2 result:

`1fb39616725c90470e5dbc35ff7f4211190448e9bb1505c256d5febeba275dc3`

Historical source identity remained unchanged:

- source SHA-256:
  `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- features SHA-256:
  `13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca`;
- selection manifest SHA-256:
  `30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb`;
- source contract SHA-256:
  `e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948`;
- selected / rehydrated records: `500 / 500`;
- duplicate selected IDs: `0`;
- missing selected IDs: `0`;
- unique text hashes: `500`.

## Determinism and privacy

Two complete M2.1 calculations were executed inside the job.

Canonical result hashes:

- run 1:
  `9e90568b3443dd1561bb900c609c0baded57227d25a66b5880d7e0fa5dce0288`;
- run 2:
  `9e90568b3443dd1561bb900c609c0baded57227d25a66b5880d7e0fa5dce0288`.

Deterministic match: **PASS**.

Evidence manifest verification: **PASS (3/3 files)**.

Persisted outputs contain no raw RAID text or raw prompts.

## Finding 1 — the apparent conformal OOD success was ambiguity

This is the most important M2.1 correction.

In M2, conformal false-known singleton rates were near zero. M2.1 decomposed
the non-singleton outcomes.

### Held-out unknown examples — four-fold means

| Representation | Empty set | Ambiguous set | Singleton false-known | Mean set size |
| --- | ---: | ---: | ---: | ---: |
| CogniPrint 12D | **0.0000** | **0.9975** | 0.0025 | 3.2600 |
| Character 3–5 | **0.0000** | **1.0000** | 0.0000 | 3.5775 |
| Word 1–2 | **0.0000** | **0.9950** | 0.0050 | 3.2675 |

There were **no conformal empty-set outcomes for held-out unknown examples in
any representation or fold**.

Therefore the near-zero M2 conformal false-known rate was not evidence that
conformal prediction detected unseen families through empty-set rejection.

It was almost entirely:

```text
multiple known classes remain admissible
-> UNKNOWN_AMBIGUOUS
```

This materially narrows the OOD interpretation.

### Known examples — four-fold means

| Representation | Singleton | Empty | Ambiguous | Prediction-set coverage | Mean set size |
| --- | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D | 0.0058 | 0.0000 | 0.9942 | 0.9334 | 3.2361 |
| Character 3–5 | 0.0280 | 0.0000 | 0.9720 | 0.9892 | 3.4211 |
| Word 1–2 | 0.0610 | 0.0000 | 0.9390 | 0.9728 | 3.1469 |

The alpha-0.05 conformal regime is therefore best described as **extremely
ambiguous/conservative**, not as a useful practical source-family decision
rule.

## Finding 2 — conformal lineage clustering did not explain the ambiguity

For every class in every conformal-calibration fold:

- `records == unique_lineage_groups`;
- largest records per lineage group = `1`;
- median records per lineage group = `1`.

Examples of conformal calibration counts were in the low-to-mid twenties and
thirties per class.

Thus the selected M2 calibration data did **not** contain duplicate records from
the same declared lineage group.

This removes one suspected explanation for the observed ambiguity.

It does not prove the stronger exchangeability assumption required for
conformal validity; it only shows that duplicate lineage clusters were not the
immediate problem.

## Finding 3 — exploratory selective risk does not reveal a 12D advantage

M2.1 froze the post-result exploratory coverage grid before execution:

`0.25, 0.50, 0.60, 0.75, 0.90, 1.00`

The following are four-fold mean selective risks at the first tie-preserving
point reaching each target.

| Target coverage | Mean achieved coverage | 12D risk | Char 3–5 risk | Word 1–2 risk |
| ---: | ---: | ---: | ---: | ---: |
| 0.25 | 0.2596 | 0.4626 | **0.2300** | 0.2512 |
| 0.50 | 0.5086 | 0.4546 | 0.3887 | **0.3037** |
| 0.60 | 0.6023 | 0.4928 | 0.4293 | **0.3842** |
| 0.75 | 0.7626 | 0.5476 | 0.4976 | **0.4199** |
| 0.90 | 0.9063 | 0.5883 | 0.5163 | **0.4566** |
| 1.00 | 1.0000 | 0.6049 | 0.5292 | **0.4623** |

These are descriptive exploratory means. The folds are not treated as
independent inferential units.

12D does not show a selective-risk advantage on this grid.

The result also shows that abstention is not enough by itself: even at roughly
25% coverage, mean 12D selective risk remains about `0.46`.

## Finding 4 — the frozen 60% development-coverage policy generalised poorly

M2 selected a confidence threshold on the threshold-development role with a
minimum requested coverage of `0.60`.

Applied unchanged to known evaluation records, the four-fold means were:

| Representation | Mean evaluation coverage | Coverage range | Mean selective risk | Risk range |
| --- | ---: | ---: | ---: | ---: |
| 12D | 0.6655 | 0.6000–0.7442 | 0.4999 | 0.4375–0.5806 |
| Character 3–5 | 0.5399 | 0.4667–0.6000 | 0.3934 | 0.3182–0.4667 |
| Word 1–2 | 0.5613 | 0.4419–0.6279 | 0.3623 | 0.1053–0.4800 |

The requested 60% development coverage is **not a held-out coverage guarantee**.

For character and word representations, evaluation coverage fell below 60% in
several folds.

The word/Mistral fold had low risk (`0.1053`) but only `0.4419` coverage,
which illustrates why risk must always be reported together with achieved
coverage.

## Finding 5 — the n-gram temperature lower bound was materially restrictive

M2 used temperature bounds `[0.05, 20]`.

All n-gram fits hit the lower bound `T=0.05`.

M2.1 prospectively froze a post-result diagnostic grid extending down to
`0.005`.

Calibration-grid best temperatures were:

### Character 3–5

```text
chatgpt unknown:      0.02
gpt4 unknown:         0.02
llama-chat unknown:   0.02
mistral-chat unknown: 0.01
```

### Word 1–2

```text
chatgpt unknown:      0.02
gpt4 unknown:         0.02
llama-chat unknown:   0.01
mistral-chat unknown: 0.01
```

On already-exposed known evaluation data, the diagnostic-grid temperatures
also produced lower mean proper scores than the frozen M2 temperatures:

| Representation | T=1 NLL | M2-T NLL | M2.1-grid NLL | T=1 Brier | M2-T Brier | M2.1-grid Brier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Character 3–5 | 1.376663 | 1.241039 | **1.178319** | 0.745172 | 0.673324 | **0.617672** |
| Word 1–2 | 1.377229 | 1.234877 | **1.085222** | 0.745452 | 0.670327 | **0.590897** |

Because M2.1 is post-result exploratory, these values do **not** replace the M2
proper-score result and are not new confirmatory evidence.

They do provide strong diagnostic evidence that `T=0.05` was an active
lower-bound restriction for the tested n-gram cosine score scale.

## Finding 6 — 12D has a different score scale and the calibration problem is not a lower-bound problem

M2.1 score summaries show a large representation-scale difference.

Four-fold mean probability-calibration score standard deviation:

- 12D: `0.4833`;
- character n-gram: `0.0450`;
- word n-gram: `0.0208`.

Four-fold mean probability-calibration top1–top2 margin:

- 12D: `0.3338`;
- character n-gram: `0.00956`;
- word n-gram: `0.00939`.

This helps explain why the n-gram score vectors require much smaller scalar
temperatures than 12D.

For 12D, the exploratory calibration grid selected `T=0.5` in all four folds,
close to the original M2 fitted temperatures rather than the lower grid edge.

Four-fold mean known-evaluation proper scores:

| 12D temperature | Mean NLL | Mean Brier |
| --- | ---: | ---: |
| T=1 | **1.277792** | **0.692123** |
| Frozen M2 fitted T | 1.348983 | 0.710081 |
| M2.1 calibration-grid T=0.5 | 1.323997 | 0.705426 |

Thus widening the lower temperature range does **not** rescue the 12D
calibration result.

The calibration-selected 12D temperatures still generalise worse than
uncalibrated `T=1` on average.

## Scientific interpretation

M2.1 sharpens rather than reverses M2.

The evidence now supports these bounded statements:

1. Near-zero conformal false-known singleton rates came almost entirely from
   multi-class ambiguity, not empty-set OOD rejection.
2. Duplicate declared lineage groups were not responsible for that ambiguity.
3. Exploratory risk-coverage analysis does not reveal a hidden 12D selective
   advantage.
4. The 60% threshold-development coverage rule does not guarantee similar
   held-out coverage.
5. The frozen n-gram temperature lower bound was materially restrictive for the
   cosine score scale.
6. The 12D calibration failure is different: a wider lower-bound search does
   not fix it, and uncalibrated `T=1` is better on average on the already
   exposed evaluation data.
7. None of these post-result diagnostics can be promoted to confirmatory M2
   evidence.

## What this changes for future research

A future sealed protocol should not simply rerun M2 with a wider temperature
range.

Before Stage B, the probability model itself needs a prospectively specified
justification.

Candidate methodological questions for independent review include:

- whether cosine-centroid similarities should be treated as logits at all;
- whether a different fixed score transformation is defensible;
- whether calibration should be assessed with nested/grouped resampling;
- whether conformal prediction should target useful singleton coverage rather
  than interpreting ambiguity as OOD rejection;
- whether the current 12D representation should remain only an interpretable
  diagnostic baseline.

## Stop rule reached

This is the one exact M2.1 diagnostic execution specified by the protocol.

The temperature grid, coverage targets, seed, fold definitions and outcomes
must not now be altered to obtain a more favorable result.

Further work requires a separately named protocol.

## Claim boundary

M2.1 does not establish:

- exact model identity;
- universal AI-generated-text detection;
- reliable OOD detection;
- authorship;
- actor/commissioner identity;
- intent or responsibility;
- legal or forensic provenance;
- production readiness.

Scientific readiness remains `descriptive_only`.
