# Scientific Claim Review — RAID M1/M2/M2.1

Date: 24 November 2026

Status: `STAGE_A_CLAIM_REVIEW / DEVELOPMENT_ONLY`

Scientific readiness before review: `descriptive_only`

Scientific readiness after review: `descriptive_only`

Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`

External methodological reviews: `0/1`

## Purpose

This review classifies public statements against the actual executed RAID Stage
A evidence.

It is not a product launch decision, a Stage B Scientific Claim Review, an
external peer review, or an attribution unlock.

Classification vocabulary:

- `ALLOW` — directly supported as a factual/reproducibility statement;
- `ALLOW_WITH_SCOPE` — supported only with explicit benchmark/development
  scope and limitations;
- `REJECT` — contradicted by the current evidence or prohibited by the
  evidence policy;
- `REQUIRES_MORE_EVIDENCE` — scientifically plausible but not established by
  M1/M2/M2.1.

## Evidence reviewed

### M1

Fixed RAID Pilot A:

- source SHA-256:
  `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- selected records: `500`;
- train/test: `351 / 149`;
- lineage overlap: `0`.

Macro-F1:

- length-only: `0.247431`;
- CogniPrint 12D: `0.535883`;
- char 3–5 hashed TF-IDF: `0.578782`;
- word 1–2 hashed TF-IDF: `0.595220`.

### M2

Primary external workflow run:

`45370233451`

Persisted result SHA-256:

`1fb39616725c90470e5dbc35ff7f4211190448e9bb1505c256d5febeba275dc3`

Separate runner-isolated CI rerun `45371006757` produced a byte-identical
persisted result. This demonstrates deterministic re-execution, not independent
scientific replication.

Aggregate point estimates:

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12D | 0.382981 | 1.348983 | 0.710081 | 0.511947 | 0.657500 |
| Char 3–5 | 0.447966 | 1.241039 | 0.673324 | 0.338034 | **0.485000** |
| Word 1–2 | **0.515231** | **1.234877** | **0.670327** | **0.303210** | 0.512500 |

All predeclared per-fold 95% lineage-group bootstrap intervals for
12D-vs-baseline NLL/Brier differences include zero.

Uniform four-class probabilities have NLL $\log 4 \approx 1.386294$ and
multiclass Brier score $0.75$ under the implemented convention. The reported
M2 proper scores are therefore only modestly better than an uninformative
probability vector, particularly for 12D. The four leave-one-family-out folds
reuse the same Stage A corpus and are not independent replications.

### M2.1

Post-result exploratory run:

`45373412957`

Canonical diagnostic result hash:

`9e90568b3443dd1561bb900c609c0baded57227d25a66b5880d7e0fa5dce0288`

M2.1 established that:

- held-out unknown conformal empty-set rate was `0.0` in every
  fold/representation;
- near-zero conformal false-known was almost entirely multi-class ambiguity;
- the exploratory risk-coverage grid did not reveal a 12D selective advantage;
- the n-gram M2 temperature lower bound `T=0.05` was materially restrictive;
- widening the lower temperature range did not rescue average 12D probability
  quality;
- every conformal-calibration record had a unique declared lineage group.

## Claim decisions

### 1. “CogniPrint has executed reproducible Stage A RAID experiments.”

**Decision: `ALLOW`**

Reason:

M1, M2 and M2.1 have persisted evidence records. M2 was re-executed in a separate runner-isolated workflow with
byte-identical `m2-results.json`; this is determinism evidence, not independent
scientific replication.

Safe wording:

> CogniPrint has executed reproducible development-stage RAID experiments with
> pinned source and metadata-selection identity checks.

Required qualifier:

`development-stage`

Do not call this independent scientific replication by another research group.

---

### 2. “The current 12D representation contains benchmark-bounded signal beyond a length-only baseline.”

**Decision: `ALLOW_WITH_SCOPE`**

Reason:

In historical M1, 12D macro-F1 `0.535883` exceeded length-only
`0.247431`.

Safe wording:

> On the fixed RAID Pilot A M1 task, the current 12D representation carried
> substantially more closed-set class-discrimination signal than the tested
> length-only control.

Not allowed:

> 12D identifies the true generating model.

---

### 3. “The current 12D representation outperforms conventional lexical baselines.”

**Decision: `REJECT`**

Reason:

Both historical M1 n-gram baselines exceeded 12D macro-F1.

M2 aggregate point estimates also favor the lexical baselines on macro-F1, NLL,
Brier and AURC.

The per-fold proper-score confidence intervals are too wide for a pooled
inferential superiority/inferiority statement, but the available evidence does
not support a 12D superiority claim.

---

### 4. “Word n-grams are scientifically proven superior to 12D.”

**Decision: `REJECT`**

Reason:

Word n-grams have stronger aggregate point estimates, but no prospectively
specified pooled cross-fold estimand/inference procedure exists, and all
predeclared per-fold proper-score intervals include zero.

Safe wording:

> Word n-grams produced stronger aggregate M2 point estimates on the tested
> Stage A protocol.

---

### 5. “Temperature scaling improves CogniPrint 12D calibration.”

**Decision: `REJECT`**

Reason:

In M2, mean held-out NLL worsened:

`1.277792 -> 1.348983`

and NLL worsened in every 12D fold.

Mean Brier also worsened:

`0.692123 -> 0.710081`.

M2.1's wider lower-temperature diagnostic did not rescue the result:
uncalibrated `T=1` remained better on average than the diagnostic
calibration-selected 12D temperature.

