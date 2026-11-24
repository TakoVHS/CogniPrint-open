# TMLR Referee Audit v0.2 — Evidence-Bounded Promotion

Status: **REVIEWER-FACING PASS 2 / CORE FROZEN / APPLICATION-FIRST FRAMING**

This pass incorporates:

- review of the full public Zhu 2026 LaTeX source;
- an executed Stage A empirical anchor;
- no change to the mathematical core;
- no Stage B execution or authorization.

## Executive verdict

The manuscript remains mathematically coherent, but the novelty boundary is
narrower than in v0.1. Zhu 2026 directly covers target-relative proxy evidence,
compatible worlds/evidence fibers, no-promotion under missing target
directions, sharp envelopes, audit/refinement repair, counterworld realization,
and a frequentist interval/union-bound argument.

Therefore the manuscript should be evaluated as a **methodology/application
paper with an explicit runtime interface**, not as a new general certificate
theory.

The central reviewer question is now:

> Does the explicit multi-certificate, scope-first, fail-closed promotion
> interface teach ML practitioners something useful enough to justify a paper,
> given the strong prior art?

## R1 — "Mostly rediscovery of Zhu"

**Severity:** critical.

**Finding:** the risk is real and stronger than v0.1.

**Disposition:** ACCEPTED / FRAMING NARROWED.

The manuscript now explicitly states that Zhu already contains:

- target-relative proxy validation;
- a no-promotion rule;
- sharp target images/envelopes;
- audit/refinement repair;
- counterworld witnesses;
- \(1-\alpha\) interval coverage and a union-bound \(1-2\alpha\) result.

The paper no longer treats frequentist coverage itself as a Zhu distinction.

## R2 — "What actually remains?"

**Severity:** critical.

**Defensible remainder:** an explicit operational organization in which:

1. multiple certificates each name a target and validity world class;
2. deployment-scope coverage is checked conjunctively before numerical work;
3. feasibility is checked before a numeric sharp envelope exists;
4. empty/inconsistent cases fail closed to a nonnumeric status;
5. PROMOTE / ABSTAIN / UNRESOLVED are separated with reason codes;
6. marginal certificate failures are composed into a false-promotion budget;
7. the interface is instantiated on AI attribution.

**Boundary:** these are not claimed to be historically unique. They are the
specific organization/application this manuscript offers.

## R3 — "The theorem is elementary"

**Severity:** high but controlled.

The Canonical Least Warrant theorem remains intentionally framed as
canonicalization, not deep new mathematics. No change to the theorem is
required.

## R4 — "Why ML?"

**Severity:** high but improved.

The manuscript now ties the failure mode to benchmark metrics, calibration,
selective risk, OOD evaluation and downstream semantic claims. The AI
attribution application remains a concrete case rather than a generic safety
slogan.

## R5 — "The application is purely synthetic"

**Severity:** high; improved in this pass.

The manuscript now includes a development-only RAID anchor:

- 500 records;
- five source classes;
- four domains;
- lineage-grouped split;
- CogniPrint 12D nearest-centroid balanced accuracy: \(0.542001\);
- character 3--5 hashed TF--IDF balanced accuracy: \(0.590475\);
- word 1--2 hashed TF--IDF balanced accuracy: \(0.601996\).

Both n-gram baselines outperform the current 12D representation.

**Interpretation allowed:** this is a concrete executed example of why a
benchmark score should not be silently promoted to open-world attribution and
why weak evidence should narrow claims.

**Interpretation forbidden:** this is not a confirmatory attribution result, a
calibrated certificate, a Stage B result, or evidence that the formal theorem
is empirically "true".

## R6 — "Why not just partial identification?"

**Severity:** high.

The answer must remain operational rather than historical: partial
identification supplies compatible-model/sharp-bound machinery; this paper
turns the promotion boundary into an explicit ML audit interface that separates
certificate target, claim target, validity scope, feasibility, risk threshold
and confidence budget. The manuscript must not imply that classical partial
identification lacks assumptions, population restrictions, or decision theory.

## R7 — "Why is the scope check separate?"

**Severity:** moderate.

A silent intersection can remove unsupported deployment worlds and make a
bound look stronger than the original claim. The separate static coverage gate
prevents that shrinkage from being mistaken for evidence.

## R8 — "Empty compatible set means safety"

**Severity:** critical correctness risk; controlled.

The sharp numerical envelope remains partial on the feasible-bound domain.
Outside that domain, the runtime result is nonnumeric and cannot be compared
with the claim threshold.

## R9 — "The union bound is standard"

**Severity:** low once positioned correctly.

Accepted. The union-bound proposition is an operational soundness guarantee,
not a novelty claim. Zhu, aHL and Eris reinforce this boundary.

## R10 — "Practical computation may be impossible"

**Severity:** moderate.

The manuscript claims no generic efficient computation. Finite worlds can be
enumerated; structured problems may use certified conservative upper
approximations. A local optimizer without a certified upper bound is not a
promotion warrant.

## Current strongest points

- fail-closed semantics are precise;
- target and scope mismatches are explicit;
- empty-set behavior is safe;
- novelty boundaries are now unusually conservative;
- the Stage A anchor provides a real ML motivation without pretending to be
  confirmatory evidence;
- the paper remains compact.

## Current weakest points

- much of the semantic core has direct Zhu overlap;
- remaining value is organizational/application-driven rather than a strong new
  theorem;
- the Stage A anchor is deliberately weak evidence and cannot substitute for a
  real empirical evaluation;
- broader prior-art search may still find an even closer runtime-interface
  analogue;
- external mathematical/methodological review gate remains open.

## Referee-style recommendation

**Recommendation: revise as a methodology/application paper; do not submit yet.**

A plausible TMLR case remains if the paper is sold on reader learning and
operational auditability rather than mathematical priority. The next
acceptance-critical task is a targeted prior-art search for the exact
multi-certificate / deployment-scope / fail-closed interface, not creation of
new mathematics.
