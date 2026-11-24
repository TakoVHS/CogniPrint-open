# CogniPrint Reviewer Bundle — Current Status

## Public release state

```text
Release: v0.1.2
DOI reference: 10.5281/zenodo.20756421 (pending direct public verification)
Repository: https://github.com/TakoVHS/CogniPrint-open
Scientific readiness: descriptive_only
External methodological reviews: 0/1
```

The public release remains a descriptive measurement framework. No source-attribution feature has been unlocked.

## Execution state

The historical hosted-runner blocker is resolved.

Fresh minimal canary evidence on 24 November 2026:

- workflow: `Runner Canary Current`;
- run id: `45371785458`;
- conclusion: `success`;
- log contains `RUNNER_EXECUTED`;
- log contains `PYTHON_EXECUTED`;
- issue #30 is closed as completed.

Current research CI also executes successfully on hosted runners, including Stage A Methods, RAID M2 Development, RAID Pilot Adapter and Public Release CI.

This resolves an infrastructure gate only. It does not change scientific readiness.

## Review state

No external methodological review has been completed. The counter remains `0/1`.

Prepared outreach, automated acknowledgements, funding correspondence, AI-generated responses and generic encouragement do not count as methodological review evidence.

## Executed Stage A RAID evidence

Historical M1 remains a fixed negative comparison for the compact 12D representation:

- CogniPrint 12D macro-F1: `0.535883`;
- character 3–5 hashed TF-IDF: `0.578782`;
- word 1–2 hashed TF-IDF: `0.595220`.

The first real pinned M2 calibration/abstention study also completed on 24 November 2026.

M2 status:

```text
EXECUTED / DEVELOPMENT_ONLY / PRE-FREEZE
Stage B: NOT_AUTHORISED_TO_START
```

Aggregate four-fold point estimates:

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D cosine centroid | 0.382981 | 1.348983 | 0.710081 | 0.511947 | 0.657500 |
| Character 3–5 hashed TF-IDF | 0.447966 | 1.241039 | 0.673324 | 0.338034 | **0.485000** |
| Word 1–2 hashed TF-IDF | **0.515231** | **1.234877** | **0.670327** | **0.303210** | 0.512500 |

The result is negative/mixed rather than a 12D win.

The first external run and a later independent repeat produced byte-identical persisted `m2-results.json` content.

Full reviewer entry point: `reviewer-bundle/m2-results.md`.

## Implemented trust architecture

The repository contains:

- `cogniprint-evidence-v1` with `OBSERVED / INFERRED / ATTESTED / UNKNOWN`;
- Claim Firewall v1 with attribution disabled until explicit evidence/calibration/OOD gates are satisfied;
- machine-readable limitation codes;
- provenance-conflict handling;
- deterministic `.cogcase` integrity/manifest primitives;
- Data Constitution and benchmark governance;
- calibration/OOD/holdout evaluation contracts;
- independent sealed-prediction evaluation architecture;
- C2PA, Article 50 and NIST AI RMF mapping documents with explicit non-certification boundaries.

These are research/evidence controls, not validation that source attribution works.

## Scientific interpretation after M2

The executed evidence currently supports **claim narrowing and abstention**, not stronger attribution.

Important negative findings:

- current 12D does not lead the tested aggregate M2 metrics;
- scalar temperature scaling worsened held-out 12D NLL in all four folds;
- max-confidence open-set separation remained weak;
- conformal false-known values were near zero only in an extremely conservative regime with very low known singleton rates.

No exact-model, AI-origin, authorship, actor/commissioner, intent, legal or forensic claim follows.

## What may change scientific status

The external-review counter may change only after a substantive independent methodological assessment from a qualified person/group is received and preserved with an appropriate permission boundary.

Scientific readiness may change only after dedicated empirical evidence, calibration/open-world evaluation, reproducibility evidence and review justify a stronger claim.

Closing issue #30 or completing M2 does not by itself change `descriptive_only`.

## Current next milestones

1. Obtain one real external methodological critique against the executed M1/M2 evidence.
2. Freeze a post-result diagnostic protocol before any temperature-bound/score-scale sensitivity analysis.
3. Keep any M2.1 analysis explicitly exploratory and separate from the frozen M2 result.
4. Complete the remaining Challenge 001 pre-freeze choices and external preregistration before any sealed Stage B work.
5. Preserve the `descriptive_only` boundary unless a separate Scientific Claim Review supports a change.
6. Resolve or replace the still-unverified Zenodo DOI reference.
7. Keep unrelated C2PA/signature/QVAC/Auto Drive tracks on their existing evidence gates.

