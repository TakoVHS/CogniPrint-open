# CogniPrint — Independent Research Portfolio (reviewer edition, November 2026)

**Researcher:** Roman Adriashkin · Independent Researcher-Engineer · founder and project lead, CogniPrint Research Initiative  
**Research page:** https://cogniprint.org/roman-adriashkin/  
**ORCID:** https://orcid.org/0009-0009-6337-1806  
**Source:** https://github.com/TakoVHS/CogniPrint-open  
**Maturity:** `descriptive_only`; Stage B `NOT_AUTHORISED_TO_START`; independent methodological review not completed.  
**Purpose:** An inspectable entry point for reviewers. This is not a paper acceptance, employment application answer, or a claim of verified AI attribution.

## Research question

What can an AI system **justifiably claim** when a measurement, an inferred source signal, an external attestation, or a missing/conflicting record provide different levels and types of evidence?

A specific **unexecuted** extension asks whether evidence-gated AI audit reports reduce unsupported conclusions under missing, conflicting and out-of-distribution records without unacceptable loss of useful coverage. That is a falsifiable proposal, **not** a completed oversight result.

## Existing implemented artifacts and source links

| Component | Grounding | Scope |
| --- | --- | --- |
| Twelve-feature interpretable text profile | [`fingerprint.py`](../../src/cogniprint/fingerprint.py) | Reproducible statistical description; no source identity |
| Comparison and change analysis | [`analysis.py`](../../src/cogniprint/analysis.py) | Cosine, Euclidean, Manhattan, component differences; not a universal classifier |
| Typed evidence categories | [`evidence_policy.py`](../../src/cogniprint/evidence_policy.py) | `OBSERVED`, `INFERRED`, `ATTESTED`, `UNKNOWN`; **not an ordered lattice** |
| Claim Firewall | [`evaluate_claim`](../../src/cogniprint/evidence_policy.py) and [tests](../../tests/test_evidence_policy.py) | Conditional claim admission; policy does **not itself validate calibration** |
| Conflicting provenance | [`provenance_conflict.py`](../../src/cogniprint/provenance_conflict.py) | Preserve typed disagreements, not a universal logic proof |
| Case integrity | [current-state summary](../current-state-summary.md) | Deterministic manifests and SHA-256 checks; **not a digital signature** |

## An unfavorable result kept public

The fixed Stage A RAID pilot contains **500 records** in five classes, with a grouped **351 train / 149 test** split and reported zero cross-split lineage overlap.

| Method | Macro-F1 |
| --- | ---: |
| Word 1–2 hashed TF-IDF | **0.595220** |
| Character 3–5 hashed TF-IDF | 0.578782 |
| CogniPrint 12D nearest centroid | **0.535883** |
| Length-only | 0.247431 |

Both hashed n-gram baselines outperformed the custom 12D profile on this bounded pilot. This limits the supported scientific claim; it does not prove or disprove model attribution in general. [Exact protocol and numerical report](../raid-ngram-baselines-m1.md).

## Proposed next study (NOT EXECUTED)

Compare the same auditor under:
1. Ordinary audit instructions;
2. Natural-language evidence citation / abstention instructions;
3. Structured claim-to-evidence contexts and deterministic claim-admission gating.

Predefine unsupported-claim rate as a primary outcome; report supported-claim coverage, unknown/false-known outcomes, selective risk, reviewer agreement, cost and calibration only when numerical probabilities are available. A result that improves only through near-universal refusal does not support the proposed benefit.

[Auditable research proposal](evidence-gated-oversight-protocol-2026.md) · [Public claim register](claim-traceability-register-2026.md).

## Why reviewers may find this useful

The contribution is not a claimed breakthrough detector. It is a testable approach to limiting model-generated assertions, retaining negative evidence, designing reproducible experiments and resisting unjustified promotion from measurement to inference.

This research is independently led and developed with AI-assisted tools and collaborators as appropriate. It does not imply exclusive manual authorship of all code or sponsorship/affiliation by any AI laboratory. Confidential applicant information, interpreter details, health data, immigration matters and private repository contents are intentionally excluded.

## Evidence priority

**Inspect in this order:** [source](https://github.com/TakoVHS/CogniPrint-open) → [Claim Firewall tests](../../tests/test_evidence_policy.py) → [negative baseline report](../raid-ngram-baselines-m1.md) → [scientific readiness](../current-state-summary.md) → [proposed unexecuted experiment](evidence-gated-oversight-protocol-2026.md).
