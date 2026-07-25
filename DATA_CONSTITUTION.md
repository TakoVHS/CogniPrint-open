# CogniPrint Data Constitution

Status: **project-level data governance contract for research corpora, benchmarks and evidence artifacts.**

## 1. Purpose

CogniPrint should never accept a dataset merely because it improves a benchmark score. Data must have a documented origin, use right, provenance record and contamination boundary.

This constitution applies to:

- reference corpora;
- benchmark samples;
- generated samples;
- human controls;
- transformation/rewrite samples;
- external evidence fixtures;
- public case-library artifacts.

## 2. Allowed source categories

A dataset/sample may enter the public research pipeline only when at least one defensible basis exists, such as:

- a clearly compatible open licence;
- public-domain status that has been checked for the relevant jurisdiction/use;
- explicit permission/consent for the intended research release;
- a benchmark licence/terms permitting the intended use;
- synthetic material generated specifically for the experiment under documented provider/tool terms.

Ambiguous rights are a HOLD, not an implied permission.

## 3. Prohibited or restricted material

Do not include in a public benchmark by default:

- private messages or documents collected without permission;
- credentials, secrets, tokens or private URLs;
- personal contact data not necessary for the research purpose;
- sensitive case material from journalists, investigators or civil-society partners;
- content whose publication could expose a vulnerable source;
- material whose licence/terms prohibit the planned redistribution;
- arbitrary scraped data with unresolved provenance.

## 4. PII and sensitive-data minimisation

Research manifests should prefer:

- sample IDs instead of names;
- broad role/category labels instead of identities;
- content hashes instead of raw sensitive artifacts;
- synthetic or consented examples for public cases;
- local/zero-retention processing when source confidentiality matters.

If PII is unnecessary, it must not enter the corpus.

## 5. Dataset card requirement

Every benchmark/reference dataset must have a machine- or human-readable card recording at least:

- dataset name and version;
- source(s);
- licence/terms reference;
- collection/generation date or observation window;
- language(s);
- domain/task classes;
- generator/provider/family where known and allowed;
- claimed model/version/checkpoint where known;
- API/tool/version evidence where applicable;
- prompt family and generation configuration where known;
- transformation lineage;
- known limitations;
- redistribution boundary;
- dataset/manifest hash.

## 6. Benchmark contamination controls

The project must actively document risks that benchmark/test data leaked into:

- model training;
- prompt design;
- feature engineering;
- threshold tuning;
- reference registry construction;
- manual error analysis before the sealed evaluation was frozen.

Sealed challenge labels must not be available to the classifier/evaluator until prediction artifacts are frozen and hashed.

## 7. Lineage and transformation provenance

Derived samples must record parent/child lineage.

Examples:

- translation;
- human editing;
- model-to-model rewrite;
- paraphrase;
- mixed production chain.

Parent and derived samples must be grouped to prevent train/test leakage when the experiment requires independent evaluation.

## 8. Human controls

Human-control data requires the same provenance and licensing discipline as model-generated data.

Do not label a text as "human" merely because no AI provenance is known. Human controls should have a documented acquisition category and inclusion protocol.

## 9. Reference registry discipline

Reference examples must not be stored as timeless evidence of a model identity.

Each reference distribution should record:

- source/provider/family;
- model/version claim where known;
- observation period;
- collection method;
- generation configuration;
- feature-space version;
- dataset version/hash;
- drift/expiry assumptions.

See `docs/fingerprint-registry-v0.1.md`.

## 10. Deletion and withdrawal

If material must be removed for rights, privacy, safety or provenance reasons:

1. remove it from future public bundles/registries;
2. preserve a non-sensitive audit record that a dataset revision changed;
3. increment the affected dataset/reference version;
4. invalidate or flag dependent benchmark results where necessary;
5. do not silently pretend earlier results used the new corpus.

Immutable third-party storage may prevent physical deletion of already published artifacts; therefore minimisation must happen **before** permanent publication.

## 11. Evidence artifacts

Public evidence should prefer derived, bounded artifacts:

- hashes;
- numeric features;
- configuration/version metadata;
- calibrated result records;
- limitations;
- provenance validation states.

Raw sensitive source material should not be embedded in Evidence Capsules or public `.cogcase` examples by default.

## 12. Reproducibility

Where possible, every result should bind:

- code commit;
- dataset/manifest hash;
- configuration hash;
- environment/container identifier;
- feature-space version;
- reference-registry version;
- calibration-model version;
- prediction/label hashes for blind evaluations.

## 13. Data-governance failure rule

If provenance, rights or contamination status cannot be determined sufficiently for the intended public use, the sample/dataset is **UNKNOWN / HOLD** and must not be promoted into the public benchmark merely to increase scale.
