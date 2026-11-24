# Certificate-to-Claim Target Typing — Candidate Formal Object

Status: **CANDIDATE / HIGH COLLISION RISK / NOT A THEOREM / NOVELTY UNESTABLISHED**

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


## 7. Newly identified collision risks

The deep audit found close antecedents that materially narrow this candidate.

### Assurance 2.0 / Toulmin-style warrants

Assurance-case theory already distinguishes:
- evidence incorporation;
- the reasoning/warrant linking evidence to a claim;
- substitution/concretion steps;
- side claims/assumptions required for the inference;
- defeaters and reasons a top-level claim is not established.

Therefore the generic rule

> evidence may support claim B only if an explicit warrant bridges evidence A to B

is established argumentation/assurance territory.

### StatWhy

StatWhy formally annotates statistical hypothesis-testing programs with the
requirements of the statistical methods and automatically checks whether those
requirements were specified, including assumptions that cannot themselves be
mechanically verified, such as properties of the unknown population.

Therefore the generic idea

> statistically typed requirements + machine checking of missing assumptions

also has strong prior art.

### Machine-checked assurance cases

Recent assurance work uses logic programming / machine checking to determine
whether a top-level claim follows and to expose defeaters or reasons for
failure.

Therefore "machine-checkable non-promotion" is not enough by itself to
establish novelty.

## 8. Surviving candidate, narrowed again

The remaining candidate is now:

> a domain-specific statistical interface in which each certificate carries
> its exact target functional, validation/deployment population scope,
> evidence channel, confidence accounting, and transport assumptions; each
> downstream AI provenance claim carries a distinct semantic target and
> tolerated risk; and rejection is witnessed by a partial-identification
> counterworld that satisfies the certificate while violating the claim.

Potential distinct ingredients are the **combination** of:

1. statistical target typing rather than generic argument typing;
2. explicit prevention of loss/population/evidence-scope upcasts;
3. partial-identification counterworlds as concrete rejection witnesses;
4. finite-sample confidence accounting that survives only admissible
   composition;
5. a claim poset that distinguishes semantic/logical strength from statistical
   confidence.

Whether this combination is actually novel is still unknown.

## 9. Revised falsification question

The external-review question should now be even narrower:

> Is there an existing formal system that types a statistical certificate by
> target functional, population/domain, evidence sigma-field and confidence
> budget, then checks whether it can support a semantically distinct downstream
> claim and emits a compatible counterworld when the promotion is invalid?

If such a system exists, the remaining theory novelty largely collapses.
