# Open Technology Fund Internet Freedom Fund — CogniPrint fit memo

Status date: 2026-07-25

## Official programme facts

OTF's Internet Freedom Fund accepts applications on a rolling basis. It supports technology development, applied research, digital security ecosystem work, and related internet-freedom efforts. Awards are published as $10,000–$900,000 for up to 24 months, with OTF describing $50,000–$200,000 over 6–12 months as an ideal request range for many applicants.

The programme evaluates whether a proposal fits OTF's internet-freedom remit, solves a real problem, is cost-effective and sustainable, and complements existing efforts.

Official reference:

- https://www.opentech.fund/funds/internet-freedom-fund/

## Current CogniPrint fit

**Fit today: conditional and weaker than the generic grant narrative suggests.**

OTF is not a general-purpose AI research fund. Its remit is centered on people and communities exposed to censorship, surveillance, and repressive information controls.

A proposal framed only as “detect which AI made a text” is not a strong OTF fit.

## Potential OTF-aligned research question

A more relevant direction would be:

> Can an open, privacy-preserving evidence tool help journalists, researchers, and civil-society investigators examine suspicious or manipulated digital text while keeping sensitive material local and clearly separating statistical hypotheses from authenticated provenance?

This remains a proposed use case until real user need is documented.

## Required work before a Concept Note

### 1. Validate user need

Obtain documented input from at least a small number of relevant practitioners such as journalists, digital-security researchers, or civil-society investigators working with censorship/disinformation/surveillance risks.

Questions should establish:

- what evidence problems they actually face;
- what data is too sensitive to upload to centralized services;
- whether provenance/fingerprint outputs would change a real workflow;
- what false-positive or attribution risks would be unacceptable;
- what languages and environments matter.

### 2. Build the privacy-preserving use case

Prefer a local/offline or privacy-preserving workflow where raw text does not have to leave the user's device.

### 3. Define the internet-freedom outcome

The proposal must explain the concrete benefit to people exposed to censorship or surveillance, rather than relying on broad AI-safety language.

### 4. Map complementary efforts

The application should explicitly distinguish CogniPrint from existing AI-text detectors, provenance standards, and digital-forensics tools. It should explain what gap remains and why an open-source, uncertainty-aware evidence layer is useful.

## Possible work packages

**WP1 — Practitioner discovery and threat model**  
Interview relevant users, document workflows, threat models, data-sensitivity requirements, and high-cost failure modes.

**WP2 — Local evidence workstation**  
Develop a privacy-preserving analysis mode that keeps sensitive text local and exports bounded evidence bundles.

**WP3 — Multilingual robustness study**  
Test the descriptive fingerprint and future attribution hypotheses across languages/domains relevant to the selected practitioner group, including translation and human-edit conditions.

**WP4 — Provenance integration**  
Prototype support for hashes, revision history, and signed provenance metadata while preserving a strict distinction between observed content signals and authenticated records.

**WP5 — Independent evaluation**  
External methodological review plus practitioner usability/safety review, including false-positive and misuse analysis.

## Claims to avoid

Do not state that CogniPrint currently:

- identifies an exact neural model from arbitrary text;
- determines who commissioned or authored a document;
- proves disinformation or malicious intent;
- provides forensic proof suitable for legal action;
- solves censorship or surveillance by itself.

## Go/no-go gate before submission

A Concept Note should be submitted only after:

- [ ] a real internet-freedom practitioner problem is documented;
- [ ] at least one intended user group is clearly defined;
- [ ] the privacy/local-processing requirement is concrete;
- [ ] the proposal complements rather than duplicates existing tools;
- [ ] a 6–12 month deliverable plan and cost model are credible;
- [ ] sanctions/export eligibility is re-checked for the actual applicant/payment arrangement;
- [ ] the current OTF guide and Concept Note form are re-checked immediately before submission.

## Current recommendation

Do **not** send a generic CogniPrint application to OTF yet. First document a real internet-freedom user need and connect the research programme to that workflow. If that evidence exists, OTF becomes a potentially serious funding target; without it, the application is likely to look outside remit.
