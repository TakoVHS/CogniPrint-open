# Full Proposal Draft — OTF ICRP 2026

> Applicant-readiness draft only. Not submitted to OTF.

## Project title

**Evidence After the Filter: Privacy-Preserving Measurement of AI-Mediated Information Controls in Vietnamese and Russian-Language Workflows**

## Applicant

Roman Adriashkin — Independent Researcher-Engineer & Founder, CogniPrint Research Initiative

## Duration

12 months, full-time.

## Executive summary

AI-assisted translation, summarization, rewriting, paraphrase, and moderation are increasingly inserted between a source document and the version that a reader, researcher, journalist, or civil-society worker actually receives. These transformations can be useful, but in sensitive information environments they can also remove, soften, compress, refuse, reframe, or otherwise alter politically or socially sensitive material. The result can be difficult to audit because the original text may be sensitive, the transformation may be performed by a remote service, and later reviewers may see only the final output.

This project will conduct a controlled, multilingual study of these effects in Vietnamese, Russian, and English workflows and will build a local-first evidence layer for recording what was observed without turning statistical similarity into an accusation or identity claim. The research will measure transformation outcomes including refusal, omission, sanitization, semantic drift, lexical substitution, compression, uncertainty inflation, and loss of provenance context. It will compare simple transparent baselines with more complex measurements, document negative results, and preserve explicit `UNKNOWN / INSUFFICIENT EVIDENCE` outcomes when the data do not support a conclusion.

The practical outputs will be an open benchmark, reproducible measurement scripts, a transformation-taxonomy and annotation protocol, a privacy-preserving Evidence Capsule schema/toolkit, aggregate analysis artifacts, a technical report, a failure/limitations report, and practitioner guidance for internet-freedom researchers and investigators who need to evaluate information after it has passed through AI-mediated workflows.

The project will not attempt to identify authors, infer legal responsibility, prove exact model identity from text similarity, or claim universal AI-origin detection. Existing CogniPrint assets will be used as research infrastructure where appropriate, while all funded outputs will be separately scoped and tracked.

## Problem statement

Information controls are no longer limited to blocking access to a website or removing a post. Sensitive information may now pass through AI-enabled layers that translate, summarize, rewrite, moderate, classify, or assist an operator before the material reaches its intended audience. A transformation can therefore affect meaning even when the underlying source remains technically accessible.

This creates three problems for internet-freedom research.

First, the effect can be subtle. A system may preserve the broad topic while removing a named actor, weakening a claim, changing certainty, compressing a sequence of events, refusing to reproduce a sensitive phrase, or replacing politically specific language with generic wording. A binary “blocked/not blocked” measure does not capture these changes.

Second, the evidence is difficult to preserve safely. Raw source texts can contain sensitive political, personal, or operational information. Publishing the raw material merely to make an analysis reproducible may create additional risk. Conversely, publishing only a score makes independent review difficult.

Third, analysis can itself become overconfident. A statistical difference between two texts does not establish who caused the change, which exact model produced it, whether the change was intentional, or who bears responsibility. A useful research method therefore has to distinguish direct observation from inference and allow uncertainty to remain unresolved.

The proposed project addresses these problems by combining controlled multilingual transformations, transparent comparative measurements, structured evidence records, and explicit claim boundaries.

## Research questions

1. **Transformation effects:** What measurable content changes occur when sensitive Vietnamese, Russian, and English material passes through translation, summarization, rewriting/paraphrase, and moderation/refusal workflows?
2. **Cross-language consistency:** Which effects are stable across languages, and which appear language- or workflow-specific?
3. **Severity and visibility:** Which changes are visible to simple lexical or length baselines, and which require semantic or structured comparison?
4. **Repeated transformation:** How do effects accumulate when text passes through more than one transformation step?
5. **Evidence sufficiency:** What information can be preserved in a privacy-aware evidence record so another reviewer can verify a transformation claim without requiring public release of sensitive source content?
6. **Failure boundaries:** Under what conditions should the system abstain and return `UNKNOWN / INSUFFICIENT EVIDENCE` rather than label a transformation?
7. **Practitioner utility:** Which outputs are actually useful to internet-freedom researchers, digital-rights practitioners, or investigators reviewing altered multilingual material?

## Research design

### 1. Controlled multilingual corpus

The project will construct a documented corpus of matched Vietnamese, Russian, and English material representing sensitive information-control contexts. Source selection will prioritize material that can be handled ethically and legally, with synthetic or safely reusable examples used when publishing raw text would create unnecessary risk.

The working target is at least **300 source passages**, balanced as closely as practical across the three languages and across several sensitivity/topic categories. The final sampling frame will be frozen with the host adviser before the main analysis.

