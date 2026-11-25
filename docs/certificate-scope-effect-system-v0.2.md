# Certificate Scope Effect-Style Judgment — Formalization v0.2

Status: **CANDIDATE CALCULUS / NOVELTY UNESTABLISHED / HIGH COLLISION RISK**

This note strengthens the Certificate Scope Judgment (CSJ) without claiming a
new type theory. The current object is an **effect-style indexed judgment**.
Calling it a full type-and-effect system is deferred until a term calculus,
static semantics, operational/denotational semantics, and metatheory are all
specified.

## 1. Why v0.1 is not yet a type-and-effect system

A classical type-and-effect system normally has a judgment such as

\[
\Gamma \vdash e : \tau \; ! \; \varepsilon,
\]

together with syntax for terms, composition rules, and a soundness theorem
connecting static judgments to program semantics.

CSJ v0.1 already has typed statistical objects and confidence bookkeeping, but
it does not yet define a programming language whose evaluation preserves those
types/effects. Therefore the defensible description is:

> a declarative certificate-to-claim judgment with effect-style confidence
> accounting.

This distinction is deliberate.

## 2. Certificate specification

A statistical certificate procedure is specified by

\[
\kappa
=
(E_\kappa,\mathcal W_\kappa^A,\rho_\kappa,B_\kappa,\alpha_\kappa),
\]

where:

- \(E_\kappa\) is the evidence channel or evidence scope;
- \(\mathcal W_\kappa^A\) is the world class on which all validity and
  transport assumptions required by the certificate hold;
- \(\rho_\kappa:\mathcal W_\kappa^A\to[0,1]\) is the certified target;
- \(B_\kappa(Z)\) is a data-dependent upper bound;
- \(\alpha_\kappa\in[0,1]\) is the certificate failure budget.

Uniform frequentist validity is

\[
\inf_{D\in\mathcal W_\kappa^A}
\Pr_D\!\left[
\rho_\kappa(D)\le B_\kappa(Z)
\right]
\ge 1-\alpha_\kappa.
\]

The assumptions are absorbed into the valid world class rather than ordered by
raw set inclusion. This avoids an ill-defined rule such as
\(A_2\subseteq A_1\), because assumptions are propositions whose strength is
determined by logical implication, not by their textual membership in a set.

## 3. Claim requirement

A claim requirement is

\[
c=(C,\mathcal W_c,\rho_c,\delta_c,\bar\alpha_c),
\]

where:

- \(C\) is the semantic claim;
- \(\mathcal W_c\) is its deployment/world class;
- \(\rho_c\) is the downstream claim-risk functional;
- \(\delta_c\) is the maximum tolerated claim risk;
- \(\bar\alpha_c\) is the maximum allowed false-promotion budget.

The risk tolerance \(\delta_c\) and the confidence/error budget
\(\bar\alpha_c\) are different quantities and must not be conflated.

## 4. Quantitative warrant

For certificates \(\kappa_1,\ldots,\kappa_m\), a quantitative warrant for
claim \(c\) is a pair

\[
T=(\mathcal W_T,g_T),
\]

where \(g_T:[0,1]^m\to[0,1]\) is coordinatewise nondecreasing and

\[
\forall D\in\mathcal W_T:
\qquad
\rho_c(D)
\le
g_T\!\left(
\rho_1(D),\ldots,\rho_m(D)
\right).
\]

The monotonicity condition is what permits substitution of certified upper
bounds:

\[
\rho_i(D)\le b_i\ \forall i
\quad\Longrightarrow\quad
\rho_c(D)\le g_T(b_1,\ldots,b_m).
\]

This is stronger and more explicit than a bare relation
\(\tau_1\models\tau_2\). A target name alone does not justify a numerical
bound transfer.

### Direct same-target warrant

Direct promotion is the special case \(m=1\) with

\[
g_T(x)=x
\]

and \(\rho_c=\rho_\kappa\) throughout the claim scope.

## 5. Static scope condition

For a warrant that does not itself transport across populations, require

\[
\boxed{
\mathcal W_c
\subseteq
\mathcal W_T
\cap
\bigcap_{i=1}^m \mathcal W_{\kappa_i}^A.
}
\]

If a certificate is calibrated on one population and the claim concerns
another, the missing transport step must be represented inside a separate
validated warrant. Scope mismatch is not repaired by confidence level.

## 6. Runtime discharge

After observing data \(Z=z\), let

\[
b_i=B_{\kappa_i}(z).
\]

Define

\[
b_c^T
=
g_T(b_1,\ldots,b_m),
\qquad
\alpha_T
=
\min\!\left(1,\sum_{i=1}^m\alpha_i\right).
\]

Runtime promotion is permitted only if

\[
b_c^T\le\delta_c
\qquad\text{and}\qquad
\alpha_T\le\bar\alpha_c.
\]

