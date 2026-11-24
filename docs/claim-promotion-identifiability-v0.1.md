# Claim Promotion and Evidence-Channel Identifiability v0.1

Status: **THEORY_DRAFT / NOVELTY_UNESTABLISHED / NOT_PEER_REVIEWED**

Related:
- Draft PR #84
- mathematical review gate #85
- finite-sample baseline: `docs/evidence-bounded-finite-sample-baseline-v0.1.md`

This note formalizes a candidate research direction above finite-sample
selective-risk control. It deliberately separates:

1. a valid risk certificate for a specified deployment distribution;
2. identification of a different claim;
3. permission to promote to a stronger or logically different claim.

The central principle is:

> A risk certificate for one target does not identify a different target when
> the available evidence channel is observationally compatible with worlds in
> which that different target has different truth values.

This is an **identifiability statement**, not yet a novelty claim.

## 1. Worlds, latent source state, and evidence channels

Let \\(\Theta\\) be a latent source-state space. It may contain known model
families, unknown model families, human sources, or other source/process states.

A world \\(D\\) is a probability law over \\(\mathcal X\times\Theta\\).

An evidence channel is a measurable map

\\[
e:\mathcal X\to\mathcal Z.
\\]

Examples include a closed-set score vector, a provenance log, a watermark
verification result, or another measured signal.

For a world \\(D\\), let \\(\mu_D^e\\) denote the induced law of
\\(e(X)\\).

For several channels \\(E=(e_1,\dots,e_m)\\), write
\\(\mu_D^E\\) for the joint induced law.

## 2. Claim targets

A claim event is a subset \\(C\subseteq\Theta\\). For example:

- known-set membership:
  \\(C_{\mathrm K}=\{\theta:\theta\in\Theta_{\mathrm{known}}\}\\);
- one specific known family:
  \\(C_k=\{k\}\\);
- unknown membership:
  \\(C_{\mathrm U}=\Theta\setminus\Theta_{\mathrm{known}}\\);
- AI-generated:
  a domain-defined subset \\(C_{\mathrm{AI}}\subseteq\Theta\\);
- an attested provenance/process claim:
  another subset or an augmented latent state.

The named claims above are **not a linear hierarchy**.

In logical-strength order, define

\\[
C\preceq C'
\quad\Longleftrightarrow\quad
C'\subseteq C.
\\]

