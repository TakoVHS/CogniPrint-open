# Evidence-Bounded Inference — Paper and Research Programme

Status: **PLANNING / THEORY_DRAFT / NOT_SUBMITTED**

## Working title

**Evidence-Bounded Inference: Calibration, Abstention, and the Limits of
Claim Admissibility**

Alternative subtitle:

**From Confidence Scores to Auditable Risk Certificates**

## Core thesis

The paper should not claim that CogniPrint invents calibration, selective
classification, conformal prediction, or OOD detection.

The research programme asks a narrower question:

> What mathematical certificate, if any, is sufficient to move from a model
> score to a bounded claim while preserving an explicit UNKNOWN outcome?

## Paper 1 scope

Paper 1 should be short and proof-centered.

1. Motivation from the negative/mixed CogniPrint Stage A result.
2. Formal definitions:
   - coverage;
   - selective risk;
   - false-known risk;
   - uniform top-label calibration defect;
   - certified correctness lower bound.
3. Theorem 1:
   \\(R_{\mathrm{sel}}(g_\tau)\le1-\tau+\epsilon\\).
4. Target-risk threshold corollary:
   \\(\tau\ge1-\delta+\epsilon\\).
5. Coverage proposition:
   \\(C(g_\tau)\ge(m-\tau)/(1-\tau)\\) when positive.
6. Open-world impossibility theorem:
   arbitrary unknown distributions can force false-known risk to one on any
   non-empty acceptance region.
7. Conformal singleton theorem:
   marginal validity gives \\(R_{\mathrm{sel}}\le\alpha/\kappa\\),
   not \\(\alpha\\).
8. Synthetic finite-space checks.
9. Existing M2/M2.1 used as motivation and descriptive evidence only.
10. Limitations and external mathematical review.

## Explicit non-claims

The manuscript must not say:

- ECE estimates the theorem's uniform calibration defect;
- confidence alone solves OOD detection;
- conformal singleton acceptance has selective risk at most alpha;
- M2.1 established a successful OOD detector;
- the current theory is novel until the literature review supports that;
- Stage B has started or has been preregistered.

## 90-day programme

### Days 1–14 — formal foundations

- complete definitions and proofs;
- add counterexamples for rejected draft claims;
- obtain at least one independent mathematical critique;
- map theorem assumptions to selective-classification and conformal literature.

Output: theory note v0.2.

### Days 15–30 — finite-sample statistics

Study how to replace the unknown population quantity epsilon with an
independent-sample confidence bound. Candidate tools:

- binomial confidence bounds on accepted risk;
- DKW-style uniform empirical-process bounds where applicable;
- calibration confidence bands;
- risk-controlling prediction-set / selective-classification results.

Output: theorem or proposition with an explicit finite-sample confidence level.

### Days 31–45 — manuscript alpha

Write a 6–10 page mathematical manuscript.

Target structure:

1. Introduction
2. Related work
3. Formal setup
4. Main results
5. Counterexamples / impossibility
6. Synthetic verification
7. CogniPrint Stage A motivation
8. Limitations

Output: private PDF alpha.

### Days 46–60 — external critique

Send the mathematical note to a small number of researchers in calibration,
selective prediction, or conformal inference. Ask for criticism of assumptions
and novelty, not endorsement.

Output: written criticism/disposition log.

### Days 61–75 — prospective empirical design

Only after the theory is stable, design a new sealed empirical test.
Do not tune on the exposed 500 Stage A records.

Output: prospective empirical protocol.

### Days 76–90 — public preprint candidate

Release only if:

- theorem statements survive review;
- proofs are independently checked;
- novelty claims are supported by literature review;
- all empirical sections distinguish exploratory, descriptive, and sealed
  evidence.

Possible surfaces: institutional repository / Zenodo / arXiv when appropriate.
A DOI or arXiv identifier is not itself evidence of scientific validity.

## Scientific identity

A coherent long-run identity for this programme is:

**Evidence-Bounded Statistical Inference**

with the recurring principle:

> Probability is not permission to claim.

Recognition should be treated as a consequence of useful mathematics,
reproducible evidence, and external uptake—not as a metric to optimize directly.
