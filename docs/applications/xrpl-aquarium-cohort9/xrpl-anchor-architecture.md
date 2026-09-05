# CogniPrint XRPL Evidence Anchor — Architecture Draft

Status: `DEVELOPMENT_ONLY / TESTNET_NOT_EXECUTED`

## Design goal

Add independent timestamp/integrity verification to CogniPrint evidence packages without putting source text, private evidence, personal data, model prompts, credentials, or secrets on a public ledger.

## Minimal architecture

```text
private/local evidence
        |
        v
Evidence Capsule / dossier
        |
        | extract public-safe manifest
        v
canonical JSON manifest
        |
        | SHA-256
        v
commitment ---------------------> XRPL transaction Memo
        |                              |
        |                              v
        |                        validated ledger
        |                              |
        +---------- verifier <---------+
```

The commitment proves equality of bytes after canonicalization. It does not prove the truth of the underlying evidence, authorship, lawful custody, or a model-source conclusion.

## Anchor payload v0.1

The proposed public payload is intentionally small:

```json
{
  "schema": "cogniprint-xrpl-anchor-v0.1",
  "commitment_alg": "sha256",
  "manifest_commitment": "<64 lowercase hex chars>",
  "artifact_type": "cogniprint-evidence-manifest",
  "artifact_schema": "<public schema identifier>"
}
```

Optional later public fields may include a non-personal project/issuer identifier or a public URI. They are not needed for the first Testnet milestone.

## Canonicalization

For the prototype, canonical bytes are UTF-8 JSON with:

- object keys sorted;
- no insignificant whitespace;
- UTF-8 characters preserved;
- NaN/Infinity rejected;
- only JSON data types accepted.

The implementation must never silently hash an unserializable or non-finite object.

## Ledger transport

XRPL transaction common fields permit `Memos` containing arbitrary hex-encoded data. The first implementation will encode the compact anchor payload as UTF-8 JSON and place it in `MemoData`, with a stable memo type/format identifier.

The transaction hash is recorded in an off-chain anchor receipt. Verification accepts an on-chain result only when the transaction is included in a validated ledger.

## Receipt states

The application-level verifier should distinguish:

- `LOCAL_COMMITMENT_READY`
- `SUBMITTED_NOT_VALIDATED`
- `VALIDATED_MATCH`
- `VALIDATED_MISMATCH`
- `TRANSACTION_NOT_FOUND`
- `MALFORMED_ANCHOR`
- `UNSUPPORTED_SCHEMA`
- `NOT_VERIFIABLE`

No ambiguous state should be upgraded to `VALIDATED_MATCH`.

## Privacy boundary

Never place the following in the XRPL memo or DID object:

- source text;
- private evidence excerpts;
- names, email addresses, phone numbers, physical addresses, or other personal data;
- prompts or hidden chain data;
- access tokens, API keys, wallet seeds, signing secrets, or credentials;
- sealed Stage B labels or research custody secrets.

The anchor is a commitment to a separately controlled manifest, not public storage for the evidence itself.

## Security boundary

A ledger anchor proves that a specific commitment was recorded by a transaction/account at a validated ledger state. It does not prove:

- the evidence was collected lawfully;
- the evidence is scientifically correct;
- a text was written by a particular person or model;
- the account owner is a legally verified identity;
- the off-chain artifact was continuously possessed by one party.

Those claims require separate evidence and policy.

## Optional Phase 2 — DID / Credentials

XRPL DID can later provide a stable decentralized identifier controlled by an XRPL account. Credentials can support issuer/subject attestations. This phase is optional and must remain privacy-minimal because XRPL ledger data is public.

Candidate use:

- evidence issuer publishes a non-personal DID;
- an organization or trusted issuer attests a narrow role/status;
- the verifier checks both the evidence commitment and the relevant identity/credential state.

This is not required to prove the Cohort 9 MVP.

## Cohort acceptance target

A successful 9-week outcome is an end-to-end Testnet demonstration where:

1. the same manifest always produces the same commitment;
2. a one-byte semantic change produces a different commitment;
3. the compact payload is anchored in an XRPL transaction;
4. the transaction is confirmed in a validated ledger;
5. an independent verifier recomputes and matches the commitment;
6. private evidence is not required on-chain;
7. failure/mismatch states remain visible and fail closed.

## Non-goals

- token issuance;
- speculative economics;
- storing evidence blobs on-chain;
- replacing content credentials or established chain-of-custody systems;
- claiming legal admissibility;
- turning XRPL into a classifier.
