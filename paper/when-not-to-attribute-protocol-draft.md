# When Not to Attribute: Calibration, Abstention and Evidence-Bounded Text Profiling

**Status:** methodological draft / no M2 result claimed  
**Research lead:** Roman Adriashkin, CogniPrint Research Initiative  
**Scientific readiness:** `descriptive_only`  
**Relationship to Challenge 001:** Stage A development only; Stage B remains `NOT_AUTHORISED_TO_START`.

**Executable M2 development protocol:** [`docs/raid-calibration-m2-development.md`](../docs/raid-calibration-m2-development.md). Real pinned RAID M2 remains `NOT EXECUTED`.

## Abstract

Text-source attribution systems are often evaluated primarily by closed-set classification metrics even when deployment requires a more basic decision: whether the available evidence supports making an attribution at all. CogniPrint's fixed Stage A RAID pilot exposed a useful limitation of its initial compact representation: on a five-class, 500-record development benchmark, a 12-dimensional nearest-centroid profile achieved macro-F1 0.535883, while word 1–2 hashed TF-IDF achieved 0.595220. Rather than treating this negative comparison as a reason to optimize the feature set against the same held-out labels, this note specifies a follow-on evaluation centered on probabilistic quality, abstention and open-world error. The proposed study compares frozen 12D, word n-gram and character n-gram representations under matched classifier/scoring procedures and lineage-disjoint calibration/evaluation partitions. Primary outcomes are held-out negative log-likelihood, multiclass Brier score, selective risk at matched coverage, and false-known behavior on held-out unknown sources. ECE, classwise ECE, AURC and reliability diagrams are secondary diagnostics. Class-conditional split conformal prediction provides prediction sets for known classes under explicit exchangeability assumptions; it is not presented as a guarantee of singleton correctness or unseen-source rejection. No empirical M2 ordering is claimed in this draft.

## 1. Motivation: a negative result that narrows the question

The fixed RAID Pilot A development comparison retained an unfavorable result:

| Method | Macro-F1 |
| --- | ---: |
| Length-only nearest centroid | 0.247431 |
| CogniPrint 12D nearest centroid | 0.535883 |
| Character 3–5 hashed TF-IDF | 0.578782 |
| Word 1–2 hashed TF-IDF | **0.595220** |

The comparison used 500 selected records, a grouped 351/149 train/test split and reported zero train/test lineage overlap. The result does **not** establish general source attribution and does **not** show that the compact 12D representation carries unique source information beyond lexical baselines.

It does establish a methodological constraint: future CogniPrint work should not assume that an interpretable representation is valuable merely because it is interpretable. A useful follow-on question is whether a system can make better bounded decisions about **when to attribute and when to abstain**, while preserving transparent baseline comparisons.

## 2. Research question

> Under lineage-disjoint held-out evaluation, do compact interpretable text profiles and transparent lexical baselines exhibit meaningfully different probability quality, selective-risk and open-world rejection behavior when classifier family, calibration procedure and evaluation data are controlled?

The study explicitly permits three outcomes:

1. **positive:** a CogniPrint representation improves one or more uncertainty/selective outcomes without hiding degradation elsewhere;
2. **mixed:** different representations dominate different operating regimes;
3. **negative:** lexical baselines remain superior or no reliable difference is found.

The third outcome is publishable evidence and does not trigger feature tuning against the held-out test.

## 3. Experimental roles and leakage boundary

The historical RAID M1 test partition must not be used to fit a temperature, choose an abstention threshold, select a conformal alpha, choose a confidence score, tune a classifier or select a representation.

M2 requires lineage-disjoint roles:

```text
reference / classifier training
probability calibration
conformal calibration
threshold development (when a threshold is required)
held-out evaluation
```

If the available Stage A-visible sample does not support these roles with adequate per-class resolution, the result is **INSUFFICIENT DEVELOPMENT EVIDENCE**. The protocol must not silently reuse training or evaluation labels to manufacture calibration.

