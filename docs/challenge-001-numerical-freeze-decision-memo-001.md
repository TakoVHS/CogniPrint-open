# Challenge 001 — Numerical Freeze Decision Memo 001

Status: **CANDIDATE / HOLD / NOT FROZEN / STAGE B NOT AUTHORISED**

Canonical base commit: `d154b8610b182fe9110bf52fcadf02914498d356`

Machine-readable candidate:

`challenge-001/protocol/frozen/NUMERICAL_FREEZE_DECISIONS_001.candidate.json`

This memo prepares issue #49. It does not change `RESEARCH_FREEZE_001.md`, submit an OSF registration, create Stage B data, reveal labels, or authorise predictions.

## 1. Why the candidate is deliberately narrow

Stage A used 500 records from the pinned RAID source with a grouped `351 / 149` split, `336 / 145` lineage groups and zero lineage overlap. Its fixed comparison produced:

| Representation | Balanced accuracy | Macro-F1 |
| --- | ---: | ---: |
| CogniPrint 12D | `0.542001` | `0.535883` |
| Character 3–5 n-grams | `0.590475` | `0.578782` |
| Word 1–2 n-grams | `0.601996` | `0.595220` |

Both conventional n-gram baselines were stronger than 12D on Pilot A. Therefore Challenge 001 cannot be designed around a promised 12D win. It must:

- allow a negative result;
- compare 12D directly with transparent lexical baselines;
- keep the public claim locked when n-grams explain the signal;
- test `UNKNOWN` and false-known behaviour as primary safety properties;
- remain English-only and domain-bounded for the first challenge.

Stage A source and evidence hashes are recorded in the machine-readable candidate.

## 2. Evidence-backed values versus policy values

### Evidence-backed

The following values are imported from executed Stage A evidence and are not newly inferred:

- source SHA-256;
- selected-record and selected-feature hashes;
- 500 selected records;
- grouped split and zero overlap;
- chance, majority, length-only, 12D, character n-gram and word n-gram metrics;
- conclusion that word `1–2` was the strongest tested Pilot A representation.

### Prospective policy choices

The following values are conservative design choices made before Stage B and are not presented as empirical facts:

- English-only scope;
- four domains and six task strata;
- three length bins beginning at 128 words;
- source-family candidate set;
- exact per-cell sample counts;
- separate probability and conformal calibration partitions;
- conformal alpha `0.05`;
- calibration acceptance thresholds;
- false-known, coverage and claim-narrowing thresholds;
- T0 as the only primary transformation track;
- T1 as a preregistered secondary track;
- exclusion and deterministic replacement rules.

Every policy value is allowed to be criticised before freeze. It cannot be changed after sealed predictions exist.

## 3. Candidate source scope

### Known reference classes

1. `human_pre2020_verified`;
2. `meta-llama/Llama-3.1-8B-Instruct` at candidate revision `0e9e39f249a16976918f6564b8830bc894c89659`;
3. `mistralai/Mistral-7B-Instruct-v0.3` at candidate revision `c170c708c41dac9275d15a8fff4eca08d52bab71`;
4. `Qwen/Qwen2.5-7B-Instruct` at candidate revision `a09a35458c702b33eeacc393d103063234e8bc28`.

### Held-out unknown class

- `tiiuae/Falcon3-7B-Instruct` at candidate revision `bed191412b3197aeb74587298fc351739ca10210`.

These are candidate immutable open-weight artifacts rather than moving hosted API aliases. The selection is prospective and not informed by Stage B outcomes.

Before this list can become frozen:

- each revision must resolve locally to the same artifact;
- config, tokenizer, generation config and relevant weight-manifest hashes must be archived;
- access and licence terms must be reviewed;
- the gated Llama access requirement must be satisfied without placing credentials in the repository;
- Falcon licensing must receive explicit review;
- no source may be silently substituted because it is inconvenient or performs poorly.

### Human control

The candidate definition is English prose first published from 2010 through 2019 with documented human provenance, one author-document lineage per sample and no known machine-generation exposure.

This definition is not enough by itself. The exact human source registry remains an unresolved blocker and must be materialised, licensed and independently reviewed before freeze.

