# Subspace Foundation / Autonomys — CogniPrint fit memo

Status date: 2026-07-25

## Decision

**Conditional GO — build and validate a narrowly differentiated Auto Drive integration before applying.**

CogniPrint has a natural fit with the Subspace Foundation Grants Program because the programme explicitly funds decentralized AI research, privacy-preserving and verifiable AI, integrations, and applications using Autonomys infrastructure.

The correct proposal is **not** a generic blockchain provenance registry and **not** a system that claims to prove human authorship.

## Current programme facts

Official programme: https://subspace.foundation/grants

As verified on 2026-07-25, the programme:

- accepts proposals on a rolling basis;
- funds infrastructure, AI-powered dApps, research, community work, and integrations;
- prioritises privacy-preserving and verifiable AI systems;
- may fund in gas credits, `$AI3`, stablecoins, or US dollars;
- uses milestone-based grant agreements and evidence of completed deliverables;
- expects technical feasibility, ecosystem impact, clear milestones, budget, and team expertise.

Eligibility must be re-checked on submission day. Current terms prohibit sanctioned applicants and participation from SECO-restricted/embargoed countries.

## Important overlap: Momento

In March 2026 the Subspace Foundation awarded a grant to **Momento**, which uses Auto Drive plus Auto EVM to preserve human-created content as verifiable records. Momento's public grant description includes:

- content capture;
- cryptographic hashes and signed metadata;
- permanent content storage on the DSN through Auto Drive;
- on-chain anchoring on Auto EVM;
- human-origin/authenticity records;
- reusable APIs around authenticated human data.

CogniPrint must not submit a proposal that merely repeats those functions.

## Differentiated CogniPrint proposal

### CogniPrint Evidence Capsule

A reproducible, content-addressed evidence artifact for AI/text research and digital-verification workflows.

Instead of storing the sensitive source text or asserting human authorship, the capsule stores a **minimal machine-readable record of what was measured and how**:

- source-content SHA-256, not source text;
- CogniPrint feature-map/fingerprint version;
- deterministic metrics and normalized fingerprint values;
- experiment or comparison configuration;
- dataset/model/tool metadata only where legitimately known;
- calibration context when available;
- explicit uncertainty and abstention state;
- separately labelled provenance assertions;
- software/repository commit SHA;
- evidence-capsule schema version;
- canonical capsule hash.

The capsule can be stored through Auto Drive and identified by its CID. Anyone with the appropriate source/evidence inputs can independently compare the reproduced evidence with the stored capsule.

## Why Auto Drive is substantive

Auto Drive provides content-addressed persistent storage on the Autonomys DSN. The current `@autonomys/auto-drive` SDK supports file/buffer upload and returns a CID. It also supports optional encryption/compression and a separate explicit public-publication operation.

This matters to CogniPrint because a research/evidence result should not depend only on a mutable project server or a screenshot. A CID-bound capsule can make the exact evidence state independently referencable across reviewers, grant milestones, research replication, and later provenance work.

The network is therefore used for a property CogniPrint actually needs: **durable, content-addressed evidence state**.

## Privacy boundary

Permanent storage changes the threat model. The default capsule MUST NOT contain:

- original source text;
- prompts containing sensitive source material;
- local file paths;
- API keys or credentials;
- personal contact information;
- private investigation identifiers;
- hidden system prompts;
- arbitrary raw metadata copied from a source document.

The integration should whitelist fields exactly as the QVAC evidence boundary does.

Two explicit modes are allowed:

### Public audit capsule

Contains only pre-approved non-sensitive measurements, hashes, versions, and claim boundaries. It may be stored unencrypted and intentionally published when appropriate.

### Encrypted capsule

Uses Auto Drive's encryption option for a bounded evidence object that should not be publicly readable. The encryption secret must never be committed or embedded in the capsule.

Encryption does not make it appropriate to upload unnecessary sensitive source material. The data-minimisation rule remains primary.

## Difference from Momento

| Momento | CogniPrint Evidence Capsule |
| --- | --- |
| Captures authentic human-created content | Captures reproducible analysis/evidence state |
| Stores the content itself on DSN | Defaults to hashes + bounded measurements, not source text |
| Human-origin/authenticity workflow | Scientific/evidence reproducibility workflow |
| Capture-time signed metadata | Analysis-time schema/version/config/metric provenance |
| Consumer authenticity records | Research/reviewer/investigation evidence capsules |
| Human-data layer for AI | Reproducible evidence layer for evaluating AI/content claims |

CogniPrint should explicitly cite this distinction in the application rather than implying that no adjacent Autonomys project exists.

## Proposed bounded grant deliverable

### Milestone 1 — Evidence Capsule schema and local verifier

- canonical JSON schema;
- deterministic canonicalisation and SHA-256;
- strict field allowlist;
- source-text/path/secret exclusion tests;
- local capsule verification command.

### Milestone 2 — Auto Drive integration

- pin a current `@autonomys/auto-drive` SDK version;
- upload a public non-sensitive test capsule from a Buffer;
- preserve returned CID;
- download by CID and verify canonical hash/content;
- optional encrypted-capsule test with secret supplied only at runtime.

### Milestone 3 — CogniPrint research integration

- generate a capsule from the M1 RAID metadata-only evidence pipeline;
- include CogniPrint commit and pinned external dataset revision;
- demonstrate that the capsule can be reproduced from the same evidence artifact;
- record disagreement/missing-provenance fields without converting them into attribution facts.

### Milestone 4 — Reviewer-facing proof

- public technical demo using non-sensitive synthetic/public evidence;
- exact commands and versions;
- stored CID and local reproduction instructions;
- privacy/abuse analysis;
- independent methodological feedback incorporated where available.

## Success criteria

The grant should be considered successful if a reviewer can:

1. inspect an input evidence artifact;
2. reproduce the canonical CogniPrint Evidence Capsule;
3. obtain the same capsule hash;
4. retrieve the stored capsule from Auto Drive by CID;
5. verify that retrieved content matches the locally reproduced capsule;
6. confirm that the capsule contains no source text or prohibited local/private fields;
7. see explicit scientific claim boundaries in the artifact itself.

No classification-accuracy target is required for this infrastructure milestone.

## Current technical pin

Prototype target, to re-check before submission:

- `@autonomys/auto-drive`: `1.6.14`;
- Auto SDK repository: https://github.com/autonomys/auto-sdk;
- Auto Drive: content-addressed storage via Autonomys DSN;
- upload API: `uploadFileFromBuffer(...)` returning a CID;
- optional upload encryption/compression;
- public URL creation requires separate `publishObject(cid)` action.

The Auto Drive API requires an API key. No API key belongs in the repository.

## Submission gate

Do not submit until:

- [ ] local Evidence Capsule schema/canonicalisation tests pass;
- [ ] at least one public non-sensitive capsule is uploaded through current Auto Drive SDK;
- [ ] CID retrieval and local verification are demonstrated;
- [ ] no raw source text/private paths/secrets appear in the capsule;
- [ ] Momento differentiation is stated explicitly;
- [ ] current grant scope and eligibility are re-checked;
- [ ] milestones and budget are sized from the demonstrated prototype rather than from the entire CogniPrint vision.

## Recommendation

This is currently the strongest blockchain/decentralized-storage grant fit for CogniPrint. Build the bounded Evidence Capsule prototype first; then apply as an **Integration / Research** proposal focused on reproducible verifiable AI evidence, not as another human-authenticity product.