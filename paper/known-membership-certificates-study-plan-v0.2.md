# Known-Membership Certificates for Open-Set AI-Text Attribution — Study Plan v0.2

Status: **CANDIDATE REDESIGN / DEVELOPMENT VIABILITY SCREEN NEGATIVE / REDESIGN REQUIRED / NO CONFIRMATORY DATA ACCESSED**

Development update (25 November 2026): the first real RAID Stage-A screen with
word 1--2 TF-IDF + multinomial logistic regression did **not** produce
meaningful certificate lift over the accept-all reference at useful certified
known coverage. See
`paper/known-membership-raid-dev-result-v0.1.md`.

This blocks freezing the current confirmatory design. The result may motivate a
scientific redesign after human review, but it must not trigger iterative
threshold/calibrator/model fishing on the exposed RAID outcome.

Date: 25 November 2026

Human methodological-review gate: `0/1`

Current 12D Challenge 001: `HOLD / REDESIGN REQUIRED`

This plan is a prospective replacement direction for the current
interface-first manuscript. It does **not** authorize Stage B, does not freeze a
confirmatory corpus, and does not permit looking at confirmatory labels or
results before the human-review gate and a separate Research Lock.

## 1. Primary scientific question

The primary claim is **known-set membership**, not exact family identity.

Let a deployed gate output `KNOWN` when a classifier score exceeds a fixed
threshold. The target risk is

$$
R(\tau) = P(Y \in U \mid A_\tau = 1),
$$

where $U$ denotes the declared unknown-generator population and
$A_\tau$ is the event that the gate accepts the text as belonging to the known
set.

The paper asks:

> Given finite held-out certificate samples and an explicit upper bound
> $\pi_U$ on unknown prevalence, when can we certify
> $R(\tau) \le \delta$ with confidence at least $1-\alpha$?

Primary tolerance:

$$
\delta = 0.10.
$$

The study reports the prevalence values and operating points for which the
certificate is nonvacuous. No result direction is predeclared as "publishable";
positive, negative, and mixed outcomes are all reported.

### Important non-claim

The formula below does **not** certify the stronger statement
"this text came from known family $k$." Exact-family attribution additionally
requires control of wrong-known-family classification error. The primary paper
therefore uses the narrower claim "the accepted text belongs to the declared
known set."

### Scope of "unknown" in the primary claim

In the primary certificate, $U$ is a finite list of **named, held-out**
families. The primary claim is therefore closed-world in substance: "the
accepted text is not from the listed held-out families." It says nothing about
generators outside that list. The open-world question (future, unlisted
generators) is addressed only by the transport stress test in Section 5, and
the paper must state this in the claim itself, not only in the limitations.

## 2. Gate and detector

Primary detector:

- word 1--2 TF-IDF + multinomial logistic regression.

Secondary detector:

- character 3--5 TF-IDF + multinomial logistic regression.

Optional reference:

- one predeclared small fine-tuned encoder only if compute, licensing, and
  implementation are fixed before confirmatory evaluation.

CogniPrint 12D is descriptive appendix material only.

For classifier score vector $p(x)$, define

$$
A_\tau(x) = \mathbf{1}\{\max_k p_k(x) \ge \tau\}.
$$

The threshold grid $\mathcal T$ is fixed using development data only before
any confirmatory certificate sample is evaluated.

The finite-sample certificate does **not** require $p_k(x)$ to be a perfectly
calibrated probability. It requires a fixed gate whose acceptance frequencies
can be bounded on independent certificate data. NLL, Brier, and ECE are
reported as probability-quality diagnostics rather than as assumptions needed
for the Clopper--Pearson acceptance-rate guarantee.

If a probability calibration method is used, its form and regularization are
fixed prospectively and fitted on a calibration split disjoint from certificate
and test data.

## 3. Family-robust finite-sample certificate

For known family $j$, let

$$
a_{K,j}(\tau) = P(A_\tau = 1 \mid Y = j).
$$

For declared unknown family $u$, let

$$
a_{U,u}(\tau) = P(A_\tau = 1 \mid Y = u).
$$

To avoid silently assuming a favorable mixture of known or unknown families,
the robust finite-scope quantities are

$$
a_K^{\min}(\tau) = \min_j a_{K,j}(\tau), \qquad a_U^{\max}(\tau) = \max_u a_{U,u}(\tau).
$$

Construct simultaneous one-sided exact binomial bounds

$$
a_{K,j}(\tau) \ge L_{K,j}(\tau), \qquad a_{U,u}(\tau) \le U_{U,u}(\tau)
$$

for every predeclared threshold and family stratum.

Then define

$$
L_K(\tau) = \min_j L_{K,j}(\tau), \qquad U_U(\tau) = \max_u U_{U,u}(\tau).
$$

The multiplicity allocation must cover the entire set of bounds used by the
primary claim, including thresholds and family strata. A simple baseline is
Bonferroni over all one-sided bounds. A less conservative alternative may be
used only if prospectively specified and formally justified before confirmatory
evaluation.

Given deployment unknown prevalence

$$
\pi \le \pi_U,
$$

the finite-scope membership-risk certificate is

