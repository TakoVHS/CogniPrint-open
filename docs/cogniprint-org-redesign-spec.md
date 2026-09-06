# cogniprint.org — evidence-lab redesign specification

Status date: 2026-09-06

Implementation state: **SPEC READY / PRODUCTION UNCHANGED**

This specification defines the public research presentation for CogniPrint. It changes information architecture and visual hierarchy, not scientific readiness or research claims.

## 1. Product position

Do not present CogniPrint as an “AI detector.”

Primary position:

> **CogniPrint is an open research instrument for measuring statistical traces in text and testing what evidence survives across human-and-AI transformation chains.**

Core promise:

> **Measure the trace. Keep the uncertainty.**

Supporting principle:

> Every conclusion should map to evidence. Every uncertainty should remain visible.

## 2. Visual direction

Aesthetic: **scientific instrument × editorial research journal × restrained data terminal**.

Avoid:

- generic SaaS gradient/neon hero sections;
- glowing AI-brain imagery;
- fake scientific dashboards;
- oversized “accuracy” percentages;
- cyberpunk styling;
- testimonial walls before evidence;
- sponsor/payment CTA above scientific status.

### Design tokens

Suggested light-first palette:

- Paper background: `#F5F2EA`
- Elevated paper: `#FCFAF5`
- Primary ink: `#111318`
- Secondary ink: `#4D525C`
- Rule/border: `#D8D3C8`
- Cobalt accent: `#2457FF`
- Cobalt quiet background: `#E8EEFF`
- Evidence warning/hold: `#A55A00`
- Failure/negative result: `#A32A2A`
- PASS/verified: `#157347`

Dark mode, if retained, should be secondary rather than the brand default. Use near-black graphite rather than pure black.

### Typography

Use three typographic roles, not decorative font overload:

1. Editorial serif for research titles/large statements — e.g. Source Serif / compatible open font.
2. Geometric/humanist sans for body and navigation — e.g. Inter / compatible system stack.
3. Monospace for hashes, versions, coordinates, evidence labels and commands — e.g. IBM Plex Mono / system mono.

Do not ship unlicensed or privately embedded font binaries.

## 3. Information architecture

Recommended top navigation:

- Lab
- Evidence
- Research
- Software
- Challenges
- About

Utility actions:

- GitHub
- Cite
- Support

`Support` must not visually outrank `Evidence` or `Research`.

## 4. Homepage structure

### Section 1 — Hero

Eyebrow:

`COGNIPRINT RESEARCH INITIATIVE`

Headline:

> **Measure the trace. Keep the uncertainty.**

Body:

> Open-source research infrastructure for reproducible statistical text profiles and evidence across human/model transformation chains.

Primary actions:

- `Try the Lab`
- `Read the Research`
- `Inspect the Evidence`

Secondary meta row:

`v0.1.2` · `MIT` · `descriptive_only` · `ORCID 0009-0009-6337-1806`

Do not show `external review 0/1` as a vanity badge. Show it as a transparent research-state label in the Evidence strip below.

### Section 2 — Live instrument

Purpose: explain the invention visually in less than 20 seconds.

Desktop layout:

Left: editable sample text or fixed public demonstration sample.

Center: transformation pipeline:

`Text T → φ(T) ∈ R¹² → comparison / perturbation → evidence state`

Right: profile visualization and evidence card.

Required visual output:

- 12D profile displayed as a clean coordinate matrix or compact radial plot;
- current extractor/version label;
- comparison distance when a reference/sample pair exists;
- perturbation delta when demonstration mode is enabled;
- visible evidence-state chip.

Do not use a single “AI probability” gauge.

### Section 3 — Four evidence classes

Four equal cards:

#### OBSERVED
Direct measurements from the text or artifact.

Examples: profile coordinates, hashes, measured distances, perturbation deltas.

#### INFERRED
A conclusion conditional on a stated reference set/model/calibration procedure.

Examples: relative similarity or candidate ranking.

#### ATTESTED
External authenticated provenance.

Examples: signatures, content credentials, trusted execution logs, repository/publication records.

#### UNKNOWN
The evidence does not justify a stronger statement.

This card must be visually equal to the others — uncertainty is a product feature, not an error state.

### Section 4 — Evidence strip

