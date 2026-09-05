# Schmidt Q1 Pre-Award Protocol 001

Status: **DEVELOPMENT_ONLY_PREAWARD / NOT_PREREGISTERED / Q1_MILESTONE_NOT_CLAIMED**

Project: *Portable Evidence Capsules for Multi-Principal Agent Workflows: Privacy-Preserving Provenance and Failure Tracing*

## Purpose

Prepare the engineering and experimental substrate for the submitted Schmidt Sciences Q1 2027 milestone without consuming or pretending to complete the funded scientific work before an award exists.

The submitted Q1 milestone requires evidence that a minimum cross-principal evidence schema can reconstruct an instrumented delegation/action graph in small realistic workflows, that the verifier deterministically distinguishes intact from mutated evidence, and that event/lineage/authorization/integrity fields can be evaluated for necessity versus redundancy.

This document is a **draft protocol**, not an external preregistration. It must be frozen, dated, and if appropriate externally preregistered only after any award terms, host/fiscal-sponsor constraints, and final project start date are known.

## Pre-award deliverables allowed now

1. Candidate schema `cogniprint-multi-principal-evidence-v0.1`.
2. Dependency-free fail-closed verifier and deterministic integrity hashing.
3. Synthetic 3-principal happy-path fixture with no raw sensitive payloads.
4. Deterministic mutation and malformed-input test vectors.
5. Structural field-ablation harness that establishes only whether the current verifier requires a field.
6. Draft scoring/evaluation protocol and Q1 report skeleton.

None of these is a scientific result demonstrating multi-agent safety effectiveness.

## Candidate evidence fields

Each event carries:

- stable event ID and sequence;
- timestamp;
- principal ID and agent ID;
- event type;
- CogniPrint truth class (`OBSERVED`, `ATTESTED`, `INFERRED`, `UNKNOWN`);
- parent event IDs;
- authorization scope;
- target principal for delegation events;
- commitment to the withheld/local payload;
- deterministic event integrity hash.

A bundle carries 3–6 declared principals and a deterministic bundle integrity hash.

## Q1 experimental design to freeze after award

### Scenario families

At least two small realistic workflow families will be selected before the main Q1 evaluation. Candidate families are:

- cross-organization research synthesis with locally held source material;
- document-processing / verification workflows with delegated subtasks.

The final scenario definitions, model IDs, tool configuration, protocol versions, seeds, and scoring code must be pinned before the scored Q1 run.

### Principal count

Primary Q1 experiments: 3–6 independent principals. Fixtures may start at three principals and expand only after the smallest configuration is stable.

### Ground truth

The testbed will instrument the true action/delegation graph separately from the evidence exported to the evaluator. Ground truth must not be inferred from the Evidence Capsule itself.

### Conditions

For each frozen scenario, compare at minimum:

1. intact candidate evidence bundle;
2. mutation/corruption controls;
3. field ablations;
4. selected missing-event / bounded partial-observability conditions.

The broader native-log and centralized-trace comparison belongs to the submitted Q2 milestone and must not be represented as a Q1 requirement.

### Q1 metrics

- event/delegation edge precision, recall, and F1 against instrumented ground truth;
- path completeness;
- deterministic integrity-verification agreement;
- false edge / wrong-principal reconstruction rate;
- UNKNOWN/abstention rate when reconstruction is underdetermined;
- per-field ablation delta for reconstruction metrics;
- verifier/runtime overhead as descriptive context.

### Required negative controls

- changed authorization scope without recomputing the event hash;
- modified event with recomputed event hash but stale bundle hash;
- missing/unknown parent event;
- duplicate event/principal identifier;
- invalid delegation target;
- fewer than three principals;
- unsupported schema/research status;
- missing required fields.

## Decision logic

A field may be called **structurally required** if removing it makes the format unverifiable under the frozen schema.

A field may be called **empirically necessary for reconstruction** only if its preregistered ablation materially degrades reconstruction performance or increases false attribution across the frozen scenarios. Structural necessity and empirical necessity must not be conflated.

If the evidence is insufficient to choose a delegation edge reliably, the evaluator must permit `UNKNOWN` rather than force an attribution.

## Evidence package expected at the real Q1 checkpoint

- frozen schema version;
- frozen/preregistered evaluation protocol;
- instrumented 3–6-principal benchmark fixtures;
- scored field-ablation results with uncertainty where appropriate;
- deterministic verifier test vectors;
- exact code/model/runtime manifests;
- technical milestone report including failures and unresolved boundary conditions.

## Hard boundaries

This pre-award branch does not:

- claim Schmidt Q1 completion;
- create a funder reporting artifact;
- claim empirical cross-principal attribution performance;
- claim authorship, legal responsibility, or forensic provenance;
- unlock current CogniPrint `descriptive_only` scientific status;
- replace the final protocol freeze or independent review required after award.
