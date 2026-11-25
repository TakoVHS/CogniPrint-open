# AI Adversarial Review Disposition — 25 November 2026

Status: **INTERNAL AI RED-TEAM / DOES NOT SATISFY HUMAN REVIEW GATE**

Source reviewed by project owner: *CogniPrint — Adversarial Scientific Review
(PR #84)* against exact historical head
`14f029f9842f7d13d08f00550200488ca5a1de57`.

This review remains an AI red-team artifact. External human-review gate #85
remains `0/1`.

## Dispositions

### 1. Significance / methodological triviality
**Disposition:** `REQUIRES_NEW_EVIDENCE_OR_PROOF`.

The criticism is materially valid. The current manuscript is reframed as an
audit note and no longer presents elementary envelope/union-bound algebra as a
research-level mathematical result. Submission remains blocked until a
substantive human review and a real-data certificate-to-claim instantiation or
other nontrivial contribution exists.

### 2. Transport is load-bearing
**Disposition:** `ACCEPT` + `REQUIRES_NEW_EVIDENCE_OR_PROOF`.

The manuscript now states explicitly that the world index encodes both
validation and deployment quantities and that scope coverage is a transport
assumption. Pearl--Bareinboim transportability is cited. Practical use requires
either restricted deployment scope or an independently justified transport
bound.

### 3. No real certificate-to-claim data instantiation
**Disposition:** `ACCEPT` + `REQUIRES_NEW_EVIDENCE_OR_PROOF`.

The RAID pilot is now labelled development context, not an empirical validation
of the formal audit. No post-hoc Stage B-like analysis will be created from the
already exposed M2/M2.1 evaluation data.

### 4. Silent scope intersection in single-certificate code
**Disposition:** `ACCEPT`.

Fixed. Single-certificate compatible-world helpers now require full claim-scope
coverage. Regression tests include an uncovered unsafe world and check
single-certificate/heterogeneous-path agreement.

### 5. Sharp envelope was not shown to belong to the warrant class
**Disposition:** `ACCEPT`.

Fixed by defining a feasible-domain warrant
$h:\mathcal B_T\to[0,1]$, proving $r(D)\in\mathcal B_T$, proving
$s_T^\star$ is itself a warrant, and only then proving pointwise minimality.
The old v0.1 note is marked superseded.

### 6. Feasibility gate overstated as safety mechanism
**Disposition:** `ACCEPT`.

Reframed. Under a correctly specified deployment world and simultaneous
certificate validity, feasibility follows automatically. The explicit empty-set
branch is retained as an inconsistency/specification diagnostic and
implementation safeguard.

### 7. Common-domain notation / warrant scope redundancy
**Disposition:** `ACCEPT`.

After static coverage is established, the numerical compatible-world set is now
defined directly over $\mathcal W_c$. Warrant/certificate scopes remain in
the static coverage hypothesis rather than being carried redundantly through
the envelope.

### 8. Pre-specification and adaptive claim selection
**Disposition:** `ACCEPT`.

The soundness statement now assumes claim, certificate family, scopes,
tolerances, and warrant procedure are fixed before observing validation data.
A family-wise union-bound statement is given for predeclared multiple claims.

### 9. Missing RCPS / Learn-then-Test / Conformal Risk Control
**Disposition:** `ACCEPT`.

Added to bibliography and Related Work. The manuscript now treats these as
direct ML-native prior art and explicitly states that it proposes no competing
risk-control algorithm.

### 10. Near-uniform M2 probability quality omitted
**Disposition:** `ACCEPT`.

Reviewer-facing evidence now reports the four-class uniform references:
NLL $\log 4\approx1.386294$, Brier $0.75$, and states that observed M2
probability scores are only modestly better than an uninformative vector,
especially for 12D.

### 11. "Conformal empty sets were mathematically impossible"
**Disposition:** `PARTIALLY_ACCEPT`.

The empirical conclusion is accepted: the executed design produced zero
empty-set OOD rejections and mostly multi-label ambiguity. The stronger claim
of mathematical impossibility is not established by the review's argument;
misclassification does not imply every true-class calibration probability is
below $0.25$. Project wording therefore remains empirical and
design-specific, not a universal theorem.

### 12. M2.1 can contaminate future design
**Disposition:** `ACCEPT`.

The evidence documents now state that M2.1 may motivate hypotheses but cannot
set numeric Stage B temperatures, thresholds, coverage targets, or conformal
settings. Any future design must be prospective and use new evidence.

### 13. "External" rerun and "privacy-preserving" hashed n-gram language
**Disposition:** `ACCEPT`.

The rerun is now described as runner-isolated deterministic re-execution, not
independent replication. "Privacy-preserving" is replaced with
raw-text-non-persisting language and an explicit statement that feature hashing
is not a privacy guarantee.

### 14. Cognitive-provenance / fingerprint terminology
**Disposition:** `PARTIALLY_ACCEPT`.

Public top-level wording is narrowed to compact descriptive text-statistics
profiles and evidence-bounded claims. The project name remains CogniPrint, but
the README explicitly says the name is historical shorthand and not a claim of
unique fingerprint identity.

### 15. Bootstrap intervals are low-power
**Disposition:** `PARTIALLY_ACCEPT`.

The original no-pooled-inference conclusion remains correct. Reviewer-facing
text now states the per-fold intervals are low-power and the folds are not
independent replications.

### 16. Single-person Stage B custody
**Disposition:** `REQUIRES_NEW_EVIDENCE_OR_PROOF`.

Current Stage B remains unauthorized. A real sealed evaluation requires
independent custody/evaluation or an equivalently strong technical separation
that prevents the researcher from accessing labels before prediction freeze.

### 17. critical_unknown_fraction edge case
**Disposition:** `ACCEPT`.

When known acceptance is zero, unknown acceptance is positive, and
$\delta<1$, the accepted-population conditional risk is undefined at
$\pi=0$ and one for every $\pi>0$. The function now returns `None`
rather than the misleading numeric boundary `0.0`; regression tests cover it.

## Stage B disposition

The AI review's `ABANDON` recommendation is not adopted as an irreversible
scientific decision because the review is not independent human peer review.

The operational disposition is stricter than before:

**CURRENT 12D-CENTERED CHALLENGE 001 = HOLD / REDESIGN REQUIRED BEFORE ANY
FUTURE AUTHORIZATION.**

No Stage B execution or parameter freeze is permitted before substantive human
review and post-review design disposition.

## Submission disposition

**CLOSED.**

Correctness repairs do not solve the significance problem. The current paper is
not to be submitted merely because CI passes. Final TMLR acceptance review
remains downstream of human review and any required real-data or methodological
strengthening.
