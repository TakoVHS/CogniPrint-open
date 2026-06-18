# Statistical Validation v1.1 Methods Summary

This package aggregates campaign-level comparison rows and benchmark-subset comparison rows into an expanded descriptive validation layer.

## Inputs

- empirical campaigns reviewed: `5`
- empirical comparison rows reviewed: `41`
- public benchmark baselines reviewed: `9`
- public benchmark variants reviewed: `54`

## Implemented summaries

- bootstrap percentile intervals for mean metric values;
- per-axis descriptive summaries for campaign rows and benchmark rows;
- within-campaign and between-campaign variance summaries;
- Hedges' g comparisons against the light-edit reference axis;
- repeatable multi-draw cross-baseline random reference distributions from released benchmark variants;
- threshold-sensitivity summaries across cosine, Euclidean, and Manhattan metric families;
- benchmark-versus-campaign bridge summaries for overlapping perturbation axes with alignment bands.

No statistical significance claims are made in this layer.
