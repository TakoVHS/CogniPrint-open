# Certificate-to-Claim Target Typing — Candidate Formal Object

Status: **CANDIDATE / NOT A THEOREM / NOVELTY UNESTABLISHED**

This note records the only novelty candidate surviving the 2026-11-24 deep
audit. It is intentionally separated from the proved/standard components.

## 1. Motivation

A certificate can be statistically valid while being evidence for the wrong
claim.

Examples:

- a closed-set class-error certificate is used to imply known-vs-unknown
  membership;
- a calibrated probability is used to imply provenance;
- a watermark-integrity record is used to imply truth of the recorded content;
- a benchmark result is used to imply performance on an unrepresented
  deployment population.

The failure is not necessarily bad calibration. It is **target mismatch**.

## 2. Typed certificate

Working schema:

[
kappa
=
(E,mathcal W,ho,B,alpha,mathsf{Assumptions}).
]

Interpretation:

- (E): evidence available to the procedure;
- (mathcal W): worlds/populations covered by the certificate;
- (ho): exact certified risk functional;
- (B): certified bound;
- (alpha): failure probability;
- assumptions: exchangeability, transport, frozen gate, prevalence envelope,
  etc.

## 3. Typed claim

Working schema:

[
c
=
(C,mathcal W_c,ho_c,delta_c).
]

The semantic proposition (C) and the error functional (ho_c) are not
assumed to equal the target of the certificate.

## 4. Promotion obligation

A certificate may support the claim only if an explicit warrant (T) proves
that, over the claim world class,

[
ho(D)le B
quadLongrightarrowquad
ho_c(D)ledelta_c.
]

The warrant may come from:
- logical implication between claim events;
- an identification result;
- a transport theorem;
- a validated auxiliary evidence channel;
- a mechanistic provenance record.

Without such a warrant, target mismatch blocks promotion.

## 5. Non-promotion witness

A machine-checkable failure object is a world (D^star) satisfying all
certificate premises but violating the claim tolerance:

[
D^starmodelsmathsf{Assumptions}(kappa),
qquad
ho(D^star)le B,
qquad
ho_c(D^star)>delta_c.
]

Its existence proves that the certificate alone does not entail the claim.

## 6. Research questions

1. Is this exactly an existing notion in statistical decision theory,
   formal assurance, or program/proof logic under a different name?
2. What is the weakest useful notion of warrant (T)?
3. Can claim implication and evidence refinement be composed without
   conflating semantic and statistical strength?
4. Can finite-sample certificates preserve their error accounting through
   such composition?
5. Can a non-promotion witness be generated automatically from a finite or
   convex world-class specification?

No theorem or novelty claim should be made until these are checked externally.
