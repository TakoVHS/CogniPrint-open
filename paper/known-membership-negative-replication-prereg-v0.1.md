# Known-Membership Negative Replication — Preregistration v0.1

Status: **DRAFT / NOT FROZEN / HUMAN REVIEW REQUIRED BEFORE RESEARCH LOCK**

Date: 25 November 2026

Human methodological-review gate: `0/1`

This document preregisters a prospective replication attempt of the negative
RAID development finding recorded in
`paper/known-membership-raid-dev-result-v0.1.md`.

It is deliberately written before selecting or inspecting confirmatory rows.
Nothing in this file authorizes access to M4, MAGE, or any other confirmatory
corpus.

## 1. Replication question

The RAID development result showed that a standard word 1--2 TF-IDF +
multinomial logistic-regression detector had useful closed-set discrimination
but essentially no certified known-membership lift over the mandatory
accept-all reference at useful known acceptance.

The replication question is:

> Does the same frozen detector/gate/certificate pipeline produce the same
> negative conclusion on a different multi-generator corpus containing machine
> families absent from RAID?

The target remains known-set membership, not exact-family attribution.

## 2. Frozen pipeline

The scientific pipeline is frozen as a single-run replication target.

Unless a substantive human reviewer requires a change before Research Lock,
the replication uses:

- one deterministic seed;
- one execution of the full analysis;
- word 1--2 TF-IDF;
- `min_df=2`;
- `max_features=200000`;
- sublinear TF scaling;
- multinomial logistic regression;
- `C=4.0`;
- `max_iter=2000`;
- the same gate definition
  $$A_\tau(x)=\mathbf 1\{\max_k p_k(x)\ge\tau\};$$
- threshold grid
  $$\mathcal T=\{0,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99\};$$
- family-wise one-sided exact Clopper--Pearson bounds;
- Bonferroni allocation over every nonzero threshold and every known/unknown
  family stratum used by the primary result;
- primary risk tolerance
  $$\delta=0.10;$$
- the mandatory accept-all reference
  $$B_0(\pi_U)=\pi_U,\qquad \pi_0^\star=\delta.$$

No alternate detector, threshold grid, seed, confidence allocation, feature
representation, or calibration scheme may be substituted after Research Lock.

### Only permitted new code

The only corpus-specific scientific code permitted after corpus selection is an
**adapter** that converts the chosen corpus into the already frozen analysis
schema.

The adapter must be written from corpus documentation/schema metadata and
tested on synthetic fixtures before any confirmatory text or family-level
outcome is inspected.

The adapter may map:

- opaque record id;
- source/prompt group id;
- family label for the independent evaluator/custodian;
- domain metadata if required by the frozen grouping rule;
- raw text into the frozen detector input.

It may not introduce a new scientific feature, detector, threshold, filtering
rule, or family exclusion after results are visible.

## 3. Corpus eligibility

The confirmatory corpus is selected from documentation only before Research
Lock.

It must satisfy all of the following:

1. at least four machine-generator families absent from the RAID development
   family set;
2. enough records to execute the frozen train/certificate/test roles without
   source-group leakage;
3. a documented license permitting the intended research use;
4. family labels and source/prompt grouping that can be mapped without
   inspecting model performance;
5. no family is removed because of an unfavorable result.

A corpus that fails these criteria is rejected before confirmatory analysis.

## 4. Detector-competence precondition P1

A negative membership result is interpretable only if the frozen classifier is
not simply incompetent on the known classes.

For each held-out-family replication fold, define the known-class test accuracy
of the frozen detector as `Acc_K`.

Precondition P1 is

$$
\boxed{\mathrm{P1}:\quad \mathrm{Acc}_K \ge 0.60.}
$$

A family whose fold fails P1 is not counted as evidence for or against the
primary replication hypothesis.

If fewer than four new held-out machine families satisfy P1, the overall
replication outcome is `INCONCLUSIVE`.

P1 is a competence screen, not a claim that 0.60 accuracy is good enough for
deployment.

## 5. Primary statistic

For each threshold and held-out family, compute the simultaneous certificate

$$
B_\tau(\pi_U)
=
\frac{\pi_U U_U(\tau)}
{(1-\pi_U)L_K(\tau)+\pi_U U_U(\tau)}
$$

and the break-even prevalence

$$
\pi_\tau^\star
=
\frac{\delta L_K(\tau)}
{U_U(\tau)(1-\delta)+\delta L_K(\tau)}.
$$

The detector-lift statistic is

$$
\mathrm{Lift}_\tau=\frac{\pi_\tau^\star}{\delta}.
$$

The primary per-family statistic is

$$
\boxed{
\mathrm{Lift}_{0.5}
=
\max_{\tau>0:\,L_K(\tau)\ge0.5}
\mathrm{Lift}_\tau.
}
$$

If no nonzero threshold reaches $L_K\ge0.5$, the family has no useful
certificate operating point and is assigned `ABSTAIN` for the primary
screen.

The unconstrained maximum lift may be reported descriptively but cannot change
the primary outcome.

## 6. Primary hypothesis H1

The RAID development result suggests that max-known-probability gating gives
little or no useful separation from held-out generator families.

The preregistered negative-replication hypothesis is:

$$
\boxed{
\mathrm{H1}:\quad
\mathrm{Lift}_{0.5}\le1.20
\text{ for every P1-eligible held-out family.}
}
$$

The 1.20 boundary is a practical effect-size boundary, not a significance
threshold.

For orientation:

