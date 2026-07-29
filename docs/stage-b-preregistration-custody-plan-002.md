# Challenge 001 — External Preregistration and Sealed Stage B Custody Plan 002

Status: **HOLD / SUBMISSION-READY STRUCTURE ONLY / STAGE B NOT AUTHORISED**

Purpose: define the exact operational package required to create an independently timestamped preregistration and a genuinely sealed Stage B evaluation without selecting data after results are visible, without exposing ground truth to the prediction process, and without expanding current public claims.

This document does **not** freeze Challenge 001, submit a registration, create Stage B data, reveal any source-family labels, or authorize predictions.

## 1. Current canonical state

- scientific readiness: `descriptive_only`;
- research mode: `PROOF_MODE`;
- research state: `PRE-FREEZE`;
- Stage B: `NOT_AUTHORISED_TO_START`;
- completed development evidence: Stage A public benchmark materialization, RAID Pilot A, and privacy-preserving character/word n-gram comparisons;
- current Stage A finding: both tested n-gram baselines outperformed the compact CogniPrint 12D representation on the fixed RAID Pilot A;
- interpretation: 12D remains a compact, interpretable signal, but it is not the strongest tested classifier;
- external preregistration: `NOT_SUBMITTED`;
- final Research Lock 001: `NOT_CREATED`;
- candidate sealed Stage B manifest: `NOT_CREATED`;
- sealed labels: `NOT_CREATED`;
- hosted-runner gate: issue #30 remains open and must not be called PASS.

The Stage A result narrows, rather than expands, the Stage B question. The preregistered primary analysis must compare CogniPrint against transparent baselines and must allow the result that CogniPrint does not outperform them.

## 2. External registration target

Preferred external mechanism: an OSF Registration/Preregistration suitable for a prospective empirical benchmark.

The final submission decision must be deliberate:

### Public immediately

Use only when publication of the exact frozen source-family design, holdout policy, and custody description does not weaken the blind evaluation.

Advantages:

- public timestamp and immutable registration record;
- public discoverability;
- DOI availability for a public registration.

### Embargoed registration

Use when disclosure of exact held-out-family identities, source-selection details, or custody metadata would materially weaken the blind design before prediction freeze.

Requirements:

- embargo is selected at submission, not after results;
- embargo end rule is fixed before submission;
- an anonymized view-only link is provided to an independent reviewer/custodian where appropriate;
- embargo must never be used to hide an incomplete protocol or an unfavorable result;
- the registration is made public no later than the preregistered reveal/publication event unless an external legal/licensing restriction requires a separately disclosed delay.

The final public-versus-embargo decision remains `TO BE FROZEN`. No registration may be submitted while `RESEARCH_FREEZE_001.md` is `PRE-FREEZE`.

## 3. Registration packet boundary

The external registration packet must contain or bind by SHA-256 the following frozen control artifacts:

1. `RESEARCH_FREEZE_001.md`;
2. `docs/attribution-challenge-001.md`;
3. `docs/preregistration-challenge-001-draft.md` after all placeholders are resolved;
4. this custody plan or its final frozen successor;
5. the exact repository commit and tree SHA;
6. the exact independent evaluator commit/hash;
7. the final Research Lock 001 file list and Research Lock Hash;
8. the Stage A development-manifest hash;
9. the development-exposure registry hash;
10. the candidate blinded Stage B manifest hash;
11. the split/reference/calibration manifest hashes;
12. the environment/dependency lock hash;
13. the frozen source-selection algorithm and seed, where randomness is used;
14. the frozen inclusion/exclusion, minimum-evidence, OOD/UNKNOWN, calibration, metric, and stop/claim-narrowing rules;
15. the custody record hash.

The external registration packet must **not** contain:

- sealed per-sample ground-truth labels;
- label-bearing filenames or paths;
- secrets, access tokens, encryption keys, recovery phrases, or private storage credentials;
- raw source text that licensing or privacy rules prohibit from publication;
- per-sample label hashes that make a small label space brute-forceable;
- any claim that the evidence bundle is digitally signed while issue #27 remains open.

A whole-file sealed-label SHA-256 may be preserved by the custodian as an integrity identifier. Whether it is included in the public registration or retained in a private custodian receipt must be frozen before registration based on leakage risk. Hashing is not a secrecy mechanism.

## 4. Logical roles

The freeze must name four logical roles. One person may administratively occupy more than one role only when the technical access controls still preserve separation and the overlap is disclosed.

### Protocol owner

May:

- prepare the preregistration draft;
- freeze scientific decisions before Stage B;
- preserve repository and protocol hashes.

