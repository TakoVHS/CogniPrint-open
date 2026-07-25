# CogniPrint research vision

## One-sentence thesis

**CogniPrint is an open research programme for cognitive provenance: studying what measurable traces survive through human-and-model production chains, where the process changes, and what evidence is sufficient to support — or refuse — a provenance hypothesis.**

Current scientific readiness remains `descriptive_only`.

## The problem

The binary question “Was this written by AI?” is becoming less informative as generative systems are embedded into writing tools, agents, translation, research workflows, media production, software, simulations, and synthetic digital environments.

A real artifact may follow a chain such as:

`human draft → model A → human rewrite → model B → translation → human approval → publishing system`

The scientifically useful question is therefore not simply whether AI appeared somewhere in the process. It is:

> **What production process is consistent with the evidence we have, where did the statistical regime change, and what remains unknown?**

CogniPrint calls this research direction **cognitive provenance**. The term is used here as a research concept, not as a claim that text alone contains complete or authenticated provenance.

## Evidence, not verdicts

CogniPrint should not be built around a single “AI probability” score.

The intended unit of output is an **evidence bundle** containing, where available:

- artifact hash;
- extraction and feature-map version;
- measured feature vector;
- reference-corpus and benchmark revision;
- comparison results and alternative candidates;
- perturbation/robustness diagnostics;
- calibration context;
- uncertainty and abstention state;
- provenance assertions from external records;
- software version and reproducibility command;
- explicit statements of what the evidence cannot establish.

The design principle is:

> **Every conclusion comes with evidence. Every uncertainty remains visible. Every reproducible claim can be independently checked.**

This is a forensic-style evidence discipline, not a claim that the current software is a validated legal-forensics instrument.

## The fingerprint idea

CogniPrint uses the fingerprint metaphor carefully.

A biological fingerprint is not the right mathematical analogy for uniqueness. Neural models do not necessarily leave a single permanent, collision-free signature in every output. Prompts, sampling parameters, fine-tuning, language, domain, post-editing, and model updates can all change observable patterns.

For CogniPrint, a **fingerprint** means a reproducible vector or ensemble of measurable properties that can be compared across controlled datasets.

The central scientific question is:

> **Can generative systems be distinguished by stable multidimensional behavioural signatures that survive some combinations of paraphrasing, editing, translation, and human intervention — and can we identify the conditions under which those signatures fail?**

A negative answer for a model, domain, transformation, or feature family is a useful result.

## Generation lineage

The long-term object of study is not a binary `human / AI` label but a **generation lineage**: a bounded hypothesis about which production regimes may have contributed to an artifact and where transitions may have occurred.

A future lineage result might look conceptually like:

`human-like regime → family-A-consistent regime → transition → substantial human edit → unknown regime`

Such a result must carry:

- observed evidence;
- candidate explanations;
- calibrated confidence where available;
- alternative hypotheses;
- change-point or span locations where supported;
- `UNKNOWN / OUT OF DISTRIBUTION / INSUFFICIENT EVIDENCE` states;
- explicit non-claims.

Generation lineage is a research target. It is not a current validated capability.

## Layer 1 — descriptive fingerprinting

**Status: implemented in the current public release.**

The present CogniPrint core constructs an interpretable statistical profile `φ(T)` for a text sample and supports:

- 12 documented feature coordinates;
- Euclidean and cosine comparison;
- perturbation analysis;
- corpus aggregation;
- entropy measurements;
- word and character n-gram diagnostics;
- corpus-relative exploratory thresholds;
- reproducible tests and evidence artifacts.

This layer answers questions about measurable structure and stability. It does not identify an author or model.

## Layer 2 — model-family attribution

**Status: research target with executable pilot infrastructure.**

The next scientific programme tests whether combinations of interpretable and learned signals contain benchmark-bounded information about known model families.

A credible study should include:

- multiple model families and versions;
- multiple prompt families;
- temperature/sampling variation;
- multiple domains and text lengths;
- multilingual material only after language-specific validation;
- paraphrase and translation attacks;
- human and mixed-production controls;
- model updates over time;
- grouped/leakage-safe evaluation;
- simple baselines before complex classifiers;
- calibration and abstention;
- unseen-model and out-of-distribution tests.

