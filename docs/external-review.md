# External methodological review request

CogniPrint is an MIT-licensed open research framework for reproducible statistical fingerprints of text and a research programme toward synthetic-language provenance.

## Current scientific boundary

- Scientific readiness: `descriptive_only`
- External methodological reviews: `0/1`
- Release line: `v0.1.2`
- The current release supports reproducible descriptive measurement.
- Model-family attribution, human–AI intervention mapping, and provenance fusion are research targets, not validated capabilities.
- No authorship, identity, exact-model, AI-origin, actor/commissioning, forensic, legal, psychological, or deterministic-source claims are made.

## What review is requested

A brief critical methodological review is sufficient. Endorsement is not requested.

Please evaluate the project as two clearly separated layers:

1. **Current evidence layer** — the implemented descriptive text-profile framework.
2. **Proposed research layer** — the benchmark protocol for testing stronger attribution/provenance hypotheses.

Useful review questions:

1. Are the current public claims appropriately bounded for a `descriptive_only` framework?
2. Are the feature definitions, corpus-relative comparisons, perturbation analyses, and uncertainty language scientifically clear enough?
3. Does `docs/model-fingerprint-benchmark-v0.1.md` separate closed-set attribution from open-world attribution strongly enough?
4. Are calibration, abstention, unseen-model tests, multilingual/domain shift, paraphrasing, translation, and human-edit robustness treated adequately?
5. Which conventional baselines or negative controls should be added before any model-family inference is considered?
6. Is the planned human–AI intervention track methodologically defensible, and what labels/controls would make it more informative?
7. Is the distinction between content-derived evidence and external provenance evidence (hashes, revision history, tool logs, signed credentials) stated strongly enough?
8. Is the reproducibility package sufficient for an independent researcher to inspect the current evidence and the planned benchmark protocol?
9. What result would convince you that the fingerprint hypothesis has failed or is too unstable to support attribution?

A response may be a short email, a GitHub issue comment, or a link to a separate review. A clear decline or referral to a more suitable reviewer is also useful.

## Reviewer entry points

Recommended reading order:

1. Grant/research summary: `docs/grant-one-pager.md`
2. Current state: `docs/current-state-summary.md`
3. Research vision: `docs/research-vision.md`
4. Model-fingerprint protocol: `docs/model-fingerprint-benchmark-v0.1.md`
5. Evidence dossier: `docs/evidence-dossier.md`
6. Manuscript source: `paper/main.tex`
7. Citation metadata: `CITATION.cff`
8. Reproduction commands: repository `README.md`

The reviewer does not need to approve the long-term vision. A useful review may conclude that one or more proposed layers are infeasible, underspecified, or likely to fail.

## Status rule

The repository must remain `descriptive_only` and `0/1` until a substantive response from a qualified external methodological reviewer is received and preserved as verifiable evidence. Automated acknowledgements, delivery receipts, generic encouragement, funding correspondence, or comments produced by the project owner do not count as methodological review.

A review is not an endorsement. If the reviewer identifies critical weaknesses, those weaknesses should be preserved and addressed publicly rather than converted into a positive status claim.
