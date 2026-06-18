# Public Benchmark v1 Results Summary

This file summarizes the current released benchmark subset as a public results layer for review and validation planning.

## Current released subset

The current benchmark release contains:

- `6` released baseline excerpts;
- `36` released controlled variants;
- `3` released languages;
- `3` released source classes;
- `6` released perturbation axes.

Each baseline currently contributes six controlled variants, giving the benchmark layer a balanced first release shape rather than a single uneven pool of examples.

## What the current subset is useful for

The present subset is useful for:

- public review of baseline-versus-variant provenance structure;
- validation-layer development;
- benchmark-versus-campaign bridge summaries;
- early review of perturbation-family coverage;
- manuscript planning around what is already public and auditable.

## Current coverage shape

The released baselines span:

- public-domain literary prose;
- public-domain political prose;
- public-domain government text.

The released languages are currently:

- `en`
- `es`
- `fr`

The released perturbation families currently include:

- punctuation cleanup;
- controlled compression;
- sentence split and merge;
- word-order shift;
- formalized style;
- informalized style.

## Interpretation

The current benchmark layer is large enough to support a first benchmark-linked validation pass and a first benchmark-versus-campaign bridge, but it is still small.

It should be read as:

- a released benchmark subset;
- a public provenance and coverage layer;
- a support layer for descriptive validation;
- not yet a broad benchmark for stronger generalization claims.

## Main limitation

The benchmark subset is still too small for broader benchmark-level conclusions on its own.

In particular, the current layer remains limited by:

- small baseline count;
- limited source-domain diversity;
- limited language diversity;
- controlled-variant coverage that is still narrow relative to the next validation goals.

## Next step

The next benchmark step should expand this public layer toward a `v1.1` release with:

- `20` to `50` public baselines;
- `100` to `300` controlled variants;
- broader multilingual coverage;
- clearer domain-level comparisons.

## Guardrail

This benchmark results summary describes released coverage and current practical usefulness. It does not claim benchmark performance, proof, certainty, or broad statistical generalization.