The intended output is not “Model X wrote this with certainty.” It is closer to:

> “Under benchmark B and reference registry R, the artifact is most consistent with family F among the tested classes; alternative candidates are G/H; confidence is C; or the correct output is UNKNOWN.”

## Layer 3 — human–AI intervention mapping

**Status: research target.**

Real documents are increasingly co-produced. The research goal is to evaluate whether a document can be represented as a sequence of regions with different production characteristics, and whether controlled revision histories can reveal transitions between machine generation and substantial human editing.

Possible research outputs include:

- sentence/span-level regime maps;
- change-point detection over fingerprint trajectories;
- human-edit intensity estimates;
- revision-chain comparisons;
- uncertainty-aware mixed-production labels.

The preferred wording is **“statistical regime change detected here”**, not “a human definitely wrote this sentence.”

This area is not solved. CogniPrint should publish failure cases as readily as successes.

## Layer 4 — cross-model lineage reconstruction

**Status: long-term research target.**

A document may be generated by one model and substantially rewritten by another. The research question is whether controlled multi-stage generation chains retain enough information to distinguish:

- one-model generation;
- model-to-model rewriting;
- human-to-model editing;
- model-to-human editing;
- translation or paraphrase transitions;
- unresolved/unknown transitions.

This layer should not be attempted as a production claim until lower-level family attribution and intervention mapping have passed dedicated benchmarks.

## Layer 5 — provenance evidence

**Status: research and integration target; bounded evidence-capsule tooling exists.**

Content analysis alone cannot responsibly answer every provenance question. CogniPrint therefore treats external provenance as a separate evidence class.

Potential inputs include:

- cryptographic hashes;
- signed content credentials;
- document revision history;
- model/tool execution logs;
- prompt and workflow records where lawfully available;
- timestamps;
- software/version identifiers;
- declared human approvals;
- repository or publication records.

CogniPrint should compare two distinct evidence channels:

1. **Observed content evidence** — what the artifact statistically looks like.
2. **Authenticated/declared provenance** — what a signed or otherwise verifiable workflow record says happened.

Agreement is informative. Disagreement is also informative. Missing provenance must remain visibly missing.

## Actor and commissioning evidence

**Status: not inferable from text alone.**

The identity of the person or organisation that requested, commissioned, approved, or deployed a generation action is not a property that can be reliably recovered from prose alone.

A future provenance graph may represent such an actor only when supported by external evidence: signed credentials, authenticated workflow records, system logs, repository history, or other independently verifiable records.

The correct research question is:

> **Can we build an auditable chain linking content measurements, tool actions, human interventions, and authenticated provenance records without confusing inference with fact?**

## Evidence-gated capability ladder

Capabilities should unlock only after benchmark evidence.

### Level 0 — descriptive profile

Current state. Measure and compare text profiles without attribution.

### Level 1 — benchmark-bounded model family

Return calibrated candidate families plus `UNKNOWN`, only after closed-set and open-world validation.

### Level 2 — specific model candidate

Attempt only if model-family performance survives version, prompt, domain, and transformation stress tests.

### Level 3 — generation configuration

Study decoding/configuration signals only after source-family identification is sufficiently stable for the relevant benchmark.

### Level 4 — human intervention map

Localise controlled production-regime changes with explicit uncertainty.

### Level 5 — cross-model lineage

Reconstruct multi-stage generation only after the lower levels have falsifiable evidence and abstention rules.

No level is unlocked by marketing language, a single demo, or one favourable dataset.

## Attribution Challenge 001

The next flagship experiment should be an explicitly preregistered **CogniPrint Attribution Challenge 001**, not a cosmetic release bump.

The challenge should include:

- known model families;
- multiple generation settings;
- multiple genres and lengths;
- human controls;
- paraphrasing;
- translation;
- substantial human editing;
- AI-to-AI rewriting;
- mixed human+AI chains;
- blinded labels during evaluation;
- Top-1 and Top-k candidates;
- calibration;
- `UNKNOWN / insufficient evidence`;
- a public failure report.

