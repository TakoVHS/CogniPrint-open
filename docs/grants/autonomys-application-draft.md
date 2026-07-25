# Subspace Foundation Grants — application draft

## HOLD — do not submit yet

Submission gate: one real Auto Drive upload + retrieval + local capsule verification must be archived before this text is used as a current-capability claim.

## Project title

**CogniPrint Evidence Capsule — reproducible, privacy-bounded AI evidence on Auto Drive**

## Category

Primary: **Integration**  
Secondary: **Research**

## One-line description

CogniPrint Evidence Capsule turns a deterministic text-analysis result into a minimal canonical evidence artifact—hashes, feature versions, measurements, experiment context, uncertainty boundaries, and typed provenance assertions—and stores that exact artifact on Autonomys Auto Drive by CID without uploading the sensitive source text by default.

## Problem

AI/content verification workflows increasingly produce derived measurements, model outputs, benchmark reports, hashes, and provenance claims. Those results are often shared as screenshots, mutable web pages, or files whose exact version cannot be independently referenced later.

At the same time, simply storing the underlying source content permanently can create privacy and safety risks.

CogniPrint needs a durable way to answer a narrower question:

> What exact evidence state was reviewed, which software/configuration produced it, and can another reviewer independently retrieve and verify that same state without requiring the sensitive source text to be permanently stored?

## Proposed solution

The Evidence Capsule is a canonical JSON artifact containing only schema-approved fields:

- SHA-256 of the analysed source artifact;
- CogniPrint feature/fingerprint version;
- deterministic measurements and normalized fingerprint;
- experiment/dataset identifiers and revision where appropriate;
- configuration/calibration hashes;
- exact CogniPrint commit ID;
- typed provenance assertion states;
- explicit scientific non-claims;
- canonical `evidence_sha256`.

The capsule is uploaded through `@autonomys/auto-drive` and receives a content-addressed CID.

The source text itself is excluded from the default schema.

## Why Autonomys

Auto Drive provides the property this deliverable is specifically testing: durable content-addressed storage backed by the Autonomys DSN.

The integration uses Auto Drive as an evidence-state layer rather than adding blockchain terminology to an otherwise unrelated product.

A reviewer should be able to:

1. reproduce a local capsule from the same evidence inputs;
2. obtain the same canonical evidence SHA-256;
3. retrieve the stored capsule by CID;
4. verify that the retrieved artifact matches the reproduced capsule;
5. inspect the scientific claim boundary embedded in the artifact.

## Relationship to Momento

The proposal is deliberately differentiated from the Foundation-funded Momento project.

Momento captures and preserves authentic human-created content, signed metadata, human-origin records, and the content itself on the DSN.

CogniPrint Evidence Capsule instead preserves **analysis state**:

- it does not claim to establish human origin;
- it does not require capture-time provenance;
- it does not default to storing the source content;
- it stores bounded measurements, software/configuration identifiers, hashes, and evidence/provenance states;
- its use case is reproducible research/review/investigation evidence rather than a consumer authenticity record.

The two approaches may be complementary, but this proposal does not duplicate Momento's human-content capture layer.

## Current implementation state

Implemented in the prototype branch/repository:

- `cogniprint-evidence-capsule-v1` canonical schema;
- strict field allowlist;
- source-content SHA-256;
- CogniPrint commit/version/configuration provenance;
- typed provenance assertions;
- embedded scientific non-claims;
- deterministic canonical JSON and `evidence_sha256`;
- local verifier that detects capsule tampering;
- Auto Drive uploader pinned to `@autonomys/auto-drive@1.6.14`;
- runtime-only API key;
- optional encrypted-capsule mode;
- no automatic `publishObject()` call;
- privacy/integrity tests.

Not yet completed:

- real Auto Drive upload;
- CID retrieval/download verification;
- archived integration receipt from a non-sensitive test capsule.

Therefore this application remains on HOLD.

## Proposed milestones

### M1 — Capsule schema and local verifier

Deliverables:

- canonical schema;
- deterministic hash;
- allowlist and non-claim boundary;
- privacy/tamper tests;
- CLI build/verify commands.

Acceptance:

- same bounded input produces the same capsule hash;
- mutation causes verification failure;
- deliberately inserted raw/private fields do not survive the schema.

### M2 — Auto Drive storage integration

Deliverables:

- pinned SDK integration;
- public non-sensitive test capsule upload;
- returned CID receipt;
- download/retrieval by CID;
- local re-verification.

Acceptance:

- retrieved canonical capsule matches the locally reproduced artifact;
- no source text or secret is present in stored data;
- exact SDK/network/CID/evidence hash are recorded.

### M3 — Research evidence integration

Deliverables:

- generate a capsule from the CogniPrint M1 external RAID evidence pipeline;
- preserve CogniPrint commit and pinned dataset revision;
- represent calibration/provenance state without converting it into an attribution fact.

Acceptance:

- capsule is reproducible from the metadata-only M1 evidence artifact;
- external source text remains outside the stored capsule;
- evidence state can be independently compared by hash/CID.

### M4 — Reviewer-facing demo and documentation

Deliverables:

- synthetic/public demo;
- technical documentation;
- privacy and abuse analysis;
- independent methodological feedback incorporated where available.

## Privacy and safety

Permanent storage makes data minimisation a first-class requirement.

The default schema refuses arbitrary metadata and excludes raw source text, local paths, credentials, private prompts, personal contact data, and untyped arbitrary notes.

The prototype supports an explicit `encrypted` intent using Auto Drive's upload encryption option, but encryption is not treated as permission to retain unnecessary sensitive source material.

Public publication is not automatic. The uploader intentionally does not call `publishObject()`.

## Scientific boundary

A durable evidence capsule does not prove:

- exact neural-model identity;
- authorship identity;
- definitive AI origin;
- the person or organisation that commissioned an action;
- intent or responsibility;
- legal or forensic provenance.

The storage layer preserves an evidence state; it does not strengthen unsupported scientific claims.

## Expected ecosystem value

- demonstrates Auto Drive as a durable evidence/reproducibility primitive for AI research;
- creates reusable open-source capsule schema/tooling;
- generates real Auto Drive usage from reproducible AI evidence workflows;
- provides a privacy-bounded example distinct from storing source datasets/content directly;
- creates an integration point for later authenticated provenance standards without conflating them with statistical inference.

## Submission gate

Change HOLD to READY only after:

- [ ] local capsule tests pass;
- [ ] one non-sensitive capsule is uploaded through the current Auto Drive SDK;
- [ ] a CID is returned and preserved;
- [ ] retrieval/download produces the expected capsule;
- [ ] local verification returns the same evidence SHA-256;
- [ ] runtime package/network versions are recorded;
- [ ] Momento differentiation is retained;
- [ ] current grant eligibility/scope is re-checked;
- [ ] milestones and budget are adjusted to actual prototype effort.
