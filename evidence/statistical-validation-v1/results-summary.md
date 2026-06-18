# Statistical Validation v1.1 Results Summary

The current validation layer summarizes `41` empirical comparison rows and `54` released benchmark variants.

## Overall metric summaries

- mean cosine similarity: `0.990429`
- mean Euclidean distance: `2.610789`
- mean Manhattan distance: `3.444352`

## Axis-level observed pattern

- largest mean Euclidean shift in current campaign rows: `expanded_version` at `4.681358`
- smallest mean Euclidean shift in current campaign rows: `minor_lexical_substitution` at `0.144192`
- overlapping benchmark axes reviewed: `6`

## Variance note

- between-campaign variance of mean Euclidean distance: `1.27235`
- light-edit reference rows available for effect-size comparison: `7`

## Random baseline reference

- repeatable random baseline draws: `64`
- cross-baseline pairs per draw: `54`
- pooled random baseline mean Euclidean distance: `9.375026`
- draw-mean Euclidean reference interval: `8.991032` to `9.75524`

## Threshold sensitivity note

- current Euclidean grid campaign counts: low=`12`, moderate=`13`, larger=`16`
- current Euclidean grid benchmark counts: low=`12`, moderate=`12`, larger=`30`
- current cosine grid campaign counts: low=`24`, moderate=`5`, larger=`12`
- current cosine grid benchmark counts: low=`34`, moderate=`6`, larger=`14`

## Benchmark-versus-campaign bridge

- shared axes reviewed in the bridge: `6`
- closest Euclidean alignment across shared axes: `formalized_style` with delta `0.871914` and band `close`
- widest Euclidean gap across shared axes: `sentence_split_merge` with delta `14.944827` and band `wider`

These values should be read as descriptive stability tendencies and perturbation-effect summaries rather than definitive inferential results.
