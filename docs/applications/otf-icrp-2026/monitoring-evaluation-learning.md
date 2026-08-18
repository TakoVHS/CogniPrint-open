# OTF ICRP 2026 — Monitoring, Evaluation and Learning Plan

## Purpose

This plan translates application `#22901` into measurable research and delivery criteria suitable for OTF's monthly oversight model. It evaluates whether agreed work was completed rigorously and usefully; it does **not** require the research hypothesis to be confirmed.

## Objectives and indicators

### Objective 1 — Build a controlled multilingual measurement protocol

**Indicators**

- research questions and primary outcome taxonomy frozen before scaled analysis;
- documented Vietnamese/Russian/English sampling frame;
- source handling and publication status recorded for every included item;
- target of at least 300 source passages unless a host-approved safety/methodology decision requires a lower number;
- all four primary workflow classes represented: translation, summarization, rewriting/paraphrase, moderation/refusal.

**Evidence**

- versioned protocol;
- corpus manifest;
- sampling audit;
- source-handling register;
- run-manifest hashes.

### Objective 2 — Measure AI-mediated transformation effects without over-attribution

**Indicators**

- baseline measurements executed before stronger interpretation;
- transformation taxonomy covers refusal, omission, sanitization, semantic drift, lexical substitution, compression, uncertainty change, context/provenance loss, unsupported addition and no-material-change;
- ambiguous cases retain UNKNOWN/insufficient-evidence status;
- language/workflow comparisons report missingness and limitations;
- negative/null results are retained in the final report.

**Evidence**

- baseline result files;
- annotation/codebook revisions;
- analysis notebooks/scripts or deterministic CLI outputs;
- limitations register;
- results/failure report.

### Objective 3 — Produce privacy-aware, independently reviewable evidence records

**Indicators**

- accepted transformation records include required run/configuration identity;
- Evidence Capsule schema distinguishes observation, inference/annotation and uncertainty;
- public reproducibility does not require publication of sensitive raw text;
- integrity/tamper checks fail closed when required evidence is missing or inconsistent;
- a clean-environment reproducibility test is completed on the safe-release subset.

**Evidence**

- schema versions;
- exported capsule fixtures;
- integrity test results;
- clean-run logs;
- checksums and release manifest.

### Objective 4 — Deliver practitioner value to the internet-freedom community

**Indicators**

- at least one structured host review of the taxonomy/evidence format before midpoint and one before final release;
- practitioner feedback sought where safe and host-approved;
- practitioner guidance explains what can and cannot be concluded;
- release artifacts are documented for reuse, not only academic publication;
- feedback-driven changes are traceable.

**Evidence**

- feedback memos;
- decision/change log;
- practitioner guidance;
- release documentation;
- final dissemination manifest.

## Monthly reporting template

Each monthly report should answer:

1. What was planned?
2. What was completed?
3. What deliverable proves completion?
4. What changed from the plan and why?
5. What risks or blockers remain?
6. What did the research learn, including negative results?
7. What is planned next month?
8. What host feedback or traffic-light status was received?

## Traffic-light interpretation

### Green

- agreed monthly deliverables exist and are reviewable;
- deviations, if any, do not threaten the research plan;
- safety/claim boundaries remain intact.

### Yellow

- partial completion or a material methodological, technical, access or safety issue exists;
- payment/release is governed by OTF/host judgment;
- a named remediation plan and target date are recorded.

### Red

- work cannot proceed safely or credibly;
- required access/host oversight is unavailable;
- a major integrity or ethics issue invalidates the planned work;
- OTF/host intervention is required before affected activities continue.

## Quality gates

### Protocol gate

Scaled analysis cannot begin until protocol, sampling, safety and taxonomy rules are versioned and reviewed.

### Baseline gate

No complex measurement is framed as useful unless transparent baselines are reported alongside it.

### Evidence gate

A result cannot enter the accepted analysis dataset without required run identity and evidence metadata.

### Claim gate

No result may be presented as authorship, intent, exact model identity, legal/forensic provenance or actor responsibility based on text similarity alone.

### Reproducibility gate

The safe-release subset must be rebuildable or re-checkable from documented code/configuration and fixed manifests.

### Release gate

Sensitive raw material is not published merely to satisfy reproducibility. A withheld/redacted/synthetic alternative is acceptable when the decision is documented.

## Learning agenda

The project will explicitly capture lessons in five areas:

1. which transformation effects survive simple baselines;
2. where multilingual comparisons break or become ambiguous;
3. when repeated transformation destroys useful evidence;
4. which metadata materially improves independent review without exposing raw content;
5. which outputs practitioners find understandable and useful.

Learning can justify changing implementation details, but material changes to research questions, sampling or promised deliverables require documented host/OTF review.

## Final success test

The project is successful if another qualified reviewer can determine:

- what was tested;
- which data were included/excluded and why;
- what changed under the tested workflows;
- which findings are direct observations versus interpretation;
- where uncertainty remains;
- how the safe public artifacts can be reproduced or checked;
- how the outputs can be reused by internet-freedom practitioners.

A negative scientific result can satisfy all of these conditions and therefore count as successful research delivery.
