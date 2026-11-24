# Evidence-Bounded Inference — Mathematical Foundations v0.1

Status: **THEORY_DRAFT / NOT_PEER_REVIEWED / NO_STAGE_B_AUTHORIZATION**

Scientific readiness: **descriptive_only**

This document starts a separate mathematical theory track for CogniPrint.
It does **not** modify M1, M2, M2.1, Challenge 001, the research freeze, or the
external-review gate. It must not be used to retroactively reinterpret exposed
Stage A results.

## 1. Motivation

CogniPrint's empirical Stage A work exposed a recurring distinction:

> Probability is not permission to claim.

A predictor can emit a large score even when calibration is poor, a confidence
threshold can fail to preserve held-out risk, and a conformal prediction set can
be highly ambiguous without producing empty-set rejection for unknown inputs.

The purpose of Evidence-Bounded Inference (EBI) is to formalize the gap between:

1. a numerical score;
2. a probabilistic correctness statement;
3. an abstention rule;
4. an evidence-backed claim.

The theory track is intentionally narrower than a universal attribution theory.

## 2. Basic setup

Let \\(\mathcal X\\) be an observation space and
\\(\mathcal Y=\{1,\dots,K\}\\) the known label space. Let
\\(\mathcal Y^*=\mathcal Y\cup\{\bot\}\\), where \\(\bot\\)
denotes an unknown or unsupported class.

A predictor returns

\\[
p(x)=(p_1(x),\dots,p_K(x))\in\Delta^{K-1}.
\\]

Define the top-label predictor and confidence

\\[
h(x)=\arg\max_k p_k(x),\qquad c(x)=\max_k p_k(x).
\\]

An acceptance rule is \\(g:\mathcal X\to\{0,1\}\\). If
\\(g(x)=0\\), the system abstains and returns UNKNOWN.

### Definition 2.1 — Coverage

\\[
C(g)=\Pr(g(X)=1).
\\]

### Definition 2.2 — Selective risk

For \\(C(g)>0\\),

\\[
R_{\mathrm{sel}}(g)
=
\Pr(h(X)\neq Y\mid g(X)=1).
\\]

### Definition 2.3 — False-known risk

When \\(\Pr(Y=\bot)>0\\),

\\[
R_{\mathrm{FK}}(g)
=
\Pr(g(X)=1\mid Y=\bot).
\\]

Because the classifier's output space is \\(\mathcal Y\\), every accepted
unknown example is necessarily emitted as some known label.

### Definition 2.4 — Pointwise correctness probability

Let

\\[
q(x)=\Pr(Y=h(x)\mid X=x).
\\]

### Definition 2.5 — Uniform top-label calibration defect

A predictor has uniform top-label calibration defect at most
\\(\epsilon\\) when

\\[
\operatorname*{ess\,sup}_{x}
|c(x)-q(x)|\le\epsilon.
\\]

This is a **strong assumption**. It is not Expected Calibration Error (ECE).
ECE is an average, binned diagnostic and must not be substituted for this
uniform defect in a theorem that requires a pointwise bound.

## 3. Theorem 1 — selective-risk certificate under uniform calibration

For a threshold \\(\tau\in[0,1]\\), define

\\[
g_\tau(x)=\mathbf 1\{c(x)\ge\tau\}.
\\]

If the uniform calibration defect is at most \\(\epsilon\\) and
\\(C(g_\tau)>0\\), then

\\[
R_{\mathrm{sel}}(g_\tau)
\le
1-\tau+\epsilon.
\\]

### Proof

On the accepted region, \\(c(x)\ge\tau\\). Uniform calibration gives

\\[
q(x)\ge c(x)-\epsilon\ge\tau-\epsilon.
\\]

Therefore the conditional pointwise error probability is at most

\\[
1-q(x)\le1-\tau+\epsilon.
\\]

Taking the conditional expectation over the accepted region preserves the
bound:

