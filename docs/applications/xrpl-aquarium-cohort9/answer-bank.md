# XRPL Aquarium Cohort 9 — Answer Bank

Status: `STRONG_DRAFT / LIVE_FORM_MAPPING_PENDING`

This answer bank is written for common accelerator/application questions. It must be mapped to the exact live Typeform fields before submission. Applicant/team/legal/traction facts must be filled from verified records only.

## Project name

CogniPrint

## Short descriptor

Verifiable evidence infrastructure for synthetic language.

## One-sentence description

CogniPrint is an open-source system for creating reproducible, privacy-aware evidence packages about synthetic and AI-mediated text, with a working XRPL Testnet layer that anchors compact cryptographic commitments so third parties can independently verify evidence integrity without publishing sensitive content on-chain.

## What problem are you solving?

AI-generated and AI-edited content increasingly moves through multiple models, people, translation systems, agents, and publishing tools. In high-trust workflows, a binary “AI or human” score is not enough: investigators and organizations need to know what evidence was measured, which transformations occurred, what remains uncertain, and whether the evidence package they received is the same one that was originally produced.

Existing analysis is often trapped in screenshots, vendor dashboards, or mutable databases. That makes independent verification and cross-organization handoff difficult. CogniPrint turns analysis into explicit evidence packages with reproducibility metadata, integrity checks, uncertainty states, and non-claims.

## What is your solution?

CogniPrint produces portable Evidence Capsules / dossiers containing reproducible measurements, artifact hashes, software/version references, transformation diagnostics, and explicit uncertainty boundaries. The XRPL layer adds a narrow public trust primitive: a deterministic cryptographic commitment to a public-safe evidence manifest is recorded in an XRPL transaction while source text and sensitive evidence remain off-chain.

A verifier can later recompute the commitment from the received evidence manifest and compare it with the validated ledger record. XRPL is therefore used to verify evidence-state integrity, not to decide whether content is AI-generated.

## Why now?

Synthetic content is no longer a single-model problem. Multi-model agents, human editing, translation, and automated publishing create complex production chains. At the same time, organizations are under pressure to make content-integrity decisions that can be audited rather than merely trusted. The missing layer is not another opaque classifier; it is evidence that can survive handoff between systems and organizations.

## Why XRPL?

CogniPrint needs a durable public verification layer for compact evidence commitments, not a token economy. XRPL transactions provide a low-friction way to associate a small application-level memo with a transaction record and validated-ledger state. This lets CogniPrint keep evidence private/off-chain while making the integrity commitment independently checkable.

The current MVP uses transaction memos and validated-ledger verification. DID/Credentials can be evaluated later for issuer identity or authorization only where they add value and without placing personal information on-chain.

## What have you built already?

CogniPrint is a public open-source project with release `v0.1.2`. Existing public components include an interpretable 12-dimensional text profile, similarity/distance analysis, controlled perturbation measurements, entropy and n-gram analysis, reproducibility scripts, benchmark infrastructure, leakage-safe baseline evaluation infrastructure, and early Evidence Capsule / bounded local-evidence workflows.

The scientific system is intentionally conservative: current readiness is `descriptive_only`, and the project explicitly does not claim author identification, definitive AI origin, unique-model identification, or legal/forensic provenance.

For the Aquarium application, an isolated branch now contains a working XRPL Testnet evidence-integrity flow with deterministic canonicalization, SHA-256 commitments, MemoData transport, validated-ledger verification, independent transaction re-fetch by hash, and fail-closed mutation detection.

Real Testnet evidence from 2026-08-12:

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

## What will you build during Aquarium?

Because the minimal Testnet anchor is already working, the 9-week goal is to turn the proof into reusable infrastructure:

1. freeze a versioned evidence-anchor schema and publish deterministic interoperability vectors;
2. integrate anchor creation and verification into CogniPrint’s self-hosted Evidence Capsule workflow;
3. make second-party verification portable across machines/users with explicit match, mismatch, malformed, ambiguous, unavailable, and not-yet-validated states;
4. publish a sanitized receipt format, threat model, privacy review, and key-management boundaries;
5. package the pattern as an open-source XRPL reference implementation for evidence-oriented systems;
6. evaluate Mainnet readiness and DID/Credentials without requiring either for cohort success.

A successful cohort result is not “we put a hash on-chain”; it is a reusable, fail-closed verification workflow that other evidence-oriented XRPL applications can adopt.

## What is technically novel or differentiated?

The XRPL anchor itself is intentionally simple. CogniPrint’s differentiation is the evidence protocol around it:

- evidence packages are generated from a reproducible analysis workflow rather than arbitrary uploaded documents;
- uncertainty and non-claims are first-class outputs;
- private source content stays off-chain;
- verification distinguishes validated matches from ambiguous or unverifiable states;
- the evidence format is designed for independent reproduction and cross-organization handoff;
- the ledger commitment is one evidence class, not a substitute for scientific validity, identity, or lawful custody;
- the working Testnet demo already proves mutation detection against a real validated transaction.