Raw RAID text should not be persisted into a convenience CSV. The existing M1 pinned-source and selected-record-manifest design should be reused: verify the authoritative source/hash, transiently rehydrate selected records, and persist only permitted aggregate artifacts.

## 4. Representations and classifier control

The principal comparison is across representations, not across arbitrarily different learning systems.

The study therefore requires the same prospectively frozen classifier/scoring family and the same partition identities for:

- CogniPrint 12D;
- word n-gram representation;
- character n-gram representation.

The historical M1 hashed baselines remain exactly documented as historical comparators: word 1–2 and character 3–5 hashed TF-IDF with the published hashing dimensions and train-only IDF. A new logistic-regression comparison may be added only as a clearly named **M2 baseline**, applied consistently to all representations and frozen before held-out evaluation.

No MLP, MC Dropout or gradient-boosting search is part of the primary Paper 1 experiment.

## 5. Probability quality

For K classes and predicted probabilities (p_i=(p_{i1},...,p_{iK})), the primary probability metrics are proper scoring rules.

### Negative log-likelihood

```text
NLL = -(1/N) * sum_i log p_i(y_i)
```

Lower is better.

### Multiclass Brier score

```text
Brier = (1/N) * sum_i sum_k (p_ik - 1[y_i=k])^2
```

Lower is better.

Per-example NLL and Brier values are retained so paired lineage-group uncertainty intervals can compare systems on the same evaluation examples.

## 6. Temperature scaling

A single positive temperature (T) is fitted only on the probability-calibration partition by minimizing NLL:

```text
p_T(y=k|x) = exp(z_k/T) / sum_j exp(z_j/T)
```

Because (T>0) preserves the ordering of logits within each example, it preserves the top-1 predicted class. Thus temperature scaling can change NLL/Brier/ECE without pretending that it improved classification accuracy or macro-F1.

The fitted temperature is frozen before held-out evaluation. Evaluation rejects lineage overlap between probability-calibration and held-out roles.

## 7. Calibration diagnostics

Top-label ECE and macro classwise ECE are secondary diagnostics, not headline evidence. Their bin count is frozen prospectively.

Classwise ECE evaluates each class probability against the one-vs-rest event across **all** evaluation examples, rather than conditioning only on examples where that class was top-1.

Reliability diagrams are descriptive figures.

## 8. Selective prediction

Let (g(x)in{0,1}) denote whether the system accepts a prediction.

Coverage is:

```text
coverage = accepted / total
```

Selective risk under 0-1 classification loss is:

```text
selective_risk = errors_among_accepted / accepted
```

The primary comparison reports selective risk at prospectively specified matched coverage values and the complete risk-coverage curve.

AURC is a secondary scalar summary. Exact confidence ties are accepted as groups so row order cannot artificially improve the curve. Raw AURC is interpreted together with full-coverage error because it reflects both classifier quality and confidence ranking.

No protocol language presupposes that the 12D curve lies below an n-gram curve.

## 9. Open-world evaluation and false-known behavior

A held-out source family that was unavailable to the known-class classifier is used to evaluate open-world failure.

For a pre-frozen acceptance threshold, the development evaluator reports:

- true-known acceptance rate;
- false-known rate on unknown examples;
- Wilson intervals;
- known-vs-unknown AUROC.

`false-known rate` is project terminology for an important open-set failure mode; it is not claimed as a novel concept unique to CogniPrint.

A maximum-softmax threshold is retained only as a transparent baseline. Thresholds are not optimized on held-out evaluation data.

## 10. Conformal prediction sets

CogniPrint currently implements class-conditional split conformal prediction using cosine nonconformity:

```text
score(x,y) = 1 - cosine_similarity(x, centroid_y)
```

For each known class, calibration scores come only from its dedicated conformal-calibration examples. The prediction set contains classes whose conformal p-values exceed the frozen alpha.

Decision mapping:

- singleton set -> candidate known class;
- empty set -> `UNKNOWN_OOD`;
- multiple classes -> `UNKNOWN_AMBIGUOUS`;
- inadequate calibration/evidence -> `UNKNOWN_INSUFFICIENT_EVIDENCE`.

