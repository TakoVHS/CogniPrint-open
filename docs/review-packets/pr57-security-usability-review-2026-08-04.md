# CogniPrint PR #57 — Independent Security and Usability Review Packet

Prepared: 4 August 2026

## Review target

- PR: `#57`
- branch: `development/self-hosted-evidence-workstation-001`
- exact head: `6832729562d4587609bb93e5af3d4f7f96911d06`
- content tree: `6d3754f3bc695c7e482c4f307316e6da99d29589`
- base: `d154b8610b182fe9110bf52fcadf02914498d356`
- scope: 22 files
- state: OPEN / DRAFT / not merged
- technical status: `EXACT_HEAD_M3_GATE=PENDING`

This packet is not approval, merge authorization, a Ready transition, scientific validation or proof of security.

## Hard boundaries

- `DEVELOPMENT_ONLY`
- `SCIENTIFIC_CLAIM_EVIDENCE=false`
- `CANONICAL_FREEZE=PRE-FREEZE`
- `EXTERNAL_REGISTRATION=NOT_SUBMITTED`
- `STAGE_B=NOT_AUTHORISED_TO_START`
- `GITHUB_ACTIONS=NOT_EXECUTED`
- no authorship, identity, legal, forensic or deterministic model-source claim

## Implemented surface

### M1 — reproducible packaging

- pinned Nix flake, package, application and development shell;
- OCI image from a pinned Python base digest;
- fixed unprivileged runtime identity `10001:10001`;
- no-network, read-only root, dropped capabilities and `no-new-privileges` Compose defaults.

### M2 — evidence dossier v1

- canonical deterministic `dossier.json`;
- versioned JSON Schema `urn:cogniprint:evidence-dossier:1`;
- local exporter and independent offline verifier;
- source/configuration represented by hash and byte length, not embedded;
- exact artifact inventory, size and SHA-256 verification;
- fail-closed schema, canonical JSON, path, symlink, inventory and mutation checks.

### M3 — hardening

- bounded manifest size, JSON nesting, tree depth, tree entries and artifact resources;
- rejection of FIFOs and unsupported filesystem objects;
- before/after inventory comparison for mutation during verification;
- self-verifying export;
- machine-readable resource limits;
- temporary-data purge with dry-run default, explicit confirmation, prefix allowlist, precomputed plan, symlink non-traversal and filesystem-boundary rejection;
- main CLI: `cogniprint dossier export|verify|limits|purge-temp`;
- separate producer/verifier wheel installations;
- socket-blocked offline verification;
- quickstart and operator guide.

## Current evidence

Functional replay:

- M2 tests: 13/13 PASS;
- M3 tests: 19/19 PASS;
- combined tests: 32/32 PASS;
- semantic repeated-output comparison: PASS;
- quickstart, mutation rejection and source-byte leakage checks: PASS;
- separate producer/verifier installations: PASS;
- socket-blocked verification: PASS;
- CLI and safe purge workflows: PASS.

Hosted run `dpl_7dyDECunNexQzVVwk9EJzKXLewMX` confirmed the exact current content tree and passed:

- exact 22-file scope and clean checkout;
- Ruff 0.16.1 correctness rules `E4,E7,E9,F`;
- `py_compile`;
- all 32 tests with semantic repeatability;
- quickstart and cross-installation;
- socket-blocked verification;
- CLI and purge;
- packaging contract;
- secret scan;
- sanitized public-release check.

It stopped only because Vercel's restricted build sandbox denied a `/proc` mount requested by Buildah's rootless runtime. A runner-only retry uses a separate unprivileged user with VFS storage and chroot isolation. No final `EXACT_HEAD_M3_GATE=PASS` is claimed yet.

## Files to review

- `src/cogniprint/dossier.py`
- `src/cogniprint/dossier_security.py`
- `src/cogniprint/entrypoint.py`
- `schemas/cogniprint-evidence-dossier-v1.schema.json`
- `tests/test_evidence_dossier.py`
- `tests/test_dossier_m3.py`
- `Containerfile`
- `compose.yaml`
- `flake.nix`
- `flake.lock`
- `docs/evidence-threat-model-v1.md`
- `docs/evidence-dossier-m3-operator-guide.md`
- `demo/cross_installation_dossier_gate.py`

## Security questions

1. Does the documentation clearly distinguish integrity/reproducibility from producer authenticity and trust?
2. Are the file-descriptor, `O_NOFOLLOW`, regular-file and before/after inventory controls adequate for the declared threat model?
3. Which `openat`/directory-descriptor controls are required before use on a filesystem shared with an adversarial local user?
4. Are resource limits checked early enough to prevent expensive or destructive work?
5. Is temporary purge conservative enough across symlinks, mounts, races and platform-specific deletion semantics?
6. Does socket blocking provide useful regression evidence without overstating OS-level network isolation?
7. Which seccomp, namespace, mount and supply-chain controls are missing from the OCI path?
8. Which Nix lock, source-verification or binary-cache controls are required?
9. Which filename, size, hash-correlation, error-message or artifact-content privacy leaks remain?
10. Can any CLI, schema or documentation wording be misunderstood as proof of authorship, identity, authenticity, model source, legal status or forensic validity?

## Usability tasks

Without undocumented maintainer assistance:

1. install through one supported path;
2. run `cogniprint dossier limits`;
3. export a dossier from a private source and synthetic artifact;
4. confirm source bytes are absent;
5. transfer to a second installation and verify offline;
6. mutate one artifact byte and confirm failure;
7. run purge without confirmation and confirm no deletion;
8. confirm purge on a disposable prefixed staging directory;
9. explain what `VERIFIED` does and does not mean;
10. record confusing wording and unsafe affordances.

## Requested outcome

Choose one:

1. **SECURITY/USABILITY REVIEW SATISFIED** — no blocking changes for a later Ready-for-review decision; merge remains unauthorized.
2. **SATISFIED WITH REQUIRED CHANGES** — list exact blockers and acceptance tests.
3. **REMAIN DRAFT** — substantial revision is required.

## Reviewer record

- reviewer name:
- affiliation or relevant expertise:
- platform/environment:
- date:
- exact head reviewed:
- exact tree reviewed:
- technical evidence reviewed:
- outcome:
- blocking findings:
- non-blocking recommendations:
- residual risks accepted/rejected:
- conflicts or limitations:

## Decision rule

PR #57 remains Draft unless both are separately documented:

1. the exact current head/tree produces `EXACT_HEAD_M3_GATE=PASS` on a clean hosted runner; and
2. an independent human security/usability reviewer records an outcome.

Even when both are satisfied, merge, Stage B, freeze, Research Lock, external registration and scientific claims remain separate decisions.