Public releases will not assume that every raw source can be shared. Public benchmark records may instead include hashes, bounded metadata, safe excerpts or synthetic equivalents, transformation labels, and independently reproducible scripts where appropriate.

### 2. Transformation matrix

Each source item will be exercised through a documented set of workflow classes:

- translation;
- summarization;
- rewriting/paraphrase;
- moderation/refusal or safety-mediated response;
- selected multi-step combinations such as translate → summarize or rewrite → summarize.

Where external model services are included, provider/model names will be recorded only as technical experimental metadata. Their inclusion will not imply partnership, sponsorship, employment, or endorsement.

The design will avoid making the project dependent on a single commercial API. Reproducible local/open implementations will be used where they support the research question, and optional third-party services will be isolated as documented experimental conditions.

### 3. Transformation taxonomy

Outputs will be coded for a bounded set of observable transformation phenomena, including:

- full or partial refusal;
- omission of entities, events, or claims;
- sanitization or euphemistic replacement;
- semantic drift;
- lexical substitution;
- compression or loss of detail;
- uncertainty inflation or deflation;
- change in attribution wording;
- change in temporal or causal structure;
- loss of provenance/context qualifiers;
- unsupported addition;
- no material change.

The codebook will distinguish directly observed differences from interpretive judgments. Ambiguous cases will remain explicitly uncertain rather than being forced into a category.

### 4. Measurement and baselines

The analysis will compare transparent baselines before relying on more complex measurements. Baselines will include, where applicable:

- length and compression ratios;
- token/lexical overlap;
- n-gram similarity;
- entity/number preservation;
- sentence and structural changes;
- embedding-based semantic similarity as a comparative measurement rather than proof of meaning preservation.

Existing CogniPrint text-profile measurements may be included as one descriptive research instrument, but the project will not presuppose that they outperform simple baselines. Negative results will be reported.

### 5. Privacy-preserving Evidence Capsules

For each transformation event, the project will develop a structured Evidence Capsule that can record:

- source/output hashes;
- bounded language and workflow metadata;
- software/configuration identity where available;
- transformation type;
- timestamps or experiment-run identifiers;
- directly observed metrics;
- annotation labels with uncertainty;
- lineage between multi-step transformations;
- reproducibility references;
- explicit limitation/status codes.

Evidence Capsules are intended to make a narrow claim reviewable. They are not a substitute for authenticated provenance and do not establish actor identity or legal responsibility.

### 6. Repeated-transformation and stress analysis

The project will test how evidence changes under repeated transformations, including selected translation and paraphrase chains. This phase will identify which measurements remain stable, which collapse, and when an evidence record should fail closed.

### 7. Practitioner review

The project will seek structured feedback from the host organization and, where safe and feasible, a small number of internet-freedom or digital-rights practitioners. Feedback will focus on usability of the taxonomy, evidence record, interpretation guidance, and failure reporting rather than on obtaining endorsement of scientific claims.

## Beneficiaries and internet-freedom relevance

Primary beneficiaries are researchers and practitioners who need to understand whether sensitive information changed after passing through AI-assisted processing, especially when they cannot safely publish or centralize the original material. Potential use cases include:

- researchers comparing information available across languages;
- civil-society analysts documenting content alteration;
- journalists or investigators checking summaries and translations of sensitive material;
- digital-rights teams building evidence-preservation workflows;
- developers of internet-freedom tools who need structured transformation and uncertainty records.

The project is designed as reusable infrastructure and methodology, not only as a paper. Public schemas, scripts, safe benchmark artifacts, failure reports, and practitioner guidance will allow other teams to reproduce or adapt the work.

## Outputs

By project completion, the intended public or shareable outputs are:

1. **Multilingual AI-mediated transformation benchmark** with documented sampling, safe-release policy, and machine-readable records.
2. **Transformation taxonomy and annotation codebook** covering refusal, omission, sanitization, semantic drift, lexical substitution, compression, uncertainty and provenance-context loss.
3. **Reproducible measurement harness** implementing transparent baselines and selected descriptive measurements.
4. **Evidence Capsule schema/toolkit** for local-first, privacy-aware transformation records.
5. **Aggregate analysis dataset/explorer artifacts** that do not require public disclosure of sensitive source text.
6. **Technical research report** describing methods, observed patterns, limitations and negative results.
7. **Failure and uncertainty report** documenting where the approach cannot support a conclusion.
8. **Practitioner guidance** for interpreting AI-mediated transformations without overclaiming provenance or attribution.
9. **Reproducibility package** containing versioned configuration, manifests, test fixtures, hashes and execution instructions.

## Monitoring, evaluation and learning

Completion will be evaluated against objective deliverables rather than a requirement to produce a positive scientific result. Key measures include:

