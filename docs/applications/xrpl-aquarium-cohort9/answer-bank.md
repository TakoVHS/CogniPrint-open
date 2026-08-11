# XRPL Aquarium Cohort 9 — Answer Bank

Status: `DRAFT / FORM_FIELDS_NOT_YET_MAPPED`

This answer bank is written for common accelerator/application questions. It must be mapped to the exact live form fields before submission. Applicant/team/legal/traction facts must be filled from verified records only.

## Project name

CogniPrint

## Short descriptor

Verifiable evidence infrastructure for synthetic language.

## One-sentence description

CogniPrint is an open-source system for creating reproducible, privacy-aware evidence packages about synthetic and AI-mediated text, with an XRPL layer that anchors compact cryptographic commitments so third parties can independently verify evidence integrity without publishing sensitive content on-chain.

## What problem are you solving?

AI-generated and AI-edited content increasingly moves through multiple models, people, translation systems, agents, and publishing tools. In high-trust workflows, a binary “AI or human” score is not enough: investigators and organizations need to know what evidence was measured, which transformations occurred, what remains uncertain, and whether the evidence package they received is the same one that was originally produced.

Existing analysis is often trapped in screenshots, vendor dashboards, or mutable databases. That makes independent verification and cross-organization handoff difficult. CogniPrint turns analysis into explicit evidence packages with reproducibility metadata, integrity checks, uncertainty states, and non-claims.

## What is your solution?

CogniPrint produces portable Evidence Capsules / dossiers containing reproducible measurements, artifact hashes, software/version references, transformation diagnostics, and explicit uncertainty boundaries. The planned XRPL integration adds a narrow public trust primitive: a deterministic cryptographic commitment to a public-safe evidence manifest is recorded in an XRPL transaction, while source text and sensitive evidence remain off-chain.

A verifier can later recompute the commitment from the received evidence manifest and compare it with the validated ledger record. XRPL is therefore used to verify evidence-state integrity, not to decide whether content is AI-generated.

## Why now?

Synthetic content is no longer a single-model problem. Multi-model agents, human editing, translation, and automated publishing create complex production chains. At the same time, organizations are under pressure to make content-integrity decisions that can be audited rather than merely trusted. The missing layer is not another opaque classifier; it is evidence that can survive handoff between systems and organizations.

## Why XRPL?

CogniPrint needs a durable public verification layer for compact evidence commitments, not a token economy. XRPL transactions provide a low-friction way to associate a small application-level memo with an immutable transaction record and a validated ledger state. This lets CogniPrint keep evidence private/off-chain while making the integrity commitment independently checkable.

The cohort MVP deliberately starts with transaction memos and validated-ledger verification. DID/Credentials can be evaluated later for issuer identity or authorization only where they add value and without placing personal information on-chain.

## What have you built already?

CogniPrint is a public open-source project with release `v0.1.2`. Existing public components include an interpretable 12-dimensional text profile, similarity/distance analysis, controlled perturbation measurements, entropy and n-gram analysis, reproducibility scripts, benchmark infrastructure, leakage-safe baseline evaluation infrastructure, and early Evidence Capsule / bounded local-evidence workflows.

The scientific system is intentionally conservative: current readiness is `descriptive_only`, and the project explicitly does not claim author identification, definitive AI origin, unique-model identification, or legal/forensic provenance.

For the Aquarium application, an isolated development branch now contains a network-free XRPL evidence commitment prototype with deterministic canonicalization, SHA-256 commitments, fail-closed verification, MemoData encoding preparation, and targeted tests. No Testnet or Mainnet deployment is claimed yet.

## What will you build during Aquarium?

The 9-week target is an end-to-end XRPL Testnet evidence-integrity workflow:

1. freeze a versioned, privacy-safe evidence anchor schema and deterministic commitment format;
2. anchor a compact commitment in an XRPL Testnet transaction and record the transaction/validated-ledger receipt;
3. implement independent lookup and verification with explicit match, mismatch, not-found, malformed, and not-yet-validated states;
4. integrate the flow into CogniPrint’s self-hosted Evidence Capsule workflow;
5. publish test vectors, verifier logic, privacy/threat-model documentation, and a portable demo dossier that can be verified independently.

A successful cohort result is not “we put a hash on-chain”; it is a reusable, fail-closed verification workflow that other evidence-oriented XRPL applications can adopt.

## What is technically novel or differentiated?

The XRPL anchor itself is intentionally simple. CogniPrint’s differentiation is the evidence protocol around it:

- evidence packages are generated from a reproducible analysis workflow rather than arbitrary uploaded documents;
- uncertainty and non-claims are first-class outputs;
- private source content stays off-chain;
- verification distinguishes validated matches from ambiguous or unverifiable states;
- the evidence format is designed for independent reproduction and cross-organization handoff;
- the ledger commitment is one evidence class, not a substitute for scientific validity, identity, or lawful custody.

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

## 9-week outcome metric

The MVP should be considered complete only when an independent verifier can:

- receive a CogniPrint public-safe evidence manifest;
- recompute the deterministic commitment;
- resolve the referenced XRPL Testnet transaction;
- confirm that it belongs to a validated ledger;
- decode the expected anchor payload;
- return `VALIDATED_MATCH` for an unchanged manifest;
- return a fail-closed mismatch/unverifiable state for any incompatible input;
- perform the process without requiring source text or sensitive evidence on-chain.

## Founder / team

PLACEHOLDER — fill only from verified applicant facts.

Suggested structure once facts are verified:

“[Name] is the founder/maintainer of CogniPrint and leads [engineering/research/product responsibilities]. [Relevant concise background]. [Full-time status if true]. The project currently has [verified team size / contributors].”

## Traction

PLACEHOLDER — use exact evidence only.

Possible evidence categories if available:

- public release(s);
- repository activity/contributors/stars/forks;
- website usage;
- downloads/installations;
- pilot users/interviews;
- external reviews;
- citations/DOI;
- grant/accelerator applications or awards;
- revenue.

Never substitute application counts or repository development activity for customer traction unless the question explicitly asks for them.

## Legal entity / incorporation

PLACEHOLDER — answer exactly as the current form requests. Do not infer a company from the project name, website, domain, grant application, or repository.

## Funding raised

PLACEHOLDER — state only documented equity, debt, grants, prizes, or revenue as the form defines them.

## Location / residency / nationality / sanctions

PLACEHOLDER — answer exactly and truthfully. Do not use another person, company, wallet, or location to bypass eligibility or sanctions screening.

## Full-time commitment

PLACEHOLDER — the current public Cohort 9 eligibility page states that at least one full-time founder is required. Confirm the applicant can truthfully satisfy this before submission.

## Closing application statement

CogniPrint is already building the evidence layer; Aquarium would be used to make that evidence independently verifiable through XRPL without turning the project into a token product or exposing sensitive content. The goal for the cohort is a small, rigorous, reusable trust primitive that can move from Testnet demonstration to production readiness with clear privacy and failure boundaries.
