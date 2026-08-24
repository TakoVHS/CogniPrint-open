# Grant readiness for the next funding cycle

Status date: 2026-07-26

## Positioning for funders

CogniPrint should be presented as an **open, reproducible research programme for cognitive provenance**, not as a finished AI detector and not as a tool that can already identify a person, organisation, or exact neural model from arbitrary text.

The strongest common narrative is:

> As AI becomes embedded into documents, agents, translation, media and software workflows, the useful trust question is no longer only “AI or human?” but what production process is consistent with the evidence, where that process changed, and what remains unknown. CogniPrint provides a local descriptive measurement layer, preregisterable attribution research, explicit abstention/failure boundaries and reproducible evidence artifacts that keep content-derived inference separate from authenticated provenance.

## Active funding tracks are intentionally different

Do not send the same application to every funder.

### Track A — Tether Developer Grants

**Status: HOLD pending one real QVAC runtime artifact.**

Deliverable: bounded local QVAC explanation layer over a redacted CogniPrint evidence envelope.

Do not submit until the QVAC SDK/model path has executed on a supported runtime and a real local explanation artifact is archived.

### Track B — Open Technology Fund

**Status: NO-GO pending practitioner discovery.**

Potential package: local evidence workstation for high-risk internet-freedom investigations.

Do not write a Concept Note from hypothetical user pain. At least three practitioner conversations and a documented GO decision are required first.

### Track C — Autonomys / Subspace Foundation

**Status: HOLD pending real Auto Drive CID round-trip.**

Deliverable: privacy-bounded CogniPrint Evidence Capsule stored by content-addressed CID without raw source text by default.

Local schema/privacy/integrity tests exist; network/storage capability is not claimed until upload → CID → retrieval → verification succeeds.

### Track D — FUTO

**Status: conditional GO for a short engineering inquiry once public-facing materials are consistent.**

Recommended package: **CogniPrint Local Provenance Workstation** — local-first, open-source evidence analysis without requiring sensitive source upload to a centralized detector.

FUTO does not need the Tether or Autonomys integrations to make the core user-control story meaningful.

Current blocker: live `cogniprint.org` still needs to match the current GitHub positioning, or the initial inquiry should link primarily to the public research repository.

### Track E — NLnet Open Internet Stack

**Status: WATCH / do not submit a generic proposal now.**

Regular calls are temporarily paused during the transition from NGI Zero to the Open Internet Stack. Taler and Fediversity remain narrowly scoped exceptions.

Use the 29 July 2026 NLnet Office Hour for one architectural fit question. Monitor Restack and CodeSupply after summer; activate only a programme whose published guide maps to a real CogniPrint deliverable.

### XRPL

**Status: NO-GO.**

No XRP Ledger-native requirement currently exists in CogniPrint. Do not add a ledger dependency merely to fit a grant.

## Flagship research package

The central scientific package is now **Attribution Challenge 001** rather than an unspecified “model detector”.

It includes:

1. blind family-level evaluation;
2. human controls;
3. lineage-safe splits;
4. length/surface/n-gram baselines;
5. calibration;
6. held-out unseen source families;
7. mandatory `UNKNOWN / OUT OF DISTRIBUTION / INSUFFICIENT EVIDENCE`;
8. paraphrase, translation, human-edit and AI-to-AI rewrite stress tracks;
9. public falsification/stop criteria;
10. `Where CogniPrint fails` reporting.

Protocol: `docs/attribution-challenge-001.md`.

## Fundable work packages

Prefer applications that fund a bounded package:

1. **Attribution Challenge 001** — controlled model-family benchmark with open-world abstention and negative results.
2. **Human–AI Intervention Map** — controlled revision chains and statistical regime-change detection.
3. **Fingerprint Registry & Drift** — versioned reference distributions and expiry/revalidation rules.
4. **Provenance Fusion** — separate content-derived measurements from signed/authenticated evidence.
5. **Reproducible Evidence Infrastructure** — Evidence Capsules/dossiers containing hashes, versions, calibration context, uncertainty and non-claims.

## Required gates before stronger broad-call submissions

1. Keep scientific readiness at `descriptive_only` until evidence justifies a change.
2. Obtain at least one substantive independent methodological review; automated replies and funding correspondence do not count.
3. Treat DOI `10.5281/zenodo.20756421` as citation/administrative metadata only; public DOI availability does not validate stronger scientific claims.
4. Execute Attribution Challenge 001 or clearly label it as an unexecuted protocol.
5. Re-run public reproduction and secret-scan commands on the exact release candidate used for an application.
6. Re-check official programme scope, eligibility and deadline immediately before submission.
7. Separate **implemented capability**, **hypothesis**, **proposed experiment**, **prototype**, and **future deployment** in every application.
8. Preserve UNKNOWN/abstention and failure reporting in any attribution-related proposal.

## Claims that must not appear as current facts

Until dedicated validation exists, do not state that CogniPrint can already:

- identify the exact neural model that generated arbitrary text;
- determine which person wrote or edited a passage;
- reconstruct a multi-model generation lineage;
- identify who commissioned a generation action;
- reconstruct intent or responsibility;
- provide legal or forensic proof of provenance.

Where actor/workflow information is discussed, state that it requires independent provenance evidence such as authenticated logs, signed credentials, revision history, or other verifiable records.

## Current blockers

- External methodological reviews: `0/1`.
- GitHub Actions/Pages runner allocation is still blocking live-site deployment of the current narrative.
- Attribution Challenge 001 is specified but not yet executed.
- QVAC runtime gate is not closed.
- Auto Drive CID round-trip gate is not closed.
- OTF practitioner discovery has not yet produced a GO decision.
- NLnet regular calls are temporarily paused outside Taler/Fediversity.

This file is grant-readiness guidance. It does not expand CogniPrint's validated scientific claims.
