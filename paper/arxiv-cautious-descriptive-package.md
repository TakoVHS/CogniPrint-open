# arXiv Cautious Descriptive Preprint Package

Status: package scaffold for a cautious descriptive preprint, not a final submission.

## Canonical Manuscript Posture

The preprint should present CogniPrint as a mathematical framework and a working empirical evidence package supporting a follow-up manuscript. It should not present the project as a completed empirical study, an authorship attribution system, or a forensic decision workflow.

## Required Package Files

- `paper/main.tex` for the formal mathematical manuscript source;
- `paper/references.bib` for bibliography;
- `paper/arxiv-abstract.txt` for submission metadata;
- `paper/submission-metadata.md` for author/category values;
- `paper/submission-checklist.md` for final manual checks;
- `paper/empirical-stability-v1.md` as the manuscript-facing empirical stability draft.

## Evidence Attachments to Cite

- `evidence/empirical-v1/`
- `evidence/empirical-growth-v1/`
- `evidence/independent-holdout-v1/`
- `evidence/public-benchmark-v1/`
- `evidence/public-benchmark-v1.1/`
- `validation/wave005-descriptive-validation/`
- `validation/statistical-validation-v1.2/`
- `validation/conventional-stylometry-baseline-v1/`
- `docs/statistical-readiness-status.json`

## Current Empirical Status

- empirical campaigns: `5`
- local empirical campaign rows: `41`
- public controlled empirical growth rows: `220`
- independent holdout rows: `50`
- combined readiness row count: `311`
- public benchmark v1 subset: `6` baselines / `36` variants
- public benchmark v1.1 layer: `20` baselines / `120` variants
- validation v1.2 correction tests: `6`
- conventional stylometry baseline: character n-gram TF cosine distance
- readiness decision: `descriptive_only`

## Required Guardrails

Before submission:

- keep all empirical wording descriptive;
- state that public controlled growth improves row count but is not an independent holdout corpus;
- state that independent holdout validation is English-only and descriptive;
- state that validation v1.2 does not remove the independent-validation limitation;
- state that corrected p-values are diagnostic until scale gates pass;
- include the conventional stylometry baseline as a comparison surface, not as a superiority claim;
- do not claim proof, source certainty, definitive attribution, or forensic determination.

## Open Work Before Submission

- final edit pass over `paper/main.tex` to decide whether the empirical stability layer belongs in the main text or supplementary note;
- final PDF build with `make paper-build`;
- final claims scan;
- final metadata review against arXiv category and endorsement requirements;
- independent external reviewer feedback recorded through `docs/external-review/status.json`.
