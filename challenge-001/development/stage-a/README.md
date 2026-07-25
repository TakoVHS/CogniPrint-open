# Challenge 001 — Stage A development area

Status: `DEVELOPMENT_ONLY`
Scientific-claim evidence: `NO`
Eligible for Stage B: `NO`

This namespace is reserved for development-calibration artifacts used **before** Challenge 001 freeze and external preregistration.

Permitted material includes:

- blinded development manifests;
- development-only sample identifiers/hashes;
- exploratory length/minimum-evidence analyses;
- OOD/UNKNOWN method development;
- calibration-method development;
- feature-stability checks;
- evaluator sanity artifacts;
- sample-count/strata feasibility evidence.

## Hard boundary

Every Stage A sample record must satisfy the blinded-sample schema with:

```text
stage = STAGE_A_DEVELOPMENT
development_visibility = true
evaluation_visibility = false
reference_set_membership = DEVELOPMENT_ONLY or REFERENCE_CANDIDATE
```

Stage A records must never be copied into sealed Stage B. Before freeze, the leakage audit must demonstrate zero `sample_id` and zero `content_sha256` overlap with candidate Stage B.

Stage A results may inform the numerical protocol **before** freeze. They must not be reported as blind Challenge 001 performance and must not be used to select favorable public demo cases.
