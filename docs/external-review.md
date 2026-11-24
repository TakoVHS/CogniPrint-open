# External methodological review request

CogniPrint is an MIT-licensed open research framework for reproducible statistical fingerprints of text and evidence-bounded research on synthetic-language production.

## Current scientific boundary

- Scientific readiness: `descriptive_only`
- External methodological reviews: `0/1`
- Release line: `v0.1.2`
- Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`
- Hosted-runner infrastructure: functioning; historical issue #30 is closed
- Real RAID M1/M2 Stage A development evidence: executed
- Model-family attribution remains unvalidated
- No authorship, identity, exact-model, universal AI-origin, actor/commissioning, forensic, legal or deterministic-source claim is made

## Why review is requested now

The project now has an executed negative/mixed result rather than only a proposed protocol.

Historical M1 showed lexical baselines outperforming the compact 12D representation on the fixed closed-set comparison.

The first real pinned M2 on 24 November 2026 also did not produce a 12D win:

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D cosine centroid | 0.382981 | 1.348983 | 0.710081 | 0.511947 | 0.657500 |
| Character 3–5 hashed TF-IDF | 0.447966 | 1.241039 | 0.673324 | 0.338034 | **0.485000** |
| Word 1–2 hashed TF-IDF | **0.515231** | **1.234877** | **0.670327** | **0.303210** | 0.512500 |

The persisted M2 result was reproduced byte-for-byte in a separate external workflow run.

The project preserved the unfavorable result and did not change the seed, role fractions, alpha or baseline definitions after inspection.

## What review is requested

A brief critical methodological review is sufficient. Endorsement is not requested.

Please evaluate three layers separately:

1. **Descriptive core** — the implemented text-profile framework.
2. **Executed Stage A evidence** — M1/M2 development analyses and their interpretation.
3. **Future sealed research** — what, if anything, should be frozen before Challenge 001 Stage B.

Especially useful questions:

1. Are the current public claims appropriately bounded for `descriptive_only`?
2. Is the M2 five-role lineage-disjoint split defensible?
3. Is leave-one-machine-family-out useful development evidence despite all families being visible to the research programme?
4. Is cosine-centroid score → scalar-temperature probability mapping methodologically acceptable?
5. How should repeated n-gram temperature lower-bound hits be handled without post-result tuning?
6. Does worsening 12D held-out NLL after temperature scaling falsify the present calibration hypothesis adequately?
7. Are AURC and matched-coverage claims scoped correctly?
8. Is max-confidence false-known/AUROC sufficient to reject confidence thresholding as a useful OOD baseline here?
9. Should conformal unknown empty-set and ambiguous-set outcomes be separated before any OOD wording?
10. What cross-fold estimand/inference method, if any, is justified?
11. Does the evidence justify retaining 12D only as an interpretable diagnostic baseline?
12. What additional evidence is required before a genuinely sealed Stage B study is scientifically worthwhile?
13. Is the distinction between content-derived evidence and authenticated provenance strong enough?
14. What result would convince you the model-family fingerprint hypothesis should be abandoned?

A response may be a short email, a GitHub issue comment or a separate review.

## Reviewer entry points

Recommended reading order:

1. Reviewer M2 summary: `reviewer-bundle/m2-results.md`
2. Current status: `reviewer-bundle/current-status.md`
3. Methodology: `reviewer-bundle/methodology.md`
4. Limitations: `reviewer-bundle/limitations.md`
5. Reviewer questions: `reviewer-bundle/reviewer-questions.md`
6. Full M2 result: `docs/raid-m2-results-2026-11-24.md`
7. Machine-readable M2 summary: `evidence/raid-m2/2026-11-24/summary.json`
8. M2 protocol: `docs/raid-calibration-m2-development.md`
9. Current project state: `docs/current-state-summary.md`
10. Manuscript draft: `paper/when-not-to-attribute-protocol-draft.md`

The DOI should not be treated as independently verified until the corresponding public Zenodo record is directly checked.

## Review classification

Only a substantive independent methodological assessment from a qualified person/group may change the review counter from `0/1`.

Automated acknowledgements, delivery receipts, generic encouragement, funding correspondence or project-owner comments do not count.

A critical or negative review can count. Agreement is not required.

## Status rule

The repository remains `descriptive_only` regardless of whether the review is favorable.

Any stronger claim requires separate empirical evidence and a Scientific Claim Review.
