# CogniPrint current state

CogniPrint is an MIT-licensed research framework for constructing compact statistical fingerprints of text and building reproducible evidence about synthetic-language production processes without collapsing measurement, inference, external provenance, and uncertainty into one verdict.

## Current scientific status

- Scientific readiness: `descriptive_only`
- Research mode: `PROOF_MODE`
- Challenge 001 Stage B: `NOT_AUTHORISED_TO_START`
- CI evidence status: `NOT_EXECUTED`
- Local exact-snapshot execution: `NOT_EXECUTED`
- External methodological reviews: `0/1`
- Release line: `v0.1.2`
- DOI: `10.5281/zenodo.20756421`
- Repository: https://github.com/TakoVHS/CogniPrint-open

The DOI is citation/administrative metadata only and does not change scientific readiness or validate any stronger claim.

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
- eight golden mathematical evaluator fixtures covering perfect, all-wrong, missing-class, all-unknown, known-as-unknown, unknown-as-known, single-class and imbalanced behavior;
- a canonical public trust/claim-unlock contract at `docs/trust.md`.

These are evidence/research controls. They do **not** make current attribution scientifically validated.

## Implemented Challenge 001 integrity controls

Challenge 001 now has explicit pre-freeze controls:

- physically separated namespaces for Stage A development, frozen protocol artifacts and sealed Stage B evaluation;
- a blinded-sample schema that forbids direct ground-truth/model-family fields;
- a separate revealed-label schema for post-prediction label reveal;
- schema-enforced Stage A/Stage B visibility and reference-membership invariants;
- a **Development Exposure Registry** that quarantines already inspected/used corpora from sealed Stage B;
- `public-benchmark-v1.1` and the already specified RAID `raid/train` Pilot A matrix are development-visible and cannot later be represented as sealed Stage B evidence;
- a Stage A public-benchmark materializer that hashes already released files into development-only blinded manifest records;
- a machine-readable leakage audit that blocks freeze on sample/content overlap or duplicate identifiers/content hashes;
- **Research Lock 001** tooling that can bind the exact frozen protocol/evaluator/config/manifests/reference files to one deterministic SHA-256.

The Research Lock is an integrity binding, **not** a digital signature or scientific-validity certificate. Its final file set and final hash do not exist yet because the protocol remains `PRE-FREEZE`.

No real Stage A manifest, real A/B leakage report, frozen Research Lock, sealed Stage B corpus, or Challenge 001 result is currently claimed.

## Proof mode / feature freeze

CogniPrint is under a **no-new-feature rule until Evidence Milestone 001 / Challenge 001**.

Allowed work is limited to:

1. correctness/security fixes;
2. reproducibility;
3. test/runner infrastructure;
4. Stage A development calibration needed to finalise the pre-registered protocol;
5. preregistration and research-freeze work;
6. benchmark integrity/sealing;
7. corrections needed to keep public claims aligned with evidence.

New detector families, new headline capabilities, decorative dashboards and additional regulatory/provenance integrations are deferred unless they are required to repair correctness or reproducibility.

The pre-freeze contract is `RESEARCH_FREEZE_001.md`. It is intentionally marked `PRE-FREEZE` until Stage A has fixed the remaining numerical/operational choices and exact model/source families, corpus/reference versions, sample strata, minimum-evidence rules, OOD/calibration methods, exclusions, thresholds and external preregistration are fixed.

## CI / execution evidence status

GitHub Actions CI: **`NOT_EXECUTED`**.

A minimal Runner Canary with no checkout, dependencies, cache, matrix or secrets was created specifically to isolate runner startup. Its job was created, but GitHub reported `steps: []`; neither the shell canary nor `python --version` executed. A control rerun after GitHub reported Actions operational produced the same `steps: []` result.

Therefore this is not evidence that tests passed or failed.

Correct public wording:

> CI execution: NOT_EXECUTED — GitHub-hosted runner did not reach the first executable step.

Local exact-snapshot execution is also **`NOT_EXECUTED`** in the current execution environment because that environment could not resolve/fetch `github.com`; it therefore could not obtain an exact repository snapshot for the requested Python 3.10/3.11/3.12 matrix.

Issue #30 closes only after the trust/evaluator tests actually execute on a functioning runner and the exact commit, Python versions, job logs and test counts are preserved.

## Stage A — development calibration

Stage A is **development-only** and is not blind Challenge 001 evidence.

It exists to fix pre-freeze choices such as:

- minimum-evidence / length bins;
- source-family feasibility;
- OOD/UNKNOWN methodology;
- calibration procedure and binning;
- feature stability;
- sample-count/strata feasibility;
- exclusion mechanics;
- evaluator sanity.

Anything used for these choices becomes development-visible. It may not later be relabelled as sealed Stage B simply because a particular script did not consume every record.

Before freeze, the real candidate Stage A and Stage B manifests must pass the leakage gate with at least:

```text
sample_id_overlap = 0
content_hash_overlap = 0
```

Prompt overlap is reported separately and its policy must be frozen before Stage B.

## External-provenance / regulatory interfaces

Documented interfaces include:

- C2PA / Content Credentials bridge contract and validation-state model;
- Article-50-oriented transparency evidence mapping that explicitly does **not** claim EU AI Act compliance or certification;
- NIST AI RMF / Generative AI Profile mapping that explicitly does **not** claim NIST certification/approval.

The C2PA runtime reader/validator is not yet implemented or validated.

## Flagship research target — Attribution Challenge 001

Stage B is currently **not authorised to start**.

The required order is:

1. obtain real execution evidence on a functioning runner;
2. execute Stage A development calibration without using future Stage B samples;
3. materialise Stage A and candidate Stage B manifests and obtain a leakage-audit PASS;
4. complete and freeze `RESEARCH_FREEZE_001.md`;
5. create/preserve the final Research Lock 001 hash;
6. complete external timestamped preregistration (issue #28);
7. seal corpus/reference/split artifacts and keep ground truth unavailable to prediction code;
8. generate and hash frozen predictions before label reveal;
9. reveal labels and evaluate with the independent evaluator without post-reveal fitting/tuning;
10. publish failure analysis and a separate Scientific Claim Review.

The frozen-design direction includes:

- leakage-safe lineage grouping;
- transparent length/surface/n-gram baselines;
- held-out unseen generators;
- `UNKNOWN / OUT_OF_DISTRIBUTION / INSUFFICIENT EVIDENCE`;
- Brier/ECE and selective-risk reporting where calibrated outputs exist;
- false-known rate as a first-class open-world safety metric;
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
- CI execution: `NOT_EXECUTED` — issue #30;
- local exact-snapshot execution: `NOT_EXECUTED` in the current environment;
- real Stage A manifest/calibration outputs: not yet executed;
- real A/B leakage audit: not yet executed;
- Challenge 001 research freeze: `PRE-FREEZE`;
- final Research Lock 001: not yet generated;
- Challenge 001 external preregistration: open issue #28;
- C2PA runtime validation: open issue #26;
- real detached `.cogcase` signatures: open issue #27;
- QVAC runtime demo remains HOLD;
- Auto Drive CID upload/retrieval round-trip remains HOLD;
- OTF practitioner discovery remains NO-GO until real user evidence exists.

## Positioning

CogniPrint should be understood as an **evidence-first cognitive-provenance research programme**. Its moat is not a headline AI score; it is the attempt to make every conclusion state whether it is observed, inferred, externally attested, or unknown — with reproducibility, scope and failure conditions preserved alongside the result.
