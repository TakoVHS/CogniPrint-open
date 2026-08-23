# Zenodo Blocker

DOI under test: `10.5281/zenodo.20756421`

## 2026-06-24 observation

- `https://doi.org/10.5281/zenodo.20756421` returned HTTP `302` to `https://zenodo.org/doi/10.5281/zenodo.20756421`.
- Direct access to `zenodo.org` and `https://zenodo.org/api/records/20756421` timed out from the execution environment.

## 2026-08-23 independent re-check

- The canonical repository still declares release `v0.1.2` / version `0.1.2` and the DOI under test remains `10.5281/zenodo.20756421`.
- Independent public web searches for the exact DOI returned no Zenodo or DOI registry result.
- Independent public web searches for the exact title `CogniPrint: A mathematical framework for cognitive fingerprint analysis of text` plus `Adriashkin` / `0.1.2` returned no Zenodo record.
- The available web execution path could reach the Zenodo public homepage, but direct record/API retrieval for record `20756421` could not be independently completed in this run.

Gate decision: `ZENODO: FAIL` until the exact Zenodo record page or API response is independently verified as publicly accessible and matches the repository release metadata.

This gate does not change scientific readiness. Current scientific claims remain bounded by the repository's existing `descriptive_only` status.
