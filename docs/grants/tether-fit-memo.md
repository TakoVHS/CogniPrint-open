# Tether Developer Grants — CogniPrint fit memo

Status date: 2026-07-25

## Official programme facts

Tether's Developer Grants programme is open and funds developers building on its open technology stack. Current programme language emphasizes local-first AI, peer-to-peer systems, cryptography, open standards, applications built on Tether's stack, documentation, and technical research. Awards are tied to concrete deliverables rather than open-ended project funding.

Public programme references:

- https://tether.io/news/tether-launches-developer-grants-program-to-fund-local-first-ai-and-payments-infrastructure/
- https://tether.dev/

The public site currently lists examples such as QVAC work and says it is looking for new applications powered by the Tether stack, research into edge AI/P2P/cryptography, and tooling/integrations/open standards.

## Current CogniPrint fit

**Fit today: conditional, not submission-ready.**

CogniPrint's public core is browser/local descriptive text analysis, which is directionally compatible with privacy-preserving local-first AI. However, the repository does not currently demonstrate a substantive QVAC/WDK/Pears integration.

A generic application saying “CogniPrint is an AI provenance project” would be weak because it would not show why Tether's technology stack is necessary.

## Strongest bounded proposal

### CogniPrint Local Evidence Node

A small open-source module that runs text-fingerprint analysis locally and produces a portable evidence bundle without uploading the analysed text to a centralized CogniPrint server.

Proposed deliverables:

1. local inference/analysis adapter compatible with the selected Tether local-first stack component;
2. deterministic CogniPrint feature extraction and input hashing on-device;
3. machine-readable evidence bundle with feature-map version, metrics, uncertainty boundary, and provenance placeholders;
4. reproducible demo showing that sensitive input can remain local;
5. documentation and tests;
6. no claim of exact-model attribution unless separately validated.

## Why this is a better fit

The application should focus on **privacy-preserving local evidence analysis**, not on speculative model attribution.

Core value proposition:

> Researchers and journalists may need to inspect sensitive text without sending the content to a centralized analysis service. CogniPrint Local Evidence Node would keep the input local, generate reproducible descriptive fingerprints, and export a bounded evidence package that clearly separates measurement from provenance claims.

## Go/no-go gate before submission

Submit only after all are true:

- [ ] one Tether stack component is selected for a real integration;
- [ ] a minimal working branch exists;
- [ ] the integration is necessary rather than decorative;
- [ ] the deliverable can be completed within the selected grant/bounty scope;
- [ ] tests and documentation are included;
- [ ] no unsupported claim that CogniPrint can identify an exact model or actor;
- [ ] current active grant/bounty details are re-checked immediately before submission.

## Current recommendation

Do **not** submit the generic CogniPrint project yet. Build the smallest credible local-first integration first, then apply with that concrete deliverable.