The finite-sample coverage interpretation applies to known-class **prediction sets** under the relevant exchangeability assumptions. It is not a guarantee that a singleton is correct and is not a guarantee that an unseen family is rejected.

The report therefore separates prediction-set coverage, singleton rate/accuracy, ambiguity, empty sets, insufficient evidence and held-out unknown false-known behavior.

## 11. Decision-theoretic reject option and Claim Firewall

For an already authorized probabilistic claim with top-class probability (p), correct-claim cost (C_c), incorrect-claim cost (C_w), and abstention cost (C_a), expected claim loss is:

```text
p*C_c + (1-p)*C_w
```

Claiming is preferred only when this does not exceed (C_a). In the symmetric special case (C_c=0), (C_w=1):

```text
claim if p >= 1 - C_a
```

This is **not** the Claim Firewall itself. It is a downstream reject-option calculation after evidence and policy gates authorize the claim type. A favorable cost parameter cannot unlock authorship, actor/commissioner, intent, legal/forensic or otherwise unsupported claims.

## 12. Primary and secondary outcomes

### Primary probability outcomes

- held-out NLL;
- held-out multiclass Brier;
- paired lineage-group confidence intervals for their differences.

### Primary selective/open-world outcomes

- selective risk at matched predeclared coverage points;
- coverage;
- false-known rate on held-out unknowns with interval;
- unknown rejection rate.

### Secondary outcomes

- AURC;
- top-label ECE;
- macro classwise ECE;
- reliability diagrams;
- known-vs-unknown AUROC;
- per-class and confusion-matrix diagnostics.

Closed-set macro-F1 and balanced accuracy remain mandatory context and cannot be hidden when uncertainty metrics improve.

## 13. Falsification and claim narrowing

The study does not support a stronger CogniPrint claim if any apparent advantage:

- disappears under lineage-disjoint evaluation;
- depends on selecting thresholds after observing held-out labels;
- is present only in a noisy ECE binning choice while NLL/Brier do not support it;
- is obtained by near-universal abstention;
- collapses on an unknown source family;
- requires replacing the frozen baseline after results are observed;
- depends on an unreported drop in closed-set classification quality.

A negative result narrows the claim and is retained.

## 14. Limitations

The historical Stage A sample is small for fine-grained calibration claims. The current feature map is not automatically language-invariant. Cross-language transfer is therefore outside the primary Paper 1 claim. Conformal validity depends on exchangeability assumptions appropriate to the chosen calibration/test design. Open-set metrics depend on the particular held-out families and cannot establish universal OOD rejection.

## 15. Planned result table — intentionally blank

| Representation | Macro-F1 | NLL | Brier | Risk @ matched coverage | FKR unknown | AURC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D | TBD | TBD | TBD | TBD | TBD | TBD |
| Word n-gram | TBD | TBD | TBD | TBD | TBD | TBD |
| Character n-gram | TBD | TBD | TBD | TBD | TBD | TBD |

No value in this table may be filled from synthetic fixtures or tuned-on-test experiments.

## References

- Gneiting, T. & Raftery, A. E. (2007). Strictly Proper Scoring Rules, Prediction, and Estimation. *JASA*.
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML*.
- Kumar, A., Liang, P. & Ma, T. (2019). Verified Uncertainty Calibration. *NeurIPS*.
- Geifman, Y. & El-Yaniv, R. (2017). Selective Classification for Deep Neural Networks. *NeurIPS*.
- Dhamija, A. R., Günther, M. & Boult, T. E. (2018). Reducing Network Agnostophobia. *NeurIPS*.
- Romano, Y., Sesia, M. & Candès, E. (2020). Classification with Valid and Adaptive Coverage. *NeurIPS*.

## Current status

This document is a research protocol/manuscript draft. M2 is **NOT EXECUTED**. No DOI, peer review, external endorsement, Stage B authorization or scientific feature unlock is implied.
