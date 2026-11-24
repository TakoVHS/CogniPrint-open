# Canonical Least Warrant — Formalization v0.1

Status: **MATHEMATICAL CORE / NOVELTY NOT CLAIMED / FAIL-CLOSED OPERATIONAL SEMANTICS**

This note isolates the canonical quantitative object underlying heterogeneous
certificate-to-claim promotion. It does **not** claim a new probability theorem
or a new theory of partial identification. Its purpose is to make the current
CogniPrint interface mathematically canonical and to separate semantic
sharpness from tractable conservative approximations.

## 1. Static domain and feasible bound vectors

Let a downstream claim \(c\) have deployment scope \(\mathcal W_c\) and claim
risk \(\rho_c:\mathcal W_c\to[0,1]\). Let certificates
\(\kappa_1,\ldots,\kappa_m\) have valid world classes
\(\mathcal W_{\kappa_i}^A\) and risk functionals
\(\rho_i:\mathcal W_{\kappa_i}^A\to[0,1]\). Let
\(T\) declare an additional warrant scope \(\mathcal W_T\).

For conjunctive use of all certificates, define the common semantic domain

\[
\mathcal W
=
\mathcal W_c
\cap
\mathcal W_T
\cap
\bigcap_{i=1}^m \mathcal W_{\kappa_i}^A.
\]

Operational promotion additionally requires the fail-closed static coverage
condition

\[
\boxed{
\mathcal W_c
\subseteq
\mathcal W_T
\cap
\bigcap_{i=1}^m \mathcal W_{\kappa_i}^A.
}
\]

For a candidate vector of certificate upper bounds
\(b=(b_1,\ldots,b_m)\in[0,1]^m\), define the compatible world set

\[
\mathcal V_T(b)
=
\left\{
D\in\mathcal W:
\rho_i(D)\le b_i
\text{ for every }i
\right\}.
\]

Define the feasible-bound domain

\[
\mathcal B_T
=
\left\{
b\in[0,1]^m:
\mathcal V_T(b)\neq\varnothing
\right\}.
\]

The operational distinction between feasible and infeasible realized
constraints is deliberate. An empty compatible set is **not** interpreted as
evidence of safety.

## 2. Sharp claim-risk envelope

For \(b\in\mathcal B_T\), define

\[
\boxed{
s_T^\star(b)
=
\sup_{D\in\mathcal V_T(b)}
\rho_c(D).
}
\]

This is the sharp claim-risk envelope induced by the declared world model,
certificate targets, and realized upper-bound constraints.

For mathematical comparison with total warrant functions on \([0,1]^m\), it is
convenient to define the total extension

\[
\widetilde s_T^\star(b)
=
\begin{cases}
s_T^\star(b), & b\in\mathcal B_T,\\
0, & b\notin\mathcal B_T.
\end{cases}
\]

The value \(0\) on infeasible \(b\) is a mathematical extension only. A runtime
decision procedure must first check feasibility and return an unresolved
diagnostic when \(\mathcal V_T(b)=\varnothing\); it must not treat the extension
value as a safety certificate.

## 3. Theorem — Canonical Least Warrant

Assume \(\mathcal W\neq\varnothing\).

### (i) Coordinatewise monotonicity

