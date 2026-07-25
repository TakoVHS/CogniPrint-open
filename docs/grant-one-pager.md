# CogniPrint — grant one-pager

## Synthetic-language fingerprints and verifiable provenance

### The problem

AI is becoming part of the production process for documents, agents, media, software, research workflows, education, and synthetic digital environments. The binary question “human or AI?” is therefore becoming inadequate. Real artifacts may pass through several models, human editors, translation systems, and publishing tools before they reach a user.

The more useful question is:

> What production process is consistent with the available evidence, where did human intervention occur, and which parts of that reconstruction are independently verifiable?

### The idea

CogniPrint is an open-source research programme that treats generated language as a fingerprinting and provenance problem.

The current system builds compact, interpretable statistical profiles of text and measures how those profiles change under comparison and controlled edits. The proposed research programme tests whether those signals can support calibrated model-family attribution, human–AI intervention mapping, and fusion with authenticated provenance such as hashes, revision history, tool logs, and Content Credentials.

### What exists now

Current release: v0.1.2. Scientific readiness: `descriptive_only`.

Implemented:

- documented 12-dimensional text profile `φ(T)`;
- Euclidean and cosine comparison;
- perturbation analysis `Δφ`;
- corpus aggregation;
- Shannon entropy analysis;
- word and character n-gram diagnostics;
- corpus-relative exploratory thresholds;
- public benchmark material, tests, evidence artifacts, and manuscript source.

The current release does not claim reliable model identification, authorship identification, AI-origin proof, or actor attribution.

### Fundable research programme

**WP1 — Open model-fingerprint benchmark**  
Build a controlled multilingual benchmark across known model families, prompt regimes, sampling settings, and domains. Compare CogniPrint with simple and learned baselines.

**WP2 — Human–AI intervention map**  
Create controlled revision chains and test sentence/span-level transition detection between generated text and substantive human editing.

**WP3 — Robustness and open-world evaluation**  
Measure failure under paraphrasing, translation, model drift, domain shift, and unseen model families. Add calibrated abstention instead of forced attribution.

**WP4 — Provenance fusion**  
Prototype a separate evidence channel for hashes, signed metadata, C2PA-style credentials, revision history, and authenticated tool records. Test content-only, provenance-only, and combined evidence.

**WP5 — Reproducible evidence bundles**  
Produce machine-readable reports containing input hashes, feature-map version, experiment configuration, calibration context, uncertainty, provenance assertions, and explicit non-claims.

### What would count as success

Success is not “a detector that always knows who made a text.” A scientifically useful outcome is a reproducible map of where fingerprint-based attribution works, where it fails, and when provenance metadata is required.

Primary outputs:

- open benchmark and protocol;
- calibrated baseline results;
- robustness/open-world evaluation;
- human–AI intervention dataset and metrics;
- provenance-fusion prototype;
- reproducible research artifacts and manuscript updates.

Negative results remain publishable outcomes.

### Why now

NIST’s synthetic-content transparency work treats detection, authentication, watermarking, and provenance as complementary approaches. NIST GenAI Text 2026 evaluates text discriminators with discrimination and calibration metrics. C2PA provides a standard architecture for cryptographically bound content provenance. CogniPrint’s research programme sits at the intersection of those problems: measurable content fingerprints plus auditable provenance.

### Scientific boundary

CogniPrint does not infer a commissioning person or organisation from text. Actor/workflow identity may only enter a provenance graph when authenticated external records support it.

Current public outputs remain descriptive until dedicated benchmarks, independent methodological review, and reproducibility evidence justify stronger claims.

### Public resources

- Website: https://cogniprint.org
- Source: https://github.com/TakoVHS/CogniPrint-open
- Research vision: `docs/research-vision.md`
- Benchmark protocol: `docs/model-fingerprint-benchmark-v0.1.md`
- ORCID: https://orcid.org/0009-0009-6337-1806
