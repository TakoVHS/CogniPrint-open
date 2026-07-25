# CogniPrint — grant one-pager

## Cognitive provenance for a synthetic internet

### The problem

“AI-generated” is becoming too coarse a description of digital artifacts.

A document may pass through several models, human editors, translation systems, agents, and publishing tools before it reaches the public. The trust problem therefore shifts from a binary question — “Was AI used?” — toward a harder one:

> **What production process is consistent with the available evidence, where did that process change, and which parts of the reconstruction are independently verifiable?**

### The idea

CogniPrint is an open-source research programme for **cognitive provenance**: measurable fingerprints, generation-lineage hypotheses, and reproducible evidence about human-and-model production processes.

The current system does **not** claim to reconstruct that lineage. It already provides the lower-level measurement foundation: compact statistical text profiles, perturbation analysis, hashes, versioned evidence artifacts, and reproducibility tooling.

The proposed research programme asks whether that foundation can support progressively stronger — and falsifiable — capabilities:

- benchmark-bounded model-family candidates;
- `UNKNOWN / OUT OF DISTRIBUTION / INSUFFICIENT EVIDENCE` abstention;
- human–AI regime-change mapping;
- fingerprint drift over time;
- controlled cross-model lineage experiments;
- fusion of content-derived measurements with authenticated provenance records.

### Evidence, not verdicts

CogniPrint is not designed around a single “87% AI” answer.

The intended product of an analysis is a reproducible evidence dossier containing, where available:

- artifact hash;
- feature-map/extractor version;
- measured feature vector;
- benchmark/reference-registry version;
- candidate results and alternatives;
- transformation/robustness diagnostics;
- calibration and abstention state;
- external provenance assertions;
- software commit and reproducibility command;
- explicit non-claims.

**Every conclusion should map to evidence. Every uncertainty should remain visible.**

### What exists now

Current public release: `v0.1.2`. Scientific readiness: `descriptive_only`.

Implemented:

- documented 12-dimensional text profile `φ(T)`;
- Euclidean and cosine comparison;
- perturbation analysis `Δφ`;
- corpus aggregation;
- entropy and n-gram diagnostics;
- public benchmark/evidence material;
- pinned RAID external-pilot infrastructure;
- leakage-safe transparent baseline evaluation;
- bounded QVAC local-evidence prototype;
- canonical CogniPrint Evidence Capsule with strict privacy/non-claim boundaries;
- reviewer and reproducibility tooling.

The current release does not claim reliable model identification, authorship identification, AI-origin proof, generation-lineage reconstruction, or actor attribution.

### Flagship experiment — Attribution Challenge 001

Before stronger public claims, CogniPrint will run a preregistered blind challenge designed to prove or falsify the model-family fingerprint hypothesis.

The protocol includes:

- multiple known source families and human controls;
- prompt/domain/length balancing;
- leakage-safe lineage grouping;
- length, surface-statistic, character n-gram and word n-gram baselines;
- blinded predictions before label reveal;
- Top-1 / Top-k candidates;
- calibration;
- held-out unseen families;
- mandatory `UNKNOWN / insufficient evidence`;
- paraphrase, translation, human-edit and AI-to-AI rewrite stress tracks;
- a public failure report.

Protocol: `docs/attribution-challenge-001.md`.

### Fundable work packages

**WP1 — Attribution Challenge 001**  
Execute and publish the controlled model-family benchmark, including open-world abstention and negative results.

**WP2 — Human–AI Intervention Map**  
Create controlled revision chains and test sentence/span-level statistical regime-change detection without converting a change point into an authorship claim.

**WP3 — Fingerprint Registry & Drift**  
Build versioned reference fingerprints and measure how model updates, time, prompting, domain and decoding change the reference space.

**WP4 — Provenance Fusion**  
Combine content-derived evidence with hashes, signed credentials, revision history and authenticated tool/workflow records while keeping those evidence classes separate.

**WP5 — Reproducible Evidence Infrastructure**  
Produce machine-readable Evidence Capsules/dossiers with hashes, configurations, calibration context, uncertainty, provenance assertions and explicit non-claims.

### What would count as success

Success is not “a detector that always knows who made a text.”

A scientifically useful outcome is a reproducible map of:

- where fingerprint-based family attribution works;
- where simple baselines explain the apparent signal;
- where human editing or translation destroys it;
- how often unseen models are falsely forced into known classes;
- when `UNKNOWN` prevents an unsafe conclusion;
- how quickly reference fingerprints drift;
- when authenticated provenance is required because content alone is insufficient.

Negative results remain publishable outcomes.

### Where CogniPrint fails

Failure reporting is a first-class deliverable, not a footnote.

The project has a public failure charter covering short inputs, domain shift, prompt leakage, length/n-gram confounding, paraphrase, translation, human editing, cross-model rewriting, unseen models, drift, multilingual limits, calibration and provenance conflicts.

Failure charter: `docs/where-cogniprint-fails.md`.

### Why this matters

As synthetic content becomes a normal layer of the internet, the useful trust question is increasingly not merely whether a model participated, but **what process produced an artifact and what evidence survives that process**.

CogniPrint’s long-term role is therefore not “another AI detector.” It is an open evidence layer for studying cognitive provenance — beginning with text, while keeping the architecture compatible with future multimodal evidence without claiming those modalities exist today.

### Scientific boundary

CogniPrint does not infer a commissioning person or organisation from text. Actor/workflow identity may only enter a provenance graph when authenticated external records support it.

CogniPrint is not currently a validated legal-forensics instrument. Current outputs remain descriptive until dedicated benchmarks, independent methodological review, calibration/open-world evidence, and reproducibility results justify stronger claims.

### Public resources

- Website: https://cogniprint.org
- Source: https://github.com/TakoVHS/CogniPrint-open
- Research vision: `docs/research-vision.md`
- Attribution Challenge 001: `docs/attribution-challenge-001.md`
- Failure charter: `docs/where-cogniprint-fails.md`
- External RAID pilot: `docs/raid-pilot-m1.md`
- ORCID: https://orcid.org/0009-0009-6337-1806
