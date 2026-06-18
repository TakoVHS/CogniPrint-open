# Independent Holdout v1 Methods

The holdout uses short Project Gutenberg excerpts stored under `datasets/independent-holdout-v1/raw/` with source metadata in `datasets/independent-holdout-v1/metadata/sources.csv`.

For each excerpt, five deterministic transforms are applied in memory. Generated variant texts are not published; only hashes and comparison metrics are stored.

Comparison metrics use the same CogniPrint profile extraction and comparison functions as the rest of the evidence package.