Compact, horizontally scannable system status:

- Software release: `v0.1.2`
- Scientific readiness: `descriptive_only`
- License: `MIT`
- Public code: `GitHub`
- Methodological external review: `0/1 — pending`
- DOI: `public verification pending` until independently verified
- Challenge 001: `protocol prepared / preregistration pending`

Every status item must link to evidence or an explanatory page.

### Section 5 — What CogniPrint can and cannot say

Two-column editorial block.

#### Can currently support

- reproducible statistical profile construction;
- documented profile comparison;
- controlled perturbation analysis;
- corpus-level descriptive diagnostics;
- versioned evidence artifacts;
- explicit uncertainty/non-claim reporting.

#### Does not currently establish

- author identity;
- unique source model;
- definitive AI origin;
- generation-lineage reconstruction;
- intent/responsibility;
- legal or forensic provenance;
- high-stakes automated decisions.

This section should be above sponsor/revenue material.

### Section 6 — Research outputs

Editorial cards, each with exact state:

1. **CogniPrint software** — open source / JOSS preparation.
2. **Cognitive Fingerprints** — mathematical manuscript / current manuscript state.
3. **Attribution Challenge 001** — blind research protocol / preregistration pending.
4. **Evidence Dossier** — current evidence and non-claim record.
5. **Failure Charter** — where the method is expected to fail.

Each card should show:

- status;
- version/date;
- primary link;
- citation/export action if available.

### Section 7 — Failure is part of the system

Headline:

> **A useful evidence system must know where it fails.**

Show stress tracks such as:

- short text;
- domain shift;
- length/n-gram confounding;
- paraphrase;
- translation;
- human editing;
- unseen models;
- model drift;
- calibration failure;
- provenance conflict.

Link to the failure charter.

### Section 8 — Reproduce

Provide copyable minimal commands from README/CONTRIBUTING.

Display exact version/SHA context. Do not imply a command reproduces results if additional public-data dependencies are required; distinguish smoke and real-data paths.

### Section 9 — Support the research

Only after evidence/research sections.

Headline:

> **Support open evidence infrastructure.**

Body:

> Funding supports maintenance, reproducibility, documentation, open benchmarking and research infrastructure — not a predetermined scientific outcome.

Primary future CTA: GitHub Sponsors after profile approval.

Secondary CTA: institutional/research support contact after legal/payment setup.

Required visible link: Sponsor independence policy.

## 5. Dedicated `/evidence` page

This should become the credibility center of the project.

Required modules:

1. **Current state** — release, SHA, scientific readiness.
2. **Evidence map** — claim → evidence → artifact → version.
3. **Diagnostics** — public-data runs with corpus, configuration, result and limitation.
4. **Negative results** — first-class section, not buried in changelog.
5. **External review** — `0/1` until substantive review; later link reviewer record if permission/public record exists.
6. **Publication state** — manuscript/preprint/submitted/accepted/published must be mutually distinguishable.
7. **DOI/archive** — only show VERIFIED when direct resolution matches intended record.
8. **Reproduce** — exact commands.

## 6. Dedicated `/research` page

Use editorial publication layout.

Sections:

- Research question;
- formal framework;
- current empirical layer;
- open problems;
- manuscripts/software papers;
- preregistrations;
- reviewer entry points;
- citations.

Avoid a marketing timeline that implies future hypotheses are capabilities.

## 7. Dedicated `/lab` page

Purpose: interactive demonstration of currently validated descriptive capabilities.

Allowed interactions:

- paste/type text;
- compute profile;
- compare two samples;
- run bounded perturbation demonstration;
- export a local evidence summary;
- show extractor/version/configuration;
- explain each coordinate;
- show `UNKNOWN` where interpretation is unsupported.

Disallowed UI until separately validated:

- “Who wrote this?”
- “Which model generated this?”
- “AI: 87%”
- “Forensic verdict”
- identity accusation/candidate labeling.

## 8. Component system

### `ResearchStateBadge`

Props conceptually:

- label;
- state: `PASS | HOLD | PENDING | UNKNOWN`;
- evidence URL;
- last verified date.

### `EvidenceClaimCard`

Fields:

