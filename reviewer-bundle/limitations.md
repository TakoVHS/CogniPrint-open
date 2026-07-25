# CogniPrint Reviewer Bundle — Limitations

## Current status

CogniPrint is `descriptive_only`.

External methodological reviews remain `0/1`.

The DOI reference `10.5281/zenodo.20756421` is not currently treated as directly verified through a public Zenodo record.

## Main limitations of the current descriptive core

1. The framework depends on the selected feature family.
2. Stability claims are conditional on explicit assumptions.
3. Public diagnostics are corpus-specific and exploratory.
4. The existing benchmark evidence is not sufficient to establish general classification performance.
5. No independent methodological review has been completed.
6. No independent replication has been completed.
7. The current lightweight tokenisation/readability features are not validated as language-neutral measurements.
8. Similarity in the current feature space is not evidence of common authorship, model identity, or common provenance.

## Limitations of the model-family research target

1. No completed external RAID empirical result is currently claimed.
2. Closed-set model-family discrimination, even if successful, would not establish open-world source identity.
3. Prompt, domain, decoding, length, training-data overlap, and model-version effects may create trivial or unstable signals.
4. Model updates can invalidate a learned fingerprint.
5. Paraphrasing, translation, substantial human editing, or another model can erase or replace observable signals.
6. Calibration and abstention are required before any source-family suggestion could be shown responsibly.
7. A useful negative result may be that current features do not retain source-family information beyond simple baselines.

## Limitations of human–AI intervention research

1. There is no current validated intervention-localisation output.
2. "Human intervention" is not a single naturally observable class; ground truth depends on controlled revision history and an explicit operational definition.
3. Sentence/span boundaries may not correspond to the true production process.
4. Human editing can imitate, remove, or introduce the same surface signals being measured.
5. A mixed-production label must not be converted into author identity, intent, or responsibility.

## Provenance limitations

1. Content-derived measurements are not authenticated provenance.
2. Hashes establish integrity relative to a known artifact but do not by themselves identify who created it.
3. Signed credentials or logs can be absent, incomplete, compromised, or limited to the assertions they actually contain.
4. Disagreement between content signals and declared provenance requires investigation; neither should be silently overwritten by the other.
5. A person or organisation that requested, commissioned, approved, or deployed a workflow cannot be inferred reliably from prose alone.

## Prototype limitations

The QVAC Local Evidence Node is currently a bounded integration prototype. Offline privacy/redaction tests exist, but no public QVAC SDK/model runtime PASS is claimed yet.

The local generative explanation is not scientific evidence and must not create conclusions stronger than the deterministic CogniPrint payload.

## Non-claims

CogniPrint does not currently establish:

- authorship or identity;
- a unique neural-model source;
- definitive AI origin;
- actor or commissioner identity;
- intent or responsibility;
- legal status;
- forensic provenance;
- universal classification;
- production readiness for high-stakes use;
- validated general accuracy.

## Reviewer request

Please identify any wording, theorem statement, empirical result, benchmark description, prototype description, or release note that could be interpreted as stronger than the current evidence supports.

Especially useful are explicit failure conditions: what result should force a research hypothesis to be abandoned or narrowed?

## Required preservation

Until evidence justifies a change, do not change:

```text
Scientific readiness: descriptive_only
External methodological reviews: 0/1
```

Closing the review counter alone is not sufficient to change scientific readiness.