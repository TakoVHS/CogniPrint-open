# OTF ICRP 2026 — 12-Month Workplan

> Draft for application `#22901`. Months are relative to contract start. Exact calendar dates remain pending OTF invitation, host agreement and contract.

## Workplan principles

- Full-time research effort.
- Every month ends with a reviewable deliverable or evidence package.
- Monthly completion is based on work performed and documented, not on obtaining a positive scientific finding.
- Host review and OTF reporting are built into every month.
- Existing CogniPrint assets are inputs, not rebilled future deliverables.
- Scientific status remains `descriptive_only` unless separate empirical and review gates justify a change.

## Month 1 — Protocol, host onboarding and safety freeze

### Activities

- Confirm host adviser, supervision cadence and remote-working protocol.
- Freeze research questions, transformation classes and primary outcome taxonomy.
- Finalize data-management, privacy, threat-model and publication rules.
- Define the source-sampling frame across Vietnamese, Russian and English.
- Freeze experiment/run manifest format and Evidence Capsule minimum fields.
- Register all pre-existing CogniPrint assets used as inputs so they cannot later be misreported as funded outputs.

### Deliverables

- Research protocol v1.
- Data and safety management plan v1.
- Transformation taxonomy/codebook v0.1.
- Prior-work registry and funded-work boundary.
- Month-1 host review package.

### Completion evidence

- Versioned documents and hashes.
- Host review notes and traffic-light input.
- No scaled transformation run begins before the protocol/safety freeze.

## Month 2 — Corpus construction and transformation harness

### Activities

- Assemble the documented multilingual source corpus.
- Balance or document imbalances across language and topic/sensitivity classes.
- Build transformation harness for translation, summarization, rewriting/paraphrase and moderation/refusal workflows.
- Add deterministic run identifiers, configuration capture and safe logging.
- Create synthetic/public fixtures for reproducibility tests.

### Deliverables

- Corpus manifest v0.1.
- Transformation harness v0.1.
- Safe public fixture set.
- Sampling audit and exclusions log.

### Completion evidence

- Every included source has documented provenance/handling status.
- No private/sensitive raw content is committed publicly by default.
- Harness can recreate a test transformation run from a clean environment.

## Month 3 — Pilot study and codebook calibration

### Activities

- Run a bounded pilot across all primary workflow classes.
- Measure length, lexical, n-gram, entity/number and semantic-change baselines.
- Test annotation categories for refusal, omission, sanitization, semantic drift, compression, uncertainty and context loss.
- Record ambiguous cases and revise codebook rather than forcing labels.

### Deliverables

- Pilot results package.
- Baseline comparison v0.1.
- Transformation taxonomy/codebook v0.2.
- Pilot failure log.

### Completion evidence

- All primary workflow classes represented in the pilot.
- Baselines executed before any stronger interpretation.
- Ambiguity/UNKNOWN cases preserved.

## Month 4 — Benchmark freeze and annotation-quality audit

### Activities

- Freeze benchmark inclusion/exclusion rules.
- Expand to the planned main corpus, targeting at least 300 source passages unless host-approved safety constraints require a lower safe number.
- Conduct structured annotation-quality review on a stratified sample.
- Document disagreement rather than hiding it.
- Finalize public/private artifact separation.

### Deliverables

- Benchmark protocol v1.
- Corpus manifest v1.
- Annotation-quality report.
- Safe-release policy v1.

### Completion evidence

- Benchmark sampling and exclusion rules are frozen before scaled analysis.
- Any deviation from the 300-source target is documented and host-approved for safety/methodological reasons.

## Month 5 — Scaled transformation collection

### Activities

- Execute scaled single-step transformations under frozen run/configuration rules.
- Capture Evidence Capsule records for each completed transformation.
- Monitor failures, rate/service changes and missing metadata.
- Keep provider/tool-specific observations bounded to the tested conditions.

### Deliverables

- Main transformation dataset tranche A.
- Evidence Capsule schema/toolkit v0.1.
- Run-integrity and missingness report.

### Completion evidence

- 100% of accepted experiment records have run identity and required evidence metadata.
- Failed/partial runs are recorded separately from accepted runs.

## Month 6 — Midpoint analysis and reproducibility release

### Activities

- Analyze first-half results by language, workflow and transformation phenomenon.
- Compare simple baselines with selected CogniPrint descriptive measurements.
- Conduct a clean-environment reproducibility run on the safe-release subset.
- Obtain structured host/practitioner feedback on taxonomy and evidence format.

