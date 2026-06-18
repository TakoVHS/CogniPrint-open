# Human Paraphrase V1

Status: descriptive mathematical diagnostic.
Readiness boundary: `descriptive_only`.

This folder implements the human-paraphrase experiment pipeline. The default
real-data command streams bounded samples from public Hugging Face datasets via
`datasets.load_dataset`. The explicit `--use-seed-fixtures` mode is only for
fast CI/smoke tests.

## Dataset Sources

- `cointegrated`: cointegrated/ru-paraphrase-NMT-Leipzig (CC-BY-4.0) - https://huggingface.co/datasets/cointegrated/ru-paraphrase-NMT-Leipzig
- `inkoziev`: inkoziev/paraphrases (CC-BY-NC-4.0) - https://huggingface.co/datasets/inkoziev/paraphrases
- `paws`: google-research-datasets/paws (Google Research PAWS public benchmark; freely usable per dataset documentation) - https://huggingface.co/datasets/google-research-datasets/paws
- `parisci`: HHousen/ParaSCI (public Hugging Face dataset card; verify upstream license before redistribution) - https://huggingface.co/datasets/HHousen/ParaSCI

Generated or machine-assisted sources are marked in `pair_source`; they are not
described as independently written human paraphrases.

## Reproduction

```bash
make human-paraphrase-real
make human-paraphrase-test
```

Equivalent direct command:

```bash
PYTHONPATH=src .venv/bin/python scripts/generate_human_paraphrase_v1.py \
  --datasets cointegrated,inkoziev,paws \
  --limit-per-source 40 \
  --random-pairs 300
```

## Inputs

- pair file: `validation/human-paraphrase-v1/pairs.csv`
- pair count: 120
- pair sources: `{'generated_paraphrase_round_trip_translation': 40, 'generated_or_curated_paraphrase_group': 40, 'adversarial_paraphrase_benchmark': 40}`
- source datasets: `{'cointegrated/ru-paraphrase-NMT-Leipzig': 40, 'inkoziev/paraphrases': 40, 'google-research-datasets/paws': 40}`
- source license notes: `['CC-BY-4.0', 'CC-BY-NC-4.0', 'Google Research PAWS public benchmark; freely usable per dataset documentation']`
- random-pair count: 300

## Outputs

- `pairs.csv`
- `results.csv`
- `random-pair-distances.csv`
- `summary.json`
- `distribution.svg`

## Current Diagnostic Summary

- mean pair Euclidean distance: 0.224497
- median pair Euclidean distance: 0.174267
- mean random-pair Euclidean distance: 0.798899
- Euclidean p<0.05 count: 76

## Boundary

These outputs do not establish validation, author identity, text origin,
AI-origin, legal status, forensic status, or a universal threshold.
