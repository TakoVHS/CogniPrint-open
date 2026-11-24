# RAID M2 results — 24 November 2026

Status: **EXECUTED / DEVELOPMENT_ONLY / PRE-FREEZE**

Scientific-claim evidence: **NO**

Stage B: **NOT_AUTHORISED_TO_START**

This record freezes the first real pinned RAID M2 result. It must not be
silently replaced by a rerun with changed seeds, role fractions, alpha,
temperature bounds, representations or coverage policy.

## Execution identity

GitHub workflow:

- workflow: `RAID M2 External Pinned Evidence`;
- run: `#1`;
- run id: `45370233451`;
- pull-request head SHA: `eee3a48e31dde2cb61207a2165a822fc8ee3bf7c`;
- PR merge checkout commit recorded inside the evidence bundle:
  `b335ed03f2e282b9d099f7166f284ca286e7c276`;
- repository tree:
  `16c7e4a1c38fe9bec52a8ed2358aa12e36622b77`.

GitHub Actions artifact:

- artifact name: `cogniprint-raid-m2-real-stage-a`;
- artifact id: `14908951672`;
- artifact service digest:
  `sha256:c929f1fce7702502bca29770c4d6290c158954dbed51f90656274ffaafc8b310`;
- retained raw-text-free evidence archive SHA-256:
  `93c2cdb6c05919fb3ba348c948c73a836358da633352e566c243dd6c8a1e2352`.

The external sidecar and an independent post-download SHA-256 check matched
that archive hash.

## Historical input gates

All historical identity gates passed before M2 metrics were produced:

