# CogniPrint mapping to NIST AI RMF / Generative AI Profile

Status: **informative mapping only; CogniPrint is not certified, approved, or endorsed by NIST.**

Status date: 2026-07-26.

References:

- NIST AI RMF 1.0: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- NIST AI RMF: Generative AI Profile (NIST AI 600-1): https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

NIST describes the AI RMF as a voluntary framework for managing AI risk. The Generative AI Profile is a companion resource for generative-AI risk management.

This document maps CogniPrint engineering/evidence practices to relevant risk-management concepts. It does not claim formal conformity.

## Mapping principles

### Govern / documentation

CogniPrint practice:

- explicit scientific readiness (`descriptive_only`);
- Claim Firewall policy version;
- machine-readable limitations;
- high-stakes non-use boundary;
- external-review register/gates;
- dataset/data-governance rules.

Purpose:

Keep system scope, limitations, responsibilities and decision boundaries visible rather than relying on implicit operator knowledge.

### Map / context and intended use

CogniPrint practice:

- separate Research API concepts from future safe/Decision API concepts;
- identify intended low-risk pilot users;
- document domain/language/reference-space scope;
- preserve OOD/UNKNOWN outcomes;
- prohibit unsupported authorship/actor/legal conclusions.

Purpose:

Avoid treating a benchmark result as universal across users, domains or decision contexts.

### Measure / TEVV

CogniPrint practice:

- preregistered Attribution Challenge 001;
- transparent baselines;
- calibration metrics;
- OOD/generator holdout;
- temporal/domain/language holdouts;
- transformation and human-edit stress tests;
- public failure reporting;
- independent evaluator design;
- reproducibility hashes/versions.

Purpose:

Measure not only predictive performance but calibration, uncertainty, generalisation and failure behaviour.

### Manage / risk controls

CogniPrint practice:

- Claim Firewall;
- minimum-evidence policy;
- UNKNOWN/abstention;
- zero-retention/local-first design target;
- provenance conflict reporting;
- no automatic resolution of contradictory evidence;
- high-stakes single-output prohibition;
- versioned evidence/case artifacts.

Purpose:

Reduce harm from overconfidence, false attribution, stale reference data, privacy leakage and downstream misuse.

## Evidence categories relevant to risk management

CogniPrint uses four truth classes:

- `OBSERVED` — directly measured;
- `INFERRED` — probabilistic and benchmark-bounded;
- `ATTESTED` — external provenance statement with validation status;
- `UNKNOWN` — insufficient/OOD/conflicting/unsupported.

This separation supports traceability because downstream users can see whether a statement is a measurement, inference, external declaration or unresolved question.

## Specific GAI risks CogniPrint is designed to surface, not solve alone

Potentially relevant risk areas include:

- confabulated or misleading provenance claims;
- overreliance on uncalibrated AI-detection scores;
- model/domain/language distribution shift;
- synthetic-content transparency gaps;
- privacy loss from uploading sensitive artifacts to centralized analysis services;
- automation bias in high-stakes attribution;
- provenance conflicts across statistical, cryptographic and metadata sources.

CogniPrint does not claim to eliminate these risks.

## What not to say

Do not state:

- "NIST certified";
- "NIST compliant" unless a precise, independently reviewed conformity claim exists;
- "NIST approved detector";
- that this mapping demonstrates regulatory compliance.

Preferred wording:

> CogniPrint evidence and evaluation controls are mapped against relevant NIST AI RMF / Generative AI risk-management concepts for review and gap analysis.

## Review gate

Before using this mapping in enterprise materials:

- [ ] have an independent reviewer check that mapped practices actually exist in the cited release;
- [ ] record gaps as explicitly as alignments;
- [ ] update references when NIST revises AI RMF 1.0 or related profiles;
- [ ] do not convert voluntary framework mapping into a certification claim.
