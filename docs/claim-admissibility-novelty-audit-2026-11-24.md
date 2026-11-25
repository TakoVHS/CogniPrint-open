> **LEGACY FORMAT WARNING — 25 November 2026.**
> This historical novelty-audit file contains Markdown/LaTeX escape corruption
> introduced during an earlier tool-to-tool transfer. Its prose conclusions are
> preserved for audit history, but damaged formulas must not be cited or reused
> as canonical mathematics. Current mathematical statements live in
> `docs/feasible-domain-claim-envelope-v0.2.md` and the current manuscript.
> This file is the only temporary exception in the repository-wide Markdown
> math integrity guard; the exception should be removed only after a
> source-grounded manual restoration.

# Novelty Audit — Claim Admissibility, Partial Identification, and Evidence Composition

Date: 2026-11-24  
Status: **DEEP NOVELTY AUDIT / NOVELTY UNESTABLISHED / EXTERNAL REVIEW REQUIRED**

Scope:
- claim-specific unsafe-world elimination;
- partial identification and decision theory;
- heterogeneous data fusion;
- Blackwell / Le Cam comparison of experiments;
- constrained decision rules;
- assurance-case claim/evidence formalisms.

This document is deliberately adversarial. Its purpose is to remove novelty
claims that collapse to established theory before submission.

## 1. Executive verdict

### Not novel as standalone mathematical contributions

The following ingredients are established or reduce immediately to established
objects:

1. observational equivalence implies non-identification;
2. identified sets / partial identification;
3. worst-case decision criteria over a compatible set of worlds;
4. robust admissibility written as
   `sup_D risk(D) <= delta`;
5. the equivalent statement that every compatible world lies in a
   risk-safe set;
6. adding joint restrictions/evidence can shrink an identified set;
7. deterministic post-processing cannot add Blackwell information;
8. comparison of experiments by decision risk / deficiency;
9. finite-sample confidence regions for partially identified sets;
10. structured claim -> subclaim -> evidence assurance arguments;
11. eliminative reasoning that accepts a top claim only after relevant
    defeaters are resolved.

The current manuscript must not present any of these generic statements as the
main novelty.

## 2. Collision map

### A. Partial identification — very high overlap

Classical and modern partial-identification work already separates:
- population identification;
- sampling uncertainty;
- decisions when the payoff-relevant state is only partially identified.

Manski's identification program and later decision-theory work explicitly ask
what decisions can be justified when the observable distribution does not
point-identify the relevant state. Modern treatment-choice papers study
minimax, minimax-regret, and robust-Bayes rules under partial identification.

**Consequence for CogniPrint**

The criterion

[
sup_{Dinmathcal W_{m obs}}ho_C(D)ledelta
]

is a robust-feasibility / worst-case decision condition, not a new decision
principle.

### B. Breakdown frontiers — high overlap

Masten--Poirier-style breakdown-frontier analysis studies the boundary between
assumption values for which a conclusion holds and those for which it fails,
with inference for that boundary.

**Consequence**

A broad claim that CogniPrint newly formalizes "which extra assumptions make a
claim defensible" would collide with existing robustness / breakdown-frontier
work.

### C. Data fusion and auxiliary data — very high overlap

Heterogeneous data sources are already used to sharpen identified sets.
Recent work includes:
- partial-identification data fusion for causal effects;
- data combination with machine-learned proxies and auxiliary validation data.

**Consequence**

The generic statement

> an additional evidence source/channel can shrink the compatible-world set

is established territory.

### D. Blackwell / Le Cam — very high overlap

Blackwell comparison asks whether one experiment is at least as informative as
another across decision problems. Le Cam deficiency quantifies the loss between
experiments. Torgersen's treatment also allows comparisons relative to
restricted classes of decision problems.

A 2026 paper, *Beyond Blackwell: Constrained Data Processing Inequalities*,
goes further: it studies constrained/admissible decision-rule classes and
defines constrained deficiency / a constrained randomization theorem.