Must not:

- alter frozen scientific rules after seeing Stage B predictions or labels;
- choose samples because they produce favorable outcomes.

### Corpus and label custodian

May:

- construct or receive the dedicated corpus under the frozen selection procedure;
- create the blinded package and sealed ground-truth package;
- preserve label-artifact bytes and integrity hashes;
- release labels only after receiving a valid prediction-freeze receipt.

Must not:

- tune features, thresholds, calibration, OOD logic, exclusions, or public examples against sealed labels;
- modify labels in response to predictions;
- reveal source-family metadata before prediction freeze.

### Prediction operator/process

May access only:

- frozen software and configuration;
- permitted reference/calibration artifacts;
- blinded Stage B inputs;
- public preregistration metadata that the frozen design allows it to know.

Must not access:

- sealed labels;
- hidden source-family metadata;
- custodian-only selection mappings;
- label-bearing provider paths;
- keys or locations that provide indirect access to ground truth.

### Independent evaluator/reviewer

May:

- verify the preregistration, Research Lock, custody receipts, prediction freeze, and reveal sequence;
- run or review the independent evaluator after reveal;
- confirm that deviations are reported.

Must not:

- provide post-hoc tuning advice based on sealed labels before the primary evaluation is frozen.

## 5. Required artifacts

### A. Public/frozen control package

Contains protocol, schemas, exact versions, source-selection rules, hashes, and the Research Lock. It contains no sealed labels.

### B. Blinded Stage B package

Conforms to `schemas/challenge-001-blinded-sample-v1.schema.json` and contains only predictor-visible fields. It must pass an explicit label-leakage audit before prediction execution.

### C. Sealed ground-truth package

Conforms to `schemas/challenge-001-revealed-label-v1.schema.json`. It is held separately and is not mounted, copied, committed, indexed, or exposed to the prediction process before prediction freeze.

### D. Custody record

Records role IDs, artifact hashes, access boundaries, creation timestamps, storage class, reveal authorization, and every custody transition. Public copies must use non-sensitive opaque identifiers rather than secret paths or credentials.

### E. Prediction-freeze receipt

Created before label reveal and records:

- `predictions.jsonl` SHA-256;
- prediction count and sample-ID set hash;
- exact repository/evaluator commit SHA;
- Research Lock Hash;
- configuration and environment hashes;
- UTC timestamp;
- repository dirty status;
- confirmation that sealed labels were unavailable.

### F. Reveal receipt

Created by the custodian after validating the prediction-freeze receipt. It records:

- original sealed-label artifact SHA-256;
- verification that label bytes were unchanged;
- reveal UTC timestamp;
- recipient/evaluator role ID;
- prediction-freeze receipt hash;
- any custody anomaly.

### G. Evaluation receipt

Records the immutable prediction hash, revealed-label hash, evaluator hash, result hash, and the preregistered deviation status.

## 6. No post-result selection rule

Before any sealed prediction is produced, the frozen protocol must define:

- exact source/model families and human controls;
- held-out unknown-family policy;
- source collection/generation window;
- sample counts and strata;
- deterministic selection procedure and seed where applicable;
- prompt/task/domain/language/length strata;
- lineage grouping and duplicate rules;
- transformations designated primary versus exploratory;
- inclusion and exclusion rules;
- reference/calibration membership;
- minimum-evidence policy;
- OOD/UNKNOWN and calibration procedures;
- baseline implementations;
- metrics and zero-division semantics;
- numeric stop and claim-narrowing criteria.

The following are prohibited:

- replacing difficult samples after viewing predictions;
- changing source-family balance because early metrics look weak;
- adding a family that the system happens to distinguish well;
- removing a family that the system confuses;
- selecting a public demonstration case before primary evaluation is complete;
- treating a post-reveal exclusion as the primary result;
- tuning n-gram dimensions, thresholds, calibration, or abstention using Stage B outcomes.

A data-quality failure discovered before label reveal follows the frozen replacement/abort rule. A failure discovered after reveal remains in the primary result unless the preregistration explicitly required exclusion; any sensitivity analysis is secondary and cannot replace the original result.

## 7. Required execution order

### Phase 0 — Preparation only

- maintain `PRE-FREEZE`;
- prepare templates and custody infrastructure;
- do not create or inspect sealed Stage B labels;
- resolve issue #30 or archive an explicitly accepted equivalent reproducible-runner record.

### Phase 1 — Freeze candidate design

- resolve every scientific placeholder;
- define exact custody roles and access matrix;
- define source selection before corpus outcomes are visible;
- construct candidate manifests without exposing labels to prediction development.

