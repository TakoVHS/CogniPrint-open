# XRPL Commons — The Aquarium Cohort 9 — Application Draft

Status: `STRONG_DRAFT / NOT SUBMITTED`

Target: The Aquarium, Cohort 9, Fall 2026  
Program dates: 2026-10-12 through 2026-12-11  
Public application deadline: 2026-09-06

This document is application preparation only. It does not change CogniPrint scientific readiness, authorize any research stage, or claim Mainnet deployment.

## Working project name

**CogniPrint — Verifiable Evidence for Synthetic Language**

Alternative short label for the cohort: **CogniPrint Evidence Anchors**

## One-line pitch

CogniPrint is open-source evidence infrastructure for synthetic-language provenance: it creates privacy-preserving, independently verifiable evidence packages and now has a working XRP Ledger Testnet anchor flow so investigators, researchers, platforms, and publishers can verify that an evidence record existed in a specific state without putting sensitive content on-chain.

## Problem

AI-generated and AI-edited content increasingly passes through multiple models, humans, translation systems, agents, and publishing tools. A binary “AI vs human” score is not enough for high-trust workflows. Teams need evidence that is reproducible, portable, privacy-aware, and explicit about uncertainty.

Today, provenance records are often fragmented across logs, screenshots, databases, and vendor-specific systems. Even when an analysis is reproducible, an external reviewer may still need a durable way to verify that the evidence bundle they received is the same bundle that was produced earlier and has not been silently replaced.

## Solution

CogniPrint produces evidence-oriented analysis with explicit non-claims and reproducibility metadata. Its XRPL integration adds a narrow trust primitive:

1. create a local Evidence Capsule / dossier;
2. canonicalize a public-safe manifest;
3. compute a cryptographic commitment to that manifest;
4. anchor only the commitment, schema identifier, and minimal public metadata to a validated XRPL transaction;
5. keep source text, private evidence, and sensitive metadata off-chain;
6. allow any verifier to recompute the commitment and compare it with the ledger record.

The blockchain is not used to decide whether content is AI-generated. It is used to make evidence-state commitments independently verifiable.

## Why XRP Ledger

The integration needs a public, durable, low-friction verification layer rather than a token product. XRPL transactions can carry application memo data, expose transaction hashes, and become final in validated ledgers. This matches CogniPrint’s evidence-first design: the analysis stays off-chain while a compact commitment becomes independently checkable.

A later phase can evaluate XRPL DID and Credentials for issuer/verifier identity and authorization, but the current MVP deliberately starts with the smallest useful primitive: evidence commitments.

## Current MVP

CogniPrint is already a public open-source project rather than a concept-only application.

Current public release: `v0.1.2`.

Implemented public components include:

- an interpretable 12-dimensional text profile;
- similarity and distance analysis;
- controlled perturbation measurements;
- entropy and n-gram analysis;
- reproducibility scripts and benchmark material;
- leakage-safe baseline evaluation infrastructure;
- Evidence Capsule / bounded local-evidence prototypes;
- explicit privacy, uncertainty, and non-claim boundaries;
- public website and repository.

Current scientific readiness remains `descriptive_only`. CogniPrint does not currently claim legal/forensic provenance, unique model identification, authorship identification, or definitive AI origin.

### Working XRPL Testnet evidence

A real end-to-end Testnet gate was executed on 2026-08-12 from the isolated application branch.

```text
REAL_TESTNET_TX=E6E716789B416612A96221A4F51D6CA3B165E16E4777C2516D434184E9B93A21
VALIDATED=true
TRANSACTION_RESULT=tesSUCCESS
INDEPENDENT_LEDGER_LOOKUP=PASS
VALIDATED_MATCH=PASS
MUTATION=FAIL_CLOSED_PASS
XRPL_REAL_TESTNET_GATE=PASS
```

Manifest commitment:

```text
238b9c52793119d1e530b522ee853c23317ac2271cd9e12df9a1b98076352d03
```

The live runner used ephemeral Testnet faucet wallets, persisted no wallet seed, independently re-fetched the transaction by hash, recomputed the local manifest commitment, and rejected a mutated manifest fail-closed.

This proves the engineering integrity workflow on XRPL Testnet. It does not prove scientific correctness, authorship, unique-model identity, lawful collection, or legal chain of custody.

## What we will build during the 9-week Aquarium cohort

Because the minimal Testnet anchor has already been demonstrated before application, the cohort plan moves beyond “put a hash on-chain.”

### Milestone A — production-grade evidence-anchor protocol

- freeze a versioned public-safe anchor schema;
- publish deterministic test vectors and interoperability fixtures;
- harden fail-closed verification states;
- complete a focused security/privacy threat-model review;
- define explicit lifecycle states such as `CREATED`, `SUBMITTED`, `VALIDATED`, `MISMATCH`, `NOT_FOUND`, and `NOT_VERIFIABLE`.

Acceptance evidence:

- deterministic cross-machine test vectors;
- verifier regression suite;
- privacy review confirming raw source text is not required on-chain;
- documented misuse and failure boundaries.

### Milestone B — self-hosted end-to-end evidence workflow

- integrate anchor creation and verification into the self-hosted Evidence Capsule workflow;
- produce a portable dossier that a second machine/user can verify independently;
- expose a compact reviewer-facing receipt containing transaction hash, ledger finality state, commitment schema, and verifier result;
- test incorrect transaction references, changed manifests, malformed memos, duplicate/ambiguous anchors, and unavailable network states.

Acceptance evidence:

- reproducible second-party verification demo;
- sanitized public receipt format;
- mutation and ambiguity negative tests;
- offline-first evidence package with online ledger verification as an explicit step.

### Milestone C — ecosystem-ready reference implementation

- publish the XRPL evidence-anchor pattern as reusable open-source infrastructure;
- document integration guidance for investigative, publisher, trust-and-safety, and agent workflows;
- evaluate key-management and operational boundaries for production deployment;
- prepare a Mainnet-readiness decision without requiring Mainnet launch during the cohort;
- validate whether DID/Credentials add real issuer/verifier value without placing personal data on-chain.

Stretch goal:

- demonstrate an authorized issuer/verifier profile using XRPL identity primitives only if privacy, governance, and user value justify it.

## Target users

Initial target users are teams that need auditable AI/content evidence rather than a black-box score:

- OSINT and investigative researchers;
- newsrooms and fact-checking teams;
- trust-and-safety and content-integrity teams;
- research groups evaluating synthetic text;
- organizations exchanging digital-evidence packages across trust boundaries.

The project should not be positioned as a substitute for lawful chain-of-custody procedures or as an automated legal verdict system.

## Why this belongs in Infrastructure / Security

The core cohort contribution is a verification primitive, not speculative tokenization. CogniPrint’s XRPL layer is designed to improve:

- integrity of evidence packages;
- independent verification;
- auditability across organizations;
- privacy-preserving provenance workflows;
- explicit handling of uncertainty and unverifiable states.

## Open-source value to XRPL

The integration can become a reusable reference pattern for other XRPL projects that need to anchor off-chain evidence without publishing the evidence itself. Deliverables include a small schema, test vectors, verifier logic, receipt format, and threat-model documentation that can be reused independently of CogniPrint.

## Sustainability hypothesis

CogniPrint should keep the core evidence formats and verification logic open-source. Potential future sustainability layers can include hosted verification, managed evidence workspaces, organizational policy controls, enterprise integrations, and support. No token is required for the core product.

## Why Aquarium now

CogniPrint has moved past the architecture-only stage: the Testnet integrity loop already works. Aquarium is useful now because the next challenge is turning a narrow technical proof into ecosystem-quality infrastructure — stronger protocol semantics, second-party verification, production threat modeling, self-hosted integration, and a credible route from Testnet evidence to real users.

The program’s Infrastructure/Security focus is therefore a direct fit.

## Founder / team fields — must be completed truthfully before submission

Do not infer or fabricate any of the following:

- founder legal name;
- age/eligibility status;
- current country of residence/location;
- company/legal-entity status;
- full-time founder commitment;
- team size and roles;
- incorporation details;
- fundraising history;
- user/revenue/traction metrics;
- sanctions/KYC representations.

The current Aquarium public eligibility page requires at least one full-time founder and active participation throughout the 9-week program. XRPL Commons' public Privacy Policy also states that its services are not available to persons under 18. These requirements must be truthfully satisfied; they must not be bypassed through another person, company, wallet, or location.

## Legal / compliance gate

XRPL Commons' published Terms reserve the right to restrict access if a person is a sanctions target or is located, organized, or resident in a listed sanctioned country/territory; the published list includes Russia. This language is about sanctions status and location/organization/residence, not a blanket nationality-only rule.

Before submission or reliance on a later grant/payment path:

- answer nationality, location, residence, organization, and sanctions questions truthfully;
- confirm the applicant satisfies the service age requirement;
- obtain written clarification from XRPL Commons where citizenship/residence/payment-route facts create uncertainty;
- do not use another person or entity to bypass compliance or age screening.

## Links

- Repository: https://github.com/TakoVHS/CogniPrint-open
- Website: https://cogniprint.org
- Testnet transaction: `E6E716789B416612A96221A4F51D6CA3B165E16E4777C2516D434184E9B93A21`

## Claims firewall for the application

Allowed:

- open-source research/evidence framework;
- deterministic evidence-package commitments;
- reproducible and privacy-aware design;
- working XRPL Testnet evidence-anchor flow;
- validated-ledger receipt verification;
- independent manifest recomputation;
- fail-closed mutation detection;
- explicit uncertainty and non-claims.

Do not claim unless separately evidenced:

- that CogniPrint can identify an author;
- that it can definitively identify a unique source model;
- that it establishes legal or forensic provenance;
- that a Mainnet product exists;
- customer, revenue, usage, partnership, grant, or investment numbers not supported by records.