The detailed protocol lives in `docs/attribution-challenge-001.md`.

## Fingerprint drift and registry

Model behaviour changes over time. A useful fingerprint cannot be treated as timeless.

CogniPrint should therefore develop a versioned **Fingerprint Registry** with entries conceptually keyed by:

`family → model/version → observation period → benchmark/configuration → reference fingerprint`

This enables explicit study of:

- model drift;
- temporal stability;
- reference-set expiry;
- false attribution caused by stale fingerprints.

A future temporal comparison may say that an artifact is more consistent with one historical reference distribution than another, but only under the benchmark and registry conditions actually tested.

## Where CogniPrint fails

Failure documentation is part of the product and the science.

Dedicated tests should cover at least:

- very short text;
- strong human rewriting;
- translation;
- temperature/decoding changes;
- domain shift;
- unseen models;
- model drift;
- adversarial rewriting;
- conflicting provenance records.

A public `Where CogniPrint fails` artifact should accompany any stronger attribution result.

## Multimodal architecture — vision, not current implementation

CogniPrint may eventually use a common evidence architecture across modalities:

- CogniPrint Text;
- CogniPrint Image;
- CogniPrint Audio;
- CogniPrint Video;
- CogniPrint Agent;
- CogniPrint World;
- CogniPrint Evidence Graph above them.

Only the text research engine exists today. Naming future modules does not imply current implementation or validation.

## Scientific principles

CogniPrint should keep these principles visible in every public description:

1. **Measurement before attribution.** A score is not an identity claim.
2. **Evidence, not verdicts.** Every conclusion should map to inspectable evidence.
3. **Uncertainty is an output.** The system must be allowed to abstain.
4. **UNKNOWN is a first-class class.** Closed-set success must not force an open-world label.
5. **Closed-set attribution is not open-world attribution.**
6. **Human editing is part of the production process, not noise to ignore.**
7. **Provenance metadata and content fingerprints are complementary evidence classes.**
8. **Negative results are valuable.** A failed fingerprint narrows the science.
9. **No actor inference without actor evidence.**
10. **Reproducibility is a feature.** Public claims should map to code, data, configuration, and evaluation artifacts.

## External research context

Relevant public work and standards include:

- NIST, *Reducing Risks Posed by Synthetic Content: An Overview of Technical Approaches to Digital Content Transparency* — https://doi.org/10.6028/NIST.AI.100-4
- NIST GenAI Text 2026 evaluation — https://ai-challenges.nist.gov/text-2026
- C2PA Content Credentials specifications — https://spec.c2pa.org/
- HACo-Det (2025), fine-grained machine-generated text detection under human–AI coauthoring — https://arxiv.org/abs/2506.02959

These references motivate the research direction; they do not validate CogniPrint's future attribution targets.

## Grant-ready research packages

### WP1 — Open model-fingerprint benchmark

Run Attribution Challenge 001 with preregistered data, baselines, calibration, open-world evaluation, and failure reporting.

### WP2 — Human–AI intervention map

Create controlled revision chains and evaluate change-point or span-level intervention detection.

### WP3 — Fingerprint registry and drift

Build versioned reference fingerprints and measure temporal/model-update drift.

### WP4 — Provenance fusion

Combine content-derived evidence with authenticated hashes, revision history, signed credentials, and tool/workflow records without conflating the evidence classes.

### WP5 — Reproducible evidence infrastructure

Produce machine-readable Evidence Capsules and reviewer-facing dossiers containing hashes, feature versions, experiment configuration, calibration context, uncertainty, provenance assertions, and non-claims.

Each work package can produce a useful scientific result even if the central attribution hypothesis fails.

## Current public claim

As of the current release, CogniPrint is a **descriptive, reproducible statistical text-profile framework** plus an open research programme toward cognitive provenance for synthetic digital artifacts.

It does **not** currently identify the exact model, reconstruct a generation lineage, identify an author/commissioner, or provide forensic proof.

Anything beyond the descriptive core remains a hypothesis until dedicated evidence exists.