**Consequence**

CogniPrint should not claim novelty for:
- information monotonicity under garbling;
- deterministic-channel redundancy;
- "informativeness relative to admissible decisions" in the abstract.

### E. Assurance cases — high conceptual overlap

Safety/security assurance cases already organize:
- top-level claims;
- subclaims;
- evidence;
- contexts and assumptions;
- confidence arguments.

Assurance 2.0 explicitly supports defeaters and eliminative argumentation:
systematically investigate reasons why a top claim could be false, and record
whether those defeaters are resolved.

**Consequence**

A generic "claim hierarchy + evidence + eliminate counterarguments" framework
is not novel.

## 3. The population unsafe-world criterion is a corollary, not a novelty theorem

For

[
mathcal W_{m obs}
=
{D:	ext{observed evidence constraints hold}}
]

and

[
mathcal S_{C,delta}
=
{D:ho_C(D)ledelta},
]

robust claim admissibility is

[
mathcal W_{m obs}subseteqmathcal S_{C,delta}.
]

Equivalently,

[
mathcal W_{m obs}cap
mathcal U_{C,delta}
=
arnothing,
qquad
mathcal U_{C,delta}
=
{D:ho_C(D)>delta}.
]

This equivalence is mathematically useful but definition-level. Calling it a
new "unsafe-world elimination theorem" would overstate the contribution.

Likewise, the conditional-kernel representation

[
mathcal W_{E,F}
=
{Dinmathcal W_E:K_D(Fmid E)=K_{m obs}(Fmid E)}
]

is a disintegration-based representation of the observed joint law. It should
be presented as a proposition/representation, not as the central novelty
claim.

## 4. Candidate gap that remains alive

The deepest search so far has **not** found a standard formalism matching all
of the following in one object:

1. a statistical certificate explicitly carries its
   - evidence sigma-field/channel,
   - target functional/loss,
   - calibration/validation population,
   - deployment/world-class assumptions,
   - confidence statement;
2. a proposed downstream claim carries a distinct
   - semantic truth condition,
   - target population,
   - tolerated risk,
   - claim strength / logical implication relation;
3. a formal judgement decides whether the certificate is permitted to support
   that claim;
4. if the certificate target and claim target differ, promotion is blocked
   unless an explicit identification/transport implication is supplied;
5. non-promotion produces an auditable witness/counterworld rather than merely
   a lower confidence score.

Call this, provisionally:

**certificate-to-claim target typing**.

This phrase is a working label, not a novelty claim.

## 5. Candidate formal object

Represent a statistical certificate as

[
kappa
=
(E,mathcal W_kappa,ho_kappa,B_kappa,alpha_kappa),
]

where:
- (E) is the observed evidence channel;
- (mathcal W_kappa) is the world/population class over which the certificate
  is valid;
- (ho_kappa) is the exact risk/target certified;
- (B_kappa) is the certified upper bound;
- (alpha_kappa) is its error probability.

Represent a downstream claim specification as

[
c
=
(C,mathcal W_c,ho_c,delta_c),
]

where (C) is the semantic proposition and (ho_c) is the risk attached to
asserting it.

A promotion judgement

[
kappadash c
]

should mean that the assumptions carried by (kappa), together with explicit
transport/identification premises, entail

[
sup_{Dinmathcal W_c}ho_c(D)ledelta_c.
]

The important case is **not** when
(ho_kappa=ho_c). Existing risk-control theory already handles much of
that situation.

The interesting case is target mismatch:

[
ho_kappa
eqho_c.
]

Then a low bound on (ho_kappa) must not be promoted to (c) unless a
separate warrant/identification map is proved.

## 6. Non-promotion witness

A useful output of the calculus would be a counterworld certificate:

find

[
D^starinmathcal W_c
]

