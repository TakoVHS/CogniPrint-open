# CogniPrint 10× Readiness Program 001

Status: `ACTIVE / GATE_BASED / NO_AUTOMATIC_CLAIM_UNLOCK`

## Purpose

This programme defines what "10/10" means for CogniPrint in measurable terms. It is not a marketing score. A category is complete only when its evidence is preserved on an exact repository state and an independent reviewer can inspect it.

The target is a credible, local-first evidence workstation and research programme that is:

- useful without overstating attribution capability;
- reproducible on clean systems;
- private by default;
- secure against malformed evidence packages;
- transparent about failure and uncertainty;
- independently reviewable;
- fundable as concrete engineering and research work.

## Canonical boundary

Until the scientific gates explicitly change:

```text
READINESS=descriptive_only
RESEARCH_MODE=PROOF_MODE
CANONICAL_FREEZE=PRE-FREEZE
EXTERNAL_REGISTRATION=NOT_SUBMITTED
STAGE_B=NOT_AUTHORISED_TO_START
EXTERNAL_METHODOLOGICAL_REVIEW=0/1
```

Product and security progress must not be converted into a model-attribution claim.

## Gate A — Reproducible local product

Completion requires:

- one-command documented installation for a supported Linux target;
- Nix flake build from a clean machine;
- rootless OCI image build and execution;
- repeat build comparison with documented expected differences;
- offline operation with outbound sockets blocked;
- main CLI, quickstart, evidence creation, verification, and safe purge;
- independent producer and verifier installations;
- versioned migration policy for dossier schemas;
- release artifacts with SHA-256 checksums;
- SBOM for packaged software;
- source commit, builder, dependencies, and artifact identity recorded.

Current state:

- application and rootless OCI portions have hosted evidence in Draft PR #57;
- Nix exact-head gate and independent human security/usability review remain open;
- no production-readiness claim is authorised.

## Gate B — Security and privacy

Completion requires:

- repository security policy and private reporting route;
- threat model covering text leakage, archive/path attacks, verification confusion, network violations, supply-chain compromise, resource exhaustion, claim escalation, and Stage B contamination;
- source-text canary tests across logs, exceptions, reports, temporary files, and exports;
- archive traversal, duplicate path, symlink, file-count, and decompression-limit tests;
- CPU, memory, disk, recursion, record-count, and report-size limits;
- socket-blocked offline integration test;
- dependency inventory, update policy, and licence audit;
- secret scan over the complete tracked tree and release candidate;
- independent human security review with findings tracked to closure or explicit residual risk;
- no high or critical unresolved vulnerability in the release target.

## Gate C — Supply-chain integrity

Completion requires:

- automated dependency update visibility;
- pinned or immutable security-sensitive CI actions where supported;
- reproducible or independently comparable builds;
- SPDX-compatible SBOM;
- SLSA-style provenance for release artifacts;
- artifact checksums published separately from the artifact being checked;
- documented signing and trust model before any artifact is called signed;
- keyless or managed-key release signature verification tested from a clean environment;
- OpenSSF Scorecard review and tracked remediation of high-impact findings;
- dependency compromise and malicious-update response procedure.

A checksum alone is integrity metadata, not signer identity or build provenance.

## Gate D — Scientific validity

Completion requires:

- Stage A methods on a frozen exact head;
- transparent length, surface, character n-gram, and word n-gram baselines;
- lineage-safe partitions and real overlap audits;
- explicit held-out unknown families;
- conformal or otherwise predeclared abstention method with finite-sample feasibility checks;
- probability calibration on a separate partition;
- Wilson or other suitable intervals for rate claims;
- paired lineage-group uncertainty for method comparisons;
- prospective claim-narrowing rules;
- model, dataset, licence, version, and access review;
- independent human methodological critique and tracked corrections;
- canonical freeze, Research Lock, and independently timestamped preregistration;
- sealed predictions before label reveal;
- independent evaluation with failures published next to positive results;
- no attribution claim unless it exceeds transparent baselines under the frozen acceptance rules.

