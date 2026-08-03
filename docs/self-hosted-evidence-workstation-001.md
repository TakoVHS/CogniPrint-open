# CogniPrint Self-Hosted Evidence Workstation — Technical Specification 001

Status: `DEVELOPMENT_ONLY`

Scientific boundary:

- `SCIENTIFIC_CLAIM_EVIDENCE=false`
- `CANONICAL_FREEZE=PRE-FREEZE`
- `EXTERNAL_REGISTRATION=NOT_SUBMITTED`
- `STAGE_B=NOT_AUTHORISED_TO_START`
- no authorship, identity, legal, forensic, psychological, intent or deterministic model-source claim

## 1. Product objective

Deliver a portable, local-first, self-hostable workflow that lets a user inspect sensitive text, compute deterministic descriptive evidence, preserve explicit uncertainty and export a dossier that another installation can verify independently.

The workstation is not a universal AI detector. It is an evidence and reproducibility layer with bounded claims, explicit failure states and no mandatory centralized inference service.

## 2. Primary users

1. Researchers comparing reproducible text measurements.
2. Administrators operating self-hosted infrastructure.
3. Journalists, civil-society practitioners and auditors handling sensitive documents.
4. Developers integrating bounded evidence checks into local workflows.

## 3. Non-goals

- Stage B execution or access.
- Canonical research freeze or Research Lock.
- Hidden model attribution presented as fact.
- Remote upload of source text by default.
- Vendor-specific hosted dependency.
- Automatic legal, disciplinary or forensic decisions.

## 4. Reference architecture

### 4.1 Local analysis service

- deterministic analysis API;
- loopback-only default binding;
- explicit offline mode;
- no telemetry by default;
- bounded resource controls;
- structured error and `UNKNOWN`/insufficient-evidence states.

### 4.2 Local user interface

- import or paste text locally;
- show source hash before analysis;
- display descriptive measurements and uncertainty;
- explain unsupported or insufficient-evidence outcomes;
- export and verify evidence dossiers.

### 4.3 Evidence dossier

Minimum manifest fields:

- dossier schema version;
- source content SHA-256;
- optional user-defined source label, never required;
- CogniPrint commit and package version;
- configuration hash;
- runtime and platform metadata;
- timestamp supplied by the local system and clearly marked as local;
- computed descriptive measurements;
- uncertainty and failure-state output;
- explicit claim boundary;
- artifact inventory with SHA-256 values.

Raw source text is excluded from the dossier by default. Inclusion requires a separate explicit option and warning.

### 4.4 Independent verifier

A second installation must be able to:

1. validate dossier schema;
2. recompute artifact hashes;
3. verify configuration and software identifiers;
4. optionally re-run analysis when the source text is supplied locally;
5. report exact match, mismatch or unverifiable state;
6. operate without contacting a CogniPrint server.

## 5. Packaging

### 5.1 Nix path

Target deliverables:

- `flake.nix` and lock file;
- reproducible CLI and local service packages;
- development shell;
- one-command smoke test;
- documented supported systems.

### 5.2 OCI path

Target deliverables:

- rootless-compatible OCI image;
- pinned base image digest;
- Docker/Podman Compose example;
- read-only container filesystem where practical;
- local bind mounts for input/output only;
- health and readiness checks;
- no privileged mode.

Nix is the reproducibility-first path. OCI is the accessibility fallback. Both must emit the same dossier schema and deterministic core results for the same pinned inputs.

## 6. Security and privacy requirements

- default network policy: no outbound application traffic;
- source text remains local;
- secrets are never stored in the dossier;
- explicit temporary-file lifecycle;
- path traversal and archive extraction protections;
- maximum input and archive sizes;
- safe JSON parsing with duplicate-key and non-finite-number rejection;
- full tracked-tree secret scan before release;
- threat model covering local attacker, malicious dossier and compromised dependency scenarios.

## 7. Milestones and acceptance criteria

### M1 — Reproducible self-hosted packaging

Deliverables:

- Nix flake;
- OCI image and Compose example;
- local CLI/service launch;
- installation documentation.

Acceptance:

- clean checkout builds on a fresh Linux environment;
- canary prints runtime and Python markers;
- identical deterministic probe output on two clean runs;
- service binds to loopback by default;
- no mandatory cloud credentials;
- Ruff, compile, tests, public-release check and secret scan pass.

### M2 — Portable dossier and verifier

Deliverables:

- versioned dossier schema;
- dossier exporter;
- independent verifier;
- fixtures for valid, corrupted and incomplete dossiers.

Acceptance:

- byte-identical dossier under pinned deterministic inputs, excluding explicitly declared local-time fields;
- every included artifact is hashed;
- source text is absent by default;
- one-byte mutation is detected;
- unknown schema and missing required fields fail closed;
- verifier runs offline on a separate clean installation.

### M3 — Privacy, security and usability hardening

Deliverables:

- threat model;
- privacy model;
- resource limits;
- deletion workflow;
- guided UI and operator documentation;
- demonstration script and short video plan.

Acceptance:

- no source-text network transmission in offline test;
- malicious dossier regression suite passes;
- temporary data deletion is documented and tested;
- accessibility and error-state review completed;
- demo reproduces install, analyze, export and verify without hidden steps.

## 8. Grant-facing evidence

For each milestone preserve:

- exact commit and tree;
- complete commands;
- runner logs;
- artifact SHA-256 manifest;
- screenshots or short video only as secondary evidence;
- known limitations and unresolved risks;
- no claim beyond the validated acceptance criteria.

## 9. Branch and integration policy

Development branch: `development/self-hosted-evidence-workstation-001`.

This work must remain separate from PR #54 and PR #50. It must not modify their validated branches, authorize Stage B, change `PRE-FREEZE`, create a Research Lock or claim scientific attribution evidence.

Any future pull request from this branch must start as Draft and remain independently reviewable from the scientific-method PRs.
