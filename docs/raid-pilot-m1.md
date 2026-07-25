# M1 RAID pilot — external model-family stress test

Status: executable pilot protocol. No RAID data or model-attribution result is bundled in this document.

## Why RAID

RAID is an independently maintained MIT-licensed benchmark for AI-generated-text detection. Its public dataset includes human controls plus outputs from multiple model families, domains, decoding settings, and adversarial transformations.

Sources:

- Dataset: https://huggingface.co/datasets/liamdugan/raid
- Repository: https://github.com/liamdugan/raid
- Paper: https://aclanthology.org/2024.acl-long.674/
- Pinned dataset revision: `865cac74188466cb0c3b7574a10204007b57a459`

The pinned revision is the verified Hugging Face commit that updates the dataset configs to `raid` and `raid_test`. Using an immutable revision prevents the pilot from silently changing if the dataset repository changes later.

Using RAID gives CogniPrint an external test bed that was not constructed to make the current 12-dimensional fingerprint look good.

## Pilot A — clean English model-family matrix

The first executable pilot deliberately fixes several obvious confounders:

- dataset config: `raid`;
- split: `train`;
- model classes: `human`, `chatgpt`, `gpt4`, `llama-chat`, `mistral-chat`;
- domains: `abstracts`, `news`, `reviews`, `wiki`;
- machine decoding: `sampling`;
- repetition penalty: `no`;
- adversarial attack: `none`;
- target: 25 samples per `model × domain` cell;
- expected balanced total: 500 feature records.

The adapter computes CogniPrint features in memory and writes only metadata, hashes, and feature values. It does not copy raw RAID generations or prompts into the evidence directory.

## Prepare the feature evidence

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[real-data]'
python scripts/prepare_raid_pilot.py \
  --split train \
  --revision 865cac74188466cb0c3b7574a10204007b57a459 \
  --per-cell 25 \
  --output-dir evidence/model-fingerprint-m1/raid-pilot
```

The script uses that immutable revision by default; it is shown explicitly in the command so a reviewer can see the data boundary without reading source code. Record the exact CogniPrint commit SHA together with the output.

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

`summary.json` records the source, config, immutable revision, selection policy, seed, row counts, fingerprint version, and cell balance.

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

Both numeric baselines are standardized using **training data only**. The nearest-centroid outputs are uncalibrated labels; probability-quality metrics and abstention thresholds belong to a later explicitly calibrated stage.

Character and word n-gram baselines should be evaluated in a second in-memory analysis that has access to RAID source text. Raw RAID text should not be committed merely to make those baselines convenient.

## Pilot B — robustness

After Pilot A is frozen, use RAID adversarial variants to measure degradation rather than silently mixing them into training. Prioritize paraphrase and other transformations that preserve much of the apparent semantic content.

A useful result may be that the current fingerprint loses model-family information under these transformations. That is a valid negative result and should be reported.

## Multilingual boundary

RAID also includes Czech and German material. CogniPrint v2 currently uses a deliberately simple dependency-light tokenizer and syllable heuristic that have not been validated for Czech/German diacritics and readability measurement.

Therefore the default RAID pilot is English-only. A multilingual benchmark must either:

- validate the existing feature map language by language; or
- introduce a separately versioned Unicode/multilingual feature map and compare it against v2.

Do not describe the current RAID adapter as multilingual validation.

## Claim boundary

This pilot tests whether current features contain benchmark-bounded information associated with known RAID source classes under controlled conditions.

It does not establish:

- that an arbitrary text was generated by AI;
- the unique model that generated an arbitrary text;
- authorship identity;
- who requested or commissioned generation;
- intent or responsibility;
- legal or forensic provenance.

Any eventual attribution output must be calibrated, allow abstention, and be tested against unseen models and transformations before the public claim scope can expand.
