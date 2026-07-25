# CogniPrint website message architecture

Status: implementation brief for the live website. This is product/communication copy guidance, not a scientific-results document.

## Core rule

The homepage may communicate the large problem and research direction strongly, but it must never imply that future research targets are current validated capabilities.

Use two layers of truth:

1. **Public / product layer:** memorable problem, vision, evidence-first value proposition.
2. **Research layer:** exact current capability, protocols, data, limitations, readiness and non-claims.

Both layers must remain factually compatible.

## Recommended hero

### Eyebrow

`COGNITIVE PROVENANCE • OPEN RESEARCH INFRASTRUCTURE`

### Headline

> **Soon, “AI-generated” will describe almost nothing.**

### Supporting line

> A digital artifact may pass through several models, humans, translation systems and agents before publication. CogniPrint studies the traces that process leaves — and preserves the evidence needed to audit what we can and cannot conclude.

### Short product thesis

> **CogniPrint investigates the trail.**

### Primary calls to action

- **See the evidence**
- **Run the benchmark**
- **For researchers**

Do not use a primary CTA such as “Detect AI now” while scientific readiness is `descriptive_only`.

## Alternative hero for a more conservative launch

### Headline

> **The synthetic internet needs an evidence layer.**

### Supporting line

> CogniPrint is open research into reproducible fingerprints, human–AI production changes and verifiable provenance — with uncertainty and failure conditions kept visible.

## The three homepage questions

The first screen or first scroll should frame the problem around:

1. **What process produced this artifact?**
2. **Where did the process change?**
3. **What evidence do we actually have — and what remains unknown?**

Avoid claiming that CogniPrint currently answers all three.

## Fingerprint metaphor block

> **Humans leave fingerprints. Generative systems may leave statistical traces. CogniPrint studies those traces.**

Immediately follow with the boundary:

> A CogniPrint fingerprint is a reproducible statistical profile, not a unique biological-style identifier and not proof of a particular model or author.

## Why binary detection is too small

Visual sequence:

`Human → Model A → human rewrite → Model B → translation → publishing agent`

Caption:

> Real digital production is increasingly a chain, not a binary label.

Then introduce the research term:

> **Generation lineage** is CogniPrint’s research target for representing that chain with candidate regimes, change points, uncertainty and external provenance evidence.

Add a visible badge:

`RESEARCH TARGET — NOT YET A VALIDATED CAPABILITY`

## Evidence, not verdicts block

Headline:

> **Every conclusion should come with evidence.**

Show a visual Evidence Bundle / Evidence Capsule containing:

- artifact SHA-256;
- feature-map version;
- reference-registry version;
- measured coordinates;
- candidate families;
- alternatives;
- calibration state;
- UNKNOWN / insufficient-evidence state;
- provenance assertions;
- software commit;
- reproduction command.

Copy:

> CogniPrint is designed to preserve the trail behind a conclusion, not just display a score.

## UNKNOWN block

Headline:

> **A trustworthy system must be allowed to say: I don’t know.**

Copy:

> Unknown models, short text, strong editing, translation and distribution shift can make attribution unsafe. CogniPrint treats `UNKNOWN / OUT OF DISTRIBUTION / INSUFFICIENT EVIDENCE` as required outputs, not edge cases.

## Where it fails block

Headline:

> **Failure is part of the evidence.**

Copy:

> We publish where fingerprints collapse: short text, domain shift, human rewriting, translation, unseen models, model drift and conflicting provenance.

CTA:

- **Where CogniPrint fails** → `docs/where-cogniprint-fails.md`

This block should be visually prominent, not hidden in the footer.

## Attribution Challenge 001 block

Headline:

> **Can model families leave stable signatures? We’re testing it blind.**

Copy:

> Attribution Challenge 001 freezes the protocol before labels are revealed. It compares CogniPrint against length, surface-statistic and n-gram baselines, includes unseen sources and transformations, and requires an UNKNOWN class.

CTAs:

- **Read the protocol**
- **See the evidence** (only after real results exist)

Before results exist, do not use “See results”.

## Current state block

Use explicit status cards:

### Implemented

- deterministic 12D text profile;
- comparison and perturbation diagnostics;
- reproducibility artifacts;
- external RAID pilot infrastructure;
- Evidence Capsule privacy/integrity tooling.

### Research targets

- calibrated model-family candidates;
- human–AI intervention map;
- fingerprint drift registry;
- cross-model lineage;
- provenance fusion.

### Not claimed

- exact model identity from arbitrary text;
- definitive AI origin;
- authorship identity;
- commissioning actor;
- legal/forensic proof.

## Audience block

Prioritise:

- researchers;
- journalists/newsrooms;
- fact-checkers;
- digital-forensics and OSINT teams;
- platform trust & safety;
- archives;
- model-evaluation researchers;
- provenance/tooling teams.

Do not centre the homepage on school-essay detection.

## Commercial framing

Avoid:

> “87% AI”

Prefer:

> **Give us the artifact. We return a reproducible evidence dossier.**

For the current research release, qualify this as the intended product direction rather than a fully validated forensic service.

## Future multimodal architecture

A long-term architecture diagram may show:

- CogniPrint Text — current research engine;
- CogniPrint Image — future;
- CogniPrint Audio — future;
- CogniPrint Video — future;
- CogniPrint Agent — future;
- CogniPrint World — future;
- CogniPrint Evidence Graph — future common evidence layer.

Every unimplemented module must be marked `FUTURE / RESEARCH VISION`.

## Footer scientific boundary

Keep a persistent plain-language boundary:

> CogniPrint’s current public release is `descriptive_only`. It does not currently establish exact model identity, AI origin, authorship, actor identity, intent, legal status or forensic provenance. Stronger capabilities remain experimental until dedicated benchmark and independent-review gates are satisfied.

## Navigation recommendation

- **Vision** — the synthetic-internet / cognitive-provenance problem.
- **Evidence** — current artifacts and Evidence Capsules.
- **Challenge 001** — preregistered benchmark protocol/results.
- **Where it fails** — negative results and boundaries.
- **Research** — dry methodology, manuscript, data and reproducibility.
- **For reviewers** — reviewer bundle.
- **Source** — GitHub.

## Language strategy

International reviewers should be able to reach English scientific material in one action from the root page.

The Russian public page may be more narrative, but all capability/status labels must match the English research language exactly.

## Copy rule

The homepage may say:

> “CogniPrint studies fingerprints of AI-assisted content.”

The research page must say exactly what that currently means:

> “CogniPrint constructs reproducible statistical text profiles and tests whether stronger source/provenance hypotheses survive controlled benchmarks.”

Those statements are compatible. Neither should be silently upgraded into “CogniPrint knows which model wrote this.”
