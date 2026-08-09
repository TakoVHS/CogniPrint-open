# Schmidt Q1 Pre-Award Readiness 001

Status: **PARTIAL / DEVELOPMENT_ONLY_PREAWARD / SCIENTIFIC_MILESTONE_NOT_CLAIMED**

This document maps the submitted Schmidt Sciences Q1 2027 milestone to concrete repository evidence. It is a readiness tracker, not a funder report.

## Submitted Q1 checkpoint

By Q1 2027 the project aims to demonstrate that a minimum cross-principal evidence schema can reconstruct an instrumented delegation/action graph in small realistic workflows and that its verifier deterministically distinguishes intact from mutated evidence, while identifying which event, lineage, authorization, and integrity fields are necessary versus redundant.

Expected evidence submitted with the application:

- Schema v0.1;
- preregistered evaluation protocol;
- instrumented 3–6-principal benchmark fixtures;
- field-ablation results;
- deterministic verifier test vectors;
- technical milestone report with failure cases.

## Current pre-award state

| Q1 evidence item | Pre-award state | Current artifact | What remains after award |
| --- | --- | --- | --- |
| Schema v0.1 | CANDIDATE_IMPLEMENTED | `schemas/cogniprint-multi-principal-evidence-v0.1.schema.json` | independent review + freeze |
| Evaluation protocol | DRAFT_NOT_PREREGISTERED | `docs/schmidt-q1-preaward-protocol-001.md` | exact scenarios/models/tools/seeds freeze and external preregistration if selected |
| 3–6-principal fixtures | SYNTHETIC_3P_STARTER | `challenge-schmidt-q1/fixtures/synthetic-3-principal-happy-path.json` | realistic frozen scenario families; expand through 6 principals as justified |
| Deterministic verifier | IMPLEMENTED_CANDIDATE | `src/cogniprint/multi_principal_evidence.py` | exact-head execution, review, frozen test vectors |
| Mutation/fail-closed tests | IMPLEMENTED_NOT_EXACT_HEAD_EXECUTED | `tests/test_schmidt_q1_preaward.py` | exact checkout execution + broader negative vector set |
| Field ablation | STRUCTURAL_HARNESS_ONLY | `structural_field_ablation()` | empirical reconstruction ablations; uncertainty/results |
| Q1 technical report | SKELETON_ONLY | this tracker + protocol | scored report with failure cases and boundary conditions |

## Readiness interpretation

The project is **engineering-prepared for Q1**, not scientifically Q1-complete. The largest remaining work is the scientifically important part: freeze a realistic protocol, instrument ground truth, run the experiments, quantify reconstruction/false-attribution/UNKNOWN behavior, and distinguish structural schema requirements from empirical evidence sufficiency.

## Gate before any Q1 completion claim

All must be true:

1. Award/host constraints are known and the funded start date is fixed.
2. Exact schema/protocol/model/runtime/scenario revisions are frozen.
3. At least two realistic Q1 scenario families are instrumented with independent ground truth.
4. Exact checkout tests and verifier gates pass.
5. Field ablations are executed on frozen scenarios.
6. Reconstruction and false-attribution metrics are computed from hidden ground truth.
7. Failure cases and negative results are preserved.
8. Independent review confirms that no content-only authorship/legal/forensic claim has been introduced.
9. A Q1 milestone report records what was demonstrated and what failed.

Until then the only allowed status is `DEVELOPMENT_ONLY_PREAWARD` / `SCIENTIFIC_MILESTONE_NOT_CLAIMED`.

## Current execution blocker

The repository branch should be executed from an exact clean checkout. A non-GitHub local runner may provide development evidence, but it must not be represented as exact-head GitHub Actions evidence. Existing repository governance around execution truth remains in force.
