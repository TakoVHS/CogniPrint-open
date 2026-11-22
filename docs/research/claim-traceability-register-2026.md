# CogniPrint claim-to-code traceability register

**Date:** 2026-11-05. **Purpose:** auditable public claims, reviewer evidence, and consistent site copy. This register describes repository evidence, **not** a certification or successful independent reproduction.

| Proposed public statement | Evidence | Permitted wording / limit |
| --- | --- | --- |
| Twelve deterministic text coordinates | `src/cogniprint/fingerprint.py`, `FEATURE_SPECS`, `feature_dict()` | Fixed-order descriptive profile. No source identity proof. |
| Fixed-bound normalization | `fingerprint.py`, `normalize_features()`; `analysis.py` `clip: False` | Not guaranteed to lie in [0,1] for arbitrary raw features. |
| Cosine, Euclidean, Manhattan, delta profile | `src/cogniprint/analysis.py`, `compare_profiles()` | Reproducible profile comparisons, not forensic attribution. |
| Typed evidence classes | `src/cogniprint/evidence_policy.py`, `EvidenceClass` | `OBSERVED/INFERRED/ATTESTED/UNKNOWN`; not an ordered lattice. |
| Admissibility policy | `evidence_policy.py`, `EvidenceContext`, `evaluate_claim()`; `tests/test_evidence_policy.py` | Code-gated claims based on explicitly supplied conditions, not automatically calibrated probabilities. |
| Restricted high-stakes claims | `evidence_policy.py`, `HIGH_STAKES_DENY` | Authorship, actor, intent and legal conclusions blocked by content-only analysis. |
| Provenance disagreement | `src/cogniprint/provenance_conflict.py`, `classify_conflict()` | Label-level conflict classification, not a formal global consistency proof. |
| Negative Stage A result | `docs/raid-ngram-baselines-m1.md`, Results; `docs/raid-pilot-m1.md` | 500 records; train/test 351/149; 12D Macro-F1 **0.535883** vs word TF-IDF **0.595220**. |
| Public research maturity | `docs/current-state-summary.md`, `docs/trust.md` | `descriptive_only`, Stage B not authorized, 0/1 external methodological reviews, CI execution status not confirmed. |
| Evidence-gated agent oversight | `docs/research/evidence-gated-oversight-protocol-2026.md` | **Proposed transfer hypothesis, not a completed oversight benchmark.** |

## Statements to reject in CVs, grant applications, and websites

- "CogniPrint proves who wrote text", "detects exact AI model", "solves calibrated oversight", or "100% traceability".
- "The four evidence classes form a validated mathematical lattice." They are categories in code.
- "UNKNOWN forbids all claims." Descriptive measurements can remain valid.
- "All normalized coordinates are clipped to [0,1]." Current code explicitly sets `clip: False`.
- "Macro-F1 0.525 versus TF-IDF 0.7." **Wrong for fixed RAID Pilot M1**; use exact published numbers.
- "Stage B complete", "externally reviewed", "cryptographically signed .cogcase", "C2PA-integrated production validation."
- "An Anthropic-endorsed project" or any implication of employment/sponsorship/partnership.

## Verification protocol

1. Verify the content of each linked source file at a known Git revision; preserve SHA, version and date.
2. Check that site copy uses the claim wording in this register.
3. Re-check baseline numbers against the pinned source hash and fixed-split report before publication.
4. Avoid public applicant contact details, unpublished personal documents, visa/immigration information, recommendation contacts or private work portfolios.
5. Any future capability upgrade requires a separately executed, reviewable benchmark and explicit claim-unlock decision—not merely a changed README.