$$
\boxed{B_\tau(\pi_U) = \frac{\pi_U\, U_U(\tau)}{(1-\pi_U)\, L_K(\tau) + \pi_U\, U_U(\tau)}}
$$

whenever the denominator is positive.

The gate can certify the known-membership claim only when

$$
B_\tau(\pi_U) \le \delta.
$$

The corresponding break-even prevalence is

$$
\boxed{\pi_\tau^\star = \frac{\delta\, L_K(\tau)}{U_U(\tau)(1-\delta) + \delta\, L_K(\tau)}}
$$

for the nondegenerate case. Edge cases remain explicitly nonnumeric when the
accepted population is undefined.

## 4. Threshold selection

Because simultaneous bounds are constructed for the complete predeclared
threshold family, the study may inspect all certified operating points after
the certificate counts are observed without invalidating the simultaneous
coverage statement.

### Mandatory accept-all reference

The threshold family must include $\tau = 0$ (accept every text), with
$L_K = U_U = 1$. Its risk is exactly the prevalence and its break-even is
exactly the tolerance:

$$
B_0(\pi_U) = \pi_U, \qquad \pi_0^\star = \delta .
$$

Consequently, **every $\pi_U \le \delta$ is certified without any
detector**. A `PROMOTE` in that region carries no information about the
detector. Even a gate that accepts every unknown ($U_U = 1$) is certified at
$\pi_U = 0.05$ when $L_K \ge 0.6$ ($B \approx 0.081$). See
`scripts/known_membership_break_even.py`.

### Primary selection rule

1. retain thresholds with $\tau > 0$ satisfying
   $B_\tau(\pi_U) \le \delta$ **and** $B_\tau(\pi_U) < \pi_U$, i.e.
   strictly better than accepting everything;
2. among them, report the threshold with the largest certified known-family
   acceptance lower bound $L_K(\tau)$;
3. if none pass, return `ABSTAIN`; if only $\tau = 0$ passes, return
   `PROMOTE_TRIVIAL` and report it as no detector evidence.

All thresholds are published regardless of which one is selected.

This replaces the ambiguous earlier combination of a separate threshold split
and post-hoc "best threshold" selection.

## 5. What the certificate does and does not transport

The exact binomial certificate controls sampling uncertainty for the
**predeclared finite family scope actually evaluated**.

It does not prove that a held-out generator family represents arbitrary future
generators.

Therefore the confirmatory paper separates:

### Primary finite-scope claim

A simultaneous certificate over the explicitly named known and unknown family
sets in the confirmatory design.

### Secondary transport stress test

Use development-only unknown families to construct a bound and then compare it
with observed acceptance on prospectively held-out confirmatory families.

This is a stress test of transport, not a guarantee for future unseen models.

A failure of the stress test is a scientific result and must not be repaired by
post-hoc widening of the world class.

## 6. Data firewall

### Development

RAID may be used for development because it is already exposed.

Permitted uses:

- implementation;
- runtime checks;
- prompt/source lineage logic;
- candidate threshold-grid construction;
- sample-size simulation;
- debugging.

RAID results are never called confirmatory.

### Confirmatory candidate

A second multi-generator corpus is selected **before** Research Lock.

Verified candidate metadata as of 25 November 2026:

- M4: EACL 2024 resource paper; multi-generator, multi-domain,
  multi-lingual benchmark.
- MAGE: ACL 2024; large multi-generator/multi-domain dataset; public project
  metadata reports an Apache-2.0 license.

No confirmatory rows, labels, family-level outcomes, or detector results may be
inspected before the human-review gate and final freeze.

Dataset license, family definitions, prompt/source identifiers, duplicate
structure, and contamination risks must be audited before selection.

## 7. Blinding and custody

A public dataset is **not automatically sealed** merely because the experiment
script hides labels.

For a confirmatory run to be treated as blinded:

1. an independent human custodian/evaluator holds the label/family manifest;
2. the research-facing package uses opaque record IDs and strips family labels;
3. all prediction files are frozen and hashed before label reveal;
4. the evaluator executes the scoring/certificate step or releases labels only
   after verifying the prediction hash;
5. no text-hash lookup or public-dataset reverse identification is permitted;
6. the complete custody log is published.

Merely asking another person to hash a prediction file is insufficient if the
researcher still has access to labels.

If independent custody cannot be obtained, the evaluation may still be useful,
but it must be called prospective/locked rather than sealed or independently
blinded.

## 8. Split structure

Within development and any training portion of the future confirmatory design,
group by source prompt / source instance so sibling generations cannot cross
roles.

Roles are:

- train;
- probability calibration, only if used;
- certificate;
- final test/transport stress-test.

The primary certificate must not reuse its own counts for model fitting.

The need for a separate threshold split is removed when the threshold family is
predeclared and simultaneously covered.

## 9. Sample-size design

Sample size is chosen prospectively from the certificate target rather than
from a generic "500 per family" rule.

For zero unknown acceptances and a one-sided tail allocation $\eta$,

$$
U_U \approx -\frac{\log \eta}{n}.
$$

But the required $U_U$ depends on $\pi_U, \delta$, and the expected
known-acceptance lower bound. Rearranging the certificate gives the target

