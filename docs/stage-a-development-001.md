# Attribution Challenge 001 — Stage A development calibration

Status: `DEVELOPMENT_ONLY`
Scientific-claim evidence: `NO`
May enter sealed Stage B: `NO`

## Purpose

Stage A exists only to determine numerical and operational choices **before** the Challenge 001 protocol is frozen and preregistered. It is not a blind evaluation and must never be presented as evidence for the Stage B scientific claim.

Stage A may be used to determine or sanity-check:

- candidate minimum-evidence / length bins;
- sample-count feasibility and strata balance;
- feature stability diagnostics;
- OOD/UNKNOWN methodology;
- calibration procedure and binning;
- exclusion mechanics;
- evaluator sanity;
- operational reproducibility of the pipeline.

## Hard separation from Stage B

Stage A and Stage B must use physically and logically separate manifests/namespaces.

Recommended structure:

```text
challenge-001/
├── development/
│   └── stage-a/
├── protocol/
│   └── FROZEN/
└── evaluation/
    └── stage-b-sealed/
```

Every sample manifest used by either stage must expose at least:

```text
sample_id
content_sha256
prompt_hash (when applicable)
origin/source identifier
reference_set_membership
development_visibility
evaluation_visibility
```

Before `RESEARCH_FREEZE_001.md` may become `FROZEN`, a leakage audit must show:

- `sample_id_overlap == 0`;
- `content_hash_overlap == 0`;
- any prompt-hash overlap is explicitly reported and handled by the frozen protocol;
- no Stage B ground-truth label was visible to fitting/threshold/calibration code;
- reference-set membership follows the preregistered policy.

If sample or content overlap is non-zero, Challenge 001 Stage B is blocked. The overlapping records must be removed/rebuilt before freeze; they must not be silently ignored after evaluation.

## Permitted Stage A changes

Before freeze, Stage A may inform choices that are still unresolved in `RESEARCH_FREEZE_001.md`, including numerical thresholds and feasibility decisions.

Those choices must be fixed **before** external preregistration and before any sealed Stage B prediction run.

## Forbidden use

Stage A must not be used to:

- report Challenge 001 accuracy as a scientific result;
- choose public demo examples because they look favorable;
- tune against any Stage B labels;
- reclassify Stage B samples as development data after seeing results;
- justify post-reveal threshold, feature, calibration, OOD, metric, exclusion or reference-registry changes.

## Freeze transition

The intended order is:

```text
PRE-FREEZE
  -> Stage A development calibration
  -> numeric/operational protocol finalised
  -> leakage audit PASS
  -> RESEARCH_FREEZE_001 = FROZEN
  -> external timestamped preregistration
  -> sealed Stage B
```

After `FROZEN + preregistered`, scientific-impacting changes require a documented protocol deviation or a new challenge. They are not silent patches to Challenge 001.
