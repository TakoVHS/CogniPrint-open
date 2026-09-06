# Contributing to CogniPrint

CogniPrint is an open research software project. Contributions are welcome when they improve reproducibility, correctness, documentation, tests, usability, benchmarking, or clearly bounded research infrastructure.

## Scientific boundary first

The current scientific readiness is `descriptive_only`.

Contributions must not present current CogniPrint outputs as proof of:

- author identity;
- a unique source model;
- definitive AI origin;
- generation-lineage reconstruction;
- intent or responsibility;
- legal or forensic provenance;
- suitability for high-stakes automated decisions.

If a contribution introduces a stronger research hypothesis, benchmark, calibration rule, or attribution claim, it must be isolated behind an explicit evidence gate and must preserve an `UNKNOWN / insufficient evidence` path where appropriate.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Optional public-data dependencies:

```bash
pip install -e '.[real-data]'
```

Optional demo dependencies:

```bash
pip install -e '.[demo]'
```

## Required checks

Before opening a pull request, run the checks relevant to your change. The public release baseline includes:

```bash
python -m unittest tests/test_public_release_export.py -v
python scripts/check_public_benchmark_v11.py
python scripts/secret_scan.py
```

For research-result changes, also run the documented Makefile target that regenerates the affected artifact and include the exact configuration, source data, and output paths in the pull request.

## Research contribution rules

Research-facing pull requests should state:

1. the question being tested;
2. the exact code/data/configuration changed;
3. the expected failure mode;
4. whether the change affects a frozen or preregistered protocol;
5. what result would falsify the proposed interpretation;
6. which evidence class applies: `OBSERVED`, `INFERRED`, `ATTESTED`, or `UNKNOWN`;
7. whether any scientific-readiness label changes. A readiness label must never be upgraded only because code was merged.

## Data and licensing

Do not add data unless its source, license, redistribution boundary, and transformation history are documented. Follow `DATA_LICENSE.md` and source-specific provenance records.

## Reproducibility

Prefer deterministic scripts, pinned configuration, recorded seeds, versioned artifacts, and exact commit references. A result that cannot be reproduced from the repository should not be presented as a project-level finding.

## Generative AI assistance

Generative AI tools may be used as development assistants, but contributors remain responsible for correctness, licensing, tests, citations, and scientific claims. AI-generated code or prose is not external methodological review and is not evidence that a scientific conclusion is valid.

## Pull requests

Keep pull requests focused. Separate product/UI changes from scientific-method changes when possible. Do not combine a visual redesign with a change in scientific interpretation.

A good pull request description includes:

- purpose and scope;
- files changed;
- commands executed;
- test/reproduction result;
- scientific impact: `none`, `descriptive-only`, or `requires separate review`;
- known limitations.

## Conduct

Participation is governed by the repository Code of Conduct. Respectful critique, replication attempts, negative results, and well-supported disagreement are explicitly welcome.
