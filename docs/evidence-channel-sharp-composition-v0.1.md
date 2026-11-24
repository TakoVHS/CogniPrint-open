# Sharp Composition of Evidence Channels v0.1

Status: **THEORY_DRAFT / NOVELTY_UNESTABLISHED / NOT_PEER_REVIEWED**

Related:
- Draft PR #84
- mathematical review gate #85
- `docs/claim-promotion-identifiability-v0.1.md`
- `docs/claim-promotion-partial-identification-literature-map.md`

## 1. Purpose

The previous theory increment established monotonicity:

\[
\mathcal R_C(E,F)\subseteq\mathcal R_C(E).
\]

That inclusion is useful but not sharp enough. The central question is:

> Exactly when does a second evidence channel eliminate the unsafe worlds that
> remain observationally compatible with the first channel?

The answer depends on the **joint law**, equivalently on the conditional law of
the added channel given the existing evidence.

No statistical-independence assumption is required.

## 2. Coarse evidence fiber

Let \(\mathcal W\) be the declared class of admissible worlds and let
\(\rho_C(D)\in[0,1]\) be the risk attached to claim \(C\).

For an observed law \(\mu_{\rm obs}^E\) of channel \(E\), define

\[
\mathcal W_E
=
\{D\in\mathcal W:\mu_D^E=\mu_{\rm obs}^E\}.
\]

The corresponding identified risk set is

\[
\mathcal R_C(E)
=
\{\rho_C(D):D\in\mathcal W_E\}.
\]

## 3. Product evidence and conditional kernels

Let \(F\) be an additional channel and let the observed joint evidence law be

\[
\nu_{\rm obs}^{E,F}.
\]

Assume the evidence spaces are standard Borel so regular conditional
probabilities exist. Disintegrate the observed joint law as

\[
\nu_{\rm obs}^{E,F}(de,df)
=
\mu_{\rm obs}^{E}(de)
K_{\rm obs}(df\mid e).
\]

For each \(D\in\mathcal W_E\), write its joint evidence law as

\[
\mu_D^{E,F}(de,df)
=
\mu_{\rm obs}^{E}(de)
K_D(df\mid e).
\]

Conditional kernels are understood up to
\(\mu_{\rm obs}^{E}\)-almost-sure equality.

## 4. Theorem — sharp conditional-kernel composition

The worlds compatible with the product channel are exactly

\[
\mathcal W_{E,F}
=
\left\{
D\in\mathcal W_E:
K_D(\cdot\mid e)
=
K_{\rm obs}(\cdot\mid e)
\quad
\mu_{\rm obs}^{E}\text{-a.s.}
\right\}.
\]

Consequently,

\[
\boxed{
\mathcal R_C(E,F)
=
\left\{
\rho_C(D):
D\in\mathcal W_E,K_D=K_{\rm obs}\ \mu_{\rm obs}^{E}\text{-a.s.}
\right\}.
}
\]

### Proof

For \(D\in\mathcal W_E\), the \(E\)-marginal already equals
\(\mu_{\rm obs}^E\). Two joint probability measures with this common
marginal are equal exactly when their regular conditional laws of \(F\)
given \(E\) agree almost surely with respect to that marginal. Therefore
\(\mu_D^{E,F}=\nu_{\rm obs}^{E,F}\) iff
\(K_D=K_{\rm obs}\) almost surely. Taking the image of this compatible-world
fiber through \(\rho_C\) gives the identified risk set. \(\square\)

This result is an exact characterization, not yet a novelty claim. It is
closely related to classical disintegration, experiment comparison, and
partial-identification reasoning.

## 5. Corollary — exact admissibility criterion

For tolerance \(\delta\), define the unsafe coarse-fiber worlds

\[
\mathcal U_\delta(E)
=
\{D\in\mathcal W_E:\rho_C(D)>\delta\}.
\]

Then the product evidence makes claim \(C\) robustly admissible iff

\[
\boxed{
\mathcal U_\delta(E)
\cap
\{D:K_D=K_{\rm obs}\ \mu_{\rm obs}^E\text{-a.s.}\}
=
\varnothing.
}
\]

Equivalently: **every unsafe world left by the first channel must be rejected
by the observed conditional behavior of the second channel.**

This is both necessary and sufficient relative to the declared world class.

## 6. Corollary — strict worst-case gain

Let

\[
U_E
=
\sup_{D\in\mathcal W_E}\rho_C(D),
\qquad
U_{E,F}
=
\sup_{D\in\mathcal W_{E,F}}\rho_C(D).
\]

Then

