# Empirical Growth v1 Methods

Rows are generated from released public benchmark v1.1 baselines.
The first part reuses released public benchmark variants. The second part applies deterministic text transforms in memory and stores only metrics, hashes, and provenance.

Additional transform axes:

- `token_pair_swap`
- `token_stride_drop`
- `token_stride_duplicate`
- `sentence_order_rotate`
- `punctuation_strip`

All comparisons use the existing CogniPrint profile extraction and profile comparison functions.
