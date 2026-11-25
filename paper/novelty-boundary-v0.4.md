# Novelty Boundary v0.4 — Post-Adversarial-Review

Status: **CURRENT / NO PRIORITY CLAIM / SIGNIFICANCE UNRESOLVED / SUBMISSION HOLD**

This file supersedes `paper/novelty-boundary-v0.3.md`.

## Directly acknowledged prior art

CogniPrint does not claim novelty for:

- compatible-world / identified-set semantics or sharp extrema;
- partial-identification confidence reasoning;
- finite-sample risk-control procedures;
- separation of a risk target from a statistical failure probability;
- multiple high-confidence constraints or family-wise calibration;
- conformal risk control;
- abstention / reject options;
- fail-closed "no solution" behavior;
- union-bound confidence accounting;
- probabilistic assume/guarantee structure;
- transportability as a research problem;
- assurance-case evidence/claim structures;
- proxy-evidence fibers, target-relative no-promotion, sharp envelopes,
  audit/refinement, or counterworlds.

Directly relevant ML-native references now include:

- Bates et al. (2021), Distribution-Free Risk-Controlling Prediction Sets;
- Angelopoulos et al. (2025), Learn Then Test;
- Angelopoulos et al. (2024), Conformal Risk Control;
- Thomas et al. (2019), Seldonian algorithms;
- El-Yaniv and Wiener (2010), selective classification.

Zhu (2026) remains direct prior art for compatible-world / target-envelope /
counterworld reasoning.

## Corrected mathematical status

The old phrase "pointwise least monotone numerical warrant" was underspecified
because the sharp envelope was partial while the comparison class was
full-domain.

The current formulation defines a feasible-domain warrant
(h:\mathcal B_T\to[0,1]), proves that the sharp envelope belongs to that
class, and then proves pointwise minimality.

This is correct but elementary. It is supporting mathematics, not a novelty
claim.

The explicit empty-compatible-set branch is now described as a
specification/inconsistency diagnostic and implementation safeguard. It is not
presented as an additional source of frequentist soundness.

## Surviving candidate contribution

The only candidate contribution currently defended is an ML-facing audit
organization that requires the following objects to be recorded separately
before a statistical guarantee is promoted to a deployment claim:

1. certified loss/target;
2. certificate validity population/world class;
3. downstream claim loss/target;
4. deployment population/world class;
5. risk tolerance;
6. statistical failure budget;
7. any warrant/transport argument connecting targets or populations;
8. realized model/bound feasibility;
9. a certified claim-risk upper bound.

This is a **possibly useful organization**, not a historical-priority claim.

## Significance gate

Correctness alone is not sufficient.

Before TMLR submission, the paper still needs at least one of:

- a real-data certificate-to-claim instantiation in which the audit changes or
  blocks a non-obvious decision;
- a substantive new theorem beyond the elementary envelope/union-bound facts;
- a testable or sensitivity-bounded treatment of transport/scope mismatch;
- or a human reviewer assessment that the methodology/application synthesis is
  itself sufficiently useful for the venue.

## Stage A relationship

M1/M2/M2.1 are development evidence and negative/failure-analysis context.

They do not empirically validate the formal audit.

The current 12D representation does not outperform the tested lexical
baselines on the reported Stage A aggregate point estimates; M2 probability
quality is only modestly better than an uninformative four-class probability
vector, and max-confidence OOD ranking is near chance.

## Stage B

Current 12D-centered Challenge 001 remains:

**HOLD / NOT_AUTHORISED_TO_START / REDESIGN REQUIRED BEFORE ANY FUTURE AUTHORIZATION**

The AI red-team recommendation to abandon the current design is treated as a
serious input, not as a substitute for independent human methodological review.

## Submission

**CLOSED.**

Human review gate remains `0/1`.
