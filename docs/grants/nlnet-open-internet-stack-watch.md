# NLnet Open Internet Stack — CogniPrint watch memo

Status date: 2026-07-26

## Current decision

**WAIT / WATCH — do not submit a generic CogniPrint proposal now.**

NLnet has temporarily paused regular open calls while transitioning from NGI Zero to the Open Internet Stack. As of this status date, ordinary proposals outside the narrowly scoped NGI Taler and NGI Fediversity programmes should wait until the regular calls reopen after summer 2026.

Official references:

- https://nlnet.nl/news/2026/20260612-NGIZero-stocktaking.html
- https://nlnet.nl/propose/
- https://nlnet.nl/events/20260729/index.html
- https://nlnet.nl/restack/
- https://nlnet.nl/codesupply/
- https://nlnet.nl/ELFA/

## Office Hour

Confirmed event:

- Wednesday, **29 July 2026**;
- **16:00 CEST**;
- NLnet Office Hour Matrix room;
- applications are **not** pre-reviewed during the session.

The correct use of the session is one architectural fit question, not a request to evaluate a draft.

### Recommended question

> **Would an open-source, reproducible evidence/provenance framework for AI-assisted digital artifacts — focused on local measurement, uncertainty, auditability and versioned evidence rather than opaque AI detection — potentially fit one of the upcoming Open Internet Stack programmes, and which programme should we monitor most closely?**

If they ask for more specificity, add:

> CogniPrint currently has a local deterministic text-profile core, preregistration-ready attribution benchmark design, a public failure/abstention contract, and a privacy-bounded Evidence Capsule that preserves hashes, software/configuration versions and typed provenance states without storing raw source text by default.

Do not ask:

> “Can you review our grant application?”

## Programme comparison

### Restack — possible broad fit

Restack is intended to support a healthy open internet stack and open, resilient, trustworthy digital infrastructure, including local-first infrastructure and user-facing applications.

Possible CogniPrint angle:

- local-first evidence tooling;
- user-controlled provenance;
- open standards/interfaces;
- reproducible trust infrastructure.

Risk: the fit may be too broad unless the call guide explicitly includes provenance/trust/evidence tooling.

Decision: **monitor**.

### CodeSupply — narrow but technically interesting fit

CodeSupply focuses on trusted/verified software metadata, software supply-chain visibility, traceability, auditability, conflicting/outdated metadata, compliance and open-source licensing.

This is not a direct fit for CogniPrint Text as a content-attribution engine.

However the **Evidence Capsule / evidence-state architecture** may be relevant if adapted to a genuine software-supply-chain problem such as:

- reproducible AI-generated code-analysis evidence;
- verifiable metadata about which model/tool/version produced or modified a code artifact;
- evidence bundles linking software artifacts, SBOM/provenance records, model/tool execution metadata and reproducibility hashes;
- conflicting provenance-state representation.

Do not force this connection. CodeSupply should become an active target only if the project can demonstrate a real software-supply-chain use case, not merely rename text provenance as supply-chain provenance.

Decision: **conditional watch**.

### ELFA — currently weak fit

ELFA is oriented toward encrypted local-first collaborative architecture and workspaces.

Possible overlap exists around local/private evidence workflows, but CogniPrint is not currently a collaborative workspace platform.

Decision: **weak / watch only** unless the final guide creates a specific fit.

## Current recommendation

1. Do not submit to Taler or Fediversity merely because they are open.
2. Attend/use the 29 July Office Hour for the single fit question above.
3. Record NLnet's answer verbatim or as a clearly marked paraphrase.
4. Re-check Restack/CodeSupply/ELFA guides after summer when calls actually open.
5. Activate only the programme whose published scope maps to a real CogniPrint deliverable.

## Strongest possible future NLnet package

If the programme fit is confirmed, the strongest package is likely not “AI detector development.”

It is closer to:

> **Open, local-first cognitive-provenance infrastructure that produces reproducible evidence bundles, separates statistical inference from authenticated provenance, exposes UNKNOWN/failure states, and can interoperate with open metadata/provenance standards.**

Potential technical deliverables:

- open Evidence Capsule schema;
- local evidence workstation;
- reference-registry/drift protocol;
- signed/provenance metadata adapter;
- reproducible challenge/evaluation artifacts;
- standards-facing interfaces where relevant to the selected programme.

## Go/no-go gate

Move from WATCH to GO only after:

- [ ] the specific Open Internet Stack call is actually open;
- [ ] the current guide is read in full;
- [ ] CogniPrint maps to a named programme objective without semantic stretching;
- [ ] a concrete FOSS deliverable is defined;
- [ ] applicant/geographic/financial eligibility is verified;
- [ ] the application does not rely on unvalidated attribution claims;
- [ ] the website/repository tell the same current-capability story.