- claim;
- evidence class;
- artifact;
- source/version;
- confidence/calibration only if scientifically defined;
- non-claims;
- reproduce link.

### `FingerprintProfile`

Must support:

- named coordinates;
- raw and normalized values where appropriate;
- extractor version;
- accessible tabular fallback;
- export without suggesting identity.

### `PublicationCard`

Explicit state enum:

`MANUSCRIPT | PREPRINT | SUBMITTED | ACCEPTED | PEER_REVIEWED_PUBLISHED`

Never derive status from presence of a PDF alone.

### `FailureTrack`

Show tested/not tested/failed/unknown independently.

## 9. Motion and interaction

Keep motion analytical:

- 150–220 ms transitions;
- profile points morph only when values actually change;
- transformation chain can animate step-by-step;
- no ambient floating particles;
- respect `prefers-reduced-motion`;
- data transitions must never imply measurement precision that does not exist.

## 10. Charts and data-viz rules

- axes/units visible;
- captions include corpus/configuration/version;
- avoid 3D charts;
- no truncated axes unless explicitly justified;
- uncertainty/dispersion shown where available;
- color cannot be the only state cue;
- SVG preferred for reproducible scientific figures;
- all figures need accessible textual/tabular equivalents.

## 11. Mobile behavior

Mobile hierarchy:

1. hero;
2. status strip;
3. simplified live profile demo;
4. evidence classes;
5. can/cannot claims;
6. research outputs;
7. support.

The 12D visualization must collapse to a scrollable coordinate list/table rather than becoming unreadable.

## 12. Accessibility acceptance criteria

- WCAG AA contrast minimum;
- keyboard-operable lab controls;
- visible focus states;
- semantic headings;
- no information encoded by color alone;
- charts have text/table equivalents;
- reduced-motion mode;
- 200% zoom without loss of functionality;
- meaningful link labels instead of repeated “Learn more.”

## 13. SEO / scholarly metadata

Required:

- canonical URLs;
- OpenGraph/title descriptions that say “research framework,” not “AI detector”;
- ORCID link;
- `CITATION.cff` link;
- software version;
- publication metadata where verified;
- structured scholarly metadata only for actually published/preprinted works;
- sitemap for Research/Evidence/Software/Challenge pages.

## 14. Trust and monetization rules

1. Sponsor CTA below evidence.
2. No sponsor logo inside scientific result cards.
3. No sponsor-selected threshold or benchmark.
4. No paid unlocking of decisive scientific evidence.
5. Sponsor independence policy always one click away.
6. Corrections/negative results remain public regardless of funding.

## 15. Implementation phases

### Phase A — information architecture preview

- implement routes/components in preview only;
- no scientific text changes except approved copy mapping;
- preserve all existing public evidence links;
- run visual/accessibility QA.

### Phase B — live instrument preview

- bind only current descriptive computations;
- add coordinate explanations;
- add evidence classes and export;
- prohibit unsupported classifier language.

### Phase C — publication/sponsor surfaces

- add JOSS preparation card only as `PREPARATION`, never `SUBMITTED`;
- add GitHub Sponsors CTA only after profile approval;
- add DOI only after direct verification.

### Phase D — production cutover

Requires separate owner approval after preview comparison and regression testing.

## 16. QA gates before production

- [ ] root route visual regression PASS;
- [ ] all existing evidence/research links preserved or redirected;
- [ ] no unsupported scientific claim introduced;
- [ ] `descriptive_only` visible;
- [ ] external review remains correct;
- [ ] DOI state correct;
- [ ] mobile 360/390/430 px PASS;
- [ ] tablet/desktop PASS;
- [ ] keyboard/accessibility smoke PASS;
- [ ] no console/runtime errors;
- [ ] performance budget defined and checked;
- [ ] no third-party sponsor/tracking script added without approval;
- [ ] production domain/DNS untouched until explicit approval.

## 17. North-star screenshot test

A first-time researcher should understand from one screenshot that:

1. CogniPrint measures text profiles rather than issuing magical identity verdicts;
2. the project exposes evidence and uncertainty;
3. current status is research-grade but `descriptive_only`;
4. code/reproduction/papers are public;
5. sponsorship supports the work but does not validate it.

If the screenshot instead looks like an AI-detection SaaS landing page, the redesign has failed.
