# CogniPrint Threat Model 001

Status: `DEVELOPMENT / REVIEW_REQUIRED`

This document defines the minimum security and misuse model for CogniPrint, the Self-Hosted Evidence Workstation, evidence dossiers, research manifests, and future provenance integrations.

## Security objectives

CogniPrint should preserve:

- confidentiality of source text and unpublished research material;
- integrity of fingerprints, dossiers, manifests, hashes, configuration, and software identity;
- reproducibility of bounded analytical results;
- separation between observed measurements, inference, attestation, and unknown states;
- availability under malformed but reasonably bounded inputs;
- honest failure when verification, calibration, evidence, or provenance is insufficient.

## Protected assets

- source documents and temporary working copies;
- content hashes and lineage identifiers;
- evidence dossiers and case manifests;
- frozen protocols, thresholds, seeds, and configuration;
- sealed Stage B labels and custody records;
- signing keys and public trust configuration;
- build artifacts, container images, packages, and dependency metadata;
- reviewer packets and unpublished vulnerability reports;
- project credentials and deployment secrets.

## Trust boundaries

### Local operator boundary

The operator controls the host, input files, output location, and optional network access. CogniPrint must not assume that all local files are benign.

### Input boundary

Text files, dossiers, archives, manifests, schemas, and configuration may be malformed, oversized, recursive, adversarial, or intentionally ambiguous.

### Dependency and build boundary

Python packages, GitHub Actions, container bases, Nix inputs, external CLIs, and installer scripts are third-party code. Version constraints alone are not proof of integrity.

### Provenance boundary

Authenticated provenance and content-derived inference are different evidence classes. A valid signature does not prove that every assertion is true; an invalid or absent signature does not prove that content is false.

### Research custody boundary

Stage A material, predictor-visible Stage B inputs, sealed labels, and post-reveal evaluation artifacts require separate access roles and storage boundaries.

## Adversaries and failure sources

- a malicious dossier author attempting verifier bypass;
- a local user supplying crafted paths, symlinks, archives, encodings, or extremely large inputs;
- a compromised dependency, action, package index, container base, or build environment;
- an insider or accidental operator exposing sealed labels or private text;
- a contributor overstating scientific meaning or bypassing claim controls;
- a reviewer or downstream consumer confusing integrity with authenticity, identity, or legal proof;
- an attacker attempting resource exhaustion or repeated malformed-input failures;
- ordinary implementation defects, stale documentation, version drift, and incomplete migrations.

## Priority threat scenarios

### T1 — Source-text leakage

Private text appears in logs, exceptions, evidence exports, tests, telemetry, crash dumps, temporary files, or public-release artifacts.

Required controls:

- metadata-only output by default;
- explicit raw-text opt-in where ever permitted;
- redaction tests using unique canary strings;
- temporary-data inventory and purge verification;
- no secret or source snippets in exception messages;
- public-release and full-tree secret scans.

### T2 — Path and archive attacks

A crafted dossier or archive writes outside the intended directory, follows symlinks, replaces files, or triggers unsafe extraction.

Required controls:

- reject absolute paths, parent traversal, duplicate paths, and symlinks;
- extract only into a new confined directory;
- reject device files and unsupported entry types;
- enforce file-count, per-file, and total-size limits;
- verify before materialising trusted outputs.

### T3 — Verification confusion

A malformed dossier is accepted because unknown schemas, missing fields, duplicate JSON keys, non-finite numbers, canonicalisation differences, or ambiguous hashes are tolerated.

Required controls:

- fail closed on unknown required schema versions;
- reject duplicate keys and non-finite values;
- define canonical byte representation explicitly;
- verify all declared files and reject unexpected files when the format requires a closed set;
- separate `INTEGRITY_VALID`, `SIGNATURE_VALID`, and `SIGNER_TRUST`.

### T4 — Offline-contract violation

The application performs DNS, telemetry, package retrieval, model download, update checks, or remote inference while described as offline.

Required controls:

- socket-blocked test execution;
- explicit network mode and dependency prefetch documentation;
- no silent fallback from local to hosted processing;
- observable error when a requested remote component is unavailable.

### T5 — Supply-chain compromise

A dependency, GitHub Action, container image, or build input changes unexpectedly or is replaced by a malicious artifact.

Required controls:

- automated dependency review and update visibility;
- pin security-sensitive Actions and immutable build inputs where practical;
- generate SBOM and checksums for releases;
- sign release artifacts only after a documented key and trust model exists;
- preserve builder, source commit, dependency, and artifact identities;
- prefer hermetic or reproducible builds and compare independent outputs.

### T6 — Scientific claim escalation

Code output, UI wording, or documentation turns a descriptive measurement into author, model, intent, responsibility, legal, or forensic attribution without sufficient evidence.

Required controls:

- machine-readable claim firewall;
- mandatory evidence class and limitation codes;
- `UNKNOWN / OOD / INSUFFICIENT_EVIDENCE` paths;
- claim-narrowing rules linked to observed metrics;
- human methodological review before defined readiness transitions;
- regression tests for prohibited outputs and wording.

### T7 — Stage B contamination

Prediction code, developers, or tuning processes gain access to sealed labels or overlapping samples before prediction freeze.

Required controls:

- separate custodians, paths, credentials, and manifests;
- zero sample/content overlap gate;
- prediction receipt before label reveal;
- immutable hashes and access records;
- automatic downgrade to development evidence after any blinding failure.

### T8 — Resource exhaustion

A small input causes extreme CPU, memory, disk, recursion, archive expansion, or report size.

Required controls:

- explicit limits and timeouts;
- streaming where feasible;
- bounded token, file, record, and matrix sizes;
- adversarial size tests;
- partial-output cleanup after failure.

## Misuse cases

CogniPrint must not be presented as a tool for making automatic high-stakes decisions about students, employees, migrants, defendants, authors, or political speakers. It must not convert uncertain text evidence into identity, guilt, plagiarism, intent, or responsibility claims.

Interfaces and reports should show:

- what was measured;
- which reference and version were used;
- what evidence class applies;
- what limitations fired;
- which alternatives remain;
- whether the result is insufficient for the requested conclusion.

## Security verification gates

A production-readiness claim requires all of the following on an exact source state:

- clean installation from documented inputs;
- unit, integration, mutation, malformed-input, and resource-limit tests;
- socket-blocked offline test;
- source-text canary leakage test;
- archive/path/symlink adversarial suite;
- dependency and licence inventory;
- SBOM and artifact checksums;
- rootless container execution;
- independent verifier installation;
- documented vulnerability reporting path;
- independent human security review with tracked findings.

## Residual risks

Even after these controls, CogniPrint cannot guarantee that:

- a local host is uncompromised;
- third-party attestations are truthful;
- a signed artifact was produced by a trustworthy process;
- statistical similarity identifies a unique source;
- all future adversarial transformations are detected;
- reproducibility implies scientific validity.

Residual risks must remain visible in reports and release notes.
