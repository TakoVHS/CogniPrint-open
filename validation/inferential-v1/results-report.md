# Inferential V1 Results Report

Status: pre-review inferential candidate outputs.
Readiness boundary: `descriptive_only`.

These results execute the frozen local-campaign versus public-growth contrast family. They do not satisfy the external-review gate and do not upgrade CogniPrint readiness.

## Primary contrasts

- `compressed_version`: n=3/20, mean delta=-4.56155, reported p=0.2238, Holm=0.975, Cliff's delta=-0.466667, median delta=-3.011392
- `formalized_style`: n=3/20, mean delta=-0.621452, reported p=0.3476, Holm=1.0, Cliff's delta=-0.266667, median delta=-0.915161
- `informalized_style`: n=3/20, mean delta=-4.566107, reported p=0.354, Holm=1.0, Cliff's delta=-0.266667, median delta=-0.632548
- `punctuation_cleanup`: n=3/20, mean delta=-0.409183, reported p=0.9838, Holm=1.0, Cliff's delta=0.166667, median delta=5.062953
- `sentence_split_merge`: n=3/20, mean delta=-15.919378, reported p=0.0592, Holm=0.3552, Cliff's delta=-0.833333, median delta=-10.760512
- `word_order_shift`: n=3/20, mean delta=-8.744299, reported p=0.195, Holm=0.975, Cliff's delta=-0.366667, median delta=-6.693934

## Sensitivity

Sensitivity rows rerun the same contrast family for `cosine_similarity` and `manhattan_distance`. They are diagnostic only and should be read alongside group sizes and limitations.

- sensitivity rows: 12

## Boundary

Do not use these outputs to claim author identification, text provenance determination, legal conclusion, deterministic classification, or universal performance.
