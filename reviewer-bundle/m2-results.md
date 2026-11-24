# CogniPrint Reviewer Bundle — RAID M2 Result

## Status

- Scientific readiness: `descriptive_only`
- M2 status: `EXECUTED / DEVELOPMENT_ONLY / PRE-FREEZE`
- Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`
- External methodological reviews: `0/1`

This page summarises the first real pinned RAID M2 development result for independent methodological review. It is not an attribution claim.

## Evidence identity

Primary external run:

- workflow: `RAID M2 External Pinned Evidence`;
- run id: `45370233451`;
- run number: `#1`;
- PR head: `eee3a48e31dde2cb61207a2165a822fc8ee3bf7c`;
- evidence archive SHA-256:
  `93c2cdb6c05919fb3ba348c948c73a836358da633352e566c243dd6c8a1e2352`.

Historical Stage A identity gates:

- source size: `801662741`;
- source SHA-256:
  `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- features SHA-256:
  `13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca`;
- selection manifest SHA-256:
  `30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb`;
- source contract SHA-256:
  `e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948`;
- selected records: `500`.

A separate external repeat, run `45371006757` (#4), produced a byte-identical persisted `m2-results.json`:

`1fb39616725c90470e5dbc35ff7f4211190448e9bb1505c256d5febeba275dc3`

## Four-fold aggregate result

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D cosine centroid | 0.382981 | 1.348983 | 0.710081 | 0.511947 | 0.657500 |
| Character 3–5 hashed TF-IDF | 0.447966 | 1.241039 | 0.673324 | 0.338034 | **0.485000** |
| Word 1–2 hashed TF-IDF | **0.515231** | **1.234877** | **0.670327** | **0.303210** | 0.512500 |

Lower is better for NLL, Brier, AURC and false-known rate.

The current 12D representation does not lead the tested representations on the aggregate point estimates. This is a negative/mixed result.

All predeclared per-fold 95% lineage-group bootstrap intervals for 12D-vs-baseline NLL and Brier differences include zero. The aggregate ordering must not be converted into a pooled significance claim without a separately specified cross-fold estimand.

## Temperature finding

For 12D, the frozen temperature procedure worsened held-out probability quality:

- mean NLL: `1.277792 -> 1.348983`;
- mean Brier: `0.692123 -> 0.710081`;
- NLL worsened in all four folds.

For both n-gram representations, all fitted temperatures hit the lower bound `T=0.05`. Their held-out NLL/Brier improved, but the repeated boundary hit creates a score-scale/bound-sensitivity question that must be studied prospectively rather than retuned after seeing this result.

## Open-set finding

The max-confidence baseline remained weak:

- mean false-known:
  - 12D: `0.6575`;
  - char: `0.4850`;
  - word: `0.5125`;
- mean known-vs-unknown AUROC:
  - 12D: approximately `0.5117`;
  - char: approximately `0.5398`;
  - word: approximately `0.5329`.

This does not support maximum calibrated class probability as reliable OOD evidence.

## Conformal finding

Mean conformal false-known rates were near zero, but known singleton rates were also very low:

- 12D singleton rate: approximately `0.6%`;
- char singleton rate: approximately `2.8%`;
- word singleton rate: approximately `6.1%`.

The correct interpretation is a highly conservative prediction-set regime, not strong practical OOD detection.

## Reviewer questions

Please focus especially on these questions:

1. Is the five-role lineage-disjoint design adequate for development calibration?
2. Is leave-one-machine-family-out a useful Stage A open-set diagnostic despite all families being development-visible to the research process?
3. Is converting cosine-centroid score vectors through scalar temperature scaling defensible, or should the score-to-probability map be reformulated prospectively?
4. How should repeated `T=0.05` boundary hits be handled without post-result tuning?
5. Is AURC being interpreted narrowly enough given differences in full-coverage error?
6. What is the correct cross-fold estimand, if any, for inferential comparison when the same Stage A corpus participates in multiple leave-one-family-out folds?
7. Should the conformal report separate unknown empty-set rejection from unknown ambiguous-set abstention before any OOD wording is used?
8. Does the negative/mixed result justify keeping the current 12D representation only as an interpretable diagnostic baseline rather than an attribution feature set?
9. What evidence would be required before authorising a genuinely sealed Stage B study?

A negative review is useful. Endorsement is not requested.

## Full records

- protocol: `docs/raid-calibration-m2-development.md`;
- result: `docs/raid-m2-results-2026-11-24.md`;
- machine-readable summary: `evidence/raid-m2/2026-11-24/summary.json`;
- manuscript draft: `paper/when-not-to-attribute-protocol-draft.md`.

## Claim boundary

This result does not establish authorship, exact model identity, universal AI origin, actor/commissioner identity, intent, legal/forensic provenance or production readiness.
