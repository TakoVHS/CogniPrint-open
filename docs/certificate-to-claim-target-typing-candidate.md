# Certificate Scope Judgment — Formalization v0.1

Status: **CANDIDATE FORMAL INTERFACE / HIGH COLLISION RISK / NOVELTY UNESTABLISHED**

This note turns the three surviving research gaps into mathematically sound
propositions. The propositions themselves are deliberately separated from any
novelty claim.

## 1. Statistical certificate semantics

A certificate procedure is typed by

\[
\tau(\kappa)
=
(E,\mathcal W_\kappa^A,\rho_\kappa,\alpha_\kappa),
\]

and, after observing validation data \(Z=z\), emits an upper bound

\[
B_\kappa(z)\in[0,1].
\]

Here:

- \(E\) is the evidence scope/channel;
- \(\mathcal W_\kappa^A\) is the population/world class on which all declared
  assumptions \(A\) hold;
- \(\rho_\kappa:\mathcal W_\kappa^A\to[0,1]\) is the exact certified risk
  functional;
- \(\alpha_\kappa\) is the certificate failure budget.

### Definition 1.1 — Uniform upper-certificate validity

The certificate is valid when

\[
\inf_{D\in\mathcal W_\kappa^A}
\Pr_D\!\left[
\rho_\kappa(D)\le B_\kappa(Z)
\right]
\ge
1-\alpha_\kappa.
\]

This is a frequentist coverage statement. It is **not** interpreted as a
posterior probability that all worlds are safe conditional on the observed
data.

## 2. Claim type

A downstream claim specification is

\[
\tau(c)
=
(C,\mathcal W_c,\rho_c,\delta_c),
\]

where:

- \(C\) is the semantic proposition;
- \(\mathcal W_c\) is the claim deployment/world class;
- \(\rho_c:\mathcal W_c\to[0,1]\) is the risk of asserting the claim;
- \(\delta_c\) is its tolerated risk.

### Definition 2.1 — Direct static compatibility

A certificate and claim are directly type-compatible when

\[
\mathcal W_c\subseteq\mathcal W_\kappa^A
\]

and

\[
\rho_c(D)=\rho_\kappa(D)
\quad
\forall D\in\mathcal W_c.
\]

The numerical condition

\[
B_\kappa(z)\le\delta_c
\]

is a **runtime discharge condition**, not part of static type compatibility.

This distinction prevents a random data-dependent bound from being confused
with a static type.

## 3. Proposition — Direct Typed Promotion Soundness

Assume direct static compatibility and uniform upper-certificate validity.
Define

\[
\operatorname{Promote}_{\kappa\to c}(z)
=
\mathbf 1\{B_\kappa(z)\le\delta_c\}.
\]

Then for every unsafe claim world

\[
D\in\mathcal W_c
\quad\text{with}\quad
\rho_c(D)>\delta_c,
\]

we have

\[
\boxed{
\Pr_D(
\operatorname{Promote}_{\kappa\to c}(Z)=1
)
\le
\alpha_\kappa.
}
\]

Equivalently,

\[
\sup_{\substack{D\in\mathcal W_c\\ \rho_c(D)>\delta_c}}
\Pr_D(\operatorname{Promote}=1)
\le
\alpha_\kappa.
\]

### Proof

For an unsafe \(D\), direct compatibility gives

\[
\rho_\kappa(D)=\rho_c(D)>\delta_c.
\]

If both the certificate-validity event

\[
\rho_\kappa(D)\le B_\kappa(Z)
\]

and promotion event

\[
B_\kappa(Z)\le\delta_c
\]

held, we would obtain the contradiction

\[
\rho_\kappa(D)\le\delta_c<\rho_\kappa(D).
\]

Therefore promotion in an unsafe world can occur only when the certificate
coverage event fails. Its probability is at most \(\alpha_\kappa\).
\(\square\)

### Status

This proposition is a soundness rule for the proposed interface. Its proof is a
direct consequence of frequentist coverage plus target equality. It is **not
claimed as a new statistical theorem**.