$$
U_U \le \frac{\delta (1-\pi_U) L_K}{\pi_U (1-\delta)}.
$$

Before freeze, compute required $n$ over the full predeclared prevalence and
coverage grid, including the actual multiplicity allocation over thresholds
and family strata.

If feasible sample sizes cannot make the certificate informative, the study is
stopped before confirmatory data are touched.

Reference numbers from `scripts/known_membership_break_even.py` (defaults:
$\delta = 0.10$, $\alpha = 0.05$, 10 thresholds, 5 known and 3 unknown
strata, so 80 one-sided bounds). These are lower limits, assuming zero
accepted unknowns:

| $\pi_U$ | $L_K$ | $U_U$ needed | min. $n$ per unknown family |
| --- | --- | --- | --- |
| 0.20 | 0.6 | 0.267 | 24 |
| 0.30 | 0.6 | 0.156 | 44 |
| 0.50 | 0.6 | 0.067 | 107 |
| 0.50 | 0.3 | 0.033 | 218 |

At an M2-like operating point (known acceptance about 0.6, unknown acceptance
about 0.5) the lift is only about 1.18 even with exact rates, so a detector of
that quality would barely beat the accept-all gate. This is a development
observation from exposed data and must not be used to tune the confirmatory
design.

## 10. Predeclared prevalence and reporting grid

Initial candidate grid, subject to human review before freeze. Because every
$\pi_U \le \delta$ is certified by the accept-all gate (Section 4), the
informative grid lies above $\delta$:

$$
\pi_U \in \{0.10, 0.20, 0.30, 0.50\}, \qquad \delta = 0.10 .
$$

A secondary low-prevalence analysis may use a proportionally stricter
tolerance, e.g. $\delta = 0.02$ with $\pi_U \in \{0.05, 0.10\}$, fixed
before freeze.

Primary output:

- **detector lift** $\pi_\tau^\star / \delta$ (break-even relative to the
  accept-all gate; values $\le 1$ mean no evidence from the detector);
- robust break-even $\pi^\star$ across the complete predeclared family scope;
- certified known acceptance $L_K$ at the selected operating point;
- `PROMOTE`, `PROMOTE_TRIVIAL` or `ABSTAIN` at each predeclared $\pi_U$.

Secondary outputs:

- family-specific break-even values;
- all threshold-level $L_K, U_U, B$ values;
- NLL/Brier/ECE with uniform references;
- transport stress-test gaps;
- detector accuracy/F1 as descriptive context.

No family, threshold, or prevalence point is removed after reveal.

## 11. Main interpretation

The central empirical question is deliberately two-sided.

A strong positive outcome would show that a standard detector can obtain a
useful finite-sample known-membership certificate over the declared finite
family scope for nontrivial $\pi_U$ and coverage.

A strong negative outcome would show that, even for a competent detector,
finite-sample uncertainty, unknown-family acceptance, prevalence sensitivity,
or family heterogeneity makes the certificate vacuous or useful only at very
small $\pi_U$ / coverage.

Neither outcome is guaranteed to be publishable; scientific value depends on
execution quality, comparison with prior art, and what the result teaches
beyond the algebra.

## 12. Relationship to the current interface manuscript

The current interface-first TMLR manuscript is not treated as a separate
submission target while this redesign is unresolved.

Its useful material is demoted to a background/methodology section explaining:

- target mismatch;
- scope coverage;
- finite compatible worlds;
- fail-closed diagnostics.

The empirical known-membership certificate becomes the load-bearing scientific
question.

No old theorem is presented as the paper's novelty.

## 13. Related-work minimum set

The future paper must engage directly with:

- risk-controlling prediction sets;
- Learn-then-Test;
- conformal risk control;
- Seldonian high-confidence safety;
- selective prediction / reject options;
- maximum-softmax-probability OOD baselines;
- open-set recognition;
- positive-unlabeled / class-prior / mixture-proportion estimation;
- AI-text detector reliability and bias;
- RAID, M4, and MAGE;
- partial identification and transportability.

Every citation is verified from a primary source before manuscript submission.

## 14. Venue status

No venue is frozen.

ICLR 2027 workshop organizers have a suggested contribution deadline of
1 February 2027, but individual workshop CFPs still determine actual topics and
deadlines. Workshop fit must be checked only after the study design is frozen.

TMLR remains a possible later full-paper target only if the final study has
sufficient methodological or empirical significance.

## 15. Hard gates

Before any confirmatory dataset is accessed:

- the negative RAID development viability screen has a predeclared scientific
  disposition after substantive human review;

- substantive independent human methodological review: `1/1`;
- all review points dispositioned;
- confirmatory corpus and license selected;
- family ontology frozen;
- threshold grid frozen;
- multiplicity allocation frozen;
- sample-size calculation frozen;
- detector and calibration method frozen;
- independent custody/evaluator established or the study explicitly downgraded
  from "sealed";
- Research Lock created and hash recorded.

Until those gates close:

$$
\boxed{\text{NO CONFIRMATORY RUN}}
$$

and the project remains `descriptive_only`.
