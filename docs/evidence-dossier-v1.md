# CogniPrint Evidence Dossier v1

Status: `DEVELOPMENT_ONLY`  
Scientific claim evidence: `false`

The dossier is a portable directory bundle containing a canonical `dossier.json` manifest and an `artifacts/` directory. Verification is fully local and does not contact a CogniPrint service.

## Claim boundary

A v1 dossier is limited to descriptive signals and reproducibility metadata. It makes no authorship, identity, legal, forensic or deterministic model-source claim.

## Privacy defaults

- Raw source text is hashed but never copied into the bundle.
- Configuration content is hashed but never copied into the bundle.
- An artifact whose bytes match the excluded source or configuration is rejected.
- No automatic timestamp, hostname, username or absolute local path is recorded.

## Export

```bash
PYTHONPATH=src python -m cogniprint.dossier export \
  --source workspace/private-source.txt \
  --artifact results/analysis.json=workspace/analysis.json \
  --software-commit <40-character-lowercase-git-sha> \
  --output workspace/dossier-001
```

An optional local configuration file may be hashed with `--configuration`. Its bytes are not included.

## Offline verification

```bash
PYTHONPATH=src python -m cogniprint.dossier verify \
  --bundle workspace/dossier-001
```

A successful result reports `VERIFIED`, `offline: true`, the schema identifier, artifact count and manifest SHA-256.

## Fail-closed checks

The verifier rejects:

- unknown schema versions;
- duplicate JSON keys and non-finite numbers;
- non-canonical JSON;
- missing or extra manifest keys;
- path traversal, absolute paths and backslashes;
- symlinks and unsupported filesystem entries;
- missing, extra, modified or oversized artifacts;
- embedded source/configuration content;
- altered claim boundaries or scientific status.

## Format

Machine-readable schema: `schemas/cogniprint-evidence-dossier-v1.schema.json`.

Bundle root:

```text
dossier.json
artifacts/
  <safe relative artifact paths>
```

The v1 manifest intentionally contains no trusted timestamp. A later timestamp or signature extension must define its authority and verification semantics rather than treating local wall-clock time as evidence.