## 4. Target mismatch and explicit warrants

Direct equality of targets is intentionally strict.

For a mismatched certificate/claim pair, promotion requires an explicit warrant

\[
T:
\left[
\rho_\kappa(D)\le b
\right]
\Longrightarrow
\left[
\rho_c(D)\le\delta_c
\right]
\]

for every \(D\) in the claim world class covered by the certificate.

A warrant can come from:

- logical implication;
- an identification result;
- a transport theorem;
- a validated auxiliary evidence channel;
- a mechanistic provenance condition.

Without such a warrant, a low bound on one risk target must not be upcast to a
different semantic claim.

## 5. Definition — Non-promotion witness

For a realized bound \(b\), define the certificate-compatible claim worlds

\[
\mathcal V_{\kappa,c}(b)
=
\left\{
D\in
\mathcal W_c\cap\mathcal W_\kappa^A:
\rho_\kappa(D)\le b
\right\}.
\]

A non-promotion witness is a world

\[
D^\star\in\mathcal V_{\kappa,c}(b)
\]

such that

\[
\rho_c(D^\star)>\delta_c.
\]

The important point is that the statistical certificate remains valid in the
witness world while the stronger or different downstream claim is unsafe.

## 6. Proposition — Witness Existence Characterization

Assume \(\mathcal V_{\kappa,c}(b)\neq\varnothing\). Then a non-promotion witness
exists iff

\[
\boxed{
\sup_{D\in\mathcal V_{\kappa,c}(b)}
\rho_c(D)
>
\delta_c.
}
\]

### Proof

If a witness \(D^\star\) exists, then the supremum is at least
\(\rho_c(D^\star)>\delta_c\).

Conversely, if the supremum is strictly larger than \(\delta_c\), it cannot be
the case that every \(D\in\mathcal V_{\kappa,c}(b)\) satisfies
\(\rho_c(D)\le\delta_c\); otherwise the supremum would be at most
\(\delta_c\). Hence at least one \(D^\star\) has
\(\rho_c(D^\star)>\delta_c\). \(\square\)

### Important limitation

This is an **existence characterization**, not yet a constructive algorithm.

Construction is immediate for finite world classes by enumeration. For convex,
moment-constrained, or otherwise parameterized world classes, producing
\(D^\star\) requires an optimization/separation procedure and appropriate
regularity or computability assumptions.

The proposition itself is closely related to countermodels, robust
optimization adversaries, and partial-identification extremizers. Novelty is
not claimed for the existential equivalence.

## 7. Proposition — Same-Target Confidence-Budget Composition

Let two certificates \(\kappa_1,\kappa_2\) be valid on a common world class
\(\mathcal W_{12}\) for the **same** risk functional \(\rho\):

\[
\Pr_D[\rho(D)\le B_i(Z)]\ge1-\alpha_i,
\qquad i\in\{1,2\},
\]

for every \(D\in\mathcal W_{12}\).

Then

\[
\boxed{
\Pr_D[
\rho(D)\le\min\{B_1(Z),B_2(Z)\}
]
\ge
1-(\alpha_1+\alpha_2)
}
\]

for every \(D\in\mathcal W_{12}\), truncated at zero if the displayed lower
confidence level becomes negative.

### Proof

On the intersection of the two certificate-validity events,

\[
\rho(D)\le B_1(Z)
\quad\text{and}\quad
\rho(D)\le B_2(Z),
\]

so

\[
\rho(D)\le\min(B_1(Z),B_2(Z)).
\]

By the union bound, the probability that at least one validity event fails is
at most \(\alpha_1+\alpha_2\). No independence assumption is required.
\(\square\)

### What this does not imply

There is no universal theorem that composition yields a strictly smaller bound,
or an additional

\[
O\!\left(\sqrt{\log(1/\alpha)/n}\right)
\]

improvement.

The realized minimum can equal one input bound exactly. Stronger combination
rules require additional statistical structure, for example independent
likelihoods, a joint model, confidence-distribution machinery, or another
validated fusion procedure.

