# OTF ICRP 2026 — Proposal Answer Bank

> Pre-draft only. OTF has not invited application `#22901` to Stage 2. Exact ICRP portal questions and character/word limits must be captured after an invitation. This answer bank is organized around OTF's published common proposal and Applied Research guidance so the final portal response can be assembled quickly without changing the submitted research scope.

## 1. Short project description

**Evidence After the Filter** is a 12-month, full-time applied research project examining how AI-assisted translation, summarization, rewriting/paraphrase, and moderation/refusal workflows alter sensitive information across Vietnamese, Russian, and English contexts. The project will measure observable effects such as refusal, omission, sanitization, semantic drift, lexical substitution, compression, uncertainty change, and loss of provenance context, while building privacy-aware evidence records that allow findings to be reviewed without requiring publication of sensitive raw source material. Outputs will include an open safe-release benchmark, reproducible measurement tooling, a transformation taxonomy, Evidence Capsule schema/toolkit, technical and failure reports, and practitioner guidance for internet-freedom researchers and investigators.

## 2. Problem statement

Information controls increasingly occur inside intermediary AI-assisted workflows rather than only at the network or platform-access layer. A sensitive source may remain technically reachable while a translation, summary, rewrite, or safety-mediated response changes what downstream readers receive. These changes can be difficult to document because they may be subtle, multilingual, service-dependent, and embedded in ordinary productivity tools.

Current binary measures such as blocked/not-blocked do not capture omissions, softened wording, uncertainty changes, loss of named entities, compression of causal detail, or repeated-transform effects. At the same time, publishing raw sensitive source material simply to make a result reproducible may create additional risk.

The project therefore addresses two linked gaps: how to measure AI-mediated changes to sensitive information rigorously, and how to preserve enough evidence for independent review without turning statistical similarity into identity/intent claims or unnecessarily exposing source content.

## 3. Main beneficiaries

Primary beneficiaries are internet-freedom researchers, digital-rights practitioners, journalists/investigators, and tool developers who need to understand whether sensitive multilingual information changed after passing through AI-assisted processing.

The outputs are designed to help these users answer bounded questions such as:

- Was material omitted or compressed?
- Did named entities, numbers, causal structure, or uncertainty change?
- Did a workflow refuse or sanitize part of the source?
- Can another reviewer verify the claimed transformation from a structured evidence record?
- Is the available evidence too incomplete to support a conclusion?

The project is not designed for automated punishment, person-level profiling, authorship accusation, or legal responsibility determination.

## 4. Why this approach

The project combines three elements that are usually separated:

1. controlled multilingual experiments across several AI-mediated workflow classes;
2. transparent baseline-first measurement with explicit negative/UNKNOWN outcomes;
3. privacy-aware evidence packaging so findings remain reviewable without requiring unrestricted publication of raw sensitive material.

This approach is chosen because it makes both positive and negative findings useful. If simple baselines explain an observed difference, that result will be reported. If repeated transformations destroy enough context that a conclusion is no longer supportable, the correct output is insufficient evidence rather than a forced label.

## 5. Research methodology

The project will construct a documented corpus of at least 300 Vietnamese, Russian, and English source passages unless host-approved safety or methodological constraints require a lower safe number. Source selection will prioritize synthetic, licensed, already-public, or otherwise safely reusable material for open release, while restricted material can be represented publicly through hashes and bounded metadata where necessary.

Each source will be exercised through documented workflow classes: translation, summarization, rewriting/paraphrase, moderation/refusal, and selected multi-step combinations. Accepted runs will include versioned configuration/run identity.

Outputs will be analyzed using transparent baselines first: length/compression, lexical overlap, n-gram similarity, entity/number preservation, structural changes, and comparative semantic similarity. Existing CogniPrint descriptive measurements may be included only as one research instrument and are not assumed to outperform simple baselines.

A bounded annotation taxonomy will record directly observable phenomena including refusal, omission, sanitization, semantic drift, lexical substitution, compression, uncertainty change, context/provenance loss, unsupported addition, and no-material-change. Ambiguous cases can remain UNKNOWN.

The research will also test selected repeated transformations and the Evidence Capsule format used to preserve hashes, bounded metadata, run identity, measurements, lineage, uncertainty, and limitation status.

## 6. How the work builds on existing research and practice

The project is positioned within the broader internet-freedom measurement tradition: reproducible methods, explicit false-positive/uncertainty handling, public artifacts where safe, and direct practitioner relevance. It differs from ordinary network-censorship measurement by focusing on AI-mediated content transformation above the access layer.

Existing CogniPrint work supplies open-source reproducibility and evidence primitives, but the multilingual ICRP corpus, transformation campaign, taxonomy validation, scaled analysis, practitioner testing, and ICRP-specific benchmark/evidence outputs are new proposed research.

The proposal should cite relevant peer-reviewed and practitioner literature in the final Stage 2 version after OTF feedback and host selection are known; the present readiness draft avoids manufacturing a literature list merely to appear complete.

## 7. Actionable and accessible results

Results will be released in multiple layers rather than only as an academic paper:

- machine-readable safe benchmark artifacts;
- transformation taxonomy/codebook;
- reproducible measurement scripts;
- Evidence Capsule schema/toolkit;
- technical methods/results report;
- dedicated negative-results and limitations report;
- practitioner guidance written for non-specialists;
- examples showing when a finding is supported and when the correct outcome is UNKNOWN;
- versioned release manifests/checksums.

