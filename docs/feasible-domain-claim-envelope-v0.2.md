# Feasible-Domain Claim Envelope — Formalization v0.2

Status: **CURRENT MATHEMATICAL SUPPORT NOTE / ELEMENTARY / NOVELTY NOT CLAIMED**

This note supersedes `docs/canonical-least-warrant-v0.1.md`.

Its purpose is to state the compatible-world envelope without claiming more
than is proved, and to separate three issues that were previously conflated:

1. static scope/transport coverage;
2. realized model/bound feasibility;
3. frequentist unsafe-promotion control.

## 1. Certificate and claim ranges

For certificates
[
\kappa_i=(E_i,\mathcal W_{\kappa_i}^A,\rho_i,B_i,\alpha_i),
]
assume
[
\rho_i:\mathcal W_{\kappa_i}^A\to[0,1].
]

For a downstream claim
[
c=(C,\mathcal W_c,\rho_c,\delta_c,\bar\alpha_c),
]
assume
[
\rho_c:\mathcal W_c\to[0,1].
]

The world index (D) represents both the law governing validation/certificate
data and the deployment quantities used by the risk functionals. Therefore
using one (D) across validation and deployment already encodes a transport
assumption.

## 2. Static scope coverage

Let a warrant have validity scope (mathcal W_T). For conjunctive use of all
certificates require

[
oxed{
\mathcal W_c
\subseteq
\mathcal W_T
\cap
\bigcap_i \mathcal W_{\kappa_i}^A.
}
]

This is a hypothesis that must be justified. It is not repaired by smaller
(alpha_i).

Once it holds, numerical compatible-world analysis can be written directly on
the deployment scope:

[
\mathcal V_T(b)
=
\left\{
D\in\mathcal W_c:
\rho_i(D)\le b_i\ \forall i
\right\}.
]

## 3. Feasible-bound domain

Define

[
\mathcal B_T
=
\{b\in[0,1]^m:\mathcal V_T(b)\neq\varnothing\}.
]

Operationally, (b\notin\mathcal B_T) returns a nonnumeric inconsistency
status. This is an audit convention and specification diagnostic. It is not an
extra source of frequentist protection.

## 4. Sharp claim-risk envelope

For (b\in\mathcal B_T),

[
s_T^\star(b)
=
\sup_{D\in\mathcal V_T(b)}\rho_c(D).
]

Write

[
r(D)=(\rho_1(D),\ldots,\rho_m(D)).
]

For every (D\in\mathcal W_c), (r(D)\in\mathcal B_T) because
(D\in\mathcal V_T(r(D))).

## 5. Feasible-domain warrant

A function

[
h:\mathcal B_T\to[0,1]
]

is a feasible-domain monotone warrant when:

1. (h) is coordinatewise nondecreasing on (mathcal B_T);
2. for every (D\in\mathcal W_c),
   [
   \rho_c(D)\le h(r(D)).
   ]

### Proposition

The sharp envelope (s_T^\star) is the pointwise least feasible-domain
monotone warrant.

### Proof

First, (mathcal B_T) is upward closed. If (b\le b'), then
[
\mathcal V_T(b)\subseteq\mathcal V_T(b'),
]
so
[
s_T^\star(b)\le s_T^\star(b').
]

Second, (s_T^\star) is itself a feasible-domain warrant because for every
(D\in\mathcal W_c),

[
\rho_c(D)
\le
\sup_{D'\in\mathcal V_T(r(D))}\rho_c(D')
=
s_T^\star(r(D)).
]

Third, let (h) be any feasible-domain monotone warrant and fix
(b\in\mathcal B_T). For every (D\in\mathcal V_T(b)),
(r(D)\le b), hence

[
\rho_c(D)
\le
h(r(D))
\le
h(b).
]

Taking the supremum over (D\in\mathcal V_T(b)) gives

[
s_T^\star(b)\le h(b).
]

Thus (s_T^\star) belongs to the comparison class and is its least element.

This proposition is elementary and is not claimed as a new extremal theorem.

## 6. Conservative computable upper bound

A practical function (widehat s_T) may replace exact optimization if it has
a certified guarantee

[
\widehat s_T(b)\ge s_T^\star(b)
qquad
\forall b\in\mathcal B_T.
]

A local optimizer value without a global upper-bound certificate does not
justify promotion.

## 7. Feasibility is diagnostic, not the source of soundness

For fixed (D\in\mathcal W_c), on simultaneous certificate-validity events,

[
\rho_i(D)\le B_i(Z)
qquad \forall i.
]

Therefore (D\in\mathcal V_T(B(Z))), so the realized vector is feasible.

Consequently, under the declared model, infeasibility can occur only when at
least one certificate validity event fails. The explicit feasibility branch is
still operationally useful because it exposes inconsistent realized bounds or
model misspecification rather than silently converting an empty set into a
favorable number.

## 8. Unsafe-promotion control

For a fixed, pre-specified claim and measurable promotion rule, if promotion
requires

[
\widehat s_T(B(Z))\le\delta_c,
]

then for every unsafe (D\in\mathcal W_c) with
(ho_c(D)>\delta_c),

[
\Pr_D(\mathrm{PROMOTE})
\le
\min\left(1,\sum_i\alpha_i\right).
]

No independence is required.

If claims or warrants are selected after observing the same data, this
fixed-claim statement is insufficient; selection must be covered by a separate
family-wise or otherwise valid correction.

## 9. Novelty boundary

None of the following is claimed as new:

- compatible-model sets;
- sharp identified-set extrema;
- union-bound confidence accounting;
- high-confidence risk control;
- abstention/refusal;
- assume/guarantee reasoning;
- transportability;
- proxy-evidence world/fiber reasoning.

The current research question is only whether the explicit ML audit ordering
(target, scope, feasibility, warrant, confidence) is useful enough to merit a
methodology/application paper once it is instantiated on real evidence.

Status:

**MATHEMATICALLY REPAIRED / SCIENTIFIC SIGNIFICANCE UNRESOLVED / SUBMISSION HOLD**
