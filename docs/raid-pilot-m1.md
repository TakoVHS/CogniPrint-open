# M1 RAID pilot — external model-family stress test

Status: executable pilot protocol with verified local evidence on Wednesday, July 29, 2026. Readiness remains `descriptive_only`, research status remains `PRE-FREEZE`, and Challenge 001 Stage B remains `NOT_AUTHORISED_TO_START`.

## Why RAID

RAID is an independently maintained MIT-licensed benchmark for AI-generated-text detection. Its public dataset includes human controls plus outputs from multiple model families, domains, decoding settings, and adversarial transformations.

Sources:

- Dataset: https://huggingface.co/datasets/liamdugan/raid
- Repository: https://github.com/liamdugan/raid
- Paper: https://aclanthology.org/2024.acl-long.674/
- Pinned dataset revision: `865cac74188466cb0c3b7574a10204007b57a459`
- Authoritative raw clean-train source contract: [raid-source-contract-m1.md](./raid-source-contract-m1.md)

The pinned Hugging Face revision remains the benchmark revision boundary for the adapter and tests. The local evidence run on Wednesday, July 29, 2026 additionally pins the authoritative published clean-train CSV by URL, byte size, and SHA-256 through a separate source contract.

Using RAID gives CogniPrint an external test bed that was not constructed to make the current 12-dimensional fingerprint look good.

## Pilot A — clean English model-family matrix

The first executable pilot deliberately fixes several obvious confounders:

- dataset config: `raid`;
- authoritative raw source: `https://dataset.raid-bench.xyz/train_none.csv`;
- model classes: `human`, `chatgpt`, `gpt4`, `llama-chat`, `mistral-chat`;
- domains: `abstracts`, `news`, `reviews`, `wiki`;
- machine decoding: `sampling`;
- repetition penalty: `no`;
- adversarial attack: `none`;
- target: 25 samples per `model × domain` cell;
- expected balanced total: 500 feature records.

The adapter computes CogniPrint features in memory and writes only metadata, hashes, and feature values. It does not copy raw RAID generations or prompts into the evidence directory or repository.

## Authoritative local evidence on Wednesday, July 29, 2026

The current local evidence run materialized the pilot from the authoritative published clean-train CSV and not from a partial parquet fragment or an inferred subset.

Observed outputs:

- `500` metadata-only feature records;
- `20` populated `model × domain` cells;
- `25` records per cell;
- `467985` scanned source rows before satisfying all quotas;
- source SHA-256 `c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4`;
- source repository revision `7cfcefef239323e6fa1ec43d1a6ecc815c8b8642`;
- evidence code commit `9d9ba5e2c34740c42864eb2810272dbc2652d69c`.

Baseline metrics from the metadata-only pilot:

- grouped split: `351` train records / `149` test records;
- grouped lineage counts: `336` train groups / `145` test groups;
- chance accuracy reference: `0.200000`;
- majority baseline: accuracy `0.161074`, balanced accuracy `0.200000`, macro-F1 `0.055491`;
- length-only nearest centroid: accuracy `0.295302`, balanced accuracy `0.302231`, macro-F1 `0.247431`;
- CogniPrint 12D nearest centroid: accuracy `0.536913`, balanced accuracy `0.542001`, macro-F1 `0.535883`.

These are descriptive benchmark-bounded baselines. They are not calibrated confidence estimates, not forensic attribution, and not a claim that the system can identify the exact generating model on arbitrary text.

## Prepare the feature evidence

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[real-data]'

RAID_SOURCE=/path/to/train_none.csv
RAID_CONTRACT=/path/to/RAID_SOURCE_CONTRACT_001.json

python scripts/prepare_raid_pilot.py \
  --input-file "$RAID_SOURCE" \
  --expected-source-sha256 c5467bca6fc7f5c728c676450c7f84ce401df6c6ccc6d82c47e3b5f3c6d6fce4 \
  --source-contract "$RAID_CONTRACT" \
  --models human,chatgpt,gpt4,llama-chat,mistral-chat \
  --domains abstracts,news,reviews,wiki \
  --per-cell 25 \
  --seed 20260725 \
  --output-dir evidence/model-fingerprint-m1/raid-pilot
```

This authoritative path verifies the local raw file against the expected SHA-256 and the machine-readable source contract before scanning it. The raw CSV remains outside the repository and outside the metadata-only evidence bundle. The pinned Hugging Face revision remains a benchmark revision boundary; it is not a substitute for the complete raw-source custody pin.

## Feature outputs

`features.jsonl` contains one metadata-only record per selected source sample:

- external source IDs and lineage IDs;
- model family and domain;
- decoding/repetition/attack metadata;
- SHA-256 of generation and prompt where available;
- text length diagnostics;
- CogniPrint fingerprint version;
- raw and normalized 12-dimensional feature dictionaries;
- `descriptive_only` readiness boundary.

`summary.json` records the source, config, immutable revision, selection policy, seed, row counts, fingerprint version, source contract hash, and cell balance.

## First analysis

Run the transparent baseline layer before introducing a learned detector:

```bash
python scripts/analyze_raid_pilot.py \
  --features evidence/model-fingerprint-m1/raid-pilot/features.jsonl \
  --output-dir evidence/model-fingerprint-m1/raid-pilot \
  --test-fraction 0.30 \
  --seed 20260725
```

The analysis keeps related samples together using `source_id`, then `prompt_sha256`, then `text_sha256` as the fallback lineage key. A lineage group can occur in train or test, never both.

It produces:

- `baseline-metrics.json` — machine-readable split counts, class counts, confusion matrices, balanced accuracy and macro F1;
- `baseline-report.md` — compact reviewer-facing summary.

The first committed comparison is deliberately simple:

1. chance accuracy reference;
2. majority baseline;
3. length-only nearest-centroid baseline using character/token counts;
4. current 12-dimensional CogniPrint nearest-centroid baseline.

Both numeric baselines are standardized using training data only. The nearest-centroid outputs are uncalibrated labels, not probabilities and not calibrated confidence scores.

Character and word n-gram baselines should be evaluated in a second in-memory analysis that has access to RAID source text. Raw RAID text should not be committed merely to make those baselines convenient.

## Pilot B — robustness

After Pilot A is frozen, use RAID adversarial variants to measure degradation rather than silently mixing them into training. Prioritize paraphrase and other transformations that preserve much of the apparent semantic content.

A useful result may be that the current fingerprint loses model-family information under these transformations. That is a valid negative result and should be reported.

## Multilingual boundary

RAID also includes Czech and German material. CogniPrint v2 currently uses a deliberately simple dependency-light tokenizer and syllable heuristic that have not been validated for Czech/German diacritics and readability measurement.

Therefore the default RAID pilot is English-only. A multilingual benchmark must either:

- validate the existing feature map language by language;
- introduce a separately versioned Unicode or multilingual feature map and compare it against v2.

Do not describe the current RAID adapter as multilingual validation.

## Claim boundary

This pilot tests whether current features contain benchmark-bounded information associated with known RAID source classes under controlled conditions.

It does not establish:

- that an arbitrary text was generated by AI;
- the unique model that generated an arbitrary text;
- authorship identity;
- who requested or commissioned generation;
- intent or responsibility;
- legal or forensic provenance;
- production readiness;
- Stage B authorization.

Any eventual attribution output must be calibrated, allow abstention, and be tested against unseen models and transformations before the public claim scope can expand.
