# Contributing to CogniPrint

CogniPrint welcomes corrections, tests, reproducibility work, privacy improvements, benchmark-integrity fixes, documentation, and carefully scoped research contributions.

## Core principle

Evidence and implementation must remain stronger than the wording used to describe them. A pull request cannot unlock a scientific claim merely because code exists or tests pass on synthetic fixtures.

## Before opening a pull request

1. Open or reference an issue for scientific, security-sensitive, schema, packaging, or public-claim changes.
2. Work from the current target branch and keep the change narrowly scoped.
3. Do not add private text, credentials, sealed labels, personal data, proprietary datasets, or unverified model artifacts.
4. Preserve the current claim boundaries unless a dedicated evidence gate explicitly authorises a change.
5. Record exact versions, seeds, hashes, and data visibility where they affect reproducibility.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Run the checks relevant to your change. At minimum:

```bash
python -m unittest discover -s tests -v
python -m py_compile $(find src scripts tests -name '*.py' -type f)
python scripts/export_public_release.py --check-only
python scripts/secret_scan.py
git diff --check
```

Where Ruff is available:

```bash
ruff check src scripts tests
```

A narrower test command is acceptable during development, but the pull request must state exactly what was and was not executed.

## Pull request requirements

A reviewable pull request should include:

- purpose and explicit non-goals;
- exact base and head commits;
- changed-file scope;
- tests and commands actually executed;
- expected security, privacy, scientific, and compatibility effects;
- deterministic evidence where applicable;
- negative results and unresolved blockers;
- whether raw text or external network access is involved;
- rollback or failure behaviour for high-risk changes.

Do not report `PASS` for a workflow that never executed its first step. Do not substitute historical results for validation of a new head unless content equivalence is demonstrated explicitly.

## Research integrity

Research-facing changes must be fail-closed.

- Stage A and development-visible data must not be represented as sealed Stage B evidence.
- Data, lineage, or prompt overlap must not be hidden through post-hoc exclusions.
- Calibration, thresholds, exclusions, and claim rules must not be tuned using sealed outcomes.
- Conventional baselines and negative results must remain visible.
- `UNKNOWN`, out-of-distribution, and insufficient-evidence outcomes must not be converted into forced labels.
- An automated or AI-assisted review does not replace independent human methodological review when that review is an explicit gate.

## AI-assisted contributions

AI assistance is permitted for drafting, implementation, tests, and review. Contributors remain responsible for every submitted line and should disclose material AI assistance when it affected scientific reasoning, security-sensitive code, or a large generated patch.

Generated content must be checked for:

- invented citations or APIs;
- unpinned dependencies;
- unsafe serialization or subprocess use;
- accidental raw-data persistence;
- unsupported scientific claims;
- tests that only reproduce the implementation rather than the intended contract.

## Privacy and datasets

Only include data that is public, licensed for the intended use, synthetic, or otherwise authorised. Prefer metadata-only fixtures and content hashes. Dataset licences and provenance must be documented separately from the MIT software licence.

## Security reports

Do not disclose exploitable vulnerabilities in a public issue. Follow [SECURITY.md](SECURITY.md).

## Commit and review style

Prefer small, descriptive commits. Keep research, infrastructure, product, and documentation changes separate when they have different review gates. Draft pull requests are encouraged until the exact-head validation record is complete.
