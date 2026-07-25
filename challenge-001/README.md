# Attribution Challenge 001 — evidence layout

This directory defines the **research-control layout** for Challenge 001. It does not contain a completed Stage B corpus or result.

## Separation rule

```text
challenge-001/
├── development/
│   └── stage-a/
├── protocol/
│   └── frozen/
└── evaluation/
    └── stage-b-sealed/
```

### Stage A

Development-only material used to choose numerical/operational parameters before freeze. Stage A samples must never enter sealed Stage B.

### Frozen protocol

Contains the exact protocol state after `RESEARCH_FREEZE_001.md` becomes `FROZEN`, together with hashes/lock metadata.

### Stage B sealed evaluation

Contains blinded sample manifests and, separately, sealed ground-truth labels. Prediction code may consume blinded manifests/content but must not consume revealed-label records before prediction freeze.

## Required data separation

A blinded sample record may contain identifiers and reproducibility metadata, but **must not contain**:

- `true_class`;
- `known_to_reference`;
- generator/model-family ground truth;
- any field that trivially reveals the sealed label.

Revealed labels use a separate schema and are only exposed after `predictions.jsonl` has been frozen and hashed.

## Leakage gate

Before freeze, `scripts/check_challenge_leakage.py` must report:

- `sample_id_overlap == 0`;
- `content_hash_overlap == 0`;
- `freeze_gate == PASS`.

Prompt overlap is reported separately and must be resolved by the frozen protocol.

## Status

- Stage A: structure defined; real development manifest not yet frozen.
- Stage B: `NOT_AUTHORISED_TO_START`.
- External preregistration: HOLD until research freeze is complete.