The first inequality discharges the risk tolerance. The second discharges the
false-promotion budget.

## 7. Effect-style promotion judgment

We write

\[
\boxed{
\kappa_1,\ldots,\kappa_m
\vdash_T^{\alpha_T}
c
}
\]

when:

1. every certificate has uniform frequentist validity on its declared world
   class;
2. the static scope condition holds;
3. \(T\) is a valid quantitative warrant;
4. the composed confidence budget is \(\alpha_T\);
5. the realized warrant-transformed bound satisfies
   \(g_T(b_1,\ldots,b_m)\le\delta_c\);
6. \(\alpha_T\le\bar\alpha_c\).

This is an indexed statistical judgment. The current manuscript should call it
a **candidate effect-style judgment**, not yet a full type-and-effect system.

## 8. Proposition — Warranted promotion soundness

Assume the judgment above is valid. For every unsafe claim world

\[
D\in\mathcal W_c,
\qquad
\rho_c(D)>\delta_c,
\]

the probability of promotion obeys

\[
\boxed{
\Pr_D(\mathrm{PROMOTE})
\le
\sum_{i=1}^m\alpha_i.
}
\]

### Proof

Let

\[
G_i=
\{\rho_i(D)\le B_i(Z)\}
\]

be the validity event of certificate \(i\). On
\(\bigcap_i G_i\), monotonicity and the warrant imply

\[
\rho_c(D)
\le
g_T(\rho_1(D),\ldots,\rho_m(D))
\le
g_T(B_1(Z),\ldots,B_m(Z))
\le
\delta_c.
\]

Thus in a world with \(\rho_c(D)>\delta_c\), promotion can occur only if at
least one \(G_i\) fails. By the union bound,

\[
\Pr_D(\mathrm{PROMOTE})
\le
\Pr_D\!\left(\bigcup_i G_i^c\right)
\le
\sum_i\alpha_i.
\qquad\square
\]

No independence assumption is needed.

## 9. Counterworld semantics of failed promotion

For realized bounds \(b=(b_1,\ldots,b_m)\), define

\[
\mathcal V_c(b)
=
\left\{
D\in\mathcal W_c\cap\bigcap_i\mathcal W_{\kappa_i}^A:
\rho_i(D)\le b_i\ \forall i
\right\}.
\]

A non-promotion witness is

\[
D^\star\in\mathcal V_c(b)
\quad\text{with}\quad
\rho_c(D^\star)>\delta_c.
\]

If such a world is found, the realized certificate constraints do not suffice
to support the claim over the declared world class.

Absence of a witness in a finite enumerated model proves only the finite model.
In a larger world class, failure to find a witness is **UNRESOLVED**, not
evidence of universal safety.

## 10. Why the proposed generic sub-effect relation is rejected

The draft relation

\[
\varepsilon_2\preceq\varepsilon_1
\]

defined only by scope inclusion, target-name entailment, alpha ordering, and
assumption-set inclusion is too weak for the intended soundness theorem.

Two specific defects are:

1. \(\tau_1\models\tau_2\) does not by itself provide a numerical map from
   an upper bound on \(\rho_1\) to an upper bound on \(\rho_2\).
2. \(A_2\subseteq A_1\) is not the correct semantic notion of assumption
   strength; what matters is implication between assumptions, equivalently
   inclusion between the world classes on which they hold.

The quantitative warrant \(g_T\) and world-class semantics repair both
problems.

## 11. Prior-art boundary

The confidence-budget part of this calculus is not novel. Approximate Hoare
Logic already indexes judgments by an error probability and composes those
budgets through union bounds. Later probabilistic program logics, including
higher-order systems, develop substantially richer error accounting.

Likewise, Belief Hoare Logic and StatWhy already formalize statistical
preconditions, postconditions, interpretations, and correct use of hypothesis
tests.

A 2026 preprint, *Proxy Evidence Certificates and World-Model Validation:
Evidence Fibers, Sharp Envelopes, and Counterworld Realization*, is a high-risk
novelty collision for the compatible-world / target-envelope / counterworld
parts of CogniPrint. Its public record explicitly describes certification over
worlds compatible with proxy evidence and compilation of residual uncertainty
into executable counterworlds. It is a preprint, not treated here as
peer-reviewed validation, but it must be included in the novelty audit.

Therefore the surviving research question is narrower:

> Does the explicit **certificate-to-claim quantitative warrant judgment**,
> combining frequentist certificate validity, claim-specific world scope,
> heterogeneous target transformers, confidence-budget accounting, and
> counterworld rejection, provide a distinct and useful formal interface not
> already subsumed by probabilistic program logics, statistical-program
> verification, assurance arguments, or proxy-evidence world-fiber methods?

Status remains **NOVELTY UNESTABLISHED**.