The practitioner guidance will explain how to inspect transformations without interpreting similarity as proof of authorship, intent, exact model identity, or legal responsibility.

## 8. Risks and ethical considerations

Primary risks are exposure of sensitive raw source material, participant/practitioner identification, accidental disclosure through third-party AI services, misuse for punitive attribution, overinterpretation of experimental provider/model metadata, and false confidence after multi-step transformations.

Mitigations include data minimization, local-first handling, strict public/restricted data separation, no confidential practitioner material sent to third-party APIs, synthetic/public fixtures for reproducibility, explicit UNKNOWN states, baseline-first analysis, host review checkpoints, and a no-person-attribution/no-automated-enforcement boundary.

A complete risk register is maintained in `risk-ethics-security.md`.

## 9. Objectives

### Objective 1

Create and freeze a safe, controlled multilingual protocol and sampling frame for measuring AI-mediated information changes.

### Objective 2

Measure and compare transformation effects across Vietnamese, Russian, and English workflow conditions using transparent baselines and explicit uncertainty.

### Objective 3

Develop and validate a privacy-aware Evidence Capsule representation for reviewable transformation evidence and multi-step lineage.

### Objective 4

Translate the findings into reusable open artifacts and practitioner guidance for the internet-freedom community.

## 10. Activities and deliverables

The detailed 12-month activity/deliverable map is in `monthly-workplan.md`.

High-level deliverables:

1. protocol/data-safety plan and transformation taxonomy;
2. multilingual corpus manifest and transformation harness;
3. pilot/baseline and annotation-quality reports;
4. scaled transformation benchmark;
5. Evidence Capsule toolkit iterations;
6. midpoint report and clean-environment reproducibility package;
7. multi-step and moderation/refusal analyses;
8. privacy/integrity audit;
9. practitioner validation and guidance;
10. final benchmark/toolkit, technical report, failure report, and sustainability package.

## 11. Monitoring, evaluation and learning

Monthly progress is evaluated by concrete deliverables, versioned evidence, deviations/risk notes, and host oversight. Scientific success is not defined as confirming a hypothesis; a well-supported negative result is a valid outcome.

Core indicators include protocol freeze before scaled analysis, coverage across all four workflow classes, documented sampling/handling status, baseline comparison, 100% accepted run identity/evidence metadata, a clean-environment reproducibility check on the safe subset, explicit limitation/UNKNOWN handling, recorded host/practitioner feedback, and a final release manifest.

Full plan: `monitoring-evaluation-learning.md`.

## 12. Team and capacity

Roman Adriashkin is the founder and lead researcher-engineer of the open-source CogniPrint Research Initiative. Existing public work demonstrates implementation of reproducibility tooling, evidence schemas, deterministic integrity records, benchmark/evaluation infrastructure, and explicit scientific limitation controls.

The project intentionally seeks a host organization that adds independent information-controls expertise, methodological oversight, ethics/data-safety review, practitioner context, and monthly supervision rather than simply duplicating the applicant's engineering role.

## 13. Host organization answer placeholder

**Status: pending. Do not invent affiliation.**

When a host is confirmed, the final answer should state:

- organization and named adviser;
- why the host's expertise is relevant to this exact research question;
- remote/in-person working arrangement;
- monthly supervision/traffic-light review process;
- ethics/data-safety review mechanism;
- practitioner/research-community access;
- any in-kind resources;
- conflict-of-interest and independence considerations.

Candidate-fit analysis: `host-organization-shortlist.md`.

## 14. Budget narrative

Requested core support is the fixed 12-month ICRP stipend: USD 7,000 per month, totaling USD 84,000.

The conservative optional direct-cost envelope preserved from the prepared application package is up to USD 3,000 equipment and up to USD 3,500 travel, for a working maximum of USD 90,500 subject to need and OTF approval.

Equipment will only be requested if existing hardware is insufficient for secure/reproducible local research handling. Travel will only be requested for a defined host/practitioner/research activity that materially improves the project. No overhead, profit, speculative staff, duplicated prior work, or unrelated SaaS/business expense is included.

Full narrative: `budget-and-contracting.md`.

## 15. Existing work and additionality

CogniPrint already provides open-source evidence/reproducibility primitives. OTF support would not pay to recreate those assets. It would support the new 12-month multilingual research campaign, its controlled experiments, ICRP-specific benchmark/evidence outputs, practitioner validation, and final reports/guidance.

Full boundary: `prior-vs-funded-work.md`.

## 16. Sustainability

The project prioritizes open formats, versioned schemas, reproducible scripts, safe benchmark artifacts, and local-first tooling so the outputs can remain useful without a proprietary hosted service after the contract ends. Optional external model-provider experiments are separable from the core evidence format.

The final month includes handoff/maintenance documentation and an unresolved-research agenda so future work can build on both positive and negative findings.

## 17. Current scientific boundary

`SCIENTIFIC_READINESS=descriptive_only`.

The proposal does not claim current capability to establish authorship, intent, exact model identity, legal/forensic provenance, actor responsibility, or universal AI-origin detection. Future ICRP experiments are proposals, not completed results.
