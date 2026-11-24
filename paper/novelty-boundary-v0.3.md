# Novelty Boundary v0.3 — Evidence-Bounded Promotion

Status: **CONSERVATIVE / APPLICATION-FIRST / NO PRIORITY CLAIM**

Purpose: record the strongest defensible scientific positioning after the
reviewer-facing prior-art pass completed on 24 November 2026.

## What the manuscript must not claim as new

### Compatible worlds, identified sets, and sharp extrema

Partial-identification work already supplies identified/compatible model sets,
sharp extrema, confidence procedures, and decision-making under ambiguity.

Zhu (2026) directly formulates proxy validation with evidence-compatible
worlds/fibers and sharp target images/envelopes.

**Boundary:** compatible-world semantics and sharp envelopes are prior art.

### Proxy evidence does not automatically certify a broader target

Zhu explicitly gives a target-relative evidence-fiber formulation and a
no-promotion rule: a proxy certificate controls only target directions
identified by the declared evidence unless missing directions are covered by
additional evidence or an envelope.

**Boundary:** the broad target-mismatch/no-promotion insight is prior art.

### Counterworlds and evidence repair

Zhu gives executable counterworld realization, minimal audits, and
validation-sufficient refinements.

**Boundary:** counterworld witnesses and audit/refinement repair are prior art.

### Frequentist confidence and additive failure accounting

Zhu's theorem package contains a random interval certificate with
(1-\alpha) coverage and a union-bound (1-2\alpha) statement for two
indistinguishable worlds.

aHL provides union-bound program logic. Eris provides first-class error
credits.

**Boundary:** frequentist coverage, union bounds, and additive error budgets are
not contributions of CogniPrint.

### High-confidence safety tests and fail-closed refusal

The Seldonian framework supports multiple behavioral constraints
((g_i,\delta_i)), high-confidence safety tests, and a distinguished
`No Solution Found` result when constraints cannot be safely certified.

**Boundary:** multiple confidence-constrained obligations, a high-confidence
accept/reject safety test, and fail-closed refusal are prior art.

### Reject / abstain behavior

Selective classification has a long-standing reject-option literature and
formal risk/coverage trade-offs.

**Boundary:** abstention is not a new action introduced by CogniPrint.

### Assumptions, guarantees, and composition

Probabilistic assume/guarantee contracts already separate environmental
assumptions from system guarantees and study satisfaction, refinement, and
composition.

Assurance-case work already organizes claims, evidence, reasoning, and
defeaters.

**Boundary:** assumption/guarantee separation and generic evidence-to-claim
reasoning are prior art.

## Defensible remainder

The manuscript should be read as a **methodological interface and application**,
not a new general mathematical theory.

Its specific organization is:

1. each upstream statistical certificate explicitly names both a certified
   risk target and a world class on which its frequentist guarantee is valid;
2. a downstream semantic claim independently names its target risk and
   deployment world class;
3. conjunctive deployment-scope coverage is checked before numeric reasoning,
   so unsupported deployment worlds cannot disappear silently through an
   intersection;
4. realized certificate bounds define a separate feasibility problem;
5. the sharp claim-risk envelope is numeric only on the nonempty feasible
   domain; empty/inconsistent cases return a nonnumeric unresolved result;
6. runtime diagnostics distinguish scope failure, assumption inconsistency,
   realized-bound inconsistency, missing warrant computation, and ordinary
   threshold failure;
7. the interface is instantiated on AI attribution, where closed-set
   source-family evidence and open-world membership/provenance claims have
   different semantics;
8. an executed development-only RAID result illustrates why claim narrowing is
   operationally relevant even when benchmark evidence exists.

This exact organization was not found as the same explicit interface in the
reviewed Zhu source or in the Seldonian, selective-classification,
probabilistic-contract, probabilistic-program-logic, and assurance references
reviewed in this pass.

That sentence is an **audit observation**, not a historical priority claim.

## Stage A empirical boundary

The manuscript may report the executed development pilot:

- CogniPrint 12D balanced accuracy: (0.542001);
- character 3--5 hashed TF--IDF: (0.590475);
- word 1--2 hashed TF--IDF: (0.601996).

Both n-gram baselines outperform the 12D representation in the fixed pilot.

Allowed interpretation: concrete motivation for claim narrowing and for
separating benchmark evidence from open-world semantic claims.

Forbidden interpretation: confirmatory attribution performance, calibrated
confidence, Stage B evidence, provenance proof, or empirical validation of the
formal theorem.

## Submission-killing conditions

The current manuscript should be withheld or reframed if a closer prior-art
source is found that already combines, in substantially the same form:

- heterogeneous statistical certificates with separately declared validity
  scopes and targets;
- a distinct downstream semantic claim target/scope;
- an explicit static scope-coverage gate;
- a partial feasible-bound domain with nonnumeric failure semantics; and
- reason-coded certificate-to-claim promotion diagnostics.

Even if such a source is not found, the paper should still avoid words such as
`first`, `novel`, or `unique` for the interface without a substantially
broader literature review.

## Current recommended framing

**Primary framing:** ML methodology / audit interface.

**Mathematical role:** elementary canonicalization and soundness bookkeeping.

**Application:** AI attribution and provenance-claim discipline.

**Empirical role:** development-only negative/diagnostic anchor.

**Not claimed:** new probability theory, new partial-identification theory, new
type system, new abstention theory, new high-confidence safe-learning
framework, or new assume/guarantee calculus.

## Current decision

**PR #84: keep Draft.**

**Stage B: keep HOLD / NOT_AUTHORISED_TO_START.**

**Submission: HOLD** until the external review gate and final manuscript review
are complete.
