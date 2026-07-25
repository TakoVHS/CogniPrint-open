# Tether Developer Grants — application draft

## HOLD — do not submit yet

Submission gate: one real QVAC runtime demonstration must be archived before this text is used as a current-capability claim.

## Project title

**CogniPrint Local Evidence Node — private, on-device explanation of reproducible text evidence**

## One-line description

CogniPrint Local Evidence Node combines deterministic local text fingerprinting with QVAC local inference so a researcher can inspect and explain a bounded evidence profile without sending sensitive source text to a cloud AI service.

## Problem

Researchers, journalists, and digital-evidence practitioners may need to inspect sensitive text while preserving source confidentiality. A cloud-based explanation layer creates an unnecessary disclosure path: the material or derived evidence must be transmitted to a remote provider simply to make the result understandable.

CogniPrint already computes a deterministic local statistical profile and SHA-256 content hash. The proposed deliverable adds a QVAC explanation layer that runs under the user's control and receives only a redacted evidence envelope, not the original source text.

## Why QVAC is necessary

QVAC is not being added as a logo or generic AI dependency. Its role is the privacy property of the deliverable:

- explanation inference runs locally;
- the model-facing payload can remain on the user's device;
- no hosted CogniPrint LLM endpoint is required;
- the deterministic measurement layer remains separate from the generative explanation layer;
- the local model cannot silently alter the underlying CogniPrint metrics.

The prototype is pinned to `@qvac/sdk@0.15.0` and uses the SDK's local `loadModel()` → `completion()` → `unloadModel()` flow.

## Proposed technical deliverable

A small open-source QVAC integration with four bounded components:

1. **Deterministic evidence generation**
   - CogniPrint processes the source locally.
   - Output contains metrics, normalized fingerprint coordinates, SHA-256, feature-map version, normalization metadata, and a scientific disclaimer.
   - Raw source text is not embedded in the profile output.

2. **Redacted evidence envelope**
   - `cogniprint-local-evidence-v1` whitelist.
   - Local filesystem paths and unapproved fields are removed.
   - Explicit claim-boundary flags prohibit exact-model, authorship, AI-origin, actor, and legal/forensic conclusions.

3. **QVAC local explanation**
   - QVAC receives the redacted evidence JSON only.
   - A small local model turns the measurements into a short human-readable explanation.
   - The prompt requires uncertainty language and explicit non-claims.

4. **Reproducible privacy demo**
   - exact CogniPrint commit;
   - exact QVAC SDK/model/runtime versions;
   - privacy-boundary tests;
   - one real local explanation artifact;
   - a record showing that the model prompt contains the bounded evidence envelope rather than raw source text.

## Current implementation state

Implemented in the prototype branch/repository:

- deterministic CogniPrint profile JSON;
- SHA-256 content hash and versioned fingerprint;
- QVAC package pinned to `0.15.0`;
- whitelist evidence sanitizer;
- bounded local-model prompt;
- local explanation runtime wrapper;
- offline privacy tests.

Offline privacy test result recorded during development: **3/3 tests passed**. The test fixture deliberately contains `TOP_SECRET_TEXT` and a `/private/path/...`; neither survives into the sanitized evidence or QVAC prompt.

Not yet completed:

- QVAC SDK/model runtime execution on a supported Node `>=22.17.0` environment;
- archived real local completion output;
- post-download offline/steady-state runtime demonstration.

Therefore this application remains on HOLD.

## Acceptance criteria

The deliverable is complete only when all are true:

- [ ] CogniPrint generates the deterministic profile locally from a text file.
- [ ] Source text is absent from the QVAC evidence payload.
- [ ] Local paths/unapproved fields are absent from the QVAC evidence payload.
- [ ] `@qvac/sdk@0.15.0` loads the selected local model on a supported runtime.
- [ ] QVAC produces a bounded explanation from the redacted evidence JSON.
- [ ] The explanation does not claim exact model identity, authorship, AI origin, actor identity, or forensic provenance.
- [ ] Runtime and model versions are recorded.
- [ ] Tests and demo commands are reproducible from a public commit.

## Scientific boundary

This deliverable is an evidence **explanation** layer, not an attribution oracle.

It does not claim to determine:

- which exact neural model generated arbitrary text;
- whether arbitrary text is definitively AI-generated;
- who authored the text;
- who requested or commissioned an action;
- intent, responsibility, legal status, or forensic provenance.

Those questions require separate validation and, for actor/workflow claims, authenticated external provenance.

## Short application summary

> CogniPrint Local Evidence Node is a bounded QVAC integration for privacy-preserving text evidence analysis. CogniPrint computes a deterministic statistical fingerprint and SHA-256 locally, strips raw text and local paths from the model-facing payload, and uses QVAC to explain only the resulting evidence JSON on-device. The deliverable is designed for researchers and journalists who may not be able to send sensitive material to a centralized AI service. The project explicitly separates deterministic measurement from generative explanation and does not claim exact-model, authorship, or actor attribution.

## Final pre-submission checklist

Before copying this text into Tether's form:

1. replace prototype language with measured runtime facts only;
2. attach/link the real demo artifact;
3. re-check the current `@qvac/sdk` version and Tether grant scope;
4. adapt deliverable size to the current form/task structure;
5. do not invent a requested amount if the active form defines one;
6. preserve the scientific non-claims.