## 4. Candidate sample design

The design crosses:

- 4 domains;
- 6 task strata;
- 3 length strata.

This creates `72` frozen cells.

For every known class and every cell, collect six independent lineages:

- 3 reference;
- 1 probability calibration;
- 1 conformal calibration;
- 1 sealed known test.

For the held-out unknown class, collect three sealed lineages per cell.

### Exact counts

| Partition | Count |
| --- | ---: |
| Per known class | `432` |
| Reference per known class | `216` |
| Probability calibration per known class | `72` |
| Conformal calibration per known class | `72` |
| Sealed known test per known class | `72` |
| All four known classes | `1728` |
| Held-out unknown sealed test | `216` |
| Clean T0 total | `1944` |
| Sealed clean T0 total | `504` |

The held-out unknown count of `216` gives a false-known estimate near `0.10` an approximate two-sided 95% Wilson half-width of about `0.04`. Per-known-class sealed estimates remain coarse at `72` samples and must always include uncertainty intervals.

Partitioning is by strongest available lineage, never individual row. Within each cell/source, lineages are deterministically ordered using SHA-256 and seed `20260730`.

## 5. Length and minimum evidence

Primary length bins:

- short: `128–255` words;
- medium: `256–511` words;
- long: `512–900` words.

A primary sample must contain at least:

- `128` normalized words;
- `600` Unicode letters.

A shorter output is not silently discarded. After at most three frozen generation attempts it receives:

`UNKNOWN_INSUFFICIENT_EVIDENCE`

It remains in coverage and insufficient-evidence denominators.

This threshold is a conservative policy choice, not a Stage A-derived optimum. Stage B may not be used to tune it.

## 6. UNKNOWN / OOD method

The candidate uses class-conditional split conformal prediction over cosine nonconformity:

`nonconformity = 1 - cosine_similarity(sample, class_centroid)`

For every class, conformal p-values are calculated from the dedicated conformal calibration partition. Alpha is fixed at `0.05`.

A known-family decision is permitted only when:

1. minimum evidence passes; and
2. exactly one known class has `p > 0.05`.

Otherwise:

- no passing class → `UNKNOWN_OOD`;
- multiple passing classes → `UNKNOWN_AMBIGUOUS`;
- evidence failure → `UNKNOWN_INSUFFICIENT_EVIDENCE`.

Any known-class assignment for the fully held-out Falcon family is a false-known event.

Conformal p-values are not class probabilities and must not be described as confidence percentages.

## 7. Probability calibration

Probability calibration is separate from the conformal decision gate.

Candidate method:

- single-temperature softmax over frozen class scores;
- fit only on the probability-calibration partition;
- temperature restricted to `[0.05, 20.0]`;
- objective: multiclass negative log-likelihood;
- ECE: 15 equal-frequency bins.

Probability-like wording is allowed only when all are true:

- ECE `<= 0.10`;
- calibrated NLL is no worse than uncalibrated NLL;
- calibrated Brier score is no worse than uncalibrated Brier score;
- each known class has at least 50 calibration samples.

Failure leaves calibrated-confidence language locked. The conformal UNKNOWN mechanism may still be evaluated because it is separately frozen.

## 8. Baselines

The primary comparison includes exactly:

1. uniform known-class chance expectation (`0.25` for four known classes);
2. reference-partition majority;
3. length-only nearest centroid;
4. fixed 12-feature punctuation/surface nearest centroid;
5. current CogniPrint 12D nearest centroid;
6. fixed character 3–5 hashed TF-IDF nearest centroid;
7. fixed word 1–2 hashed TF-IDF nearest centroid.

The n-gram settings match the executed Stage A protocol. No primary learned representation may be added after prediction freeze.

## 9. Primary metrics

Known sealed T0:

- Top-1 accuracy with UNKNOWN counted as incorrect;
- balanced accuracy with UNKNOWN counted as incorrect;
- macro-F1 with `zero_division=0` and UNKNOWN counted as a false negative;
- per-class precision/recall/F1;
- confusion matrix with an UNKNOWN prediction column.

Open-world:

- known coverage;
- selective accuracy and risk;
- unknown rejection;
- false-known rate;
- insufficient-evidence rate.

Uncertainty:

- two-sided 95% Wilson intervals for proportions;
- 10,000 lineage-group paired bootstrap resamples for system differences;
- deterministic bootstrap seed `20260730`.

No best-stratum result may replace the frozen overall result.

## 10. Stop and claim-narrowing decisions

| Gate | Exact candidate condition | Consequence |
| --- | --- | --- |
| False-known | point `> 0.10` or Wilson upper `> 0.15` | open-world claim locked |
| Unknown rejection | `< 0.90` | UNKNOWN/OOD effectiveness claim locked |
| Known coverage | `< 0.60` | no operational attribution claim |
| Known signal | best system BA `< 0.50` or macro-F1 `< 0.50` | no family-level discrimination claim |
| 12D vs n-gram | paired 95% CI for macro-F1 delta includes/below zero, or point delta `< 0.02` | no claim that 12D adds value beyond n-grams |
| Per-class collapse | any recall `< 0.40` | result labelled mixed; collapsed classes named |
| Calibration | ECE `> 0.10`, or calibrated NLL/Brier worsens | calibrated-confidence claim locked |
| Domain collapse | any domain BA `< 0.40`, or `> 0.15` below overall | cross-domain claim locked |
| Missing sealed cell | any frozen cell lacks an eligible primary sample | protocol deviation; incomplete primary run |
| T1 degradation | BA drop `> 0.15` or false-known rise `> 0.05` | no light-edit robustness claim |

A failed gate does not erase the run. It narrows the permitted public conclusion.

## 11. Transformation boundary

Primary analysis includes only `T0_CLEAN`.

Secondary preregistered track:

- `T1_LIGHT_HUMAN_EDIT`;
- exactly one medium-length sealed lineage per domain × task pair × source class;
- `120` T1 derived samples total;
- at most 10% token replacement;
- punctuation/typo/local lexical edits only;
- no sentence reordering, addition or removal;
- parent and edit-log hashes preserved.

T2 through T6 are excluded from Challenge 001. They require a later challenge and cannot be added after results are visible.

## 12. Exclusion boundary

Permitted before prediction only:

- unreadable artifact or hash mismatch;
- licence/consent failure;
- exact duplicate;
- frozen MinHash near-duplicate threshold `>= 0.90`;
- label/source leak in predictor-visible metadata;
- lineage or prompt partition violation.

Not permitted as exclusions:

- refusal;
- poor style;
- difficult sample;
- unfavourable prediction;
- inconvenient class behaviour.

Before prediction, an excluded candidate may be replaced only with the next entry in a precommitted reserve list. After prediction starts, no replacement is allowed.

## 13. Why this is still HOLD

The numerical table is substantially specified, but a real freeze is not yet justified. Remaining blockers:

1. exact human-control manifest;
2. local immutable revision resolution and artifact hashes for all model candidates;
3. licence/access review;
4. development-only implementation and validation of surface, conformal, calibration and interval methods;
5. independent methodological review;
6. issue #30 executed runner record or formally accepted equivalent;
7. candidate blinded/sealed manifests;
8. real zero-overlap Stage A/B leakage audit;
9. final Research Lock;
10. external timestamped registration.

Until every blocker is resolved:

```text
RESEARCH_FREEZE = PRE-FREEZE
PREREGISTRATION = NOT_SUBMITTED
STAGE_B = NOT_AUTHORISED_TO_START
```

## 14. Review questions

The independent reviewer should challenge at least:

- whether `128` words is defensible as a policy floor;
- whether `72` sealed samples per known class are sufficient;
- whether the conformal exactly-one-class rule is too conservative;
- whether alpha `0.05`, false-known `0.10`, coverage `0.60` and BA/F1 `0.50` are scientifically coherent;
- whether model families are sufficiently distinct and operationally reproducible;
- whether pre-2020 human controls introduce domain/source artifacts;
- whether the T1 edit protocol is reproducible;
- whether any threshold accidentally rewards excessive abstention.

Criticism must occur before freeze. Changes after sealed predictions require a new versioned challenge.