such that:
- all premises/certificates remain valid;
- the observed evidence is compatible with (D^star);
- but
  [
  ho_c(D^star)>delta_c.
  ]

Then (kappa
vdash c).

This is closely related to countermodels in logic, identified-set witnesses in
econometrics, robust-optimization adversaries, and defeaters in assurance
cases. The candidate contribution is therefore not the existence of
counterexamples itself, but a **typed statistical interface** that turns the
mismatch into a machine-checkable non-promotion result.

## 7. Why this may still be distinct

The closest fields each cover only part of the proposed object:

- **partial identification:** compatible parameter/world sets and decisions;
- **Blackwell/Le Cam:** relative informativeness of experiments for decision
  problems;
- **data fusion:** how extra datasets/restrictions sharpen identification;
- **assurance cases:** structured claim/evidence arguments and defeaters;
- **risk-control / conformal methods:** finite-sample guarantees for specified
  losses/targets.

The candidate research question is whether a formal **interface between these
layers** is already known:

> Given a statistical certificate whose formal target is A, when is it
> logically/statistically permissible to use it as evidence for semantically
> different claim B?

That question is narrower than "what is identified?" and narrower than "which
experiment is more informative?"

## 8. Strongest defensible paper claim today

Do **not** write:

> We introduce a new theory of identified sets, evidence composition, or
> unsafe-world elimination.

A defensible current framing is:

> We study a target-mismatch problem in AI evidence use: statistical
> certificates are often valid for one loss, population, or evidence channel
> but are informally promoted to stronger provenance or semantic claims. We
> connect partial identification, comparison of experiments, and assurance
> reasoning to define an auditable certificate-to-claim interface, and we use
> counterworlds to block unsupported promotion.

Even this remains a **candidate contribution** until reviewed against adjacent
formal methods / assurance / statistics literature.

## 9. Novelty status by component

- Observational-equivalence impossibility: **ESTABLISHED / NOT NOVEL**
- Identified risk sets: **ESTABLISHED / NOT NOVEL**
- Worst-case admissibility: **ESTABLISHED / NOT NOVEL**
- Unsafe-world set containment: **DEFINITIONAL COROLLARY**
- Product-channel monotonicity: **ESTABLISHED / NOT NOVEL**
- Conditional-kernel representation: **STANDARD REPRESENTATION**
- Deterministic redundancy / garbling: **ESTABLISHED / NOT NOVEL**
- Finite-sample CP fixed-gate certificate: **BASELINE APPLICATION**
- Claim hierarchy + evidence: **HIGH PRIOR-ART OVERLAP**
- Eliminative / defeater reasoning: **HIGH PRIOR-ART OVERLAP**
- Certificate-to-claim target typing: **POTENTIAL GAP / UNESTABLISHED**
- Machine-checkable non-promotion witness: **POTENTIAL GAP / UNESTABLISHED**
- Typed composition across certificate targets: **POTENTIAL GAP / UNESTABLISHED**

## 10. Recommended next external-review question

Do not ask a reviewer:

> Is our unsafe-world theorem novel?

Ask instead:

> Is there an established formalism in statistical decision theory,
> partial identification, comparison of experiments, or assurance cases that
> treats a statistical certificate as a typed object carrying its target loss,
> population/world class, and evidence scope, and formally forbids using that
> certificate to authorize a semantically stronger claim unless a separate
> identification/transport implication is supplied?

A positive answer may collapse the remaining novelty.
A negative answer would identify the actual research gap much more precisely.

## 11. Publication decision rule

Until that question receives external scrutiny:

- manuscript status: **THEORY DRAFT**;
- novelty: **UNESTABLISHED**;
- no Zenodo/arXiv novelty claim;
- no Stage B change;
- do not add new RAID experiments to rescue novelty.

The research value remains real even if the final paper becomes a bridge /
application paper: the target-mismatch failure is practically important and
the existing CogniPrint evidence provides a concrete motivating case.
