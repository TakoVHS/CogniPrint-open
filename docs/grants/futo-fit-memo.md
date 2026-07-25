# FUTO grants — CogniPrint fit memo

Status date: 2026-07-26

## Current public programme facts

FUTO publicly invites grant inquiries from engineers with projects aligned with its mission and states that its sponsored grant programme has awarded more than $5 million.

Official references:

- https://www.futo.org/grants/
- https://www.futo.org/about/futo-faq/

FUTO's broader public position emphasises user control, open/source-first software, independence from centralized platforms, and sustainable open technology.

## Fit decision

**Conditional GO — stronger fit than a generic AI-detection pitch.**

CogniPrint should not approach FUTO as:

> “an AI detector that tells users whether text is machine-generated.”

The stronger fit is:

> **A local-first, open-source cognitive-provenance workstation that lets users inspect sensitive digital artifacts without sending the source text to a centralized detector or hosted AI service.**

## Why the fit is real

CogniPrint already has a local deterministic core and can produce bounded evidence without embedding raw source text in the analysis payload.

Relevant existing components:

- local text-profile extraction;
- SHA-256 content hashes;
- versioned feature maps;
- reproducibility artifacts;
- explicit scientific non-claims;
- privacy-bounded Evidence Capsule tooling;
- optional local explanation prototype;
- no requirement for a centralized CogniPrint inference server in the core workflow.

This is materially related to user control rather than a cosmetic grant narrative.

## Recommended project title

**CogniPrint Local Provenance Workstation — open, reproducible evidence without cloud document upload**

Alternative:

**CogniPrint Evidence Workstation — local-first cognitive provenance for sensitive text**

## Problem statement

Researchers, journalists, reviewers, developers and other users may need to inspect sensitive or disputed text while preserving control over the source artifact.

Many AI-analysis products require the artifact to be uploaded to a hosted service and return an opaque score. This creates two problems:

1. source material leaves the user's environment;
2. the returned conclusion is difficult to reproduce or audit independently.

CogniPrint's proposed FUTO deliverable instead keeps the deterministic measurement layer local and exports only a bounded evidence artifact that the user controls.

## Bounded engineering deliverable

The FUTO proposal should be a concrete local-first engineering package rather than funding for the whole long-term research vision.

### Deliverable 1 — local workstation UX

Provide a clear local workflow for:

- opening a text artifact;
- computing its deterministic profile locally;
- viewing feature evidence and uncertainty boundaries;
- comparing against local/reference evidence sets;
- exporting a reproducible evidence dossier.

### Deliverable 2 — privacy boundary

Default behaviour should ensure:

- no raw source upload to a CogniPrint cloud service;
- local paths excluded from export artifacts;
- arbitrary private metadata rejected from Evidence Capsules;
- explicit user action required before any external publication/storage step.

### Deliverable 3 — evidence dossier

Export machine-readable and human-readable artifacts containing:

- source SHA-256;
- feature-map/extractor version;
- measured profile;
- reference-set version;
- candidate/alternative results only where benchmark-supported;
- `UNKNOWN / INSUFFICIENT EVIDENCE` state;
- software commit;
- reproduction command;
- explicit non-claims.

### Deliverable 4 — local verification

A second machine should be able to verify the evidence artifact and reproduce the deterministic measurement from the same source/version/configuration.

### Deliverable 5 — public failure modes

The package should link directly to the `Where CogniPrint fails` contract and never hide uncertainty behind a single confidence score.

## What not to pitch

Do not promise:

- exact-model identification from arbitrary text;
- universal AI detection;
- authorship identity;
- actor/commissioner attribution;
- legal or forensic proof;
- a cloud SaaS as the central architecture.

Do not make the FUTO application depend on Tether/QVAC or Autonomys. Those are separate integrations; the FUTO value proposition should stand on CogniPrint's own local/open architecture.

## Strong short pitch

> CogniPrint is building a local-first evidence workstation for synthetic-language provenance. Instead of uploading sensitive documents to a centralized AI detector and receiving an opaque score, users can compute a deterministic statistical profile locally, preserve hashes and software/configuration versions, see uncertainty and failure boundaries, and export a reproducible evidence dossier under their control. The current scientific core is descriptive; the funded engineering deliverable would make that open evidence workflow significantly easier to run, inspect and verify without requiring a hosted CogniPrint inference service.

## Evidence to attach

Before contacting FUTO, point to:

- public source repository;
- `docs/research-vision.md`;
- `docs/where-cogniprint-fails.md`;
- Evidence Capsule code/tests;
- reviewer bundle;
- local reproducibility instructions.

Do not lead with grants, speculative market size, or future multimodal modules.

## Submission recommendation

Unlike Tether, FUTO does not require a specific external-stack integration before an inquiry is meaningful.

Therefore a **short grant inquiry can be sent once the public repository clearly reflects the cognitive-provenance/local-first positioning** and the live website is not contradicting it.

Current blocker before sending: the live `cogniprint.org` deployment still needs to match the current repository positioning, or the email should link primarily to the public GitHub research package until that deployment issue is fixed.