- sampling frame and protocol frozen before scaled analysis;
- at least 300 documented source passages unless the host-approved safety review requires a lower safe number;
- transformation coverage across all four principal workflow classes and selected multi-step chains;
- 100% of released experiment records linked to a versioned configuration/run identity;
- baseline comparison completed before any stronger interpretation;
- uncertainty and limitation codes present for ambiguous or unsupported cases;
- a reproducibility run performed from a clean environment on the public/safe-release subset;
- practitioner/host feedback recorded and changes traced;
- a public negative-result/failure section regardless of headline performance;
- final outputs mapped to the month-by-month workplan.

The detailed MEL plan is maintained in `monitoring-evaluation-learning.md`.

## Ethics, privacy and security

The project uses data minimization as a design requirement. Raw sensitive material will not be placed in the public repository merely for convenience. Public records will prefer synthetic, licensed, already-public and safely reusable content, or hashes and bounded metadata where raw publication is unnecessary.

The project will not covertly collect private communications, identify vulnerable individuals, or build a system for punitive attribution. If practitioner feedback involves non-public operational material, participation and handling rules will be agreed with the host before collection.

Dual-use risk is addressed by keeping the tool focused on transparent comparison and evidence preservation, not surveillance or identity inference. High-impact claims require authenticated external evidence; statistical similarity alone remains insufficient.

The detailed risk register is maintained in `risk-ethics-security.md`.

## Existing work versus proposed funded work

CogniPrint already contains open-source evidence schemas, deterministic integrity records, descriptive text measurements, reproducibility tooling, baseline/evaluation infrastructure, and claim-safety controls. These existing assets demonstrate execution capacity but are **not** presented as future work to be funded again.

The proposed ICRP work is the new multilingual research campaign: corpus/protocol finalization, controlled AI-mediated transformation experiments, the specific multilingual transformation benchmark, validated transformation taxonomy, scaled analysis, ICRP-specific Evidence Capsule tooling, practitioner validation, and final research/practitioner outputs.

See `prior-vs-funded-work.md` for the formal boundary.

## Host organization

The applicant did not require a confirmed host at Stage 1. For Stage 2, the preferred host should provide:

- substantive expertise in internet freedom, censorship, digital rights, or related measurement research;
- a named adviser able to review the research monthly;
- methodological challenge rather than nominal sponsorship;
- an ethical/data-safety review channel;
- practitioner or research-community context relevant to the outputs;
- support for remote full-time collaboration if the researcher remains based in Viet Nam;
- the ability to provide the monthly progress oversight expected by OTF.

No candidate organization listed in `host-organization-shortlist.md` is represented as having agreed to host the project.

## Dissemination and sustainability

The project will release reusable outputs throughout the research period rather than wait for a single final publication. The dissemination plan includes versioned repository releases, concise technical notes, practitioner-oriented guidance, safe benchmark artifacts, reproducibility instructions, and final methodology/failure reports.

Post-project sustainability is based on open formats and low operational dependency: schemas, manifests, baselines and local-first tools should remain usable without requiring a proprietary hosted service. Any optional model-provider experiments will be separable from the core evidence format.

## Applicant capacity

Roman Adriashkin is the founder and lead researcher-engineer of the open-source CogniPrint Research Initiative. Existing public work demonstrates implementation of reproducibility tooling, evidence schemas, explicit uncertainty states, benchmark infrastructure, deterministic integrity records, and public scientific limitations. The project intentionally preserves a `descriptive_only` scientific boundary while stronger empirical questions remain open.

The host organization is expected to complement this engineering capacity with independent methodological oversight, internet-freedom context, and practitioner connection.

## Requested support

Core stipend:

- USD 7,000/month × 12 months = **USD 84,000**.

Conservative optional direct-cost envelope preserved from the prepared application materials:

- equipment: up to **USD 3,000**;
- travel: up to **USD 3,500**;
- working maximum: **USD 90,500**, subject to OTF approval and actual research need.

No overhead, profit, unrelated business expense, or unverified staffing cost is requested in this readiness draft.

## Success and failure criteria

The project succeeds if it produces a reproducible, practically useful account of how AI-mediated workflows alter sensitive multilingual information and a safer way to preserve the evidence needed to review those alterations.

A finding that many effects are inconsistent, dominated by simple baselines, highly context-specific, or not reliably measurable is still a valid research outcome if documented rigorously.

The project fails scientifically if it hides negative results, forces uncertain cases into confident labels, conflates text similarity with actor/model identity, or publishes sensitive source material without a justified need.

## Claim boundary

This proposal does not claim that CogniPrint currently establishes authorship, intent, exact model identity, legal/forensic provenance, actor responsibility, or universal AI-origin detection. Current project scientific readiness remains `descriptive_only`.
