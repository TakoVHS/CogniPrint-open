# CogniPrint

CogniPrint is an MIT-licensed research framework for constructing compact, interpretable statistical profiles of text and studying profile similarity and stability under controlled perturbations.

## Scientific status

- Readiness: `descriptive_only`
- External methodological reviews: `0/1`
- Release: `v0.1.2`
- DOI: `10.5281/zenodo.20756421`
- Repository: https://github.com/TakoVHS/CogniPrint-open

CogniPrint does **not** establish authorship, source, AI origin, legal status, forensic identity, or a universal classification result.

## Public research package

The release candidate contains the Python research engine, tests, bounded benchmark material, evidence artifacts, manuscript source, citation metadata, and provenance notes.

Administrative records, application payloads, personal contact data, mailbox identifiers, billing operations, hosted deployment records, and local workspaces are intentionally excluded.

## Reproduce

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
python -m unittest tests/test_public_release_export.py -v
python scripts/check_public_benchmark_v11.py
python scripts/secret_scan.py
```

Reviewer entry points:

- [`docs/current-state-summary.md`](docs/current-state-summary.md)
- [`docs/evidence-dossier.md`](docs/evidence-dossier.md)
- [`paper/main.tex`](paper/main.tex)
- [`CITATION.cff`](CITATION.cff)

Repository: https://github.com/TakoVHS/CogniPrint-open

Project website: https://cogniprint.org

DOI: https://doi.org/10.5281/zenodo.20756421

## License

Software is released under the MIT License. Dataset and evidence reuse boundaries are documented in [`DATA_LICENSE.md`](DATA_LICENSE.md) and source-specific provenance records.