If \(b\le b'\) coordinatewise, then

\[
\mathcal V_T(b)\subseteq\mathcal V_T(b').
\]

Therefore

\[
\boxed{
\widetilde s_T^\star(b)
\le
\widetilde s_T^\star(b').
}
\]

In particular, \(s_T^\star\) is coordinatewise nondecreasing on its feasible
domain.

### (ii) Pointwise minimality

Let \(g:[0,1]^m\to[0,1]\) be any coordinatewise nondecreasing quantitative
warrant satisfying

\[
\forall D\in\mathcal W:
\qquad
\rho_c(D)
\le
g\!\left(
\rho_1(D),\ldots,\rho_m(D)
\right).
\]

Then for every \(b\in[0,1]^m\),

\[
\boxed{
\widetilde s_T^\star(b)
\le
g(b).
}
\]

Hence \(\widetilde s_T^\star\) is the pointwise least total monotone warrant
compatible with the declared semantic model.

### Proof

For monotonicity, \(b\le b'\) implies every world satisfying
\(\rho_i(D)\le b_i\) also satisfies \(\rho_i(D)\le b_i'\), so
\(\mathcal V_T(b)\subseteq\mathcal V_T(b')\). Taking suprema of the same
claim-risk functional over nested feasible sets yields the desired inequality.
If the smaller set is empty, the total extension equals zero and the inequality
still holds.

For minimality, fix \(b\in\mathcal B_T\) and any
\(D\in\mathcal V_T(b)\). By the warrant property and coordinatewise
monotonicity,

\[
\rho_c(D)
\le
g(\rho_1(D),\ldots,\rho_m(D))
\le
g(b).
\]

Taking the supremum over \(D\in\mathcal V_T(b)\) gives

\[
s_T^\star(b)\le g(b).
\]

If \(b\notin\mathcal B_T\), then
\(\widetilde s_T^\star(b)=0\le g(b)\) because \(g\) is
\([0,1]\)-valued. \(\square\)

## 4. Corollary — Conservative computable warrants

Let \(\widehat s_T:[0,1]^m\to[0,1]\) be a computable function satisfying

\[
\widehat s_T(b)
\ge
\widetilde s_T^\star(b)
\qquad
\forall b\in[0,1]^m.
\]

Then, for every feasible \(b\),

\[
D\in\mathcal V_T(b)
\quad\Longrightarrow\quad
\rho_c(D)\le \widehat s_T(b).
\]

Thus \(\widehat s_T\) is a valid conservative envelope for runtime promotion.
If \(\widehat s_T\) is also coordinatewise nondecreasing, then it is a
quantitative warrant in the current effect-style definition.

This gives the intended hierarchy:

\[
\boxed{
\text{sharp envelope}
\;\le\;
\text{tractable conservative warrant}.
}
\]

The sharp envelope is the semantic optimum; a practical \(g_T\) is an upper
approximation chosen for tractability, closed form, optimization guarantees, or
machine verification.

## 5. Fail-closed operational rule

For realized certificate bounds \(b_i=B_i(z)\), the runtime sequence is:

1. verify static scope coverage;
2. check whether \(\mathcal V_T(b)\) is nonempty;
3. compute \(s_T^\star(b)\), or a certified conservative upper approximation;
4. compare the resulting claim-risk bound with \(\delta_c\);
5. separately discharge the confidence/failure-event budget.

The first two gates are semantic consistency checks. They are not replaced by a
small numerical risk bound.

A minimum diagnostic vocabulary should distinguish at least:

- \`SCOPE_GAP\`: the claim deployment scope is not covered by every certificate
  and the warrant scope required by the conjunctive rule;
- \`INCONSISTENT_ASSUMPTIONS\`: the declared model assumptions have no common
  admissible world;
- \`INCONSISTENT_BOUNDS\`: realized certificate constraints are incompatible with
  the declared model;
- \`EMPTY_IDENTIFIED_SET\`: no compatible world remains and the cause has not
  been refined further;
- \`NO_WARRANT_COMPUTED\`: a required optimization or proof procedure did not
  establish a bound;
- \`DEPENDENCE_UNKNOWN\`: a stronger composition rule requires dependence
  information that has not been justified.

These are unresolved verification states. They are not synonymous with either
safe or unsafe.

## 6. Relation to the current finite-world prototype

The existing function
\`sharp_finite_claim_bound_under_certificates()\` already computes the finite
enumeration analogue of \(s_T^\star(b)\). Its current behavior of returning
\`None\` when the compatible set is empty is intentionally fail closed.

For the finite-world prototype, exact computation is by enumeration. In
general world classes, computing or tightly approximating \(s_T^\star\) may
require optimization, separation, or identification machinery. No generic
polynomial-time claim is made.

## 7. Novelty boundary

This theorem is used as a canonicalization result for the CogniPrint
methodology, not as a novelty claim. Sharp identified sets, extremal envelopes,
robust optimization, and partial-identification reasoning have substantial
prior art.

The open research question is narrower: whether the surrounding
certificate-to-claim interface — combining explicit frequentist certificate
semantics, claim-specific deployment scope, heterogeneous risk targets,
fail-closed promotion, failure-event accounting, and AI-attribution
applications — provides a useful methodological abstraction beyond existing
formal and statistical frameworks.

Until the prior-art comparison is complete, status remains:

**NOVELTY UNESTABLISHED / HIGH COLLISION RISK.**
