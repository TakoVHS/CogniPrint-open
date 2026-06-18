# Public Benchmark v1.1 Release Gate

Status: **passed for the current bounded dataset release; repository publication still requires the separate public-release gate.**

## Verified release conditions

For the current `20` baselines and `120` controlled variants:

- provenance is recorded for every released baseline;
- a reuse or license note is recorded for every released baseline and variant;
- a source URL is recorded for every released baseline and variant;
- an acquisition date is recorded for every released baseline and variant;
- every released variant maps to a released baseline;
- released counts match the evidence manifest and counts file;
- no private or `workspace/` source text is used by this benchmark layer.

Canonical records:

- `datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv`;
- `evidence/public-benchmark-v1.1/manifest.json`;
- `evidence/public-benchmark-v1.1/counts.json`;
- `evidence/public-benchmark-v1.1/provenance-summary.md`;
- `evidence/public-benchmark-v1.1/limitations-summary.md`.

## Source-license boundary

The source works are recorded as public-domain texts obtained through Wikisource. Wikisource page material and user contributions can carry additional free-content attribution or share-alike requirements. The source-page license notice and source-specific provenance record remain authoritative; source URLs and attribution must be preserved.

## Remaining publication checks

Before publishing a new repository release:

- rerun source-link checks and record the date;
- verify the exported file count and SHA-256 manifest;
- confirm that the sanitized release contains no private administrative or operational material;
- retain the benchmark limitations and `descriptive_only` claim boundary.

## Release recommendation

Prefer a narrower clean release over a larger ambiguous release. Weak language or domain balance must be disclosed as a limitation and must not be hidden behind broader performance claims.
