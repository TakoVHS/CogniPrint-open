# Partial Identification / Decision Theory Literature Map

Status: **LITERATURE_BOUNDARY / NOVELTY_UNESTABLISHED**

Purpose: prevent CogniPrint from claiming novelty for identified sets, confidence
regions for partially identified parameters, or generic ambiguity-aware
decision rules.

## Classical boundary

### Manski (1990)

Charles F. Manski, *Nonparametric Bounds on Treatment Effects*, American
Economic Review 80(2):319–323.

Relevant contribution:
- partial identification through bounds when assumptions do not point-identify
  the target.

CogniPrint must not claim invention of interval/identified-set reasoning.

### Manski (2000)

Charles F. Manski, *Identification Problems and Decisions under Ambiguity:
Empirical Analysis of Treatment Response and Normative Analysis of Treatment
Choice*, Journal of Econometrics 95(2):415–442.

Relevant contribution:
- explicitly connects identification failure with decision ambiguity;
- distinguishes what available evidence and assumptions identify from how a
  decision-maker should act under remaining ambiguity.

This is very close to the philosophical bridge CogniPrint is using.

### Imbens & Manski (2004)

Guido W. Imbens and Charles F. Manski, *Confidence Intervals for Partially
Identified Parameters*, Econometrica 72(6):1845–1857.

Relevant contribution:
- finite-sample/asymptotic inference must be separated from the population
  identification region;
- confidence procedures for partially identified scalar parameters.

CogniPrint must not conflate an identified set with a confidence interval for
that set or for a point inside it.

### Romano & Shaikh (2008)

Joseph P. Romano and Azeem M. Shaikh, *Inference for Identifiable Parameters in
Partially Identified Econometric Models*, Journal of Statistical Planning and
Inference 138(9):2786–2807.

Relevant contribution:
- random confidence sets under partial identification;
- uniformity and inference over identified parameter sets.

### Stoye (2009)

Jörg Stoye, *More on Confidence Intervals for Partially Identified Parameters*,
Econometrica 77(4):1299–1315.

Relevant contribution:
- further clarifies confidence-region construction and nonuniformity issues
  around partially identified intervals.

### Gilboa & Schmeidler (1989)

Itzhak Gilboa and David Schmeidler, *Maxmin Expected Utility with Non-Unique
Prior*, Journal of Mathematical Economics 18(2):141–153.

Relevant contribution:
- classical maxmin decision-making under ambiguity represented by a set of
  priors.

CogniPrint should not call robust admissibility "maximin" unless an explicit
loss/utility model is stated.

## Current CogniPrint boundary

Already-classical ingredients:
- identified sets;
- partial identification;
- observational equivalence;
- Blackwell garbling / information comparison;
- minimax/maxmin ambiguity decisions;
- finite-sample confidence regions for partially identified targets;
- finite-sample selective-risk certificates.

Candidate CogniPrint contribution, still **UNESTABLISHED**:

> an auditable claim-admissibility calculus in which heterogeneous evidence
> channels induce claim-specific identified risk sets, claims are ordered by
> logical implication, and promotion is permitted only when the entire
> compatible risk set satisfies the declared tolerance.

Potentially nontrivial questions:
1. composition of heterogeneous certificates that target different losses and
   populations;
2. formal non-promotion rules between provenance, source-family, semantic, and
   mechanistic claims;
3. sharp identified risk sets under explicit channel-refinement assumptions;
4. conditions under which a new channel is claim-relevant rather than merely
   redundant;
5. prospective finite-sample procedures that combine identification
   uncertainty and sampling uncertainty without tuning on exposed evidence.

## Rejected shortcuts

Do not claim:
- a point estimate is necessarily inside the identified set;
- every point estimate underestimates worst-case risk;
- finite-sample confidence sets are the same object as population identified
  sets;
- a generic Hausdorff convergence rate yields a sample-size lower bound without
  a specified statistical model;
- statistical independence of two channels is equivalent to identification
  gain;
- adding an OOD score automatically makes an open-set claim identified.

## Working publication position

The manuscript should say:

> We do not claim novelty for identified sets or decision-making under partial
> identification. We study whether heterogeneous AI evidence channels support a
> useful claim-specific admissibility calculus, and we treat novelty of that
> calculus as an open question pending external mathematical review.
