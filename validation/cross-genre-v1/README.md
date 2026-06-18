# Cross Genre V1

Status: descriptive mathematical diagnostic.
Readiness boundary: `descriptive_only`.

This folder implements a cross-genre stress test. In real-data mode it uses the
PAN15 Author Identification / Verification dataset from Zenodo:

- record: https://zenodo.org/records/3737563
- file: `pan15-authorship-verification-test-and-training.zip`
- checksum used by the preparer: `md5:0ee8837ff58fe43e1c5f2e004484e8d7`
- source license note: `['Zenodo open dataset record; verify reuse terms before redistribution']`

PAN15 exposes verification problems, not a clean author-by-genre table. The
Dutch and Spanish prefixes are documented by PAN15 as cross-genre problems, so
the experiment compares known-vs-questioned documents for same-author (`Y`) and
cross-author (`N`) verification cases.

## Reproduction

```bash
make cross-genre-real
make cross-genre-test
```

Equivalent direct commands:

```bash
PYTHONPATH=src .venv/bin/python scripts/prepare_cross_genre_data.py --max-problems 60
PYTHONPATH=src .venv/bin/python scripts/generate_cross_genre_v1.py --max-pairs 100
```

## Inputs

- corpus file: `validation/cross-genre-v1/corpus.csv`
- text count: 173
- author count: 90
- role/genre count: 2
- corpus sources: `{'pan15_author_verification': 173}`

## Outputs

- `corpus.csv`
- `results.csv`
- `summary.json`
- `genre-stability.svg`

## Current Diagnostic Summary

- within-author cross-genre rows: 41
- cross-author control rows: 59
- mean within-author cross-genre distance: 0.39727
- mean cross-author control distance: 0.467665
- permutation p-value: 0.003996

## Boundary

These outputs do not establish validation, author identity, text origin,
AI-origin, legal status, forensic status, or a universal threshold.
