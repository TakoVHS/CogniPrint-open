# CogniPrint Model-Fingerprint Benchmark v0.1

Status: M0 protocol/scaffold. No attribution result is claimed by this directory.

## Goal

Provide a reproducible structure for collecting controlled human/model/mixed text samples and evaluating whether CogniPrint-derived signals support calibrated, benchmark-bounded model-family research.

## Files

- `manifest.schema.json` — normative metadata schema.
- `sample.example.json` — non-empirical example record showing the expected shape.
- `../../scripts/check_model_fingerprint_manifest.py` — lightweight manifest validator.
- `../../docs/model-fingerprint-benchmark-v0.1.md` — experimental protocol and failure criteria.

## Data policy

Do not commit:

- API keys or credentials;
- private prompts or system prompts containing secrets;
- personal data that is not necessary and lawfully releasable;
- provider-confidential metadata;
- copyrighted corpora without an appropriate release basis.

Where full text cannot be released, a metadata-only record may use `release_status: releasable_metadata` and retain only permitted hashes/metadata.

## M0 acceptance criteria

M0 is complete when:

1. the protocol is public;
2. the schema is public;
3. the example manifest passes the validator;
4. collection/split rules prevent prompt leakage;
5. current claims remain `descriptive_only`;
6. a pilot-corpus issue defines the first legal and reproducible collection wave.

## Next milestone: M1 pilot corpus

The first pilot should be deliberately small and auditable before scaling. It should contain multiple known model families, human controls, more than one language/domain, and a documented transformation subset. The exact sample count may be revised based on lawful data availability and cost, but all deviations from the protocol should be recorded before evaluation.
