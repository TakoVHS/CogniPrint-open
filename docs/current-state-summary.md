# CogniPrint current state

CogniPrint is an MIT-licensed research framework for constructing compact statistical fingerprints of text and building reproducible evidence about synthetic-language production processes without collapsing measurement, inference, external provenance, and uncertainty into one verdict.

## Current scientific status

- Scientific readiness: `descriptive_only`
- Research mode: `PROOF_MODE`
- Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`
- CI evidence status: `NOT_EXECUTED`
- External methodological reviews: `0/1`
- Release line: `v0.1.2`
- DOI: pending direct public Zenodo verification
- Repository: https://github.com/TakoVHS/CogniPrint-open

The current public release supports reproducible **measurement and evidence structuring**, not validated source attribution.

## Implemented measurement core

CogniPrint currently provides:

- a documented 12-dimensional text profile `φ(T)`;
- profile comparison with Euclidean distance and cosine similarity;
- corpus-relative exploratory thresholds/diagnostics;
- perturbation analysis for measuring profile change under edits;
- corpus aggregation and dispersion summaries;
- entropy and word/character n-gram diagnostics;
- reproducibility, validation, benchmark, and evidence artifacts.

## Implemented trust/evidence foundation

The repository contains implementation-level primitives for the next research layer:

- **Evidence Schema v1** with four explicit truth classes: `OBSERVED`, `INFERRED`, `ATTESTED`, `UNKNOWN`;
- **Claim Firewall v1** that keeps model-family attribution disabled by default until minimum-evidence, in-distribution, calibration and explicit research gates are satisfied;
- exact-model identity is not inferred from prose; under the current policy it may only be represented as a validated external `ATTESTED` statement;
- authorship, actor/commissioner, intent/responsibility and legal/forensic conclusions remain blocked as content-only claims;
- machine-readable limitations such as `SHORT_TEXT`, `OUT_OF_DISTRIBUTION`, `UNCALIBRATED_SCORE`, `NO_EXTERNAL_PROVENANCE`, `CONFLICTING_PROVENANCE` and `UNSUPPORTED_CLAIM`;
- **Provenance Conflict Engine** that preserves disagreement between authorised statistical inference and validated external provenance rather than silently choosing one source as truth;
- deterministic `.cogcase` manifest/integrity primitives with SHA-256, file-set validation and tamper detection;
- `.cogcase` signing is **not implemented**: v0.1 accepts only `UNSIGNED` and rejects a fake signed status;
- Data Constitution for licensing, PII minimisation, benchmark contamination, lineage and reference-registry governance;
- evaluation contracts for calibration, OOD, generator/temporal/domain/language holdouts, human-edit survival and model-to-model rewrite tests;
- an independent sealed-challenge evaluator that is separate from fitting/threshold tuning and binds prediction/label artifacts by SHA-256;
- a canonical public trust/claim-unlock contract at `docs/trust.md`.

These are evidence/research controls. They do **not** make current attribution scientifically validated.

## Proof mode / feature freeze

CogniPrint is now under a **no-new-feature rule until Evidence Milestone 001 / Challenge 001**.

Allowed work is limited to:

1. correctness/security fixes;
2. reproducibility;
3. test/runner infrastructure;
4. preregistration and research-freeze work;
5. benchmark integrity/sealing;
6. corrections needed to keep public claims aligned with evidence.

New detector families, new headline capabilities, decorative dashboards and additional regulatory/provenance integrations are deferred unless they are required to repair correctness or reproducibility.

The pre-freeze contract is `RESEARCH_FREEZE_001.md`. It is intentionally marked `PRE-FREEZE` until exact model/source families, corpus/reference versions, sample strata, minimum-evidence rules, OOD/calibration methods, exclusions, thresholds and external preregistration are fixed.

## CI evidence status

Current status: **`NOT_EXECUTED`**.

Recent GitHub Actions jobs were created but reached no executable steps (`steps: []`), so checkout and test commands did not run. This is not evidence that tests passed or failed.

Correct public wording:

> CI evidence status: NOT_EXECUTED — runner failed before checkout.

Issue #30 closes only after the trust/evaluator tests actually execute on a functioning runner and the commit, Python versions, job logs and test counts are preserved.

## External-provenance / regulatory interfaces

Documented interfaces include:

- C2PA / Content Credentials bridge contract and validation-state model;
- Article-50-oriented transparency evidence mapping that explicitly does **not** claim EU AI Act compliance or certification;
- NIST AI RMF / Generative AI Profile mapping that explicitly does **not** claim NIST certification/approval.

The C2PA runtime reader/validator is not yet implemented or validated.

## Flagship research target — Attribution Challenge 001

Stage B is currently **not authorised to start**.

Before sealed evaluation the project must:

1. complete and freeze `RESEARCH_FREEZE_001.md`;
2. preserve the exact protocol/commit hashes;
3. complete external timestamped preregistration (issue #28);
4. establish actual runtime test evidence (issue #30 or equivalent reproducible runner record);
5. freeze corpus/reference/split artifacts;
6. keep sealed ground truth unavailable to the prediction process;
7. generate/freeze predictions before label reveal;
8. evaluate with the independent evaluator without post-reveal fitting/tuning;
9. publish failure analysis with the result.

The frozen-design direction includes:

- leakage-safe lineage grouping;
- transparent length/surface/n-gram baselines;
- held-out unseen generators;
- `UNKNOWN / OUT_OF_DISTRIBUTION / INSUFFICIENT EVIDENCE`;
- Brier/ECE and selective-risk reporting where calibrated outputs exist;
- domain/temporal/generalisation checks;
- translation, human-edit and model-to-model rewrite stress tracks;
- explicit falsification criteria and public failure reporting;
- independent post-reveal evaluation.

No Challenge 001 result is currently claimed.

## Evidence Milestone 001

Evidence Milestone 001 is reached only when all of these exist together:

- timestamped preregistration;
- actually executed reproducible test suite;
- frozen/sealed blind benchmark;
- frozen predictions and SHA-256;
- revealed labels and SHA-256 after prediction freeze;
- independent evaluator output;
- calibration metrics where calibrated outputs are claimed;
- OOD/UNKNOWN metrics including false-known rate;
- published failure analysis;
- immutable integrity-verifiable evidence bundle;
- external methodological review requested against the actual results.

Reaching the milestone does **not** automatically change `descriptive_only`. A separate Scientific Claim Review must classify each proposed public claim as `ALLOW`, `ALLOW_WITH_SCOPE`, `REJECT`, or `REQUIRES_MORE_EVIDENCE`.

## What the research is trying to reach

The longer programme remains evidence-gated:

1. **Model-family candidates:** benchmark-bounded probabilistic source-family inference with UNKNOWN/OOD.
2. **Human–AI intervention mapping:** controlled regime-change/segment research without converting change points into authorship claims.
3. **Cross-model generation lineage:** controlled multi-stage production-chain research only after lower-level gates succeed.
4. **Provenance fusion:** combine content-derived measurements with C2PA/provider/log/revision attestations while preserving evidence class and conflict state.
5. **Portable evidence cases:** reproducible, eventually signed `.cogcase` artifacts after a real cryptographic signing implementation is reviewed.

## Critical boundary

CogniPrint does **not** currently establish from text alone:

- a unique author;
- a unique/exact source model;
- definitive AI origin;
- generation-lineage reconstruction;
- who commissioned or requested generation;
- intent or responsibility;
- legal status;
- forensic provenance suitable for high-stakes decisions.

Content-derived signals can support bounded hypotheses. Claims about actors, tools, workflow history or legal effect require independent evidence appropriate to the specific claim.

## Open gates

- external methodological review: `0/1`;
- DOI reference not directly publicly verified;
- CI evidence status: `NOT_EXECUTED` — issue #30;
- Challenge 001 research freeze: `PRE-FREEZE`;
- Challenge 001 external preregistration: open issue #28;
- C2PA runtime validation: open issue #26;
- real detached `.cogcase` signatures: open issue #27;
- QVAC runtime demo remains HOLD;
- Auto Drive CID upload/retrieval round-trip remains HOLD;
- OTF practitioner discovery remains NO-GO until real user evidence exists.

## Positioning

CogniPrint should be understood as an **evidence-first cognitive-provenance research programme**. Its moat is not a headline AI score; it is the attempt to make every conclusion state whether it is observed, inferred, externally attested, or unknown — with reproducibility, scope and failure conditions preserved alongside the result.
