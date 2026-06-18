# Inferential V1 Limitations Report

Status: pre-review limitations for inferential-v1 candidate outputs.
Readiness boundary: `descriptive_only`.

## Current limitations

- Local campaign axis counts remain small; most shared axes have only three local campaign rows.
- Public growth rows improve scale but are still corpus-bound and transformation-protocol-bound.
- Independent holdout rows are source-separation context and are not included in the primary permutation family.
- Feature-group ablation is deferred because the current comparison-row schema does not expose recomputed profile vectors after major feature-group removal.
- P-values are reported with effect sizes and confidence intervals; they are not standalone validation claims.
- External non-owner review is still required before any stronger readiness wording.

## Counts

- local campaign rows: 41
- public growth rows: 220
- independent holdout rows: 50
- minimum local axis count: 3

## Non-claims

CogniPrint is not an authorship system, provenance detector, legal tool, deterministic classifier, or final decision layer.
