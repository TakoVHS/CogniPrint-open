# RAID source contract — M1 Pilot A

Status: authoritative local source contract recorded on Wednesday, July 29, 2026. Research state remains `PRE-FREEZE`, readiness remains `descriptive_only`, and Challenge 001 Stage B remains `NOT_AUTHORISED_TO_START`.

## Purpose

This note records the exact external raw source used for the local RAID Pilot A evidence rerun so reviewers can distinguish:

- the benchmark revision boundary;
- the raw-file custody boundary;
- the metadata-only publication boundary.

The goal is reproducibility and provenance discipline, not a claim of scientific validation by itself.

## Authoritative source

The local evidence run used the published clean-train CSV referenced by the official RAID repository README:

- repository landing page: `https://github.com/liamdugan/raid`
- repository revision observed on Wednesday, July 29, 2026: `7cfcefef239323e6fa1ec43d1a6ecc815c8b8642`
- published download URL: `https://dataset.raid-bench.xyz/train_none.csv`
- final resolved URL at acquisition: `https://dataset.raid-bench.xyz/train_none.csv`
- acquisition time (UTC): `2026-07-29T07:25:30Z`
- byte size: `801662741`
- SHA-256: `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`
- HTTP ETag at acquisition: `"a3b0661bddab1f7e63499e8f309c5eb4-8"`
- HTTP Last-Modified at acquisition: `Tue, 04 Jun 2024 20:20:08 GMT`
- license context used by the adapter: `MIT`

The benchmark revision boundary for the adapter and tests remains the pinned Hugging Face dataset revision `865cac74188466cb0c3b7574a10204007b57a459`.

## Why not partial parquet or inferred subsets

A partial parquet extract, ad hoc slice, or inferred subset was rejected for Pilot A evidence because it would weaken provenance and can silently distort per-cell availability.

The accepted source needed all of the following at once:

- a published upstream location referenced by the official RAID project;
- a stable raw-file SHA-256;
- a stable byte-size check;
- enough clean-train rows to satisfy the fixed `5 × 4 × 25 = 500` matrix without hidden substitutions.

Using the authoritative published clean-train CSV preserves a reviewer-auditable chain from upstream source to metadata-only evidence.

## Materialization boundary

The local materializer computes features in memory and writes only:

- source identifiers;
- lineage identifiers;
- metadata fields such as model family, domain, decoding, repetition penalty, and attack;
- SHA-256 hashes of prompt and generation where available;
- character and token counts;
- CogniPrint feature values.

It does not commit or export raw RAID generations or raw prompts into the public repository or final evidence bundle.

## Local evidence outcome

The local authoritative run on Wednesday, July 29, 2026 produced:

- `500` metadata-only records;
- `20` populated cells;
- `25` records per cell;
- `467985` scanned rows before quota completion;
- `500` unique text hashes in the selected metadata-only evidence;
- no train/test lineage overlap in the grouped analysis split.

These outputs support a descriptive benchmark-bounded Pilot A record. They do not authorize Stage B, do not create a freeze by themselves, and do not establish forensic or authorship claims.

## Remaining boundary

This source contract closes the raw-source provenance gap for the local RAID Pilot A evidence rerun, but it does not close the remaining freeze checklist. The project is still missing the full pre-registered Stage B specification, including unknown-family handling, calibration, n-gram baselines, exclusion rules, numerical stop criteria, and sealed custody implementation.
