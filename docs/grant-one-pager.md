# CogniPrint — grant one-pager

## Cognitive provenance for a synthetic internet

### The problem

“AI-generated” is becoming too coarse a description of digital artifacts.

A document may pass through several models, human editors, translation systems, agents, and publishing tools before it reaches the public. The trust problem therefore shifts from a binary question — “Was AI used?” — toward a harder one:

> **What production process is consistent with the available evidence, where did that process change, and which parts of the reconstruction are independently verifiable?**

### The idea

CogniPrint is an open-source research programme for **cognitive provenance**: measurable fingerprints, generation-lineage hypotheses, and reproducible evidence about human-and-model production processes.

The core design principle is that CogniPrint must never collapse every signal into one verdict. Every evidence item belongs to an explicit truth class:

- **OBSERVED** — directly measured;
- **INFERRED** — probabilistic and benchmark-bounded;
- **ATTESTED** — supported by an external provenance source whose validation state is recorded;
- **UNKNOWN** — insufficient, out-of-distribution, uncalibrated, conflicting, or unsupported.

**Every conclusion should map to evidence. Every uncertainty should remain visible.**

### What exists now

Current public release line: `v0.1.2`. Scientific readiness: `descriptive_only`.

Implemented:

- documented 12-dimensional text profile `φ(T)`;
- Euclidean/cosine comparison, perturbation analysis, entropy and n-gram diagnostics;
- hashes, benchmark/evidence artifacts and reproducibility tooling;
- **Evidence Schema v1** (`OBSERVED / INFERRED / ATTESTED / UNKNOWN`);
- **Claim Firewall v1**, with source-family attribution disabled by default until evidence, calibration and OOD gates are satisfied;
- machine-readable limitations and mandatory abstention/UNKNOWN semantics;
- **Provenance Conflict Engine**, which reports disagreement instead of choosing whichever signal is convenient;
- Data Constitution for corpus licensing, PII minimisation, lineage and benchmark contamination;
- unsigned `.cogcase` integrity manifests with deterministic hashing and tamper detection;
- independent sealed-challenge evaluator that does not fit/tune the model and binds frozen predictions/revealed labels by SHA-256;
- pinned RAID external-pilot infrastructure and transparent baseline evaluation;
- bounded QVAC local-evidence and Autonomys Evidence Capsule prototypes.

The current system does **not** claim reliable model identification, authorship identification, AI-origin proof, generation-lineage reconstruction, actor attribution, legal compliance, or forensic proof.

### Why the evidence architecture matters

Most detection systems optimise for a headline score. CogniPrint is being built around a different research proposition:

> **An attribution result is only useful if another reviewer can see what was measured, what was inferred, which external records were attested, what remains unknown, and which exact software/reference state produced the result.**

This creates a path from research benchmark to auditable evidence infrastructure without pretending that statistical similarity is cryptographic provenance.

### Flagship experiment — Attribution Challenge 001

Before stronger public claims, CogniPrint will run a preregistered blind family-level challenge designed to prove or falsify the model-fingerprint hypothesis.

The protocol includes:

- multiple known source families and human controls;
- prompt/domain/length balancing and lineage-safe splits;
- simple length/surface/n-gram baselines before complex models;
- frozen predictions before label reveal;
- Top-1 / Top-k candidates;
- Brier/ECE and selective-risk evaluation where calibrated outputs exist;
- held-out unseen generator families;
- mandatory `UNKNOWN / OUT OF DISTRIBUTION / INSUFFICIENT EVIDENCE`;
- temporal/domain holdout design;
- paraphrase, translation, human-edit and model-to-model rewrite stress tracks;
- explicit falsification/stop criteria;
- independent post-reveal evaluator;
- public failure report.

External preregistration remains an open gate and must occur before sealed Stage B analysis.

### Provenance and transparency layer

CogniPrint does not replace cryptographic provenance.

The architecture is designed to consume external provenance as a separate `ATTESTED` evidence class and compare it with content-derived observations/inferences.

Planned C2PA bridge behavior:

- detect supported Content Credentials;
- validate them with a pinned standards-conformant validator/trust configuration;
- preserve validation state;
- map whitelisted assertions into evidence records;
- report **PROVENANCE CONFLICT** when validated external claims and authorised statistical inference disagree.

The C2PA runtime bridge is **not yet implemented or validated**.

A separate Article-50-oriented evidence mapping has also been added for synthetic-content transparency workflows. It explicitly does **not** claim EU AI Act compliance/certification.

### Fundable work packages

**WP1 — Execute Attribution Challenge 001**  
Preregister, run and publish the controlled family-level benchmark, calibration/OOD evaluation and negative results.

**WP2 — C2PA / provenance conflict bridge**  
Implement a standards-conformant Content Credentials reader/validator and map validation states into the evidence ontology without treating metadata as absolute truth.

**WP3 — Human–AI intervention & laundering stress study**  
Measure statistical regime changes, human-edit survival curves, translation attacks and model-to-model rewriting.

**WP4 — Fingerprint Registry & Drift**  
Build versioned, time-scoped reference distributions and measure provider/model drift rather than assuming a timeless fingerprint.

**WP5 — Portable evidence cases**  
Complete `.cogcase` with reproducibility metadata and real detached cryptographic signatures after integrity/signature/trust semantics are independently reviewed.

### What would count as success

Success is not “a detector that always knows who made a text.”

A scientifically useful outcome is a reproducible map of:

- where source-family information exists beyond trivial baselines;
- where it disappears under editing/translation/domain/time shift;
- how often unseen generators are falsely forced into known classes;
- whether confidence is calibrated;
- when UNKNOWN prevents a false attribution;
- when external provenance is required;
- when provenance sources conflict;
- which claims must remain unresolved.

Negative results are publishable outcomes.

### Scientific and safety boundary

CogniPrint does not infer a commissioning person or organisation from prose. Actor/workflow identity may enter an evidence graph only when independent authenticated records actually support the specific statement.

CogniPrint output must not, by itself, be used to accuse a person, automatically punish a student, terminate employment, determine legal liability, or establish criminal/civil responsibility.

CogniPrint is not currently a validated legal-forensics instrument. Current outputs remain `descriptive_only` until dedicated benchmarks, calibration/open-world evidence, independent methodological review and reproducibility results justify stronger claims.

### Public resources

- Website: https://cogniprint.org
- Source: https://github.com/TakoVHS/CogniPrint-open
- Evidence ontology: `docs/evidence-ontology-v1.md`
- Attribution Challenge 001: `docs/attribution-challenge-001.md`
- Evaluation contract: `docs/evaluation-contract-v1.md`
- Independent evaluator: `docs/independent-evaluator-v0.1.md`
- C2PA bridge contract: `docs/c2pa-conflict-bridge-v0.1.md`
- Failure charter: `docs/where-cogniprint-fails.md`
- ORCID: https://orcid.org/0009-0009-6337-1806
