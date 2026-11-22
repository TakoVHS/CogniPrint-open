# Evidence-gated oversight under incomplete or conflicting evidence

**Status:** PROPOSED RESEARCH PROTOCOL — no experimental result for this transfer hypothesis is claimed.  
**Date:** 2026-11-05  
**Owner:** Roman Adriashkin, independent researcher-engineer, CogniPrint Research Initiative  
**Scientific readiness:** `descriptive_only` for CogniPrint source-family claims; this oversight study has **not been executed**.  
**Relationship to Challenge 001:** This is a separate research direction; it does **not** authorize Stage B, change the freeze, unlock attribution, or supersede `docs/trust.md`.

## Motivation and question

The question is **not** "can CogniPrint detect AI text?" It is:

> Can evidence-gated reporting reduce unsupported conclusions by AI auditing agents when evidence is incomplete, contradictory, or out of distribution, without an unacceptable reduction in useful coverage?

CogniPrint is a testbed for the narrower engineering problem of deciding **which claims the available evidence permits**. Generalization to AI-agent oversight remains a hypothesis, not a demonstrated result.

## Existing mechanisms — what is implemented

1. **Interpretable measurements.** `src/cogniprint/fingerprint.py` implements a fixed-order twelve-coordinate text profile; `src/cogniprint/analysis.py` implements cosine, Euclidean, Manhattan and componentwise difference comparison. Fixed-bound normalization is **not clipped** to [0,1].
2. **Evidence taxonomy.** `src/cogniprint/evidence_policy.py:19-23` defines `OBSERVED`, `INFERRED`, `ATTESTED`, `UNKNOWN`. These are **evidence categories**, not a mathematically implemented lattice or truth ranking. An observation is not inherently stronger than a validated attestation.
3. **Claim admissibility.** `EvidenceContext` includes evidence strength, minimum evidence, in-distribution check, calibration flag, explicit attribution unlock, attestation validation, limitations. `evaluate_claim(kind, context)` returns a `ClaimDecision` with `allowed`, `evidence_class`, `maximum_level`, `safe_statement`, `limitations`, and policy version. Its strongest supported statement is conditioned on a specified evidence state; the policy **does not itself measure or certify calibration**.
4. **High-stakes restrictions.** Claims of authorship, actor/commissioner, intent/responsibility, and legal/forensic provenance are disallowed as content-only conclusions, including in a context that contains a validated external attestation.
5. **Conflict handling.** `src/cogniprint/provenance_conflict.py` compares an authorized inferred label with a validated attested label. When the normalized labels disagree it retains both records and emits `PROVENANCE_CONFLICT`. This is a **typed label-comparison rule**, **not** a general theorem prover or formal satisfiability test.
6. **Integrity.** The `.cogcase` prototype supports deterministic manifests and SHA-256 integrity checks; a cryptographic signature is not implemented. C2PA runtime validation is not implemented.

### A descriptive policy abstraction (not a proved theorem)

Let `K` denote implemented claim kinds, `Γ` the `EvidenceContext` fields and `D` a structured `ClaimDecision`. The code implements a deterministic policy of the form:

`F: K × Γ → D`

This is a **documentation abstraction** of `evaluate_claim`, not a claim about probabilistic calibration or logical completeness. `UNKNOWN` is an outcome for unsupported inferences, not a blanket prohibition on accurate direct measurements.

## Existing negative empirical result

The fixed RAID Stage A pilot selected **500** records across **five** classes and **four** domains, reused a grouped lineage-safe split of **351 train / 149 test**, with zero train-test lineage overlap in the recorded run.

| Baseline | Macro-F1 |
| --- | ---: |
| Length-only nearest centroid | 0.247431 |
| CogniPrint 12D nearest centroid | 0.535883 |
| Character 3–5 hashed TF-IDF | 0.578782 |
| Word 1–2 hashed TF-IDF | **0.595220** |

