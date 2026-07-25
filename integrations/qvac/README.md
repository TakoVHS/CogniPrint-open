# CogniPrint Local Evidence Node — QVAC prototype

Status: **experimental integration scaffold; QVAC runtime validation is still required.**

This module tests a narrow Tether/QVAC grant hypothesis: can CogniPrint keep sensitive source text local, compute deterministic evidence locally, and use a local QVAC model only to explain the resulting bounded evidence JSON?

It is intentionally **not** a model-attribution feature.

## Architecture

```text
sensitive text
    |
    | local Python only
    v
CogniPrint deterministic profile
    |
    | whitelist + redact local paths/unapproved fields
    v
cogniprint-local-evidence-v1 JSON
    |
    | local QVAC completion only
    v
bounded human-readable explanation
```

The QVAC layer never needs the original source text. It receives only:

- SHA-256 content hash;
- fingerprint version;
- deterministic metrics;
- normalized fingerprint coordinates/vector;
- normalization metadata;
- explicit scientific disclaimer and claim-boundary flags.

The sanitizer intentionally drops `source`, local filesystem paths, saved-profile paths, raw text, and any field that is not explicitly allowed.

## Runtime target

- Node.js `>=22.17.0`;
- `@qvac/sdk` pinned to `0.15.0` for this prototype;
- QVAC `QWEN3_600M_INST_Q4` local model;
- no cloud inference endpoint.

The model must be downloaded on the first run if it is not already cached. The intended steady-state inference path is on-device.

## Prepare CogniPrint evidence

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

cogniprint profile \
  --file path/to/sensitive-input.txt \
  --output workspace/qvac-local-evidence/profile.json
```

`cogniprint profile` computes the deterministic profile locally. The produced profile does not contain the original source text.

## Install the QVAC prototype

```bash
cd integrations/qvac
npm install
```

## Run the local explanation

```bash
node src/explain.mjs \
  ../../workspace/qvac-local-evidence/profile.json \
  ../../workspace/qvac-local-evidence/explanation.md
```

The prompt instructs the local model to explain measured evidence only and explicitly forbids conclusions about:

- exact neural-model identity;
- authorship identity;
- definitive AI origin;
- commissioning actor;
- intent or responsibility;
- legal or forensic provenance.

## Offline boundary tests

The privacy/redaction tests do not require QVAC or a downloaded model:

```bash
node --test test/*.test.mjs
```

The fixture deliberately contains `TOP_SECRET_TEXT` and `/private/path/...`; tests fail if either survives into the sanitized QVAC evidence or prompt.

## Runtime-validation gate

This branch is **not grant-submission ready** until all are demonstrated on a supported QVAC runtime:

1. `npm install` succeeds on Node `>=22.17.0`;
2. QVAC model loads successfully;
3. local completion produces an explanation from the redacted evidence JSON;
4. after the initial model download, the explanation path is demonstrated without a cloud inference call;
5. raw source text is absent from the QVAC prompt and output artifact inputs;
6. tests and exact SDK/model versions are preserved in a reproducible demo record.

Until that gate closes, public language must say **QVAC integration prototype/scaffold**, not “working QVAC integration.”
