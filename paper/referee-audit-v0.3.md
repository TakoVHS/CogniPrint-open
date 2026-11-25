# TMLR Referee Audit v0.3 — Post-Adversarial-Review

Status: **CURRENT INTERNAL REFEREE PASS / SUBMISSION CLOSED**

This pass incorporates the 25 November 2026 AI adversarial review without
counting it toward the independent-human-review gate.

## What was actually wrong

### Code-level correctness defect — fixed

The single-certificate finite-world helpers silently intersected certificate
and claim scopes. An uncovered unsafe deployment world could disappear from the
calculation.

Disposition: **ACCEPT / FIXED**.

All single-certificate compatible-world helpers now require full claim-scope
coverage. Regression tests reproduce the uncovered-unsafe-world case.

### Least-warrant statement — fixed

The previous comparison class used full-domain warrants while the sharp
envelope was defined only on the feasible domain.

Disposition: **ACCEPT / FIXED**.

The current paper defines a feasible-domain warrant, proves the sharp envelope
belongs to that class, and proves minimality within that class.

### Feasibility role — corrected

The old wording could make the explicit empty-set branch sound like part of the
frequentist soundness proof.

Disposition: **ACCEPT / FIXED**.

Under simultaneous validity events, the true world makes the realized bound
vector feasible automatically. The empty-set branch is now a
misspecification/inconsistency diagnostic and implementation safeguard.

### Pre-specification — fixed

The fixed-claim soundness statement now says that claim, certificates, scopes,
tolerances, and warrant procedure are fixed before observing validation data.
A family-wise union-bound statement is added for multiple predeclared claims.

### Missing ML risk-control prior art — fixed

RCPS, Learn-then-Test, and Conformal Risk Control are now explicit direct prior
art. The paper states that it proposes no competing calibration/risk-control
algorithm.

## What remains scientifically weak

### Significance

The mathematics is elementary and cannot carry the paper by itself.

**Blocking.**

### Transport/scope

The coverage condition is load-bearing and is a transport assumption. The
paper now says this plainly, but a practical deployment claim still requires
evidence or a validated transport bound.

**Blocking for real deployment claims.**

### Real-data instantiation

The RAID Stage A paragraph is now labelled development context, not an
instantiation of the certificate-to-claim guarantee.

A publication-strength methodology paper still needs a real case where a
valid upstream certificate is available and the audit produces a non-obvious
PROMOTE/ABSTAIN/UNRESOLVED result.

**Blocking for current TMLR submission.**

### Stage A strength

The negative result remains useful as research discipline, but the probability
outputs are weak and OOD ranking is near chance. The current 12D representation
should not be promoted as an attribution feature set.

### Stage B

The present 12D-centered Challenge 001 design should not execute. Future work
requires human review and prospective redesign; exposed M2/M2.1 outcomes may
not set numeric parameters.

## Points where the AI review overreached

The review's statement that empty conformal sets were mathematically
"impossible" is stronger than its argument proves. With four classes, a
misclassified point can still assign more than (0.25) probability to the true
class, so low macro-F1 alone does not establish the claimed impossibility.

The defensible conclusion is empirical and design-specific: M2 produced zero
empty-set rejections, mostly ambiguous multi-label sets, and therefore did not
demonstrate OOD rejection.

The AI review's `ABANDON` recommendation is also not treated as an irreversible
gate decision. It is strong evidence against the current design, but the
project's hard gate requires substantive independent human review before final
scientific disposition.

## Current referee-style decision

**DO NOT SUBMIT CURRENT VERSION.**

Reason: correctness is repaired, but significance and real-data instantiation
remain unresolved.

The next legitimate transition is not cosmetic rewriting. It is:

`human review -> disposition -> prospective evidence/methodological
strengthening if required -> exact-head CI/PDF audit -> final TMLR acceptance
pass`.
