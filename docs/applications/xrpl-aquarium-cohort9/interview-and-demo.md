# XRPL Aquarium Cohort 9 — Interview and Demo Pack

Status: `DRAFT / NOT SUBMITTED`

## 60-second founder pitch

AI content is increasingly produced through chains of models, human edits, translation tools, and agents. In those workflows, a simple “AI or human” score is not enough. Teams need evidence they can inspect, reproduce, exchange, and verify.

CogniPrint is an open-source evidence framework for synthetic language. It creates structured evidence packages with measurable signals, artifact hashes, reproducibility metadata, uncertainty states, and explicit non-claims.

During Aquarium, we want to add a narrow XRPL trust layer: keep sensitive evidence off-chain, create a deterministic commitment to a public-safe evidence manifest, anchor that commitment in an XRPL transaction, and let an independent verifier confirm the exact evidence state against a validated ledger.

The blockchain does not decide whether content is AI-generated. It makes the evidence record tamper-evident and independently verifiable. Our 9-week goal is a working Testnet integration, independent verifier, self-hosted workflow, test vectors, and a reusable open-source reference pattern for evidence-oriented XRPL applications.

## 20-second answer: what is CogniPrint?

CogniPrint is open-source infrastructure for turning synthetic-language analysis into reproducible evidence packages. The XRPL integration adds public integrity verification to those packages without putting private text or sensitive evidence on-chain.

## 20-second answer: why blockchain?

We do not need blockchain for the analysis itself. We need it only for one thing a private database cannot provide as cleanly across organizations: a durable public commitment that an independently received evidence manifest can later be checked against.

## 20-second answer: why XRPL?

XRPL gives us a straightforward transaction and validated-ledger model plus compact memo transport, so we can keep the product small: evidence stays off-chain, only the commitment is public, and verification does not require a token design.

## 20-second answer: what is defensible?

The anchor is not the moat. The defensible part is the evidence workflow around it: reproducible manifests, explicit uncertainty, privacy boundaries, fail-closed verification states, and integration with content-analysis and evidence-handling workflows.

## 20-second answer: why not just timestamp a PDF?

Because timestamping an arbitrary file proves very little about how the evidence was produced. CogniPrint structures the evidence itself: what was measured, with which software and references, what changed, what is uncertain, and what is explicitly not claimed. XRPL then protects the integrity of that structured evidence state.

## 20-second answer: what does the ledger prove?

It proves that a specific cryptographic commitment was included in a validated ledger transaction and can be matched against a recomputed commitment. It does not prove authorship, model identity, scientific correctness, lawful collection, or legal chain of custody.

## 20-second answer: why open source?

Evidence verification should not require trusting CogniPrint as a black box. Open schemas, test vectors, and verifier logic let third parties reproduce the check and make the integration useful as XRPL infrastructure, not just as a feature inside one product.

## 2-minute product demo storyboard

### 0:00–0:20 — show a real evidence package

Open a CogniPrint Evidence Capsule / public-safe dossier manifest. Point out only the fields needed for the demo: artifact identifier, schema/version references, file hashes or result commitments, and explicit non-claim/verification metadata.

Narration:

“Here is the evidence package. The source content and sensitive material stay local. What we want to make public is only a cryptographic commitment to this safe manifest.”

### 0:20–0:40 — create deterministic commitment

Run the local anchor command/prototype and display:

- anchor schema version;
- commitment algorithm;
- 64-character SHA-256 manifest commitment;
- artifact schema identifier.

Narration:

“The same canonical manifest always produces the same commitment. We reject malformed and non-interoperable inputs instead of silently producing an anchor.”

### 0:40–1:05 — publish to XRPL Testnet

Once the transport is implemented, show submission of the compact payload in an XRPL Testnet transaction Memo. Display the returned transaction hash but do not expose a seed, private key, API credential, or wallet secret.

Narration:

“Only this compact payload goes to XRPL. No raw text, private evidence, prompts, personal data, or secrets are placed on-chain.”

### 1:05–1:25 — independent verification

Use a verifier that resolves the transaction, confirms it belongs to a validated ledger, decodes the anchor payload, recomputes the local commitment, and returns:

`VALIDATED_MATCH`

Narration:

“A second party can verify the evidence state without trusting our database and without receiving any blockchain secret.”

### 1:25–1:45 — mutation test

Change one manifest field in a copy of the evidence package and re-run verification. Show:

`VALIDATED_MISMATCH`

Narration:

“If the evidence package changes, verification fails closed. We never convert a mismatch or an unvalidated transaction into a successful result.”

### 1:45–2:00 — end on boundaries and value

Show three lines:

- evidence private / commitment public;
- independently verifiable integrity;
- evidence, not verdicts.

Narration:

“XRPL does not make our scientific conclusions true. It makes the state of the evidence independently verifiable. That narrow boundary is what makes the workflow useful for investigators, publishers, trust-and-safety teams, and other organizations exchanging digital evidence.”

## Interview questions we should expect

### Why does this need XRPL instead of GitHub timestamps?

GitHub is valuable development evidence but is not the neutral application-level trust boundary for every evidence package or every organization. An XRPL commitment can be created independently of repository publication, attached to a specific evidence event, and verified by parties that do not share the same code-hosting account or workflow. GitHub and XRPL can be complementary evidence classes.

### What data goes on-chain?

Only the minimal anchor payload: schema identifier, commitment algorithm, evidence-manifest commitment, artifact type, and public artifact-schema identifier. Sensitive evidence remains off-chain.

### Are you building a token?

No. The current use case does not require a token. The value is verifiable evidence integrity and interoperability.

### What happens if XRPL is unavailable?

Local evidence creation should continue. The receipt remains in a not-yet-validated/not-verifiable state until the network record can be confirmed. The system should never fabricate validation.

### How will you measure success after nine weeks?

A third party should be able to take a public-safe CogniPrint manifest and transaction reference, independently resolve a validated Testnet transaction, recompute the deterministic commitment, and receive a correct match/mismatch result without exposing the underlying private evidence.

### Why will users care?

The strongest early users are those who already exchange or audit evidence across trust boundaries. The value is not a blockchain badge; it is reducing disputes about whether the reviewed evidence package is the same package that was originally produced and recorded.

## Red-flag answers to avoid

Do not say:

- “blockchain proves the content is true”;
- “we can identify exactly which AI wrote any text”;
- “this is legally admissible evidence”;
- “XRPL gives us chain of custody”;
- “we already have a production XRPL deployment”;
- “we need a token to monetize this”;
- unsupported customer/revenue/partnership/funding numbers.

## Demo security checklist

- use Testnet only for the cohort prototype;
- never screen-share a seed/private key;
- never hard-code wallet credentials in the repository;
- never upload source evidence to the ledger;
- use a disposable Testnet account for demonstrations;
- show transaction hash and verification result, not signing secrets;
- preserve `NOT_VALIDATED` and `NOT_VERIFIABLE` as legitimate states.
