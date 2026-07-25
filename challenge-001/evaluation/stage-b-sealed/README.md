# Challenge 001 — sealed Stage B evaluation area

Status: `NOT_AUTHORISED_TO_START`

This namespace is reserved for sealed blind evaluation **after** all required gates are complete:

1. Stage A development calibration finished;
2. real A/B leakage audit passes;
3. `RESEARCH_FREEZE_001.md` is `FROZEN`;
4. Research Lock 001 is preserved;
5. external timestamped preregistration is complete;
6. exact benchmark/split manifests are sealed.

## Blinding rule

Prediction code may receive blinded sample records/content needed for inference, but must not receive ground-truth labels before predictions are frozen and hashed.

Every Stage B blinded record must satisfy:

```text
stage = STAGE_B_SEALED
development_visibility = false
evaluation_visibility = true
reference_set_membership = SEALED_EVALUATION
```

The blinded schema forbids direct ground-truth fields such as `true_class`, `known_to_reference`, `generator`, `model_family` and `ground_truth`.

Ground-truth labels live separately and are revealed only after `predictions.jsonl` and its SHA-256 are fixed.

Any Stage A sample/content overlap blocks Stage B rather than becoming a post-hoc exclusion.
