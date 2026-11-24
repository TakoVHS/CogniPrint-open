# Finite-Sample Composition Certificate v0.1

Status: **BASELINE / APPLICATION OF EXACT BINOMIAL INFERENCE / NOVELTY_NOT_CLAIMED**

Related:
- population sharp composition: `docs/evidence-channel-sharp-composition-v0.1.md`
- partial-identification map:
  `docs/claim-promotion-partial-identification-literature-map.md`

## 1. Why the naive epsilon construction is not adopted

The initial proposal suggested estimating a marginal law
\\(\mu^E\\), estimating a conditional kernel \\(K(F\mid E)\\), and
adding two radii \\(\epsilon_\mu+\epsilon_K\\).

That is not a theorem without:

1. a specified metric on joint laws;
2. a proved inequality translating marginal/kernel deviations into that joint
   metric;
3. a valid confidence region for the conditional kernel, including rare/empty
   bins;
4. a proof that the resulting neighborhood gives the desired coverage.

Also:

- a Clopper--Pearson upper confidence limit for a probability is not a radius
  \\( |\hat p-p| \\);
- enlarging an epsilon-neighborhood enlarges the compatible-world set, so its
  worst-case risk is monotone nondecreasing in epsilon;
- no generic internal "optimal epsilon" follows from this nesting alone.

Chernozhukov--Hong--Tamer (2007) provide a general criterion-inversion
framework for estimation and confidence regions of identified parameter sets.
This note does not attribute the naive additive-epsilon formula to that paper.

## 2. A simpler exact finite-sample problem

For a known-membership claim, let

\\[
A=A(E,F)\in\{0,1\}
\\]

be a **fixed product gate**, specified before validation labels are observed.

Let

\\[
a_K=\Pr(A=1\mid K),
\qquad
a_U=\Pr(A=1\mid U),
\\]

where \\(K\\) means the declared known component and \\(U\\) the
declared unknown component.

Let deployment unknown prevalence satisfy the external world-class restriction

\\[
\pi\le\pi_U.
\\]

The risk of claiming "known" among accepted observations is

\\[
\rho(\pi,a_K,a_U)
=
\frac{\pi a_U}
{(1-\pi)a_K+\pi a_U},
\\]

when the denominator is positive.

This function is increasing in \\(\pi\\) and \\(a_U\\), and decreasing
in \\(a_K\\).

## 3. Validation samples

Assume:

- \\(X_K\sim\mathrm{Binomial}(n_K,a_K)\\) from an i.i.d. validation
  sample representative of the declared known component;
- \\(X_U\sim\mathrm{Binomial}(n_U,a_U)\\) from an i.i.d. validation
  sample representative of the declared unknown component.

The transportability of these acceptance probabilities to the declared target
world class is an explicit assumption.

Let

\\[
L_K
=
L_{\mathrm{CP}}(X_K,n_K;\alpha/2)
\\]

be the one-sided Clopper--Pearson lower confidence bound for \\(a_K\\), and

\\[
U_U
=
U_{\mathrm{CP}}(X_U,n_U;\alpha/2)
\\]

the one-sided upper bound for \\(a_U\\).

By the union bound,

\\[
\Pr(a_K\ge L_K\ \land\ a_U\le U_U)
\ge 1-\alpha.
\\]

Independence between the two confidence events is not required for this
coverage statement.

## 4. Proposition — finite-sample product-gate certificate

With probability at least \\(1-\alpha\\),

\\[
\boxed{
\rho
\le
\frac{\pi_U U_U}
{(1-\pi_U)L_K+\pi_U U_U}
=:B_{1-\alpha}.
}
\\]

### Proof

On the simultaneous confidence event,

\\[
a_K\ge L_K,
\qquad
a_U\le U_U,
\qquad
\pi\le\pi_U.
\\]

Because \\(\rho(\pi,a_K,a_U)\\) is monotone increasing in
\\(\pi,a_U\\) and decreasing in \\(a_K\\), its largest value over the
confidence rectangle is attained at
\\((\pi_U,L_K,U_U)\\). \\(\square\\)

If the corner has zero accepted mass, the implementation returns the vacuous
upper bound one.

## 5. Structural limitation

This certificate separates two uncertainties:

### Sampling uncertainty

As \\(n_K,n_U\\) grow, the Clopper--Pearson bounds contract around the
component acceptance rates.

### Structural uncertainty

The bound \\(\pi\le\pi_U\\) does **not** improve merely because more
known/unknown validation observations are collected.

If \\(\pi_U=1\\), the robust known-membership risk upper bound is one for
any product gate that can accept unknown observations. More same-channel
validation data cannot remove that structural uncertainty.

Likewise, if the "unknown validation sample" is not representative of the
deployment unknown component, the certificate does not transport to that
deployment world.

## 6. Multiple predeclared product gates

For a finite family of \\(m\\) product gates fixed before validation-label
inspection, there are \\(2m\\) one-sided component bounds.

Assign each bound level

\\[
\alpha/(2m).
\\]

Then, by Bonferroni,

\\[
\Pr(
\text{all }2m\text{ component bounds hold}
)
\ge1-\alpha.
\\]

All resulting risk upper bounds are therefore simultaneously valid, so a gate
may be selected from this predeclared family after validation data are
observed.

This is analogous in spirit to the earlier finite-grid selective-risk baseline
and is not claimed as a novel multiple-testing result.

## 7. Why direct gate certification is preferable here

For a fixed gate, estimating \\(\mu^E\\) and \\(K(F\mid E)\\)
separately is unnecessary.

The target risk depends on the aggregate gate acceptance probabilities
\\(a_K\\) and \\(a_U\\). Direct binomial validation:

- avoids division by small bin counts;
- avoids nonparametric conditional-kernel estimation;
- gives an exact finite-sample confidence statement;
- makes the required transportability and prevalence assumptions visible.

Binned conditional-kernel estimation becomes relevant only when the research
question specifically requires the kernel itself or adaptive composition
across bins.

## 8. Prior-art boundary

This finite-sample layer is **not** presented as a new general inference
framework.

Relevant established work includes:

- Imbens & Manski (2004): confidence intervals under partial identification;
- Chernozhukov, Hong & Tamer (2007): estimation and confidence regions for
  identified parameter sets through sample criterion inversion;
- Romano & Shaikh (2008): inference for parameters in partially identified
  models;
- Kaido & Santos (2014): efficient estimation for convex
  moment-inequality identified sets.

Recent data-combination work also shows that auxiliary information can sharpen
identified sets, so heterogeneous-evidence composition itself is broad
prior-art territory.

The candidate CogniPrint contribution remains the **claim-admissibility
interpretation** and the exact population unsafe-world elimination criterion,
pending external review.

## 9. What is intentionally not claimed

- No generic \\(\epsilon_\mu+\epsilon_K\\) finite-sample theorem.
- No universal \\(n^{-1/4}\\) conditional-kernel rate.
- No Dinkelbach optimization is needed for this scalar fixed-gate certificate.
- No claim that the finite-sample upper bound itself converges to zero.
  It converges toward the structural risk determined by the deployment
  prevalence bound and component acceptance rates.
- No use of exposed RAID Stage A data.
