# CogniPrint Reviewer Bundle — Executive Summary

## Purpose

CogniPrint is an open research framework for constructing compact, interpretable statistical profiles of text and studying profile similarity, perturbation stability, uncertainty and evidence admissibility.

The current public release remains a **descriptive measurement framework**. The research programme asks whether the same reproducible foundation can support bounded model-family studies, abstention, human–AI intervention research and provenance fusion.

The purpose of this reviewer bundle is to support a real external methodological review of the implemented framework **and the executed negative/mixed Stage A evidence**, not to seek endorsement.

## Current public baseline

- Release: `v0.1.2`
- DOI reference: `10.5281/zenodo.20756421` — pending direct public Zenodo verification
- Repository: `https://github.com/TakoVHS/CogniPrint-open`
- Scientific readiness: `descriptive_only`
- External methodological reviews: `0/1`
- Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`

## What CogniPrint currently claims

CogniPrint claims only a descriptive research status.

It defines:

- a versioned statistical text-profile framework;
- comparison and perturbation diagnostics;
- evidence/claim separation;
- reproducibility and integrity artifacts;
- development-only evaluation infrastructure for calibration, abstention and open-set failure.

It is not presented as a validated attribution system.

## Executed model-family development evidence

The historical RAID M1 comparison showed that the tested lexical baselines outperformed the compact 12D representation on the fixed closed-set task.

The first real pinned RAID M2 run completed on 24 November 2026 with exact source/features/selection/source-contract hash gates and an independently repeated byte-identical result payload.

Aggregate M2 point estimates:

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D cosine centroid | 0.382981 | 1.348983 | 0.710081 | 0.511947 | 0.657500 |
| Character 3–5 hashed TF-IDF | 0.447966 | 1.241039 | 0.673324 | 0.338034 | **0.485000** |
| Word 1–2 hashed TF-IDF | **0.515231** | **1.234877** | **0.670327** | **0.303210** | 0.512500 |

The result is negative/mixed:

- 12D does not lead the aggregate tested metrics;
- all predeclared per-fold 95% proper-score bootstrap intervals for 12D-vs-baseline differences include zero;
- temperature scaling worsened held-out 12D NLL in all four folds;
- max-confidence OOD ranking was weak;
- conformal prediction was extremely conservative and rarely emitted singleton known-class claims.

This evidence strengthens the case for **abstention and claim narrowing**, not stronger attribution.

## Research programme under review

The next-stage programme remains falsifiable:

1. **Calibration/abstention diagnostics:** determine whether score scaling, probability mapping and rejection rules can be improved without post-result tuning.
2. **Sealed Stage B design:** only after freeze/preregistration, test genuinely held-out source families and transformations.
3. **Human–AI intervention mapping:** test whether controlled revision chains support bounded localisation claims.
4. **Provenance fusion:** keep content-derived measurements separate from authenticated hashes, signed credentials, revision history and workflow records.

None of those items is a current validated product claim.

## What CogniPrint does not claim

CogniPrint does not currently establish:

- authorship or identity;
- a unique/exact source model;
- definitive AI origin;
- actor/commissioner identity;
- intent or responsibility;
- legal or forensic provenance;
- universal classification accuracy;
- production readiness for high-stakes decisions.

## Reviewer request

A reviewer is asked to evaluate:

- whether the current descriptive core is responsibly bounded;
- whether the executed M1/M2 analyses are methodologically defensible;
- whether the negative/mixed interpretation is appropriately conservative;
- whether the proposed follow-up work avoids post-result tuning;
- what evidence would be required before any sealed Stage B attribution study is justified.

Endorsement is not requested. A negative assessment is useful evidence.

## Entry points

- Reviewer M2 summary: `reviewer-bundle/m2-results.md`
- Executed result: `docs/raid-m2-results-2026-11-24.md`
- Machine-readable result: `evidence/raid-m2/2026-11-24/summary.json`
- M2 protocol: `docs/raid-calibration-m2-development.md`
- Current state: `docs/current-state-summary.md`
- External-review request: `docs/external-review.md`
- Manuscript draft: `paper/when-not-to-attribute-protocol-draft.md`

The DOI should be added to reviewer-facing citation instructions only after the public Zenodo record is directly verified.
