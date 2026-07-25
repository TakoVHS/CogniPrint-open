# CogniPrint Evidence Capsule — Autonomys prototype

Status: **experimental integration scaffold; real Auto Drive upload/retrieval validation is still required.**

This module tests a narrow Subspace Foundation / Autonomys grant hypothesis:

> Can a CogniPrint research result be reduced to a privacy-bounded, reproducible evidence capsule whose exact state is content-addressed and durably stored on Auto Drive without uploading the sensitive source text?

It is not a human-authorship protocol and does not replace Momento or C2PA.

## Architecture

```text
sensitive/public source text
        |
        | local CogniPrint analysis
        v
CogniPrint profile JSON
        |
        | strict allowlist
        v
cogniprint-evidence-capsule-v1
        |
        | canonical JSON + SHA-256
        v
local verification
        |
        | explicit Auto Drive upload
        v
Auto Drive CID
```

The default capsule includes measurements and identifiers needed to reproduce the evidence state, not the source text.

## Data minimisation

The capsule schema does not copy arbitrary source/profile/context fields.

Allowed high-level contents include:

- SHA-256 of the analysed content;
- fingerprint version;
- deterministic metrics and fingerprint values;
- normalization information;
- CogniPrint commit ID;
- experiment/dataset identifiers and dataset revision;
- hashes of configuration/calibration context;
- tightly typed provenance assertion state;
- explicit scientific claim boundaries;
- canonical evidence SHA-256.

The prototype intentionally drops fields such as:

- raw text;
- local source/output paths;
- arbitrary notes;
- credentials;
- private prompts;
- arbitrary raw metadata.

A permanent network should never become a reason to retain more sensitive data.

## Prototype dependency pin

As of the 2026-07-25 prototype:

- `@autonomys/auto-drive`: `1.6.14`;
- `@autonomys/auto-utils`: `1.6.14`.

Re-check current versions before a grant submission or public demo.

Auto Drive requires an API key. It belongs only in `AUTO_DRIVE_API_KEY` at runtime and must never be committed.

## 1. Produce a local CogniPrint profile

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

cogniprint profile \
  --file path/to/input.txt \
  --output workspace/autonomys/profile.json
```

The profile records hashes and measurements but not the original text body.

## 2. Optional bounded context

Example `workspace/autonomys/context.json`:

```json
{
  "publication_intent": "public-audit",
  "cogniprint_commit_sha": "0123456789abcdef0123456789abcdef01234567",
  "experiment_id": "raid-m1-clean-en",
  "dataset_id": "liamdugan/raid",
  "dataset_revision": "865cac74188466cb0c3b7574a10204007b57a459",
  "configuration_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "provenance_assertions": [
    {
      "kind": "publication-record",
      "state": "verified",
      "reference_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    }
  ]
}
```

Only schema-approved fields survive capsule construction.

## 3. Build and verify locally

```bash
cd integrations/autonomys
node src/build.mjs \
  ../../workspace/autonomys/profile.json \
  ../../workspace/autonomys/context.json \
  ../../workspace/autonomys/capsule.json

node src/verify.mjs ../../workspace/autonomys/capsule.json
```

The verifier recomputes the capsule hash from canonical JSON and fails on modification.

## 4. Run privacy/integrity tests

These tests require no Auto Drive account or network access:

```bash
node --test test/*.test.mjs
```

The fixtures deliberately contain values such as `TOP_SECRET_TEXT`, private filesystem paths, a fake encryption password, and arbitrary hidden context. Tests fail if those values survive into the capsule.

## 5. Upload explicitly to Auto Drive

Install dependencies and provide a runtime API key:

```bash
npm install
export AUTO_DRIVE_API_KEY='...'

node src/upload.mjs \
  ../../workspace/autonomys/capsule.json \
  ../../workspace/autonomys/upload-receipt.json
```

The command:

- verifies the capsule before upload;
- uploads canonical capsule JSON from a Buffer;
- enables compression;
- records the returned CID in a local receipt;
- never logs or stores the API key;
- **does not call `publishObject()`**.

The prototype therefore does not create a public download URL automatically.

## Encrypted mode

Set context:

```json
{"publication_intent":"encrypted"}
```

and provide the password only at runtime:

```bash
export AUTO_DRIVE_ENCRYPTION_PASSWORD='...'
node src/upload.mjs capsule.json receipt.json
```

The uploader refuses an encrypted capsule without a runtime password. It also refuses an ambiguous `public-audit` capsule when an encryption password is supplied.

Encryption is not permission to upload source text. The capsule remains data-minimised.

## Missing runtime gate

Do **not** describe this as a completed Autonomys integration until all of the following are demonstrated with a non-sensitive capsule:

1. `npm install` succeeds with the pinned SDK;
2. local capsule tests pass;
3. `AUTO_DRIVE_API_KEY` is supplied outside the repository;
4. `uploadFileFromBuffer()` succeeds and returns a CID;
5. the capsule is downloaded/retrieved by CID;
6. the retrieved JSON passes local `verify.mjs` with the same `evidence_sha256`;
7. the exact CogniPrint commit, SDK versions, CID, and test output are archived;
8. no raw source/private field is present in the stored capsule.

A separate explicit publication demo may later call Auto Drive's public publishing function for a deliberately public synthetic capsule. It is outside this uploader by design.

## Scientific boundary

A stored CID proves neither model identity nor human authorship.

The capsule can make an exact evidence state durable and independently referencable. It does not make the evidence scientifically stronger than the measurements and authenticated provenance it contains.