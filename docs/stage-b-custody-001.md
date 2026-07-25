# Challenge 001 — Stage B Custody Contract

Status: `PRE-FREEZE CONTRACT / NO STAGE B DATA EXISTS YET`

Purpose: define the minimum custody and exposure rules required for a dataset to qualify as **sealed Stage B** evidence in Attribution Challenge 001.

This contract is stricter than merely keeping a `labels.jsonl` file out of the prediction command. A corpus is not meaningfully blind if the people/processes selecting inference rules have already inspected the labels or tuned against the examples.

## 1. Eligibility rule

A candidate Stage B source/sample is eligible only if all of the following are true:

- it is not listed in the Development Exposure Registry;
- its content hash and sample ID do not overlap any materialised Stage A record;
- it has not been used for feature design, threshold selection, calibration, OOD design, debugging, evaluator changes or demo cherry-picking;
- its ground-truth source family/control label has not been inspected by the prediction-rule development process;
- its selection procedure was fixed before sealed predictions;
- its lineage/provenance is sufficient to create a separate hidden ground-truth record;
- licensing/API/provider terms permit the planned research use and evidence retention.

When prior exposure is ambiguous, classify the sample as **development-visible** and exclude it from Stage B.

## 2. Preferred Stage B construction

For Challenge 001, the strongest practical design is a **dedicated corpus collected/generated under the frozen protocol**, rather than re-labelling an already explored public benchmark as “sealed”.

The frozen protocol must define before Stage B collection/evaluation:

- source/model families and human controls;
- held-out unknown family/families;
- endpoint/checkpoint/version evidence where available;
- prompt/task/domain/language strata;
- generation/configuration rules where exposed;
- sample counts and lineage rules;
- minimum-evidence and exclusion rules;
- calibration/reference membership policy;
- transformation tracks included in primary versus exploratory analysis.

No source family may be added or removed after sealed predictions are produced.

## 3. Two-artifact rule

Stage B must be represented by two logically and physically separate artifacts.

### A. Blinded evaluation package

May be exposed to the prediction process. It contains only fields permitted by:

`schemas/challenge-001-blinded-sample-v1.schema.json`

It must not contain direct or trivial label leakage, including:

- `true_class`;
- `known_to_reference`;
- generator/model-family ground truth;
- label-bearing filenames/directories;
- provider/model names in predictor-visible metadata when those names are the target class;
- any convenience field that trivially reconstructs the hidden label.

### B. Sealed ground-truth package

Uses the revealed-label schema but is **not exposed to the prediction process before prediction freeze**.

Before reveal, this package must not be committed to the public CogniPrint repository, included in CI artifacts visible to the prediction workflow, mounted into the prediction job, or stored beside blinded inputs under an obvious label-bearing path.

The sealed-label artifact may be held by an independent custodian or in a logically separate private/offline location. The custody method must be documented at freeze.

## 4. Custodian boundary

The freeze must identify at least two logical roles, even if automation performs one of them:

### Corpus/label custodian

Permitted to create or preserve ground truth.

Must not:

- tune CogniPrint thresholds/features/calibration against sealed labels;
- reveal labels before the prediction artifact is frozen;
- alter labels in response to observed predictions.

### Prediction process

Permitted to access:

- frozen reference/calibration material explicitly allowed by protocol;
- blinded Stage B inputs;
- frozen software/configuration.

Must not access:

- sealed ground-truth labels;
- hidden source-family metadata;
- label-bearing source paths or provider metadata prohibited by the frozen protocol.

If one human performs both administrative roles, the technical process must still prevent the prediction job from receiving the sealed labels, and any manual label exposure before prediction freeze must be disclosed as a blinding failure.

## 5. Label-artifact integrity

At creation, the custodian should preserve the exact sealed-label file bytes and its SHA-256 in the custody record.

The hash is an **integrity identifier**, not a secrecy mechanism. The secrecy boundary comes from custody/access separation, not from hashing a low-entropy label value.

Do not publish per-sample hashes as a substitute for secrecy when the class space is small enough to brute-force.

At reveal:

1. preserve/freeze `predictions.jsonl` and its SHA-256;
2. record the Research Lock Hash and exact software/config state;
3. reveal the original sealed-label artifact without modification;
4. verify its preserved SHA-256;
5. evaluate without fitting/tuning;
6. retain both original prediction and label artifacts in the evidence package.

## 6. Development Exposure Registry rule

Any Stage B candidate becomes Stage A/development-visible if, before prediction freeze:

- labels are inspected during debugging or method design;
- examples are selected because they produce favorable/unfavorable outcomes used to change the method;
- the sample is added to training/reference/calibration data;
- prediction thresholds are changed after examining its source identity;
- the sample is used to choose a public demo/highlight case;
- leakage is discovered and the sample is manually reclassified after seeing predictions.

Such a sample is not “bad data”; it simply loses sealed-evaluation eligibility for Challenge 001.

## 7. Leakage Audit gate

Before `RESEARCH_FREEZE_001.md` may move to `FROZEN`, materialised Stage A and candidate Stage B manifests must be checked with:

`scripts/check_challenge_leakage.py`

Minimum required result:

```text
freeze_gate = PASS
sample_id_overlap = 0
content_hash_overlap = 0
```

Prompt-hash overlap is reported separately and must follow the policy frozen in the protocol.

Any sample/content overlap blocks freeze. Do not silently exclude overlapping rows after sealed evaluation.

## 8. Public-dataset warning

A public labelled benchmark can be useful for Stage A, replication or external comparison, but public availability weakens claims of human blinding if the researcher can freely inspect the labels.

Using a public source for Stage B therefore requires a stronger custody design, such as an independent custodian who selects/remaps the sealed subset and withholds the label mapping until prediction freeze. Merely promising not to look at a public label column is weaker evidence than a dedicated or independently custodied blind corpus.

For Challenge 001, already exposed `public-benchmark-v1.1` and the documented RAID `raid/train` Pilot A matrix are explicitly development-visible and are not eligible as sealed Stage B evidence.

## 9. Reveal failure conditions

The primary Stage B blind claim is compromised and must be reported as such if any of the following occurs before prediction freeze:

- sealed labels become accessible to the prediction process;
- target labels are encoded in predictor-visible paths/metadata;
- source identities are manually inspected and then used to alter inference rules;
- Stage A/Stage B sample or content overlap is non-zero;
- the sealed-label file is modified after predictions are observed without preserving/reporting the original;
- the source/selection protocol is changed after inspecting Stage B outcomes.

A compromised blind run may remain useful as development evidence, but it must not be presented as the preregistered sealed Challenge 001 result.

## 10. Current state

- actual Stage B source set: `TO BE FROZEN`;
- actual source/model families: `TO BE FROZEN`;
- held-out unknown family/families: `TO BE FROZEN`;
- sample counts/strata: `TO BE FROZEN`;
- label custodian/custody location: `TO BE FROZEN`;
- candidate Stage B blinded manifest: `NOT CREATED`;
- sealed-label artifact: `NOT CREATED`;
- real Stage A/B Leakage Audit: `NOT EXECUTED`;
- Stage B execution: `NOT AUTHORISED TO START`.