Therefore the proposed generic Composition Bound with an automatic
\(n^{-1/2}\) gain is **rejected**.

## 8. Proposition — Warranted Heterogeneous Composition Soundness

Let \(\kappa_1,\dots,\kappa_m\) certify possibly different targets
\(\rho_1,\dots,\rho_m\), with failure budgets
\(\alpha_1,\dots,\alpha_m\).

Suppose the common claim scope is covered by every certificate, and for the
realized bounds \(b_1,\dots,b_m\) there is an explicit warrant satisfying

\[
\forall D\in\mathcal W_c:
\left[
\bigwedge_{i=1}^{m}\rho_i(D)\le b_i
\right]
\Longrightarrow
\rho_c(D)\le\delta_c.
\]

Then promoting claim \(c\) on the basis of that warrant has unsafe-promotion
probability at most

\[
\boxed{
\sum_{i=1}^{m}\alpha_i
}
\]

for every \(D\in\mathcal W_c\).

### Proof sketch

Whenever all certificate-validity events hold, the warrant implies the claim
risk is within tolerance. Therefore an unsafe promotion requires at least one
certificate-validity event to fail. Apply the union bound. \(\square\)

This is the confidence-budget bookkeeping rule needed by the candidate type
interface. The probability algebra is standard; the candidate research object
is the explicit typing of targets, scopes, warrants, and downstream semantic
claims.

## 9. Certificate Scope Judgment

Working notation:

\[
\boxed{
\kappa_1,\dots,\kappa_m
\vdash_T
c
}
\]

means that:

1. population/world scopes are compatible;
2. every certificate statistical validity statement is well typed;
3. the confidence budget is accounted for;
4. an explicit warrant \(T\) maps the certified target statements to the claim
   target;
5. no unresolved counterworld witness exists within the declared world class.

Possible outputs are:

- DIRECT: same target and scope; direct soundness rule applies;
- WARRANTED: target mismatch bridged by an explicit verified warrant;
- REJECT_WITH_WITNESS: a compatible unsafe world is available;
- UNRESOLVED: neither a warrant nor a witness has been established.

## 10. Novelty boundary after prior-art review

### Belief Hoare Logic / StatWhy

Belief Hoare Logic already provides a sound program logic for reasoning about
statistical beliefs produced by hypothesis tests, with explicit preconditions
and rules for multiple tests. StatWhy operationalizes this idea: statistical
programs are annotated with method requirements and interpretations, and the
tool checks whether the required assumptions have been specified.

This is a **direct collision** with any broad claim that CogniPrint invents
formal typing or verification of statistical inference requirements.

### Assurance 2.0 / SACM / Isabelle-SACM

Assurance frameworks already distinguish claims, evidence, assumptions, and
inferential links. Assurance 2.0 explicitly separates statistical evidence
incorporation from the reasoning step that justifies a higher-level claim.
Isabelle/SACM supports machine-checked assurance structures integrating
heterogeneous evidence.

This is a **direct collision** with any broad claim that CogniPrint invents
machine-checkable claim/evidence reasoning.

### Probabilistic programming semantics

Typed probabilistic programming languages and formally justified Bayesian
inference systems type programs, distributions, and inference transformations.
They do not, in the reviewed material, directly provide the specific
certificate-to-semantic-claim scope judgement proposed here, but they
substantially narrow any generic probabilistic type-system novelty claim.

### Confidence combination

There is an established literature on combining confidence distributions and
confidence procedures across sources. Therefore no novelty is claimed for
generic combination of confidence information or for the union-bound rule
above.

## 11. Surviving research question

The still-unresolved question is extremely narrow:

> Is there an existing formal system in which a frequentist statistical
> certificate is typed simultaneously by its target risk functional,
> population or domain, evidence scope, assumption set, and confidence budget,
> and the system checks whether that certificate may support a semantically
> distinct downstream claim, with a partial-identification counterworld as a
> rejection witness when the promotion is invalid?

This remains **NOVELTY UNESTABLISHED**.
