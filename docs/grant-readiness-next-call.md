# Grant readiness for the next regular open call

Status date: 2026-07-25

## Positioning for funders

CogniPrint should be presented as an **open, reproducible research programme for synthetic-language fingerprints and provenance**, not as a finished AI detector and not as a tool that can already identify a person, organisation, or neural model from arbitrary text.

The strongest grant narrative is:

> As AI increasingly mediates documents and digital environments, the hard problem is no longer only “AI or human?” but how to build auditable evidence about the production process. CogniPrint provides the current descriptive fingerprinting layer and proposes controlled research on model-family attribution, human–AI intervention mapping, and fusion with cryptographic or workflow provenance.

This framing is ambitious while remaining consistent with the public evidence.

## Fundable work packages

Prefer applications that fund a falsifiable research package with explicit deliverables:

1. **Model fingerprint benchmark** — controlled multilingual corpus across known model families, prompt regimes, domains, and sampling settings.
2. **Human–AI coauthoring study** — sentence/span-level intervention mapping and revision-chain analysis.
3. **Provenance fusion prototype** — combine content-derived fingerprints with signed metadata, hashes, tool logs, or C2PA-style credentials.
4. **Robustness/evasion evaluation** — paraphrasing, translation, rewriting, model updates, and substantial human edits.
5. **Reproducible evidence bundles** — machine-readable outputs with hashes, feature versions, calibration context, uncertainty, and explicit non-claims.

A useful grant result may be positive, negative, or mixed. Demonstrating where attribution fails is scientifically valuable.

## Current decision on NLnet

Do not submit CogniPrint to the August 1, 2026 NLnet call unless the project independently develops work that genuinely fits NGI Taler or NGI Fediversity. The current CogniPrint research scope does not claim such fit.

## Required gates before the next broad open-call submission

1. Keep scientific readiness at `descriptive_only` until evidence justifies a change.
2. Obtain at least one substantive external methodological review from a qualified independent reviewer; automated replies and funding correspondence do not count.
3. Resolve or replace the unverified Zenodo DOI reference before presenting a DOI as publicly verified.
4. Re-run the documented public reproduction and secret-scan commands on the exact release candidate used for an application.
5. Update grant text only from verified public facts and clearly disclose generative-AI assistance where a funder requires it.
6. Re-check the official programme scope and deadline immediately before submission; do not reuse an old call's eligibility assumptions.
7. For every application, separate **implemented capability**, **hypothesis**, **proposed experiment**, and **future deployment**.

## Claims that must not appear as current facts

Until dedicated validation exists, do not state that CogniPrint can already:

- identify the exact neural model that generated an arbitrary text;
- determine which person wrote or edited a passage;
- identify who commissioned a generation action;
- reconstruct intent or responsibility;
- provide legal or forensic proof of provenance.

Where actor or workflow information is discussed, state that it would require independent provenance evidence such as authenticated logs, signed credentials, revision history, or other verifiable records.

## Current blockers

- External methodological reviews: `0/1`.
- DOI `10.5281/zenodo.20756421` is not yet directly verified through a public Zenodo record.
- NLnet's regular open call is temporarily paused; the August 1 call is restricted to Taler/Fediversity.
- The model-attribution and human–AI coauthoring layers do not yet have dedicated controlled benchmarks in the public release.

This file is grant-readiness guidance. It does not expand CogniPrint's validated scientific claims.
