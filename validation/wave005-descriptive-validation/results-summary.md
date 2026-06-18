# Wave-005 Descriptive Validation Results Summary

The current validation layer summarizes `41` empirical comparison rows and `120` released benchmark variants.

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
- cross-baseline pairs per draw: `120`
- pooled random baseline mean Euclidean distance: `8.341167`
- draw-mean Euclidean reference interval: `8.120563` to `8.556909`

## Threshold sensitivity note

- current Euclidean grid campaign counts: low=`12`, moderate=`13`, larger=`16`
- current Euclidean grid benchmark counts: low=`34`, moderate=`32`, larger=`54`
- current cosine grid campaign counts: low=`24`, moderate=`5`, larger=`12`
- current cosine grid benchmark counts: low=`77`, moderate=`12`, larger=`31`

## Benchmark-versus-campaign bridge

- shared axes reviewed in the bridge: `6`
- closest Euclidean alignment across shared axes: `punctuation_cleanup` with delta `0.409183` and band `close`
- widest Euclidean gap across shared axes: `sentence_split_merge` with delta `15.919378` and band `wider`

These values should be read as descriptive stability tendencies and perturbation-effect summaries rather than definitive inferential results.
