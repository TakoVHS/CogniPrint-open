> **SUPERSEDED — 25 November 2026.** This development note is preserved for
> audit history. Its "least warrant" statement did not define the comparison
> class tightly enough for the sharp envelope itself to be a member. Use
> `docs/feasible-domain-claim-envelope-v0.2.md` and the current manuscript
> instead.

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
\boxed{
\mathcal B_T
=
\left\{
b\in[0,1]^m:
\mathcal V_T(b)\neq\varnothing
\right\}.
}
\]

The sharp numerical envelope below is defined only on \(\mathcal B_T\).
For \(b\notin\mathcal B_T\), the semantic result is the distinguished
non-numeric state \(\bot\) (infeasible / unresolved), not a numerical risk
bound.

This avoids a dangerous proof shortcut: no comparison such as
\(s_T^\star(b)\le\delta_c\) is even well formed until feasibility has been
established.

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

Operationally, we use the partial map

\[
\overline s_T(b)
=
\begin{cases}
s_T^\star(b), & b\in\mathcal B_T,\\
\bot, & b\notin\mathcal B_T.
\end{cases}
\]

The symbol \(\bot\) is not ordered against claim-risk thresholds. It forces a
diagnostic branch before any promotion comparison.

## 3. Theorem — Canonical Least Warrant

Assume \(\mathcal W\neq\varnothing\).

### (i) Coordinatewise monotonicity on the feasible domain

If \(b\in\mathcal B_T\) and \(b\le b'\) coordinatewise, then

\[
\mathcal V_T(b)\subseteq\mathcal V_T(b').
\]

Because \(\mathcal V_T(b)\neq\varnothing\), it follows automatically that
\(b'\in\mathcal B_T\). Therefore

\[
\boxed{
s_T^\star(b)
\le
s_T^\star(b').
}
\]

Thus \(s_T^\star\) is coordinatewise nondecreasing on its feasible-bound
domain.

### (ii) Pointwise minimality on the feasible domain

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

Then for every \(b\in\mathcal B_T\),

\[
\boxed{
s_T^\star(b)
\le
g(b).
}
\]

Hence \(s_T^\star\) is the pointwise least monotone numerical warrant on the
feasible-bound domain induced by the declared semantic model.

### Proof

For monotonicity, \(b\le b'\) implies every world satisfying
\(\rho_i(D)\le b_i\) also satisfies \(\rho_i(D)\le b_i'\), so
\(\mathcal V_T(b)\subseteq\mathcal V_T(b')\). Since the first set is nonempty,
so is the second. Taking suprema of the same claim-risk functional over nested
nonempty sets yields

\[
s_T^\star(b)\le s_T^\star(b').
\]

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
\qquad\square
\]

No claim is made about a numerical value of \(s_T^\star\) outside
\(\mathcal B_T\); there the operational result is \(\bot\).

## 4. Corollary — Conservative computable warrants

Let \(\widehat s_T\) be a computable numerical upper approximation defined on
the feasible-bound domain and satisfying

\[
\widehat s_T(b)
\ge
s_T^\star(b)
\qquad
\forall b\in\mathcal B_T.
\]

Then, for every \(b\in\mathcal B_T\),

\[
D\in\mathcal V_T(b)
\quad\Longrightarrow\quad
\rho_c(D)\le \widehat s_T(b).
\]

Thus \(\widehat s_T\) is a valid conservative envelope for runtime promotion
after feasibility has been established. If \(\widehat s_T\) is coordinatewise
nondecreasing on \(\mathcal B_T\), it is a tractable monotone warrant on the
feasible domain.

This gives the intended hierarchy:

\[
\boxed{
\text{sharp envelope}
\;\le\;
\text{tractable conservative warrant}
\qquad
\text{on }\mathcal B_T.
}
\]

The sharp envelope is the semantic optimum; a practical \(g_T\) or
\(\widehat s_T\) is an upper approximation chosen for tractability, closed
form, optimization guarantees, or machine verification.

## 5. Fail-closed operational rule

For realized certificate bounds \(b_i=B_i(z)\), the runtime sequence is:

1. verify static scope coverage;
2. check whether \(\mathcal V_T(b)\) is nonempty;
3. if it is empty, return an unresolved diagnostic and stop;
4. otherwise compute \(s_T^\star(b)\), or a certified conservative upper
   approximation;
5. compare the resulting claim-risk bound with \(\delta_c\);
6. separately discharge the confidence/failure-event budget.

The first two gates are semantic consistency checks. They are not replaced by a
small numerical risk bound.

A minimum diagnostic vocabulary should distinguish at least:

- \`SCOPE_GAP\`: the claim deployment scope is not covered by every certificate
  and the warrant scope required by the conjunctive rule;
- \`INCONSISTENT_ASSUMPTIONS\`: the declared model assumptions have no common
  admissible world;
- \`INCONSISTENT_BOUNDS\`: realized certificate constraints are incompatible
  with the declared model;
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
\`None\` when the compatible set is empty is intentionally fail closed and
matches the \(\bot\) branch above.

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