- lift $=1$ is the accept-all reference;
- a neutral point-estimate gate can yield certified lift below one because
  lower/upper confidence bounds widen the two acceptance rates;
- lift around $1.5$ corresponds to a clearly nontrivial separation regime
  rather than a near-neutral certificate.

## 7. Preregistered outcome classes

Exactly one overall label is assigned.

### REPLICATED

Requirements:

- at least four machine families absent from RAID satisfy P1; and
- every P1-eligible family has
  $$\mathrm{Lift}_{0.5}\le1.20.$$

Prewritten interpretation:

> The negative RAID finding replicated: under the frozen max-known-probability
> gate, a competent closed-set detector did not produce more than modest
> known-membership certificate lift at useful certified known acceptance on the
> new generator families.

### REFUTED

Requirements:

- at least four machine families absent from RAID satisfy P1; and
- every P1-eligible family has
  $$\mathrm{Lift}_{0.5}\ge1.50.$$

Prewritten interpretation:

> The negative RAID finding did not replicate: the unchanged gate produced
> substantial certified membership separation on every eligible new generator
> family, so the RAID result was not a general property of this pipeline.

### MIXED

Requirements:

- at least four machine families absent from RAID satisfy P1; and
- neither `REPLICATED` nor `REFUTED` applies.

This includes transition-band outcomes $1.20<\mathrm{Lift}_{0.5}<1.50$ and
heterogeneous families on opposite sides of the preregistered boundaries.

Prewritten interpretation:

> The replication was heterogeneous: the unchanged pipeline produced useful
> membership separation for some new generator families but not others.
> Family identity therefore materially affects whether the certificate is
> informative.

### INCONCLUSIVE

Requirements:

- fewer than four new machine families satisfy P1; or
- a frozen implementation/custody failure invalidates the one-run protocol.

Prewritten interpretation:

> The replication was inconclusive because the preregistered competence or
> execution conditions were not met; no conclusion about replication of the
> RAID membership result is drawn.

No outcome class may be renamed after reveal.

## 8. Point estimates and confidence interpretation

For every held-out family, publish:

- known-class test accuracy;
- NLL and Brier with uniform references;
- point acceptance rate of every known family at every threshold;
- point acceptance rate of the held-out family at every threshold;
- simultaneous $L_K$ and $U_U$;
- all threshold-level lift values;
- $\mathrm{Lift}_{0.5}$;
- unconstrained maximum lift as a diagnostic only.

Certified lift below one is not automatically interpreted as a gate that is
causally or intrinsically harmful. It can arise because the Clopper--Pearson
and Bonferroni margins widen an approximately neutral point-estimate gate.

## 9. Data roles and leakage control

Source/prompt siblings must remain in the same role.

The frozen conceptual roles are:

- train;
- certificate;
- final test.

A separate calibration role is used only if the frozen detector requires one;
the current logistic-regression replication does not introduce post-hoc
temperature or vector scaling.

The exact corpus-specific counts and grouping field must be frozen before row
inspection and recorded in the Research Lock.

## 10. Custody modes

Two allowed modes exist.

### Mode A — independently blinded

An independent custodian/evaluator holds the family manifest, provides opaque
research-facing ids, verifies the frozen prediction hash, and performs or
controls the label reveal.

This mode may be described as independently blinded if the custody log supports
that description.

### Mode B — prospective/locked, not sealed

If no independent custodian is available, the study may still proceed only
after a public Research Lock that fixes the corpus, adapter, hashes, seed,
pipeline, thresholds, outcome rules, and analysis script.

This mode must be described as:

`PROSPECTIVE / LOCKED / NOT SEALED`

It must not be called independently blinded.

## 11. Forbidden post-lock actions

After Research Lock, the following are prohibited:

- trying another random seed;
- changing the detector or feature representation;
- changing logistic-regression hyperparameters;
- adding/removing thresholds;
- changing $\alpha$, $\delta$, $L_K$ floor, or lift boundaries;
- removing a family because its result is inconvenient;
- changing corpus filters using observed outcomes;
- adding calibration because the frozen score behaves poorly;
- rerunning the confirmatory analysis after seeing the result except to repair
  a demonstrated implementation error that invalidates the run.

A qualifying implementation error must be documented before rerun, with the
original failed output preserved.

## 12. One-run rule

There is one confirmatory analysis execution.

Dry runs are permitted only on synthetic fixtures that contain no confirmatory
texts, labels, family identities, or outcome-derived statistics.

The confirmatory run id, exact repository commit, corpus hash/manifest hash,
adapter hash, and artifact hashes are preserved.

## 13. Research Lock checklist

This preregistration cannot be frozen until all boxes are satisfied:

- [ ] substantive independent human methodological review gate is `1/1`;
- [ ] every review criticism has a recorded disposition;
- [ ] corpus selected from documentation and eligibility criteria;
- [ ] at least four non-RAID machine families documented;
- [ ] corpus license verified;
- [ ] corpus-specific grouping rule fixed;
- [ ] corpus-specific sample-count rule fixed;
- [ ] adapter complete and synthetic tests PASS;
- [ ] exact repository commit recorded;
- [ ] seed recorded;
- [ ] detector/hyperparameters recorded;
- [ ] thresholds recorded;
- [ ] confidence allocation recorded;
- [ ] P1/H1/outcome classes unchanged;
- [ ] custody mode selected and documented;
- [ ] confirmatory data remain uninspected before lock.

Until all items are satisfied:

$$
\boxed{\text{PREREGISTRATION NOT FROZEN / NO CONFIRMATORY RUN}}
$$