- authoritative `train_none.csv` byte size: `801662741`;
- authoritative source SHA-256:
  `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- historical metadata-only `features.jsonl` SHA-256:
  `13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca`;
- selected-record manifest SHA-256:
  `30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb`;
- source-contract SHA-256:
  `e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948`;
- selected records: `500`;
- selection-manifest identity: **PASS**.

The historical 500-record metadata selection was regenerated from the pinned
raw source on the hosted runner and matched the historical feature and
selection hashes exactly.

## Reproducibility and privacy

The M2 evaluator executed twice with identical inputs and parameters:

- run 1 canonical result SHA-256:
  `ead3facf0771b724b2d54a142feaad9b6f5b494d44a521aca1a05503844db6d7`;
- run 2 canonical result SHA-256:
  `ead3facf0771b724b2d54a142feaad9b6f5b494d44a521aca1a05503844db6d7`;
- deterministic match: **PASS**.

The evidence manifest verified every persisted bundle file.

Privacy audit:

- status: **PASS**;
- raw source persisted: `false`;
- raw prompt persisted: `false`;
- raw generation persisted: `false`;
- recoverable vocabulary persisted: `false`.

## Aggregate four-fold development result

| Representation | Mean macro-F1 | Mean calibrated NLL | Mean calibrated Brier | Mean AURC | Mean max-confidence false-known | Mean conformal false-known |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CogniPrint 12D cosine centroid | 0.382981 | 1.348983 | 0.710081 | 0.511947 | 0.657500 | 0.002500 |
| Character 3–5 hashed TF-IDF | 0.447966 | 1.241039 | 0.673324 | 0.338034 | 0.485000 | 0.000000 |
| Word 1–2 hashed TF-IDF | **0.515231** | **1.234877** | **0.670327** | **0.303210** | 0.512500 | 0.005000 |

Lower is better for NLL, Brier, AURC and false-known rate.

On aggregate point estimates, the current 12D representation does **not**
outperform the two lexical baselines. Word 1–2 hashed TF-IDF has the strongest
macro-F1, NLL, Brier and AURC point estimates. Character 3–5 has the lowest
max-confidence false-known point estimate.

This ordering is descriptive. M2 currently has no predeclared pooled
four-fold confidence interval for the aggregate means.

## Per-unknown-family results

### ChatGPT held out

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12D | 0.370123 | 1.366492 | 0.720503 | 0.507055 | 0.73 |
| Char 3–5 | 0.452546 | 1.247613 | 0.673768 | **0.296058** | 0.75 |
| Word 1–2 | **0.498962** | **1.241478** | **0.672869** | 0.334248 | **0.63** |

### GPT-4 held out

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12D | 0.299279 | 1.391849 | 0.756200 | 0.643985 | 0.60 |
| Char 3–5 | 0.434587 | 1.240351 | 0.672407 | 0.371893 | 0.51 |
| Word 1–2 | **0.461261** | **1.234247** | **0.669550** | **0.314539** | **0.40** |

### Llama-chat held out

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12D | 0.395984 | 1.344968 | 0.710138 | 0.478119 | 0.55 |
| Char 3–5 | 0.381225 | **1.252528** | **0.682277** | 0.413000 | **0.36** |
| Word 1–2 | **0.495417** | 1.256388 | 0.683106 | **0.382051** | 0.53 |

### Mistral-chat held out

| Representation | Macro-F1 | NLL | Brier | AURC | False-known |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12D | 0.466536 | 1.292625 | **0.653484** | 0.418630 | 0.75 |
| Char 3–5 | 0.523504 | 1.223666 | 0.664843 | 0.271185 | **0.32** |
| Word 1–2 | **0.605282** | **1.207395** | 0.655782 | **0.182003** | 0.49 |

The isolated lower 12D Brier point estimate in the Mistral fold is not a
resolved advantage: its paired 95% bootstrap intervals against both n-gram
baselines include zero.

## Proper-score paired uncertainty

Each fold used 10,000 lineage-group bootstrap resamples. The estimand is:

`CogniPrint 12D loss - baseline loss`

so negative values favor CogniPrint.

Across all four folds, all 95% intervals for both NLL and Brier differences
between 12D and either n-gram baseline include zero.

Examples:

- ChatGPT unknown, 12D vs word:
  - NLL delta `+0.125014`, 95% CI
    `[-0.096354, +0.344350]`;
  - Brier delta `+0.047634`, 95% CI
    `[-0.071297, +0.166694]`.
- GPT-4 unknown, 12D vs word:
  - NLL delta `+0.157602`, 95% CI
    `[-0.029704, +0.344763]`;
  - Brier delta `+0.086650`, 95% CI
    `[-0.014289, +0.182306]`.
- Mistral unknown, 12D vs word:
  - NLL delta `+0.085230`, 95% CI
    `[-0.243367, +0.426609]`;
  - Brier delta `-0.002299`, 95% CI
    `[-0.157577, +0.152231]`.

Therefore M2 does not support a claim of statistically resolved per-fold
proper-score superiority for any 12D comparison.

The aggregate point-estimate ordering should not be converted into a pooled
significance claim without a separately specified cross-fold estimand.

## Temperature-scaling result

The temperature experiment produced a useful negative result.

### CogniPrint 12D

Fitted temperatures by unknown fold:

- ChatGPT: `0.517396`;
- GPT-4: `0.534324`;
- Llama-chat: `0.381979`;
- Mistral-chat: `0.360158`.

Mean held-out NLL:

- before temperature scaling: `1.277792`;
- after temperature scaling: `1.348983`.

Held-out NLL worsened in all four folds.

Mean held-out Brier:

- before: `0.692123`;
- after: `0.710081`.

Brier worsened in three folds and improved only in the Mistral fold.

Top-label ECE improved on average
(`0.226980 -> 0.210194`), illustrating why ECE alone must not be treated as
primary calibration evidence.

**Conclusion:** the present temperature procedure does not improve 12D
probability quality on held-out M2 data.

### N-gram representations

For both character and word n-grams, every fitted temperature hit the lower
bound `T = 0.05`.

Held-out means improved substantially:

- char NLL: `1.376663 -> 1.241039`;
- char Brier: `0.745172 -> 0.673324`;
- word NLL: `1.377229 -> 1.234877`;
- word Brier: `0.745452 -> 0.670327`.

This is not automatically evidence that `0.05` is an optimal physical
temperature. Repeated boundary hits indicate that cosine-similarity score
scale and temperature-bound sensitivity deserve a separately specified
follow-up analysis.

The primary M2 result must retain the frozen bound and must not be retroactively
retuned.

## Conformal result: important interpretation limit

At alpha `0.05`, known-class prediction-set coverage was high, but singleton
rates were extremely low.

Four-fold mean known singleton rates:

- 12D: `0.005814` (~0.6%);
- char 3–5: `0.027997` (~2.8%);
- word 1–2: `0.060995` (~6.1%).

Mean known prediction-set coverage:

- 12D: `0.933450`;
- char 3–5: `0.989186`;
- word 1–2: `0.972817`.

Mean conformal false-known rates on the held-out machine families were near
zero:

- 12D: `0.0025`;
- char 3–5: `0.0000`;
- word 1–2: `0.0050`.

These low false-known values must **not** be presented as proof of strong OOD
recognition. The current evaluator treats both an empty conformal set and a
multi-class ambiguous set as non-known/rejected for unknown examples, while
known examples themselves are almost always ambiguous.

The result is therefore better interpreted as:

> the alpha-0.05 class-conditional conformal layer is extremely conservative
> on this small Stage A design and rarely emits a singleton claim.

A post-result follow-up may separately measure unknown empty-set rate versus
unknown ambiguous-set rate. That follow-up must be labeled post hoc and must
not replace the frozen M2 result.

## Max-confidence open-set result

The simpler frozen max-confidence rule also does not demonstrate useful
open-set separation.

Mean false-known rates:

- 12D: `0.6575`;
- char 3–5: `0.4850`;
- word 1–2: `0.5125`.

Mean known-vs-unknown AUROC:

- 12D: `0.5117`;
- char 3–5: `0.5398`;
- word 1–2: `0.5329`.

These values are weak and close to chance-level ranking in aggregate. M2 does
not support a claim that maximum calibrated class probability is a reliable
OOD detector here.

## Scientific conclusion

The first real M2 result is **negative / mixed**, not a 12D win.

It supports five bounded conclusions:

1. The current compact 12D representation is not the strongest tested
   representation on the real pinned RAID Stage A M2.
2. N-gram representations have better aggregate point estimates for closed-set
   and most probability/selective metrics, but the per-fold proper-score
   bootstrap intervals are too wide to claim resolved 12D-vs-baseline
   superiority/inferiority from those intervals alone.
3. Temperature scaling improves the n-gram score quality under the frozen
   procedure but degrades held-out 12D NLL, so “temperature scaling improves
   CogniPrint calibration” is rejected for this M2 run.
4. Max-confidence thresholding has high false-known rates and is not adequate
   open-set evidence.
5. The alpha-0.05 conformal layer is conservative enough to suppress
   false-known singleton claims, but its very low known singleton rate means
   this is not yet a useful practical attribution rule or proof of OOD
   detection.

The result strengthens the paper's core question **When Not to Attribute**:
the current evidence favors abstention and claim narrowing rather than stronger
source-attribution claims.

## Claim boundary

This result does not establish:

- exact generating model identity for arbitrary text;
- universal AI-generated-text detection;
- authorship;
- operator or commissioner identity;
- intent or responsibility;
- legal or forensic provenance;
- production readiness;
- Stage B authorization.

Readiness remains `descriptive_only`.
