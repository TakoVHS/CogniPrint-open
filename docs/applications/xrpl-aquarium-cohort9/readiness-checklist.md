# XRPL Aquarium Cohort 9 — Submission Readiness Checklist

Status: `STRONG DRAFT / REAL TESTNET MVP / NOT SUBMITTED`

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

## Project fit

- [x] Existing public MVP / release
- [x] Open-source codebase
- [x] Infrastructure / Security positioning
- [x] Privacy-preserving provenance use case
- [x] Clear reason for XRPL beyond token issuance
- [x] 9-week technical milestone plan drafted
- [x] Claims firewall drafted
- [x] Network-free deterministic anchor prototype added on isolated application branch
- [x] Prototype unit checks written
- [x] Independent read-only ledger receipt verifier implemented
- [x] Validated/mutation/ambiguous-memo verifier checks implemented
- [x] XRPL Testnet submit transport implemented
- [x] XRPL Testnet transaction validated by the live runner
- [x] Real transaction hash and sanitized public receipt captured
- [x] End-to-end technical demo flow completed
- [ ] 2–3 minute polished demo recording produced

Real Testnet transaction:

```text
E6E716789B416612A96221A4F51D6CA3B165E16E4777C2516D434184E9B93A21
```

Observed acceptance sequence:

```text
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

The current public Cohort 9 page says the online program welcomes founders from around the world, with a particular focus on EMEA. XRPL Commons' public Privacy Policy states that it may collect nationality and address and process personal data to comply with applicable legal obligations.

The publicly indexed pages reviewed for this application do not provide enough evidence to make a blanket nationality-based eligibility conclusion for the later contract or grant stage. Therefore eligibility must not be guessed either positively or negatively.

Before relying on admission or future grant/payment eligibility:

- answer nationality, residence and location questions exactly and truthfully;
- do not imply incorporation or residence that does not exist;
- do not submit through another person to bypass compliance screening;
- obtain written clarification from XRPL Commons if citizenship, residence, payment route or sanctions compliance could affect contracting or grant disbursement;
- preserve the written answer with the private application records, not in the public repository.

This checklist is not legal advice and does not claim eligibility approval.

## Application evidence pack

Prepare only evidence that is already public or can be safely shared:

- [x] GitHub repository
- [x] project website
- [x] current release / README
- [x] clear scientific non-claims
- [x] XRPL integration architecture draft
- [x] cohort milestones
- [x] read-only independent XRPL receipt verifier
- [x] real XRPL Testnet transaction hash
- [x] sanitized Testnet public receipt
- [x] mutation-detection evidence
- [ ] concise founder bio
- [ ] team slide / team paragraph if form requests it
- [ ] 60–90 second founder pitch recording
- [ ] 2–3 minute product demo recording
- [ ] screenshots of Evidence Capsule / self-hosted workflow
- [ ] exact current traction metrics, if any
- [ ] exact prior grants/funding disclosure, if requested

## Recommended application framing

Lead with:

**“Verifiable evidence infrastructure for synthetic language, with privacy-preserving XRPL commitments.”**

Avoid leading with:

- “AI detector”;
- “blockchain for AI” without a concrete trust primitive;
- tokenization;
- legal/forensic claims;
- unique-model or author identification.

## Interview proof points

A strong interview can now demonstrate:

1. a real CogniPrint Evidence Capsule or equivalent evidence manifest;
2. deterministic local commitment generation;
3. actual XRPL Testnet submission;
4. the real public transaction hash;
5. `validated=true` and `meta.TransactionResult=tesSUCCESS` as the finality gate;
6. read-only lookup of the transaction by hash;
7. independent recomputation of the local manifest commitment;
8. mutation -> fail-closed mismatch;
9. why raw evidence stays off-chain;
10. what XRPL does *not* prove.

## Hard submission gate

Do not submit until all of the following are true:

- applicant identity/team fields are correct;
- full-time-founder requirement is truthfully satisfiable;
- legal/residency eligibility is not being guessed or bypassed;
- all traction/funding statements are evidenced;
- no future capability is presented as already deployed;
- final form answers have been reviewed against the claims firewall.
