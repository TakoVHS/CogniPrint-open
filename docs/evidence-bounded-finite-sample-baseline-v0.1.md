# Finite-Sample Selective-Risk Certificates — Baseline v0.1

Status: **THEORY_BASELINE / KNOWN_STATISTICAL_PRINCIPLE / NOT_A_NOVELTY_CLAIM**

Related theory PR: #84

This note turns the population discussion in Evidence-Bounded Inference into an
operational finite-sample certificate. The construction is deliberately
positioned as a **baseline**: held-out risk control is an active and established
research area, including risk-controlling prediction sets, Learn-then-Test,
Conformal Risk Control, selective conformal risk control, and recent
selection-conditioned risk-control methods.

## 1. Why not estimate the pointwise epsilon directly?

The population theorem in the theory note assumes

\[
\operatorname*{ess\,sup}_x |c(x)-q(x)|\le\epsilon.
\]

A finite i.i.d. calibration sample does not, without additional regularity
assumptions, identify this pointwise supremum over arbitrary \(x\).

Therefore this baseline does **not** estimate that \(\epsilon\), and it does
not use ECE as a substitute.

Instead, it certifies the quantity that matters for abstention directly:

\[
R_{\mathrm{sel}}(g)
=
\Pr(h(X)\neq Y\mid g(X)=1).
\]

## 2. Fixed-threshold finite-sample certificate

Assume:

1. the predictor \(h\), confidence score \(c\), and threshold \(\tau\)
   are fixed independently of the calibration labels;
2. \((X_i,Y_i)_{i=1}^N\) are i.i.d. from the deployment distribution;
3. \(g_\tau(x)=\mathbf 1\{c(x)\ge\tau\}\).

Let

\[
N_\tau
=
\sum_{i=1}^N g_\tau(X_i)
\]

be the number of accepted calibration observations and

\[
E_\tau
=
\sum_{i=1}^N
g_\tau(X_i)\mathbf 1\{h(X_i)\neq Y_i\}
\]

the number of accepted errors.

Conditional on \(N_\tau=n>0\),

\[
E_\tau
\sim
\operatorname{Binomial}(n,R_{\mathrm{sel}}(g_\tau)).
\]

Let \(U_{\mathrm{CP}}(e,n;\alpha)\) be the one-sided
Clopper--Pearson upper confidence limit. Then

\[
\Pr\left(
R_{\mathrm{sel}}(g_\tau)
\le
U_{\mathrm{CP}}(E_\tau,N_\tau;\alpha)
\right)
\ge
1-\alpha.
\]

This is an exact binomial confidence statement, not a new CogniPrint theorem.

For zero accepted errors,

\[
U_{\mathrm{CP}}(0,n;\alpha)
=
1-\alpha^{1/n}.
\]

This makes the sample-size cost of strong claims explicit: zero observed errors
do not imply zero population risk.

## 3. Finite predeclared threshold grid

Let

\[
\mathcal T=\{\tau_1,\dots,\tau_m\}
\]

be fixed **before observing calibration labels**.

For each threshold, construct

\[
U_j
=
U_{\mathrm{CP}}
\left(
E_{\tau_j},
N_{\tau_j};
\frac{\alpha}{m}
\right).
\]

By the union bound,

\[
\Pr\left(
\forall j\in\{1,\dots,m\}:
R_{\mathrm{sel}}(g_{\tau_j})\le U_j
\right)
\ge
1-\alpha.
\]

Therefore, after calibration data are observed, any data-dependent selector
\(\hat j\) choosing among this **predeclared finite grid** inherits

\[
R_{\mathrm{sel}}(g_{\tau_{\hat j}})
\le U_{\hat j}
\]

on the same simultaneous high-probability event.

A practical selector may choose the threshold with largest empirical retention
subject to

\[
U_j\le\delta.
\]

## 4. Evidence-Bounded claim certificate

For a selected threshold, define

\[
s_{\mathrm{FS}}
=
1-U_j.
\]

Then, on the simultaneous confidence event,

\[
\Pr(h(X)=Y\mid g_{\tau_j}(X)=1)
\ge
s_{\mathrm{FS}}.
\]

This is a finite-sample, auditable meaning for "claim strength":

- it is a lower confidence bound on correctness among accepted predictions;
- it has an explicit confidence level;
- it can fail to certify anything when accepted sample support is too small;
- it does not imply OOD or false-known control.

## 5. What this does NOT solve

This baseline does not provide:

- pointwise calibration guarantees;
- distribution-free conditional validity for every input;
- false-known control for arbitrary unknown distributions;
- protection against distribution shift;
- validity if the model or threshold grid is tuned on the same labels without
  accounting for that adaptivity;
- novelty relative to modern risk-control literature.

## 6. Literature collision / prior art

The finite-sample risk-control layer must be treated as prior-art territory.

Relevant lines include:

- Clopper & Pearson (1934): exact binomial confidence limits;
- Bates et al. (2021): distribution-free risk-controlling prediction sets;
- Learn-then-Test: held-out calibration with high-probability risk control;
- Angelopoulos et al. (2024): Conformal Risk Control;
- Xu, Guo & Wei (2025): Selective Conformal Risk Control;
- Wang et al. (ICML 2026): LEC, finite-sample selection-conditioned risk
  control from a held-out calibration set;
- Aldirawi, Li & Guo (2026): finite-sample CRC over non-monotone finite grids.

Therefore CogniPrint should not claim novelty for "using a held-out calibration
set to select a safe threshold".

## 7. Where potential novelty may still exist

The stronger research question is not "can selective risk be controlled?"

It is:

> How should multiple statistically different evidence certificates be mapped
> into an auditable hierarchy of admissible claims, especially when
> open-world/unknown inputs make some claims structurally uncertifiable?

Candidate directions:

1. a formal claim lattice combining EvidenceClass and ClaimLevel;
2. composition rules for multiple certificates with different failure modes;
3. open-world claim admissibility under explicit families of unknown shifts;
4. impossibility theorems for promotion from closed-set risk control to
   provenance/attribution claims;
5. finite-sample claim-admissibility under jointly controlled selective risk
   and false-known risk.

These remain research questions, not established results.

## 8. Implementation

Implemented in:

- `src/cogniprint/stats/evidence_bounded.py`
- `tests/test_evidence_bounded.py`

Functions:

- `clopper_pearson_upper`
- `fixed_threshold_risk_certificate`
- `simultaneous_threshold_certificates`
- `select_max_coverage_certified_threshold`

No exposed RAID Stage A record is retrained or retuned by this implementation.
