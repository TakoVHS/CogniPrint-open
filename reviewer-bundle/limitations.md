# CogniPrint Reviewer Bundle — Limitations

## Current status

CogniPrint is `descriptive_only`.

External methodological reviews remain `0/1`.

Challenge 001 Stage B remains `NOT_AUTHORISED_TO_START`.

The DOI reference `10.5281/zenodo.20756421` is not currently treated as directly verified through a public Zenodo record.

## Main limitations of the descriptive core

1. The framework depends on the selected feature family.
2. Stability claims are conditional on explicit assumptions.
3. Benchmark evidence is corpus- and protocol-specific.
4. No independent methodological review has been completed.
5. No independent external replication by another research group has been completed.
6. The current lightweight tokenisation/readability features are not validated as language-neutral measurements.
7. Similarity in the feature space is not evidence of common authorship, exact model identity or common provenance.

## Limitations exposed by M1/M2

1. The compact 12D representation did not outperform the tested lexical baselines on historical M1 macro-F1.
2. In M2, 12D also did not lead aggregate point estimates for macro-F1, NLL, Brier or AURC.
3. Per-fold 95% paired bootstrap intervals for 12D-vs-baseline NLL/Brier differences are wide and include zero; aggregate ordering is descriptive rather than a pooled inferential claim.
4. Scalar temperature scaling worsened held-out 12D NLL in all four M2 folds.
5. Both n-gram representations hit the lower temperature bound `T=0.05` in every fold, indicating unresolved score-scale/bound sensitivity.
6. Max-confidence open-set separation was weak; mean known-vs-unknown AUROC remained near chance-like values.
7. The conformal layer was extremely conservative: near-zero false-known singleton behavior coexisted with very low known singleton rates.
8. The current conformal summary combines unknown empty-set rejection and ambiguous-set abstention in a broad non-known/rejected category; this must be decomposed before strong OOD wording.
9. All source families used in M2 were development-visible to the research process; leave-one-family-out protects within-fold fitting but is not equivalent to a blind external unknown source.
10. The same Stage A corpus participates in multiple folds, so cross-fold dependence must be addressed before any pooled significance claim.
11. Model updates, prompt/domain changes, paraphrasing, translation, substantial human editing and new model families may invalidate observed relationships.
12. A useful outcome may be that the current 12D feature set remains an interpretable diagnostic baseline rather than an attribution representation.

## Limitations of human–AI intervention research

1. There is no current validated intervention-localisation output.
2. "Human intervention" is not a single naturally observable class; ground truth requires controlled revision history and an explicit operational definition.
3. Sentence/span boundaries may not correspond to the true production process.
4. Human editing can imitate, remove or introduce the same surface signals being measured.
5. A mixed-production label must not be converted into author identity, intent or responsibility.

## Provenance limitations

1. Content-derived measurements are not authenticated provenance.
2. Hashes establish integrity relative to a known artifact but do not identify its creator.
3. Signed credentials/logs can be absent, incomplete, compromised or limited to their explicit assertions.
4. Disagreement between content signals and declared provenance requires investigation; neither should be silently overwritten.
5. A person or organisation that requested, commissioned, approved or deployed a workflow cannot be inferred reliably from prose alone.

## Non-claims

CogniPrint does not currently establish:

- authorship or identity;
- a unique neural-model source;
- definitive AI origin;
- actor or commissioner identity;
- intent or responsibility;
- legal status;
- forensic provenance;
- universal classification;
- production readiness for high-stakes use;
- validated general accuracy.

## Reviewer request

Please identify any wording, empirical result or protocol step that remains stronger than the evidence supports.

Especially useful are explicit failure conditions and recommendations on whether the present 12D representation should remain only an interpretable development baseline.

## Required preservation

Until evidence justifies a change:

```text
Scientific readiness: descriptive_only
External methodological reviews: 0/1
Stage B: NOT_AUTHORISED_TO_START
```

Closing the review counter alone is not sufficient to change scientific readiness.
