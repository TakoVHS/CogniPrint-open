# CogniPrint research vision

## One-sentence thesis

**CogniPrint studies whether digital text can carry reproducible fingerprints of the human-and-model process that produced it, and how those fingerprints can be combined with provenance evidence without overstating what the text alone can prove.**

## The problem

The question “Was this written by AI?” is already too small.

As generative models become embedded in writing tools, agents, research workflows, education, media production, software, simulations, and synthetic digital environments, many artifacts will be neither purely human nor purely machine. A document may be drafted by one model, rewritten by another, edited by a person, translated, paraphrased, and published through a separate system.

The scientifically useful question becomes:

> **What production process is consistent with the evidence we have, and how certain are we?**

That requires more than a binary detector. It requires a layered provenance model that separates measurable content signals from signed or externally observed workflow evidence.

## The fingerprint idea

CogniPrint uses the metaphor of a fingerprint carefully.

A biological fingerprint is not the right mathematical analogy for uniqueness. Neural models do not necessarily leave a single permanent, collision-free signature in every output. Prompts, sampling parameters, fine-tuning, language, domain, post-editing, and model updates can all change observable patterns.

For CogniPrint, a **fingerprint** means a reproducible vector or ensemble of measurable properties that can be compared across controlled datasets.

The research questions are:

- Which properties are stable within outputs from the same generation process?
- Which properties differ between model families or versions?
- Which signals survive paraphrasing, translation, and human editing?
- Which signals disappear or become misleading?
- Can mixed human–AI documents be localised at sentence, span, or revision level?
- How should uncertainty be reported so that a profile is not mistaken for proof of identity?

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

**Status: research target.**

The next scientific programme is to build controlled corpora from known model families and evaluate whether combinations of interpretable and learned signals support probabilistic source-family attribution.

A credible study should include:

- multiple model families and versions;
- multiple prompt families;
- temperature/sampling variation;
- multilingual material;
- cross-domain holdouts;
- paraphrase and translation attacks;
- model updates over time;
- human baselines;
- calibration and abstention;
- out-of-distribution tests.

The intended output is not “Model X wrote this with certainty.” It is closer to:

> “Under benchmark B, the observed profile is most consistent with family F among the tested classes, with confidence C and stated limitations.”

## Layer 3 — human–AI intervention mapping

**Status: research target.**

Real documents are increasingly coauthored. The research goal is to evaluate whether a document can be represented as a sequence of regions with different production characteristics, and whether revision histories can reveal transitions between machine generation and substantial human editing.

Possible research outputs include:

- sentence/span-level machine-likelihood maps;
- change-point detection over fingerprint trajectories;
- human-edit intensity estimates;
- revision-chain comparisons;
- uncertainty-aware “mixed provenance” labels.

This area is not solved. Fine-grained human–AI coauthoring detection remains an active research problem, and CogniPrint should publish negative results as readily as positive ones.

## Layer 4 — provenance evidence

**Status: research and integration target.**

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

C2PA is especially relevant because its Content Credentials architecture records provenance assertions about creation and edits and binds them cryptographically to an asset.

CogniPrint's long-term architecture should be able to compare two distinct evidence channels:

1. **Observed content evidence** — what the artifact statistically looks like.
2. **Declared/cryptographic provenance** — what a signed workflow says happened.

Agreement is informative. Disagreement is also informative.

## Layer 5 — actor and commissioning evidence

**Status: not inferable from text alone.**

The identity of the person or organisation that requested, commissioned, approved, or deployed a generation action is not a property that can be reliably recovered from prose alone.

A future CogniPrint provenance graph may represent such an actor only when supported by external evidence: signed credentials, authenticated workflow records, system logs, repository history, or other independently verifiable records.

The intended research question is therefore not:

> “Can we guess who ordered this from the text?”

It is:

> **“Can we build an auditable chain linking content measurements, tool actions, human interventions, and authenticated provenance records without confusing inference with fact?”**

## Why this can matter

If successful, the programme could support research in:

- AI transparency and governance;
- scientific and academic integrity research;
- journalism and source verification;
- content provenance;
- digital-evidence research;
- platform trust and safety;
- dataset auditing;
- model-behaviour measurement;
- human–AI collaboration studies.

High-stakes deployment would require substantially stronger validation, governance, privacy review, and domain-specific evidence than the current release provides.

## Scientific principles

CogniPrint should keep the following principles visible in every public description:

1. **Measurement before attribution.** A score is not an identity claim.
2. **Uncertainty is an output.** A system must be allowed to abstain.
3. **Closed-set attribution is not open-world attribution.** Success among tested models does not prove the true source is one of them.
4. **Human editing is part of the problem, not noise to ignore.**
5. **Provenance metadata and content fingerprints are complementary evidence classes.**
6. **Negative results are valuable.** A failed fingerprint is evidence about the limits of attribution.
7. **No actor inference without actor evidence.**
8. **Reproducibility is a feature.** Public claims should map to code, data, and evaluation artifacts.

## External research context

Relevant public work and standards include:

- NIST, *Reducing Risks Posed by Synthetic Content: An Overview of Technical Approaches to Digital Content Transparency* — https://doi.org/10.6028/NIST.AI.100-4
- NIST GenAI Text 2026 evaluation — https://ai-challenges.nist.gov/text-2026
- C2PA Content Credentials specifications — https://spec.c2pa.org/
- HACo-Det (2025), a study of fine-grained machine-generated text detection under human–AI coauthoring — https://arxiv.org/abs/2506.02959

These references motivate the research direction; they do not validate CogniPrint's future attribution targets.

## Grant-ready research packages

The broad vision should be decomposed into fundable, falsifiable work packages rather than sold as one universal detector.

### WP1 — Open benchmark for model fingerprints

Build and publish a controlled multilingual benchmark across model families, prompts, sampling regimes, and domains. Evaluate CogniPrint features against simple and learned baselines.

### WP2 — Human–AI coauthoring map

Create controlled revision chains and evaluate sentence/span-level intervention detection, change points, and calibration.

### WP3 — Provenance fusion

Prototype a provenance graph that can ingest content fingerprints plus C2PA-style or other signed workflow evidence and report agreements, conflicts, and missing evidence.

### WP4 — Robustness and evasion study

Measure what happens under paraphrasing, translation, compression, rewriting, prompt variation, and substantial human editing.

### WP5 — Reproducible evidence interface

Produce machine-readable evidence bundles containing input hashes, feature versions, model/version metadata when available, metrics, calibration context, and explicit non-claims.

Each work package can produce a useful scientific result even if the central hypothesis fails.

## Current public claim

As of the current release, CogniPrint is a **descriptive, reproducible statistical text-profile framework** and an open research programme toward stronger synthetic-language provenance methods.

Anything beyond that remains a hypothesis until dedicated evidence exists.