Current Stage A evidence showing n-gram baselines outperforming the 12D representation is a valid negative result and must remain public.

## Gate E — Evidence semantics and provenance

Completion requires:

- every report field mapped to `OBSERVED`, `INFERRED`, `ATTESTED`, or `UNKNOWN`;
- machine-readable limitations and claim firewall;
- integrity, signature validity, signer identity/trust, and scientific meaning represented separately;
- dossier schema validation and mutation rejection;
- source/config/software/reference hashes preserved;
- C2PA runtime bridge tested with valid, invalid, absent, unsupported, and conflicting fixtures;
- signed `.cogcase` or successor format only after real detached signature verification exists;
- no arbitrary credential or personal metadata copied into public evidence by default;
- report wording that exposes alternatives and residual uncertainty.

## Gate F — Product usefulness

Completion requires at least three complete operator journeys:

1. local analyst creates a privacy-preserving dossier and verifies it on a second machine;
2. researcher runs a development-visible benchmark and produces a reproducible evidence packet;
3. reviewer inspects hashes, methods, limitations, failures, and exact reproduction commands without trusting a hosted CogniPrint service.

Each journey must include:

- a five-minute quickstart;
- sample data that is synthetic or clearly licensed;
- expected outputs and failure examples;
- recovery and purge steps;
- accessibility and plain-language explanation;
- no forced account, cloud service, or remote upload.

## Gate G — Governance and external trust

Completion requires:

- contribution contract;
- security policy;
- ownership rules for research, release, configuration, and security paths;
- changelog and migration policy;
- release checklist;
- independent methodological review;
- independent security/usability review;
- DOI and public archive independently resolvable;
- funding and reviewer materials aligned with the exact public state;
- no grant or website statement stronger than repository evidence;
- public record of material disagreements, negative findings, and unresolved risks.

## Priority execution order

### P0 — unblock exact evidence

- finish the PR #57 Nix exact-head gate;
- obtain the PR #57 security/usability review;
- obtain the PR #54 independent methodological review;
- resolve GitHub Actions runner execution or document a stable equivalent-runner policy;
- keep PR #50, #54, #56, and #57 isolated until their own gates are satisfied.

### P1 — release and supply-chain hardening

- add SBOM generation and validation;
- add release checksums and provenance statement;
- design artifact signing with explicit signer trust semantics;
- run OpenSSF Scorecard and create remediation issues;
- add adversarial archive, leakage-canary, and resource-limit suites;
- define supported-platform and vulnerability-fix policy.

### P2 — evidence workstation beta

- merge only reviewed self-hosted components;
- publish a versioned beta dossier schema;
- provide a deterministic end-to-end demonstration;
- test fresh installation by an external operator;
- publish a failure-and-limitations report for the beta.

### P3 — scientific freeze preparation

- resolve the four methodological hardening findings recorded for PR #54;
- complete human-control and model-revision provenance review;
- materialise candidate Stage A and blinded Stage B manifests;
- execute the real zero-overlap leakage audit;
- freeze the exact protocol only after independent review;
- create the final Research Lock and preregistration packet.

### P4 — sealed Challenge 001

- execute frozen predictions without labels;
- preserve prediction receipt and hash;
- reveal labels through the custody process;
- run the independent evaluator;
- publish positive, mixed, negative, and insufficient-evidence outcomes;
- conduct a separate scientific claim review.

## Definition of 10/10

CogniPrint reaches the programme's 10/10 threshold only when:

- every Gate A–G requirement is either passed with inspectable evidence or explicitly scoped out with a justified residual-risk statement;
- no critical gate depends only on the project owner's assertion;
- exact release artifacts can be independently installed, verified, and traced to source;
- scientific claims remain no stronger than the sealed evidence;
- a failure, unknown, or negative result remains an acceptable published outcome.

The programme does not promise that CogniPrint will identify a unique model or author. It promises that the project will become substantially more trustworthy, reproducible, useful, and difficult to misuse.
