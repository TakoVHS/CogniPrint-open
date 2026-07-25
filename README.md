# CogniPrint — cognitive provenance for synthetic language

**CogniPrint is an open-source research framework for measuring statistical fingerprints in text and testing what evidence survives across human-and-model production chains.**

The long-term research question is larger than binary “AI vs. human” detection:

> **What production process is consistent with the evidence, where did that process change, and what remains unknown?**

CogniPrint starts from a deliberately narrow mathematical core: interpretable text profiles that can be reproduced, compared, perturbed, hashed, and audited.

Current scientific readiness remains **`descriptive_only`**.

## Why this matters

A digital artifact may pass through several models, human editors, translation systems, agents, and publishing tools before it reaches a user.

In that environment, “AI-generated” can become a very incomplete description. The trust problem shifts toward **cognitive provenance**: understanding measurable production traces while keeping content-derived inference separate from authenticated provenance records.

CogniPrint uses the fingerprint metaphor carefully. A fingerprint here is a reproducible statistical profile or reference distribution — not a unique biological-style identifier and not proof of a particular model or person.

The project asks:

- which measurable signals repeat within controlled generation processes;
- which differ across source families or versions;
- which survive paraphrasing, translation, human editing, and model-to-model rewriting;
- where statistical regimes change within mixed-production artifacts;
- when the correct output is `UNKNOWN / OUT OF DISTRIBUTION / INSUFFICIENT EVIDENCE`;
- which conclusions require external provenance rather than text alone.

## Evidence, not verdicts

CogniPrint is not intended to end with a single “87% AI” score.

The research direction is to produce reproducible evidence packages containing, where available:

- artifact hashes;
- feature/extractor versions;
- measured coordinates;
- reference-registry revisions;
- candidate results and alternatives;
- transformation/robustness diagnostics;
- calibration and abstention state;
- provenance assertions;
- software commits and reproduction commands;
- explicit non-claims.

**Every conclusion should map to evidence. Every uncertainty should remain visible.**

## What exists today

Current public release: **v0.1.2**.

Implemented research components include:

- a documented 12-dimensional profile `φ(T)` built from interpretable statistics;
- Euclidean-distance and cosine-similarity comparison;
- corpus-relative exploratory thresholds and diagnostics;
- controlled perturbation analysis `Δφ`;
- corpus aggregation and dispersion measurements;
- entropy and word/character n-gram analysis;
- reproducibility scripts, tests, benchmark material, evidence artifacts, and manuscript source;
- pinned external RAID pilot infrastructure;
- leakage-safe transparent baseline evaluation;
- bounded local-evidence and Evidence Capsule prototypes with explicit privacy/non-claim boundaries.

The current release is intentionally labelled **`descriptive_only`**. Broader attribution and lineage claims remain unvalidated.

## Evidence-gated research programme

Capabilities are intended to unlock only after dedicated benchmark evidence.

### Level 0 — descriptive fingerprinting — implemented

Construct compact statistical profiles and measure how they behave under controlled transformations.

### Level 1 — model-family candidates — research target

Test whether model-family information survives leakage-safe benchmarks beyond simple length/surface/n-gram baselines.

A future output must permit `UNKNOWN` rather than force every artifact into a known class.

### Level 2 — specific-model candidate — future research target

Attempt only if family-level evidence survives model-version, domain, prompt and transformation stress tests.

### Level 3 — generation configuration — future research target

Study whether decoding/configuration properties are measurable under controlled conditions.

### Level 4 — human–AI intervention map — research target

Study sentence/span-level **statistical regime changes** and controlled revision chains without converting change points into authorship claims.

### Level 5 — cross-model generation lineage — long-term research target

Study multi-stage chains such as:

`human → model A → human edit → model B → translation → publishing system`

This is not a current validated capability.

## Attribution Challenge 001

The next flagship experiment is a preregistration-ready blind challenge rather than a cosmetic version bump.

It is designed to test — or falsify — the model-family fingerprint hypothesis using:

- controlled source families and human controls;
- prompt/domain/length balancing;
- lineage-safe splits;
- transparent baselines;
- blinded predictions before label reveal;
- calibration;
- held-out unseen families;
- mandatory `UNKNOWN / insufficient evidence`;
- paraphrase, translation, human-edit and AI-to-AI rewrite stress tracks;
- explicit stop/falsification criteria;
- a public failure report.

Protocol: [`docs/attribution-challenge-001.md`](docs/attribution-challenge-001.md)

## Fingerprint Registry and drift

Model behaviour changes over time. A useful reference fingerprint cannot be assumed permanent.

CogniPrint therefore defines a research registry keyed conceptually by:

`family → source/version → observation window → benchmark configuration → feature-map version`

The registry is for observed benchmark distributions, not immutable model identities.

Specification: [`docs/fingerprint-registry-v0.1.md`](docs/fingerprint-registry-v0.1.md)

## Where CogniPrint fails

Failure reporting is part of the project, not a hidden caveat.

Future attribution results must report degradation under short text, domain shift, prompt leakage, length/n-gram confounding, paraphrase, translation, human editing, unseen models, model drift, multilingual transfer, adversarial rewriting, calibration failure and provenance conflicts.

Failure charter: [`docs/where-cogniprint-fails.md`](docs/where-cogniprint-fails.md)

## Provenance evidence

Content-derived measurements and authenticated provenance are different evidence classes.

Possible external provenance inputs include:

- hashes;
- signed content credentials;
- document history;
- model/tool execution logs;
- timestamps;
- repository/publication records;
- lawful workflow records.

CogniPrint does **not** claim that a commissioning person or organisation can be inferred from prose alone.

## Scientific boundary

Current CogniPrint outputs do **not** currently establish:

- author identity;
- unique source model;
- definitive AI origin;
- generation-lineage reconstruction;
- the person or organisation that requested generation;
- intent or responsibility;
- legal or forensic provenance;
- a final classifier suitable for high-stakes decisions.

These boundaries are part of the design. A provenance system becomes more credible when each conclusion states what evidence supports it, what alternatives remain, and when it must abstain.

## Scientific status

- Readiness: `descriptive_only`
- External methodological reviews: `0/1`
- Release: `v0.1.2`
- DOI: pending direct public Zenodo verification
- Repository: https://github.com/TakoVHS/CogniPrint-open
- Project website: https://cogniprint.org

## Reviewer entry points

- [`docs/research-vision.md`](docs/research-vision.md)
- [`docs/attribution-challenge-001.md`](docs/attribution-challenge-001.md)
- [`docs/where-cogniprint-fails.md`](docs/where-cogniprint-fails.md)
- [`docs/fingerprint-registry-v0.1.md`](docs/fingerprint-registry-v0.1.md)
- [`docs/current-state-summary.md`](docs/current-state-summary.md)
- [`docs/evidence-dossier.md`](docs/evidence-dossier.md)
- [`docs/external-review.md`](docs/external-review.md)
- [`docs/reviewer-response-template.md`](docs/reviewer-response-template.md)
- [`paper/main.tex`](paper/main.tex)
- [`CITATION.cff`](CITATION.cff)

## Reproduce

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
python -m unittest tests/test_public_release_export.py -v
python scripts/check_public_benchmark_v11.py
python scripts/secret_scan.py
```

## License

Software is released under the MIT License. Dataset and evidence reuse boundaries are documented in [`DATA_LICENSE.md`](DATA_LICENSE.md) and source-specific provenance records.