### Deliverables

- Midpoint technical report.
- Reproducibility package v0.1.
- Baseline-vs-profile comparison.
- Practitioner/host feedback memo.

### Completion evidence

- Negative and null findings included.
- Public/safe subset is reproducible from documented instructions.
- Feedback items are traceable to accepted/rejected changes.

## Month 7 — Multi-step transformation stress study

### Activities

- Execute selected chains such as translate → summarize and rewrite → summarize.
- Measure cumulative omission, compression, semantic drift and context loss.
- Test when Evidence Capsule lineage is sufficient and when it must return insufficient evidence.

### Deliverables

- Multi-step transformation dataset.
- Lineage analysis report.
- Evidence Capsule toolkit v0.2.

### Completion evidence

- At least two pre-specified multi-step workflow families executed across all three languages where technically feasible.
- Failure/UNKNOWN criteria applied consistently.

## Month 8 — Moderation/refusal and sensitive-content analysis

### Activities

- Focus analysis on refusal, partial refusal, sanitization and safety-mediated response behavior.
- Compare outcomes across language and workflow conditions without inferring hidden intent.
- Separate directly observed response behavior from hypotheses about cause.

### Deliverables

- Moderation/refusal analysis package.
- Cross-language comparison memo.
- Updated limitations register.

### Completion evidence

- Every causal/intent interpretation is either externally supported or explicitly excluded from the finding.
- Language-specific uncertainty is reported.

## Month 9 — Privacy-preserving verification and evidence audit

### Activities

- Evaluate which transformation claims can be independently checked from hashes, bounded metadata, safe fixtures and structured records.
- Test tamper/integrity checks on exported evidence packages.
- Review data-retention and release decisions with host.

### Deliverables

- Evidence verification protocol v1.
- Evidence Capsule toolkit v1 release candidate.
- Privacy and integrity audit report.

### Completion evidence

- Evidence records fail closed on missing/conflicting required fields.
- Public release does not depend on exposing sensitive raw source text.

## Month 10 — Practitioner validation and workflow usability

### Activities

- Conduct structured usability/relevance review with host and, if safe/approved, a small number of internet-freedom/digital-rights practitioners.
- Test whether outputs answer practical questions without encouraging over-attribution.
- Revise practitioner guidance and export format.

### Deliverables

- Practitioner validation memo.
- Evidence Capsule toolkit v1.
- Practitioner guidance draft v0.1.

### Completion evidence

- Feedback source/type and resulting changes documented.
- No practitioner is represented as endorsing scientific validity unless they explicitly provide such an assessment.

## Month 11 — Final analysis, limitations and dissemination preparation

### Activities

- Complete aggregate analysis and sensitivity checks.
- Write technical methods/results report.
- Produce dedicated failure/limitations and negative-results sections.
- Prepare benchmark/tool documentation and release notes.

### Deliverables

- Final technical report draft.
- Failure and limitations report draft.
- Benchmark/tool release candidate.
- Practitioner guidance v0.2.

### Completion evidence

- Main findings map directly to recorded analyses.
- Unsupported attribution/identity claims are absent.
- Reproducibility and limitations sections complete before final release.

## Month 12 — Final release, handoff and sustainability

### Activities

- Incorporate final host/OTF review comments.
- Publish safe open-source artifacts and final reports.
- Archive reproducibility manifests and checksums.
- Document maintenance/sustainability path and unresolved research questions.
- Produce final OTF and host reporting package.

### Deliverables

- Final multilingual benchmark safe release.
- Final reproducibility package.
- Evidence Capsule schema/toolkit final research release.
- Technical report.
- Failure/limitations report.
- Practitioner guidance.
- Sustainability/handoff note.
- Final monthly/project report package.

### Completion evidence

- All promised outputs either released or explicitly documented as withheld/modified for safety with rationale.
- Final deliverable manifest maps each output to its objective, source commit/version and release status.

## Monthly oversight cadence

Every month includes:

1. applicant progress note;
2. deliverable/evidence manifest;
3. risks, deviations and remediation note;
4. host adviser review / traffic-light input;
5. OTF program-manager reporting as required;
6. next-month plan.

A green status means the agreed monthly work is complete and reviewable. A yellow status means progress exists but a named issue requires remediation. A red status means a material interruption requires discussion before continuing the affected work.
