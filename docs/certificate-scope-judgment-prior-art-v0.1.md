# Certificate Scope Judgment — Prior-Art Check v0.1

Status: **NOVELTY FALSIFICATION / HIGH COLLISION RISK**

## 1. Belief Hoare Logic

Kawamoto, Sato, and Suenaga develop Belief Hoare Logic for formally describing
requirements of statistical inference and reasoning about statistical beliefs
obtained through hypothesis testing.

Relevant collision:

- explicit statistical preconditions;
- formal postconditions and beliefs;
- soundness and relative completeness;
- rules for multiple hypothesis tests;
- discussion of justification inside and outside the program logic.

**Consequence:** Gap 1 is not novel in any broad sense of formal
typing or soundness for statistical inference.

The narrower unresolved distinction is that Certificate Scope Judgment treats
an already-produced certificate as carrying a target risk functional,
population scope, evidence scope, and confidence budget, and asks whether it may
be promoted to a semantically distinct downstream claim.

## 2. StatWhy

StatWhy requires statistical programs to be annotated with requirements and
interpretations of statistical methods. It automatically checks whether those
requirements have been specified, including assumptions about an unknown true
population that cannot themselves be mechanically established.

**Consequence:** Any claim that CogniPrint is the first framework to attach
assumptions or population requirements to statistical inference and verify
their use is false.

## 3. Assurance 2.0

Assurance 2.0 separates evidence incorporation from the reasoning step that
justifies a higher-level claim, and represents side claims, assumptions,
defeaters, and residual doubt. Its statistical-testing examples explicitly
separate a factual test result from the argument that the result supports a
reliability claim.

**Consequence:** The generic statement that statistical evidence needs an
explicit warrant before supporting a stronger semantic claim is prior art.

Potential remaining distinction: a warrant whose premises and conclusion are
typed by statistical target functionals, deployment scopes, and confidence
budgets, with partial-identification counterworlds used as rejection witnesses.

## 4. SACM and Isabelle/SACM

SACM provides formal vocabulary for claims, evidence, argument relationships,
and evidence interpretation/evaluation. The specification does not equate
representation with correctness.

Isabelle/SACM gives a machine-checked assurance language that integrates
heterogeneous formal and informal evidence with explicit inferential links.

**Consequence:** machine-checkable heterogeneous evidence-to-claim structure is
prior art.

## 5. Probabilistic programming and modular inference

Typed probabilistic programming gives formal semantics to probabilistic
programs, distributions, and inference transformations. Work by Staton and by
Scibior and collaborators provides typed and measure-theoretic foundations for
probabilistic programming and formally justified modular Bayesian inference.

**Consequence:** no broad novelty claim is available for a probabilistic or
statistical type system as such.

The searched material does not directly match the proposed downstream
certificate-to-semantic-claim scope judgement.

## 6. Confidence composition

Combining confidence distributions and confidence procedures is established
statistics.

For two same-target upper-confidence certificates, the generic safe rule is

\[
\rho(D)\le\min(B_1,B_2)
\]

on the intersection of their validity events, with failure budget bounded by

\[
\alpha_1+\alpha_2.
\]

There is no generic strict-improvement result and no universal
\(O(n^{-1/2})\) gain from merely having two evidence channels.

**Consequence:** the proposed rate theorem in Gap 3 is rejected.

## 7. Gap status after review

### Gap 1 — Typed Certificate Algebra

Status: **HEAVY COLLISION / NARROW CANDIDATE REMAINS**

Not novel:

- statistical preconditions and postconditions;
- program-logic soundness;
- machine-checked statistical assumptions;
- generic evidence-to-claim warrants.

Potentially distinct:

- explicit target-functional, population, evidence-scope, and confidence-budget
  type carried by a certificate;
- forbidden cross-target upcasts unless a separate warrant is supplied.

### Gap 2 — Non-Promotion Witness

Status: **USEFUL FORMAL DEVICE / NOVELTY UNESTABLISHED**

The existence equivalence is elementary and overlaps countermodel,
partial-identification, and robust-optimization reasoning.

Potentially distinct:

- a standardized partial-identification counterworld emitted specifically as a
  rejection witness when an otherwise valid statistical certificate is being
  used for the wrong downstream claim.

### Gap 3 — Confidence-Budget-Preserving Composition

Status: **PROPOSED RATE THEOREM REJECTED**

Valid baseline:

- union-bound confidence budget;
- same-target bound intersection;
- explicit warrant for heterogeneous targets.

Potentially distinct:

- type-safe confidence bookkeeping across different certified target
  functionals and a downstream semantic claim.

## 8. Current strongest candidate

The strongest surviving research object is the Certificate Scope Judgment

\[
\kappa_1,\dots,\kappa_m\vdash_T c
\]

with:

- statistical target typing;
- population/domain typing;
- evidence-scope typing;
- confidence-budget accounting;
- explicit semantic or statistical warrant;
- counterworld rejection witness.

Novelty remains **UNESTABLISHED**.
