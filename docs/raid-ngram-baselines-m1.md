# M1 RAID pilot — privacy-preserving n-gram baselines

Status: executed local Stage A development evidence on Wednesday, July 29, 2026. Readiness remains `descriptive_only`, research mode remains `PROOF_MODE`, research status remains `PRE-FREEZE`, and Challenge 001 Stage B remains `NOT_AUTHORISED_TO_START`.

## Purpose

The completed RAID Pilot A showed that the current 12-dimensional CogniPrint representation outperformed the majority and length-only baselines on the fixed 500-record benchmark slice. That result was still incomplete: conventional lexical and surface-form baselines might carry more model-family signal than the compact 12D representation.

This protocol adds two deliberately fixed comparisons without changing the Pilot A source, selected records, grouped split, seed, or scientific claim boundary:

- character n-grams of lengths 3–5;
- word n-grams of lengths 1–2.

## Frozen input boundary

The n-gram run reuses the completed Pilot A artifacts:

- authoritative source: official RAID `train_none.csv`;
- source SHA-256: `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- source byte size: `801662741`;
- source-contract SHA-256: `e0efa8ddf06861e0fbfd2ccb76313e9451986592b5d007a7cb71d30503fd9948`;
- selected metadata-only features SHA-256: `13faba4a3efaa1c7f88761722f146b7eb654fd08e4b833f2d7768a0ff45646ca`;
- selected-record manifest SHA-256: `30685ed738c3f1f1074a1f89a67a504f0c9d0607b958894e385172623591f6cb`;
- 500 selected records across 20 cells, 25 per cell;
- seed `20260725`;
- test fraction `0.30`;
- grouped lineage split based on `source_id`, then `prompt_sha256`, then `text_sha256`.

The prior evidence archive is:

`cogniprint-stage-a-raid-complete-20260729-072317.tar.gz`

with SHA-256:

`9f7a0c39f24ee71539cb74d896d204e4220261dc1ddfa2343b44d2ac72a04a82`

## Privacy-preserving design

The analyzer streams the pinned raw CSV and rehydrates only the 500 selected source rows. Every selected generation is verified against the persisted `text_sha256`; prompts are verified by hash where present.

Raw source material is used only in memory. The implementation does not persist:

- generation text;
- prompt text;
- token lists;
- n-gram strings;
- recoverable vocabulary;
- sparse document vectors.

Permitted outputs are aggregate protocol settings, source and selection hashes, split counts, occupied hash-bin counts, classification metrics, per-class metrics, confusion matrices, and reproducibility hashes.

## Fixed feature protocol

### Character baseline

- Unicode normalization: NFKC;
- case normalization: `casefold`;
- whitespace: collapsed to single spaces;
- n-gram lengths: 3–5;
- hashing: SHA-256 into `262144` non-negative bins;
- term frequency: `1 + log(count)`;
- IDF: fitted on training records only using `log((1+n_train)/(1+df))+1`;
- document normalization: L2;
- classifier: cosine nearest centroid;
- deterministic lexical label tie-break.

### Word baseline

- the same Unicode, case, TF, IDF, normalization, classifier, and tie-break policy;
- word n-gram lengths: 1–2;
- hashing: SHA-256 into `131072` non-negative bins.

These parameters are fixed before the real test metrics are observed. They are not tuned against the held-out Pilot A test partition.

## Executed local evidence on Wednesday, July 29, 2026

The fixed-source local run verified:

- exact authoritative source byte size and SHA-256;
- exact prior evidence archive SHA-256;
- exact selected-features SHA-256;
- exact selected-record manifest SHA-256;
- exact source-contract SHA-256;
- exact 500/500 record rehydration;
- zero train/test lineage overlap on the reused grouped split;
- deterministic two-run equality for metrics and rehydration audit outputs.

Split counts remained:

- train/test records: `351 / 149`;
- train/test lineage groups: `336 / 145`;
- lineage overlap: `0`.

## Results

Comparison on the fixed Pilot A split:

- chance accuracy reference: `0.200000`;
- majority: accuracy `0.161074`, balanced accuracy `0.200000`, macro-F1 `0.055491`;
- length-only nearest centroid: accuracy `0.295302`, balanced accuracy `0.302231`, macro-F1 `0.247431`;
- CogniPrint 12D nearest centroid: accuracy `0.536913`, balanced accuracy `0.542001`, macro-F1 `0.535883`;
- character 3–5 hashed TF-IDF: accuracy `0.583893`, balanced accuracy `0.590475`, macro-F1 `0.578782`;
- word 1–2 hashed TF-IDF: accuracy `0.597315`, balanced accuracy `0.601996`, macro-F1 `0.595220`.

Within this fixed descriptive pilot, both conventional n-gram baselines outperformed the current 12D representation. The strongest of the tested baselines was word `1–2` hashed TF-IDF.

## Interpretation boundary

A stronger n-gram result shows that conventional lexical or surface-form features outperform the compact CogniPrint 12D representation on this controlled benchmark slice. It does not prove general model attribution.

All outputs remain uncalibrated Stage A diagnostics. They do not establish exact model identity, AI origin, authorship, operator identity, commissioner identity, intent, responsibility, legal provenance, or forensic provenance. They do not authorize Stage B or change the project from `PRE-FREEZE`.