### Phase 2 — Leakage and eligibility audit

- compare materialized Stage A and candidate Stage B manifests;
- require `sample_id_overlap = 0`;
- require `content_hash_overlap = 0`;
- apply the frozen prompt/lineage overlap policy;
- downgrade any ambiguous or exposed candidate to development-visible.

### Phase 3 — Research freeze and lock

- set `RESEARCH_FREEZE_001.md` to `FROZEN` only after all fields are resolved;
- preserve protocol SHA-256;
- generate final Research Lock 001 over the exact frozen file list;
- preserve repository commit and tree SHA;
- permit no scientific-impacting silent changes.

### Phase 4 — External preregistration

- submit the exact frozen packet;
- record registration ID/URL, UTC timestamp, visibility/embargo decision, protocol hash, commit SHA, and Research Lock Hash;
- verify that registered files and form values match the repository packet;
- keep Stage B execution unauthorized until the registration is accepted/timestamped.

### Phase 5 — Blind prediction

- expose only the blinded package to the prediction process;
- produce predictions once under the frozen state;
- freeze predictions and create the prediction-freeze receipt;
- no tuning or replacement after viewing predictions.

### Phase 6 — Reveal

- custodian verifies the prediction-freeze receipt;
- reveal the original unchanged label artifact;
- verify its preserved hash;
- create the reveal receipt.

### Phase 7 — Independent evaluation

- run the frozen evaluator without fitting or tuning;
- preserve all outputs and hashes;
- report the original primary result before sensitivity/exploratory analyses.

### Phase 8 — Publication and failure reporting

- publish positive, negative, and mixed results together;
- publish the `Where CogniPrint Fails` section;
- disclose all deviations and custody failures;
- keep claims within the registered language/domain/source scope.

## 8. Automatic abort or downgrade conditions

A Stage B run cannot be presented as the preregistered sealed result if any of the following occurs before prediction freeze:

- labels or hidden family mappings become accessible to the prediction process;
- target labels are encoded in visible metadata or paths;
- sample/content overlap with development evidence is non-zero;
- source selection is changed after inspecting predictions or labels;
- frozen software/configuration differs without an approved preregistered amendment;
- the custodian changes labels after predictions exist;
- the prediction artifact is not frozen and hashed before reveal;
- exact sample-ID sets cannot be reconciled;
- the external registration does not match the Research Lock state.

The affected run may be preserved as development evidence, but must be labelled `BLINDING_COMPROMISED` or `PROTOCOL_DEVIATION` and cannot unlock an attribution claim.

## 9. Amendment rule

After registration but before sealed predictions, an unavoidable scientific-impacting change requires:

1. a timestamped registration update/amendment that preserves the original record;
2. a new protocol and Research Lock version;
3. a statement of why the change was necessary and its expected effect;
4. confirmation that sealed predictions and labels were not inspected;
5. re-running all applicable eligibility/leakage gates.

After sealed predictions exist, a scientific-impacting change requires a new explicitly versioned challenge. It must not be edited into Challenge 001.

## 10. Current HOLD blockers

The packet must not be submitted while any of these remain unresolved:

- issue #30 lacks actual hosted-runner execution markers or a formally accepted equivalent record;
- exact Stage B source families/checkpoints/endpoints are not frozen;
- held-out unknown-family policy is not frozen;
- human-control definition is not frozen;
- sample and stratum counts are not frozen;
- minimum-evidence/length rule is not frozen;
- OOD/UNKNOWN method and thresholds are not frozen;
- calibration method, partition, ECE binning, and acceptance criteria are not frozen;
- exclusion criteria are not frozen;
- numeric stop/claim-narrowing criteria are not frozen;
- custodian identities/role IDs and storage/access separation are not frozen;
- candidate blinded and sealed manifests do not exist;
- real Stage A/B leakage audit has not passed;
- final protocol SHA and Research Lock Hash do not exist;
- external registration has not been timestamped.

## 11. Submission acceptance record

Only after successful external registration create a repository record containing:

- registration provider;
- registration ID and canonical URL;
- submitted/accepted UTC timestamps;
- public or embargoed status and end rule;
- exact registered title;
- contributor verification status;
- registered repository commit/tree SHA;
- protocol SHA-256;
- Research Lock Hash;
- custody-record hash;
- blinded-manifest hash;
- confirmation that no sealed predictions or label reveal occurred before registration.

Until that record exists, status remains:

```text
PREREGISTRATION = NOT_SUBMITTED
RESEARCH_FREEZE = PRE-FREEZE
STAGE_B = NOT_AUTHORISED_TO_START
```
