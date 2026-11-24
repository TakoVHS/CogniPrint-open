# RAID M2.1 — post-result diagnostic protocol

Status: `POST_RESULT_EXPLORATORY / NOT EXECUTED`

Parent result: `RAID M2 #1 — EXECUTED / DEVELOPMENT_ONLY / PRE-FREEZE`

Scientific-claim evidence: `NO`

Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`

## Why M2.1 exists

The first real pinned M2 result is preserved unchanged.

M2.1 is created **after** M2 result inspection to investigate four concrete
methodological findings:

1. the M2 protocol named matched-coverage selective risk as a primary outcome,
   but no concrete matched-coverage grid was frozen or persisted;
2. conformal false-known was near zero while known singleton rates were also
   extremely low, so unknown empty-set rejection must be separated from
   ambiguous-set abstention;
3. every n-gram temperature fit hit the frozen lower bound `T=0.05`;
4. class-conditional conformal validity may be sensitive to within-lineage
   dependence because calibration is record-based while role assignment is
   lineage-group-based.

M2.1 is not allowed to replace, overwrite, relabel or improve the M2 #1 primary
result.

## Parent evidence identity

The parent M2 result is bound to:

- primary workflow run id: `45370233451`;
- primary PR head:
  `eee3a48e31dde2cb61207a2165a822fc8ee3bf7c`;
- evidence archive SHA-256:
  `93c2cdb6c05919fb3ba348c948c73a836358da633352e566c243dd6c8a1e2352`;
- persisted `m2-results.json` SHA-256:
  `1fb39616725c90470e5dbc35ff7f4211190448e9bb1505c256d5febeba275dc3`;
- independent repeat run id: `45371006757`;
- independent repeat result: byte-identical.

Historical data identity remains unchanged:

- source SHA-256:
  `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- features SHA-256:
  `13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca`;
- selection-manifest SHA-256:
  `30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb`;
- source-contract SHA-256:
  `e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948`.

## Frozen non-negotiable carry-over

M2.1 may not change:

- the 500 selected Stage A records;
- unknown-family fold order;
- lineage key semantics;
- role assignment seed `20261124`;
- role fractions `35/15/30/10/10`;
- representation definitions;
- char hash dimension `262144`;
- word hash dimension `131072`;
- cosine-nearest-centroid scoring family;
- M2 conformal alpha `0.05`;
- M2 minimum-known-coverage policy `0.60`;
- the historical M2 result.

No seed search is allowed.

## Diagnostic A — conformal outcome decomposition

For every fold and representation, persist separate counts/rates for known and
unknown evaluation records.

### Known examples

Report:

- singleton accepted known class;
- singleton correct;
- singleton incorrect;
- empty prediction set;
- ambiguous prediction set;
- prediction-set coverage;
- set-size mean;
- set-size median;
- set-size maximum.

### Held-out unknown examples

Report separately:

- **empty-set rate**;
- **ambiguous-set rate**;
- **singleton false-known rate**;
- set-size mean;
- set-size median;
- set-size maximum.

Do not combine empty and ambiguous outcomes into a single OOD-rejection claim.

Interpretation:

- empty set may be described only as an operational empty conformal set;
- ambiguous set is abstention due to multiple admissible known classes;
- neither is proof that the source is genuinely unknown.

## Diagnostic B — selective-risk completion

M2 did not freeze a matched-coverage grid before execution. Therefore no new
coverage grid may be described as a primary M2 result.

M2.1 prospectively freezes the following **exploratory** targets:

```text
0.25, 0.50, 0.60, 0.75, 0.90, 1.00
```

For each target, use the first tie-preserving risk-coverage point whose achieved
coverage is greater than or equal to the target.

Persist:

- target coverage;
- achieved coverage;
- accepted records;
- errors among accepted;
- selective risk;
- confidence threshold corresponding to the accepted tie group.

Also report the operational risk at the already-frozen M2
threshold-development policy:

```text
minimum_known_coverage = 0.60
```

This threshold is fitted only on the M2 threshold-development role and then
applied unchanged to known evaluation records.

The operational-threshold result is a missing-output diagnostic from an
already-frozen policy, but remains reported under M2.1 rather than retroactively
inserted as an M2 primary result.

## Diagnostic C — score-scale / temperature-bound audit

Purpose: determine whether repeated n-gram `T=0.05` fits primarily reflect
the arbitrary scale of cosine similarity scores.

This is exploratory. It must not replace the frozen M2 temperature result.

For every fold and representation, report raw score diagnostics on:

- probability-calibration role;
- known evaluation role.

For each role report:

- score minimum/maximum;
- global mean and standard deviation;
- per-example top-1 score;
- top-1 minus top-2 margin;
- margin median and interquartile range.

### Frozen temperature sensitivity grid

Evaluate calibration-partition NLL on this fixed grid:

```text
0.005
0.010
0.020
0.050
0.100
0.200
0.500
1.000
2.000
5.000
10.000
20.000
50.000
100.000
200.000
```

Persist the full profile.

For diagnostic purposes only, identify the best grid temperature using the
**probability-calibration partition only**.

Then report held-out known-evaluation NLL/Brier at:

- `T=1`;
- the frozen M2 temperature;
- the M2.1 calibration-grid diagnostic temperature.

Because the held-out evaluation results are already exposed to the research
process, this comparison is exploratory and cannot be promoted to confirmatory
evidence.

No new temperature bound may be substituted into M2 #1.

## Diagnostic D — conformal effective sample structure

For every conformal-calibration class/fold report:

- calibration records;
- unique lineage groups;
- largest records-per-lineage group;
- median records-per-lineage group.

The current record-level conformal p-value calculation assumes the relevant
exchangeability conditions. M2.1 does not claim that lineage role separation
alone proves record-level exchangeability.

If substantial clustering is present, future sealed work should consider a
group-aware conformal design or a sampling unit aligned to the exchangeability
assumption.

## Cross-fold reporting

M2.1 must report every fold individually.

Allowed aggregate summaries:

- arithmetic mean;
- minimum/maximum;
- sign consistency;
- descriptive range.

Not allowed:

- pooled p-value;
- pooled confidence interval;
- claim of independent folds.

A pooled estimand requires a separate protocol.

## No representation tuning

M2.1 must not add:

- new 12D features;
- feature selection;
- neural networks;
- gradient boosting;
- new n-gram ranges;
- new hash dimensions;
- new classifier families;
- threshold optimisation on evaluation labels.

Any such work requires a separate future protocol and cannot be called M2.1.

## Expected interpretation outcomes

M2.1 is designed to answer diagnostic questions, not to produce a win.

Examples of admissible findings:

- near-zero conformal false-known is mostly ambiguity rather than empty-set
  rejection;
- temperature lower-bound hits are score-scale artifacts;
- wider temperature exploration still does not improve 12D held-out quality;
- selective risk remains poor even after abstention;
- apparent performance differences depend strongly on one unknown-family fold;
- effective conformal calibration sample size is smaller than record count
  suggests because of lineage clustering.

All are publishable diagnostic outcomes.

## Stop rule

After one exact M2.1 execution:

- do not change the grid;
- do not change coverage targets;
- do not change fold order;
- do not change outcome definitions;
- do not rerun with a different seed because a result is unattractive.

A code-correctness rerun is permitted only if the original run is explicitly
marked invalid and the defect is documented before replacement.

## Publication boundary

M2.1 must be labelled:

```text
POST_RESULT_EXPLORATORY
```

It may support failure analysis and Stage B protocol design.

It may not be cited as confirmatory evidence that CogniPrint identifies a
source model, detects AI origin, establishes authorship or provides reliable
OOD detection.
