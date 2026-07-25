# CogniPrint — fingerprints for synthetic language

**CogniPrint is an open-source research framework for measuring statistical fingerprints in text and studying how those fingerprints change across editing, paraphrasing, human intervention, and generative-model workflows.**

The long-term research question is larger than binary “AI vs. human” detection:

> **Can we reconstruct a bounded, evidence-based description of how a digital text was produced — which model family may have contributed, where a human may have intervened, and what provenance evidence supports that reconstruction?**

CogniPrint starts from a deliberately narrow mathematical core: interpretable text profiles that can be reproduced, compared, perturbed, and audited.

## Why this matters

A growing share of documents, interfaces, simulations, agents, educational material, media, and other digital environments will be generated or transformed by AI systems. In that world, provenance becomes infrastructure: researchers and users need ways to distinguish **what is measured**, **what is inferred**, and **what is actually known from signed metadata or workflow evidence**.

CogniPrint treats this as a fingerprinting problem. Different generation and editing processes may leave measurable regularities in text. Human revision can alter those regularities. The research programme asks which signals remain stable enough to be useful, which disappear under transformation, and which conclusions are not justified at all.

This is **not** a claim that a text uniquely identifies a neural model or a person. It is a programme for building reproducible evidence around those questions.

## What exists today

Current public release: **v0.1.2**.

Implemented research components include:

- a documented 12-dimensional profile `φ(T)` built from interpretable statistics;
- Euclidean-distance and cosine-similarity comparison;
- corpus-relative exploratory thresholds and p-value diagnostics;
- controlled perturbation analysis `Δφ`;
- corpus aggregation and dispersion measurements;
- Shannon entropy measurements;
- word/character n-gram analysis;
- reproducibility scripts, tests, public benchmark material, evidence artifacts, and manuscript source.

The current release is intentionally labelled **`descriptive_only`**. That status means the measurements are available and reproducible, while broader attribution claims remain unvalidated.

## Research programme

CogniPrint is being developed toward four increasingly demanding layers.

### 1. Statistical fingerprinting — implemented

Construct compact, interpretable signatures of text and measure how they behave under controlled transformations.

### 2. Model-family attribution — research target

Evaluate whether ensembles of statistical, stylometric, entropy, and learned features can distinguish outputs from known model families under controlled benchmarks, including cross-domain and multilingual tests.

A future result here would be probabilistic and benchmark-bounded — not a universal “this was written by model X” oracle.

### 3. Human–AI intervention mapping — research target

Study whether mixed-authorship documents can be segmented into regions that show different generation/editing characteristics, and whether revision chains can reveal where machine output was substantially transformed by a human.

This aligns with an emerging research problem sometimes described as fine-grained human–AI coauthoring detection. It remains an open problem, not a solved CogniPrint capability.

### 4. Provenance reconstruction — research target

Combine content-derived signals with external provenance evidence such as signed metadata, document history, model/tool logs, hashes, and standards such as **C2PA Content Credentials**.

Only this evidence layer can responsibly support questions such as **which tool performed an action, when an edit occurred, or which actor commissioned a workflow**. CogniPrint does **not** claim that the commissioning person or organisation can be inferred from text alone.

## Scientific boundary

Current CogniPrint outputs are descriptive research measurements. They do **not** currently establish:

- the identity of an author;
- a unique source model;
- definitive AI origin;
- the person or organisation that requested generation;
- legal or forensic provenance;
- intent or responsibility;
- a final classifier suitable for high-stakes decisions.

These boundaries are part of the design, not a disclaimer added after the fact. A provenance system becomes more credible when each conclusion states what evidence supports it and what uncertainty remains.

## Research context

The direction is motivated by the broader shift from simple synthetic-content detection toward **content transparency and provenance**. NIST surveys detection, watermarking, authentication, and provenance as complementary technical approaches, while C2PA defines a standard for cryptographically bound content provenance and edit history.

- NIST, *Reducing Risks Posed by Synthetic Content*: https://doi.org/10.6028/NIST.AI.100-4
- C2PA specifications: https://spec.c2pa.org/
- NIST GenAI Text 2026 evaluation: https://ai-challenges.nist.gov/text-2026

## Scientific status

- Readiness: `descriptive_only`
- External methodological reviews: `0/1`
- Release: `v0.1.2`
- DOI: pending direct public Zenodo verification
- Repository: https://github.com/TakoVHS/CogniPrint-open
- Project website: https://cogniprint.org

## Public research package

The release contains the Python research engine, tests, bounded benchmark material, evidence artifacts, manuscript source, citation metadata, and provenance notes.

Administrative records, application payloads, personal contact data, mailbox identifiers, billing operations, hosted deployment records, and local workspaces are intentionally excluded.

Reviewer entry points:

- [`docs/research-vision.md`](docs/research-vision.md)
- [`docs/current-state-summary.md`](docs/current-state-summary.md)
- [`docs/evidence-dossier.md`](docs/evidence-dossier.md)
- [`docs/external-review.md`](docs/external-review.md)
- [`docs/reviewer-response-template.md`](docs/reviewer-response-template.md)
- [`docs/grant-readiness-next-call.md`](docs/grant-readiness-next-call.md)
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
