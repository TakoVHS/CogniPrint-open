# XRPL Commons — The Aquarium Cohort 9 — Application Draft

Status: `DRAFT / NOT SUBMITTED`

Target: The Aquarium, Cohort 9, Fall 2026
Program dates: 2026-10-12 through 2026-12-11
Public application deadline: 2026-09-06

This document is application preparation only. It does not change CogniPrint scientific readiness, authorize any research stage, or claim an XRPL deployment that does not yet exist.

## Working project name

**CogniPrint — Verifiable Evidence for Synthetic Language**

Alternative short label for the cohort: **CogniPrint Evidence Anchors**

## One-line pitch

CogniPrint is open-source evidence infrastructure for synthetic-language provenance: it creates privacy-preserving, independently verifiable evidence packages and is extending them with XRP Ledger anchors so investigators, researchers, platforms, and publishers can prove that an evidence record existed in a specific state without putting sensitive content on-chain.

## Problem

AI-generated and AI-edited content increasingly passes through multiple models, humans, translation systems, agents, and publishing tools. A binary “AI vs human” score is not enough for high-trust workflows. Teams need evidence that is reproducible, portable, privacy-aware, and explicit about uncertainty.

Today, provenance records are often fragmented across logs, screenshots, databases, and vendor-specific systems. Even when an analysis is reproducible, an external reviewer may still need a durable way to verify that the evidence bundle they received is the same bundle that was produced earlier and has not been silently replaced.

## Solution

CogniPrint produces evidence-oriented analysis with explicit non-claims and reproducibility metadata. The XRPL integration adds a narrow trust primitive:

1. create a local Evidence Capsule / dossier;
2. canonicalize a public-safe manifest;
3. compute a cryptographic commitment to that manifest;
4. anchor only the commitment, schema identifier, and minimal public metadata to a validated XRPL transaction;
5. keep source text, private evidence, and sensitive metadata off-chain;
6. allow any verifier to recompute the commitment and compare it with the ledger record.

The blockchain is not used to decide whether content is AI-generated. It is used to make evidence-state commitments independently verifiable.

## Why XRP Ledger

The integration needs a public, durable, low-friction verification layer rather than a token product. XRPL transactions can carry arbitrary memo data, have transaction hashes, and become final in validated ledgers. This matches CogniPrint’s evidence-first design: the analysis stays off-chain while a compact commitment becomes independently checkable.

A later phase can evaluate XRPL DID and Credentials for issuer/verifier identity and authorization, but the cohort MVP deliberately starts with the smallest useful primitive: evidence commitments.

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

## What we will build during the 9-week Aquarium cohort

### Milestone A — deterministic evidence commitment

- freeze a versioned public-safe anchor schema;
- derive a deterministic commitment from an Evidence Capsule manifest;
- add fail-closed local verification;
- demonstrate mutation detection without exposing private content.

Acceptance evidence:

- deterministic test vectors;
- verifier tests;
- privacy review showing raw text is not required on-chain.

### Milestone B — XRPL Testnet anchor + independent verifier

- publish the compact commitment in an XRPL Testnet transaction memo;
- record transaction hash and validated-ledger identity in the capsule receipt;
- implement independent lookup and verification;
- distinguish `CREATED`, `SUBMITTED`, `VALIDATED`, `MISMATCH`, and `NOT_VERIFIABLE` states.

Acceptance evidence:

- reproducible Testnet demo;
- transaction/ledger verification receipt;
- negative tests for modified manifests and wrong transaction references.

### Milestone C — end-to-end trust workflow

- expose anchor creation and verification through the self-hosted evidence workflow;
- produce a portable demo dossier that can be verified by a second machine/user;
- document threat model, privacy boundaries, key-management boundaries, and failure modes;
- prepare a mainnet-readiness decision without requiring mainnet launch during the cohort.

Stretch goal:

- evaluate XRPL DID as an optional identity layer for evidence issuers, keeping personal data off-chain.

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

The planned integration can become a reusable reference pattern for other XRPL projects that need to anchor off-chain evidence without publishing the evidence itself. Deliverables should include a small schema, test vectors, verifier logic, and threat-model documentation that can be reused independently of CogniPrint.

## Sustainability hypothesis

CogniPrint should keep the core evidence formats and verification logic open-source. Potential future sustainability layers can include hosted verification, managed evidence workspaces, organizational policy controls, enterprise integrations, and support. No token is required for the core product.

## Why Aquarium now

CogniPrint has enough implementation to satisfy an MVP-stage program, but the XRPL trust layer is intentionally early. The cohort is useful at exactly this boundary: convert an existing evidence system into a verifiable XRPL-integrated workflow, validate the architecture with XRPL experts, and reach a demonstrable Testnet-to-market prototype instead of adding blockchain after product decisions have already hardened.

## Founder / team fields — must be completed truthfully before submission

Do not infer or fabricate any of the following:

- founder legal name;
- current country of residence/location;
- company/legal-entity status;
- full-time founder commitment;
- team size and roles;
- incorporation details;
- fundraising history;
- user/revenue/traction metrics;
- sanctions/KYC representations.

The current Aquarium public eligibility page requires at least one full-time founder and active participation through the 9-week program. These fields must be confirmed by the applicant before submission.

## Links

- Repository: https://github.com/TakoVHS/CogniPrint-open
- Website: https://cogniprint.org

## Claims firewall for the application

Allowed:

- open-source research/evidence framework;
- deterministic evidence-package commitments;
- reproducible and privacy-aware design;
- planned XRPL Testnet anchoring;
- explicit uncertainty and non-claims.

Do not claim unless separately evidenced:

- that CogniPrint can identify an author;
- that it can definitively identify a unique source model;
- that it establishes legal or forensic provenance;
- that XRPL integration is already deployed;
- that a mainnet product exists;
- customer, revenue, usage, partnership, grant, or investment numbers not supported by records.
