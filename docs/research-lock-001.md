# Research Lock 001

Status: `IMPLEMENTED AS INTEGRITY TOOLING / NOT YET FINALIZED FOR CHALLENGE 001`

## Purpose

`Research Lock 001` binds the exact bytes of the frozen research control files into one deterministic SHA-256 identifier.

It is intended to link the same research state across:

1. the repository;
2. external preregistration;
3. the frozen prediction manifest;
4. the final Challenge 001 report/evidence bundle.

## What it is not

A Research Lock Hash is **not**:

- a digital signature;
- proof of author identity;
- proof that the methodology is scientifically valid;
- proof that the files were not replaced before the lock was created.

It is an integrity binding over the exact file bytes selected at freeze time.

## Candidate lock inputs

The final lock set must be fixed before preregistration. It is expected to include at minimum:

- `RESEARCH_FREEZE_001.md`;
- frozen Challenge 001 protocol/configuration;
- independent evaluator source;
- Evidence Schema / relevant manifest schemas;
- Claim Firewall implementation/version contract;
- dataset/corpus manifest;
- Stage A/Stage B split or leakage-audit manifest where appropriate;
- reference-registry manifest/version;
- metric definitions;
- environment/dependency lock.

The exact final list remains `TO BE FROZEN`.

## Build

Example only — do not treat this as the final Challenge 001 lock command until the file set is frozen:

```bash
python scripts/build_research_lock_001.py build \
  --root . \
  --commit <FROZEN_COMMIT_SHA> \
  --include RESEARCH_FREEZE_001.md \
  --include scripts/evaluate_challenge_predictions.py \
  --include schemas/cogniprint-evidence-v1.schema.json \
  --output challenge-001/protocol/frozen/RESEARCH_LOCK_001.json
```

The builder sorts paths, hashes each file with SHA-256, then hashes a canonical JSON payload containing the commit and file hashes.

## Verify

```bash
python scripts/build_research_lock_001.py verify \
  --root . \
  --lock challenge-001/protocol/frozen/RESEARCH_LOCK_001.json
```

A verification PASS means the current locked files match the recorded bytes. It does not imply scientific correctness.

## Change control

After external preregistration, changes to thresholding, features, calibration, OOD rules, exclusions, metrics, evaluator semantics, or reference data require a documented protocol deviation or a new challenge when scientifically material.

The original Research Lock must remain preserved; do not overwrite it to hide a deviation.
