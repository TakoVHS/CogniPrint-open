# Finite-Sample Composition Prior-Art Map

Status: **LITERATURE_BOUNDARY / NOVELTY_UNESTABLISHED**

## Verified references

### Imbens & Manski (2004)

*Confidence Intervals for Partially Identified Parameters*, Econometrica
72(6):1845–1857.

What it establishes:
- distinguishes population identification regions from sampling uncertainty;
- constructs confidence intervals for a scalar partially identified parameter;
- highlights nonuniform coverage issues as the width of the identification
  region changes.

Boundary for CogniPrint:
- confidence inference over a partially identified target is not new;
- a population identified set must not be called a finite-sample confidence
  set.

### Chernozhukov, Hong & Tamer (2007)

*Estimation and Confidence Regions for Parameter Sets in Econometric Models*,
Econometrica 75(5):1243–1284.

What it establishes:
- a general estimation/inference framework for identified parameter sets;
- population identified sets represented as minimizers of a criterion;
- sample-criterion inversion, consistency, convergence rates, and confidence
  regions.

Boundary for CogniPrint:
- we do not attribute a generic additive
  `epsilon_mu + epsilon_K` kernel-neighborhood theorem to CHT;
- our fixed product-gate CP certificate is a much simpler special-purpose
  construction, not a replacement for CHT.

### Romano & Shaikh (2008)

*Inference for Identifiable Parameters in Partially Identified Econometric
Models*, Journal of Statistical Planning and Inference 138(9):2786–2807.

What it establishes:
- confidence regions for points/functions associated with a partially
  identified model;
- uniformity considerations and computational procedures.

Boundary for CogniPrint:
- generic confidence-region machinery under partial identification is prior
  art.

### Kaido & Santos (2014)

*Asymptotically Efficient Estimation of Models Defined by Convex Moment
Inequalities*, Econometrica.

What it establishes:
- efficient estimation for convex moment-inequality identified sets;
- support-function representation;
- root-n regular estimation under their structural conditions;
- consistent bootstrap for the limiting distribution.

Boundary for CogniPrint:
- there is no universal slow conditional-kernel rate such as `n^{-1/4}`;
  rates depend on the model class and regularity conditions.

## Additional collision risk

### Data combination / data fusion

Modern partial-identification work explicitly studies how heterogeneous data
sources and additional restrictions sharpen identified sets. Examples include
data-combination models and recent partial-identification data-fusion work.

This materially weakens any broad novelty claim of the form:

> "combining heterogeneous evidence channels shrinks an identified set."

That phenomenon is established territory.

### Machine-learned proxies

Recent work also studies partial identification when machine-learned proxies
link a downstream sample and an auxiliary validation sample.

This is particularly close to CogniPrint's proposed use of model-produced
evidence as a linking variable and should be treated as a novelty-collision
risk.

## What remains potentially distinctive

The current candidate contribution is narrower:

1. define claim-specific risk targets for AI provenance/source assertions;
2. represent each evidence channel by the world restrictions its observed law
   imposes;
3. require robust claim admissibility over the entire compatible-world set;
4. characterize population promotion exactly as elimination of every
   claim-unsafe world by the added channel's observed conditional behavior;
5. expose when a statistically valid certificate is about the wrong target and
   therefore cannot authorize promotion.

This remains **UNESTABLISHED** as a novelty claim.

## Finite-sample position

For a fixed product gate, CogniPrint now uses a deliberately simple baseline:

- one-sided exact Clopper--Pearson lower bound on known acceptance;
- one-sided exact upper bound on unknown acceptance;
- external deployment prevalence bound `pi <= pi_upper`;
- monotonic worst-case propagation through Bayes' formula;
- Bonferroni extension to a frozen finite family of gates.

This is an application/baseline, not a new general confidence-set theory.

## Rejected claims from the proposed finite-sample draft

Do not state:

- `epsilon_mu = max CP_upper(p_b)` as a confidence radius;
- `epsilon_K = max CP_upper(q_b)` as a kernel-error radius;
- that outer worst-case risk is non-monotone in epsilon;
- that an internal optimum epsilon follows from set stabilization;
- a universal `n^{-1/4}` rate for arbitrary conditional-kernel estimation;
- that the finite-sample risk upper bound must converge to zero;
- that Dinkelbach or Charnes--Cooper is required for the scalar fixed-gate
  posterior-risk problem.