---

### 6. “The M2 n-gram temperatures prove that T=0.01–0.02 is the correct calibrated setting.”

**Decision: `REQUIRES_MORE_EVIDENCE`**

Reason:

M2.1 was post-result exploratory and the held-out evaluation data were already
exposed to the research process.

M2.1 does support the narrower diagnostic statement that `T=0.05` was an
active lower-bound restriction for the tested n-gram cosine score scale.

A future sealed protocol must preregister the score-to-probability mapping and
temperature domain before evaluation. Numeric choices for that future protocol
must not be selected from the already exposed M2/M2.1 evaluation outcomes.

---

### 7. “Conformal prediction successfully detects unseen/OOD model families.”

**Decision: `REJECT`**

Reason:

M2.1 found unknown empty-set rate `0.0` in every fold and representation.

Near-zero false-known singleton behavior came almost entirely from
`UNKNOWN_AMBIGUOUS` prediction sets containing multiple known classes.

Safe wording:

> Under the executed alpha-0.05 design, the conformal layer produced no
> empty-set unknown rejection and usually abstained through multi-class
> ambiguity.

This is an observed design outcome, not a theorem that empty sets are
mathematically impossible for every dataset with the same nominal alpha.

Not allowed:

> Conformal OOD detection achieved ~99–100% rejection.

---

### 8. “Conformal ambiguity was caused by duplicate lineage groups in calibration.”

**Decision: `REJECT`**

Reason:

Every conformal-calibration record in the M2.1 audit had a unique declared
lineage group; largest records per lineage group was `1`.

This does not prove exchangeability, but duplicate declared lineage groups are
not the observed cause.

---

### 9. “Maximum calibrated class confidence is a reliable OOD detector.”

**Decision: `REJECT`**

Reason:

M2 mean known-vs-unknown AUROC was only approximately:

- 12D: `0.5117`;
- char: `0.5398`;
- word: `0.5329`.

False-known rates remained high.

---

### 10. “Abstention makes the current 12D representation practically safe for attribution.”

**Decision: `REJECT`**

Reason:

M2.1 exploratory selective-risk analysis did not reveal a hidden 12D
advantage.

At approximately 25% achieved coverage, mean 12D risk remained about
`0.4626`.

At the existing frozen threshold policy, mean 12D evaluation risk was about
`0.4999`.

Abstention alone does not turn the current representation into a reliable
attribution system.

---

### 11. “The 60% threshold-development coverage policy guarantees 60% held-out coverage.”

**Decision: `REJECT`**

Reason:

It is an operating rule chosen on the threshold-development partition, not a
coverage theorem.

M2.1 showed held-out mean evaluation coverage:

- 12D: `0.6655`;
- char: `0.5399`;
- word: `0.5613`.

Individual lexical folds fell as low as approximately `0.44–0.47`.

---

### 12. “The current 12D representation is useful as an interpretable development baseline.”

**Decision: `ALLOW_WITH_SCOPE`**

Reason:

It is deterministic, interpretable, reproducible, and has nontrivial M1
benchmark-bounded signal, while current evidence does not support stronger
attribution use.

Safe wording:

> The 12D representation remains useful as an interpretable development
> baseline and failure-analysis object.

This decision is not a claim that 12D should remain the final attribution
representation.

---

### 13. “CogniPrint can make benchmark-bounded model-family suggestions in a user-facing system today.”

**Decision: `REQUIRES_MORE_EVIDENCE`**

Required before reconsideration includes:

- prospectively justified probability model;
- genuinely sealed unseen families or equivalent external holdout;
- preregistered calibration/OOD method;
- useful risk/coverage operating regime;
- acceptable false-known behavior;
- external methodological review;
- Stage B custody and independent evaluation;
- separate Scientific Claim Review.

---

### 14. “CogniPrint identifies the exact generating model from text.”

**Decision: `REJECT`**

Reason:

Unsupported by M1/M2/M2.1 and prohibited by the current Claim Firewall absent a
separately validated method or appropriate external attestation.

---

### 15. “CogniPrint determines whether arbitrary text is AI-generated.”

**Decision: `REJECT`**

Reason:

No universal AI-origin result exists. RAID labels/families and current Stage A
protocol do not support this claim.

---

### 16. “CogniPrint establishes authorship, operator identity, commissioner identity, intent, responsibility, or legal/forensic provenance from prose.”

**Decision: `REJECT`**

Reason:

These claims are outside the evidentiary scope of content-derived statistical
features and remain locked by policy.

## Resulting public position

The strongest current public scientific statement is:

> CogniPrint is a descriptive and evidence-structuring research framework with
> reproducible Stage A experiments showing that the current compact 12D
> representation does not outperform tested lexical baselines on the studied
> RAID tasks. Calibration, open-set confidence and conformal diagnostics expose
> substantial uncertainty and support abstention/claim narrowing rather than
> source attribution.

## Readiness decision

No readiness change.

```text
Scientific readiness: descriptive_only
External methodological reviews: 0/1
Research freeze: PRE-FREEZE
Challenge 001 Stage B: NOT_AUTHORISED_TO_START
```

## Next claim-review trigger

Repeat a Scientific Claim Review only after a materially new evidence gate is
closed, for example:

- substantive independent methodological review;
- new prospectively frozen probability/OOD method;
- sealed Stage B evaluation;
- independent external replication.

Do not repeat the review merely because a post-result exploratory analysis
finds a more favorable number.