Thus \\(C'\\) is the stronger claim. In particular,

\\[
C_{\mathrm K}\preceq C_k,
\\]

because "source is exactly family \\(k\\)" implies "source is in the known
set". Known and unknown membership are incompatible rather than successive
levels. The AI-generated event can be incomparable with either, depending on
how the source state is defined.

The full powerset \\(2^\Theta\\) is a Boolean lattice under set inclusion,
but any named subset of claims should be called a **claim poset** unless closure
under meet and join has actually been established.

## 3. Identifiability of a claim functional

For a claim event \\(C\\), define a world-level target functional

\\[
\eta_C(D)=\Pr_D(\Theta\in C).
\\]

For a selected population with acceptance rule \\(g\\), define

\\[
\eta_{C,g}(D)
=
\Pr_D(\Theta\in C\mid g(X)=1),
\\]

when the conditioning event has positive probability.

### Definition 3.1 — E-identifiability

A target functional \\(\eta\\) is identified by evidence channels
\\(E\\) over a world class \\(\mathcal W\\) if

\\[
\mu_D^E=\mu_{D'}^E
\implies
\eta(D)=\eta(D')
\\]

for every \\(D,D'\in\mathcal W\\).

If two allowed worlds are observationally equivalent through \\(E\\) but
have different target values, \\(\eta\\) is not identified by \\(E\\).

## 4. Theorem — observational-equivalence claim non-identifiability

Let \\(\mathcal W\\) contain worlds \\(D_0,D_1\\). Let \\(E\\) be
the available evidence channels. Suppose

\\[
\mu_{D_0}^E=\mu_{D_1}^E
\\]

but

\\[
\eta(D_0)\ne\eta(D_1).
\\]

Then \\(\eta\\) is not identified by \\(E\\) over \\(\mathcal W\\).

Moreover, for every sample size \\(n\\), the induced laws of
\\(E_1,\dots,E_n\\) are identical under \\(D_0\\) and \\(D_1\\).
Therefore no statistical test based only on \\(E\\) can distinguish the two
worlds with minimax error below \\(1/2\\) under equal prior weights.

### Proof

Equality of one-observation evidence laws implies equality of their product
laws for every i.i.d. sample size:

\\[
(\mu_{D_0}^{E})^{\otimes n}
=
(\mu_{D_1}^{E})^{\otimes n}.
\\]

Hence every measurable statistic or decision rule based on the evidence sample
has the same distribution in the two worlds. A target taking different values
in those worlds cannot be a function of the evidence law, so it is not
identified.

For binary testing with equal priors, identical observation laws have total
variation distance zero. The optimal Bayes error is therefore
\\((1-\mathrm{TV})/2=1/2\\). \\(\square\\)

### Interpretation

This theorem is a standard identifiability consequence. The potential
CogniPrint contribution is not the existence of observational equivalence
itself, but a disciplined mapping from such identification limits to
evidence-bounded claim admissibility.

## 5. Closed-set certificate non-transfer construction

Let \\(e_{\mathrm{closed}}(x)\\) contain only a closed-set predictor's
output over \\(K\\) known classes.

Consider a known-only world \\(D_0\\), and let an acceptance rule
\\(g\\) depend only on \\(e_{\mathrm{closed}}\\).

Construct \\(D_\pi\\) as follows:

1. with probability \\(1-\pi\\), draw a known-source observation exactly
   as in \\(D_0\\);
2. with probability \\(\pi\\), draw an unknown-source observation whose
   closed-set evidence has the **same law** as the known-source evidence.

Then

\\[
\mu_{D_\pi}^{e_{\mathrm{closed}}}
=
\mu_{D_0}^{e_{\mathrm{closed}}}.
\\]

Because acceptance depends only on that channel, the unknown fraction among
accepted observations is also \\(\pi\\).

If every accepted unknown source is counted as an error for known-family
classification and the known-only selective risk is \\(r_0\\), then

\\[
R_{\mathrm{sel}}^{D_\pi}(g)
=
\pi+(1-\pi)r_0
\ge\pi.
\\]

As \\(\pi\to1\\), the selective risk approaches one.

### Consequence

A finite-sample certificate calibrated for \\(D_0\\) remains a valid
statement **about \\(D_0\\)** under its assumptions. It does not become a
certificate for \\(D_\pi\\).

The phenomenon is therefore a **transfer failure / target mismatch**, not a
violation of Clopper--Pearson, RCPS, CRC, LEC, or any other correctly stated
closed-distribution guarantee.

## 6. Candidate Claim Promotion Impossibility principle

Let a claim target \\(\eta_C\\) be required for some proposed claim
\\(C\\). Let \\(E\\) be the currently available evidence channels.

If \\(\eta_C\\) is not identified by \\(E\\) over the declared world
class, then no risk certificate whose observable content is entirely
\\(E\\)-measurable can, by itself, identify \\(C\\).

Therefore a valid promotion to that claim requires **at least one** of:

1. **world restriction** — add scientifically defensible assumptions that make
   \\(\eta_C\\) identified from the existing channels; or
2. **evidence refinement** — add a channel that breaks the relevant
   observational equivalence; or
3. **claim narrowing** — replace \\(C\\) with a weaker target that is
   identified by the existing evidence.

This is more precise than saying "every stronger claim requires an OOD
detector". An OOD channel is one possible refinement, not a universal
necessity.

## 7. Claim-poset admissibility

Let claims be ordered by logical implication:

\\[
C\preceq C'
\iff
C'\subseteq C,
\\]

so \\(C'\\) is stronger.

Suppose each claim \\(C\\) has an error tolerance \\(\delta(C)\\), and
tolerances are implication-compatible:

\\[
C\preceq C'
\implies
\delta(C)\ge\delta(C').
\\]

If an evidence procedure certifies a stronger claim \\(C'\\) with error at
most \\(\delta(C')\\), then the implied weaker claim \\(C\\) has error
no larger than that of \\(C'\\), so it is also admissible.

Hence the admissible claims form a **down-set** in the claim poset.

Calling this set an "ideal of a lattice" requires additional closure conditions;
the down-set statement is the result established here.

## 8. Evidence monotonicity

If evidence \\(E'\\) refines \\(E\\) in the sense that every
\\(E\\)-measurable decision rule is also \\(E'\\)-measurable, then any
decision procedure available under \\(E\\) remains available under
\\(E'\\) by ignoring the extra information.

Therefore the best achievable risk for a fixed claim cannot worsen under
evidence refinement, and the set of certifiable claims can only expand.

This is consistent with the Blackwell comparison-of-experiments viewpoint:
a deterministic compression is a garbling of the richer experiment. But
Blackwell sufficiency/equivalence is defined relative to a specified experiment
family; one must not infer that a closed-set score is "insufficient for all
unknowns" merely from terminology.

## 9. Blackwell connection — precise finite counterexample

Let the latent state be known \\(K\\) versus unknown \\(U\\). Let

\\[
\mathcal X=\{a,b,c,d\}.
\\]

Under \\(K\\), put probability \\(1/2\\) on each of \\(a,b\\).
Under \\(U\\), put probability \\(1/2\\) on each of \\(c,d\\).

Define a compressed closed-set channel by

\\[
e(a)=e(c)=z_1,\qquad e(b)=e(d)=z_2.
\\]

Then the induced channel law is identical under \\(K\\) and \\(U\\):

\\[
P_K^e=P_U^e=(1/2,1/2).
\\]

The compressed experiment cannot distinguish the states at all. The full
observation \\(X\\), however, distinguishes them perfectly because the
supports are disjoint.

Thus the full experiment strictly dominates this compressed channel for the
known-versus-unknown decision problem. The example illustrates information
loss under garbling; it does not establish that every real closed-set score has
this property.

## 10. Why the proposed OOD-composition formula is not retained

The draft expression

\\[
R_{\mathrm{sel}}(g\land e_{\mathrm{ood}})
\le
\max(U_{\mathrm{CP}},\gamma)+\text{overlap}
\\]

is not a theorem as written.

An unknown pass-rate bound alone does not determine posterior unknown
contamination among accepted examples; it also depends on the unknown prior,
known acceptance, and dependence between gates.

A valid combined guarantee must either:

- certify the **combined rule directly** on a representative target mixture; or
- state explicit assumptions and derive a Bayes/union-bound composition from
  quantities sufficient to control the combined error.

## 11. Literature collision map

The direction intersects established theory and therefore remains
**NOVELTY_UNESTABLISHED**.

Relevant areas include:

- Blackwell comparison of statistical experiments and garbling;
- Le Cam comparison/deficiency of experiments;
- identification and partial identification in decision theory;
- impossibility and learnability results for OOD detection;
- finite-sample selective-risk control (RCPS/LTT/CRC/LEC/SCRC);
- information-theoretic limits of AI-generated-text detection and provenance.

The publication question is not whether observational equivalence is new. It
is whether the **claim-admissibility formalism**, its composition rules, and
its application to evidence/provenance systems yield a nontrivial result not
already subsumed by these literatures.

## 12. Scientific safeguards

Until external mathematical review:

- do not call Claim Promotion Impossibility a novel theorem as a factual claim;
- do not claim a closed-set CP/CRC/LEC certificate "fails" when evaluated
  outside its target distribution; say it does not transfer/apply;
- do not claim every OOD/provenance assertion needs a physically separate
  channel; world restrictions can also restore identifiability;
- do not call the named claims a linear hierarchy;
- do not call the admissible set a lattice ideal unless lattice closure is
  actually proved;
- do not use exposed Stage A records to tune a new theory demonstration.


## 13. Identified-set claim admissibility

The clean object is the **identified risk set**, rather than a point estimate of
a latent target.

Let \\(\rho_C(D)\in[0,1]\\) be the population error risk associated with
claim \\(C\\). For an observed evidence law \\(\mu_{\mathrm{obs}}^E\\),
define

\\[
\mathcal R_C(E;\mu_{\mathrm{obs}}^E)
=
\{
\rho_C(D):
D\in\mathcal W,
\mu_D^E=\mu_{\mathrm{obs}}^E
\}.
\\]

### Definition 13.1 — Robust evidence admissibility

Claim \\(C\\) is robustly admissible at tolerance \\(\delta\\) under
evidence \\(E\\) when

\\[
\sup \mathcal R_C(E;\mu_{\mathrm{obs}}^E)
\le
\delta.
\\]

This is a worst-case statement over all worlds that remain observationally
compatible with the declared evidence and world class.

### Proposition 13.2 — Plug-in non-certification under partial identification

Suppose

\\[
r_{\mathrm{safe}}
\le
\delta
<
r_{\mathrm{unsafe}}
\\]

and both values lie in
\\(\mathcal R_C(E;\mu_{\mathrm{obs}}^E)\\).

Then a plug-in value \\(\hat r\le\delta\\) computed only from
\\(E\\) cannot by itself certify robust admissibility.

#### Proof

By definition of the identified risk set there exist observationally
compatible worlds with claim risk \\(r_{\mathrm{safe}}\\) and
\\(r_{\mathrm{unsafe}}\\). The same evidence law is therefore compatible
with a world violating the tolerance. Hence
\\(\sup\mathcal R_C>\delta\\), so robust admissibility fails.
\\(\square\\)

This replaces the stronger but incorrect claim that *every* point estimator
"systematically underestimates" risk. A point estimator can equal the
supremum; the problem is that a non-worst-case plug-in value does not certify
the unidentified remainder.

### Theorem 13.3 — No-data-at-the-same-channel impossibility

Let \\(D_0,D_1\in\mathcal W\\) satisfy

\\[
\mu_{D_0}^{E}=\mu_{D_1}^{E},
\\]

while

\\[
\rho_C(D_0)\le\delta<\rho_C(D_1).
\\]

For any sample size \\(n\\) and any decision rule

\\[
\varphi_n:
\mathcal Z^{n}\to\{\mathrm{CLAIM},\mathrm{ABSTAIN}\}
\\]

based only on \\(n\\) i.i.d. observations from channel \\(E\\),

\\[
\Pr_{D_0}(\varphi_n=\mathrm{CLAIM})
=
\Pr_{D_1}(\varphi_n=\mathrm{CLAIM}).
\\]

Consequently, if the rule is \\(\alpha\\)-sound in the unsafe world,

\\[
\Pr_{D_1}(\varphi_n=\mathrm{CLAIM})\le\alpha,
\\]

then it can claim in the safe observationally equivalent world with probability
at most \\(\alpha\\) as well.

#### Proof

The equality of one-observation evidence laws implies equality of the
\\(n\\)-fold product laws for every \\(n\\). Therefore every
\\(E^n\\)-measurable decision rule has the same distribution under the two
worlds. \\(\square\\)

This is stronger and cleaner than saying that a finite-sample identified set
must literally contain the infinite-sample identified set for every realized
sample. Sampling uncertainty and population non-identification are distinct
objects.

### Proposition 13.4 — Channel-refinement monotonicity

Let \\(E'=(E,F)\\) be a product/refined channel with observed joint law
\\(\nu_{\mathrm{obs}}^{E,F}\\), and let
\\(\mu_{\mathrm{obs}}^E\\) be its \\(E\\)-marginal. Then

\\[
\mathcal R_C(E';\nu_{\mathrm{obs}}^{E,F})
\subseteq
\mathcal R_C(E;\mu_{\mathrm{obs}}^E).
\\]

#### Proof

Every world matching the observed joint law automatically matches its
\\(E\\)-marginal. Hence the world set compatible with \\(E'\\) is a
subset of the world set compatible with \\(E\\). Taking the image through
\\(\rho_C\\) preserves set inclusion. \\(\square\\)

If \\(F=\phi(E)\\) is a deterministic transformation of the existing
channel, then the product carries no additional information beyond \\(E\\)
and the identified risk set need not shrink at all.

We call a refinement **claim-relevant** when the inclusion above is strict for
the target claim. This avoids the misleading term "channel independence":
statistical independence is neither necessary nor sufficient for identification
gain.

### 13.5 Exact camouflage example

For known/unknown mixture fraction \\(\pi\\), known acceptance
\\(a_K\\), and unknown acceptance \\(a_U\\), the risk of falsely
claiming known-set membership among accepted observations is

\\[
\rho_{K}(\pi)
=
\frac{\pi a_U}
{(1-\pi)a_K+\pi a_U}.
\\]

Under exact camouflage, \\(a_U=a_K>0\\), so

\\[
\rho_K(\pi)=\pi.
\\]

If the world class only restricts
\\(\pi\in[\pi_L,\pi_U]\\), then the sharp identified risk interval is

\\[
\mathcal R_K
=
[\pi_L,\pi_U].
\\]

An illustrative refining channel with
\\(a_K=0.95\\), \\(a_U=0.05\\), and
\\(\pi\in[0,0.5]\\) instead yields

\\[
\mathcal R_K=[0,0.05].
\\]

These rates are synthetic assumptions, not measured CogniPrint OOD
performance.

### 13.6 Why the proposed bootstrap is rejected

A bootstrap that leaves \\(\pi\\) unrestricted on \\([0,1]\\) while
recomputing \\(\sup_{\pi}\rho_K(\pi)\\) returns the same supremum in
every resample. It does not learn the unidentified quantity and must not be
presented as a confidence interval for the identified set.

Finite-sample inference for partially identified sets is a separate problem;
classical references include Imbens & Manski (2004), Romano & Shaikh (2008),
and Stoye (2009).

### 13.7 No sample-size theorem is claimed yet

The proposed formula involving a generic Hausdorff rate \\(r_n\\) is not
established. Structural non-identification already gives a sharper statement:
if a safe and unsafe world are observationally equivalent through \\(E\\),
no amount of same-channel data can distinguish them. A genuine finite-sample
lower bound would require a specified statistical model, loss, separation
metric, and confidence criterion.