This avoids the common failure mode where blockchain notarization is presented as proof that the underlying claim is true.

## Who are the users?

Initial users are teams that need auditable AI/content evidence rather than a black-box score: OSINT and investigative researchers, newsrooms/fact-checking teams, trust-and-safety/content-integrity teams, research groups evaluating synthetic text, and organizations exchanging evidence packages across trust boundaries.

## What is the business model?

The core evidence formats, commitment schema, verifier logic, and reference implementation should remain open-source. Sustainable commercial layers can include managed evidence workspaces, hosted verification, organizational policy controls, integrations, audit/reporting workflows, and enterprise support.

No token is required for the core business model.

## Why open source?

A trust system is stronger when independent parties can inspect how evidence commitments are created and verified. Open schemas, test vectors, and verifier logic reduce dependence on CogniPrint as a trusted intermediary and make the XRPL integration useful beyond a single product.

## Why is this a fit for Infrastructure / Security?

The cohort deliverable is a trust and verification primitive for evidence workflows: tamper-evident commitments, independent verification, explicit failure states, privacy-preserving off-chain storage, and auditable cross-organization handoff. It is infrastructure that can be embedded into investigator, publisher, trust-and-safety, and agent workflows rather than a consumer token application.

## Competitive landscape

CogniPrint should not compete on generic document notarization. Blockchain ecosystems already contain products that anchor records or documents. CogniPrint focuses on the layer before and after anchoring: producing structured AI/content evidence, preserving scientific uncertainty, protecting sensitive material, creating deterministic manifests, and verifying the exact evidence state against the ledger.

The positioning is therefore:

**evidence-aware content provenance + independent integrity verification**

rather than:

**generic blockchain timestamping/notarization**.

## What does XRPL not prove here?

An XRPL anchor does not prove that the underlying analysis is scientifically correct, that evidence was collected lawfully, that an author or model was identified, or that a legal chain of custody exists. It proves only that a particular commitment was included in a validated ledger record and can later be compared with a recomputed commitment.

Those boundaries are a product feature: the verifier should never turn integrity evidence into a broader claim it cannot support.

## Current traction / proof

Use only factual engineering/project evidence unless the form explicitly asks for customer traction.

Verified evidence available now:

- public open-source repository;
- release `v0.1.2`;
- MIT-licensed Python project;
- public website;
- active development history and benchmark/reproducibility materials;
- working XRPL Testnet transaction with validated-ledger verification;
- independent commitment recomputation;
- fail-closed mutation demo;
- public sanitized Testnet receipt in the application branch.

Do **not** claim customer adoption from repository activity. Current public GitHub metadata shows zero stars and zero forks, so those numbers should not be highlighted as traction.

## 9-week outcome metric

The cohort MVP should be considered successful only when an independent second party can:

- receive a CogniPrint public-safe evidence manifest;
- recompute the deterministic commitment;
- resolve the referenced XRPL transaction;
- confirm that it belongs to a validated ledger;
- decode the expected anchor payload;
- return `VALIDATED_MATCH` for an unchanged manifest;
- return a fail-closed mismatch/unverifiable state for incompatible input;
- perform the process without requiring source text or sensitive evidence on-chain;
- reproduce the flow from an independently documented open-source reference implementation.

## Founder / team

PLACEHOLDER — fill only from verified applicant facts.

Suggested structure once facts are verified:

“[Name] is the founder/maintainer of CogniPrint and leads [engineering/research/product responsibilities]. [Relevant concise background]. [Full-time status if true]. The project currently has [verified team size / contributors].”

## Legal entity / incorporation

PLACEHOLDER — answer exactly as the live form requests. Do not infer a company from the project name, website, domain, grant application, or repository.

## Funding raised

PLACEHOLDER — state only documented equity, debt, grants, prizes, or revenue as the form defines them.

## Location / residency / nationality / sanctions

PLACEHOLDER — answer exactly and truthfully. XRPL Commons' published Terms reserve the right to restrict access for sanctions targets and for persons located, organized, or resident in listed sanctioned countries/territories, including Russia. This is not written as a blanket nationality-only rule.

Do not use another person, company, wallet, or location to bypass eligibility or sanctions screening.

## Age eligibility

XRPL Commons' published Privacy Policy states that persons under 18 may not use XRPL Commons Services. This requirement must be satisfied directly. Do not attempt to bypass age screening through another person or account.

## Full-time commitment

PLACEHOLDER — the current public Cohort 9 eligibility page states that at least one full-time founder is required. Confirm the applicant can truthfully satisfy this before submission.

## Closing application statement

CogniPrint is already building the evidence layer, and its XRPL Testnet integrity loop now works end to end. Aquarium would be used to turn that proof into robust, reusable infrastructure: self-hosted integration, second-party verification, interoperability vectors, threat modeling, and a production-readiness path that preserves privacy and explicit failure boundaries.