**Interpretation:** compact interpretable 12D features did **not** outperform simple text n-gram baselines in this bounded descriptive pilot. This is not an independent sealed test or general attribution result; all scores are uncalibrated. See `docs/raid-ngram-baselines-m1.md`.

## Proposed falsifiable hypothesis

A monitoring layer that requires typed, traceable claim-evidence links and provides scoped abstention **will lower the proportion of unsupported audit conclusions** relative to a comparable baseline auditor, **at comparable useful coverage**, on controlled, independently reviewed cases with missing, contradictory and OOD evidence.

The hypothesis fails if the reduction is absent, statistically uncertain, or obtained only by refusing nearly every answer; research must report both error and coverage.

## Proposed experimental plan — NOT EXECUTED

**Data and ground truth.** Construct or select authorized multi-step agent audit scenarios with independently verified ground-truth event traces. Include complete records, missing events, contradictory statements, stale/invalid attestations, withheld source identities, injected irrelevant logs, and held-out tool/domain families. Avoid including secrets, private documents, or harmful actionable content. Use scenario-lineage grouping to prevent train/test leakage.

**Arms on the same cases:**
- B0: baseline audit assistant with ordinary task instructions.
- B1: baseline plus a natural-language "cite evidence and say unknown" instruction.
- B2: the same underlying assistant with structured evidence fields, explicit provenance validation flags, a deterministic claim-admission layer, and structured `UNKNOWN`/limitation outputs.

**Primary outcome:** unsupported conclusion rate, defined and adjudicated by independent reviewers on the preselected claim taxonomy; report denominator explicitly.

**Secondary outcomes:** useful supported-claim coverage, correctness/precision-recall on answerable cases, abstention and false-known rates on unanswerable or held-out cases, calibration error (ECE/Brier **only if** calibrated probabilities are actually produced), selective risk vs coverage, reviewer agreement, latency and token/compute overhead.

**Pre-registration and protections:** freeze claim taxonomy, scenario generation, splits, annotation rubric, prompts, thresholds, model versions, metrics, exclusion criteria, and negative-result policy before blinded evaluation. No prediction tuning after label reveal. Keep independent evaluator separate from generation pipeline; hash artifacts and preserve error cases.

**Minimum acceptable evidence of progress:** a completed preregistered protocol, reproduced run logs, agreed review rubric, transparent baseline comparisons, independent audit of failure cases, and bounded conclusions. Numeric target thresholds must be chosen using separate development evidence and frozen before the blind run; none are asserted today.

## Research significance and limitations

This direction connects to **Scalable Oversight, AI Control and Safeguards Research** by testing whether claim-evidence accountability improves the accuracy of AI-generated audit reports. It does not establish agent monitoring guarantees, solve alignment, or imply endorsement by any model provider or research organization.

## Source-of-truth links

- [Claim Firewall implementation](https://github.com/TakoVHS/CogniPrint-open/blob/main/src/cogniprint/evidence_policy.py)
- [Claim Firewall tests](https://github.com/TakoVHS/CogniPrint-open/blob/main/tests/test_evidence_policy.py)
- [Conflict engine](https://github.com/TakoVHS/CogniPrint-open/blob/main/src/cogniprint/provenance_conflict.py)
- [Feature map](https://github.com/TakoVHS/CogniPrint-open/blob/main/src/cogniprint/fingerprint.py)
- [Fixed Stage A baseline report](https://github.com/TakoVHS/CogniPrint-open/blob/main/docs/raid-ngram-baselines-m1.md)
- [Trust contract](https://github.com/TakoVHS/CogniPrint-open/blob/main/docs/trust.md)
- [Current state and open gates](https://github.com/TakoVHS/CogniPrint-open/blob/main/docs/current-state-summary.md)

**Research attribution:** independent work directed by Roman Adriashkin; public code and documents may also involve collaborators and AI-assisted engineering. No claim of sole authorship for every line of code, peer review, or external validation is made.