\\[
R_{\mathrm{sel}}(g_\tau)
=
\mathbb E[1-q(X)\mid g_\tau(X)=1]
\le1-\tau+\epsilon.
\\]

\\(\square\\)

### Corollary 3.1 — threshold required for target risk

To certify \\(R_{\mathrm{sel}}\le\delta\\) using Theorem 1, it is
sufficient to choose

\\[
\tau\ge1-\delta+\epsilon.
\\]

If \\(1-\delta+\epsilon>1\\), this theorem alone cannot certify the
target risk at any confidence threshold. This is a limitation of the
certificate, **not** a proof that the model's actual risk must exceed
\\(\delta\\).

### Claim-strength interpretation

A defensible numerical "claim strength" for this theorem is not a subjective
scale from "nothing" to "proof". It is a **certified correctness lower bound**

\\[
s_{\mathrm{cert}}(\tau,\epsilon)
=
\max\{0,\tau-\epsilon\}.
\\]

This has a direct decision-theoretic meaning:

\\[
\Pr(Y=h(X)\mid g_\tau(X)=1)
\ge s_{\mathrm{cert}}.
\\]

## 4. Proposition 1 — coverage bound from mean confidence

Let \\(m=\mathbb E[c(X)]\\). For \\(0\le\tau<1\\),

\\[
C(g_\tau)
\ge
\max\left\{0,\frac{m-\tau}{1-\tau}\right\}.
\\]

### Proof

Let \\(C=C(g_\tau)\\). Because \\(c<\tau\\) on the rejected region
and \\(c\le1\\) everywhere,

\\[
m
=
\mathbb E[c]
\le
\tau(1-C)+C
=
\tau+(1-\tau)C.
\\]

Rearranging gives the result. \\(\square\\)

This replaces the incorrect Markov-based lower bound in the initial draft.

## 5. Theorem 2 — no distribution-free false-known guarantee for arbitrary unknowns

Let \\(g\\) be any fixed acceptance rule with non-empty acceptance region

\\[
A=\{x:g(x)=1\}\neq\varnothing.
\\]

Let \\(\mathcal Q_\bot\\) be the class of all possible distributions of
unknown inputs over \\(\mathcal X\\). Then

\\[
\sup_{Q\in\mathcal Q_\bot}
\Pr_{X\sim Q}(g(X)=1)
=
1.
\\]

Equivalently,

\\[
\sup_{Q\in\mathcal Q_\bot}R_{\mathrm{FK}}(g)=1.
\\]

### Proof

Choose any probability distribution \\(Q\\) supported entirely on the
non-empty set \\(A\\). Then \\(g(X)=1\\) almost surely under
\\(Q\\), so the false-known risk equals one. \\(\square\\)

### Consequence

A nontrivial open-world false-known guarantee requires **additional
assumptions or evidence about the unknown distribution**. Merely thresholding
closed-set confidence cannot provide a distribution-free guarantee.

This theorem does **not** imply that conformal prediction or energy scores
automatically solve OOD detection. They require their own validity assumptions
and evaluation.

The proposed inequality

\\[
R_{\mathrm{FK}}\ge\pi(1-\mathrm{ACC}_{\mathrm{closed}})
\\]

is rejected: there is no such universal relation without further assumptions.

## 6. Theorem 3 — what marginal conformal validity implies for singleton abstention

Suppose a conformal method returns a set
\\(\Gamma_\alpha(X)\subseteq\mathcal Y\\) satisfying marginal coverage

\\[
\Pr(Y\in\Gamma_\alpha(X))\ge1-\alpha.
\\]

Define singleton acceptance

\\[
A=\{|\Gamma_\alpha(X)|=1\},
\\]

and let

\\[
\kappa=\Pr(A).
\\]

When \\(\kappa>0\\), predict the unique element of
\\(\Gamma_\alpha(X)\\) on \\(A\\) and abstain otherwise. Then

\\[
R_{\mathrm{sel}}
\le
\min\left\{1,\frac{\alpha}{\kappa}\right\}.
\\]

