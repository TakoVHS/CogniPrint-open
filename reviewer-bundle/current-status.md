# CogniPrint Reviewer Bundle — Current Status

## Public release state

```text
Release: v0.1.2
DOI: 10.5281/zenodo.20756421
Repository: https://github.com/TakoVHS/CogniPrint-open
Scientific readiness: descriptive_only
External methodological reviews: 0/1
```

## Gate state

The public source release, README, citation metadata, current-state summary, GitHub release, evidence ontology, Claim Firewall, evaluation contracts and reproducibility artifacts are available for inspection.

The Zenodo DOI `10.5281/zenodo.20756421` is now treated as a public citation identifier. This is an administrative/citation-metadata update only and does not change scientific readiness, validation state, or any research claim.

## Review state

No external methodological review has been completed. The counter remains `0/1`.

Prepared outreach, automated acknowledgements, funding correspondence, AI-generated responses and generic encouragement do not count as methodological review evidence.

## Implemented trust architecture

The repository now contains:

- `cogniprint-evidence-v1` with `OBSERVED / INFERRED / ATTESTED / UNKNOWN` truth classes;
- Claim Firewall v1 with attribution disabled by default until explicit evidence/calibration/OOD gates are satisfied;
- machine-readable limitation codes;
- a provenance-conflict classifier that does not silently choose a winner;
- deterministic `.cogcase` integrity/manifest primitives;
- Data Constitution and reference/benchmark governance;
- calibration/OOD/holdout evaluation contract;
- an independent sealed-prediction evaluator separated from model fitting;
- C2PA, Article 50 evidence-mapping and NIST AI RMF mapping documents with explicit non-certification boundaries.

These are **research/evidence controls**, not validation that source attribution works.

## Next-stage research state

The repository also includes infrastructure/protocols for:

- pinned external RAID model-family pilot;
- leakage-safe transparent baselines;
- Attribution Challenge 001;
- open-world/robustness and model-drift research;
- human–AI intervention research;
- provenance/evidence separation;
- QVAC local-evidence prototype;
- Autonomys Evidence Capsule prototype.

No completed RAID family-attribution result, Challenge 001 result, QVAC runtime PASS, Auto Drive CID round-trip, C2PA runtime validation, or digital `.cogcase` signature is currently claimed.

## What may change scientific status

The external-review counter may change only after a substantive independent methodological assessment from a qualified person/group is received and preserved with an appropriate permission boundary.

Scientific readiness may change only after dedicated empirical evidence, calibration/open-world evaluation, reproducibility evidence and review justify a stronger claim. Closing `0/1` alone does not change `descriptive_only`.

## Current next milestones

1. Execute truth/evaluator unit tests on a functioning runner (issue #30).
2. Externally preregister Attribution Challenge 001 before sealed Stage B evaluation (issue #28).
3. Execute Stage A / RAID pilot and preserve reproducible metrics.
4. Implement/validate the real C2PA bridge with fixtures and trust configuration (issue #26).
5. Add real detached `.cogcase` signatures only after cryptographic verification is implemented (issue #27).
6. Obtain one real external methodological critique.
7. Keep the DOI as citation metadata only; it does not alter scientific readiness.
8. Keep QVAC/Auto Drive grant tracks on their current evidence gates until their runtime/practitioner prerequisites close.
