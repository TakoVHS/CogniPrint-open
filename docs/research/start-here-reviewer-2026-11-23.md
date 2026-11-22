# CogniPrint — start here (independent research review)

**Research lead:** Roman Adriashkin — independent researcher-engineer, founder and project lead, CogniPrint Research Initiative  
**ORCID identifier stated in project metadata:** [0009-0009-6337-1806](https://orcid.org/0009-0009-6337-1806)  
**Repository:** [TakoVHS/CogniPrint-open](https://github.com/TakoVHS/CogniPrint-open)  
**Evidence snapshot:** 2026-11-23; this guide is documentation in a **Draft PR**, not a released scientific result.  
**Scientific readiness:** `descriptive_only`; Attribution Challenge 001 remains `PRE-FREEZE`, Stage B `NOT_AUTHORISED_TO_START`, independent methodological review `0/1`.

## The one-minute research question

**Which assertions may an AI analysis system legitimately make from measurements, statistical inference and authenticated external records — and when should it answer UNKNOWN?**

CogniPrint presently offers reproducible descriptive statistics and an explicit claim-admission policy. Its long-term source-family and generation-lineage proposals remain research hypotheses, not validated AI detectors.

## What has actually been implemented

- **Measurement:** [fixed-order 12-feature map](../../src/cogniprint/fingerprint.py), profile geometry, entropy and controlled perturbation diagnostics. A "fingerprint" is a statistical vector, **not** a unique identifier.
- **Claim policy:** [typed evidence and `evaluate_claim`](../../src/cogniprint/evidence_policy.py), tested in [evidence-policy tests](../../tests/test_evidence_policy.py). Evidence categories are `OBSERVED`, `INFERRED`, `ATTESTED`, `UNKNOWN`; they are not a proved mathematical lattice.
- **Evidence integrity:** deterministic case manifests and SHA-256 consistency checks. **Cryptographic signatures and C2PA runtime validation are not established capabilities.**
- **Research governance:** [trust contract](../trust.md), [current status](../current-state-summary.md), [failure charter](../where-cogniprint-fails.md).

`evaluate_claim` checks explicitly supplied evidence-context flags. It does **not** independently establish the correctness of those flags, statistical calibration, source identity or forensic truth.

## Recorded Stage A result — unfavorable baseline, retained

Five-class fixed RAID Pilot A: **500 selected records**; **351 train / 149 test**; reported train/test lineage overlap **0** under the fixed grouped split.

| Comparator | Macro-F1 on fixed Pilot A test split |
| --- | ---: |
| Length-only nearest centroid | 0.247431 |
| CogniPrint 12D nearest centroid | **0.535883** |
| Character 3–5 hashed TF-IDF | 0.578782 |
| Word 1–2 hashed TF-IDF | **0.595220** |

The strongest tested n-gram baseline exceeded 12D by **0.059337 macro-F1 points**. These are **historical reported Stage A development results**, not a rerun during this review and not blinded Challenge 001 Stage B evidence. Read the [protocol, pinned hashes and limitations](../raid-ngram-baselines-m1.md).

## Engineering execution is not scientific validation

For Draft [PR #80](https://github.com/TakoVHS/CogniPrint-open/pull/80), commit `126a1b3e0984330cab134784293f6b2c69bde9ad`, [Public Release CI run #179](https://github.com/TakoVHS/CogniPrint-open/actions/runs/41968850843) reports successful completed jobs on **Python 3.10, 3.11, 3.12**. Retrieved job-step summaries show checkout, installation, release gate tests, tracked-tree scan and sanitized export steps executed successfully.

**Scope limitation:** this is evidence for that *specific public-release CI workflow and commit*. It is not proof of a complete full-suite run, independent rerunning of the 801 MB RAID experiment, a successful sealed evaluation, statistical significance, or external review. In the currently published `main`, `make test` targets `tests/test_public_release_export.py` rather than the full test directory. Existing historical `NOT_EXECUTED` runner incidents must not be silently rewritten as successful runs.

## Two separate next research studies

1. **Attribution Challenge 001** — [protocol](../attribution-challenge-001.md): test whether interpretable signals add family-level information beyond lexical baselines, under lineage-safe splits, OOD and abstention. **NOT EXECUTED at Stage B.** Do not use Stage A-exposed RAID/public benchmarks as sealed test data.
2. **Evidence-gated oversight** — [proposal](evidence-gated-oversight-protocol-2026.md): compare an ungated auditor, a prompt-only caution baseline and a structured claim-policy gate on independently labelled audit tasks. Measure **unsupported-claim rate at matched useful coverage**. **NOT EXECUTED.** It cannot inherit validation from the RAID classifier comparison.

## Research integrity and publication gates

1. Preserve a clean, exact-revision source snapshot, reproducibility manifest, Python versions, dependency versions, runnable commands and actual logs for the **complete relevant test suite**.
2. Produce an independently rerunnable RAID Stage A package within dataset redistribution and privacy limits; document access to the pinned external source and what cannot be redistributed.
3. Freeze hypothesis, strata, sample-size rationale, exclusions, baselines, metric definitions, calibration and abstention decisions *before* blind Stage B. Keep train/test lineage and exposure audits independent.
4. Register the frozen protocol externally; seal fresh Stage B material; freeze predictions and hashes before revealing labels; publish all relevant failure cases.
5. Request substantive **non-owner** methodological review. Do not claim peer review, endorsements, formal academic affiliations, or scientific feature unlocks until evidence actually exists.
6. Verify any DOI by reading the intended public record and matching its title, authors, version and content. The DOI currently listed in a Draft PR is **not verified by this audit**.

## How to evaluate this project in 10 minutes

1. [Code and fixed feature definitions](../../src/cogniprint/fingerprint.py) + [Claim Firewall tests](../../tests/test_evidence_policy.py).
2. [Negative Stage A comparison](../raid-ngram-baselines-m1.md), including source and split hashes.
3. [Mathematics manuscript source](../../paper/main.tex). It is a *working manuscript*, not evidence of peer-reviewed publication; stability statements are conditional on stated assumptions.
4. [Current readiness / blocked gates](../current-state-summary.md).
5. [Researcher portfolio](reviewer-portfolio-2026.md) + [claim-to-code traceability](claim-traceability-register-2026.md).
6. [Independent reviewer response template](../reviewer-response-template.md).

## Approved professional description

> **Roman Adriashkin** is an independent researcher-engineer and founder/project lead of the CogniPrint Research Initiative. His work focuses on reproducible statistical text measurements, evidence-bounded conclusions, and evaluating how AI systems should handle missing or conflicting evidence. CogniPrint is MIT-licensed research software with a published descriptive Stage A pilot; validated source attribution, sealed blind Stage B results, and independent methodological review remain outstanding.

**Author-contribution boundary:** the research and software involve AI-assisted engineering tools and collaborators where relevant; this description does not claim exclusive manual authorship of every commit. No PhD degree, university appointment, accepted paper, laboratory affiliation, or sponsor endorsement is implied.

## Website and release coordination

[PR #77](https://github.com/TakoVHS/CogniPrint-open/pull/77) and [PR #79](https://github.com/TakoVHS/CogniPrint-open/pull/79) contain **alternative draft website directions**. Their content must be reconciled rather than merged in bulk. Preview, mobile/accessibility checks and explicit owner approval are required before changing `cogniprint.org`. This review guide is safe to inspect separately; it does not authorize a site release or a scientific status change.
