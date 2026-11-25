# RAID Known-Membership Development Screen — Result v0.1

Status: **STAGE_A_DEVELOPMENT_ONLY / NEGATIVE VIABILITY SCREEN / NOT CONFIRMATORY**

Date: 25 November 2026

This document records the first real RAID development run for the
known-membership certificate redesign.

It does **not** satisfy the independent-human-review gate, does not authorize
Stage B, and must not be represented as confirmatory evidence.

## Provenance

Workflow:

`RAID Known-Membership Development (Stage A only)`

Run:

`45581653607`

Historical run head:

`ee93c19f8233f304c0a3dc9099ab9113fed0dce1`

Artifact:

`known-membership-dev-stage-a`

Artifact id:

`15006638080`

Artifact digest:

`sha256:d59a8be6a071e1827dcce3c9a57e12eadf10f239d15edd988b2f61bd2f4562c8`

Pinned RAID source SHA-256:

`c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`

The run verified the pinned source size and SHA before analysis.

## Design

Families:

- human;
- ChatGPT;
- GPT-4;
- Cohere-Chat;
- Llama-Chat;
- Mistral-Chat;
- MPT-Chat.

For each machine family in turn, that family was treated as the declared
unknown family and all remaining families were treated as known.

The detector was word 1--2 TF-IDF plus multinomial logistic regression.

The analysis used 3,000 common source groups per family with group-stable roles:

- train: 1,536 per family;
- certificate: 864 per family;
- test: 600 per family.

The machine-generation regime was fixed to sampling with no repetition
penalty. The same source group was assigned to the same role across all
families.

The mandatory accept-all reference was included.

Primary tolerance:

$
\delta = 0.10.
$

Development prevalence grid:

$
\pi_U \in \{0.10, 0.20, 0.30, 0.50\}.
$

## Result

| Held-out family | Known test accuracy | NLL / uniform | lift at $L_K \ge 0.5$ | unconstrained best lift |
| --- | ---: | ---: | ---: | ---: |
| ChatGPT | 0.728 | 0.904 / 1.792 | 0.866 | 0.866 |
| GPT-4 | 0.707 | 0.944 / 1.792 | 0.861 | 0.861 |
| Cohere-Chat | 0.788 | 0.839 / 1.792 | 0.894 | 0.894 |
| Llama-Chat | 0.741 | 0.904 / 1.792 | 0.913 | 0.913 |
| Mistral-Chat | 0.802 | 0.806 / 1.792 | 1.004 | 1.154 |
| MPT-Chat | 0.787 | 0.828 / 1.792 | 1.000 | 1.310 |

At the fixed useful-coverage screen $L_K \ge 0.5$, no held-out family achieved
meaningful lift over the accept-all reference.

For four families, the **certified** lift was below one. This should not be
read as evidence that the point-estimate gate is intrinsically harmful.
The main reason is the finite-sample confidence margin: the lower
Clopper--Pearson bound on known acceptance and upper bound on unknown
acceptance make a nearly neutral gate look slightly worse than the exact
accept-all reference.

For Mistral-Chat and MPT-Chat, useful-coverage lift was effectively one.

The apparently larger unconstrained MPT/Mistral values occur only at low
certified known acceptance:

- Mistral-Chat: best unconstrained lift (1.154) at
  $L_K \approx 0.091$;
- MPT-Chat: best unconstrained lift (1.310) at
  $L_K \approx 0.080$.

These are not useful deployment operating points and are retained only to show
why unconstrained maximum lift is a misleading viability metric.

## Point acceptance rates at the representative threshold

At $\tau=0.3$, the point acceptance rates from the saved Stage-A artifact are:

| Held-out family | min known-family point acceptance | held-out-family point acceptance | $L_K$ | $U_U$ |
| --- | ---: | ---: | ---: | ---: |
| ChatGPT | 0.810 | 0.862 | 0.765 | 0.897 |
| GPT-4 | 0.766 | 0.807 | 0.718 | 0.847 |
| Cohere-Chat | 0.815 | 0.833 | 0.770 | 0.871 |
| Llama-Chat | 0.818 | 0.816 | 0.774 | 0.855 |
| Mistral-Chat | 0.839 | 0.748 | 0.796 | 0.793 |
| MPT-Chat | 0.845 | 0.758 | 0.803 | 0.802 |

These point rates show why the certificate is nearly neutral for most
held-out families: the unknown-family acceptance rate is close to the weakest
known-family acceptance rate. The confidence bounds then widen that already
small separation.

## Representative threshold behavior

At $\tau = 0.3$:

- ChatGPT: $L_K=0.765$, $U_U=0.897$, $\pi^\star=0.0866$;
- GPT-4: $L_K=0.718$, $U_U=0.847$, $\pi^\star=0.0861$;
- Cohere-Chat: $L_K=0.770$, $U_U=0.871$, $\pi^\star=0.0894$;
- Llama-Chat: $L_K=0.774$, $U_U=0.855$, $\pi^\star=0.0913$;
- Mistral-Chat: $L_K=0.796$, $U_U=0.793$, $\pi^\star=0.1004$;
- MPT-Chat: $L_K=0.803$, $U_U=0.802$, $\pi^\star=0.1000$.

Thus the main problem is not weak closed-set discrimination. Known-family test
accuracy is roughly 0.71--0.80 and NLL is far below the six-class uniform
reference. The problem is that confidence on held-out generator families is
also high, so thresholding maximum known-class probability does not produce
useful known-vs-unknown separation.

## Decisions on the development prevalence grid

At $\pi_U \in \{0.20,0.30,0.50\}$, every held-out family returned
`ABSTAIN`.

At $\pi_U=0.10=\delta$, accepting everything is already trivially
certified. Four families therefore returned `PROMOTE_TRIVIAL`.

Mistral-Chat and MPT-Chat produced a formally nontrivial `PROMOTE` at
$\tau = 0.3$, but their lift over accept-all was only approximately
1.004 and 1.000 respectively. These should be interpreted as essentially
trivial improvements, not detector evidence of practical value.

## Scientific interpretation

The development screen answers the intended pre-freeze viability question
negatively for this detector/gate design.

A competent closed-set lexical classifier can discriminate the known classes
reasonably well while still assigning high maximum known-class probability to a
held-out generator family. Closed-set performance therefore does not translate
into a useful finite-sample known-membership certificate under this max-score
gate.

This result supports the claim-boundary motivation but does **not** by itself
make a publishable paper.

## Process disposition

The optional transport stress test was **not run** after this result.

Reason: transport is a secondary assumption check. Once the primary
known-membership gate fails to provide meaningful lift at useful coverage,
running the full pairwise transport matrix would add exploratory complexity
without rescuing the primary design.

Current disposition:

`REDESIGN REQUIRED / DO NOT FREEZE CONFIRMATORY STUDY`

No confirmatory corpus may be accessed.

The next scientific decision must be made after substantive human review and
must not consist of repeatedly tuning thresholds, calibrators, or detector
families on this exposed RAID outcome until a favorable lift appears.
