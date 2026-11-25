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

### Days 15–30 — finite-sample baseline + novelty separation

The first finite-sample baseline is now implemented:

- exact one-sided binomial upper confidence bound for a fixed threshold;
- Bonferroni simultaneous validity over a predeclared finite threshold grid;
- post-calibration threshold selection from that fixed grid;
- explicit refusal to replace pointwise calibration defect with ECE.

This is **not** a novelty claim. RCPS, Learn-then-Test, Conformal Risk Control,
Selective Conformal Risk Control, LEC (ICML 2026), and related work already
occupy finite-sample held-out risk-control territory.

The research task for this phase is therefore to identify a genuinely distinct
claim-admissibility result above the risk-control baseline.

Output: literature collision map + candidate theorem that is not a restatement
of existing selective-risk control.

### Days 31–45 — manuscript alpha

Write a 6–10 page mathematical manuscript.

Target structure:

1. Introduction
2. Related work
3. Formal setup
4. Known finite-sample risk-control baseline
5. Candidate claim-admissibility result
6. Counterexamples / impossibility
7. Synthetic verification
8. CogniPrint Stage A motivation
9. Limitations and novelty audit

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
