# Public Benchmark v1 Methods Summary

This file records the release method for the current public benchmark subset.

## Current release method

- choose candidate sources with stable public URLs and clear reuse status;
- release short baseline excerpts rather than full imported works;
- derive controlled variants locally from each released baseline excerpt;
- document every released row in `datasets/public-benchmark-v1/metadata/samples.csv`;
- keep benchmark analysis and statistical validation out of scope for this subset release.

## Current subset profile

- `6` released baseline excerpts;
- `36` released controlled variants;
- English-language, Spanish-language, and French-language release;
- perturbation axes released in this subset:
  - punctuation cleanup;
  - controlled compression;
  - sentence split and merge;
  - word-order shift;
  - formalized style;
  - informalized style.