\[
U_{E,F}\le U_E.
\]

The composition gives a strict worst-case improvement exactly when

\[
U_{E,F}<U_E.
\]

If the supremum in \(\mathcal W_E\) is attained, strict improvement requires
the joint evidence to exclude all maximizers and also to leave a positive gap
below their risk. Without compactness/attainment assumptions, "the maximizer
is excluded" alone is not enough because compatible worlds may approach the
same supremum.

## 7. Redundancy theorem

A strong sufficient condition for complete redundancy is:

there exists a world-invariant Markov kernel \(K\) such that for every
\(D\in\mathcal W_E\),

\[
K_D(\cdot\mid e)=K(\cdot\mid e)
\quad
\mu_{\rm obs}^{E}\text{-a.s.},
\]

and the observed kernel is the same \(K_{\rm obs}=K\).

Then

\[
\mathcal W_{E,F}=\mathcal W_E
\]

and therefore

\[
\boxed{
\mathcal R_C(E,F)=\mathcal R_C(E).
}
\]

### Deterministic special case

If

\[
F=\phi(E)
\]

for a fixed measurable function \(\phi\), then the conditional kernel is the
degenerate kernel

\[
K(df\mid e)=\delta_{\phi(e)}(df),
\]

which is world-invariant. Hence adding a deterministic transformation of the
same evidence cannot reduce the identified set.

This formalizes one important kind of "another classifier adds no evidence":
not because the output names differ, but because the added output is already a
garbling/deterministic function of what is available.

## 8. Claim-relevant refinement

We define \(F\) to be **claim-relevant at the observed law** relative to
\(E\) and claim \(C\) if

\[
\mathcal R_C(E,F)
\subsetneq
\mathcal R_C(E).
\]

For a particular tolerance \(\delta\), call it
**\(\delta\)-separating** if

\[
\sup\mathcal R_C(E)>\delta
\quad\text{but}\quad
\sup\mathcal R_C(E,F)\le\delta.
\]

This is the property needed for actual claim promotion.

It is intentionally different from "statistical independence".
Independence of \(E\) and \(F\) is neither necessary nor sufficient for
strict identification gain.

## 9. Marginal channels are not enough

In general,

\[
\mathcal R_C(E,F)
\subseteq
\mathcal R_C(E)\cap\mathcal R_C(F),
\]

but equality need not hold.

The reason is that separate marginals do not encode the dependence structure
between channels. The observed joint law can exclude worlds that match each
marginal separately.

This is the same broad phenomenon behind many sharp-bound and data-fusion
problems: a target depending on a joint distribution may remain partially
identified from marginals alone.

## 10. Finite synthetic example

Consider a finite coarse fiber containing three worlds:

| World | Claim risk | Coarse evidence | Conditional kernel signature |
|---|---:|---|---|
| safe | 0.04 | z | k_obs |
| unsafe-A | 0.35 | z | k_A |
| unsafe-B | 0.60 | z | k_B |

With only \(E=z\),

\[
\mathcal R_C(E)=\{0.04,0.35,0.60\}.
\]

If the observed second-channel kernel is \(k_{\rm obs}\), then

\[
\mathcal R_C(E,F)=\{0.04\}.
\]

At \(\delta=0.10\), the first channel is not admissible while the product
channel is admissible.

For a redundant channel where all three worlds have conditional signature
\(k_{\rm obs}\),

\[
\mathcal R_C(E,F)=\mathcal R_C(E),
\]

so no amount of relabeling the second output creates evidence.

## 11. Relation to Blackwell and prior art

This theorem must be positioned conservatively.

Blackwell comparison already formalizes when one experiment is more informative
than another via garbling and decision value. Le Cam deficiency generalizes
quantitative comparison between experiments. Partial-identification and
sharp-bound literatures already study how additional restrictions/data reduce
compatible parameter sets.

The candidate CogniPrint contribution is narrower:

> applying an exact channel-composition criterion to a claim-specific
> admissibility calculus, where unsafe worlds must be eliminated before a
> stronger AI provenance/source claim is authorized.

Novelty remains **UNESTABLISHED** until an external mathematical reviewer and a
deeper literature search support it.

## 12. Next research question

The next nontrivial step is finite-sample composition:

- the coarse evidence law is estimated rather than known;
- the conditional kernel of the refinement channel is estimated from data;
- both sampling uncertainty and structural identification uncertainty must be
  propagated into a confidence region for
  \(\sup\mathcal R_C(E,F)\).

That step must be designed prospectively and must not be tuned on the exposed
RAID Stage A records.
