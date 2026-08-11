# XRPL Aquarium Cohort 9 — Submission Readiness Checklist

Status: `TECHNICALLY_READY / EXTERNAL_ELIGIBILITY_GATE_PENDING / NOT SUBMITTED`

## Public program facts verified

- Cohort: 9 / Fall 2026
- Format: 9-week online incubator
- Dates: 2026-10-12 through 2026-12-11
- Public application deadline: 2026-09-06
- Target stage: pre-seed / seed
- MVP required
- At least one full-time founder required
- Active participation throughout the program required
- Relevant thesis areas include Infrastructure / Security and Agentic Web
- Selected candidates proceed through interview and contract validation
- Startups become eligible for milestone-based grants after the program; the public cohort page does not state a guaranteed grant amount
- Program language: English

## Project fit

- [x] Existing public MVP / release
- [x] Open-source codebase
- [x] Infrastructure / Security positioning
- [x] Privacy-preserving provenance use case
- [x] Clear reason for XRPL beyond token issuance
- [x] Claims firewall drafted
- [x] Deterministic anchor prototype
- [x] Independent read-only ledger receipt verifier
- [x] Validated/mutation/ambiguous-memo verifier checks
- [x] XRPL Testnet submit transport
- [x] Real XRPL Testnet transaction validated
- [x] Real transaction hash captured
- [x] Independent ledger re-fetch by hash
- [x] `VALIDATED_MATCH` demonstrated
- [x] Mutation fails closed
- [x] Sanitized public Testnet receipt committed
- [x] Revised post-Testnet 9-week milestone plan
- [ ] Polished 2-minute screen-recorded demo captured

## Real Testnet evidence

```text
REAL_TESTNET_TX=E6E716789B416612A96221A4F51D6CA3B165E16E4777C2516D434184E9B93A21
MANIFEST_COMMITMENT=238b9c52793119d1e530b522ee853c23317ac2271cd9e12df9a1b98076352d03
VALIDATED=true
TRANSACTION_RESULT=tesSUCCESS
INDEPENDENT_LEDGER_LOOKUP=PASS
VALIDATED_MATCH=PASS
MUTATION=FAIL_CLOSED_PASS
XRPL_REAL_TESTNET_GATE=PASS
```

## Applicant facts that must be confirmed before submission

Do not commit sensitive personal records to this repository.

- [ ] Legal name as used for application/contract
- [ ] Current country of residence and current location
- [ ] Full-time-founder requirement satisfied
- [ ] Team members and roles confirmed
- [ ] Legal entity / incorporation status answered exactly as requested by form
- [ ] Any prior funding / revenue / users supported by evidence
- [ ] Availability for the full 9-week online program confirmed
- [ ] English-language interview availability confirmed

## Legal / eligibility gate

XRPL Commons' published Terms state that access may be restricted where a person is a sanctions target or is located, organized, or resident in a listed sanctioned country/territory. The published list includes Russia. The wording is not a blanket nationality-only prohibition, so citizenship and residence must not be conflated.

Before submission or reliance on a future grant/payment route:

- answer nationality, residence, location, organization and sanctions questions exactly and truthfully;
- do not imply incorporation or residence that does not exist;
- do not submit through another person, company, wallet, or location to bypass compliance screening;
- obtain written clarification from XRPL Commons if citizenship, residence, contracting, payment route, or sanctions compliance creates uncertainty;
- preserve any written eligibility response with private application records, not in the public repository.

This checklist is not legal advice and does not claim eligibility approval.

## Application evidence pack

- [x] GitHub repository
- [x] project website
- [x] current release / README
- [x] clear scientific non-claims
- [x] XRPL integration architecture
- [x] working XRPL Testnet transaction
- [x] public Testnet receipt
- [x] read-only independent XRPL receipt verifier
- [x] mutation-detection proof
- [x] revised cohort milestones
- [x] answer bank updated to working-Testnet positioning
- [ ] concise founder bio — verified applicant facts only
- [ ] exact team paragraph — verified applicant facts only
- [ ] exact traction/customer numbers, if any
- [ ] exact prior funding disclosure, if requested
- [ ] legal entity / incorporation answer
- [ ] polished screen-recorded demo asset
- [ ] final live-Typeform field mapping

## Recommended application framing

Lead with:

**“Verifiable evidence infrastructure for synthetic language, with a working privacy-preserving XRPL Testnet integrity layer.”**

Core proof sentence:

**“CogniPrint already anchors a public-safe evidence-manifest commitment to XRPL Testnet, independently re-fetches the validated transaction by hash, recomputes the local commitment, returns `VALIDATED_MATCH` for the original manifest, and fails closed after mutation.”**

Avoid leading with:

- “AI detector”;
- “blockchain for AI” without a concrete trust primitive;
- tokenization;
- legal/forensic claims;
- unique-model or author identification;
- unsupported customer/traction claims.

## Interview proof points

A strong interview/demo should demonstrate:

1. a real CogniPrint public-safe evidence manifest;
2. deterministic local commitment generation;
3. the real Testnet transaction hash;
4. `validated=true` and `tesSUCCESS`;
5. read-only independent lookup of the transaction by hash;
6. independent recomputation of the local manifest commitment;
7. `VALIDATED_MATCH`;
8. one visible manifest mutation;
9. `MUTATION=FAIL_CLOSED_PASS`;
10. why raw source evidence stays off-chain;
11. what XRPL does *not* prove.

## Hard submission gate

Do not submit until all of the following are true:

- applicant identity/team fields are correct;
- full-time-founder requirement is truthfully satisfiable;
- legal/residency/sanctions eligibility is not being guessed or bypassed;
- all traction/funding statements are evidenced;
- no future capability is presented as already deployed;
- live Typeform answers are mapped and reviewed against the claims firewall.