### Proof

If a singleton prediction is accepted and wrong, then the true label is not in
the conformal set. Therefore

\\[
\Pr(\text{error}\cap A)
\le
\Pr(Y\notin\Gamma_\alpha(X))
\le\alpha.
\\]

Dividing by \\(\Pr(A)=\kappa\\) gives

\\[
R_{\mathrm{sel}}
=
\frac{\Pr(\text{error}\cap A)}{\kappa}
\le\frac{\alpha}{\kappa}.
\\]

\\(\square\\)

### Important limitation

Marginal conformal validity alone does **not** imply

\\[
R_{\mathrm{sel}}\le\alpha.
\\]

It also gives no positive lower bound on singleton coverage
\\(\kappa\\). A conformal method can have perfect marginal coverage while
always returning a multi-class set, yielding \\(\kappa=0\\).

This is directly relevant to CogniPrint M2.1, where near-zero false-known was
explained by multi-class ambiguity rather than empty-set OOD rejection.

### Unknown labels outside the conformal label space

If \\(\bot\notin\mathcal Y\\), the standard conformal coverage theorem
over \\(\mathcal Y\\) does not, by itself, guarantee empty-set rejection
or any particular false-known rate for \\(Y=\bot\\).

## 7. What is rejected from the initial draft

The following statements must not appear as CogniPrint theorems without new
assumptions:

1. \\(s^*\le1-\delta-\epsilon\\) as a universal maximum claim-strength
   theorem.
2. "If \\(\epsilon>1-\delta\\), every claim is inadmissible."
3. \\(R_{\mathrm{FK}}\ge\pi(1-\mathrm{ACC}_{\mathrm{closed}})\\)
   without assumptions connecting known and unknown distributions.
4. "Only conformal or energy-based methods can provide nontrivial OOD
   guarantees."
5. \\(R_{\mathrm{sel}}(g_{\mathrm{conf}})\le\alpha\\) from marginal
   conformal validity alone.
6. A positive singleton-coverage lower bound derived only from conformal
   marginal coverage and the empty-set rate.
7. ECE used as an estimator of the uniform \\(L_\infty\\) calibration
   defect.

## 8. Relationship to existing literature

This theory track must be positioned conservatively.

- Gneiting & Raftery (2007): proper scoring rules.
- Guo et al. (2017): post-hoc calibration and temperature scaling.
- Geifman & El-Yaniv (2017): selective classification and risk/coverage.
- Angelopoulos & Bates (2021/2023): distribution-free conformal prediction.
- Dabah & Tirer (2025): interaction between temperature scaling and conformal
  prediction.

Potential CogniPrint contribution is **not** "inventing abstention" or
"inventing risk/coverage". A defensible research question is whether a useful,
auditable claim-admissibility layer can be built by combining:

- calibrated or otherwise justified correctness certificates;
- explicit abstention;
- open-world false-known analysis;
- evidence-class and claim-level restrictions.

Novelty remains **UNESTABLISHED** until a literature review and external
mathematical critique are complete.

## 9. Empirical policy

The theory track must not use the already exposed Stage A 500-record benchmark
to select a new probability model, threshold, feature set, calibration range,
or OOD method and then call the result confirmatory.

Allowed now:

- exact algebraic unit tests;
- finite-space synthetic demonstrations;
- derivations from already-persisted M2/M2.1 outputs;
- literature review;
- independent mathematical review.

Future empirical validation should use prospectively frozen or sealed evidence.

## 10. Next mathematical targets

Candidate results worth pursuing:

1. finite-sample confidence bands for selective risk with a fixed acceptance
   rule;
2. claim-admissibility certificates under calibration uncertainty estimated
   from an independent calibration sample;
3. false-known control under an explicitly specified family of distribution
   shifts;
4. conditions under which conformal ambiguity can be converted into a valid
   abstention certificate;
5. impossibility results separating marginal validity, conditional validity,
   and OOD rejection.

These are research targets, not established CogniPrint results.
