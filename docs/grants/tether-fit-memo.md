# Tether Developer Grants — CogniPrint fit memo

Status date: 2026-07-25

## Official programme facts

Tether's Developer Grants programme is open and funds developers building on its open technology stack. Current programme language emphasizes local-first AI, peer-to-peer systems, cryptography, open standards, applications built on Tether's stack, documentation, and technical research. Awards are tied to concrete deliverables rather than open-ended project funding.

Public programme references:

- https://tether.io/news/tether-launches-developer-grants-program-to-fund-local-first-ai-and-payments-infrastructure/
- https://tether.dev/
- https://docs.qvac.tether.io/

The current Tether.dev page visibly lists bounties including ANE/CoreML acceleration with QVAC integration and a QVAC Swift client. Those tasks are not a natural CogniPrint fit and should not be pursued merely because they have published payouts.

Tether.dev also explicitly invites new applications powered by Tether's open stack, edge-AI research, and tooling/integrations. That is the correct route for CogniPrint if a substantive QVAC integration is demonstrated.

## Selected stack component

**QVAC SDK** is the selected component for Grant Track A.

Prototype pin:

- `@qvac/sdk`: `0.15.0`;
- runtime: Node.js `>=22.17.0`;
- initial local model: `QWEN3_600M_INST_Q4`;
- SDK flow: `loadModel()` → local `completion()` → `unloadModel()`.

The version pin is for prototype reproducibility and must be re-checked immediately before grant submission.

## Current CogniPrint fit

**Fit today: implementation in progress; not submission-ready.**

CogniPrint's deterministic Python core already computes a local text profile, SHA-256 content hash, feature-map version, metrics, normalized fingerprint coordinates, and a scientific disclaimer without embedding the original source text in the analysis payload.

The experimental integration under `integrations/qvac/` adds a strict redaction boundary before QVAC:

1. sensitive text is processed only by the local deterministic CogniPrint core;
2. CogniPrint emits a profile JSON without raw source text;
3. a whitelist sanitizer removes local paths and all non-approved fields;
4. QVAC receives only `cogniprint-local-evidence-v1` JSON;
5. the local model produces a human-readable explanation under explicit non-claims.

This makes QVAC substantive rather than decorative: its role is a private local explanation layer for sensitive research evidence where sending the source or evidence to a cloud LLM would defeat the privacy goal.

## Proposed bounded deliverable

### CogniPrint Local Evidence Node

A small open-source QVAC integration that turns deterministic CogniPrint measurements into a local-only, human-readable evidence explanation without uploading analysed text to a centralized inference service.

Deliverables:

1. deterministic CogniPrint profile and input hashing performed locally;
2. redacted machine-readable evidence envelope with fingerprint version, metrics, normalization and claim boundary;
3. QVAC local completion over the redacted evidence only;
4. tests proving that raw text/local paths do not enter the QVAC prompt;
5. reproducible demo with exact QVAC SDK/model/runtime versions;
6. explicit scientific limitations and no exact-model/actor attribution claim.

## Why this is a stronger grant story

Core value proposition:

> Researchers and journalists may need to inspect sensitive text without sending the content to a centralized analysis service. CogniPrint Local Evidence Node computes a reproducible statistical fingerprint locally, strips the source from the model-facing payload, and uses QVAC to explain the bounded evidence on-device.

This proposal directly uses the property Tether is emphasizing: local inference under user control rather than a remote AI API.

## Completed gates

- [x] Tether stack component selected: QVAC SDK.
- [x] bounded architecture defined.
- [x] QVAC package/version pinned for the prototype.
- [x] redacted evidence envelope implemented in branch form.
- [x] explicit non-claim prompt boundary implemented.
- [x] offline privacy-boundary tests written.

## Remaining go/no-go gates before submission

- [ ] run the integration on Node `>=22.17.0` with `@qvac/sdk@0.15.0` installed;
- [ ] load the selected QVAC model successfully;
- [ ] produce one real local explanation from a CogniPrint evidence JSON;
- [ ] demonstrate the steady-state inference path without a cloud inference request after model acquisition;
- [ ] preserve test output and exact runtime/model metadata;
- [ ] publish a compact demo/evidence record;
- [ ] re-check the current Tether grant application page, active scope and requested deliverable format immediately before submission.

## Claim boundary

Do not state that this module:

- identifies the exact neural model that generated arbitrary text;
- establishes authorship;
- proves AI origin;
- identifies who commissioned an action;
- provides legal or forensic provenance.

The QVAC model explains deterministic evidence; it does not create stronger evidence.

## Current recommendation

Do **not** submit yet. Finish one real QVAC runtime demonstration first. Once that evidence exists, apply as a small local-first technical deliverable rather than pitching the entire CogniPrint research programme as a generic AI grant request.
