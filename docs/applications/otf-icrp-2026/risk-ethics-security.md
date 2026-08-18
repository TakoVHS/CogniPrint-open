# OTF ICRP 2026 — Risk, Ethics and Security Plan

## Scope

This plan covers the proposed multilingual research on AI-mediated translation, summarization, rewriting/paraphrase and moderation/refusal workflows. It is designed for internet-freedom research where source material, participants or conclusions may be sensitive.

## Core safety principles

1. **Data minimization:** collect and retain only what is needed to answer the research questions.
2. **Local-first handling:** prefer local processing and bounded evidence records when raw content does not need to leave the research environment.
3. **No punitive attribution:** text similarity or transformation measurements are not used to identify or accuse a person, organization or exact model.
4. **Explicit uncertainty:** ambiguous, missing, conflicting or out-of-scope evidence can remain `UNKNOWN / INSUFFICIENT EVIDENCE`.
5. **Safe publication:** reproducibility does not override privacy, consent, legal or operational risk.
6. **Host oversight:** material ethics/security deviations are reviewed with the host adviser before continuing affected work.

## Risk register

### R1 — Sensitive raw source material leaks through public artifacts

**Risk:** source material may contain politically sensitive, personal or operational information.

**Controls:**

- do not commit sensitive raw source text to public version control by default;
- classify each source by handling/publication status;
- use synthetic, already-public, licensed, redacted or safely reusable fixtures for public reproducibility where possible;
- publish hashes/bounded metadata when raw publication is unnecessary;
- perform a release review before every public benchmark/package release.

**Stop condition:** any release package contains material whose publication status is unclear.

### R2 — Research output is misread as proof of authorship, intent or responsibility

**Risk:** readers may overinterpret transformation or similarity measurements.

**Controls:**

- retain `descriptive_only` scientific status;
- separate observed metrics from inferred/annotated findings;
- publish limitation codes and explicit non-claims;
- avoid person-level or organization-level attribution from content statistics;
- require authenticated external evidence for claims about actor identity/responsibility.

**Stop condition:** a planned finding cannot be stated without implying unsupported identity, intent or legal responsibility.

### R3 — Exact-model or provider claims exceed the experimental evidence

**Risk:** a provider/model label in an experiment may be mistaken for a general identification capability.

**Controls:**

- provider/model names are experimental configuration metadata only;
- no universal fingerprint claim;
- compare transparent baselines;
- report version/date/configuration limits;
- unseen/out-of-distribution conditions may return UNKNOWN.

### R4 — At-risk practitioner participation exposes people or organizations

**Risk:** interviews/feedback can reveal identity, workflow, location or sensitive cases.

**Controls:**

- practitioner participation is optional and host-approved;
- collect the minimum information needed for usability/relevance review;
- do not publish participant identity without explicit permission;
- avoid requesting live sensitive case data where synthetic examples can answer the usability question;
- separate research feedback notes from public evidence artifacts.

**Stop condition:** useful participation would require collecting unnecessary identifying or operational information.

### R5 — Third-party AI/API services receive sensitive content

**Risk:** remote providers may log, retain or process prompts under policies outside researcher control.

**Controls:**

- do not send confidential/private practitioner material to third-party APIs;
- use public/synthetic/safely reusable test material for remote-service conditions;
- maintain local/open alternatives so the core research is not dependent on a remote API;
- record provider/model/API version as experiment metadata where available;
- review current service data-handling terms before any sensitive use; absent an adequate basis, do not send sensitive material.

### R6 — Prompt/output content creates unsafe or discriminatory annotation decisions

**Risk:** annotators or automated rules may conflate political sensitivity with harmfulness, legality or truth.

**Controls:**

- taxonomy describes observable transformation behavior rather than judging political legitimacy;
- separate factual comparison from normative interpretation;
- document annotation disagreement;
- allow abstention/uncertain labels;
- review codebook with host expertise.

### R7 — Research creates a censorship or surveillance-enabling capability

**Risk:** a transformation-analysis tool could be repurposed to profile people or optimize censorship.

**Controls:**

- no person identification or ranking;
- no behavioral dossier construction;
- no automated enforcement or punishment interface;
- evidence format emphasizes auditability and uncertainty;
- public documentation states prohibited/unsupported interpretations;
- reconsider release granularity if a specific component creates disproportionate misuse risk.

### R8 — Repeated transformations destroy provenance while producing false confidence

**Risk:** multi-step processing may produce apparently clean text while lineage evidence becomes incomplete.

**Controls:**

- maintain explicit transformation lineage when known;
- mark missing steps instead of reconstructing them as fact;
- fail closed when required lineage is unavailable;
- report cumulative uncertainty rather than a single forced verdict.

### R9 — Service drift or software changes make results irreproducible

**Risk:** external models and APIs change during the 12-month study.

**Controls:**

- capture date/version/configuration metadata where available;
- use frozen local fixtures for regression and reproducibility checks;
- distinguish longitudinal drift from experimental error;
- avoid claiming a timeless provider/model behavior.

### R10 — Scope expansion causes delivery failure

**Risk:** the research could expand into general AI detection, broad OSINT, network censorship measurement or unrelated CogniPrint work.

**Controls:**

- contract scope remains the submitted multilingual AI-mediated information-controls study;
- every activity maps to a monthly milestone;
- unrelated CogniPrint features remain pre-existing or separately funded work;
- material scope changes require OTF/host agreement.

## Data handling classes

### Public-safe

Material already public and appropriate for redistribution, or synthetic fixtures specifically created for open release.

### Research-restricted

Material that may be analyzed but should not be published verbatim. Public outputs use hashes, bounded metadata, derived aggregate measures or safe excerpts where justified.

### Do-not-collect

Private communications, credentials, unnecessary PII, live operational secrets, or other material that the research does not need.

## Security controls

- no credentials, bank details, tax forms or sensitive contracting records in GitHub;
- secrets supplied through environment/secret stores, never source files;
- deterministic manifests/checksums for release artifacts;
- least-privilege access to non-public research data;
- separate public and restricted working directories/data stores;
- incident log for accidental exposure, corruption or integrity failure;
- dependency and release review before public distribution;
- backups for research artifacts, with sensitive-data copies minimized.

## Ethics review checkpoints

Required host review points:

1. Month 1 — sampling, handling and publication rules;
2. Month 4 — benchmark freeze and annotation-quality plan;
3. Month 6 — midpoint release and practitioner-feedback plan;
4. Month 9 — privacy/integrity audit;
5. Month 12 — final public release.

A material risk can trigger an additional review at any time.

## Claim-safety language for outputs

Every major public report should state, in substance:

- findings apply to the tested languages, workflows, systems, dates and configurations;
- observed text changes do not establish intent;
- statistical similarity does not establish authorship or exact model identity;
- missing/conflicting evidence can remain unresolved;
- the project is not a validated legal-forensics or automated enforcement system.

## Incident response

If sensitive information is accidentally exposed or a release is found to be unsafe:

1. stop further distribution of the affected artifact where under project control;
2. preserve an internal incident record without replicating the exposed content unnecessarily;
3. notify the host adviser and OTF program manager as contractually appropriate;
4. rotate affected credentials if any are implicated;
5. remove/replace unsafe public artifacts where technically possible;
6. document the remediation and any methodological impact;
7. resume affected work only after the safety issue is understood.

## Acceptance criterion

The research is not considered Stage-2-ready if reproducibility depends on publishing sensitive raw material, if the planned method requires person-level attribution, or if the proposal cannot explain how at-risk users benefit without increasing their exposure.
