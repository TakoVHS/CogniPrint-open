# Public Benchmark v1.1

Status: released benchmark increment with bounded descriptive scope.

`public-benchmark-v1.1` extends the earlier `v1` subset with a larger multilingual set while preserving explicit provenance and reuse notes.

## Released scope

The current release contains:

- `20` baseline excerpts;
- `120` controlled variants;
- `5` languages: English, French, German, Spanish, and Russian;
- `3` source classes: public-domain literary text, government text, and political prose;
- `6` controlled perturbation axes.

These counts are recorded in:

- `evidence/public-benchmark-v1.1/manifest.json`;
- `evidence/public-benchmark-v1.1/counts.json`;
- `datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv`.

## Structure

- `raw/` contains the released baseline excerpts;
- `variants/` contains controlled variants derived from those baselines;
- `metadata/` contains source URLs, acquisition dates, license/reuse notes, release status, coverage targets, and gate documentation;
- `exports/` is reserved for benchmark-level descriptive exports.

## Provenance and licensing

Every released baseline has a source URL, acquisition date, source class, language, and reuse note in `metadata/sample-plan-template.csv`. A human-readable source list is available in `evidence/public-benchmark-v1.1/provenance-summary.md`.

The source works are recorded as public-domain texts. Wikisource also applies its own licensing rules to user contributions and page material, so the source-page license notice and the repository's source-specific provenance record remain authoritative. Preserve source attribution and links when redistributing the benchmark.

## Guardrail

This is a corpus release, not a universal benchmark-performance result. It does not establish authorship, source, AI origin, legal status, or forensic identity. CogniPrint remains `descriptive_only`, and the external methodological review gate remains `0/1`.
