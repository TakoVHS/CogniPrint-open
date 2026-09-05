# Contributing to CogniPrint

CogniPrint is an evidence-first research project. Contributions are welcome when they improve correctness, reproducibility, security, testability, documentation, or the integrity of the current research programme.

## Research boundary

Current scientific readiness is `descriptive_only`. Challenge 001 Stage B is `NOT_AUTHORISED_TO_START`, and the project remains under the proof-mode/no-new-feature rule documented in `RESEARCH_FREEZE_001.md` and `docs/current-state-summary.md`.

A code change must not silently unlock a scientific claim. Changes that affect attribution, provenance, calibration, OOD/UNKNOWN handling, evaluator behaviour, benchmark membership, frozen artifacts, or public claims require explicit evidence and review.

## Development setup

Python 3.10, 3.11, and 3.12 are supported.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install build ruff
```

The Makefile provides the canonical local quality commands:

```bash
make test
make lint
make release-check
make verify
```

`make test` intentionally discovers every `tests/test_*.py` test. `make test-fast` is only the narrow public-release/secret-scan subset and must not be represented as a full-suite result.

## Pull-request expectations

Before requesting review:

1. keep the change scoped to one clear purpose;
2. preserve existing scientific non-claims and evidence classes unless a separately reviewed evidence change justifies an update;
3. add or update tests for changed behaviour;
4. run `make verify` on the exact commit when a functioning execution environment is available;
5. never report a test, benchmark, security, or deployment result that did not actually execute;
6. do not commit live credentials, API keys, private datasets, or personal data;
7. keep Stage A development-visible material separate from any future sealed Stage B material;
8. document any remaining unverified gate explicitly.

## Reproducibility

The library metadata in `pyproject.toml` intentionally uses compatible version ranges. Exact environment reproduction must be based on a lock/constraints artifact generated from a validated environment; exact dependency versions must not be guessed or hand-authored merely to make a repository look pinned.

Until such a validated lock exists, record the Python version, exact CogniPrint commit SHA, install command, and complete execution logs with every preserved result.

## Security and data handling

Run the tracked-tree secret scanner before proposing a public release:

```bash
python scripts/secret_scan.py
```

The history scan is a stronger release-time gate and requires a real Git checkout:

```bash
python scripts/secret_scan.py --history
```

Respect `DATA_CONSTITUTION.md` and `DATA_LICENSE.md` for licensing, provenance, PII minimisation, contamination, and lineage rules.

## Scientific claims

A passing build is engineering evidence, not scientific validation. Challenge 001 results, model-family attribution claims, external provenance claims, and any change from `descriptive_only` require the dedicated research gates described in the repository. When evidence is missing, the correct state is `UNKNOWN`, `NOT_VERIFIED`, or the more specific fail-closed status defined by the relevant contract.
