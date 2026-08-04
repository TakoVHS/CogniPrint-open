# CogniPrint Status Evidence Policy

Status: `ACTIVE / FAIL-CLOSED / DEVELOPMENT-ONLY UNTIL MERGED`

## Purpose

CogniPrint has several valid but different evidence layers: the public `main` release, validated development branches, hosted/equivalent runner records, GitHub Actions, external review, and future sealed scientific evidence. These layers must not be collapsed into one headline status.

The machine-readable snapshot is `docs/evidence-project-status.json`.

## Canonical versus development evidence

The canonical public capability state is determined by files merged into `main` and by evidence explicitly accepted by the project status contract.

A Draft pull request may contain strong technical evidence without changing the public capability state. Therefore:

- branch evidence does not make branch code available in `main`;
- a passing product or packaging gate does not unlock a scientific claim;
- a passing equivalent runner does not rewrite GitHub Actions from `NOT_EXECUTED` to `PASS`;
- `NOT_EXECUTED` is neither a code failure nor a test pass;
- external review remains `0/1` until a qualifying substantive human review is archived;
- DOI verification remains pending until the public record is directly reachable and matches the intended release.

## Status surfaces

The following public surfaces must remain mutually consistent:

- `README.md`;
- `docs/current-state-summary.md`;
- `docs/trust.md`;
- `docs/external-review.md`;
- `docs/external-review/status.json`;
- `CITATION.cff`;
- `pyproject.toml`;
- `RESEARCH_FREEZE_001.md`;
- `docs/evidence-project-status.json`.

## Required distinctions

### Product state

Describes installed functionality, packaging, offline operation, dossier verification, security and usability. Product progress may reach beta while scientific attribution claims remain locked.

### Execution state

Must name the exact execution environment and target:

- `GITHUB_ACTIONS=NOT_EXECUTED` means GitHub-hosted jobs did not run executable steps;
- an equivalent hosted runner record is reported separately with exact commit/tree and logs;
- historical evidence cannot be reused for a changed tree without demonstrated content equivalence.

### Scientific state

Until a separate claim review changes it, the canonical state remains:

```text
SCIENTIFIC_READINESS=descriptive_only
RESEARCH_MODE=PROOF_MODE
CANONICAL_FREEZE=PRE-FREEZE
STAGE_B=NOT_AUTHORISED_TO_START
EXTERNAL_METHODOLOGICAL_REVIEW=0/1
```

### Provenance and integrity state

Hashes, signatures, signer trust, build provenance and scientific validity are separate properties. A checksum does not establish signer identity; a valid signature does not establish scientific truth.

## Change control

A status update must include:

1. exact repository commit and tree where relevant;
2. the evidence source and execution environment;
3. what changed and what did not change;
4. whether the evidence is canonical or development-only;
5. blockers that remain;
6. no automatic expansion of claims.

Any update that raises scientific readiness, authorises Stage B, marks a review complete, verifies the DOI, or calls an artifact signed must fail closed unless the corresponding independently inspectable evidence exists.

## Versioning policy

- Keep the public package/release line at `0.1.2` while new capabilities remain in Draft PRs.
- Do not reuse `0.1.2` for a merged workstation release.
- After the workstation, security and release gates are complete, prepare a separately reviewed pre-release such as `0.2.0b1` before a stable `0.2.0`.
- A product version bump does not change the scientific readiness label.
