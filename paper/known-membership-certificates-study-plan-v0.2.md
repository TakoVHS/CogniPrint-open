# Known-Membership Certificates for Open-Set AI-Text Attribution — Study Plan v0.2

Status: **CANDIDATE REDESIGN / PRE-REGISTRATION DRAFT / NO CONFIRMATORY DATA ACCESSED**

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

[
R(	au)
=
P(Yin U mid A_	au=1),
]

where (U) denotes the declared unknown-generator population and
(A_	au) is the event that the gate accepts the text as belonging to the known
set.

The paper asks:

> Given finite held-out certificate samples and an explicit upper bound
> (pi_U) on unknown prevalence, when can we certify
> (R(	au)ledelta) with confidence at least (1-alpha)?

Primary tolerance:

[
delta=0.10.
]

The study reports the prevalence values and operating points for which the
certificate is nonvacuous. No result direction is predeclared as "publishable";
positive, negative, and mixed outcomes are all reported.

### Important non-claim

The formula below does **not** certify the stronger statement
"this text came from known family (k)." Exact-family attribution additionally
requires control of wrong-known-family classification error. The primary paper
therefore uses the narrower claim "the accepted text belongs to the declared
known set."

## 2. Gate and detector

Primary detector:

- word 1--2 TF-IDF + multinomial logistic regression.

Secondary detector:

- character 3--5 TF-IDF + multinomial logistic regression.

Optional reference:

- one predeclared small fine-tuned encoder only if compute, licensing, and
  implementation are fixed before confirmatory evaluation.

CogniPrint 12D is descriptive appendix material only.

For classifier score vector (p(x)), define

[
A_	au(x)=
mathbf 1{max_k p_k(x)ge	au}.
]

The threshold grid (mathcal T) is fixed using development data only before
any confirmatory certificate sample is evaluated.

The finite-sample certificate does **not** require (p_k(x)) to be a perfectly
calibrated probability. It requires a fixed gate whose acceptance frequencies
can be bounded on independent certificate data. NLL, Brier, and ECE are
reported as probability-quality diagnostics rather than as assumptions needed
for the Clopper--Pearson acceptance-rate guarantee.

If a probability calibration method is used, its form and regularization are
fixed prospectively and fitted on a calibration split disjoint from certificate
and test data.

## 3. Family-robust finite-sample certificate

For known family (j), let

[
a_{K,j}(	au)
=
P(A_	au=1mid Y=j).
]

For declared unknown family (u), let

[
a_{U,u}(	au)
=
P(A_	au=1mid Y=u).
]

To avoid silently assuming a favorable mixture of known or unknown families,
the robust finite-scope quantities are

[
a_K^{min}(	au)=min_j a_{K,j}(	au),
qquad
a_U^{max}(	au)=max_u a_{U,u}(	au).
]

Construct simultaneous one-sided exact binomial bounds

[
a_{K,j}(	au)ge L_{K,j}(	au),
qquad
a_{U,u}(	au)le U_{U,u}(	au)
]

for every predeclared threshold and family stratum.

Then define

[
L_K(	au)=min_j L_{K,j}(	au),
qquad
U_U(	au)=max_u U_{U,u}(	au).
]

The multiplicity allocation must cover the entire set of bounds used by the
primary claim, including thresholds and family strata. A simple baseline is
Bonferroni over all one-sided bounds. A less conservative alternative may be
used only if prospectively specified and formally justified before confirmatory
evaluation.

Given deployment unknown prevalence

[
pilepi_U,
]

the finite-scope membership-risk certificate is

[
oxed{
B_	au(pi_U)
=
rac{pi_U U_U(	au)}
{(1-pi_U)L_K(	au)+pi_U U_U(	au)}
}
]

whenever the denominator is positive.

The gate can certify the known-membership claim only when

[
B_	au(pi_U)ledelta.
]

The corresponding break-even prevalence is

[
oxed{
pi_	au^star
=
rac{delta L_K(	au)}
{U_U(	au)(1-delta)+delta L_K(	au)}
}
]

for the nondegenerate case. Edge cases remain explicitly nonnumeric when the
accepted population is undefined.

## 4. Threshold selection

Because simultaneous bounds are constructed for the complete predeclared
threshold family, the study may inspect all certified operating points after
the certificate counts are observed without invalidating the simultaneous
coverage statement.

Primary selection rule:

1. retain thresholds satisfying (B_	au(pi_U)ledelta);
2. among them, report the threshold with the largest certified known-family
   acceptance lower bound (L_K(	au));
3. if none pass, return `ABSTAIN`.

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

For zero unknown acceptances and a one-sided tail allocation (eta),

[
U_U approx -rac{log eta}{n}.
]

But the required (U_U) depends on (pi_U,delta), and the expected
known-acceptance lower bound. Rearranging the certificate gives the target

[
U_U
le
rac{delta(1-pi_U)L_K}
{pi_U(1-delta)}.
]

Before freeze, compute required (n) over the full predeclared prevalence and
coverage grid, including the actual multiplicity allocation over thresholds
and family strata.

If feasible sample sizes cannot make the certificate informative, the study is
stopped before confirmatory data are touched.

## 10. Predeclared prevalence and reporting grid

Initial candidate grid, subject to human review before freeze:

[
pi_Uin
{0.01,0.02,0.05,0.10,0.20}.
]

Primary output:

- robust break-even (pi^star) across the complete predeclared family scope;
- certified known acceptance (L_K) at the selected operating point;
- `PROMOTE` or `ABSTAIN` at each predeclared (pi_U).

Secondary outputs:

- family-specific break-even values;
- all threshold-level (L_K,U_U,B) values;
- NLL/Brier/ECE with uniform references;
- transport stress-test gaps;
- detector accuracy/F1 as descriptive context.

No family, threshold, or prevalence point is removed after reveal.

## 11. Main interpretation

The central empirical question is deliberately two-sided.

A strong positive outcome would show that a standard detector can obtain a
useful finite-sample known-membership certificate over the declared finite
family scope for nontrivial (pi_U) and coverage.

A strong negative outcome would show that, even for a competent detector,
finite-sample uncertainty, unknown-family acceptance, prevalence sensitivity,
or family heterogeneity makes the certificate vacuous or useful only at very
small (pi_U) / coverage.

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

[
oxed{	ext{NO CONFIRMATORY RUN}}
]

and the project remains `descriptive_only`.
