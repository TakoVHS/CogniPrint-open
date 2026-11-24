# Claim Promotion Research Roadmap — 24 November 2026

Status: **ACTIVE THEORY PROGRAMME / NOVELTY_UNESTABLISHED / NOT_SUBMITTED**

## Current state

- Draft PR: #84
- mathematical review gate: #85
- theory CI: PASS
- public release CI: PASS
- Stage B: NOT_AUTHORISED_TO_START
- scientific readiness: descriptive_only
- external mathematical review: 0/1
- first targeted mathematical-review email sent to Anastasios Angelopoulos
- no Zenodo/arXiv submission has been made for this theory track

## Corrected publication timing

The previous plan contained already-passed 2026 workshop deadlines.

### Closed / not actionable now

- NeurIPS 2026 ICBINB-BIO paper deadline: 2 September 2026 — CLOSED.
- ICML 2026 is already past.

### Confirmed upcoming opportunity

ICML 2027:
- submission opens: 8 January 2027;
- abstract deadline: 14 January 2027 (AoE);
- full paper deadline: 22 January 2027 (AoE);
- conference: 31 July–6 August 2027;
- workshops: 5–6 August 2027.

ICML 2027 workshop-specific submission deadlines are not frozen here until
official calls are published.

## 0–14 days

1. Preserve the current identifiability formulation.
2. Add counterexamples showing why a linear ClaimLevel ladder is wrong.
3. Keep the closed-channel non-transfer demonstration synthetic only.
4. Collect at least one independent mathematical response on:
   - identifiability;
   - Blackwell comparison;
   - relation to OOD impossibility;
   - whether the claim-admissibility formalism is already known.
5. Do not publish a novelty claim before this review.

Deliverable:
- theory draft v0.2;
- reviewer criticism/disposition log;
- literature collision map.

## 15–30 days

Formalize the candidate contribution above known identification theory.

Priority questions:

1. Can claim admissibility be defined as a partially ordered family of target
   functionals with certified promotion/non-promotion rules?
2. Can heterogeneous evidence certificates be composed without silently
   changing their target populations or loss functions?
3. Under what assumptions can a closed-set risk certificate and an
   open-world contamination certificate jointly authorize a stronger claim?
4. What is the sharp identified set for a claim when evidence channels are
   observationally insufficient?

Deliverable:
- one candidate theorem whose statement is not merely observational
  equivalence, Blackwell garbling, or generic OOD impossibility.

## 31–45 days

Prepare a 6–10 page private manuscript alpha.

Required sections:

1. problem and motivation;
2. prior art / collision map;
3. evidence-channel formalism;
4. observational-equivalence baseline theorem;
5. candidate genuinely new claim-admissibility result;
6. Blackwell/Le Cam interpretation;
7. synthetic demonstration;
8. limitations and non-claims.

Do not use the exposed RAID Stage A records as confirmatory evidence.

## 46–60 days

External critique.

Send at most a small number of targeted messages, one reviewer at a time.
Ask for counterexamples and prior art, not endorsement.

A negative critique counts if it is mathematically substantive.

## 61–75 days

Decide publication path.

Only proceed to a public preprint if:
- theorem statements survived review;
- novelty claims are supportable;
- proof assumptions are explicit;
- the manuscript does not imply Stage B authorization;
- all prior-art collisions are cited.

Possible public repository/DOI release may be considered at this point.
A DOI itself is not a scientific validation signal.

## 76–90 days

If the theory remains nontrivial, prepare a submission candidate.

ICML 2027 main/position-paper track is a stretch target only if the paper is
mathematically mature before the January 2027 deadlines.

Otherwise prefer a later 2027 workshop or journal route rather than rushing a
weak theorem.

## Long-run research identity

Working programme:

**Evidence-Bounded Statistical Inference**

Core principle:

> A valid certificate is evidence about its stated target; it is not a license
> to promote to a different claim unless that claim is identified by the
> available assumptions and evidence.

Recognition is an outcome of useful mathematics, external uptake, and
reproducible reasoning—not a release criterion.
