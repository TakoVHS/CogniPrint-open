# Public Benchmark v1.1 Metadata

This directory tracks the next benchmark-expansion pass.

## Purpose

The `v1.1` metadata layer is meant to separate:

- intake candidates;
- coverage targets;
- release gating;
- baseline-to-variant planning;
- provenance review status.

from the already released `public-benchmark-v1` subset.

## Current files

- `intake-candidates.csv` — expansion candidate registry
- `coverage-targets.md` — target baseline and language mix
- `release-gate.md` — minimum release requirements for the next increment
- `sample-plan-template.csv` — schema for the next wave of released baselines and variants

## Guardrail

Do not promote `v1.1` candidates into a released evidence layer until provenance, license, and source-boundary checks are complete.
