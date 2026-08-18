# OTF ICRP 2026 — Prior Work vs Proposed Funded Work

## Purpose

OTF contracts support future deliverables. This file prevents existing CogniPrint work from being relabeled as future funded work and provides a clear boundary for application `#22901`.

## Existing CogniPrint work — not future OTF deliverables

The public repository already contains, in varying stages of implementation or research readiness:

- CogniPrint `v0.1.2` public release line;
- documented descriptive text-profile measurements;
- transparent baseline/evaluation infrastructure;
- evidence ontology with `OBSERVED / INFERRED / ATTESTED / UNKNOWN` classes;
- Claim Firewall and machine-readable limitation concepts;
- deterministic evidence/case integrity primitives;
- reproducibility scripts/manifests;
- public scientific limitations and `descriptive_only` status;
- public grant/reviewer materials;
- research infrastructure for separate attribution, provenance and evidence experiments.

These assets may be reused as inputs where they reduce duplicated engineering, but their existence is disclosed and they are **not** described as work that OTF must pay to create from scratch.

## Proposed new ICRP-funded research work

The ICRP project is a distinct 12-month multilingual information-controls study. Proposed new work includes:

### 1. ICRP-specific protocol and sampling frame

- freeze the Vietnamese/Russian/English research protocol;
- define the sensitive-content sampling frame and safe-release rules;
- finalize the AI-mediated transformation taxonomy for the ICRP question.

### 2. New multilingual corpus/benchmark

- construct and document the matched source corpus;
- execute the specified translation, summarization, rewriting/paraphrase and moderation/refusal conditions;
- create multi-step transformation tracks;
- release a safe benchmark form with appropriate privacy controls.

### 3. New ICRP transformation analysis

- measure refusal, omission, sanitization, semantic drift, lexical substitution, compression, uncertainty change and provenance-context loss;
- compare results across Vietnamese, Russian and English;
- compare transparent baselines with selected descriptive CogniPrint measurements;
- document negative/null results.

### 4. ICRP Evidence Capsule adaptation and validation

- define the evidence fields specifically needed for transformation experiments;
- implement/export privacy-aware experiment records;
- test integrity, missing-evidence and multi-step lineage behavior;
- validate the safe-release/reproducibility workflow.

### 5. Practitioner/host validation

- obtain structured feedback on the taxonomy, evidence format and guidance;
- revise outputs based on documented feedback;
- test whether the outputs answer practical internet-freedom questions without encouraging unsupported attribution.

### 6. ICRP final outputs

- multilingual transformation benchmark;
- reproducibility package;
- technical methods/results report;
- dedicated failure/limitations report;
- practitioner guidance;
- final evidence/toolkit research release;
- sustainability/handoff documentation.

## Separate CogniPrint tracks that must not silently enter the ICRP scope

Unless OTF explicitly approves a scope change, the following are outside application `#22901` merely because they exist elsewhere in CogniPrint:

- universal or family-level AI source attribution research;
- general-purpose authorship detection;
- legal/forensic identity determination;
- unrelated blockchain/XRPL/Autonomys integrations;
- unrelated grant deliverables;
- general website redesign;
- product monetization;
- unrelated social-media or content-publishing systems;
- broad C2PA implementation not directly necessary for the ICRP transformation-evidence question.

A component from another track may be reused only when it is clearly an existing dependency or when OTF explicitly approves a new scoped deliverable.

## Overlapping-funding rule

Before final Stage 2 submission, every proposed future deliverable must be checked against:

- other active or pending grant applications;
- existing funded contracts;
- already completed public repository work;
- host-provided in-kind support.

The same future work must not be represented as independently payable by multiple funders without transparent cost/scope separation.

## Scientific-status rule

Completing OTF application materials, receiving an invitation, receiving funding, or completing engineering deliverables does not by itself change CogniPrint's scientific status.

`SCIENTIFIC_READINESS=descriptive_only` remains until empirical evidence and the project's independent scientific gates justify a different status.

## Proposal wording rule

Preferred wording:

> CogniPrint already provides open-source evidence and reproducibility primitives that will serve as infrastructure for the proposed research. OTF support would fund the new 12-month multilingual information-controls study, its controlled experiments, ICRP-specific benchmark/evidence outputs, practitioner validation, and research reporting.

Avoid wording that suggests OTF would fund the creation of already-completed repository assets.

## Final audit gate

Before submission, label each material proposal activity as one of:

- `EXISTING_INPUT`;
- `NEW_FUNDED_RESEARCH`;
- `HOST_IN_KIND`;
- `OPTIONAL_OTF_DIRECT_COST`;
- `OUT_OF_SCOPE`.

Any activity that cannot be classified must be resolved before the proposal is submitted.
